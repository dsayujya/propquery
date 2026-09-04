import { useState, useEffect } from "react";
import { api } from "../api/client";
import Card from "../components/ui/Card";
import DataTable from "../components/ui/DataTable";
import Modal from "../components/ui/Modal";

export default function Tenants() {
  const [tenants, setTenants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState({
    first_name: "", last_name: "", email: "", phone_number: ""
  });
  const [submitting, setSubmitting] = useState(false);

  const fetchTenants = () => {
    setLoading(true);
    api.getTenants()
      .then(data => {
        setTenants(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchTenants();
  }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await api.createTenant(formData);
      setIsModalOpen(false);
      fetchTenants();
      setFormData({ first_name: "", last_name: "", email: "", phone_number: "" });
    } catch (err) {
      console.error(err);
      alert("Failed to create tenant.");
    } finally {
      setSubmitting(false);
    }
  };

  const columns = [
    { header: "ID", accessor: "id" },
    { header: "Name", render: (row) => <span className="font-medium text-[var(--color-charcoal-txt)]">{row.first_name} {row.last_name}</span> },
    { header: "Email", accessor: "email" },
    { header: "Phone", accessor: "phone_number" },
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold text-[var(--color-charcoal-txt)]">Tenant Directory</h2>
        <button className="btn btn-primary" onClick={() => setIsModalOpen(true)}>Add Tenant</button>
      </div>

      <Card>
        <DataTable 
          columns={columns} 
          data={tenants} 
          isLoading={loading} 
          emptyMessage="No tenants found." 
        />
      </Card>

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Add New Tenant">
        <form onSubmit={handleCreate} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">First Name</label>
              <input required type="text" className="input" value={formData.first_name} onChange={e => setFormData({...formData, first_name: e.target.value})} />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Last Name</label>
              <input required type="text" className="input" value={formData.last_name} onChange={e => setFormData({...formData, last_name: e.target.value})} />
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Email</label>
            <input required type="email" className="input" value={formData.email} onChange={e => setFormData({...formData, email: e.target.value})} />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Phone Number</label>
            <input type="text" className="input" value={formData.phone_number} onChange={e => setFormData({...formData, phone_number: e.target.value})} />
          </div>
          <div className="flex justify-end gap-3 mt-6">
            <button type="button" className="btn btn-secondary" onClick={() => setIsModalOpen(false)}>Cancel</button>
            <button type="submit" className="btn btn-primary" disabled={submitting}>
              {submitting ? "Saving..." : "Save Tenant"}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
