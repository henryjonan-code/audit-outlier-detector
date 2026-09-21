(() => {
  'use strict';

  const STATUS_META = [
    { key: 'backlog', label: 'Backlog' },
    { key: 'todo', label: 'To Do' },
    { key: 'in_progress', label: 'In Progress' },
    { key: 'in_review', label: 'In Review' },
    { key: 'done', label: 'Done' },
  ];
  const PRIORITIES = ['low', 'medium', 'high'];
  const SESSION_KEY = 'audit-board-session';

  const app = document.getElementById('app');
  app.innerHTML = '<div id="page"></div><div id="modal-root"></div><div id="toast-root"></div>';
  const pageEl = document.getElementById('page');
  const modalRoot = document.getElementById('modal-root');
  const toastRoot = document.getElementById('toast-root');

  const state = {
    session: loadSession(),
    workspace: null,
    activeTab: 'board',
    search: '',
    priorityFilter: 'all',
    socket: null,
    connected: false,
  };

  let draft = null; // modal working copy
  let modalMode = null; // 'create' | 'edit' | null

  function loadSession() {
    try {
      return JSON.parse(localStorage.getItem(SESSION_KEY) || 'null');
    } catch {
      return null;
    }
  }
  function saveSession(session) {
    state.session = session;
    localStorage.setItem(SESSION_KEY, JSON.stringify(session));
  }
  function clearSession() {
    state.session = null;
    localStorage.removeItem(SESSION_KEY);
  }

  function escapeHtml(str) {
    return String(str ?? '').replace(/[&<>"']/g, (c) => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
    }[c]));
  }

  function toast(msg, isError) {
    toastRoot.innerHTML = `<div class="toast" style="${isError ? 'background:#8f2c23' : ''}">${escapeHtml(msg)}</div>`;
    clearTimeout(toast._t);
    toast._t = setTimeout(() => { toastRoot.innerHTML = ''; }, 3200);
  }

  async function api(path, options = {}) {
    const headers = Object.assign({ 'Content-Type': 'application/json' }, options.headers || {});
    if (state.session) headers['x-member-id'] = state.session.memberId;
    const res = await fetch(path, Object.assign({}, options, { headers }));
    let body = null;
    try { body = await res.json(); } catch { /* no body */ }
    if (!res.ok) {
      const err = new Error((body && body.error) || `Request failed (${res.status})`);
      err.status = res.status;
      throw err;
    }
    return body;
  }

  // ---------------- bootstrap ----------------
  async function boot() {
    const params = new URLSearchParams(location.search);
    const wsParam = params.get('ws');

    if (state.session && (!wsParam || wsParam === state.session.workspaceId)) {
      try {
        const ws = await api(`/api/workspaces/${state.session.workspaceId}`);
        state.workspace = ws;
        connectSocket();
        renderPage();
        return;
      } catch {
        clearSession();
      }
    }
    renderAuth(wsParam ? { mode: 'join', workspaceId: wsParam } : { mode: 'create' });
  }

  function connectSocket() {
    if (state.socket) return;
    const socket = io();
    state.socket = socket;
    socket.on('connect', () => {
      state.connected = true;
      socket.emit('workspace:join', { workspaceId: state.session.workspaceId, memberId: state.session.memberId });
      renderConnDot();
    });
    socket.on('disconnect', () => { state.connected = false; renderConnDot(); });
    socket.on('workspace:updated', (ws) => {
      if (!state.session || ws.id !== state.session.workspaceId) return;
      state.workspace = ws;
      renderPage();
      refreshModalFromWorkspace();
    });
  }

  function renderConnDot() {
    const el = document.getElementById('conn-dot');
    if (!el) return;
    el.className = 'conn-dot' + (state.connected ? ' online' : '');
    el.innerHTML = `<span class="dot2"></span>${state.connected ? 'Live sync on' : 'Reconnecting…'}`;
  }

  // ---------------- auth screens ----------------
  function renderAuth({ mode, workspaceId }) {
    if (mode === 'join') {
      pageEl.innerHTML = `
        <div class="auth-card">
          <div class="eyebrow" style="color:var(--red);font-weight:700;letter-spacing:.06em;font-size:.78rem;text-transform:uppercase;">Shared Audit Room</div>
          <h1>Join the audit workspace</h1>
          <p class="muted">Enter the email that was invited to this workspace.</p>
          <form id="join-form">
            <label>Your name</label>
            <input name="name" placeholder="Jane Auditor" />
            <label>Your email</label>
            <input name="email" type="email" required placeholder="you@company.com" />
            <div class="auth-error" id="auth-error"></div>
            <button class="primary-btn" type="submit">Join workspace →</button>
          </form>
          <div class="auth-switch">Setting up a new team instead? <a id="switch-create">Create a workspace</a></div>
        </div>`;
      pageEl.querySelector('#join-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const fd = new FormData(e.target);
        try {
          const result = await api(`/api/workspaces/${workspaceId}/join`, {
            method: 'POST',
            body: JSON.stringify({ email: fd.get('email'), name: fd.get('name') }),
          });
          saveSession({ workspaceId, memberId: result.memberId });
          const url = new URL(location.href);
          url.searchParams.set('ws', workspaceId);
          history.replaceState({}, '', url);
          state.workspace = result.workspace;
          connectSocket();
          renderPage();
        } catch (err) {
          pageEl.querySelector('#auth-error').textContent = err.message;
        }
      });
      pageEl.querySelector('#switch-create').addEventListener('click', () => renderAuth({ mode: 'create' }));
      return;
    }

    pageEl.innerHTML = `
      <div class="auth-card">
        <div style="color:var(--red);font-weight:700;letter-spacing:.06em;font-size:.78rem;text-transform:uppercase;">New Shared Audit Room</div>
        <h1>Create an audit workspace</h1>
        <p class="muted">You'll be the owner and can invite members by email.</p>
        <form id="create-form">
          <label>Workspace name</label>
          <input name="name" required placeholder="Henry's audit workspace" />
          <label>Your name</label>
          <input name="ownerName" placeholder="Henry Jonan" />
          <label>Your email</label>
          <input name="ownerEmail" type="email" required placeholder="you@company.com" />
          <div class="auth-error" id="auth-error"></div>
          <button class="primary-btn" type="submit">Create workspace →</button>
        </form>
        <div class="auth-switch">Have an invite link? Paste it below.</div>
        <form id="link-form" style="margin-top:8px;">
          <input name="link" placeholder="Paste invite link or workspace ID" />
          <button class="ghost-btn" style="margin-top:10px;" type="submit">Open link</button>
        </form>
      </div>`;
    pageEl.querySelector('#create-form').addEventListener('submit', async (e) => {
      e.preventDefault();
      const fd = new FormData(e.target);
      try {
        const result = await api('/api/workspaces', {
          method: 'POST',
          body: JSON.stringify({
            name: fd.get('name'),
            ownerName: fd.get('ownerName'),
            ownerEmail: fd.get('ownerEmail'),
          }),
        });
        saveSession({ workspaceId: result.workspace.id, memberId: result.memberId });
        const url = new URL(location.href);
        url.searchParams.set('ws', result.workspace.id);
        history.replaceState({}, '', url);
        state.workspace = result.workspace;
        connectSocket();
        renderPage();
      } catch (err) {
        pageEl.querySelector('#auth-error').textContent = err.message;
      }
    });
    pageEl.querySelector('#link-form').addEventListener('submit', (e) => {
      e.preventDefault();
      const raw = new FormData(e.target).get('link').trim();
      let id = raw;
      try {
        const u = new URL(raw);
        id = u.searchParams.get('ws') || raw;
      } catch { /* not a URL, treat as raw id */ }
      if (!id) return;
      renderAuth({ mode: 'join', workspaceId: id });
    });
  }

  // ---------------- main page ----------------
  function currentMember() {
    if (!state.workspace || !state.session) return null;
    return state.workspace.members.find((m) => m.id === state.session.memberId) || null;
  }

  function filteredTasks() {
    const q = state.search.trim().toLowerCase();
    return state.workspace.tasks.filter((t) => {
      if (state.priorityFilter !== 'all' && t.priority !== state.priorityFilter) return false;
      if (q && !(t.title.toLowerCase().includes(q) || (t.description || '').toLowerCase().includes(q))) return false;
      return true;
    });
  }

  function renderPage() {
    if (!state.workspace) return;
    const ws = state.workspace;
    const me = currentMember();
    const tasks = filteredTasks();

    pageEl.innerHTML = `
      <div class="app-shell">
        <div class="board-header">
          <div>
            <div class="eyebrow">Shared Audit Room</div>
            <h1>${escapeHtml(ws.name)}</h1>
            <div class="meta">${ws.tasks.length} items · ${ws.members.filter(m=>m.status==='active').length} members ·
              <span id="conn-dot" class="conn-dot"></span>
            </div>
          </div>
          <button class="primary-btn" id="new-task-btn">+ New task</button>
        </div>

        <div class="tabbar">
          <button data-tab="board" class="${state.activeTab === 'board' ? 'active' : ''}">Board</button>
          <button data-tab="team" class="${state.activeTab === 'team' ? 'active' : ''}">Team</button>
        </div>

        ${state.activeTab === 'board' ? renderBoardTab(tasks) : renderTeamTab(ws, me)}
      </div>`;

    renderConnDot();
    bindPageEvents(me);
  }

  function renderBoardTab(tasks) {
    return `
      <div class="toolbar">
        <input class="search-input" id="search-input" placeholder="Search tasks" value="${escapeHtml(state.search)}" />
        <button class="filter-chip ${state.priorityFilter === 'all' ? 'active' : ''}" data-filter="all">All</button>
        <button class="filter-chip ${state.priorityFilter === 'high' ? 'active' : ''}" data-filter="high">High</button>
        <button class="filter-chip ${state.priorityFilter === 'medium' ? 'active' : ''}" data-filter="medium">Medium</button>
        <button class="filter-chip ${state.priorityFilter === 'low' ? 'active' : ''}" data-filter="low">Low</button>
      </div>
      <div class="section-label">Workflow · Live team board</div>
      <div class="board">
        ${STATUS_META.map((col) => renderColumn(col, tasks.filter((t) => t.status === col.key))).join('')}
      </div>`;
  }

  function renderColumn(col, tasks) {
    return `
      <div class="column" data-status="${col.key}">
        <div class="column-head">
          <div class="title"><span class="dot ${col.key}"></span>${col.label}</div>
          <div>
            <span class="count">${tasks.length}</span>
            <button class="add-btn" data-quick-add="${col.key}" title="Add task">+</button>
          </div>
        </div>
        ${tasks.length === 0 ? '<div class="empty-col">No tasks</div>' : ''}
        ${tasks.map(renderCard).join('')}
      </div>`;
  }

  function renderCard(t) {
    return `
      <div class="task-card" draggable="true" data-task-id="${t.id}">
        <div class="title">${escapeHtml(t.title)}</div>
        <div class="row">
          <span class="priority-badge ${t.priority}">${t.priority}</span>
          <span>${t.assignee ? escapeHtml(t.assignee) : ''}${t.dueDate ? ' · ' + escapeHtml(t.dueDate) : ''}</span>
        </div>
        ${t.labels && t.labels.length ? `<div class="labels">${t.labels.map((l) => `<span class="label-chip">${escapeHtml(l)}</span>`).join('')}</div>` : ''}
      </div>`;
  }

  function renderTeamTab(ws, me) {
    const isOwner = me && me.role === 'owner';
    const inviteLink = `${location.origin}${location.pathname}?ws=${ws.id}`;
    return `
      <div class="team-panel">
        <div class="section-label">Team Access</div>
        <h2 style="margin:4px 0;">Invite audit members</h2>
        <p style="color:var(--ink-dim);margin-top:0;">Admins can invite members by email. Everyone can create, edit, and delete tasks.</p>
        ${isOwner ? `
          <form id="invite-form" class="invite-row">
            <input name="email" type="email" required placeholder="member@company.com" />
            <button class="primary-btn" type="submit">Invite</button>
          </form>
          <div class="copy-link">
            <code id="invite-link">${escapeHtml(inviteLink)}</code>
            <button class="ghost-btn" id="copy-link-btn" type="button">Copy</button>
          </div>
        ` : '<p style="color:var(--ink-dim);font-size:.85rem;">Only the workspace owner can invite or remove members.</p>'}
        <div style="margin-top:18px;">
          ${ws.members.map((m) => `
            <div class="member-row">
              <div class="member-id">
                <div class="avatar">${escapeHtml(m.initials || '?')}</div>
                <div class="member-meta">
                  <div class="name">${escapeHtml(m.name || m.email)}</div>
                  <div class="email">${escapeHtml(m.email)}</div>
                </div>
              </div>
              <div style="display:flex;align-items:center;gap:10px;">
                <span class="member-tag ${m.role === 'owner' ? 'owner' : (m.status === 'invited' ? 'invited' : '')}">${m.role === 'owner' ? 'owner' : m.status}</span>
                ${isOwner && m.role !== 'owner' ? `<button class="remove-btn" data-remove-member="${m.id}">Remove</button>` : ''}
              </div>
            </div>`).join('')}
        </div>
        <button class="sign-out" id="sign-out-btn">← Sign out</button>
      </div>`;
  }

  function bindPageEvents(me) {
    const newTaskBtn = pageEl.querySelector('#new-task-btn');
    if (newTaskBtn) newTaskBtn.addEventListener('click', () => openCreateModal());

    pageEl.querySelectorAll('[data-tab]').forEach((b) => b.addEventListener('click', () => {
      state.activeTab = b.dataset.tab;
      renderPage();
    }));

    const searchInput = pageEl.querySelector('#search-input');
    if (searchInput) {
      searchInput.addEventListener('input', (e) => {
        state.search = e.target.value;
        renderPage();
        pageEl.querySelector('#search-input').focus();
        const v = pageEl.querySelector('#search-input');
        v.selectionStart = v.selectionEnd = v.value.length;
      });
    }

    pageEl.querySelectorAll('[data-filter]').forEach((b) => b.addEventListener('click', () => {
      state.priorityFilter = b.dataset.filter;
      renderPage();
    }));

    pageEl.querySelectorAll('[data-quick-add]').forEach((b) => b.addEventListener('click', () => {
      openCreateModal(b.dataset.quickAdd);
    }));

    pageEl.querySelectorAll('.task-card').forEach((card) => {
      card.addEventListener('click', () => openEditModal(card.dataset.taskId));
      card.addEventListener('dragstart', (e) => {
        e.dataTransfer.setData('text/plain', card.dataset.taskId);
      });
    });

    pageEl.querySelectorAll('.column').forEach((col) => {
      col.addEventListener('dragover', (e) => { e.preventDefault(); col.classList.add('drag-over'); });
      col.addEventListener('dragleave', () => col.classList.remove('drag-over'));
      col.addEventListener('drop', async (e) => {
        e.preventDefault();
        col.classList.remove('drag-over');
        const taskId = e.dataTransfer.getData('text/plain');
        const status = col.dataset.status;
        try {
          const ws = await api(`/api/workspaces/${state.session.workspaceId}/tasks/${taskId}`, {
            method: 'PATCH',
            body: JSON.stringify({ status }),
          });
          state.workspace = ws;
          renderPage();
        } catch (err) {
          toast(err.message, true);
        }
      });
    });

    const inviteForm = pageEl.querySelector('#invite-form');
    if (inviteForm) {
      inviteForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = new FormData(e.target).get('email');
        try {
          const ws = await api(`/api/workspaces/${state.session.workspaceId}/members`, {
            method: 'POST',
            body: JSON.stringify({ email }),
          });
          state.workspace = ws;
          toast(`Invited ${email}`);
          renderPage();
        } catch (err) {
          toast(err.message, true);
        }
      });
    }

    const copyBtn = pageEl.querySelector('#copy-link-btn');
    if (copyBtn) copyBtn.addEventListener('click', () => {
      const text = pageEl.querySelector('#invite-link').textContent;
      navigator.clipboard?.writeText(text).then(() => toast('Invite link copied')).catch(() => toast('Copy the link manually', true));
    });

    pageEl.querySelectorAll('[data-remove-member]').forEach((b) => b.addEventListener('click', async () => {
      if (!confirm('Remove this member from the workspace?')) return;
      try {
        const ws = await api(`/api/workspaces/${state.session.workspaceId}/members/${b.dataset.removeMember}`, { method: 'DELETE' });
        state.workspace = ws;
        renderPage();
      } catch (err) {
        toast(err.message, true);
      }
    }));

    const signOutBtn = pageEl.querySelector('#sign-out-btn');
    if (signOutBtn) signOutBtn.addEventListener('click', () => {
      if (state.socket) state.socket.disconnect();
      clearSession();
      state.workspace = null;
      const url = new URL(location.href);
      url.searchParams.delete('ws');
      history.replaceState({}, '', url);
      renderAuth({ mode: 'create' });
    });
  }

  // ---------------- task modal ----------------
  function blankDraft(status) {
    return {
      id: null, title: '', description: '', status: status || 'backlog', priority: 'medium',
      assignee: '', dueDate: '', labels: [], checklist: [], comments: [],
    };
  }

  function openCreateModal(status) {
    modalMode = 'create';
    draft = blankDraft(status);
    renderModal();
  }

  function openEditModal(taskId) {
    const task = state.workspace.tasks.find((t) => t.id === taskId);
    if (!task) return;
    modalMode = 'edit';
    draft = JSON.parse(JSON.stringify(task));
    renderModal();
  }

  function closeModal() {
    modalMode = null;
    draft = null;
    modalRoot.innerHTML = '';
  }

  function refreshModalFromWorkspace() {
    if (modalMode !== 'edit' || !draft) return;
    const task = state.workspace.tasks.find((t) => t.id === draft.id);
    if (!task) { closeModal(); return; }
    draft = JSON.parse(JSON.stringify(task));
    renderModal();
  }

  function renderModal() {
    if (!modalMode) { modalRoot.innerHTML = ''; return; }
    modalRoot.innerHTML = `
      <div class="modal-backdrop" id="modal-backdrop">
        <div class="modal">
          <div class="modal-head">
            <div>
              <div style="color:var(--red);font-weight:700;letter-spacing:.06em;font-size:.75rem;text-transform:uppercase;">${modalMode === 'create' ? 'New work item' : 'Work item'}</div>
              <h2>${modalMode === 'create' ? 'Create task' : 'Edit task'}</h2>
            </div>
            <button class="modal-close" id="modal-close">✕</button>
          </div>

          <div class="field-label">Title</div>
          <input class="field-input" id="f-title" value="${escapeHtml(draft.title)}" placeholder="What needs to happen?" />

          <div class="field-label">Description</div>
          <textarea class="field-textarea" id="f-desc" placeholder="Add context or acceptance criteria">${escapeHtml(draft.description)}</textarea>

          <div class="field-label">Status</div>
          <div class="status-pills">
            ${STATUS_META.map((s) => `<button type="button" class="pill-btn ${draft.status === s.key ? 'selected' : ''}" data-status-pill="${s.key}">${s.label}</button>`).join('')}
          </div>

          <div class="two-col">
            <div>
              <div class="field-label">Priority</div>
              <select class="field-select" id="f-priority">
                ${PRIORITIES.map((p) => `<option value="${p}" ${draft.priority === p ? 'selected' : ''}>${p[0].toUpperCase() + p.slice(1)}</option>`).join('')}
              </select>
            </div>
            <div>
              <div class="field-label">Assignee</div>
              <input class="field-input" id="f-assignee" value="${escapeHtml(draft.assignee)}" placeholder="Initials" />
            </div>
          </div>

          <div class="field-label">Due date</div>
          <input class="field-input" id="f-due" type="date" value="${escapeHtml(draft.dueDate || '')}" />

          <div class="field-label">Labels</div>
          <div class="chip-input-row">
            <input class="field-input" id="f-label-input" placeholder="Add label" />
            <button type="button" class="chip-add-btn" id="add-label-btn">+</button>
          </div>
          <div class="chips">${draft.labels.map((l, i) => `<span class="chip">${escapeHtml(l)}<button type="button" data-remove-label="${i}">✕</button></span>`).join('')}</div>

          <div class="field-label">Checklist</div>
          <div class="chip-input-row">
            <input class="field-input" id="f-checklist-input" placeholder="Add checklist item" />
            <button type="button" class="chip-add-btn" id="add-checklist-btn">+</button>
          </div>
          <div>
            ${draft.checklist.map((c, i) => `
              <div class="checklist-item ${c.done ? 'done' : ''}">
                <input type="checkbox" data-toggle-check="${i}" ${c.done ? 'checked' : ''} />
                <span>${escapeHtml(c.text)}</span>
                <button type="button" data-remove-check="${i}" class="remove-btn">✕</button>
              </div>`).join('')}
          </div>

          ${modalMode === 'edit' ? `
            <div class="field-label">Comments</div>
            <div>
              ${draft.comments.length ? draft.comments.map((c) => `
                <div class="comment-item"><span class="who">${escapeHtml(c.author)}</span><span class="when">${new Date(c.createdAt).toLocaleString()}</span><div>${escapeHtml(c.text)}</div></div>`).join('') : '<div style="color:var(--ink-dim);font-size:.85rem;">No comments yet.</div>'}
            </div>
            <div class="chip-input-row" style="margin-top:8px;">
              <input class="field-input" id="f-comment-input" placeholder="Write a comment" />
              <button type="button" class="chip-add-btn" id="add-comment-btn">+</button>
            </div>
          ` : ''}

          <div class="modal-actions">
            <button class="primary-btn" id="modal-submit" style="flex:1;">${modalMode === 'create' ? 'Create task →' : 'Save changes →'}</button>
            ${modalMode === 'edit' ? '<button class="danger-btn" id="modal-delete">Delete</button>' : ''}
          </div>
        </div>
      </div>`;
    bindModalEvents();
  }

  function bindModalEvents() {
    const backdrop = document.getElementById('modal-backdrop');
    backdrop.addEventListener('click', (e) => { if (e.target === backdrop) closeModal(); });
    document.getElementById('modal-close').addEventListener('click', closeModal);

    document.getElementById('f-title').addEventListener('input', (e) => { draft.title = e.target.value; });
    document.getElementById('f-desc').addEventListener('input', (e) => { draft.description = e.target.value; });
    document.getElementById('f-assignee').addEventListener('input', (e) => { draft.assignee = e.target.value; });
    document.getElementById('f-due').addEventListener('input', (e) => { draft.dueDate = e.target.value; });
    document.getElementById('f-priority').addEventListener('change', (e) => { draft.priority = e.target.value; });

    modalRoot.querySelectorAll('[data-status-pill]').forEach((b) => b.addEventListener('click', () => {
      draft.status = b.dataset.statusPill;
      renderModal();
    }));

    document.getElementById('add-label-btn').addEventListener('click', () => {
      const input = document.getElementById('f-label-input');
      const val = input.value.trim();
      if (!val) return;
      draft.labels.push(val);
      renderModal();
    });
    modalRoot.querySelectorAll('[data-remove-label]').forEach((b) => b.addEventListener('click', () => {
      draft.labels.splice(Number(b.dataset.removeLabel), 1);
      renderModal();
    }));

    document.getElementById('add-checklist-btn').addEventListener('click', () => {
      const input = document.getElementById('f-checklist-input');
      const val = input.value.trim();
      if (!val) return;
      draft.checklist.push({ text: val, done: false });
      renderModal();
    });
    modalRoot.querySelectorAll('[data-toggle-check]').forEach((b) => b.addEventListener('change', (e) => {
      draft.checklist[Number(b.dataset.toggleCheck)].done = e.target.checked;
      renderModal();
    }));
    modalRoot.querySelectorAll('[data-remove-check]').forEach((b) => b.addEventListener('click', () => {
      draft.checklist.splice(Number(b.dataset.removeCheck), 1);
      renderModal();
    }));

    const commentBtn = document.getElementById('add-comment-btn');
    if (commentBtn) {
      commentBtn.addEventListener('click', async () => {
        const input = document.getElementById('f-comment-input');
        const text = input.value.trim();
        if (!text) return;
        try {
          const ws = await api(`/api/workspaces/${state.session.workspaceId}/tasks/${draft.id}/comments`, {
            method: 'POST',
            body: JSON.stringify({ text }),
          });
          state.workspace = ws;
          draft = JSON.parse(JSON.stringify(ws.tasks.find((t) => t.id === draft.id)));
          renderPage();
          renderModal();
        } catch (err) {
          toast(err.message, true);
        }
      });
    }

    document.getElementById('modal-submit').addEventListener('click', submitModal);

    const deleteBtn = document.getElementById('modal-delete');
    if (deleteBtn) {
      deleteBtn.addEventListener('click', async () => {
        if (!confirm('Delete this task? This cannot be undone.')) return;
        try {
          const ws = await api(`/api/workspaces/${state.session.workspaceId}/tasks/${draft.id}`, { method: 'DELETE' });
          state.workspace = ws;
          closeModal();
          renderPage();
        } catch (err) {
          toast(err.message, true);
        }
      });
    }
  }

  async function submitModal() {
    const payload = {
      title: draft.title,
      description: draft.description,
      status: draft.status,
      priority: draft.priority,
      assignee: draft.assignee,
      dueDate: draft.dueDate || null,
      labels: draft.labels,
      checklist: draft.checklist,
    };
    if (!payload.title.trim()) { toast('Title is required', true); return; }
    try {
      const ws = modalMode === 'create'
        ? await api(`/api/workspaces/${state.session.workspaceId}/tasks`, { method: 'POST', body: JSON.stringify(payload) })
        : await api(`/api/workspaces/${state.session.workspaceId}/tasks/${draft.id}`, { method: 'PATCH', body: JSON.stringify(payload) });
      state.workspace = ws;
      toast(modalMode === 'create' ? 'Task created' : 'Task updated');
      closeModal();
      renderPage();
    } catch (err) {
      toast(err.message, true);
    }
  }

  boot();
})();
