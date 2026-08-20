const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');

// Isolated DB file per test run so tests never touch real data.
const tmpDb = path.join(os.tmpdir(), `audit-board-test-${Date.now()}-${Math.random().toString(36).slice(2)}.json`);
process.env.DB_PATH = tmpDb;

const request = require('supertest');
const { createApp } = require('../server/index');

const { app } = createApp();

test.after(() => {
  if (fs.existsSync(tmpDb)) fs.unlinkSync(tmpDb);
});

async function createWorkspace(overrides = {}) {
  const res = await request(app)
    .post('/api/workspaces')
    .send(Object.assign({ name: 'INPP Hotel Audit', ownerName: 'Henry Jonan', ownerEmail: 'henry.jonan@gmail.com' }, overrides));
  assert.equal(res.status, 201);
  return res.body; // { workspace, memberId }
}

test('creating a workspace makes the creator the active owner', async () => {
  const { workspace, memberId } = await createWorkspace();
  assert.equal(workspace.members.length, 1);
  assert.equal(workspace.members[0].role, 'owner');
  assert.equal(workspace.members[0].status, 'active');
  assert.equal(workspace.members[0].id, memberId);
});

test('creating a workspace without a name or email fails', async () => {
  const res = await request(app).post('/api/workspaces').send({ name: '' });
  assert.equal(res.status, 400);
});

test('non-members cannot read a workspace', async () => {
  const { workspace } = await createWorkspace();
  const res = await request(app).get(`/api/workspaces/${workspace.id}`);
  assert.equal(res.status, 403);
});

test('owner can invite a member by email, and that email can join', async () => {
  const { workspace, memberId } = await createWorkspace();
  const inviteRes = await request(app)
    .post(`/api/workspaces/${workspace.id}/members`)
    .set('x-member-id', memberId)
    .send({ email: 'auditor2@company.com' });
  assert.equal(inviteRes.status, 201);
  const invited = inviteRes.body.members.find((m) => m.email === 'auditor2@company.com');
  assert.equal(invited.status, 'invited');

  const joinRes = await request(app)
    .post(`/api/workspaces/${workspace.id}/join`)
    .send({ email: 'AUDITOR2@company.com', name: 'Second Auditor' });
  assert.equal(joinRes.status, 200);
  assert.ok(joinRes.body.memberId);

  const readRes = await request(app)
    .get(`/api/workspaces/${workspace.id}`)
    .set('x-member-id', joinRes.body.memberId);
  assert.equal(readRes.status, 200);
  const member = readRes.body.members.find((m) => m.email === 'auditor2@company.com');
  assert.equal(member.status, 'active');
  assert.equal(member.name, 'Second Auditor');
});

test('an uninvited email cannot join the workspace', async () => {
  const { workspace } = await createWorkspace();
  const res = await request(app)
    .post(`/api/workspaces/${workspace.id}/join`)
    .send({ email: 'stranger@company.com', name: 'Nobody' });
  assert.equal(res.status, 403);
});

test('only the owner can invite members', async () => {
  const { workspace, memberId: ownerId } = await createWorkspace();
  await request(app).post(`/api/workspaces/${workspace.id}/members`).set('x-member-id', ownerId).send({ email: 'member@company.com' });
  const joinRes = await request(app).post(`/api/workspaces/${workspace.id}/join`).send({ email: 'member@company.com', name: 'Member' });

  const res = await request(app)
    .post(`/api/workspaces/${workspace.id}/members`)
    .set('x-member-id', joinRes.body.memberId)
    .send({ email: 'someoneelse@company.com' });
  assert.equal(res.status, 403);
});

test('inviting the same email twice is rejected', async () => {
  const { workspace, memberId } = await createWorkspace();
  await request(app).post(`/api/workspaces/${workspace.id}/members`).set('x-member-id', memberId).send({ email: 'dup@company.com' });
  const res = await request(app).post(`/api/workspaces/${workspace.id}/members`).set('x-member-id', memberId).send({ email: 'dup@company.com' });
  assert.equal(res.status, 409);
});

test('owner cannot be removed, but a regular member can be', async () => {
  const { workspace, memberId: ownerId } = await createWorkspace();
  await request(app).post(`/api/workspaces/${workspace.id}/members`).set('x-member-id', ownerId).send({ email: 'member@company.com' });
  const joinRes = await request(app).post(`/api/workspaces/${workspace.id}/join`).send({ email: 'member@company.com', name: 'Member' });

  const removeOwner = await request(app).delete(`/api/workspaces/${workspace.id}/members/${ownerId}`).set('x-member-id', ownerId);
  assert.equal(removeOwner.status, 400);

  const removeMember = await request(app)
    .delete(`/api/workspaces/${workspace.id}/members/${joinRes.body.memberId}`)
    .set('x-member-id', ownerId);
  assert.equal(removeMember.status, 200);
  assert.equal(removeMember.body.members.find((m) => m.email === 'member@company.com'), undefined);
});

