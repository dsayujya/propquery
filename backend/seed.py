import os
import sys
from datetime import date, datetime, timedelta
import random

# Add backend directory to sys.path to allow imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from app.core.database import SessionLocal, engine
from app.core.security import get_password_hash
from app.models.user import User
from app.models.property import Property
from app.models.unit import Unit
from app.models.tenant import Tenant
from app.models.lease import Lease
from app.models.payment import Payment
from app.models.maintenance import MaintenanceRequest

def seed_db():
    db = SessionLocal()
    try:
        print("Wiping existing data...")
        # Use CASCADE to delete dependent rows
        tables = [
            "support_ticket_updates", "support_tickets", "maintenance_requests",
            "payments", "leases", "units", "properties", "tenants", "users"
        ]
        for table in tables:
            db.execute(text(f"TRUNCATE TABLE {table} CASCADE;"))
        db.commit()

        print("Seeding Users...")
        admin = User(
            email="admin@propquery.com",
            hashed_password=get_password_hash("password123"),
            full_name="Rajesh Admin",
            role="admin",
            is_superuser=True
        )
        owner1 = User(
            email="owner1@propquery.com",
            hashed_password=get_password_hash("password123"),
            full_name="Aarav Patel",
            role="owner"
        )
        owner2 = User(
            email="owner2@propquery.com",
            hashed_password=get_password_hash("password123"),
            full_name="Priya Sharma",
            role="owner"
        )
        
        tenant_users = []
        tenant_names = ["Rohan Gupta", "Ananya Singh", "Vikram Malhotra", "Neha Desai", "Arjun Kapoor"]
        for i, name in enumerate(tenant_names, 1):
            t_user = User(
                email=f"tenant{i}@propquery.com",
                hashed_password=get_password_hash("password123"),
                full_name=name,
                role="tenant"
            )
            tenant_users.append(t_user)

        db.add_all([admin, owner1, owner2] + tenant_users)
        db.commit()
        
        print("Seeding Properties...")
        prop1 = Property(name="Marine Drive Residency", address="Marine Drive", city="Mumbai", state="Maharashtra", zip_code="400020", property_type="apartment", year_built=2015, owner_id=owner1.id, image_url="/images/marine_drive.png")
        prop2 = Property(name="Koramangala Heights", address="100ft Road", city="Bengaluru", state="Karnataka", zip_code="560034", property_type="complex", year_built=2018, owner_id=owner1.id, image_url="/images/koramangala.png")
        prop3 = Property(name="Connaught Place Suites", address="CP Inner Circle", city="New Delhi", state="Delhi", zip_code="110001", property_type="apartment", year_built=2020, owner_id=owner2.id, image_url="/images/connaught.png")
        prop4 = Property(name="Bandra West Lofts", address="Pali Hill", city="Mumbai", state="Maharashtra", zip_code="400050", property_type="complex", year_built=2019, owner_id=owner2.id, image_url="/images/bandra.png")
        
        properties = [prop1, prop2, prop3, prop4]
        db.add_all(properties)
        db.commit()

        print("Seeding Units...")
        units = []
        for prop in properties:
            for i in range(1, 4):
                units.append(Unit(
                    property_id=prop.id,
                    unit_number=f"{i}0{i}",
                    bedrooms=random.randint(1, 3),
                    bathrooms=random.randint(1, 2),
                    square_feet=random.randint(600, 1500),
                    market_rent=random.randint(15000, 50000),
                    status="vacant"
                ))
        db.add_all(units)
        db.commit()

        print("Seeding Tenants...")
        tenants = []
        for i, t_user in enumerate(tenant_users):
            first, last = t_user.full_name.split()
            tenants.append(Tenant(
                first_name=first,
                last_name=last,
                email=t_user.email,
                phone=f"+91 987654321{i}",
                user_id=t_user.id
            ))
        db.add_all(tenants)
        db.commit()

        print("Seeding Leases and Payments...")
        leased_units = random.sample(units, len(tenants))
        leases = []
        payments = []
        m_requests = []
        
        today = date.today()
        
        for idx, tenant in enumerate(tenants):
            unit = leased_units[idx]
            unit.status = "occupied"
            
            # Start lease 6 months ago
            start_month = today.month - 6 if today.month > 6 else today.month + 6
            start_year = today.year if today.month > 6 else today.year - 1
            
            # Handle edge cases for day of month
            try:
                start = date(start_year, start_month, today.day)
            except ValueError:
                start = date(start_year, start_month, 28)
                
            end = start.replace(year=start.year + 1)
            
            lease = Lease(
                unit_id=unit.id,
                tenant_id=tenant.id,
                start_date=start,
                end_date=end,
                monthly_rent=unit.market_rent,
                security_deposit=unit.market_rent * 2,
                status="active"
            )
            leases.append(lease)
            db.add(lease)
            db.commit() # commit to get lease.id
            
            # Generate payments for past 6 months
            for m in range(6):
                pay_month = start.month + m
                pay_year = start.year
                if pay_month > 12:
                    pay_month -= 12
                    pay_year += 1
                
                try:
                    pay_date = date(pay_year, pay_month, start.day)
                except ValueError:
                    pay_date = date(pay_year, pay_month, 28)
                
                status = "completed"
                amount = float(lease.monthly_rent)
                if m == 5 and idx % 2 == 0:
                    status = "pending"
                    amount = amount / 2 # partial payment
                    
                payment = Payment(
                    lease_id=lease.id,
                    payment_date=pay_date,
                    amount=amount,
                    status=status,
                    payment_method="UPI"
                )
                payments.append(payment)
                
            # Generate maintenance requests
            if idx % 2 != 0:
                mr = MaintenanceRequest(
                    unit_id=unit.id,
                    title="AC not cooling",
                    description="The bedroom AC is blowing warm air.",
                    priority="high",
                    status="open",
                    created_date=today - timedelta(days=random.randint(1, 10))
                )
                m_requests.append(mr)
            else:
                mr = MaintenanceRequest(
                    unit_id=unit.id,
                    title="Leaking faucet",
                    description="Kitchen sink is leaking.",
                    priority="low",
                    status="resolved",
                    created_date=today - timedelta(days=20),
                    resolved_date=today - timedelta(days=18),
                    resolution_notes="Replaced O-ring."
                )
                m_requests.append(mr)

        db.add_all(payments)
        db.add_all(m_requests)
        db.commit()

        print("Database seeded successfully with Indian data!")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
