import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Signup() {
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("tenant");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { signup } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await signup(email, password, fullName, role);
      navigate("/dashboard");
    } catch (err) {
      if (err.response && err.response.data && err.response.data.detail) {
        if (typeof err.response.data.detail === 'string') {
          setError(err.response.data.detail);
        } else {
          setError(JSON.stringify(err.response.data.detail));
        }
      } else {
        setError("An error occurred during signup.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex">
      {/* Left side: Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center bg-[var(--color-beige-bg)] px-4 sm:px-6 lg:px-8 py-12 lg:py-0 overflow-y-auto">
        <div className="w-full max-w-md">
          <div className="text-center lg:text-left mb-10">
            <h1 className="text-3xl font-bold tracking-tight text-[var(--color-charcoal-txt)] mb-2">Create an account</h1>
            <p className="text-[var(--color-taupe-txt)]">Join PropQuery to manage your properties or find your next home.</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-5">
            {error && (
              <div className="bg-rose-50 text-rose-700 p-4 rounded-xl text-sm border border-rose-100 flex items-center">
                <svg className="w-5 h-5 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd"></path></svg>
                {error}
              </div>
            )}
            
            <div>
              <label className="block text-sm font-semibold text-[var(--color-charcoal-txt)] mb-2">Full Name</label>
              <input 
                type="text" 
                required 
                className="w-full px-4 py-3 rounded-xl border border-[var(--color-taupe-border)] focus:ring-2 focus:ring-[var(--color-accent-blue)] focus:border-transparent transition-all outline-none" 
                placeholder="John Doe"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-[var(--color-charcoal-txt)] mb-2">Email address</label>
              <input 
                type="email" 
                required 
                className="w-full px-4 py-3 rounded-xl border border-[var(--color-taupe-border)] focus:ring-2 focus:ring-[var(--color-accent-blue)] focus:border-transparent transition-all outline-none" 
                placeholder="name@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            
            <div>
              <label className="block text-sm font-semibold text-[var(--color-charcoal-txt)] mb-2">Password</label>
              <div className="relative">
                <input 
                  type={showPassword ? "text" : "password"} 
                  required 
                  className="w-full px-4 py-3 rounded-xl border border-[var(--color-taupe-border)] focus:ring-2 focus:ring-[var(--color-accent-blue)] focus:border-transparent transition-all outline-none pr-14" 
                  placeholder="Create a strong password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
                <button
                  type="button"
                  className="absolute inset-y-0 right-0 pr-4 flex items-center text-sm font-medium text-[var(--color-taupe-txt)] hover:text-[var(--color-charcoal-txt)] transition-colors"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? "Hide" : "Show"}
                </button>
              </div>
            </div>

            <div>
              <label className="block text-sm font-semibold text-[var(--color-charcoal-txt)] mb-2">I am a...</label>
              <select 
                className="w-full px-4 py-3 rounded-xl border border-[var(--color-taupe-border)] focus:ring-2 focus:ring-[var(--color-accent-blue)] focus:border-transparent transition-all outline-none bg-white"
                value={role}
                onChange={(e) => setRole(e.target.value)}
              >
                <option value="tenant">Prospective Tenant</option>
                <option value="owner">Property Owner / Landlord</option>
                <option value="admin">Platform Admin</option>
              </select>
            </div>
            
            <button 
              type="submit" 
              disabled={loading}
              className="w-full bg-[var(--color-charcoal-txt)] text-white font-semibold py-3 px-4 rounded-xl hover:bg-black focus:ring-4 focus:ring-gray-300 transition-all disabled:opacity-70 disabled:cursor-not-allowed mt-4"
            >
              {loading ? "Creating account..." : "Sign up"}
            </button>
            
            <div className="text-center mt-6">
              <span className="text-[var(--color-taupe-txt)]">Already have an account? </span>
              <Link to="/login" className="text-[var(--color-charcoal-txt)] font-semibold hover:underline">Log in</Link>
            </div>
          </form>
        </div>
      </div>

      {/* Right side: Image */}
      <div className="hidden lg:flex lg:w-1/2 relative bg-gray-900">
        <img 
          src="/images/auth-bg.png" 
          alt="Luxury apartment interior" 
          className="absolute inset-0 w-full h-full object-cover opacity-90 scale-x-[-1]"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent"></div>
        <div className="absolute bottom-12 right-12 left-12 text-white text-right">
          <Link to="/" className="text-2xl font-bold tracking-tight mb-4 block">PropQuery</Link>
          <p className="text-lg text-gray-200 font-light ml-auto max-w-md">
            Join thousands of property owners and tenants experiencing the future of real estate management.
          </p>
        </div>
      </div>
    </div>
  );
}
