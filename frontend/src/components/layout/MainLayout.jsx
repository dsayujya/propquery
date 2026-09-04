import { Outlet, useLocation } from "react-router-dom";
import Sidebar from "./Sidebar";
import Topbar from "./Topbar";

export default function MainLayout() {
  const location = useLocation();
  
  // Simple mapping to get title from path
  const getPageTitle = () => {
    const path = location.pathname;
    if (path === "/") return "Dashboard";
    const name = path.split("/")[1];
    if (!name) return "Dashboard";
    return name.charAt(0).toUpperCase() + name.slice(1);
  };

  return (
    <div className="flex h-screen overflow-hidden bg-[var(--color-beige-bg)]">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Topbar title={getPageTitle()} />
        <main className="flex-1 overflow-y-auto p-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
