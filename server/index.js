const path = require('path');
const http = require('http');
const express = require('express');
const { Server } = require('socket.io');
const db = require('./db');

function createApp() {
  const app = express();
  app.use(express.json());
  app.use(express.static(path.join(__dirname, '..', 'public')));

  const server = http.createServer(app);
  const io = new Server(server);

  function broadcast(workspaceId) {
    const ws = db.getWorkspace(workspaceId);
    if (ws) io.to(workspaceId).emit('workspace:updated', ws);
    return ws;
  }

  io.on('connection', (socket) => {
    socket.on('workspace:join', ({ workspaceId, memberId }) => {
      const member = db.findMember(workspaceId, memberId);
      if (!member) return;
      socket.join(workspaceId);
    });
  });

  function requireMember(req, res, next) {
    const { workspaceId } = req.params;
    const memberId = req.header('x-member-id');
    const member = db.findMember(workspaceId, memberId);
    if (!member) {
      return res.status(403).json({ error: 'Not an active member of this workspace' });
    }
    req.member = member;
    next();
  }

  function handleError(res, err) {
    const status = err.status || 500;
    if (status === 500) console.error(err);
    res.status(status).json({ error: err.message || 'Internal server error' });
  }

  app.post('/api/workspaces', (req, res) => {
    try {
      const { name, ownerName, ownerEmail } = req.body || {};
      const result = db.createWorkspace({ name, ownerName, ownerEmail });
      res.status(201).json(result);
    } catch (err) {
      handleError(res, err);
    }
  });

  app.get('/api/workspaces/:workspaceId', requireMember, (req, res) => {
    res.json(db.getWorkspace(req.params.workspaceId));
  });

  app.post('/api/workspaces/:workspaceId/join', (req, res) => {
    try {
      const { email, name } = req.body || {};
      const result = db.joinWorkspace(req.params.workspaceId, email, name);
      broadcast(req.params.workspaceId);
      res.json(result);
    } catch (err) {
      handleError(res, err);
    }
  });

  app.post('/api/workspaces/:workspaceId/members', requireMember, (req, res) => {
    try {
      const { email } = req.body || {};
      db.inviteMember(req.params.workspaceId, req.member.id, email);
      const ws = broadcast(req.params.workspaceId);
      res.status(201).json(ws);
    } catch (err) {
      handleError(res, err);
    }
  });

  app.delete('/api/workspaces/:workspaceId/members/:memberId', requireMember, (req, res) => {
    try {
      db.removeMember(req.params.workspaceId, req.member.id, req.params.memberId);
      const ws = broadcast(req.params.workspaceId);
      res.json(ws);
    } catch (err) {
      handleError(res, err);
    }
  });

  app.post('/api/workspaces/:workspaceId/tasks', requireMember, (req, res) => {
    try {
      db.createTask(req.params.workspaceId, req.member.id, req.body || {});
      const ws = broadcast(req.params.workspaceId);
      res.status(201).json(ws);
    } catch (err) {
      handleError(res, err);
    }
  });

  app.patch('/api/workspaces/:workspaceId/tasks/:taskId', requireMember, (req, res) => {
    try {
      db.updateTask(req.params.workspaceId, req.member.id, req.params.taskId, req.body || {});
      const ws = broadcast(req.params.workspaceId);
      res.json(ws);
    } catch (err) {
      handleError(res, err);
    }
  });

  app.post('/api/workspaces/:workspaceId/tasks/:taskId/comments', requireMember, (req, res) => {
    try {
      const { text } = req.body || {};
      db.addComment(req.params.workspaceId, req.member.id, req.params.taskId, text);
      const ws = broadcast(req.params.workspaceId);
      res.status(201).json(ws);
    } catch (err) {
      handleError(res, err);
    }
  });

  app.delete('/api/workspaces/:workspaceId/tasks/:taskId', requireMember, (req, res) => {
    try {
      db.deleteTask(req.params.workspaceId, req.member.id, req.params.taskId);
      const ws = broadcast(req.params.workspaceId);
      res.json(ws);
    } catch (err) {
      handleError(res, err);
    }
  });

  return { app, server, io };
}

if (require.main === module) {
  const { server } = createApp();
  const PORT = process.env.PORT || 3000;
  server.listen(PORT, () => {
    console.log(`Audit workspace board listening on http://localhost:${PORT}`);
  });
}

module.exports = { createApp };
