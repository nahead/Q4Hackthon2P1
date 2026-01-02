---
id: 2
title: phase2-fullstack-constitution-update
stage: constitution
date: 2026-01-02
surface: agent
model: claude-sonnet-4.5-20250929
feature: none
branch: main
user: unknown
command: /sp.constitution
labels: ["constitution","governance","phase2-transition","fullstack","security"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

"""Project: Evolution of Todo – Phase II (Full-Stack Web Application)

Core principles:
- Spec-driven development:
  All implementation must originate from structured specifications managed by Spec-Kit Plus.
- Architectural continuity:
  Phase II must evolve cleanly from Phase I without breaking core domain logic.
- Separation of concerns:
  Frontend, backend, database, and authentication layers must remain clearly isolated.
- API-first design:
  Backend behavior is defined by REST contracts before UI implementation.
- Security by default:
  Authentication, authorization, and user isolation are mandatory and enforced consistently.
- AI-native workflow:
  Claude Code is the sole implementation agent; no manual coding is permitted.

Key standards:
- Development workflow:
  Spec → Plan → Tasks → Implement → Review (Agentic Dev Stack enforced)
- Backend standards:
  - FastAPI with RESTful endpoints
  - SQLModel for ORM and schema alignment
  - Stateless services with JWT-based authentication
- Frontend standards:
  - Next.js 16+ using App Router
  - Responsive UI with clear task state representation
  - All API calls routed through a centralized client
- Authentication standards:
  - Better Auth used on frontend
  - JWT tokens issued on login
  - JWT verified on every backend request
  - Task ownership enforced at API level
- Data standards:
  - Persistent storage in Neon Serverless PostgreSQL
  - All tasks scoped to authenticated users
  - Database schema defined in specs and mirrored in SQLModel

Constraints:
- No console-based UI
- No in-memory-only storage
- No shared session state between frontend and backend
- No direct database access from frontend
- No bypassing JWT verification
- No manual code edits outside Claude Code
- No deviation from defined API contracts
- No phase-advanced features (AI chatbot, event systems, Kubernetes)

Monorepo & spec governance:
- Repository must follow Spec-Kit monorepo structure
- Specifications live under /specs with typed subdirectories:
  - /features
  - /api
  - /database
  - /ui
- CLAUDE.md files define navigation and coding rules at:
  - Root
  - /frontend
  - /backend
- Claude Code must reference specs using @specs paths
- Specs are the single source of truth

Security guarantees:
- All API endpoints require a valid JWT token
- Requests without a token return 401 Unauthorized
- User identity extracted from JWT must match route user context
- Backend filters all data by authenticated user ID
- Shared JWT secret managed via environment variables

Success criteria:
- All 5 basic todo features work as a web application
- Multi-user support with strict user data isolation
- REST API behaves exactly as specified
- Frontend and backend integrate via authenticated API calls
- Database persistence verified across sessions
- Codebase is reviewable, traceable, and spec-aligned
- Phase II is ready to evolve into Phase III (AI chatbot)

Failure conditions:
- Mixing frontend and backend responsibilities
- Accessing or modifying tasks across users
- Implementing features not defined in specs
- Skipping authentication on any endpoint
- Writing code without a corresponding spec reference
- Manual coding outside Claude Code

Quality bar:
- Clean, idiomatic FastAPI and Next.js code
- Predictable API responses and error handling
- Clear, navigable monorepo structure
- High signal-to-noise specs and prompts
- Reviewer can trace every feature to a spec file"""

## Response snapshot

Successfully updated project constitution from v1.0.0 to v2.0.0 for Phase II transition. Key changes include:

**Core Principles (6 updated):**
1. Spec-Driven Development - specs are single source of truth
2. Architectural Continuity - evolve from console to web, single to multi-user
3. Separation of Concerns - frontend/backend/database/auth layers isolated
4. API-First Design - REST contracts before UI implementation
5. Security by Default - mandatory JWT authentication, user data isolation
6. AI-Native Workflow - Claude Code as sole implementation agent

**New Technical Standards:**
- Backend: FastAPI, SQLModel, JWT auth, Neon PostgreSQL
- Frontend: Next.js 16+ App Router, Better Auth, TypeScript
- Authentication: JWT tokens, Better Auth frontend, token verification on every request
- Data: Persistent storage, user-scoped data, SQLModel ORM

**New Sections Added:**
- Monorepo & Spec Governance - spec organization and authority
- Security Guarantees - comprehensive authentication/authorization requirements
- Updated Constraints - removed Phase I restrictions, added Phase II requirements

**Forward-Compatibility:**
- Phase III: AI agents can access REST API
- Phase IV: Kubernetes-ready (environment config, stateless design)
- Phase V: Event architecture compatible (observable state transitions)

Included Sync Impact Report documenting version change (1.0.0 → 2.0.0), all template reviews, and no pending TODOs.

## Outcome

- ✅ Impact: Constitution now governs Phase II full-stack web application development with comprehensive security and multi-user support
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md (v1.0.0 → v2.0.0)
- 🔁 Next prompts: Phase II feature specification, API contracts, database schema design
- 🧠 Reflection: Successfully transitioned constitution from Phase I (console app) to Phase II (full-stack web) while maintaining architectural continuity and adding critical security guarantees

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): n/a
- Prompt variant (if applicable): Phase II constitution amendment
- Next experiment (smallest change to try): Validate constitution alignment during Phase II feature specification and API contract design
