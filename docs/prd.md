```
# PropQuery — Product Requirements Document
```

```
## 1. Product Overview
```

```
PropQuery is an enterprise-style property management reporting and application-
support system.
```

```
It manages property-related operational data and provides SQL-powered reporting,
support-ticket management, maintenance tracking, and financial summaries.
```

```
The primary purpose of the project is to demonstrate:
```

- `Relational database design` 

- `SQL` 

- `Backend development` 

- `Application support` 

- `Troubleshooting` 

- `Reporting` 

- `Performance optimization` 

- `Software testing` 

```
---
```

```
## 2. Problem Statement
```

```
Property-management systems contain multiple interconnected datasets such as
properties, units, tenants, leases, and payments.
```

```
Users need a system that can:
```

- `Maintain this information` 

- `Retrieve information efficiently` 

- `Generate operational reports` 

- `Identify payment and maintenance issues` 

- `Track software/application issues` 

- `Support troubleshooting and resolution` 

```
PropQuery provides a simplified implementation of such a system.
```

```
---
```

```
## 3. Target Users
```

```
### 3.1 Property Administrator
```

```
Uses the system to:
```

- `View properties` 

- `Track occupancy` 

- `Monitor rent` 

- `Review maintenance requests` 

```
### 3.2 Finance / Reporting User
```

```
Uses the system for:
```

```
- Rent reports
```

- `Payment reports` 

- `Outstanding balance reports` 

- `Revenue summaries` 

```
### 3.3 Application Support Engineer
```

```
Uses the system for:
```

```
- Support tickets
```

```
- Troubleshooting history
```

```
- Resolution notes
```

- `Application issue tracking` 

```
---
```

```
# 4. Functional Requirements
```

```
## FR-01 — Property Management
```

```
The system shall allow users to:
```

```
- Create properties
- View properties
- Update properties
```

```
- Manage property information
```

```
---
```

```
## FR-02 — Unit Management
```

```
The system shall:
```

```
- Associate units with properties
```

```
- Maintain unit information
```

```
- Track occupancy status
```

- `Allow users to view unit details` 

```
---
```

```
## FR-03 — Tenant Management
```

```
The system shall:
```

```
- Maintain tenant information
```

- `Associate tenants with leases` 

```
- Allow users to view tenant details
```

- `Allow users to update tenant information` 

```
---
```

```
## FR-04 — Lease Management
```

```
The system shall maintain lease details between tenants and units.
```

```
Lease information shall include, where applicable:
```

```
- Tenant
- Unit
- Start date
- End date
- Monthly rent
- Security deposit
- Lease status
```

```
---
```

```
## FR-05 — Payment Management
```

```
The system shall:
```

```
- Record payment information
```

```
- Associate payments with leases
```

- `Retrieve payment history` 

- `Track payment status` 

- `Support payment reporting` 

```
---
```

```
## FR-06 — Maintenance Management
```

```
The system shall allow users to:
```

```
- Create maintenance requests
```

```
- Associate requests with properties and/or units
```

```
- Set request priority
```

```
- Track request status
- Record resolution information
```

```
- View maintenance history
```

```
---
```

```
## FR-07 — Support Ticket Management
```

```
The system shall allow application issues to be:
```

```
- Created
- Viewed
- Updated
- Assigned
- Tracked
- Resolved
```

```
Support tickets should contain information such as:
```

```
- Ticket ID
- Title
- Description
- Category
- Priority
- Status
- Related property
- Related unit
- Related tenant
- Assigned engineer
- Created timestamp
- Updated timestamp
- Resolved timestamp
- Resolution notes
```

```
---
```

```
## FR-08 — Support Workflow
```

```
Support tickets shall follow a controlled workflow:
```

```
```text
OPEN
  |
  v
INVESTIGATING
  |
  v
RESOLVED
```

```
The system should prevent invalid state transitions where appropriate.
```

```
Support-ticket updates should be stored as historical records.
Example:
Ticket: Payment missing from monthly report
Status: OPEN
        ↓
