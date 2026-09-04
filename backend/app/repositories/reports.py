"""Repository for SQL Reports."""

from typing import List, Dict, Any
from sqlalchemy import text
from sqlalchemy.orm import Session

class ReportRepository:
    
    @staticmethod
    def get_property_occupancy(db: Session) -> List[Dict[str, Any]]:
        """A. Property Occupancy Report"""
        query = text("""
            SELECT 
                p.name AS property_name,
                COUNT(u.id) AS total_units,
                SUM(CASE WHEN u.status = 'occupied' THEN 1 ELSE 0 END) AS occupied_units,
                SUM(CASE WHEN u.status = 'vacant' THEN 1 ELSE 0 END) AS vacant_units,
                CASE 
                    WHEN COUNT(u.id) = 0 THEN 0.0
                    ELSE ROUND((SUM(CASE WHEN u.status = 'occupied' THEN 1.0 ELSE 0.0 END) / COUNT(u.id)) * 100, 2)
                END AS occupancy_percentage
            FROM properties p
            LEFT JOIN units u ON p.id = u.property_id
            GROUP BY p.id, p.name
            ORDER BY p.name;
        """)
        result = db.execute(query).mappings().all()
        return [dict(row) for row in result]

    @staticmethod
    def get_rent_collection(db: Session) -> List[Dict[str, Any]]:
        """B. Rent Collection Report"""
        query = text("""
            WITH ExpectedRent AS (
                SELECT 
                    p.id AS property_id,
                    p.name AS property_name,
                    SUM(l.monthly_rent) AS expected_rent
                FROM properties p
                JOIN units u ON p.id = u.property_id
                JOIN leases l ON u.id = l.unit_id
                WHERE l.status = 'active'
                GROUP BY p.id, p.name
            ),
            CollectedRent AS (
                SELECT 
                    p.id AS property_id,
                    SUM(pay.amount) AS collected_rent
                FROM properties p
                JOIN units u ON p.id = u.property_id
                JOIN leases l ON u.id = l.unit_id
                JOIN payments pay ON l.id = pay.lease_id
                WHERE pay.status = 'completed'
                  AND EXTRACT(MONTH FROM pay.payment_date) = EXTRACT(MONTH FROM CURRENT_DATE)
                  AND EXTRACT(YEAR FROM pay.payment_date) = EXTRACT(YEAR FROM CURRENT_DATE)
                GROUP BY p.id
            )
            SELECT 
                er.property_name,
                COALESCE(er.expected_rent, 0) AS expected_rent,
                COALESCE(cr.collected_rent, 0) AS collected_rent,
                GREATEST(0, COALESCE(er.expected_rent, 0) - COALESCE(cr.collected_rent, 0)) AS outstanding_amount,
                CASE 
                    WHEN COALESCE(er.expected_rent, 0) = 0 THEN 0.0
                    ELSE ROUND((COALESCE(cr.collected_rent, 0) / er.expected_rent) * 100, 2)
                END AS collection_percentage
            FROM ExpectedRent er
            LEFT JOIN CollectedRent cr ON er.property_id = cr.property_id
            ORDER BY er.property_name;
        """)
        result = db.execute(query).mappings().all()
        return [dict(row) for row in result]

    @staticmethod
    def get_tenant_payment_history(db: Session, tenant_id: int = None) -> List[Dict[str, Any]]:
        """C. Tenant Payment History"""
        base_query = """
            SELECT 
                t.first_name || ' ' || t.last_name AS tenant_name,
                u.unit_number,
                p.name AS property_name,
                pay.payment_date,
                pay.amount,
                pay.status
            FROM tenants t
            JOIN leases l ON t.id = l.tenant_id
            JOIN units u ON l.unit_id = u.id
            JOIN properties p ON u.property_id = p.id
            JOIN payments pay ON l.id = pay.lease_id
        """
        if tenant_id:
            base_query += " WHERE t.id = :tenant_id"
            
        base_query += " ORDER BY pay.payment_date DESC"
        
        query = text(base_query)
        params = {"tenant_id": tenant_id} if tenant_id else {}
        result = db.execute(query, params).mappings().all()
        return [dict(row) for row in result]

    @staticmethod
    def get_outstanding_payments(db: Session) -> List[Dict[str, Any]]:
        """D. Outstanding Payments Report"""
        query = text("""
            SELECT 
                t.first_name || ' ' || t.last_name AS tenant_name,
                p.name AS property_name,
                u.unit_number,
                l.monthly_rent,
                COALESCE(SUM(CASE WHEN pay.status = 'completed' THEN pay.amount ELSE 0 END), 0) AS total_paid,
                -- A simplistic outstanding logic for demo: assume outstanding if payment is pending/failed
                COALESCE(SUM(CASE WHEN pay.status IN ('pending', 'failed') THEN pay.amount ELSE 0 END), 0) AS outstanding_balance
            FROM leases l
            JOIN tenants t ON l.tenant_id = t.id
            JOIN units u ON l.unit_id = u.id
            JOIN properties p ON u.property_id = p.id
            LEFT JOIN payments pay ON l.id = pay.lease_id
            WHERE l.status = 'active'
            GROUP BY t.id, t.first_name, t.last_name, p.name, u.unit_number, l.monthly_rent
            HAVING COALESCE(SUM(CASE WHEN pay.status IN ('pending', 'failed') THEN pay.amount ELSE 0 END), 0) > 0
            ORDER BY outstanding_balance DESC;
        """)
        result = db.execute(query).mappings().all()
        return [dict(row) for row in result]

    @staticmethod
    def get_maintenance_performance(db: Session) -> List[Dict[str, Any]]:
        """E. Maintenance Performance Report"""
        query = text("""
            SELECT 
                p.name AS property_name,
                COUNT(mr.id) AS total_requests,
                SUM(CASE WHEN mr.status IN ('open', 'in_progress') THEN 1 ELSE 0 END) AS open_requests,
                SUM(CASE WHEN mr.status IN ('resolved', 'closed') THEN 1 ELSE 0 END) AS resolved_requests,
                ROUND(AVG(
                    CASE 
                        WHEN mr.status IN ('resolved', 'closed') AND mr.resolved_date IS NOT NULL 
                        THEN mr.resolved_date - mr.created_date
                        ELSE NULL 
                    END
                ), 1) AS avg_resolution_days
            FROM properties p
            LEFT JOIN units u ON p.id = u.property_id
            LEFT JOIN maintenance_requests mr ON u.id = mr.unit_id
            GROUP BY p.id, p.name
            ORDER BY p.name;
        """)
        result = db.execute(query).mappings().all()
        return [dict(row) for row in result]

    @staticmethod
    def get_property_financial_summary(db: Session) -> List[Dict[str, Any]]:
        """F. Property Financial Summary"""
        query = text("""
            SELECT 
                p.name AS property_name,
                COALESCE(SUM(pay.amount), 0) AS total_revenue,
                COUNT(DISTINCT u.id) AS total_units,
                CASE 
                    WHEN COUNT(DISTINCT u.id) = 0 THEN 0.0
                    ELSE ROUND(COALESCE(SUM(pay.amount), 0) / COUNT(DISTINCT u.id), 2)
                END AS avg_rent_per_unit
            FROM properties p
            LEFT JOIN units u ON p.id = u.property_id
            LEFT JOIN leases l ON u.id = l.unit_id
            LEFT JOIN payments pay ON l.id = pay.lease_id AND pay.status = 'completed'
            GROUP BY p.id, p.name
            ORDER BY total_revenue DESC;
        """)
        result = db.execute(query).mappings().all()
        return [dict(row) for row in result]

    @staticmethod
    def get_monthly_revenue(db: Session) -> List[Dict[str, Any]]:
        """G. Monthly Revenue Report"""
        query = text("""
            SELECT 
                TO_CHAR(payment_date, 'YYYY-MM') AS revenue_month,
                SUM(amount) AS total_revenue,
                COUNT(id) AS payment_count
            FROM payments
            WHERE status = 'completed'
            GROUP BY TO_CHAR(payment_date, 'YYYY-MM')
            ORDER BY revenue_month DESC;
        """)
        result = db.execute(query).mappings().all()
        return [dict(row) for row in result]

report_repository = ReportRepository()
