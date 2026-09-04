import { NavLink } from "react-router-dom";
import { LayoutDashboard, Building2, Users, Receipt, Wrench, LifeBuoy, LineChart } from "lucide-react";

export default function Sidebar() {
  const navItems = [
    { name: "Dashboard", path: "/", icon: LayoutDashboard },
    { name: "Properties", path: "/properties", icon: Building2 },
    { name: "Units & Tenants", path: "/tenants", icon: Users },
    { name: "Payments", path: "/payments", icon: Receipt },
    { name: "Maintenance", path: "/maintenance", icon: Wrench },
    { name: "Support", path: "/support", icon: LifeBuoy },
    { name: "Reports", path: "/reports", icon: LineChart },
  ];

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
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-[#D6D3D1] flex items-center justify-center text-sm font-bold text-[var(--color-charcoal-txt)]">
            JD
          </div>
          <div className="text-sm">
            <p className="font-medium">Jane Doe</p>
            <p className="text-xs text-[var(--color-taupe-txt)]">System Admin</p>
          </div>
        </div>
      </div>
    </div>
  );
}
