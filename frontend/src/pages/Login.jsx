import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import Card from "../components/ui/Card";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
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
      navigate("/");
    } catch (err) {
      setError("Invalid email or password.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[var(--color-beige-bg)] px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold tracking-tight text-[var(--color-charcoal-txt)]">PropQuery</h1>
          <p className="text-sm text-[var(--color-taupe-txt)] mt-2">Sign in to your account</p>
        </div>

        <Card>
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="bg-rose-50 text-rose-700 p-3 rounded-md text-sm border border-rose-100">
                {error}
              </div>
            )}
            <div>
              <label className="block text-sm font-medium text-[var(--color-charcoal-txt)] mb-1">Email</label>
              <input 
                type="email" 
                required 
                className="input" 
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-[var(--color-charcoal-txt)] mb-1">Password</label>
              <input 
                type="password" 
                required 
                className="input" 
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            <button 
              type="submit" 
              disabled={loading}
              className="btn btn-primary w-full mt-4 h-10"
            >
              {loading ? "Signing in..." : "Sign In"}
            </button>
          </form>
        </Card>
      </div>
    </div>
  );
}
