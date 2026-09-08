import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";
import Card from "../components/ui/Card";
import DataTable from "../components/ui/DataTable";

function AdminOwnerDashboard() {
  const [loading, setLoading] = useState(true);
  const [metrics, setMetrics] = useState({
    totalProperties: 0,
    occupancyRate: 0,
    collectedRent: 0,
    openTickets: 0,
  });
  const [rentData, setRentData] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        const [occupancy, rent, maintenance] = await Promise.all([
          api.getOccupancyReport(),
          api.getRentCollection(),
          api.getMaintenancePerformance()
        ]);

        const totalProps = occupancy.length;
        
        let totalUnits = 0;
        let occupiedUnits = 0;
        occupancy.forEach(p => {
          totalUnits += p.total_units;
          occupiedUnits += p.occupied_units;
        });
        const occRate = totalUnits > 0 ? ((occupiedUnits / totalUnits) * 100).toFixed(1) : 0;

        let totalCollected = 0;
        rent.forEach(p => {
          totalCollected += p.collected_rent;
        });

        let totalOpenTickets = 0;
        maintenance.forEach(p => {
          totalOpenTickets += p.open_requests;
        });

        setMetrics({
          totalProperties: totalProps,
          occupancyRate: occRate,
          collectedRent: totalCollected,
          openTickets: totalOpenTickets
        });
        
        setRentData(rent);

      } catch (error) {
        console.error("Failed to fetch dashboard data", error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const formatCurrency = (val) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(val);

  const rentColumns = [
    { header: "Property", accessor: "property_name" },
    { header: "Expected", render: (row) => formatCurrency(row.expected_rent), align: "right" },
    { header: "Collected", render: (row) => formatCurrency(row.collected_rent), align: "right" },
    { header: "Outstanding", render: (row) => (
      <span className={row.outstanding_amount > 0 ? "text-amber-600 font-medium" : "text-emerald-600 font-medium"}>
        {formatCurrency(row.outstanding_amount)}
      </span>
    ), align: "right" },
    { header: "Collection %", render: (row) => `${row.collection_percentage}%`, align: "right" }
  ];

  if (loading) return <div className="text-[var(--color-taupe-txt)]">Loading dashboard...</div>;

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <h3 className="text-sm font-medium text-[var(--color-taupe-txt)]">Total Properties</h3>
          <p className="text-3xl font-bold mt-2 text-[var(--color-charcoal-txt)]">{metrics.totalProperties}</p>
        </Card>
        <Card>
          <h3 className="text-sm font-medium text-[var(--color-taupe-txt)]">Avg Occupancy Rate</h3>
          <p className="text-3xl font-bold mt-2 text-[var(--color-charcoal-txt)]">{metrics.occupancyRate}%</p>
        </Card>
        <Card>
          <h3 className="text-sm font-medium text-[var(--color-taupe-txt)]">MTD Collected Rent</h3>
          <p className="text-3xl font-bold mt-2 text-[var(--color-charcoal-txt)]">{formatCurrency(metrics.collectedRent)}</p>
        </Card>
        <Card>
          <h3 className="text-sm font-medium text-[var(--color-taupe-txt)]">Open Maintenance</h3>
          <p className="text-3xl font-bold mt-2 text-[var(--color-charcoal-txt)]">{metrics.openTickets}</p>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <Card title="Rent Collection by Property" subtitle="Month-to-date collection status">
            {rentData.length > 0 ? (
              <DataTable columns={rentColumns} data={rentData} />
            ) : (
              <div className="text-sm text-[var(--color-taupe-txt)]">No rent data available.</div>
            )}
          </Card>
        </div>
        <div className="lg:col-span-1">
          <Card title="Quick Actions">
            <div className="space-y-3">
              <button onClick={() => navigate('/tenants')} className="btn btn-primary w-full justify-start">Manage Tenants</button>
              <button onClick={() => navigate('/payments')} className="btn btn-secondary w-full justify-start">Log Payment</button>
              <button onClick={() => navigate('/maintenance')} className="btn btn-secondary w-full justify-start">Maintenance Requests</button>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}

function TenantDashboard() {
  const [loading, setLoading] = useState(true);
  const [payments, setPayments] = useState([]);
  const [maintenance, setMaintenance] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        const [paymentHistory, maintPerf] = await Promise.all([
          api.getTenantPayments(),
          api.getMaintenancePerformance()
        ]);
        setPayments(paymentHistory || []);
        setMaintenance(maintPerf || []);
      } catch (error) {
        console.error("Failed to fetch tenant dashboard data", error);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboardData();
  }, []);

  const formatCurrency = (val) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(val);
  const formatDate = (dateString) => new Date(dateString).toLocaleDateString();

  const paymentColumns = [
    { header: "Date", render: (row) => formatDate(row.payment_date) },
    { header: "Amount", render: (row) => formatCurrency(row.amount), align: "right" },
    { header: "Status", render: (row) => (
      <span className={`px-2 py-1 text-xs rounded-full ${row.status === 'completed' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'}`}>
        {row.status}
      </span>
    ) }
  ];

  if (loading) return <div className="text-[var(--color-taupe-txt)]">Loading dashboard...</div>;

  const totalPaid = payments.filter(p => p.status === 'completed').reduce((sum, p) => sum + p.amount, 0);
  const totalOpenMaint = maintenance.reduce((sum, p) => sum + p.open_requests, 0);

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Card>
          <h3 className="text-sm font-medium text-[var(--color-taupe-txt)]">Total Paid (Lifetime)</h3>
          <p className="text-3xl font-bold mt-2 text-[var(--color-charcoal-txt)]">{formatCurrency(totalPaid)}</p>
        </Card>
        <Card>
          <h3 className="text-sm font-medium text-[var(--color-taupe-txt)]">Recent Payments</h3>
          <p className="text-3xl font-bold mt-2 text-[var(--color-charcoal-txt)]">{payments.length}</p>
        </Card>
        <Card>
          <h3 className="text-sm font-medium text-[var(--color-taupe-txt)]">Open Maintenance</h3>
          <p className="text-3xl font-bold mt-2 text-[var(--color-charcoal-txt)]">{totalOpenMaint}</p>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <Card title="Payment History">
            {payments.length > 0 ? (
              <DataTable columns={paymentColumns} data={payments} />
            ) : (
              <div className="text-sm text-[var(--color-taupe-txt)]">No payment history available.</div>
            )}
          </Card>
        </div>
        <div className="lg:col-span-1">
          <Card title="Quick Actions">
            <div className="space-y-3">
              <button onClick={() => navigate('/payments')} className="btn btn-primary w-full justify-start">Make a Payment</button>
              <button onClick={() => navigate('/maintenance')} className="btn btn-secondary w-full justify-start">Request Maintenance</button>
              <button onClick={() => navigate('/support')} className="btn btn-secondary w-full justify-start">Contact Support</button>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}

export default function Dashboard() {
  const { user } = useAuth();
  
  if (!user) return null;

  if (user.role === 'tenant') {
    return <TenantDashboard />;
  }
  
  return <AdminOwnerDashboard />;
}
