"""Seed the PropQuery database with realistic sample data.

Run from the backend directory:
    python -m database.seed
"""

import sys
from datetime import date, datetime, timedelta
from pathlib import Path

# Add backend to path so we can import app modules
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from sqlalchemy import text

from app.core.database import SessionLocal, engine
from app.models import (
    Lease,
    MaintenanceRequest,
    Payment,
    Property,
    SupportTicket,
    SupportTicketUpdate,
    Tenant,
    Unit,
)


def clear_tables(db) -> None:
    """Delete all rows from all tables in dependency order."""
    db.execute(text("DELETE FROM support_ticket_updates"))
    db.execute(text("DELETE FROM support_tickets"))
    db.execute(text("DELETE FROM maintenance_requests"))
    db.execute(text("DELETE FROM payments"))
    db.execute(text("DELETE FROM leases"))
    db.execute(text("DELETE FROM units"))
    db.execute(text("DELETE FROM tenants"))
    db.execute(text("DELETE FROM properties"))
    db.commit()


def seed_properties(db) -> list[Property]:
    """Create 5 realistic properties."""
    properties = [
        Property(
            name="Oakwood Apartments",
            address="142 Elm Street",
            city="Austin",
            state="TX",
            zip_code="73301",
            property_type="apartment",
            year_built=2005,
        ),
        Property(
            name="Riverside Terrace",
            address="880 River Road",
            city="Denver",
            state="CO",
            zip_code="80201",
            property_type="apartment",
            year_built=2012,
        ),
        Property(
            name="Maple Court",
            address="55 Maple Avenue",
            city="Portland",
            state="OR",
            zip_code="97201",
            property_type="townhouse",
            year_built=1998,
        ),
        Property(
            name="Summit Plaza",
            address="310 High Street",
            city="Nashville",
            state="TN",
            zip_code="37201",
            property_type="apartment",
            year_built=2018,
        ),
        Property(
            name="Cedar Ridge",
            address="720 Pine Lane",
            city="Raleigh",
            state="NC",
            zip_code="27601",
            property_type="apartment",
            year_built=2010,
        ),
    ]
    db.add_all(properties)
    db.flush()
    return properties


def seed_units(db, properties: list[Property]) -> list[Unit]:
    """Create 20 units across properties — mix of sizes and rents."""
    units_data = [
        # Oakwood Apartments — 5 units
        ("101", 1, 1, 650, 1100.00, properties[0].id),
        ("102", 2, 1, 850, 1350.00, properties[0].id),
        ("201", 2, 2, 950, 1500.00, properties[0].id),
        ("202", 3, 2, 1200, 1800.00, properties[0].id),
        ("301", 1, 1, 600, 1050.00, properties[0].id),
        # Riverside Terrace — 4 units
        ("A1", 1, 1, 700, 1200.00, properties[1].id),
        ("A2", 2, 1, 900, 1450.00, properties[1].id),
        ("B1", 2, 2, 1000, 1600.00, properties[1].id),
        ("B2", 3, 2, 1300, 1900.00, properties[1].id),
        # Maple Court — 3 units
        ("1", 2, 1, 1100, 1400.00, properties[2].id),
        ("2", 3, 2, 1400, 1750.00, properties[2].id),
        ("3", 2, 2, 1050, 1350.00, properties[2].id),
        # Summit Plaza — 5 units
        ("401", 1, 1, 550, 1150.00, properties[3].id),
        ("402", 2, 1, 800, 1400.00, properties[3].id),
        ("403", 2, 2, 950, 1550.00, properties[3].id),
        ("404", 3, 2, 1250, 1850.00, properties[3].id),
        ("405", 1, 1, 580, 1100.00, properties[3].id),
        # Cedar Ridge — 3 units
        ("C1", 2, 1, 880, 1300.00, properties[4].id),
        ("C2", 2, 2, 1000, 1500.00, properties[4].id),
        ("C3", 3, 2, 1200, 1700.00, properties[4].id),
    ]

    units = []
    for unit_number, beds, baths, sqft, rent, prop_id in units_data:
        units.append(
            Unit(
                property_id=prop_id,
                unit_number=unit_number,
                bedrooms=beds,
                bathrooms=baths,
                square_feet=sqft,
                market_rent=rent,
                status="vacant",  # Will be updated when leases are created
            )
        )
    db.add_all(units)
    db.flush()
    return units


