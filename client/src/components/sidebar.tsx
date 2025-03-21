import { useAuth } from "@/hooks/use-auth";
import { Link, useLocation } from "wouter";
import { cn } from "@/lib/utils";
import { 
  BarChart, 
  FileText, 
  User, 
  Coins, 
  BarChartHorizontal, 
  PieChart, 
  CalendarCheck, 
  Building, 
  Layout, 
  Map, 
  Users, 
  BookOpen, 
  HelpCircle, 
  Settings, 
  LogOut,
  Landmark
} from "lucide-react";

type SidebarSection = {
  title: string;
  items: {
    name: string;
    icon: React.ReactNode;
    path: string;
  }[];
};

export default function Sidebar({ isOpen, toggle }: { isOpen: boolean; toggle: () => void }) {
  const { user, logoutMutation } = useAuth();
  const [location] = useLocation();

  const sections: SidebarSection[] = [
    {
      title: "Dashboard",
      items: [
        { name: "Overview", icon: <BarChart className="h-5 w-5" />, path: "/" },
        { name: "Projects", icon: <FileText className="h-5 w-5" />, path: "/projects" },
        { name: "Profile", icon: <User className="h-5 w-5" />, path: "/profile" },
      ],
    },
    {
      title: "TokenomicsLabs",
      items: [
        { name: "Token Designer", icon: <Coins className="h-5 w-5" />, path: "/token-designer" },
        { name: "Economic Models", icon: <BarChartHorizontal className="h-5 w-5" />, path: "/economic-models" },
        { name: "Distribution Plans", icon: <PieChart className="h-5 w-5" />, path: "/distribution-plans" },
        { name: "Vesting Schedules", icon: <CalendarCheck className="h-5 w-5" />, path: "/vesting-schedules" },
      ],
    },
    {
      title: "Web3StartupBuild",
      items: [
        { name: "Startup Planner", icon: <Building className="h-5 w-5" />, path: "/startup-planner" },
        { name: "Business Models", icon: <Layout className="h-5 w-5" />, path: "/business-models" },
        { name: "Project Roadmap", icon: <Map className="h-5 w-5" />, path: "/project-roadmap" },
        { name: "Team Builder", icon: <Users className="h-5 w-5" />, path: "/team-builder" },
      ],
    },
    {
      title: "Resources",
      items: [
        { name: "Learning Center", icon: <BookOpen className="h-5 w-5" />, path: "/learning-center" },
        { name: "Help & Support", icon: <HelpCircle className="h-5 w-5" />, path: "/help" },
      ],
    },
  ];

  const handleLogout = () => {
    logoutMutation.mutate();
  };

  return (
    <aside
      className={cn(
        "fixed z-30 w-64 h-full bg-surface border-r border-gray-700 transition-transform duration-300 ease-in-out",
        isOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0"
      )}
    >
      <div className="flex flex-col h-full">
        {/* Logo */}
        <div className="p-4 border-b border-gray-700">
          <div className="flex items-center">
            <div className="h-8 w-8 rounded-md bg-gradient-to-br from-primary to-secondary flex items-center justify-center mr-3">
              <Landmark className="h-5 w-5 text-white" />
            </div>
            <h1 className="text-xl font-bold text-white">TokenomicsPro</h1>
          </div>
        </div>

        {/* User Profile */}
        {user && (
          <div className="p-4 border-b border-gray-700">
            <div className="flex items-center space-x-3">
              <div className="h-10 w-10 rounded-full bg-surface-light flex items-center justify-center">
                <User className="h-5 w-5 text-gray-300" />
              </div>
              <div>
                <p className="text-sm font-medium text-white">{user.name || user.username}</p>
                <p className="text-xs text-gray-400">{user.email || 'No email set'}</p>
              </div>
            </div>
          </div>
        )}

        {/* Navigation */}
        <nav className="px-4 py-2 overflow-y-auto flex-1">
          {sections.map((section) => (
            <div key={section.title} className="space-y-1">
              <p className="px-2 pt-4 pb-2 text-xs font-semibold text-gray-400 uppercase tracking-wider">
                {section.title}
              </p>
              {section.items.map((item) => (
                <Link
                  key={item.name}
                  href={item.path}
                  className={cn(
                    "flex items-center px-2 py-2 text-sm font-medium rounded-md group",
                    location === item.path 
                      ? "text-white bg-surface-light" 
                      : "text-gray-300 hover:bg-surface-light hover:text-white transition duration-150"
                  )}
                >
                  {item.icon}
                  <span className="ml-3">{item.name}</span>
                </Link>
              ))}
            </div>
          ))}
        </nav>

        {/* Sidebar Footer */}
        <div className="p-4 border-t border-gray-700">
          <Link
            href="/settings"
            className="flex items-center px-2 py-2 text-sm font-medium rounded-md text-gray-300 hover:bg-surface-light hover:text-white transition duration-150 group"
          >
            <Settings className="h-5 w-5 mr-3" />
            Settings
          </Link>
          <button
            onClick={handleLogout}
            disabled={logoutMutation.isPending}
            className="flex items-center px-2 py-2 text-sm font-medium rounded-md text-gray-300 hover:bg-surface-light hover:text-white transition duration-150 group w-full text-left"
          >
            <LogOut className="h-5 w-5 mr-3" />
            {logoutMutation.isPending ? "Logging out..." : "Logout"}
          </button>
        </div>
      </div>
    </aside>
  );
}
