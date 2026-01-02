<!--
  SYNC IMPACT REPORT
  ===================
  Version Change: 1.0.0 → 2.0.0 (MAJOR - Phase II transition)

  Modified Principles:
    - Architectural Continuity → Architectural Continuity (redefined for full-stack)
    - Simplicity with Intent → Separation of Concerns (new emphasis)
    - Deterministic Behavior → API-First Design (new focus)
    - AI-First Collaboration → AI-Native Workflow (retained, refined)
    - Explicit State Management → Security by Default (new emphasis)
    - Interface Agnosticism → retained with web API focus

  Added Sections:
    - Monorepo & Spec Governance (new for Phase II)
    - Security Guarantees (new comprehensive section)
    - Multi-User Data Isolation requirements

  Removed Sections:
    - Phase I constraints (console-only, in-memory storage)

  Templates Updated:
    - ✅ .specify/templates/plan-template.md - Reviewed for Constitution Check section
    - ✅ .specify/templates/spec-template.md - Reviewed for requirements alignment
    - ✅ .specify/templates/tasks-template.md - Reviewed for task categorization

  Follow-up TODOs:
    - None
-->

# Evolution of Todo Constitution - Phase II

## Core Principles

### I. Spec-Driven Development

All implementation MUST originate from structured specifications managed by Spec-Kit Plus. Specs are the single source of truth and define all requirements, API contracts, database schemas, and UI behavior. No feature shall be implemented without a corresponding spec reference.

**Rationale**: Ensures traceability, prevents scope creep, and maintains alignment between frontend, backend, database, and authentication layers. Specifications enable clear review and validation at every stage.

### II. Architectural Continuity

Phase II MUST evolve cleanly from Phase I without breaking core domain logic. The todo domain (tasks, status, operations) remains the same, but the implementation shifts from console to web, in-memory to persistent storage, single-user to multi-user. Business logic MUST be preserved and reusable.

**Rationale**: Maintains conceptual continuity across phases while enabling the architectural evolution from console app to full-stack web application. Core domain operations (add, list, update, complete, delete) remain invariant across all phases.

### III. Separation of Concerns

Frontend, backend, database, and authentication layers MUST remain clearly isolated. Frontend SHALL NOT directly access the database or implement business logic. Backend SHALL NOT contain UI logic. Authentication MUST be a distinct, reusable service. Each layer communicates only through defined interfaces (REST APIs, database models, authentication tokens).

**Rationale**: Enables independent development, testing, and scaling of each layer. Prevents tight coupling that would impede future evolution (Phase III: AI agents, Phase IV: Kubernetes, Phase V: event-driven architecture).

### IV. API-First Design

Backend behavior MUST be defined by REST contracts before UI implementation. Every feature MUST have a corresponding API specification including endpoints, request/response schemas, error handling, and authentication requirements. Frontend implementation MUST align exactly with the API contracts.

**Rationale**: Frontend and backend teams can work in parallel with clear contracts. API stability ensures frontend remains functional as backend evolves. Simplifies testing, documentation, and future integration with AI agents.

### V. Security by Default

Authentication, authorization, and user isolation are mandatory and enforced consistently. All API endpoints MUST require valid JWT tokens. User identity MUST be extracted from JWT and match route context. Backend MUST filter all data by authenticated user ID. No cross-user data access is permitted.

**Rationale**: Multi-user environments require strict security boundaries. JWT verification at the API layer and user-scoped data queries prevent data leaks. Security enforcement must be automatic, not optional.

### VI. AI-Native Workflow

Claude Code is the sole implementation agent; no manual coding is permitted. All development, planning, coding, and review MUST be executed through Claude Code with Spec-Kit Plus tools. Humans provide requirements and approve; AI generates all code, tests, and documentation.

**Rationale**: Ensures consistent adherence to specs and architectural patterns. Accelerates development while maintaining quality standards. All changes are traceable to prompts and decisions recorded in Prompt History Records (PHRs).

## Technical Standards

### Backend Standards
- **Framework**: FastAPI with RESTful endpoints
- **ORM**: SQLModel for database schema alignment and type safety
- **Architecture**: Stateless services with JWT-based authentication
- **API Design**: RESTful contracts defined in specifications
- **Error Handling**: Consistent error taxonomy with status codes
- **Authentication**: JWT token verification on every request
- **Database**: Neon Serverless PostgreSQL (managed, serverless)

### Frontend Standards
- **Framework**: Next.js 16+ using App Router
- **UI Pattern**: Responsive web interface with clear task state representation
- **API Client**: Centralized API client for all backend communication
- **Authentication**: Better Auth for frontend authentication flow
- **State Management**: Component-level state with API-driven updates
- **Type Safety**: TypeScript for all frontend code

### Authentication Standards
- **Frontend**: Better Auth handles login/logout flows
- **Token Issuance**: Backend issues JWT tokens on successful authentication
- **Token Verification**: Backend verifies JWT on every API request
- **User Context**: User identity extracted from JWT must match route parameters
- **Session Management**: No shared session state between frontend and backend
- **Secret Management**: JWT secret managed via environment variables

### Data Standards
- **Storage**: Persistent storage in Neon Serverless PostgreSQL
- **ORM**: SQLModel for schema definition and queries
- **User Isolation**: All tasks scoped to authenticated users (user_id foreign key)
- **Schema Alignment**: Database schema defined in specs and mirrored in SQLModel
- **Migration**: Schema changes must be backward compatible where possible
- **Data Access**: No direct database access from frontend (API only)

## Constraints

### Prohibited in Phase II
- Console-based UI or command-line interfaces
- In-memory-only storage (all data must persist)
- Shared session state between frontend and backend
- Direct database access from frontend
- Bypassing JWT verification on any endpoint
- Manual code edits outside Claude Code
- Implementing features not defined in specs
- Accessing or modifying tasks across users
- Phase-advanced features (AI chatbot, event systems, Kubernetes)