```

```
Status: INVESTIGATING
Engineer investigates payment transaction
and reporting query.
```

```
Status: RESOLVED
```

```
Resolution:
Payment existed but was excluded because
of an incorrect date filter.
FR-09 — Reporting
The system shall generate SQL-based operational reports.
```

```
Reports should retrieve data directly from the PostgreSQL database through the
backend.
```

```
The reporting system should demonstrate meaningful SQL operations rather than
simply displaying raw database records.
```

```
The reporting layer should support:
```

```
Occupancy analysis
Rent collection analysis
Payment history
Outstanding payments
Maintenance performance
Property financial summaries
Monthly revenue analysis
```

```
SQL should make appropriate use of:
```

```
JOIN
LEFT JOIN
GROUP BY
HAVING
CASE
Aggregate functions
Subqueries where appropriate
Common Table Expressions (CTEs) where useful
SQL views where useful
```

```
Complexity should be justified by the reporting requirement. Queries should not
be made artificially complex.
```

```
FR-10 — Performance Analysis
```

```
The system shall provide a mechanism to analyze and optimize SQL query
performance.
```

```
The project shall demonstrate:
```

```
EXPLAIN
EXPLAIN ANALYZE
Query execution-plan analysis
Identification of inefficient queries
Index creation
Query optimization
Before-and-after comparison
```

```
At least one reporting query should be analyzed and optimized.
```

```
The project must document:
```

```
Original query
Identified performance issue
Execution plan
Optimization applied
Optimized execution plan
Actual performance results
```

```
Performance numbers must be obtained from actual local PostgreSQL execution and
must not be fabricated.
```

```
FR-11 — Testing
```

```
Core functionality shall have automated tests.
```

```
Testing shall cover important:
```

```
API endpoints
Validation rules
Business logic
CRUD operations
Support-ticket workflows
Reporting logic
Error handling
Database operations where appropriate
```

```
The project shall use Pytest.
```

```
5. Database Requirements
```

```
5.1 Database Technology
```

```
The system shall use:
```

```
PostgreSQL
```

# `5.2 Core Entities` 

```
The initial database shall contain the following core entities:
```

```
Property
   |
   └── Unit
          |
          └── Lease
                 |
                 ├── Tenant
                 |
                 └── Payment
```

```
Unit
```

```
 |
 └── MaintenanceRequest
```

```
Property / Unit / Tenant
 |
 └── SupportTicket
        |
```

```
        └── SupportTicketUpdate
