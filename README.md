# PropQuery 🏢

> **Property Management Reporting & Application Support System**

PropQuery is an enterprise-grade portfolio project demonstrating clean architecture, advanced SQL reporting, database performance optimization, and rigorous application support workflows. Built as a technical showcase for backend engineering, relational database design, and robust API development.

---

## 🎯 Project Overview

This application manages the core lifecycle of property management—properties, units, tenants, leases, payments, and maintenance—while prioritizing two critical technical requirements:

1. **SQL Reporting**: Generation of complex business intelligence reports (Occupancy, Rent Collection, Performance) using advanced PostgreSQL querying (CTEs, Aggregate functions, JOINs, CASE statements).
2. **Application Support Workflows**: A rigorous support ticketing system that enforces strict state transitions (`OPEN` → `INVESTIGATING` → `RESOLVED`) and automatically manages audit trails for troubleshooting.

The frontend is purposefully designed using a restrained "beige/cream" enterprise aesthetic, prioritizing data density and usability over flashy marketing elements.

---

## 🛠️ Technology Stack

**Backend**
- **Python 3.12**
- **FastAPI** (REST APIs & Dependency Injection)
- **SQLAlchemy 2.0** (ORM & Raw SQL Execution)
- **PostgreSQL 18.6** (Relational Database)
- **Pytest** (Automated Testing with In-Memory SQLite)
- **JWT (python-jose & passlib)** (Authentication Gateway)

**Frontend**
- **React 19**
- **Vite**
- **Tailwind CSS v4** (Strict Enterprise Design System)
- **Axios** (API Client with Interceptors)
- **React Router**

---

## 📂 Architecture

The backend strictly adheres to Clean Architecture principles, ensuring separation of concerns:

```text
app/
 ├── api/routes/      # FastAPI endpoint definitions
 ├── services/        # Business logic & state transitions
 ├── repositories/    # SQLAlchemy data access & query execution
 ├── schemas/         # Pydantic validation models (In/Out)
 ├── models/          # SQLAlchemy table schemas
 ├── core/            # Config, Security (JWT), and DB setup
```
*Flow: Route → Service → Repository → Database*

---

## 📊 SQL Reporting & Performance Optimization

### Reporting Module
The system features 7 core SQL reports executed natively via SQLAlchemy `text()`, including:
- **Property Occupancy Report**: Aggregates total, occupied, and vacant units to generate occupancy percentages.
- **Rent Collection Report**: Compares expected lease amounts vs collected payments.
- **Maintenance Performance**: Calculates ticket resolution times and open backlogs.

### Query Performance (`docs/performance.md`)
A key focus of this project is query optimization. Using `EXPLAIN ANALYZE`, we identified sequential scan bottlenecks on large aggregated views (e.g., Monthly Revenue). We designed and implemented **Covering Indexes** (e.g., `CREATE INDEX ix_payments_covering ON payments(payment_date, amount, status) INCLUDE (lease_id)`) to force highly efficient Index-Only scans, significantly reducing query execution time.

---

## ✅ Testing

The project includes an automated test suite located in `tests/`, utilizing `pytest` and an in-memory SQLite database.

Tests cover:
- CRUD API Validation
- Support Ticket state transition enforcement (Audit logging)
- Security & JWT generation

---

## 🚀 Setup Instructions

### 1. Prerequisites
- Python 3.12+
- Node.js & npm
- PostgreSQL running locally

### 2. Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Environment Setup (in your shell)
set DATABASE_URL="postgresql://propquery_user:propquery_pass@localhost:5432/propquery"

# Start Server
python -m uvicorn app.main:app --reload
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 4. Default Admin Credentials
- **Email:** `admin@propquery.com`
- **Password:** `password123`

---

## 🔮 Future Improvements
- Implement Alembic for formal database migrations.
- Expand test coverage to the React frontend using Vitest/React Testing Library.
- Implement Docker & Docker Compose for one-click environment spin up.
