# Quickstart Guide: Phase II Full-Stack Web Application

**Feature Branch**: `002-phase2-webapp`
**Created**: 2026-01-02
**Purpose**: Developer quickstart guide for setting up and running Phase II full-stack todo application

## Prerequisites

- **Python 3.11+**: Backend runtime
- **Node.js 18+**: Frontend runtime
- **npm or yarn**: Frontend package manager
- **pip**: Python package manager
- **Neon PostgreSQL Account**: Free tier available at https://neon.tech
- **Git**: Version control

## Project Structure

```
ph1/
├── backend/              # FastAPI backend
├── frontend/             # Next.js 16+ frontend
└── specs/002-phase2-webapp/  # Specifications and documentation
```

## Environment Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd ph1
git checkout 002-phase2-webapp
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
```

### 3. Configure Backend Environment

Edit `backend/.env` with your values:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@ep-xyz.us-east-2.aws.neon.tech/neondb?sslmode=require

# JWT Secret (generate a strong random string)
JWT_SECRET=your-super-secret-jwt-key-here-change-in-production

# Application Configuration
API_HOST=http://localhost:8000
CORS_ORIGINS=http://localhost:3000

# Performance Configuration
MAX_CONNECTION_POOL_SIZE=10
```

**Getting Neon Database URL**:
1. Sign up at https://neon.tech
2. Create a new project
3. Copy the connection string (looks like `postgresql://user:password@ep-xyz.aws.neon.tech/neondb?sslmode=require`)
4. Paste into `DATABASE_URL` in `.env` file

**Generating JWT Secret**:
```bash
# Generate secure random string
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

### 4. Initialize Database

```bash
# Run database migrations (creates users and tasks tables)
cd backend
python -m src.models

# Or use Alembic if migrations are set up:
alembic upgrade head
```

### 5. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Copy environment template
cp .env.local.example .env.local
```

### 6. Configure Frontend Environment

Edit `frontend/.env.local` with your values:

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000/v1

# Better Auth Configuration (if using Better Auth)
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-nextauth-secret-here
```

**Generating NextAuth Secret**:
```bash
# Generate secure random string
openssl rand -base64 32
```

### 7. Create First User (via API)

**Option 1: Use API directly**:

```bash
curl -X POST http://localhost:8000/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "securepassword123"
  }'
```

**Option 2: Use frontend registration page**:

1. Open `http://localhost:3000` in browser
2. Click "Register" link
3. Fill in email and password
4. Submit form

## Running the Application

### Run Backend

```bash
cd backend
source venv/bin/activate  # Activate virtual environment

# Start FastAPI development server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at:
- API: http://localhost:8000
- API Docs (Swagger): http://localhost:8000/docs
- Alternative Docs (Redoc): http://localhost:8000/redoc

### Run Frontend

```bash
cd frontend

# Start Next.js development server
npm run dev
```

Frontend will be available at:
- Application: http://localhost:3000

### Run Both Services (Simultaneously)

**Using two terminal windows**:

**Terminal 1**:
```bash
cd backend
source venv/bin/activate
uvicorn src.main:app --reload --port 8000
```

**Terminal 2**:
```bash
cd frontend
npm run dev
```

**Or use concurrently**:

```bash
# Install concurrently globally
npm install -g concurrently

# Run both services from root
concurrently "cd backend && source venv/bin/activate && uvicorn src.main:app --reload --port 8000" "cd frontend && npm run dev"
```

## Development Workflow

### 1. View API Documentation

Open http://localhost:8000/docs in browser. This interactive Swagger UI shows:
- All available endpoints
- Request/response schemas
- Try out API calls directly
- JWT authentication flow

### 2. Test Authentication

**Register user**:
```bash
curl -X POST http://localhost:8000/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

**Login and get JWT**:
```bash
curl -X POST http://localhost:8000/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

Save the `access_token` from response for authenticated requests.

### 3. Test Task Operations

**Create task** (requires JWT):
```bash
curl -X POST http://localhost:8000/v1/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <YOUR_JWT_TOKEN>" \
  -d '{"title": "My first task", "description": "Test task description"}'
```

**List tasks** (requires JWT):
```bash
curl http://localhost:8000/v1/tasks \
  -H "Authorization: Bearer <YOUR_JWT_TOKEN>"
```

**Update task** (requires JWT):
```bash
curl -X PUT http://localhost:8000/v1/tasks/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <YOUR_JWT_TOKEN>" \
  -d '{"status": "completed"}'
```

**Delete task** (requires JWT):
```bash
curl -X DELETE http://localhost:8000/v1/tasks/1 \
  -H "Authorization: Bearer <YOUR_JWT_TOKEN>"
```

## Testing Multi-User Data Isolation

### 1. Create User A

```bash
curl -X POST http://localhost:8000/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "usera@example.com", "password": "password123"}'

# Save token as TOKEN_A
```

### 2. Create User B

```bash
curl -X POST http://localhost:8000/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "userb@example.com", "password": "password123"}'

# Save token as TOKEN_B
```

### 3. User A creates task

```bash
curl -X POST http://localhost:8000/v1/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN_A>" \
  -d '{"title": "User A task"}'
```

### 4. Verify User B cannot see User A's task

```bash
# List User B's tasks (should be empty)
curl http://localhost:8000/v1/tasks \
  -H "Authorization: Bearer <TOKEN_B>"