5.3 Database Design Principles
```

```
The database must:
```

```
Follow normalized relational database design
Use primary keys
Use foreign keys
Use appropriate unique constraints
Use appropriate NOT NULL constraints
Use CHECK constraints where appropriate
Maintain referential integrity
Use indexes where justified
Store timestamps where appropriate
Avoid unnecessary duplication of data
5.4 Database Migrations
```

```
Database schema changes shall be managed using:
```

```
Alembic
```

```
Do not rely on manually modifying production-like database structures.
```

```
Schema changes should be represented as migrations.
```

# `5.5 Seed Data` 

```
The project shall contain realistic seed data.
```

```
Seed data should be sufficient to demonstrate:
```

```
Multiple properties
Multiple units per property
Occupied and vacant units
Multiple tenants
Active and completed leases
Successful and outstanding payments
Maintenance requests
Support tickets
Ticket updates
```

```
The dataset should be large enough to make SQL reporting meaningful while
remaining lightweight enough for local development.
```

```
6. Reporting Requirements
```

```
6.1 Occupancy Report
```

```
The system shall provide an occupancy report containing:
```

```
Field
Property
Total Units
Occupied Units
Vacant Units
Occupancy %
```

```
Example calculation:
```

```
Occupancy % =
```

```
(Occupied Units / Total Units) × 100
6.2 Rent Collection Report
```

```
The system shall provide a rent collection report containing:
```

```
Field
Property
Expected Rent
Collected Rent
Outstanding Rent
Collection %
Example calculation:
Outstanding Rent =
Expected Rent - Collected Rent
Collection % =
(Collected Rent / Expected Rent) × 100
6.3 Maintenance Performance Report
```

```
The system shall provide a maintenance report containing:
```

```
Field
Property
Total Requests
Open Requests
Resolved Requests
Average Resolution Time
6.4 Payment Report
```

```
The system shall provide a payment report containing:
```

```
Field
Tenant
Lease
Payment Date
Amount
Status
6.5 Property Financial Summary
The system should provide a property-level financial summary containing, where
applicable:
```

```
Property
Total expected rent
Total collected rent
Outstanding rent
Collection percentage
Number of active leases
Number of occupied units
6.6 Monthly Revenue Report
```

```
The system should support monthly revenue analysis.
```

```
The report should allow users to understand:
```

```
Revenue by month
Number of payments
Total collected amount
Outstanding amount where applicable
7. Application Support Requirements
```

```
Application support is a major component of PropQuery.
```

```
The system should simulate a realistic software-support environment.
```

```
7.1 Support Ticket Creation
```

```
A user should be able to create a ticket describing an application issue.
```

```
Example:
```

```
Title:
Payment missing from rent report
Category:
Reporting
Priority:
High
Description:
Payment exists in the payment table but
does not appear in the monthly rent report.
7.2 Ticket Investigation
```

```
Support engineers should be able to:
```

```
Open a ticket
Investigate the issue
Add troubleshooting updates
Record findings
Change priority
Update status
7.3 Ticket Resolution
```

```
When the issue is resolved, the system should store:
```

```
Resolution description
Resolved timestamp
Engineer responsible
Final ticket status
7.4 Support History
```

```
Every important support-ticket update should be retained.
```

```
Example:
```

```
Ticket #1024
```

```
09:30 — Ticket created
09:42 — Assigned to Support Engineer
10:15 — Investigation started
10:45 — SQL reporting query reviewed
11:05 — Incorrect date condition identified
11:20 — Query corrected
11:30 — Ticket resolved
```

```
This history should be stored in the database rather than being generated only
on the frontend.
```

```
8. Backend Requirements
8.1 Backend Technology
```

```
The backend shall use:
```

```
Python
FastAPI
```

```
SQLAlchemy
Pydantic
PostgreSQL
Alembic
8.2 Backend Architecture
```

```
The backend should follow a clean layered architecture.
```

```
Recommended structure:
```

```
backend/
│
├── app/
│   ├── main.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── logging.py
│   │
│   ├── models/
│   │
│   ├── schemas/
│   │
│   ├── repositories/
│   │
│   ├── services/
│   │
│   ├── api/
│   │   └── routes/
│   │
│   └── utils/
│
├── tests/
│
├── alembic/
│
├── requirements.txt
│
└── .env.example
8.3 Separation of Responsibilities
```

```
The architecture should follow:
```

```
API Routes
     |
     v
Service Layer
     |
     v
Repository / Data Access Layer
     |
     v
SQLAlchemy
     |
     v
