import { useState, useEffect } from "react";
import { api } from "../api/client";
import Card from "../components/ui/Card";
import DataTable from "../components/ui/DataTable";
import StatusBadge from "../components/ui/StatusBadge";
import Modal from "../components/ui/Modal";

export default function Support() {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState({
    title: "", description: "", category: "General", priority: "Low"
  });
  const [submitting, setSubmitting] = useState(false);

  const fetchTickets = () => {
    setLoading(true);
    api.getSupportTickets()
      .then(data => {
        setTickets(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchTickets();
  }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await api.createSupportTicket(formData);
      setIsModalOpen(false);
      fetchTickets();
      setFormData({ title: "", description: "", category: "General", priority: "Low" });
    } catch (err) {
      console.error(err);
      alert("Failed to create ticket.");
    } finally {
      setSubmitting(false);
    }
  };

  const columns = [
    { header: "Ticket ID", render: (row) => `#${row.id}` },
    { header: "Title", render: (row) => <span className="font-medium">{row.title}</span> },
    { header: "Category", accessor: "category" },
    { header: "Assigned To", accessor: "assigned_engineer" },
    { header: "Status", render: (row) => <StatusBadge status={row.status} /> },
    { header: "Created", render: (row) => new Date(row.created_at).toLocaleDateString(), align: "right" }
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold text-[var(--color-charcoal-txt)]">Application Support</h2>
        <button className="btn btn-primary" onClick={() => setIsModalOpen(true)}>New Ticket</button>
      </div>

      <Card>
        <DataTable 
          columns={columns} 
          data={tickets} 
          isLoading={loading} 
          emptyMessage="No support tickets found." 
        />
      </Card>

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Create Support Ticket">
        <form onSubmit={handleCreate} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Title</label>
            <input required type="text" className="input" value={formData.title} onChange={e => setFormData({...formData, title: e.target.value})} />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Description</label>
            <textarea required className="input min-h-[100px]" value={formData.description} onChange={e => setFormData({...formData, description: e.target.value})} />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Category</label>
              <select className="input" value={formData.category} onChange={e => setFormData({...formData, category: e.target.value})}>
                <option value="General">General</option>
                <option value="Bug">Bug</option>
                <option value="Feature Request">Feature Request</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Priority</label>
              <select className="input" value={formData.priority} onChange={e => setFormData({...formData, priority: e.target.value})}>
                <option value="Low">Low</option>
                <option value="Medium">Medium</option>
                <option value="High">High</option>
              </select>
            </div>
          </div>
          <div className="flex justify-end gap-3 mt-6">
            <button type="button" className="btn btn-secondary" onClick={() => setIsModalOpen(false)}>Cancel</button>
            <button type="submit" className="btn btn-primary" disabled={submitting}>
              {submitting ? "Submitting..." : "Submit Ticket"}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
