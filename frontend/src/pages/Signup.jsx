import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import Card from "../components/ui/Card";

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
      navigate("/");
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
    <div className="min-h-screen flex items-center justify-center bg-[var(--color-beige-bg)] px-4 py-8">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold tracking-tight text-[var(--color-charcoal-txt)]">PropQuery</h1>
          <p className="text-sm text-[var(--color-taupe-txt)] mt-2">Create a new account</p>
        </div>

        <Card>
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="bg-rose-50 text-rose-700 p-3 rounded-md text-sm border border-rose-100">
                {error}
              </div>
            )}
            
            <div>
              <label className="block text-sm font-medium text-[var(--color-charcoal-txt)] mb-1">Full Name</label>
              <input 
                type="text" 
                required 
                className="input w-full" 
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-[var(--color-charcoal-txt)] mb-1">Email</label>
              <input 
                type="email" 
                required 
                className="input w-full" 
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-[var(--color-charcoal-txt)] mb-1">Password</label>
              <div className="relative">
                <input 
                  type={showPassword ? "text" : "password"} 
                  required 
                  className="input w-full pr-14" 
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
                <button
                  type="button"
                  className="absolute inset-y-0 right-0 pr-3 flex items-center text-xs font-medium text-[var(--color-taupe-txt)] hover:text-[var(--color-charcoal-txt)]"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? "Hide" : "Show"}
                </button>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-[var(--color-charcoal-txt)] mb-1">Role</label>
              <select 
                className="input w-full"
                value={role}
                onChange={(e) => setRole(e.target.value)}
              >
                <option value="tenant">Tenant</option>
                <option value="owner">Property Owner</option>
                <option value="admin">Admin</option>
              </select>
            </div>

            <button 
              type="submit" 
              disabled={loading}
              className="btn btn-primary w-full mt-4 h-10"
            >
              {loading ? "Creating Account..." : "Create Account"}
            </button>

            <div className="mt-4 text-center text-sm pt-2">
              <span className="text-[var(--color-taupe-txt)]">Already have an account? </span>
              <Link to="/login" className="text-[var(--color-primary)] hover:underline font-medium">Sign in</Link>
            </div>
          </form>
        </Card>
      </div>
    </div>
  );
}