PostgreSQL
API Layer
```

```
Responsible for:
```

```
HTTP requests
HTTP responses
Request validation
```

```
Authentication/authorization if implemented
Calling service-layer operations
Service Layer
Responsible for:
```

```
Business rules
Workflow logic
Validation beyond simple schema validation
Coordinating multiple repository operations
Repository Layer
```

```
Responsible for:
Database access
Queries
Persistence
Retrieval
```

```
Business logic should not be placed directly inside route handlers.
9. REST API Requirements
```

```
The backend shall expose RESTful endpoints.
Example endpoint structure:
```

```
/api/properties
/api/units
/api/tenants
/api/leases
/api/payments
/api/maintenance
/api/support
/api/reports
```

```
The API should use appropriate HTTP methods:
```

```
GET
POST
PUT/PATCH
DELETE
```

```
Appropriate HTTP status codes should be returned.
```

```
Examples:
```

```
200 OK
201 Created
204 No Content
400 Bad Request
404 Not Found
409 Conflict
422 Unprocessable Entity
500 Internal Server Error
10. Validation Requirements
```

```
Input validation shall be handled using Pydantic schemas.
```

```
Validation should cover:
```

```
Required fields
Data types
Valid dates
```

```
Positive monetary values
Valid statuses
Valid priorities
Valid relationships
```

```
Invalid requests should receive clear and appropriate error responses.
```

# `11. Error Handling Requirements` 

```
The backend shall implement consistent error handling.
```

```
The system should handle:
```

```
Resource not found
Invalid input
Duplicate records
Invalid state transitions
Database errors
Unexpected application errors
```

```
Internal stack traces must not be exposed to API clients.
```

# `12. Logging Requirements` 

```
The backend should implement structured and useful application logging.
```

```
Important events may include:
```

```
Application startup
API errors
Database failures
Support-ticket creation
Support-ticket status changes
Important business operations
```

```
Sensitive information must not be logged.
```

```
Do not log:
```

```
Passwords
Authentication tokens
Database credentials
Other sensitive secrets
13. Security Requirements
```

```
The initial project does not require a complex authentication system unless it
can be implemented cleanly without distracting from the core functionality.
```

```
The application shall nevertheless follow basic security practices.
```

```
Requirements include:
```

```
No hardcoded database credentials
Environment variables for configuration
Input validation
Safe database queries
SQLAlchemy parameterization
Appropriate CORS configuration
No sensitive information in logs
No secrets committed to Git
```

```
An .env.example file should be included.
```

```
14. Testing Requirements
```

```
The project shall use:
```

```
Pytest
```

```
Testing should be organized into meaningful categories.
```

```
Example:
```

```
tests/
│
├── unit/
│   ├── test_services.py
│   └── test_validation.py
│
├── integration/
│   ├── test_properties.py
│   ├── test_payments.py
│   └── test_support.py
│
└── conftest.py
```

```
The exact structure may be adjusted if a simpler organization is more
appropriate.
```

```
14.1 Unit Tests
```

```
Test:
Business rules
Service functions
Validation
Ticket state transitions
Calculations
14.2 API Tests
```

```
Test:
GET endpoints
POST endpoints
UPDATE endpoints
DELETE endpoints
Invalid requests
Missing resources
Conflict cases
14.3 Reporting Tests
Important report calculations should be tested.
Examples:
Occupancy percentage
Outstanding rent
Collection percentage
Maintenance statistics
15. Performance Requirements
```

```
The project must demonstrate practical SQL performance analysis.
```

```
15.1 Query Analysis
```

```
Use:
```

```
EXPLAIN
```

```
and:
```

```
EXPLAIN ANALYZE
15.2 Index Optimization
Identify at least one query that benefits from indexing.
Example process:
Initial Query
     ↓
EXPLAIN ANALYZE
     ↓
Identify Bottleneck
     ↓
Create Appropriate Index
     ↓
EXPLAIN ANALYZE Again
     ↓
