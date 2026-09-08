import { useState, useEffect } from "react";
import { api } from "../api/client";
import Card from "../components/ui/Card";
import DataTable from "../components/ui/DataTable";
import Modal from "../components/ui/Modal";
import { Plus } from "lucide-react";

export default function Properties() {
  const [properties, setProperties] = useState([]);
  const [loading, setLoading] = useState(true);
  
  // Property Modal State
  const [isPropModalOpen, setIsPropModalOpen] = useState(false);
  const [propFormData, setPropFormData] = useState({
    name: "", address: "", city: "", state: "", zip_code: "", property_type: "apartment", year_built: ""
  });
  const [imageFile, setImageFile] = useState(null);
  const [submittingProp, setSubmittingProp] = useState(false);

  // Unit Modal State
  const [isUnitModalOpen, setIsUnitModalOpen] = useState(false);
  const [selectedPropId, setSelectedPropId] = useState(null);
  const [unitFormData, setUnitFormData] = useState({
    unit_number: "", bedrooms: 1, bathrooms: 1, square_feet: "", market_rent: "", status: "vacant"
  });
  const [submittingUnit, setSubmittingUnit] = useState(false);

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

  const handleCreateProperty = async (e) => {
    e.preventDefault();
    setSubmittingProp(true);
    try {
      let image_url = null;
      
      // 1. Upload Image if selected
      if (imageFile) {
        const formData = new FormData();
        formData.append("file", imageFile);
        const uploadRes = await api.uploadImage(formData);
        image_url = uploadRes.image_url;
      }

      // 2. Create Property with image_url
      await api.createProperty({
        ...propFormData,
        year_built: parseInt(propFormData.year_built) || null,
        image_url: image_url
      });
      
      setIsPropModalOpen(false);
      fetchProperties();
      setPropFormData({ name: "", address: "", city: "", state: "", zip_code: "", property_type: "apartment", year_built: "" });
      setImageFile(null);
    } catch (err) {
      console.error(err);
      alert("Failed to create property.");
    } finally {
      setSubmittingProp(false);
    }
  };

  const handleCreateUnit = async (e) => {
    e.preventDefault();
    setSubmittingUnit(true);
    try {
      await api.createUnit({
        ...unitFormData,
        property_id: selectedPropId,
        bedrooms: parseInt(unitFormData.bedrooms),
        bathrooms: parseInt(unitFormData.bathrooms),
        square_feet: parseInt(unitFormData.square_feet) || null,
        market_rent: parseFloat(unitFormData.market_rent)
      });
      
      setIsUnitModalOpen(false);
      alert("Unit created successfully!");
      // Might want to fetch units if we displayed them, but for now just close modal
      setUnitFormData({ unit_number: "", bedrooms: 1, bathrooms: 1, square_feet: "", market_rent: "", status: "vacant" });
    } catch (err) {
      console.error(err);
      alert("Failed to create unit.");
    } finally {
      setSubmittingUnit(false);
    }
  };

  const openUnitModal = (propId) => {
    setSelectedPropId(propId);
    setIsUnitModalOpen(true);
  };

  const columns = [
    { header: "ID", accessor: "id" },
    { header: "Image", render: (row) => row.image_url ? <img src={row.image_url} alt="property" className="w-12 h-12 rounded object-cover" /> : <div className="w-12 h-12 bg-gray-200 rounded"></div> },
    { header: "Property Name", accessor: "name" },
    { header: "City", accessor: "city" },
    { header: "Type", accessor: "property_type" },
    { header: "Actions", render: (row) => (
      <button onClick={() => openUnitModal(row.id)} className="text-[var(--color-accent-blue)] hover:underline flex items-center text-sm font-medium">
        <Plus size={16} className="mr-1" /> Add Unit
      </button>
    ) }
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold text-[var(--color-charcoal-txt)]">Property Portfolio</h2>
        <button className="btn btn-primary" onClick={() => setIsPropModalOpen(true)}>Add Property</button>
      </div>

      <Card>
        <DataTable 
          columns={columns} 
          data={properties} 
          isLoading={loading} 
          emptyMessage="No properties found in the portfolio." 
        />
      </Card>

      {/* Add Property Modal */}
      <Modal isOpen={isPropModalOpen} onClose={() => setIsPropModalOpen(false)} title="Add New Property">
        <form onSubmit={handleCreateProperty} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Property Name</label>
            <input required type="text" className="input" value={propFormData.name} onChange={e => setPropFormData({...propFormData, name: e.target.value})} />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Address</label>
            <input required type="text" className="input" value={propFormData.address} onChange={e => setPropFormData({...propFormData, address: e.target.value})} />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">City</label>
              <input required type="text" className="input" value={propFormData.city} onChange={e => setPropFormData({...propFormData, city: e.target.value})} />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">State</label>
              <input required type="text" className="input" value={propFormData.state} onChange={e => setPropFormData({...propFormData, state: e.target.value})} />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Zip Code</label>
              <input required type="text" className="input" value={propFormData.zip_code} onChange={e => setPropFormData({...propFormData, zip_code: e.target.value})} />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Year Built</label>
              <input type="number" className="input" value={propFormData.year_built} onChange={e => setPropFormData({...propFormData, year_built: e.target.value})} />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Property Type</label>
              <select className="input" value={propFormData.property_type} onChange={e => setPropFormData({...propFormData, property_type: e.target.value})}>
                <option value="apartment">Apartment</option>
                <option value="complex">Complex</option>
                <option value="house">House</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Property Image</label>
              <input 
                type="file" 
                accept="image/*" 
                className="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-[var(--color-accent-blue)] file:text-white hover:file:bg-blue-700" 
                onChange={e => setImageFile(e.target.files[0])} 
              />
            </div>
          </div>
          <div className="flex justify-end gap-3 mt-6 pt-4 border-t border-[var(--color-taupe-border)]">
            <button type="button" className="btn btn-secondary" onClick={() => setIsPropModalOpen(false)}>Cancel</button>
            <button type="submit" className="btn btn-primary" disabled={submittingProp}>
              {submittingProp ? "Uploading & Saving..." : "Save Property"}
            </button>
          </div>
        </form>
      </Modal>

      {/* Add Unit Modal */}
      <Modal isOpen={isUnitModalOpen} onClose={() => setIsUnitModalOpen(false)} title="Add Unit to Property">
        <form onSubmit={handleCreateUnit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Unit Number</label>
            <input required type="text" className="input" value={unitFormData.unit_number} onChange={e => setUnitFormData({...unitFormData, unit_number: e.target.value})} placeholder="e.g. 101, Apt B" />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Bedrooms</label>
              <input required type="number" min="0" className="input" value={unitFormData.bedrooms} onChange={e => setUnitFormData({...unitFormData, bedrooms: e.target.value})} />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Bathrooms</label>
              <input required type="number" min="0" className="input" value={unitFormData.bathrooms} onChange={e => setUnitFormData({...unitFormData, bathrooms: e.target.value})} />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Square Feet (Optional)</label>
              <input type="number" className="input" value={unitFormData.square_feet} onChange={e => setUnitFormData({...unitFormData, square_feet: e.target.value})} />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Market Rent (₹)</label>
              <input required type="number" step="0.01" className="input" value={unitFormData.market_rent} onChange={e => setUnitFormData({...unitFormData, market_rent: e.target.value})} />
            </div>
          </div>
          <div className="flex justify-end gap-3 mt-6 pt-4 border-t border-[var(--color-taupe-border)]">
            <button type="button" className="btn btn-secondary" onClick={() => setIsUnitModalOpen(false)}>Cancel</button>
            <button type="submit" className="btn btn-primary" disabled={submittingUnit}>
              {submittingUnit ? "Saving..." : "Save Unit"}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
