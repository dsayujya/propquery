import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { api } from "../api/client";
import { MapPin, BedDouble, Bath, Square, ArrowLeft, Calendar, CheckCircle2 } from "lucide-react";

export default function ListingDetail() {
  const { id } = useParams();
  const [property, setProperty] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showContactModal, setShowContactModal] = useState(false);

  useEffect(() => {
    const fetchProperty = async () => {
      try {
        const data = await api.getPublicListing(id);
        setProperty(data);
      } catch (error) {
        console.error("Failed to fetch property details", error);
      } finally {
        setLoading(false);
      }
    };
    fetchProperty();
  }, [id]);

  const formatCurrency = (val) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(val);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen bg-[var(--color-beige-bg)]">
        <div className="text-[var(--color-taupe-txt)] text-lg animate-pulse">Loading property details...</div>
      </div>
    );
  }

  if (!property) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-20 text-center">
        <h2 className="text-2xl font-bold text-[var(--color-charcoal-txt)]">Property not found</h2>
        <Link to="/" className="text-[var(--color-accent-blue)] mt-4 inline-block hover:underline">Return to listings</Link>
      </div>
    );
  }

  return (
    <div className="bg-white min-h-screen">
      {/* Hero Image Section */}
      <div className="relative h-[60vh] w-full bg-gray-900">
        {property.image_url ? (
          <img 
            src={property.image_url} 
            alt={property.name} 
            className="w-full h-full object-cover opacity-80"
          />
        ) : (
          <div className="w-full h-full bg-gray-200 flex items-center justify-center">
            <span className="text-gray-400">No Image</span>
          </div>
        )}
        
        <div className="absolute top-8 left-8">
          <Link to="/" className="flex items-center gap-2 bg-white/20 backdrop-blur-md hover:bg-white/40 text-white px-4 py-2 rounded-full transition-colors text-sm font-medium">
            <ArrowLeft size={16} /> Back to Search
          </Link>
        </div>
        
        <div className="absolute bottom-0 left-0 w-full bg-gradient-to-t from-black/80 to-transparent pt-32 pb-12 px-4 sm:px-6 lg:px-8">
          <div className="max-w-7xl mx-auto">
            <span className="inline-block px-3 py-1 bg-white/20 backdrop-blur-md text-white text-xs font-bold uppercase tracking-wider rounded-full mb-4">
              {property.property_type}
            </span>
            <h1 className="text-4xl md:text-5xl font-extrabold text-white mb-2">{property.name}</h1>
            <div className="flex items-center text-gray-300 text-lg">
              <MapPin size={20} className="mr-2" />
              {property.address}, {property.city}, {property.state} {property.zip_code}
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 flex flex-col lg:flex-row gap-12">
        {/* Main Content */}
        <div className="flex-1">
          <h2 className="text-2xl font-bold text-[var(--color-charcoal-txt)] mb-6 border-b border-[var(--color-taupe-border)] pb-4">About this property</h2>
          <p className="text-[var(--color-taupe-txt)] leading-relaxed mb-8">
            Experience luxury living at {property.name}. Located in the heart of {property.city}, this premium {property.property_type} offers modern amenities and spectacular views. Built in {property.year_built || "recent years"}, it stands as a testament to elegant architectural design combined with everyday functionality.
          </p>

          <h3 className="text-xl font-bold text-[var(--color-charcoal-txt)] mb-6">Available Units ({property.units.length})</h3>
          
          <div className="space-y-4">
            {property.units.map((unit) => (
              <div key={unit.id} className="border border-[var(--color-taupe-border)] rounded-xl p-6 flex flex-col md:flex-row items-center justify-between hover:border-[var(--color-accent-blue)] transition-colors">
                <div>
                  <div className="flex items-center gap-3 mb-2">
                    <h4 className="text-lg font-bold text-[var(--color-charcoal-txt)]">Unit {unit.unit_number}</h4>
                    <span className="px-2 py-1 bg-emerald-100 text-emerald-800 text-xs font-bold rounded-full flex items-center gap-1">
                      <CheckCircle2 size={12} /> Available Now
                    </span>
                  </div>
                  <div className="flex items-center gap-6 text-[var(--color-taupe-txt)] text-sm">
                    <span className="flex items-center gap-1"><BedDouble size={16}/> {unit.bedrooms} Bedrooms</span>
                    <span className="flex items-center gap-1"><Bath size={16}/> {unit.bathrooms} Bathrooms</span>
                    {unit.square_feet && <span className="flex items-center gap-1"><Square size={16}/> {unit.square_feet} sqft</span>}
                  </div>
                </div>
                <div className="mt-4 md:mt-0 text-right w-full md:w-auto flex md:flex-col items-center md:items-end justify-between">
                  <p className="text-2xl font-bold text-[var(--color-charcoal-txt)]">{formatCurrency(unit.market_rent)}<span className="text-sm font-normal text-[var(--color-taupe-txt)]">/mo</span></p>
                  <button onClick={() => setShowContactModal(true)} className="btn btn-secondary mt-2 text-sm">Apply Now</button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Sidebar */}
        <div className="w-full lg:w-96">
          <div className="bg-[var(--color-beige-bg)] rounded-2xl p-6 sticky top-24 border border-[var(--color-taupe-border)]">
            <h3 className="text-xl font-bold text-[var(--color-charcoal-txt)] mb-2">Interested?</h3>
            <p className="text-[var(--color-taupe-txt)] text-sm mb-6">Contact the owner to schedule a viewing or ask questions.</p>
            
            <button 
              onClick={() => setShowContactModal(true)}
              className="w-full btn btn-primary py-3 mb-4 text-center justify-center text-lg"
            >
              Contact Owner
            </button>
            <button 
              onClick={() => setShowContactModal(true)}
              className="w-full btn btn-secondary py-3 text-center justify-center flex items-center gap-2 text-lg"
            >
              <Calendar size={18} /> Schedule Tour
            </button>
            
            <div className="mt-6 pt-6 border-t border-[var(--color-taupe-border)] text-sm text-[var(--color-taupe-txt)] text-center">
              Listing ID: PRQ-{property.id}
            </div>
          </div>
        </div>
      </div>

      {/* Simple Modal */}
      {showContactModal && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl p-8 max-w-md w-full text-center">
            <h3 className="text-2xl font-bold text-[var(--color-charcoal-txt)] mb-2">Sign in required</h3>
            <p className="text-[var(--color-taupe-txt)] mb-8">You must have an account to contact property owners or submit rental applications.</p>
            <div className="flex flex-col gap-3">
              <Link to="/login" className="btn btn-primary w-full justify-center">Sign In</Link>
              <Link to="/signup" className="btn btn-secondary w-full justify-center">Create an Account</Link>
              <button onClick={() => setShowContactModal(false)} className="mt-4 text-[var(--color-taupe-txt)] hover:text-gray-900 font-medium">Cancel</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