Compare Results
The selected index must have a clear justification.
Do not create indexes arbitrarily.
```

```
16. Frontend Requirements
The frontend shall use the existing Vite React project.
```

```
Preferred technologies:
```

```
React
Vite
Tailwind CSS
The frontend should consume the FastAPI REST API.
```

```
16.1 Required Pages
/dashboard
/properties
/units
/tenants
/leases
/payments
/maintenance
/support
/reports
16.2 Dashboard
```

```
The dashboard should display useful operational information such as:
```

```
Total properties
Total units
Occupied units
Vacant units
Occupancy rate
Expected rent
Collected rent
Outstanding rent
Open maintenance requests
Open support tickets
```

```
The dashboard should prioritize useful information rather than decorative
```

```
visualizations.
```

```
17. UI Design Requirements
```

```
The visual design should be professional and restrained.
```

```
17.1 Overall Style
```

```
The interface should resemble:
```

```
Professional enterprise internal software.
```

```
It should NOT resemble:
A generic AI-generated SaaS dashboard.
```

```
17.2 Color Scheme
Primary
```

```
Warm beige / cream.
Secondary
Off-white.
```

```
Text
```

```
Dark charcoal / dark brown.
```

```
Accent
```

```
One muted earthy accent color.
```

```
Status Colors
```

```
Status colors may be used where necessary, but should remain restrained and
functional.
```

```
17.3 Visual Elements to Avoid
```

```
Do NOT use:
```

```
Purple AI gradients
Neon colors
Excessive glassmorphism
Excessive rounded cards
Excessive shadows
Animated backgrounds
Huge typography
AI-themed visual clichés
Random decorative illustrations
Excessive animations
Excessive icons
Overly colorful charts
Marketing-style hero sections
17.4 UI Principles
```

```
Prioritize:
```

```
Information density
Readability
Tables
Forms
Search
```

```
Filtering
Sorting
Status indicators
Reports
Clear navigation
Consistent spacing
Consistent typography
```

```
The interface should feel functional and believable.
```

# `18. Documentation Requirements` 

```
The project shall include comprehensive technical documentation.
```

```
Recommended structure:
```

```
docs/
│
├── PRD.md
├── SRS.md
├── architecture.md
├── database.md
├── api.md
├── sql-reporting.md
├── performance.md
└── testing.md
```

```
The root README should include:
```

```
Project overview
Problem statement
Features
Technology stack
Architecture
Database design
API overview
SQL reporting
Performance optimization
Testing
Setup instructions
Environment variables
Example API calls
Screenshots
Future improvements
19. Git and Version Control Requirements
```

```
The project should use Git.
```

```
The repository should contain meaningful commits.
```

```
Avoid commits such as:
```

```
update
final
final final
changes
test
abc
Prefer:
```

```
feat: add property database models
feat: implement property CRUD APIs
feat: add occupancy reporting
```

```
feat: implement support ticket workflow
perf: optimize payment reporting query
test: add support workflow tests
docs: add database architecture
20. Project Structure
```

```
The recommended final repository structure is:
```

```
propquery/
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
│
├── backend/
│   ├── app/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── repositories/
│   │   ├── services/
│   │   ├── api/
│   │   └── utils/
│   │
│   ├── tests/
│   ├── alembic/
│   ├── requirements.txt
│   └── .env.example
│
├── database/
│   ├── seed.sql
│   └── README.md
│
├── docs/
│   ├── PRD.md
│   ├── SRS.md
│   ├── architecture.md
│   ├── database.md
│   ├── api.md
│   ├── sql-reporting.md
│   ├── performance.md
│   └── testing.md
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

```
The exact structure may be modified if there is a strong technical reason.
```

```
21. Suggested Development Phases
```

```
The application must be developed incrementally.
```

```
Do NOT generate the entire application in one step.
```

```
Phase 1 — Architecture + Database
```

```
Implement:
```

```
Repository structure
PostgreSQL setup
SQLAlchemy
```

```
Alembic
Database models
Relationships
Constraints
Indexes where justified
Seed data
Deliverable
```

```
A working PostgreSQL database with realistic relational data and migrations.
```

```
Phase 2 — Backend Core
```

```
Implement:
```

```
FastAPI
REST APIs
CRUD operations
Pydantic schemas
Repository layer
Service layer
Error handling
Validation
Deliverable
```

```
A working backend with clean separation of responsibilities.
```

```
Phase 3 — SQL Reporting
```

```
Implement:
Occupancy reports
Rent collection reports
Payment reports
Maintenance reports
Financial reports
Monthly revenue reports
```

```
Use meaningful SQL involving:
```

```
JOIN
LEFT JOIN
GROUP BY
HAVING
CASE
Aggregate functions
Subqueries where appropriate
CTEs where useful
SQL views where useful
Deliverable
```

```
A working SQL reporting layer accessible through the backend.
```

```
Phase 4 — Application Support
```

```
Implement:
```

```
Support tickets
Ticket statuses
Ticket assignment
Troubleshooting history
Resolution notes
Ticket updates
Ticket Workflow
OPEN
```

```
  ↓
INVESTIGATING
  ↓
RESOLVED
Deliverable
```

```
A realistic application-support workflow.
```

```
Phase 5 — Performance Optimization
```

```
Implement:
```

```
EXPLAIN
EXPLAIN ANALYZE
Query performance analysis
Index optimization
Before/after query analysis
```

```
At least one inefficient query should be intentionally analyzed and optimized.
```

```
Deliverable
```

```
A documented performance optimization case study based on actual PostgreSQL
execution.
```

