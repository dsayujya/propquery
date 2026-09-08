import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client";
import { MapPin, BedDouble, Bath, Square, ArrowRight } from "lucide-react";

export default function Listings() {
  const [listings, setListings] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchListings = async () => {
      try {
        const data = await api.getPublicListings();
        setListings(data);
      } catch (error) {
        console.error("Failed to fetch listings", error);
      } finally {
        setLoading(false);
      }
    };
    fetchListings();
  }, []);

  const formatCurrency = (val) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(val);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-96">
        <div className="text-[var(--color-taupe-txt)] text-lg animate-pulse">Discovering beautiful homes...</div>
      </div>
    );
  }

  return (
    <div>
      {/* Hero Section */}
      <div className="bg-[var(--color-charcoal-txt)] text-white py-24 px-4 sm:px-6 lg:px-8 text-center relative overflow-hidden">
        <div className="absolute inset-0 opacity-20 bg-[url('https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&q=80')] bg-cover bg-center"></div>
        <div className="relative z-10 max-w-3xl mx-auto">
          <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold tracking-tight mb-6">
            Find your next perfect home.
          </h1>
          <p className="text-lg sm:text-xl text-gray-300 font-light mb-10">
            Browse our curated collection of premium apartments and lofts across India.
          </p>
          <div className="flex max-w-md mx-auto bg-white rounded-full p-2 shadow-lg">
            <input 
              type="text" 
              placeholder="Search by city (e.g., Mumbai, Bengaluru)" 
              className="flex-1 px-6 py-3 rounded-l-full focus:outline-none text-gray-900"
            />
            <button className="bg-[var(--color-accent-blue)] text-white px-8 py-3 rounded-full font-medium hover:bg-blue-700 transition-colors">
              Search
            </button>
          </div>
        </div>
      </div>

      {/* Listings Grid */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="flex justify-between items-end mb-10">
          <div>
            <h2 className="text-3xl font-bold text-[var(--color-charcoal-txt)]">Featured Properties</h2>
            <p className="text-[var(--color-taupe-txt)] mt-2">Explore {listings.length} available properties in our network.</p>
          </div>
        </div>

        {listings.length === 0 ? (
          <div className="text-center py-20 bg-white rounded-2xl shadow-sm border border-[var(--color-taupe-border)]">
            <p className="text-lg text-[var(--color-taupe-txt)]">No vacant properties available at the moment.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-10">
            {listings.map((property) => {
              // Find the cheapest unit to show "Starting at"
              const cheapestUnit = property.units.reduce((prev, curr) => prev.market_rent < curr.market_rent ? prev : curr, property.units[0]);
              
              return (
                <Link to={`/listings/${property.id}`} key={property.id} className="group flex flex-col bg-white rounded-2xl overflow-hidden shadow-sm hover:shadow-xl transition-all duration-300 border border-[var(--color-taupe-border)]">
                  <div className="relative h-72 w-full overflow-hidden">
                    {property.image_url ? (
                      <img 
                        src={property.image_url} 
                        alt={property.name} 
                        className="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-700"
                      />
                    ) : (
                      <div className="w-full h-full bg-gray-200 flex items-center justify-center">
                        <span className="text-gray-400">No Image</span>
                      </div>
                    )}
                    <div className="absolute top-4 left-4 bg-white/90 backdrop-blur-sm px-3 py-1 rounded-full text-xs font-bold text-[var(--color-charcoal-txt)]">
                      {property.units.length} Unit{property.units.length !== 1 ? 's' : ''} Available
                    </div>
                  </div>
                  
                  <div className="p-6 flex-1 flex flex-col">
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="text-2xl font-bold text-[var(--color-charcoal-txt)] group-hover:text-[var(--color-accent-blue)] transition-colors">
                        {property.name}
                      </h3>
                      <div className="text-right">
                        <p className="text-xs text-[var(--color-taupe-txt)] font-medium uppercase tracking-wider">Starting at</p>
                        <p className="text-xl font-bold text-[var(--color-accent-blue)]">{formatCurrency(cheapestUnit.market_rent)}</p>
                      </div>
                    </div>
                    
                    <div className="flex items-center text-[var(--color-taupe-txt)] mb-6">
                      <MapPin size={16} className="mr-1" />
                      <span className="text-sm">{property.address}, {property.city}</span>
                    </div>
                    
                    <div className="mt-auto pt-6 border-t border-[var(--color-taupe-border)] flex items-center justify-between text-sm text-[var(--color-taupe-txt)]">
                      <div className="flex gap-4">
                        <span className="flex items-center gap-1"><BedDouble size={16}/> {cheapestUnit.bedrooms} Beds</span>
                        <span className="flex items-center gap-1"><Bath size={16}/> {cheapestUnit.bathrooms} Baths</span>
                        {cheapestUnit.square_feet && <span className="flex items-center gap-1"><Square size={16}/> {cheapestUnit.square_feet} sqft</span>}
                      </div>
                      <div className="flex items-center text-[var(--color-accent-blue)] font-medium">
                        View Details <ArrowRight size={16} className="ml-1 group-hover:translate-x-1 transition-transform" />
                      </div>
                    </div>
                  </div>
                </Link>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