```

### 5. Verify User B cannot access User A's task by ID

```bash
# Attempt to access User A's task (should get 403 Forbidden)
curl http://localhost:8000/v1/tasks/1 \
  -H "Authorization: Bearer <TOKEN_B>"
```

Expected response: `403 Forbidden` with "You don't have permission to perform this action" message.

## Troubleshooting

### Database Connection Issues

**Symptom**: "Connection refused" or "database does not exist"

**Solutions**:
1. Verify `DATABASE_URL` in `.env` is correct
2. Check Neon project is active (not paused)
3. Ensure SSL mode is enabled (`sslmode=require`)
4. Test connection: `psql $DATABASE_URL`

### JWT Token Issues

**Symptom**: "401 Unauthorized" errors even with correct credentials

**Solutions**:
1. Verify `JWT_SECRET` is set in backend `.env`
2. Check token is included in `Authorization: Bearer <token>` header
3. Verify token hasn't expired (default 24 hours)
4. Check JWT secret matches between login and verification

### CORS Issues

**Symptom**: "CORS policy blocked request" in browser console

**Solutions**:
1. Verify `CORS_ORIGINS` in backend `.env` includes frontend URL
2. Ensure frontend URL includes protocol (`http://` not just `localhost:3000`)
3. Check backend CORS middleware configuration in `src/main.py`

### Frontend Build Issues

**Symptom**: Module not found or TypeScript errors

**Solutions**:
1. Run `npm install` to install dependencies
2. Delete `node_modules` and run `npm install` again
3. Check TypeScript version matches requirements (`npm list typescript`)
4. Verify API client uses correct base URL from `NEXT_PUBLIC_API_URL`

### Password Issues

**Symptom**: "Authentication failed" on login

**Solutions**:
1. Verify password is at least 8 characters
2. Check email is correct (case-insensitive)
3. Ensure user is registered (check `/auth/register` response)
4. Clear browser cache if recently changed password

## Production Deployment

### Backend Deployment (Production Checklist)

1. **Environment Variables**:
   - Set `DATABASE_URL` to production Neon database
   - Set strong, unique `JWT_SECRET` (not default value)
   - Set `CORS_ORIGINS` to production frontend domain
   - Set `API_HOST` to production domain

2. **Database**:
   - Use production Neon database (not dev copy)
   - Run migrations: `alembic upgrade head`
   - Verify database indexes are created

3. **Security**:
   - Enable HTTPS (requirement per specification)
   - Never commit `.env` file (use secrets management)
   - Review error messages don't leak sensitive information
   - Set appropriate CORS origins (not wildcard `*`)

4. **Performance**:
   - Configure appropriate connection pool size
   - Add health check endpoint (`/health`)
   - Enable production logging

### Frontend Deployment (Production Checklist)

1. **Environment Variables**:
   - Set `NEXT_PUBLIC_API_URL` to production backend API
   - Set `NEXTAUTH_URL` to production domain
   - Set strong `NEXTAUTH_SECRET`

2. **Build**:
   ```bash
   npm run build
   ```

3. **Deployment**:
   - Deploy built files to Vercel, Netlify, or CDN
   - Configure custom domain
   - Set environment variables in deployment platform

## Monitoring & Logs

### Backend Logs

FastAPI logs to console by default. For production:

```bash
# Start with logging configuration
uvicorn src.main:app --log-level info
```

### Database Performance

Monitor Neon dashboard for:
- Connection pool usage
- Query performance
- Storage usage
- Slow queries

### Frontend Monitoring

Add error tracking (e.g., Sentry) if needed (out of Phase II scope).

## Development Tips

1. **Hot Reload**: Both FastAPI (`--reload` flag) and Next.js (`npm run dev`) support hot reload during development.

2. **API Testing**: Use Swagger UI at `/docs` for interactive API testing without frontend.

3. **Database Inspection**: Use Neon dashboard SQL Editor to inspect data directly during development.

4. **Type Checking**: Both Python (type hints) and TypeScript provide type safety. Fix type errors early.

5. **Git Ignore**: Ensure `.env`, `venv/`, `node_modules/`, `__pycache__` are in `.gitignore`.

6. **Spec Alignment**: Reference specs using `@specs` paths in code comments for traceability.

7. **Test First**: Write tests before implementing features when possible. Follow `/sp.tasks` output for test implementation.

## Next Steps

After quickstart setup:

1. Run `/sp.tasks` to generate actionable task breakdown
2. Follow tasks in implementation plan ([plan.md](plan.md))
3. Test all endpoints against API contracts ([contracts/endpoints.md](contracts/endpoints.md))
4. Validate multi-user data isolation (User A vs. User B tests)
5. Verify all success criteria (SC-001 through SC-008) are met
6. Review code against specification ([spec.md](spec.md))

## Support

- **Specifications**: `/specs/002-phase2-webapp/`
- **API Documentation**: http://localhost:8000/docs (when backend running)
- **Constitution**: `.specify/memory/constitution.md`
- **Claude Code**: Use `/sp.plan`, `/sp.tasks`, `/sp.implement` commands

## Summary

This quickstart guide provides:
- Prerequisites and project structure
- Step-by-step environment setup
- Backend and frontend configuration
- Running both services
- Testing authentication and task operations
- Multi-user data isolation validation
- Troubleshooting common issues
- Production deployment checklist
- Development tips and best practices

All setup instructions align with [plan.md](plan.md) architecture decisions and [data-model.md](data-model.md) database schema.
