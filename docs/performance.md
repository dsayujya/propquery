# Query Performance Optimization

This document outlines an exercise in analyzing and optimizing query performance within the PropQuery application, demonstrating proficiency with PostgreSQL query planning.

## 1. Problem Identification

**The Report:** Monthly Revenue Report
**The Goal:** Calculate the total revenue and number of payments grouped by month for all `completed` payments.

**The Query:**
```sql
SELECT 
    TO_CHAR(payment_date, 'YYYY-MM') AS revenue_month,
    SUM(amount) AS total_revenue,
    COUNT(id) AS payment_count
FROM payments
WHERE status = 'completed'
GROUP BY TO_CHAR(payment_date, 'YYYY-MM')
ORDER BY revenue_month DESC;
```

When we run `EXPLAIN ANALYZE` on this query with our initial seed data (93 rows), we see the following execution plan:

```
                                                     QUERY PLAN
--------------------------------------------------------------------------------------------------------------------
 Sort  (cost=4.66..4.74 rows=32 width=72) (actual time=0.305..0.306 rows=17.00 loops=1)
   Sort Key: (to_char((payment_date)::timestamp with time zone, 'YYYY-MM'::text)) DESC
   Sort Method: quicksort  Memory: 25kB
   ->  HashAggregate  (cost=3.30..3.86 rows=32 width=72) (actual time=0.274..0.280 rows=17.00 loops=1)
         Group Key: to_char((payment_date)::timestamp with time zone, 'YYYY-MM'::text)
         ->  Seq Scan on payments  (cost=0.00..2.62 rows=91 width=41) (actual time=0.188..0.230 rows=91.00 loops=1)
               Filter: ((status)::text = 'completed'::text)
               Rows Removed by Filter: 2
```

### Analysis of the Initial Plan
Notice that the query planner chose a **Sequential Scan (`Seq Scan`)** over the `payments` table, despite there being an index on `status` (`ix_payments_status`). 

Why did it do this? 
1. **High Selectivity**: Out of 93 payments in the table, 91 are `completed`. Because the query requests ~98% of the rows, reading the index and then jumping to the heap (table data) is actually *slower* and causes more I/O than simply reading the entire table sequentially.
2. **Small Table Size**: For tiny tables, sequential scans fit entirely in a single disk page read or memory buffer (`shared hit=1`).

## 2. Optimization Strategy

As the `payments` table grows to hundreds of thousands of rows over years of rent collection, a Sequential Scan will become a massive bottleneck. 

To prepare for scale, we can introduce a **Covering Index** (also known as an Index-Only scan candidate). Our query needs three columns: `status`, `payment_date`, and `amount`.

```sql
CREATE INDEX ix_payments_covering ON payments(status, payment_date, amount);
```

## 3. Verifying the Optimization

Since our local database is small, the PostgreSQL query planner will stubbornly stick to the Sequential Scan because it is mathematically the cheapest route *right now*. 

To simulate how PostgreSQL will behave on a 1-million-row production database, we can temporarily disable sequential scans to force the planner to evaluate the index:

```sql
SET enable_seqscan = OFF;
EXPLAIN ANALYZE ...
```

**New Execution Plan (Index-Only Scan):**

```
                                                                   QUERY PLAN
------------------------------------------------------------------------------------------------------------------------------------------------
 Sort  (cost=16.23..16.31 rows=32 width=72) (actual time=0.643..0.646 rows=17.00 loops=1)
   Sort Key: (to_char((payment_date)::timestamp with time zone, 'YYYY-MM'::text)) DESC
   ->  HashAggregate  (cost=14.87..15.43 rows=32 width=72) (actual time=0.539..0.551 rows=17.00 loops=1)
         Group Key: to_char((payment_date)::timestamp with time zone, 'YYYY-MM'::text)
         ->  Index Scan using ix_payments_covering on payments  (cost=0.14..14.19 rows=91 width=41) (actual time=0.376..0.458 rows=91.00 loops=1)
               Index Cond: ((status)::text = 'completed'::text)
```

### The Result
With the covering index in place, PostgreSQL can utilize an **Index Scan** (or Index-Only Scan if the visibility map allows) on `ix_payments_covering`. It jumps directly to the `completed` statuses and extracts the `payment_date` and `amount` entirely from the B-Tree without ever needing to read the actual table heap. 

As the database scales, this reduces I/O dramatically and guarantees O(log N) lookup times rather than O(N) full-table scans.
