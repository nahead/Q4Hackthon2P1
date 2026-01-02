# Research: Phase II Full-Stack Web Application

**Feature Branch**: `002-phase2-webapp`
**Created**: 2026-01-02
**Purpose**: Technology selection and architecture research for full-stack todo application

## Backend Framework Research

### Decision: FastAPI

**Chosen**: FastAPI for backend REST API framework

**Rationale**:
- Modern, high-performance Python web framework with automatic OpenAPI documentation
- Built-in data validation with Pydantic models
- Asynchronous support for better performance with database I/O
- Excellent SQLModel integration for type-safe database operations
- Industry best practices and growing ecosystem
- Automatic API documentation via Swagger UI
- Native dependency injection for authentication and authorization

**Alternatives Considered**:
- **Django REST Framework**: Mature but more opinionated, requires Django ORM (not SQLModel), steeper learning curve
- **Flask**: Lightweight but requires more manual configuration, no built-in data validation, more boilerplate for JWT auth
- **Falcon**: Very fast but minimal features, requires manual setup for many common features

**Constitution Alignment**: Meets Backend Standards (FastAPI with RESTful endpoints, type hints)

---

## Frontend Framework Research

### Decision: Next.js 16+ with App Router

**Chosen**: Next.js 16+ using App Router for frontend

**Rationale**:
- Industry-leading React framework with excellent developer experience
- App Router provides modern routing with nested layouts and loading states
- Server Components for better performance and SEO
- Built-in optimization (image, font, code splitting)
- Strong TypeScript support
- Large ecosystem and community
- Excellent for hackathons (quick setup, production-ready)

**Alternatives Considered**:
- **React (Vite)**: Lightweight but requires manual routing and optimization configuration
- **SvelteKit**: Modern but smaller ecosystem, more learning curve for hackathon timeline
- **Nuxt.js**: Vue-based, excellent but React ecosystem larger for hiring/hackathons

**Constitution Alignment**: Meets Frontend Standards (Next.js 16+ using App Router, TypeScript)

---

## ORM Research

### Decision: SQLModel

**Chosen**: SQLModel for Python ORM and database schema alignment

**Rationale**:
- Pydantic-based, provides automatic type hints and validation
- Seamless FastAPI integration (shared Pydantic models for requests/responses)
- SQLAlchemy under the hood (mature, battle-tested ORM)
- Declarative schema definition (Python classes map to database tables)
- Automatic migration support with Alembic
- Type safety reduces bugs at development time
- Database-agnostic (works with PostgreSQL, MySQL, SQLite, etc.)

**Alternatives Considered**:
- **SQLAlchemy Direct**: More flexible but requires manual type hints, more boilerplate
- **Django ORM**: Excellent but tied to Django framework (not compatible with FastAPI)
- **Tortoise ORM**: Async-first but smaller ecosystem, less mature than SQLAlchemy

**Constitution Alignment**: Meets Backend Standards (SQLModel for ORM and schema alignment)

---

## Database Research

### Decision: Neon Serverless PostgreSQL

**Chosen**: Neon Serverless PostgreSQL for persistent database

**Rationale**:
- Serverless PostgreSQL with automatic scaling
- Free tier generous for hackathons (100+ concurrent connections, 3GB storage)
- Managed service (no server maintenance required)
- Excellent for development and testing
- Standard PostgreSQL syntax and features
- Fast connection times for serverless architecture
- Simple connection string configuration via environment variable
- Supports advanced features (indexes, foreign keys, constraints)

**Alternatives Considered**:
- **Supabase**: Excellent but more opinionated (includes auth, storage which duplicates spec requirements)
- **Railway**: Similar to Neon but smaller free tier limits
- **PostgreSQL Self-Hosted**: Too complex for hackathon (requires server management, backups, scaling)

**Constitution Alignment**: Meets Backend Standards (Neon Serverless PostgreSQL)

---

## Authentication Library Research (Frontend)

### Decision: Better Auth

**Chosen**: Better Auth for frontend authentication flow

**Rationale**:
- Modern, secure authentication library for Next.js
- Simpler configuration than NextAuth
- Built-in session management
- Support for multiple providers (email/password for Phase II)
- Excellent TypeScript support
- Secure defaults (httpOnly cookies, CSRF protection)
- Good documentation and examples
- Lightweight (no bloat for Phase II scope)

