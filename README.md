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
ephemeral — otherwise every redeploy/restart wipes the board.

### Deploy on Render (recommended, has a free-tier-friendly path)

This repo includes a `render.yaml` Blueprint, so Render can provision
everything (web service + a small persistent disk for `data/db.json`) from
one click:

1. Merge this PR (or deploy straight from the branch — Render can point at
   any branch).
2. Go to <https://dashboard.render.com>, sign in with GitHub.
3. **New +** → **Blueprint**, pick the `audit-outlier-detector` repo. Render
   reads `render.yaml` automatically and shows one service:
   `audit-workspace-board`.
4. Confirm the plan. The blueprint requests the **Starter** plan (~$7/mo)
   because a persistent disk (needed so tasks survive restarts) isn't
   available on the free plan. If you want $0/mo instead, edit
   `render.yaml` before deploying: change `plan: starter` to `plan: free`
   and delete the `disk:` block — the board will work, but every redeploy
   or spin-down resets all tasks/members to empty.
5. Click **Apply** / **Deploy**. First build takes 1–2 minutes.
6. Once live, Render gives you a URL like
   `https://audit-workspace-board.onrender.com` — that's the link your team
   opens to create/join the workspace.

I can't click through your Render/Railway/Fly.io account myself (no
credentials to it), so steps 2–6 need you at the keyboard — but the repo is
ready to deploy as-is. Ping me if a build fails and paste the error; I can
fix the code from here.

### Alternative: Railway / Fly.io / any VM

Same idea, no `render.yaml` needed — these hosts auto-detect
`npm start` from `package.json`:

- **Railway**: New Project → Deploy from GitHub repo → it builds and starts
  automatically. Add a volume mounted at e.g. `/data` and set
  `DB_PATH=/data/db.json` in the service's environment variables so tasks
  persist across deploys.
- **Fly.io** / **a small VM**: `npm install --omit=dev && npm start`, with
  `DB_PATH` pointed at a persistent disk/volume and `PORT` set by the
  platform (Fly.io sets this automatically).