def seed_tenants(db) -> list[Tenant]:
    """Create 15 realistic tenants."""
    tenants_data = [
        ("James", "Mitchell", "james.mitchell@email.com", "512-555-0101"),
        ("Sarah", "Chen", "sarah.chen@email.com", "303-555-0102"),
        ("David", "Rodriguez", "david.rodriguez@email.com", "503-555-0103"),
        ("Emily", "Thompson", "emily.thompson@email.com", "615-555-0104"),
        ("Michael", "Patel", "michael.patel@email.com", "919-555-0105"),
        ("Jessica", "Williams", "jessica.williams@email.com", "512-555-0106"),
        ("Robert", "Kim", "robert.kim@email.com", "303-555-0107"),
        ("Amanda", "Davis", "amanda.davis@email.com", "503-555-0108"),
        ("Christopher", "Garcia", "christopher.garcia@email.com", "615-555-0109"),
        ("Lauren", "Brown", "lauren.brown@email.com", "919-555-0110"),
        ("Daniel", "Wilson", "daniel.wilson@email.com", "512-555-0111"),
        ("Rachel", "Martinez", "rachel.martinez@email.com", "303-555-0112"),
        ("Kevin", "Anderson", "kevin.anderson@email.com", "503-555-0113"),
        ("Megan", "Taylor", "megan.taylor@email.com", "615-555-0114"),
        ("Brian", "Johnson", "brian.johnson@email.com", "919-555-0115"),
    ]

    tenants = []
    for first, last, email, phone in tenants_data:
        tenants.append(
            Tenant(first_name=first, last_name=last, email=email, phone=phone)
        )
    db.add_all(tenants)
    db.flush()
    return tenants


def seed_leases(db, units: list[Unit], tenants: list[Tenant]) -> list[Lease]:
    """Create 18 leases — active, expired, and terminated.

    Updates unit status to 'occupied' for active leases.
    """
    today = date.today()
    leases = []

    # Active leases (14 units occupied)
    active_pairs = [
        (0, 0, 1100.00),   # Oakwood 101 - James
        (1, 1, 1350.00),   # Oakwood 102 - Sarah
        (2, 5, 1500.00),   # Oakwood 201 - Jessica
        (3, 10, 1800.00),  # Oakwood 202 - Daniel
        (5, 2, 1200.00),   # Riverside A1 - David
        (6, 6, 1450.00),   # Riverside A2 - Robert
        (7, 11, 1600.00),  # Riverside B1 - Rachel
        (9, 3, 1400.00),   # Maple Court 1 - Emily
        (10, 7, 1750.00),  # Maple Court 2 - Amanda
        (12, 4, 1150.00),  # Summit 401 - Michael
        (13, 8, 1400.00),  # Summit 402 - Christopher
        (14, 12, 1550.00), # Summit 403 - Kevin
        (17, 9, 1300.00),  # Cedar C1 - Lauren
        (18, 13, 1500.00), # Cedar C2 - Megan
    ]

    for unit_idx, tenant_idx, rent in active_pairs:
        start = today - timedelta(days=180 + (unit_idx * 15))
        lease = Lease(
            unit_id=units[unit_idx].id,
            tenant_id=tenants[tenant_idx].id,
            start_date=start,
            end_date=start + timedelta(days=365),
            monthly_rent=rent,
            security_deposit=rent,
            status="active",
        )
        leases.append(lease)
        units[unit_idx].status = "occupied"

    # Expired leases (previous tenants on now-vacant units)
    expired_pairs = [
        (4, 14, 1000.00),   # Oakwood 301 - Brian (expired)
        (11, 3, 1300.00),   # Maple Court 3 - Emily (expired, moved to unit 9)
        (15, 9, 1800.00),   # Summit 404 - Lauren (expired, moved to Cedar)
    ]

    for unit_idx, tenant_idx, rent in expired_pairs:
        start = today - timedelta(days=500)
        lease = Lease(
            unit_id=units[unit_idx].id,
            tenant_id=tenants[tenant_idx].id,
            start_date=start,
            end_date=start + timedelta(days=365),
            monthly_rent=rent,
            security_deposit=rent,
            status="expired",
        )
        leases.append(lease)
        # These units stay vacant

    # Terminated lease
    term_start = today - timedelta(days=300)
    leases.append(
        Lease(
            unit_id=units[19].id,  # Cedar C3
            tenant_id=tenants[14].id,  # Brian
            start_date=term_start,
            end_date=term_start + timedelta(days=365),
            monthly_rent=1700.00,
            security_deposit=1700.00,
            status="terminated",
        )
    )

    db.add_all(leases)
    db.flush()
    return leases


