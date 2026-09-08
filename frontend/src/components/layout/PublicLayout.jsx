import { Outlet, Link } from "react-router-dom";
import { Building2 } from "lucide-react";

export default function PublicLayout() {
  return (
    <div className="min-h-screen bg-[var(--color-beige-bg)] font-sans">
      <header className="bg-white border-b border-[var(--color-taupe-border)] sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <Link to="/" className="flex items-center gap-2">
              <div className="bg-[var(--color-accent-blue)] text-white p-2 rounded-lg">
                <Building2 size={24} />
              </div>
              <span className="text-xl font-bold text-[var(--color-charcoal-txt)] tracking-tight">PropQuery</span>
            </Link>
            
            <nav className="hidden md:flex gap-8">
              <Link to="/" className="text-sm font-medium text-[var(--color-charcoal-txt)] hover:text-[var(--color-accent-blue)] transition-colors">
                Browse Listings
              </Link>
              <Link to="/login" className="text-sm font-medium text-[var(--color-charcoal-txt)] hover:text-[var(--color-accent-blue)] transition-colors">
                Sign In
              </Link>
            </nav>
            
            <div className="flex md:hidden">
              <Link to="/login" className="btn btn-primary text-sm">
                Sign In
              </Link>
            </div>
          </div>
        </div>
      </header>

      <main>
        <Outlet />
      </main>
      
      <footer className="bg-white border-t border-[var(--color-taupe-border)] py-12 mt-20">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <p className="text-[var(--color-taupe-txt)] text-sm">
            &copy; {new Date().getFullYear()} PropQuery Marketplace. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
}
