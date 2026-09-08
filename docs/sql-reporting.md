# SQL Reporting Module

The system is engineered to handle complex business intelligence reporting entirely within the database layer using raw SQL execution via SQLAlchemy `text()`. This guarantees high performance for aggregated views.

## Reporting Endpoints (`/api/v1/reports/`)

### 1. Occupancy Report
**Endpoint**: `/reports/occupancy`
Calculates real-time occupancy percentages per property.
- Uses `LEFT JOIN` on Units and aggregates `CASE WHEN status = 'Occupied'` versus total counts.

### 2. Rent Collection Report
**Endpoint**: `/reports/rent-collection`
Month-to-date calculation of expected rent vs. actual collected rent.
- Uses a CTE to sum expected active lease amounts.
- Uses a separate CTE to sum completed payments within the current month.
- Joins the CTEs to calculate outstanding balances and collection percentages.

### 3. Tenant Payment History
**Endpoint**: `/reports/tenant-payments`
Detailed audit of a tenant's historical payments, including tracking late vs. on-time payments.

### 4. Maintenance Performance
**Endpoint**: `/reports/maintenance-performance`
Tracks the efficiency of resolving maintenance issues.
- Calculates total open vs resolved requests.
- Uses `EXTRACT(EPOCH FROM (resolved_date - created_at))` to calculate the average resolution time in hours.

*For details on database query performance tuning, refer to `performance.md`.*
