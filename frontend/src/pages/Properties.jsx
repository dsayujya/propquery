import { useState, useEffect } from "react";
import { api } from "../api/client";
import Card from "../components/ui/Card";
import DataTable from "../components/ui/DataTable";
import Modal from "../components/ui/Modal";

export default function Properties() {
  const [properties, setProperties] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState({
    name: "", address: "", city: "", state: "", zip_code: "", property_type: "Residential", year_built: ""
  });
  const [submitting, setSubmitting] = useState(false);

  const fetchProperties = () => {
    setLoading(true);
    api.getProperties()
      .then(data => {
        setProperties(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchProperties();
  }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await api.createProperty({
        ...formData,
        year_built: parseInt(formData.year_built) || null
      });
      setIsModalOpen(false);
      fetchProperties();
      setFormData({ name: "", address: "", city: "", state: "", zip_code: "", property_type: "Residential", year_built: "" });
    } catch (err) {
      console.error(err);
      alert("Failed to create property.");
    } finally {
      setSubmitting(false);
    }
  };

  const columns = [
    { header: "ID", accessor: "id" },
    { header: "Property Name", accessor: "name" },
    { header: "Address", accessor: "address" },
    { header: "City", accessor: "city" },
    { header: "Type", accessor: "property_type" },
    { header: "Built", accessor: "year_built", align: "right" }
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold text-[var(--color-charcoal-txt)]">Property Portfolio</h2>
        <button className="btn btn-primary" onClick={() => setIsModalOpen(true)}>Add Property</button>
      </div>

      <Card>
        <DataTable 
          columns={columns} 
          data={properties} 
          isLoading={loading} 
          emptyMessage="No properties found in the portfolio." 
        />
      </Card>

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Add New Property">
        <form onSubmit={handleCreate} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Property Name</label>
            <input required type="text" className="input" value={formData.name} onChange={e => setFormData({...formData, name: e.target.value})} />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Address</label>
            <input required type="text" className="input" value={formData.address} onChange={e => setFormData({...formData, address: e.target.value})} />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">City</label>
              <input required type="text" className="input" value={formData.city} onChange={e => setFormData({...formData, city: e.target.value})} />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">State</label>
              <input required type="text" className="input" value={formData.state} onChange={e => setFormData({...formData, state: e.target.value})} />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Zip Code</label>
              <input required type="text" className="input" value={formData.zip_code} onChange={e => setFormData({...formData, zip_code: e.target.value})} />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Year Built</label>
              <input type="number" className="input" value={formData.year_built} onChange={e => setFormData({...formData, year_built: e.target.value})} />
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Property Type</label>
            <select className="input" value={formData.property_type} onChange={e => setFormData({...formData, property_type: e.target.value})}>
              <option value="Residential">Residential</option>
              <option value="Commercial">Commercial</option>
              <option value="Mixed-Use">Mixed-Use</option>
            </select>
          </div>
          <div className="flex justify-end gap-3 mt-6">
            <button type="button" className="btn btn-secondary" onClick={() => setIsModalOpen(false)}>Cancel</button>
            <button type="submit" className="btn btn-primary" disabled={submitting}>
              {submitting ? "Saving..." : "Save Property"}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
