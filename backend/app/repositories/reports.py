"""Repository for SQL Reports."""

from typing import List, Dict, Any
from sqlalchemy import text
from sqlalchemy.orm import Session

class ReportRepository:
    
    @staticmethod
    def get_property_occupancy(db: Session, owner_id: int = None) -> List[Dict[str, Any]]:
        """A. Property Occupancy Report"""
        base_query = """
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
        """
        if owner_id:
            base_query += " WHERE p.owner_id = :owner_id"
            
        base_query += " GROUP BY p.id, p.name ORDER BY p.name;"
        
        query = text(base_query)
        params = {"owner_id": owner_id} if owner_id else {}
        result = db.execute(query, params).mappings().all()
        return [dict(row) for row in result]

    @staticmethod
    def get_rent_collection(db: Session, owner_id: int = None) -> List[Dict[str, Any]]:
        """B. Rent Collection Report"""
        where_clause = " WHERE p.owner_id = :owner_id" if owner_id else ""
        
        base_query = f"""
            WITH ExpectedRent AS (
                SELECT 
                    p.id AS property_id,
                    p.name AS property_name,
                    SUM(l.monthly_rent) AS expected_rent
                FROM properties p
                JOIN units u ON p.id = u.property_id
                JOIN leases l ON u.id = l.unit_id
                WHERE l.status = 'active'
                {"AND p.owner_id = :owner_id" if owner_id else ""}
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
                  {"AND p.owner_id = :owner_id" if owner_id else ""}
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
        """
        query = text(base_query)
        params = {"owner_id": owner_id} if owner_id else {}
        result = db.execute(query, params).mappings().all()
        return [dict(row) for row in result]

    @staticmethod
    def get_tenant_payment_history(db: Session, tenant_id: int = None, user_id: int = None) -> List[Dict[str, Any]]:
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
            WHERE 1=1
        """
        params = {}
        if tenant_id:
            base_query += " AND t.id = :tenant_id"
            params["tenant_id"] = tenant_id
        if user_id:
            base_query += " AND t.user_id = :user_id"
            params["user_id"] = user_id
            
        base_query += " ORDER BY pay.payment_date DESC"
        
        query = text(base_query)
        result = db.execute(query, params).mappings().all()
        return [dict(row) for row in result]

    @staticmethod
    def get_outstanding_payments(db: Session, owner_id: int = None) -> List[Dict[str, Any]]:
        """D. Outstanding Payments Report"""
        base_query = """
            SELECT 
                t.first_name || ' ' || t.last_name AS tenant_name,
                p.name AS property_name,
                u.unit_number,
                l.monthly_rent,
                COALESCE(SUM(CASE WHEN pay.status = 'completed' THEN pay.amount ELSE 0 END), 0) AS total_paid,
                COALESCE(SUM(CASE WHEN pay.status IN ('pending', 'failed') THEN pay.amount ELSE 0 END), 0) AS outstanding_balance
            FROM leases l
            JOIN tenants t ON l.tenant_id = t.id
            JOIN units u ON l.unit_id = u.id
            JOIN properties p ON u.property_id = p.id
            LEFT JOIN payments pay ON l.id = pay.lease_id
            WHERE l.status = 'active'
        """
        if owner_id:
            base_query += " AND p.owner_id = :owner_id"
            
        base_query += """
            GROUP BY t.id, t.first_name, t.last_name, p.name, u.unit_number, l.monthly_rent
            HAVING COALESCE(SUM(CASE WHEN pay.status IN ('pending', 'failed') THEN pay.amount ELSE 0 END), 0) > 0
            ORDER BY outstanding_balance DESC;
        """
        query = text(base_query)
        params = {"owner_id": owner_id} if owner_id else {}
        result = db.execute(query, params).mappings().all()
        return [dict(row) for row in result]

    @staticmethod
    def get_maintenance_performance(db: Session, owner_id: int = None, tenant_user_id: int = None) -> List[Dict[str, Any]]:
        """E. Maintenance Performance Report"""
        base_query = """
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
        """
        if tenant_user_id:
            # Join through lease and tenant to restrict to tenant's unit
            base_query = """
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
                FROM maintenance_requests mr
                JOIN units u ON mr.unit_id = u.id
                JOIN properties p ON u.property_id = p.id
                JOIN leases l ON u.id = l.unit_id
                JOIN tenants t ON l.tenant_id = t.id
                WHERE t.user_id = :tenant_user_id AND l.status = 'active'
            """
            
        elif owner_id:
            base_query += " WHERE p.owner_id = :owner_id"
            
        base_query += " GROUP BY p.id, p.name ORDER BY p.name;"
        query = text(base_query)
        
        params = {}
        if tenant_user_id:
            params["tenant_user_id"] = tenant_user_id
        elif owner_id:
            params["owner_id"] = owner_id
            
        result = db.execute(query, params).mappings().all()
        return [dict(row) for row in result]

    @staticmethod
    def get_property_financial_summary(db: Session, owner_id: int = None) -> List[Dict[str, Any]]:
        """F. Property Financial Summary"""
        base_query = """
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
        """
        if owner_id:
            base_query += " WHERE p.owner_id = :owner_id"
            
        base_query += " GROUP BY p.id, p.name ORDER BY total_revenue DESC;"
        query = text(base_query)
        params = {"owner_id": owner_id} if owner_id else {}
        result = db.execute(query, params).mappings().all()
        return [dict(row) for row in result]

    @staticmethod
    def get_monthly_revenue(db: Session, owner_id: int = None) -> List[Dict[str, Any]]:
        """G. Monthly Revenue Report"""
        base_query = """
            SELECT 
                TO_CHAR(pay.payment_date, 'YYYY-MM') AS revenue_month,
                SUM(pay.amount) AS total_revenue,
                COUNT(pay.id) AS payment_count
            FROM payments pay
        """
        if owner_id:
            base_query += """
                JOIN leases l ON pay.lease_id = l.id
                JOIN units u ON l.unit_id = u.id
                JOIN properties p ON u.property_id = p.id
                WHERE pay.status = 'completed' AND p.owner_id = :owner_id
            """
        else:
             base_query += " WHERE pay.status = 'completed'"
             
        base_query += " GROUP BY TO_CHAR(pay.payment_date, 'YYYY-MM') ORDER BY revenue_month DESC;"
        query = text(base_query)
        params = {"owner_id": owner_id} if owner_id else {}
        result = db.execute(query, params).mappings().all()
        return [dict(row) for row in result]

report_repository = ReportRepository()
