const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const low = require('lowdb');
const FileSync = require('lowdb/adapters/FileSync');

const DB_PATH = process.env.DB_PATH || path.join(__dirname, '..', 'data', 'db.json');
fs.mkdirSync(path.dirname(DB_PATH), { recursive: true });
const adapter = new FileSync(DB_PATH);
const db = low(adapter);

db.defaults({ workspaces: [] }).write();

const STATUSES = ['backlog', 'todo', 'in_progress', 'in_review', 'done'];
const PRIORITIES = ['low', 'medium', 'high'];

function normalizeEmail(email) {
  return String(email || '').trim().toLowerCase();
}

function initials(name, email) {
  const source = (name || email || '?').trim();
  const parts = source.split(/\s+/).filter(Boolean);
  if (parts.length === 0) return '?';
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
  return (parts[0][0] + parts[1][0]).toUpperCase();
}

function toPublicWorkspace(ws) {
  if (!ws) return null;
  return {
    id: ws.id,
    name: ws.name,
    createdAt: ws.createdAt,
    members: ws.members.map((m) => ({
      id: m.id,
      name: m.name,
      email: m.email,
      role: m.role,
      status: m.status,
      initials: m.initials,
    })),
    tasks: ws.tasks,
  };
}

function createWorkspace({ name, ownerName, ownerEmail }) {
  const email = normalizeEmail(ownerEmail);
  if (!name || !email) {
    throw Object.assign(new Error('name and ownerEmail are required'), { status: 400 });
  }
  const id = crypto.randomUUID();
  const ownerId = crypto.randomUUID();
  const ws = {
    id,
    name,
    createdAt: new Date().toISOString(),
    members: [
      {
        id: ownerId,
        name: ownerName || email,
        email,
        role: 'owner',
        status: 'active',
        initials: initials(ownerName, email),
      },
    ],
    tasks: [],
  };
  db.get('workspaces').push(ws).write();
  return { workspace: toPublicWorkspace(ws), memberId: ownerId };
}

function getWorkspaceRaw(workspaceId) {
  return db.get('workspaces').find({ id: workspaceId }).value();
}

function getWorkspace(workspaceId) {
  return toPublicWorkspace(getWorkspaceRaw(workspaceId));
}

function findMember(workspaceId, memberId) {
  const ws = getWorkspaceRaw(workspaceId);
  if (!ws) return null;
  return ws.members.find((m) => m.id === memberId && m.status === 'active') || null;
}

function inviteMember(workspaceId, requesterId, email) {
  const ws = getWorkspaceRaw(workspaceId);
  if (!ws) throw Object.assign(new Error('Workspace not found'), { status: 404 });
  const requester = ws.members.find((m) => m.id === requesterId && m.status === 'active');
  if (!requester || requester.role !== 'owner') {
    throw Object.assign(new Error('Only the owner can invite members'), { status: 403 });
  }
  const normalized = normalizeEmail(email);
  if (!normalized || !normalized.includes('@')) {
    throw Object.assign(new Error('A valid email is required'), { status: 400 });
  }
  if (ws.members.some((m) => m.email === normalized)) {
    throw Object.assign(new Error('That email is already a member'), { status: 409 });
  }
  const invited = {
    id: crypto.randomUUID(),
    name: '',
    email: normalized,
    role: 'member',
    status: 'invited',
    initials: initials('', normalized),
  };
  ws.members.push(invited);
  db.get('workspaces').find({ id: workspaceId }).assign(ws).write();
  return toPublicWorkspace(ws);
}

function joinWorkspace(workspaceId, email, name) {
  const ws = getWorkspaceRaw(workspaceId);
  if (!ws) throw Object.assign(new Error('Workspace not found'), { status: 404 });
  const normalized = normalizeEmail(email);
  const member = ws.members.find((m) => m.email === normalized);
  if (!member) {
    throw Object.assign(new Error('This email has not been invited to this workspace'), { status: 403 });
  }
  member.status = 'active';
  if (name) member.name = name;
  member.initials = initials(member.name, member.email);
  db.get('workspaces').find({ id: workspaceId }).assign(ws).write();
  return { workspace: toPublicWorkspace(ws), memberId: member.id };
}

function removeMember(workspaceId, requesterId, memberId) {
  const ws = getWorkspaceRaw(workspaceId);
  if (!ws) throw Object.assign(new Error('Workspace not found'), { status: 404 });
  const requester = ws.members.find((m) => m.id === requesterId && m.status === 'active');
  if (!requester || requester.role !== 'owner') {
    throw Object.assign(new Error('Only the owner can remove members'), { status: 403 });
  }
  const target = ws.members.find((m) => m.id === memberId);
  if (!target) throw Object.assign(new Error('Member not found'), { status: 404 });
  if (target.role === 'owner') {
    throw Object.assign(new Error('Cannot remove the workspace owner'), { status: 400 });
  }
  ws.members = ws.members.filter((m) => m.id !== memberId);
  db.get('workspaces').find({ id: workspaceId }).assign(ws).write();
  return toPublicWorkspace(ws);
}

