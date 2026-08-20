# Audit Workspace Board

Online, real-time collaborative task board for INPP audit teams — like a
Kanban / scrum board, but shared: invite members by email and everyone can
create, edit, and move tasks live.

## Features

- **Shared workspace with a private invite link.** The owner creates a
  workspace and invites members by email; only invited emails can join.
- **5-column Kanban board**: Backlog → To Do → In Progress → In Review → Done.
  Drag and drop cards between columns, or use the quick "+" per column.
- **Rich tasks**: title, description, status, priority, assignee, due date,
  labels, checklist, and comments.
- **Live sync**: every create/edit/move/delete/invite is pushed instantly to
  every connected member over WebSockets (Socket.IO) — no refresh needed.
- **Everyone can create, edit, and delete tasks.** Only the workspace owner
  can invite or remove members.

## Tech stack

- Backend: Node.js + Express + Socket.IO, JSON file storage via `lowdb`
  (`server/index.js`, `server/db.js`).
- Frontend: plain HTML/CSS/JS, no build step (`public/`).
- Tests: Node's built-in test runner (`node:test`) + `supertest`
  (`test/api.test.js`).

## Running locally

```bash
npm install
npm start          # http://localhost:3000
```

For auto-reload during development:

```bash
npm run dev
```

## Running the test suite

```bash
npm test
```

This runs 14 automated tests covering: workspace creation/validation, invite
and join permissions (only the owner can invite; only invited emails can
join), member removal rules (owner can't be removed), task create/update/
delete permissions, comments, and input validation (empty title, invalid
status, etc.).

Automated tests only cover the HTTP API. Before every deploy, also run a
quick manual pass in a real browser:

1. Create a workspace, invite a second email, open the invite link in a
   second browser/incognito window, and join with that email.
2. Create a task from both windows and confirm each shows up on the other
   side within ~1 second (live sync).
3. Drag a card across columns and confirm it moves on the other window too.
4. Edit fields (priority, due date, labels, checklist, comments), delete a
   task, and remove a member — confirm both windows stay in sync.

(This exact flow — two simulated members, live task creation, and a
drag-and-drop status change — was also verified with an automated
Socket.IO + Playwright smoke test against a running server before this was
pushed.)

## Data & access model

- Each workspace has a random, unguessable ID (used in the invite link
  `?ws=<id>`). Anyone with the link can request to join, but joining only
  succeeds if their email was invited by the owner.
- Membership is identified via an `x-member-id` header issued when creating
  or joining a workspace (stored in the browser's `localStorage`). This is
  intentionally lightweight (link-based access, like sharing a Google Doc)
  and is **not** hardened for storing sensitive audit workpapers — treat it
  as a task/status tracker, not a system of record for confidential data.
- Data is stored in `data/db.json` (gitignored). For production use beyond a
  single small team, swap `lowdb` for a real database — the `server/db.js`
  module is the only place that would need to change.

## Deploying

The app is a single Node process serving both the API and the static
frontend, so it runs anywhere Node.js runs (Render, Fly.io, Railway, a small
VM, etc.):

```bash
npm install --omit=dev
PORT=3000 npm start
```

Set `DB_PATH` to point at a persistent volume if your host's filesystem is
ephemeral.
