import { NavLink, useNavigate } from "react-router-dom";
import { LayoutDashboard, Building2, Users, Receipt, Wrench, LifeBuoy, LineChart, LogOut } from "lucide-react";
import { useAuth } from "../../context/AuthContext";

export default function Sidebar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const getInitials = (name) => {
    if (!name) return "U";
    return name.split(" ").map(n => n[0]).join("").toUpperCase().substring(0, 2);
  };

  const role = user?.role || "tenant";
  
  const allNavItems = [
    { name: "Dashboard", path: "/dashboard", icon: LayoutDashboard, roles: ["admin", "owner", "tenant"] },
    { name: "Properties", path: "/dashboard/properties", icon: Building2, roles: ["admin", "owner"] },
    { name: "Units & Tenants", path: "/dashboard/tenants", icon: Users, roles: ["admin", "owner"] },
    { name: "Payments", path: "/dashboard/payments", icon: Receipt, roles: ["admin", "tenant"] },
    { name: "Maintenance", path: "/dashboard/maintenance", icon: Wrench, roles: ["admin", "owner", "tenant"] },
    { name: "Support", path: "/dashboard/support", icon: LifeBuoy, roles: ["admin", "tenant"] },
    { name: "Reports", path: "/dashboard/reports", icon: LineChart, roles: ["admin", "owner"] },
  ];

  const navItems = allNavItems.filter(item => item.roles.includes(role));

  return (
    <div className="w-64 bg-[var(--color-beige-bg)] border-r border-[var(--color-taupe-border)] h-screen flex flex-col">
      <div className="p-6">
        <h1 className="text-xl font-bold tracking-tight text-[var(--color-charcoal-txt)]">
          PropQuery
        </h1>
        <p className="text-xs text-[var(--color-taupe-txt)] mt-1">Property Management</p>
      </div>

      <nav className="flex-1 px-4 space-y-1">
        {navItems.map((item) => (
          <NavLink
            key={item.name}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-md transition-colors ${
                isActive
                  ? "bg-[var(--color-accent-blue)] text-white"
                  : "text-[var(--color-charcoal-txt)] hover:bg-[#E7E5E4]"
              }`
            }
          >
            <item.icon size={18} />
            {item.name}
          </NavLink>
        ))}
      </nav>

      <div className="p-4 border-t border-[var(--color-taupe-border)]">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-full bg-[#D6D3D1] flex items-center justify-center text-sm font-bold text-[var(--color-charcoal-txt)]">
              {getInitials(user?.full_name)}
            </div>
            <div className="text-sm">
              <p className="font-medium truncate max-w-[100px]">{user?.full_name || "User"}</p>
              <p className="text-xs text-[var(--color-taupe-txt)] capitalize">{role}</p>
            </div>
          </div>
          <button 
            onClick={handleLogout}
            className="p-2 text-[var(--color-taupe-txt)] hover:text-rose-600 transition-colors"
            title="Log out"
          >
            <LogOut size={18} />
          </button>
        </div>
      </div>
    </div>
  );
}
