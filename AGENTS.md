You are the lead software engineer responsible for building a portfolio project called "PropQuery".

IMPORTANT CONTEXT:
This project is being developed as a portfolio project specifically targeted toward a Software Engineer Trainee role at a property-management software company.

The project should demonstrate:
- Strong SQL knowledge
- Relational database design
- SQL reporting
- Application support workflows
- Troubleshooting
- Backend development
- REST API design
- Query performance optimization
- Unit testing
- Clean code and maintainable architecture

The application is NOT intended to be a production SaaS product. It is a realistic enterprise-style portfolio project that should be technically credible and easy to explain in a technical interview.

TECH STACK:
Frontend:
- React
- Vite
- Tailwind CSS
- JavaScript/TypeScript only if already configured; do not unnecessarily migrate the project

Backend:
- Python
- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL
- Alembic
- Pytest

Development:
- Git/GitHub
- Docker/Docker Compose where useful
- Postman-compatible REST APIs

PROJECT NAME:
PropQuery
Property Management Reporting & Application Support System

CORE REQUIREMENT:
The backend and database are more important than visual complexity.

Do NOT build a shallow CRUD demo.

The application must demonstrate meaningful relational data, non-trivial SQL queries, reporting, support-ticket workflows, validation, error handling, testing and database performance optimization.

UI REQUIREMENTS:
The UI should look like a professional enterprise property-management application.

It must NOT look AI-generated, overly futuristic, flashy, or like a generic SaaS landing page.

Use a restrained professional beige/cream visual language.

Preferred palette:
- Warm beige / cream background
- Off-white cards
- Dark brown/charcoal text
- Muted brown/taupe secondary elements
- One restrained accent color for actions/statuses

Avoid:
- Neon colors
- Purple AI gradients
- Excessive glassmorphism
- Excessive rounded cards
- Huge dashboard cards
- Excessive animations
- Decorative gradients
- Random icons everywhere
- Marketing-style UI

The UI should prioritize information density, readability and usability.

ARCHITECTURE REQUIREMENTS:
Use clean architecture principles.

Backend should be organized approximately as:

backend/
    app/
        main.py
        core/
            config.py
            database.py
            logging.py
        models/
        schemas/
        repositories/
        services/
        api/
            routes/
        utils/
    tests/
    alembic/
    requirements.txt

Keep responsibilities separated:

API routes
    ↓
Services / business logic
    ↓
Repositories / data access
    ↓
SQLAlchemy
    ↓
PostgreSQL

Do not place business logic directly inside route handlers.

Do not put raw SQL randomly throughout the application.

Use dependency injection where appropriate.

Use Pydantic schemas for request/response validation.

Use SQLAlchemy models for database entities.

Use service classes/functions for business rules.

Use repository/data-access functions for persistence.

Use centralized configuration.

Use environment variables for secrets and database credentials.

Never hardcode credentials.

DATABASE:
Design a normalized relational PostgreSQL database.

Core entities:

Property
Unit
Tenant
Lease
Payment
MaintenanceRequest
SupportTicket
SupportTicketUpdate

Relationships should be properly modeled using foreign keys.

Use:
- Primary keys
- Foreign keys
- Unique constraints
- NOT NULL constraints
- CHECK constraints where appropriate
- Indexes where justified
- Created/updated timestamps

The database should contain realistic seed data.

CORE FUNCTIONALITY:

1. Dashboard
Display:
- Total properties
- Total units
- Occupied units
- Vacant units
- Occupancy rate
- Monthly expected rent
- Collected rent
- Outstanding rent
- Open maintenance requests
- Open support tickets

2. Property Management
Support:
- Create property
- View properties
- View property details
- Update property
- Delete property where safe

3. Unit Management
Support:
- Create units
- Assign units to properties
- Track occupancy status
- View unit details
- Track current tenant/lease

4. Tenant Management
Support:
- Add tenant
- View tenant
- Update tenant
- View lease/payment information

5. Lease Management
Track:
- Tenant
- Unit
- Start date
- End date
- Monthly rent
- Security deposit
- Lease status

6. Payment Management
Track:
- Payment date
- Amount
- Payment status
- Lease
- Payment reference

7. Maintenance Requests
Track:
- Property
- Unit
- Description
- Priority
- Status
- Created date
- Resolved date
- Resolution notes

8. APPLICATION SUPPORT MODULE

This is one of the most important parts of the project.

Support tickets should contain:
- Ticket ID
- Title
- Description
- Category
- Priority
- Status
- Related property/unit/tenant where applicable
- Assigned engineer
- Created timestamp
- Updated timestamp
- Resolved timestamp
- Resolution notes