test('any active member can create, edit, and delete tasks', async () => {
  const { workspace, memberId: ownerId } = await createWorkspace();
  await request(app).post(`/api/workspaces/${workspace.id}/members`).set('x-member-id', ownerId).send({ email: 'member@company.com' });
  const joinRes = await request(app).post(`/api/workspaces/${workspace.id}/join`).send({ email: 'member@company.com', name: 'Member' });
  const memberId = joinRes.body.memberId;

  const createRes = await request(app)
    .post(`/api/workspaces/${workspace.id}/tasks`)
    .set('x-member-id', memberId)
    .send({ title: 'Reconcile hotel occupancy report', status: 'todo', priority: 'high' });
  assert.equal(createRes.status, 201);
  const task = createRes.body.tasks.find((t) => t.title === 'Reconcile hotel occupancy report');
  assert.ok(task);
  assert.equal(task.status, 'todo');
  assert.equal(task.priority, 'high');
  assert.equal(task.createdBy, memberId);

  const updateRes = await request(app)
    .patch(`/api/workspaces/${workspace.id}/tasks/${task.id}`)
    .set('x-member-id', ownerId)
    .send({ status: 'in_review', checklist: [{ text: 'Match ACL export vs PMS', done: true }] });
  assert.equal(updateRes.status, 200);
  const updated = updateRes.body.tasks.find((t) => t.id === task.id);
  assert.equal(updated.status, 'in_review');
  assert.equal(updated.checklist[0].done, true);

  const deleteRes = await request(app)
    .delete(`/api/workspaces/${workspace.id}/tasks/${task.id}`)
    .set('x-member-id', memberId);
  assert.equal(deleteRes.status, 200);
  assert.equal(deleteRes.body.tasks.find((t) => t.id === task.id), undefined);
});

test('a non-member cannot create tasks', async () => {
  const { workspace } = await createWorkspace();
  const res = await request(app)
    .post(`/api/workspaces/${workspace.id}/tasks`)
    .set('x-member-id', 'not-a-real-member-id')
    .send({ title: 'Should fail' });
  assert.equal(res.status, 403);
});

test('creating a task without a title fails', async () => {
  const { workspace, memberId } = await createWorkspace();
  const res = await request(app)
    .post(`/api/workspaces/${workspace.id}/tasks`)
    .set('x-member-id', memberId)
    .send({ title: '   ' });
  assert.equal(res.status, 400);
});

test('updating a task with an invalid status is rejected', async () => {
  const { workspace, memberId } = await createWorkspace();
  const createRes = await request(app)
    .post(`/api/workspaces/${workspace.id}/tasks`)
    .set('x-member-id', memberId)
    .send({ title: 'Check AR aging' });
  const task = createRes.body.tasks[0];
  const res = await request(app)
    .patch(`/api/workspaces/${workspace.id}/tasks/${task.id}`)
    .set('x-member-id', memberId)
    .send({ status: 'not_a_status' });
  assert.equal(res.status, 400);
});

test('comments can be added to a task and record the author', async () => {
  const { workspace, memberId } = await createWorkspace();
  const createRes = await request(app)
    .post(`/api/workspaces/${workspace.id}/tasks`)
    .set('x-member-id', memberId)
    .send({ title: 'Verify voucher sequence gaps' });
  const task = createRes.body.tasks[0];

  const commentRes = await request(app)
    .post(`/api/workspaces/${workspace.id}/tasks/${task.id}/comments`)
    .set('x-member-id', memberId)
    .send({ text: 'Found 3 gaps in voucher #4500-4600' });
  assert.equal(commentRes.status, 201);
  const updatedTask = commentRes.body.tasks.find((t) => t.id === task.id);
  assert.equal(updatedTask.comments.length, 1);
  assert.equal(updatedTask.comments[0].author, 'Henry Jonan');
  assert.equal(updatedTask.comments[0].text, 'Found 3 gaps in voucher #4500-4600');
});

test('acting on a task in a workspace that does not exist returns 403 (unknown member)', async () => {
  const res = await request(app)
    .post('/api/workspaces/does-not-exist/tasks')
    .set('x-member-id', 'whoever')
    .send({ title: 'x' });
  assert.equal(res.status, 403);
});
