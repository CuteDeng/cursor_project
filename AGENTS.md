# AGENTS.md

Guidance for cloud agents working in this repository.

## Repository status

This repository is a minimal starter project. It currently contains only `README.md` (title: `cursor_project`). There is no application source code, dependency manifests, Docker configuration, CI workflows, or test suites yet.

## Cursor Cloud specific instructions

### Services

| Service | Required? | Notes |
|---------|-----------|-------|
| — | — | No services are defined. Nothing needs to be started for local development. |

### Development workflow

Until application code is added, there is nothing to lint, test, build, or run beyond normal git operations.

When code is added, update this file with:

- How to install dependencies (package manager and lockfile)
- Commands to lint, test, and run the app in **development** mode (not production build)
- Any non-obvious startup caveats (ports, env vars, background services)

### Base environment

The cloud VM provides standard tooling out of the box (git, Node.js via nvm, Python 3). No project-specific dependency refresh is required on VM startup for the current repository state.

### Git

- Default branch: `main`
- Feature branches for agent work should use the pattern `cursor/<descriptive-name>-b77c`