function createTask(workspaceId, requesterId, data) {
  const ws = getWorkspaceRaw(workspaceId);
  if (!ws) throw Object.assign(new Error('Workspace not found'), { status: 404 });
  const requester = ws.members.find((m) => m.id === requesterId && m.status === 'active');
  if (!requester) throw Object.assign(new Error('Not a member of this workspace'), { status: 403 });

  const title = String(data.title || '').trim();
  if (!title) throw Object.assign(new Error('Title is required'), { status: 400 });

  const status = STATUSES.includes(data.status) ? data.status : 'backlog';
  const priority = PRIORITIES.includes(data.priority) ? data.priority : 'medium';

  const task = {
    id: crypto.randomUUID(),
    title,
    description: String(data.description || ''),
    status,
    priority,
    assignee: String(data.assignee || ''),
    dueDate: data.dueDate || null,
    labels: Array.isArray(data.labels) ? data.labels.filter(Boolean).map(String) : [],
    checklist: Array.isArray(data.checklist)
      ? data.checklist.map((c) => ({ text: String(c.text || c), done: !!(c && c.done) }))
      : [],
    comments: [],
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    createdBy: requester.id,
  };
  ws.tasks.push(task);
  db.get('workspaces').find({ id: workspaceId }).assign(ws).write();
  return toPublicWorkspace(ws);
}

const EDITABLE_TASK_FIELDS = [
  'title',
  'description',
  'status',
  'priority',
  'assignee',
  'dueDate',
  'labels',
  'checklist',
];

function updateTask(workspaceId, requesterId, taskId, patch) {
  const ws = getWorkspaceRaw(workspaceId);
  if (!ws) throw Object.assign(new Error('Workspace not found'), { status: 404 });
  const requester = ws.members.find((m) => m.id === requesterId && m.status === 'active');
  if (!requester) throw Object.assign(new Error('Not a member of this workspace'), { status: 403 });

  const task = ws.tasks.find((t) => t.id === taskId);
  if (!task) throw Object.assign(new Error('Task not found'), { status: 404 });

  if (patch.status !== undefined && !STATUSES.includes(patch.status)) {
    throw Object.assign(new Error('Invalid status'), { status: 400 });
  }
  if (patch.priority !== undefined && !PRIORITIES.includes(patch.priority)) {
    throw Object.assign(new Error('Invalid priority'), { status: 400 });
  }
  if (patch.title !== undefined && !String(patch.title).trim()) {
    throw Object.assign(new Error('Title cannot be empty'), { status: 400 });
  }

  for (const field of EDITABLE_TASK_FIELDS) {
    if (patch[field] !== undefined) task[field] = patch[field];
  }
  task.updatedAt = new Date().toISOString();
  db.get('workspaces').find({ id: workspaceId }).assign(ws).write();
  return toPublicWorkspace(ws);
}

function addComment(workspaceId, requesterId, taskId, text) {
  const ws = getWorkspaceRaw(workspaceId);
  if (!ws) throw Object.assign(new Error('Workspace not found'), { status: 404 });
  const requester = ws.members.find((m) => m.id === requesterId && m.status === 'active');
  if (!requester) throw Object.assign(new Error('Not a member of this workspace'), { status: 403 });
  const task = ws.tasks.find((t) => t.id === taskId);
  if (!task) throw Object.assign(new Error('Task not found'), { status: 404 });
  const body = String(text || '').trim();
  if (!body) throw Object.assign(new Error('Comment text is required'), { status: 400 });
  task.comments.push({
    author: requester.name || requester.email,
    text: body,
    createdAt: new Date().toISOString(),
  });
  task.updatedAt = new Date().toISOString();
  db.get('workspaces').find({ id: workspaceId }).assign(ws).write();
  return toPublicWorkspace(ws);
}

function deleteTask(workspaceId, requesterId, taskId) {
  const ws = getWorkspaceRaw(workspaceId);
  if (!ws) throw Object.assign(new Error('Workspace not found'), { status: 404 });
  const requester = ws.members.find((m) => m.id === requesterId && m.status === 'active');
  if (!requester) throw Object.assign(new Error('Not a member of this workspace'), { status: 403 });
  const exists = ws.tasks.some((t) => t.id === taskId);
  if (!exists) throw Object.assign(new Error('Task not found'), { status: 404 });
  ws.tasks = ws.tasks.filter((t) => t.id !== taskId);
  db.get('workspaces').find({ id: workspaceId }).assign(ws).write();
  return toPublicWorkspace(ws);
}

module.exports = {
  STATUSES,
  PRIORITIES,
  createWorkspace,
  getWorkspace,
  findMember,
  inviteMember,
  joinWorkspace,
  removeMember,
  createTask,
  updateTask,
  addComment,
  deleteTask,
};
