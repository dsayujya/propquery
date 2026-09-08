import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./components/layout/ProtectedRoute";
import MainLayout from "./components/layout/MainLayout";
import PublicLayout from "./components/layout/PublicLayout";

// Public Pages
import Listings from "./pages/Listings";
import ListingDetail from "./pages/ListingDetail";
import Login from "./pages/Login";
import Signup from "./pages/Signup";

// Protected Pages
import Dashboard from "./pages/Dashboard";
import Properties from "./pages/Properties";
import Tenants from "./pages/Tenants";
import Support from "./pages/Support";

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public Marketplace Routes */}
          <Route element={<PublicLayout />}>
            <Route path="/" element={<Listings />} />
            <Route path="/listings/:id" element={<ListingDetail />} />
          </Route>

          {/* Auth Routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          
          {/* Protected Dashboard Routes */}
          <Route element={<ProtectedRoute />}>
            <Route path="/dashboard" element={<MainLayout />}>
              <Route index element={<Dashboard />} />
              <Route path="properties" element={<Properties />} />
              <Route path="tenants" element={<Tenants />} />
              <Route path="payments" element={<div className="card p-6">Payments Page</div>} />
              <Route path="maintenance" element={<div className="card p-6">Maintenance Page</div>} />
              <Route path="support" element={<Support />} />
              <Route path="reports" element={<div className="card p-6">Reports Page</div>} />
            </Route>
          </Route>
          
          {/* Redirect /admin to /dashboard just in case */}
          <Route path="/admin" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