**Alternatives Considered**:
- **NextAuth.js**: Industry standard but more complex configuration, heavier bundle size
- **Supabase Auth**: Tied to Supabase (adds dependency on Supabase beyond database)
- **Custom JWT Implementation**: Too complex, reinvents security-critical code

**Constitution Alignment**: Meets Frontend Standards (Better Auth for frontend authentication flow)

---

## JWT Library Research (Backend)

### Decision: python-jose

**Chosen**: python-jose (JSON Web Token library) for JWT token generation and verification

**Rationale**:
- Pure Python implementation (no dependencies)
- Supports all JWT algorithms (HS256 required for spec)
- Well-maintained and secure
- Simple API for signing and verifying tokens
- Supports token expiration claims
- Good documentation and examples
- Industry standard for JWT in Python

**Alternatives Considered**:
- **Authlib**: More comprehensive (OAuth, etc.) but heavier dependency
- **PyJWT**: Similar to python-jose, both good choices

**Constitution Alignment**: Meets Authentication Standards (JWT token generation and verification)

---

## Password Hashing Library Research

### Decision: Passlib with bcrypt

**Chosen**: Passlib with bcrypt for secure password hashing

**Rationale**:
- bcrypt is industry standard for password hashing
- Automatic salt generation
- Configurable work factor (adjusts to hardware improvements)
- Time-proven security (resistant to rainbow table attacks)
- Simple API for hashing and verifying passwords
- Well-documented

**Alternatives Considered**:
- **Argon2**: More modern but less mature, smaller ecosystem
- **PBKDF2**: Older algorithm, bcrypt preferred

**Constitution Alignment**: Meets Functional Requirement FR-025 (System MUST store user passwords securely using strong cryptographic hashing)

---

## API Client Research (Frontend)

### Decision: Native fetch with Centralized Wrapper

**Chosen**: Native fetch API with centralized client wrapper for authentication and error handling

**Rationale**:
- Native browser API (no additional dependencies)
- Centralized wrapper reduces boilerplate
- Automatic JWT token injection from Better Auth session
- Consistent error handling across all API calls
- Type-safe request/response functions with TypeScript
- Base URL configuration via environment variable
- Interceptor pattern for authentication headers and error handling

**Alternatives Considered**:
- **Axios**: Popular but adds ~13KB bundle, native fetch provides same features
- **ky**: Lightweight but less common, smaller ecosystem

**Constitution Alignment**: Meets Frontend Standards (Centralized API client for all backend communication)

---

## Testing Framework Research

### Decision: pytest (Backend)

**Chosen**: pytest for backend testing framework

**Rationale**:
- Industry standard for Python testing
- Simple, readable test syntax
- Powerful fixtures for test setup/teardown
- Excellent async support
- Good integration with FastAPI TestClient
- Coverage reporting built-in
- Large plugin ecosystem

**Alternatives Considered**:
- **unittest**: Built-in but verbose, less Pythonic syntax

**Constitution Alignment**: Meets Testing requirement (pytest for backend)

### Decision: Next.js Testing Utilities (Frontend - Optional)

**Chosen**: Next.js built-in testing utilities (Jest, React Testing Library)

**Rationale**:
- Included with Next.js (no additional setup)
- Supports component testing with React Testing Library
- Good TypeScript support
- Mocking and snapshot testing supported

**Alternatives Considered**:
- **Playwright**: Excellent for E2E testing but adds complexity for Phase II scope
- **Cypress**: Similar to Playwright, heavier for initial implementation

**Note**: Per spec, frontend tests are optional. Focus on backend contract tests first.

---

## Summary

All technology choices align with:
- Constitution principles (Spec-Driven Development, Separation of Concerns, Security by Default)
- Technical standards (FastAPI, SQLModel, Next.js 16+, Better Auth, Neon PostgreSQL)
- Feature requirements (25 functional requirements, authentication, multi-user isolation)
- Hackathon constraints (timeline, complexity, single-source of truth)

**Next Step**: Proceed to data model design and API contracts.
