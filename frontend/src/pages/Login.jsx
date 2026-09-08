import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(email, password);
      navigate("/dashboard");
    } catch (err) {
      setError("Invalid email or password.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex">
      {/* Left side: Image */}
      <div className="hidden lg:flex lg:w-1/2 relative bg-gray-900">
        <img 
          src="/images/auth-bg.png" 
          alt="Luxury apartment interior" 
          className="absolute inset-0 w-full h-full object-cover opacity-90"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent"></div>
        <div className="absolute bottom-12 left-12 right-12 text-white">
          <Link to="/" className="text-2xl font-bold tracking-tight mb-4 block">PropQuery</Link>
          <p className="text-lg text-gray-200 font-light max-w-md">
            Streamline your property management. Discover the most elegant way to manage your real estate portfolio in India.
          </p>
        </div>
      </div>

      {/* Right side: Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center bg-[var(--color-beige-bg)] px-4 sm:px-6 lg:px-8">
        <div className="w-full max-w-md">
          <div className="text-center lg:text-left mb-10">
            <h1 className="text-3xl font-bold tracking-tight text-[var(--color-charcoal-txt)] mb-2">Welcome back</h1>
            <p className="text-[var(--color-taupe-txt)]">Please enter your details to sign in.</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            {error && (
              <div className="bg-rose-50 text-rose-700 p-4 rounded-xl text-sm border border-rose-100 flex items-center">
                <svg className="w-5 h-5 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd"></path></svg>
                {error}
              </div>
            )}
            
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
                  placeholder="••••••••"
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
            
            <button 
              type="submit" 
              disabled={loading}
              className="w-full bg-[var(--color-accent-blue)] text-white font-semibold py-3 px-4 rounded-xl hover:bg-blue-700 focus:ring-4 focus:ring-blue-200 transition-all disabled:opacity-70 disabled:cursor-not-allowed mt-2"
            >
              {loading ? "Signing in..." : "Sign in"}
            </button>
            
            <div className="text-center mt-6">
              <span className="text-[var(--color-taupe-txt)]">Don't have an account? </span>
              <Link to="/signup" className="text-[var(--color-accent-blue)] font-semibold hover:underline">Sign up</Link>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
