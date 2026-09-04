# Database Seed Data

This directory contains scripts to populate the PropQuery database with realistic sample data.

## Usage

```bash
cd backend
python -m database.seed
```

## What Gets Created

- **5 properties** — apartment buildings across different cities
- **20 units** — distributed across properties, mix of occupied and vacant
- **15 tenants** — with unique emails and phone numbers
- **18 leases** — active, expired, and terminated
- **50+ payments** — completed, pending, and failed
- **12 maintenance requests** — various priorities and statuses
- **8 support tickets** — with update history demonstrating the support workflow