def seed_payments(db, leases: list[Lease]) -> list[Payment]:
    """Create ~50 payments across leases — completed, pending, and failed."""
    payments = []
    today = date.today()

    # Generate monthly payments for active leases
    for i, lease in enumerate(leases[:14]):  # Active leases
        months_active = min((today - lease.start_date).days // 30, 6)
        for month in range(months_active):
            payment_date = lease.start_date + timedelta(days=30 * month + 1)
            if payment_date > today:
                break

            # Most payments completed, a few pending or failed
            if i == 3 and month == months_active - 1:
                status = "pending"
            elif i == 7 and month == 2:
                status = "failed"
            else:
                status = "completed"

            payments.append(
                Payment(
                    lease_id=lease.id,
                    payment_date=payment_date,
                    amount=lease.monthly_rent,
                    status=status,
                    payment_method="bank_transfer" if i % 3 == 0 else "check" if i % 3 == 1 else "online",
                    reference_number=f"PAY-{lease.id:03d}-{month + 1:02d}",
                )
            )

    # Add some payments for expired leases too
    for lease in leases[14:17]:  # Expired leases
        for month in range(3):
            payments.append(
                Payment(
                    lease_id=lease.id,
                    payment_date=lease.start_date + timedelta(days=30 * month + 1),
                    amount=lease.monthly_rent,
                    status="completed",
                    payment_method="check",
                    reference_number=f"PAY-{lease.id:03d}-{month + 1:02d}",
                )
            )

    db.add_all(payments)
    db.flush()
    return payments


def seed_maintenance_requests(db, units: list[Unit]) -> list[MaintenanceRequest]:
    """Create 12 maintenance requests across units."""
    today = date.today()
    requests = [
        MaintenanceRequest(
            unit_id=units[0].id,
            title="Leaking kitchen faucet",
            description="Kitchen faucet has a slow drip. Washer may need replacement.",
            priority="medium",
            status="resolved",
            created_date=today - timedelta(days=45),
            resolved_date=today - timedelta(days=42),
            resolution_notes="Replaced faucet washer and tightened connections.",
        ),
        MaintenanceRequest(
            unit_id=units[2].id,
            title="HVAC not cooling properly",
            description="Air conditioning not reaching set temperature. Unit runs constantly but apartment stays warm.",
            priority="high",
            status="resolved",
            created_date=today - timedelta(days=30),
            resolved_date=today - timedelta(days=27),
            resolution_notes="Replaced air filter and recharged refrigerant. System now cooling normally.",
        ),
        MaintenanceRequest(
            unit_id=units[3].id,
            title="Broken window latch",
            description="Bedroom window latch is broken. Window cannot be securely closed.",
            priority="high",
            status="in_progress",
            created_date=today - timedelta(days=5),
        ),
        MaintenanceRequest(
            unit_id=units[5].id,
            title="Garbage disposal jammed",
            description="Kitchen garbage disposal is jammed and making grinding noise.",
            priority="medium",
            status="resolved",
            created_date=today - timedelta(days=60),
            resolved_date=today - timedelta(days=59),
            resolution_notes="Cleared jam with Allen wrench. Disposal functioning normally.",
        ),
        MaintenanceRequest(
            unit_id=units[7].id,
            title="Water heater intermittent",
            description="Hot water supply is intermittent. Sometimes runs cold after a few minutes.",
            priority="high",
            status="open",
            created_date=today - timedelta(days=2),
        ),
        MaintenanceRequest(
            unit_id=units[9].id,
            title="Bathroom exhaust fan noisy",
            description="Bathroom exhaust fan vibrates loudly when turned on.",
            priority="low",
            status="open",
            created_date=today - timedelta(days=10),
        ),
        MaintenanceRequest(
            unit_id=units[10].id,
            title="Front door deadbolt sticking",
            description="Deadbolt lock is difficult to turn. Key gets stuck occasionally.",
            priority="urgent",
            status="resolved",
            created_date=today - timedelta(days=15),
            resolved_date=today - timedelta(days=14),
            resolution_notes="Lubricated lock mechanism and adjusted strike plate alignment.",
        ),
        MaintenanceRequest(
            unit_id=units[12].id,
            title="Ceiling light flickering",
            description="Living room ceiling light fixture flickers intermittently.",
            priority="low",
            status="resolved",
            created_date=today - timedelta(days=20),
            resolved_date=today - timedelta(days=18),
            resolution_notes="Replaced bulb and tightened wiring connections in fixture.",
        ),
        MaintenanceRequest(
            unit_id=units[13].id,
            title="Dishwasher not draining",
            description="Dishwasher fills with water but does not drain at end of cycle.",
            priority="medium",
            status="in_progress",
            created_date=today - timedelta(days=3),
        ),
        MaintenanceRequest(
            unit_id=units[14].id,
            title="Smoke detector beeping",
            description="Smoke detector in hallway beeps every 30 seconds. Battery replaced but issue persists.",
            priority="medium",
            status="open",
            created_date=today - timedelta(days=1),
        ),
        MaintenanceRequest(
            unit_id=units[17].id,
            title="Carpet stain in bedroom",
            description="Large carpet stain in master bedroom from previous tenant. Needs professional cleaning.",
            priority="low",
            status="resolved",
            created_date=today - timedelta(days=90),
            resolved_date=today - timedelta(days=85),
            resolution_notes="Professional carpet cleaning completed. Stain removed successfully.",
        ),
        MaintenanceRequest(
            unit_id=units[18].id,
            title="Balcony railing loose",
            description="Balcony railing on second floor feels loose when leaned on. Safety concern.",
            priority="urgent",
            status="resolved",
            created_date=today - timedelta(days=8),
            resolved_date=today - timedelta(days=7),
            resolution_notes="Re-anchored railing bolts and added additional support bracket.",
        ),
    ]

    db.add_all(requests)
    db.flush()
    return requests


def seed_support_tickets(db, properties, units, tenants) -> list[SupportTicket]:
    """Create 8 support tickets with update history demonstrating the workflow."""
    today = datetime.now()
    tickets = []

    # Ticket 1: Resolved — payment missing from report (the canonical example)
    t1 = SupportTicket(
        title="Tenant payment missing from monthly report",
        description="Payment for lease on unit 201 at Oakwood Apartments shows as completed in payment records but does not appear in the monthly rent collection report for last month.",
        category="reporting",
        priority="high",
        status="resolved",
        property_id=properties[0].id,
        unit_id=units[2].id,
        tenant_id=tenants[5].id,
        assigned_engineer="Alex Kumar",
        created_at=today - timedelta(days=12),
        updated_at=today - timedelta(days=11),
        resolved_at=today - timedelta(days=11),
        resolution_notes="Payment record existed but was excluded from the report because of an incorrect date filter in the reporting query. The payment_date was recorded as the last day of the previous month, but the report filter used a strict less-than comparison instead of less-than-or-equal. Corrected the query boundary condition.",
    )
    tickets.append(t1)

    # Ticket 2: Resolved — duplicate tenant record
    t2 = SupportTicket(
        title="Duplicate tenant record in system",
        description="Tenant David Rodriguez appears twice in the tenant list with slightly different email addresses. This is causing confusion in lease assignment.",
        category="accounts",
        priority="medium",
        status="resolved",
        tenant_id=tenants[2].id,
        assigned_engineer="Alex Kumar",
        created_at=today - timedelta(days=20),
        updated_at=today - timedelta(days=18),
        resolved_at=today - timedelta(days=18),
        resolution_notes="Identified that the duplicate was created during a manual data entry error. Merged records and updated the lease association to point to the correct tenant ID. Added a note to implement email uniqueness validation.",
    )
    tickets.append(t2)

    # Ticket 3: Investigating — occupancy mismatch
    t3 = SupportTicket(
        title="Occupancy report shows incorrect vacancy count",
        description="The occupancy report for Summit Plaza shows 2 vacant units, but the property manager confirms only 1 unit is actually vacant. Possible data inconsistency.",
        category="reporting",
        priority="high",
        status="investigating",
        property_id=properties[3].id,
        assigned_engineer="Priya Sharma",
        created_at=today - timedelta(days=3),
        updated_at=today - timedelta(days=2),
    )
    tickets.append(t3)

    # Ticket 4: Open — maintenance request not updating
    t4 = SupportTicket(
        title="Maintenance request status not updating",
        description="After marking maintenance request as resolved, the status on the dashboard still shows as open. Refresh does not fix the issue.",
        category="maintenance",
        priority="medium",
        status="open",
        property_id=properties[1].id,
        assigned_engineer=None,
        created_at=today - timedelta(days=1),
        updated_at=today - timedelta(days=1),
    )
    tickets.append(t4)

    # Ticket 5: Resolved — lease end date calculation
    t5 = SupportTicket(
        title="Lease end date showing wrong year",
        description="When creating a new 12-month lease starting Feb 2025, the system calculated the end date as Feb 2024 instead of Feb 2026.",
        category="leases",
        priority="critical",
        status="resolved",
        assigned_engineer="Alex Kumar",
        created_at=today - timedelta(days=30),
        updated_at=today - timedelta(days=28),
        resolved_at=today - timedelta(days=28),
        resolution_notes="Bug in date calculation logic. The year was not being incremented when the lease duration crossed a year boundary. Fixed the date arithmetic in the lease creation service.",
    )
    tickets.append(t5)

    # Ticket 6: Open — slow report generation
    t6 = SupportTicket(
        title="Monthly revenue report takes too long to load",
        description="The monthly revenue report page takes over 10 seconds to load. Other reports load in under 2 seconds.",
        category="reporting",
        priority="medium",
        status="open",
        assigned_engineer=None,
        created_at=today - timedelta(hours=6),
        updated_at=today - timedelta(hours=6),
    )
    tickets.append(t6)

    # Ticket 7: Resolved — payment method not saving
    t7 = SupportTicket(
        title="Payment method field not saved",
        description="When recording a new payment, the payment method dropdown selection is not being persisted to the database. The field shows as null after saving.",
        category="payments",
        priority="high",
        status="resolved",
        assigned_engineer="Priya Sharma",
        created_at=today - timedelta(days=15),
        updated_at=today - timedelta(days=14),
        resolved_at=today - timedelta(days=14),
        resolution_notes="The payment creation API schema did not include payment_method as an accepted field. Added the field to the Pydantic schema and the repository create function.",
    )
    tickets.append(t7)

    # Ticket 8: Investigating — tenant search not finding results
    t8 = SupportTicket(
        title="Tenant search returns no results for partial name",
        description="Searching for 'Mitch' in the tenant search does not return James Mitchell. Full name search works but partial does not.",
        category="system",
        priority="low",
        status="investigating",
        assigned_engineer="Alex Kumar",
        created_at=today - timedelta(days=2),
        updated_at=today - timedelta(days=1),
    )
    tickets.append(t8)

    db.add_all(tickets)
    db.flush()
    return tickets


def seed_ticket_updates(db, tickets: list[SupportTicket]) -> None:
    """Create support ticket update history for resolved and investigating tickets."""
    updates = []

    # Ticket 1 updates (resolved payment report issue)
    t1 = tickets[0]
    updates.extend([
        SupportTicketUpdate(
            ticket_id=t1.id,
            update_type="status_change",
            content="Ticket created. Payment for unit 201 not appearing in monthly report.",
            author="System",
            old_status=None,
            new_status="open",
            created_at=t1.created_at,
        ),
        SupportTicketUpdate(
            ticket_id=t1.id,
            update_type="assignment",
            content="Assigned to Alex Kumar for investigation.",
            author="System",
            old_status=None,
            new_status=None,
            created_at=t1.created_at + timedelta(minutes=12),
        ),
        SupportTicketUpdate(
            ticket_id=t1.id,
            update_type="status_change",
            content="Beginning investigation. Checking payment records and reporting query.",
            author="Alex Kumar",
            old_status="open",
            new_status="investigating",
            created_at=t1.created_at + timedelta(minutes=30),
        ),
        SupportTicketUpdate(
            ticket_id=t1.id,
            update_type="note",
            content="Payment record found in payments table with status 'completed' and correct amount. Payment date is 2025-01-31. Checking report query date boundaries.",
            author="Alex Kumar",
            old_status=None,
            new_status=None,
            created_at=t1.created_at + timedelta(hours=2),
        ),
        SupportTicketUpdate(
            ticket_id=t1.id,
            update_type="note",
            content="Found the issue. Report query uses WHERE payment_date < '2025-02-01' but should use payment_date <= '2025-01-31' or payment_date < '2025-02-01'. The boundary date was being generated incorrectly, using the 30th instead of the last day of the month.",
            author="Alex Kumar",
            old_status=None,
            new_status=None,
            created_at=t1.created_at + timedelta(hours=3),
        ),
        SupportTicketUpdate(
            ticket_id=t1.id,
            update_type="status_change",
            content="Issue resolved. Corrected date filter in reporting query. Payment now appears in report.",
            author="Alex Kumar",
            old_status="investigating",
            new_status="resolved",
            created_at=t1.created_at + timedelta(hours=4),
        ),
    ])

    # Ticket 3 updates (investigating — occupancy mismatch)
    t3 = tickets[2]
    updates.extend([
        SupportTicketUpdate(
            ticket_id=t3.id,
            update_type="status_change",
            content="Ticket created. Occupancy numbers for Summit Plaza appear incorrect.",
            author="System",
            old_status=None,
            new_status="open",
            created_at=t3.created_at,
        ),
        SupportTicketUpdate(
            ticket_id=t3.id,
            update_type="assignment",
            content="Assigned to Priya Sharma.",
            author="System",
            old_status=None,
            new_status=None,
            created_at=t3.created_at + timedelta(minutes=20),
        ),
        SupportTicketUpdate(
            ticket_id=t3.id,
            update_type="status_change",
            content="Investigating. Comparing unit status in database with active lease records.",
            author="Priya Sharma",
            old_status="open",
            new_status="investigating",
            created_at=t3.created_at + timedelta(hours=1),
        ),
        SupportTicketUpdate(
            ticket_id=t3.id,
            update_type="note",
            content="Found that unit 405 has status 'vacant' in the units table but has an active lease record. The unit status was not updated when the lease was created. Checking if this is a data issue or a bug in lease creation logic.",
            author="Priya Sharma",
            old_status=None,
            new_status=None,
            created_at=t3.created_at + timedelta(hours=3),
        ),
    ])

    # Ticket 5 updates (resolved — lease date bug)
    t5 = tickets[4]
    updates.extend([
        SupportTicketUpdate(
            ticket_id=t5.id,
            update_type="status_change",
            content="Ticket created. Lease end date calculated incorrectly.",
            author="System",
            old_status=None,
            new_status="open",
            created_at=t5.created_at,
        ),
        SupportTicketUpdate(
            ticket_id=t5.id,
            update_type="status_change",
            content="Investigating date calculation logic in lease creation service.",
            author="Alex Kumar",
            old_status="open",
            new_status="investigating",
            created_at=t5.created_at + timedelta(hours=1),
        ),
        SupportTicketUpdate(
            ticket_id=t5.id,
            update_type="status_change",
            content="Fixed. The timedelta calculation was subtracting instead of adding the year offset. Deployed fix and verified with test cases.",
            author="Alex Kumar",
            old_status="investigating",
            new_status="resolved",
            created_at=t5.created_at + timedelta(days=2),
        ),
    ])

    # Ticket 8 updates (investigating — tenant search)
    t8 = tickets[7]
    updates.extend([
        SupportTicketUpdate(
            ticket_id=t8.id,
            update_type="status_change",
            content="Ticket created. Partial name search not returning expected results.",
            author="System",
            old_status=None,
            new_status="open",
            created_at=t8.created_at,
        ),
        SupportTicketUpdate(
            ticket_id=t8.id,
            update_type="status_change",
            content="Investigating. Checking search query implementation — likely an exact match vs ILIKE issue.",
            author="Alex Kumar",
            old_status="open",
            new_status="investigating",
            created_at=t8.created_at + timedelta(hours=8),
        ),
    ])

    db.add_all(updates)
    db.flush()


def run_seed() -> None:
    """Execute the full seed process."""
    db = SessionLocal()
    try:
        print("Clearing existing data...")
        clear_tables(db)

        print("Seeding properties...")
        properties = seed_properties(db)

        print("Seeding units...")
        units = seed_units(db, properties)

        print("Seeding tenants...")
        tenants = seed_tenants(db)

        print("Seeding leases...")
        leases = seed_leases(db, units, tenants)

        print("Seeding payments...")
        payments = seed_payments(db, leases)

        print("Seeding maintenance requests...")
        maintenance = seed_maintenance_requests(db, units)

        print("Seeding support tickets...")
        tickets = seed_support_tickets(db, properties, units, tenants)

        print("Seeding support ticket updates...")
        seed_ticket_updates(db, tickets)

        db.commit()
        print(
            f"\nSeed complete:"
            f"\n  {len(properties)} properties"
            f"\n  {len(units)} units"
            f"\n  {len(tenants)} tenants"
            f"\n  {len(leases)} leases"
            f"\n  {len(payments)} payments"
            f"\n  {len(maintenance)} maintenance requests"
            f"\n  {len(tickets)} support tickets"
        )
    except Exception as e:
        db.rollback()
        print(f"Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