```
Phase 6 — Testing
```

```
Implement automated testing using Pytest.
```

```
Tests should cover:
```

```
API endpoints
Validation
Service/business logic
CRUD operations
Support-ticket state transitions
Reporting logic
Error handling
Database operations where appropriate
Deliverable
```

```
A meaningful automated test suite.
```

```
Phase 7 — Frontend
```

```
Implement the React frontend.
```

```
Required pages:
```

```
/dashboard
/properties
/units
/tenants
/leases
/payments
/maintenance
/support
/reports
```

```
The frontend should include:
```

```
Dashboard
Tables
Forms
```

```
Search
Filtering
Sorting
Detail views
Reports
Support-ticket interface
API integration
Deliverable
```

```
A functional enterprise-style frontend connected to the FastAPI backend.
```

```
Phase 8 — Finalization
```

```
Complete:
```

```
README
Architecture documentation
Database ER diagram
API documentation
SQL reporting documentation
Performance analysis documentation
Testing documentation
Screenshots
Docker/Docker Compose where appropriate
GitHub repository cleanup
Deliverable
```

```
A complete, documented, interview-ready portfolio project.
```

```
22. Development Quality Rules
```

```
The project should follow clean-code principles.
```

```
Code Quality
```

```
Use:
```

```
Meaningful variable names
Meaningful function names
Small focused functions
Single-responsibility principles
Type hints in Python
Pydantic schemas
Clear module boundaries
Consistent error handling
```

```
Avoid:
```

```
Giant files
Giant functions
Duplicated logic
Dead code
Commented-out code
Unnecessary abstractions
Unnecessary dependencies
Hardcoded credentials
Fake functionality
Placeholder implementations presented as complete features
23. AI-Assisted Development Rules
```

```
The project may be developed using AI coding agents.
```

```
However, generated code must still satisfy the project's engineering standards.
```

```
The agent must:
```

```
Inspect existing code before modifying it
Avoid unnecessary rewrites
Explain significant architectural decisions
Run tests after major changes
Run the application after major changes
Fix errors before moving to the next phase
Avoid introducing unnecessary dependencies
Keep code maintainable
Follow the documented architecture
```

```
The agent should not generate large amounts of unrelated code merely to increase
project complexity.
```

# `24. Development Workflow` 

```
Development should follow this process:
```

```
Read Requirements
       ↓
Inspect Existing Project
       ↓
Design
       ↓
Implement One Phase
       ↓
Run Application
       ↓
Run Tests
       ↓
Review Code
       ↓
Fix Issues
       ↓
Document
       ↓
Proceed to Next Phase
Each phase must be functional before proceeding to the next phase.
```

```
25. Final Project Goal
```

```
PropQuery should ultimately demonstrate the ability to:
```

```
Design a normalized relational database
Write meaningful SQL queries
Build REST APIs
Implement business logic cleanly
Build SQL-powered reporting
Troubleshoot application issues
Track application-support workflows
Analyze database performance
Optimize SQL queries
Write automated tests
Build a maintainable software system
Document technical decisions clearly
```

```
The project should be:
```

```
Technically credible
Realistic
Maintainable
Well documented
```

```
Interview-defensible
Appropriate for an enterprise software environment
```

```
The backend, database, SQL reporting, application support, testing, and
performance optimization are higher priorities than visual complexity.
```

```
26. Definition of Done
```

```
PropQuery shall be considered complete when:
```

```
 PostgreSQL database is working
 Database schema is normalized
 Alembic migrations are implemented
 Realistic seed data exists
 FastAPI backend is operational
 CRUD APIs are implemented
 Service and repository layers are separated
 Validation is implemented
 Error handling is implemented
 SQL reporting is implemented
 Support-ticket workflow is implemented
 Troubleshooting history is persisted
 Query performance has been analyzed
 At least one query has been optimized
 Automated tests are implemented
 React frontend is connected to the backend
 Dashboard is functional
 Reports are accessible
 Documentation is complete
 README is complete
 ER diagram is available
 API documentation is available
 Git repository is clean
 Project can be run by another developer using documented instructions
```