Workflow:

OPEN
→ INVESTIGATING
→ RESOLVED

Allow support updates/history to be stored.

Example:

Ticket:
"Tenant payment missing from monthly report"

Engineer:
"Investigating payment transaction and reporting query"

Resolution:
"Payment record existed but was excluded because of an incorrect date filter."

The system should demonstrate realistic troubleshooting.

9. SQL REPORTING MODULE

This is a major feature.

Create meaningful reports using SQL.

At minimum:

A. Property Occupancy Report
- Property
- Total units
- Occupied units
- Vacant units
- Occupancy percentage

B. Rent Collection Report
- Property
- Expected rent
- Collected rent
- Outstanding amount
- Collection percentage

C. Tenant Payment History

D. Outstanding Payments Report

E. Maintenance Performance Report
- Total requests
- Open requests
- Resolved requests
- Average resolution time

F. Property Financial Summary

G. Monthly Revenue Report

Use meaningful SQL involving:
- JOIN
- LEFT JOIN
- GROUP BY
- HAVING
- CASE
- Aggregate functions
- Subqueries where appropriate
- CTEs where useful
- Views where useful

Do not artificially make queries complex just to show complexity.

10. QUERY PERFORMANCE

Implement a small performance-analysis section.

Demonstrate:

EXPLAIN
EXPLAIN ANALYZE

Identify at least one inefficient query.

Create an appropriate index.

Compare query performance before and after indexing.

Document:
- Problem
- Query
- Execution plan
- Optimization
- Result

Do not fabricate performance numbers.

Use actual results from the local PostgreSQL environment.

11. TESTING

Use Pytest.

Test:
- API validation
- Service/business logic
- Repository operations where practical
- CRUD operations
- Support-ticket state transitions
- Important reporting logic
- Error handling

The project should contain a meaningful test suite, not just one placeholder test.

12. ERROR HANDLING

Implement:
- Consistent HTTP status codes
- Pydantic validation
- Not-found errors
- Conflict errors
- Database errors
- Centralized exception handling where appropriate

Do not expose internal stack traces to API users.

13. LOGGING

Implement useful backend logging.

Log:
- API errors
- Important application events
- Support-ticket operations
- Database/application failures

Do not log passwords, tokens or sensitive credentials.

14. API DOCUMENTATION

FastAPI's OpenAPI documentation should be usable.

Use:
- Clear endpoint names
- Meaningful request/response schemas
- HTTP status codes
- Descriptions
- Tags

15. SECURITY BASICS

Implement sensible security practices:
- Environment variables
- Input validation
- SQLAlchemy parameterization
- No hardcoded credentials
- CORS configuration
- No sensitive information in logs

Authentication is NOT required for the first version unless it can be implemented cleanly without distracting from the core project.

16. FRONTEND

The frontend should consume the backend REST APIs.

Pages:

/dashboard
/properties
/units
/tenants
/leases
/payments
/maintenance
/support
/reports

The UI should feel like an internal enterprise application.

Prioritize:
- Tables
- Filters
- Search
- Sorting
- Status indicators
- Forms
- Detail views
- Report views

Avoid unnecessary animations.

17. DOCUMENTATION

Create a high-quality README containing:

- Project overview
- Problem statement
- Features
- Architecture
- Technology stack
- Database schema
- API structure
- SQL reporting
- Performance optimization
- Testing
- Setup instructions
- Environment variables
- Example API calls
- Screenshots placeholder section
- Future improvements

Also create:

docs/
    architecture.md
    database.md
    api.md
    sql-reporting.md
    performance.md
    testing.md

18. DEVELOPMENT RULES

Follow clean code practices.

Rules:
- Meaningful variable/function names
- Small focused functions
- Avoid duplicated logic
- Avoid giant files
- Avoid giant functions
- Type hints in Python
- Pydantic schemas
- Clear module boundaries
- Consistent error handling
- No unnecessary dependencies
- No unnecessary abstractions
- No dead code
- No commented-out code
- No fake functionality
- No placeholder implementations presented as complete features

IMPORTANT:
Do not generate the entire application blindly in one step.

First:
1. Inspect the existing Vite project.
2. Propose the final repository structure.
3. Identify required dependencies.
4. Design the database schema.
5. Explain the implementation phases.
6. Then implement Phase 1.

After each major phase:
- Run the application
- Run tests
- Check for errors
- Fix issues
- Summarize what changed

Do not change technologies without a strong reason.

Do not over-engineer the application.

The goal is a technically strong, realistic and interview-defensible portfolio project.