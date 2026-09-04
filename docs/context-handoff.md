# PropQuery — Context Handoff for New Chat

## Project Overview

PropQuery is a portfolio project for a Software Engineer Trainee role at a property-management software company. Full requirements are in `d:\propquery\AGENTS.md` and `d:\propquery\docs\prd.md`.

**Tech Stack**: React/Vite (frontend), Python/FastAPI/SQLAlchemy/PostgreSQL (backend)

---

## What Has Been Completed (Phase 1)

### Environment
- **PostgreSQL 18** installed locally on Windows
- **Database**: `propquery` on `localhost:5432`
- **DB User**: `propquery_user` / `propquery_pass`
- **Superuser**: `postgres` / `12345`
- **psql path**: `C:\Program Files\PostgreSQL\18\bin\psql.exe`
- **Python 3.12** with all backend deps installed globally (not in venv)
- **Node 24** with frontend Vite scaffold

### Backend Scaffold (`d:\propquery\backend\`)
All directories and files created:

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app with CORS, health endpoint
│   ├── core/
│   │   ├── config.py        # Pydantic Settings (loads from .env)
│   │   ├── database.py      # SQLAlchemy engine, session, Base, get_db
│   │   └── logging.py       # Structured logging setup
│   ├── models/
│   │   ├── __init__.py      # Imports all models for Alembic discovery
│   │   ├── property.py      # Property model
│   │   ├── unit.py          # Unit model (CHECK: status, market_rent, beds, baths)
│   │   ├── tenant.py        # Tenant model (unique email)
│   │   ├── lease.py         # Lease model (CHECK: dates, rent, deposit, status)
│   │   ├── payment.py       # Payment model (CHECK: amount > 0, status enum)
│   │   ├── maintenance.py   # MaintenanceRequest model (CHECK: priority, status)
│   │   └── support.py       # SupportTicket + SupportTicketUpdate (CHECK: status, priority, category)
│   ├── schemas/__init__.py  # Empty — Phase 2
│   ├── repositories/__init__.py  # Empty — Phase 2
│   ├── services/__init__.py      # Empty — Phase 2
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/__init__.py    # Empty — Phase 2
│   └── utils/__init__.py         # Empty — Phase 2
├── tests/__init__.py              # Empty — Phase 6
├── alembic/
│   ├── env.py               # Configured: imports models, reads DB URL from config
│   └── versions/
│       └── 169611f88fa5_initial_schema.py  # Initial migration (applied)
├── alembic.ini              # DB URL set in env.py, not hardcoded here
├── requirements.txt
├── .env                     # DATABASE_URL=postgresql://propquery_user:propquery_pass@localhost:5432/propquery
└── .env.example
```

### Database State
All 8 tables created and seeded:

| Table | Rows | Key Constraints |
|-------|------|-----------------|
| properties | 5 | PK, indexes |
| units | 20 | FK→properties, CHECK(status IN occupied/vacant), CHECK(market_rent>0) |
| tenants | 15 | PK, unique(email) |
| leases | 18 | FK→units, FK→tenants, CHECK(end_date>start_date), CHECK(rent>0), CHECK(status) |
| payments | 93 | FK→leases, CHECK(amount>0), CHECK(status), index(payment_date) |
| maintenance_requests | 12 | FK→units, CHECK(priority), CHECK(status) |
| support_tickets | 8 | FK→properties(nullable), FK→units(nullable), FK→tenants(nullable), CHECK(status/priority/category) |
| support_ticket_updates | 15 | FK→support_tickets |

**Unit occupancy**: 14 occupied, 6 vacant across 5 properties.
**Lease statuses**: 14 active, 3 expired, 1 terminated.
**Payment statuses**: mostly completed, a few pending/failed for realistic reporting.
**Maintenance statuses**: 6 resolved, 2 in_progress, 3 open, 1 resolved.
**Ticket statuses**: 3 resolved, 2 investigating, 3 open — with full update histories.

### Seed Data Script
Located at `d:\propquery\database\seed.py`. Run with:
```bash
cd d:\propquery
python -c "import sys; sys.path.insert(0, '.'); from database.seed import run_seed; run_seed()"
```

### Frontend State
Fresh Vite + React 19 scaffold at `d:\propquery\frontend\`. Default template — **no modifications yet**. No Tailwind, no router installed. Will be set up in Phase 7.

---

## What's Next (Phase 2 — Backend Core)

Build the full CRUD REST API with clean layer separation:

1. **Pydantic schemas** (`app/schemas/`) — create/update/response schemas for each entity
2. **Repository layer** (`app/repositories/`) — data access functions using SQLAlchemy
3. **Service layer** (`app/services/`) — business logic, validation beyond Pydantic
4. **API routes** (`app/api/routes/`) — REST endpoints for all entities + dashboard
5. **Exception handling** (`app/utils/exceptions.py`) — custom exceptions + FastAPI handlers
6. **Wire everything up** in `app/main.py` — include routers, register exception handlers

### Architecture Pattern
```
API Routes → Services → Repositories → SQLAlchemy → PostgreSQL
```
No business logic in route handlers. No raw SQL scattered around.

### Key Decisions Already Made
- **JavaScript (JSX)** for frontend — no TypeScript migration
- **No SRS document** — PRD + architecture docs are sufficient
- **Local PostgreSQL** — not Docker, not cloud
- **No authentication** for v1

---

## Important File Paths
- Project root: `d:\propquery\`
- AGENTS.md (full spec): `d:\propquery\AGENTS.md`
- PRD: `d:\propquery\docs\prd.md`
- Backend: `d:\propquery\backend\`
- Frontend: `d:\propquery\frontend\`
- Seed script: `d:\propquery\database\seed.py`
- psql: `C:\Program Files\PostgreSQL\18\bin\psql.exe`

## Useful Commands
```powershell
# Start backend
cd d:\propquery\backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# Run Alembic migration
cd d:\propquery\backend
python -m alembic upgrade head

# Query database
$env:PGPASSWORD='propquery_pass'; & "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U propquery_user -d propquery

# Reseed database
cd d:\propquery
python -c "import sys; sys.path.insert(0, '.'); from database.seed import run_seed; run_seed()"
```