### Required
- FastAPI backend with RESTful endpoints
- SQLModel for ORM and schema alignment
- Next.js 16+ frontend with App Router
- Better Auth on frontend for authentication
- JWT-based authentication with token verification
- Neon Serverless PostgreSQL for persistent storage
- User-scoped data access and filtering
- Spec-driven development for all features
- Claude Code as sole implementation agent

## Monorepo & Spec Governance

### Repository Structure
Repository MUST follow Spec-Kit monorepo structure:
- `/specs` - All specifications organized by type
  - `/features` - Feature specifications and requirements
  - `/api` - API contracts, endpoints, request/response schemas
  - `/database` - Database schemas, migrations, entity definitions
  - `/ui` - UI specifications, component definitions, user flows

### Navigation & Coding Rules
CLAUDE.md files define navigation and coding rules at:
- Root `/CLAUDE.md` - Project-level agent instructions
- `/frontend/CLAUDE.md` - Frontend-specific rules and patterns
- `/backend/CLAUDE.md` - Backend-specific rules and patterns

### Spec References
Claude Code MUST reference specs using `@specs` paths. For example:
- "Implement task creation per @specs/api/endpoints.md#post-tasks"
- "Database schema defined in @specs/database/schema.md#tasks-table"

### Authority
Specs are the single source of truth. All implementation must trace back to a spec file. Discrepancies between code and specs must be resolved by updating the spec first, then the code.

## Security Guarantees

### Authentication Enforcement
- All API endpoints require a valid JWT token
- Requests without a token return 401 Unauthorized
- Invalid tokens return 401 Unauthorized with descriptive message
- Token expiration must be handled with appropriate 401 response

### Authorization & Data Isolation
- User identity extracted from JWT must match route user context
- Backend filters all data by authenticated user ID
- No endpoint may return data belonging to another user
- No endpoint may allow modification of another user's data
- Cross-user access attempts return 403 Forbidden

### Token Management
- JWT secret managed via environment variables (never in code)
- Tokens must include user ID and expiration claim
- Token payload must be signed with HMAC-SHA256 or equivalent
- Frontend stores token securely (httpOnly cookie recommended)

### Error Handling
- Authentication failures MUST NOT reveal whether user exists
- Authorization errors must be generic (no data leakage)
- Sensitive information must not appear in error messages
- Server errors (500) must be logged without exposing internals

## Quality Standards

### Code Quality
- **Clean Idiomatic Code**: Follow framework best practices (FastAPI, Next.js)
- **Type Safety**: TypeScript on frontend, type hints on backend
- **Predictable Responses**: Consistent API response structure
- **Clear Error Messages**: User-friendly error messages with actionable guidance
- **Minimal Dependencies**: Prefer framework-native solutions over external libraries

### Failure Conditions
- Mixing frontend and backend responsibilities
- Accessing or modifying tasks across users
- Implementing features not defined in specs
- Skipping authentication on any endpoint
- Writing code without a corresponding spec reference
- Manual coding outside Claude Code

### Success Criteria
- All 5 basic todo features work as a web application
- Multi-user support with strict user data isolation
- REST API behaves exactly as specified in contracts
- Frontend and backend integrate via authenticated API calls
- Database persistence verified across sessions
- Codebase is reviewable, traceable, and spec-aligned
- Phase II is ready to evolve into Phase III (AI chatbot)

## Forward-Compatibility Requirements

### Phase III: Natural-Language AI Agents
- All API endpoints remain accessible to AI agents
- Domain operations callable programmatically via HTTP
- Clear separation between interpretation (AI) and execution (API)
- JWT authentication supported by AI agent integration
- No UI-specific logic in backend (agents bypass UI)

### Phase IV: Containerization & Kubernetes
- Configuration environment-based (no hardcoded values)
- Stateless backend design (state in database, not memory)
- Clear startup/shutdown hooks
- Health check endpoints definable
- Secrets managed via environment variables (already done)

### Phase V: Event-Driven Architecture (Kafka + Dapr)
- API endpoints remain as primary interface
- State transitions observable via database
- No circular dependencies between services
- Clear boundaries for future event sourcing
- Current REST API compatible with event ingestion

## Governance

### Amendment Procedure
1. Propose change with rationale and impact analysis
2. Identify affected phases and compatibility issues
3. Document transition strategy if required
4. Update constitution with version bump following semantic versioning
5. Review and propagate changes to dependent templates
6. Create Prompt History Record (PHR) documenting the change

### Versioning Policy
- **MAJOR (X.0.0)**: Backward incompatible governance changes, principle removal or redefinition, phase transitions
- **MINOR (x.Y.0)**: New principle or section added, material guidance expansion
- **PATCH (x.y.Z)**: Clarifications, wording fixes, non-semantic refinements

### Compliance Review
- All plans MUST reference relevant principles
- All decisions MUST justify deviations with complexity tracking
- Architectural Decision Records (ADRs) MUST cite constitution principles
- Code reviews MUST verify compliance with constraints and standards
- All code changes MUST trace to spec references

### Authoritative Sources
- **This Constitution**: Governs all project phases
- **CLAUDE.md**: Agent-specific execution rules and tooling guidance
- **Feature Specs**: User requirements and acceptance criteria (MUST align with constitution)
- **Plans**: Technical decisions and architecture (MUST pass constitution gates)
- **API Contracts**: REST endpoint definitions (MUST align with authentication standards)
- **Database Schemas**: Data model definitions (MUST align with data isolation requirements)

**Version**: 2.0.0 | **Ratified**: 2026-01-01 | **Last Amended**: 2026-01-02
