import { useState } from "react";
import { Search, Menu, Bell, PlusCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ThemeToggle } from "@/components/ui/theme-toggle";
import { useAuth } from "@/hooks/use-auth";
import { useLocation } from "wouter";

type NavbarProps = {
  toggleSidebar: () => void;
};

export default function Navbar({ toggleSidebar }: NavbarProps) {
  const { user } = useAuth();
  const [location] = useLocation();
  const [searchQuery, setSearchQuery] = useState("");

  const getPageTitle = (path: string): string => {
    if (path === "/") return "Dashboard";
    if (path === "/projects") return "Projects";
    if (path === "/profile") return "Profile";
    if (path === "/token-designer") return "Token Designer";
    if (path === "/economic-models") return "Economic Models";
    if (path === "/distribution-plans") return "Distribution Plans";
    if (path === "/vesting-schedules") return "Vesting Schedules";
    if (path === "/startup-planner") return "Startup Planner";
    if (path === "/business-models") return "Business Models";
    if (path === "/project-roadmap") return "Project Roadmap";
    if (path === "/team-builder") return "Team Builder";
    if (path === "/learning-center") return "Learning Center";
    if (path === "/help") return "Help & Support";
    return "TokenomicsPro";
  };

  return (
    <header className="bg-surface border-b border-gray-700 z-10">
      <div className="flex items-center justify-between p-4">
        <div className="flex items-center">
          <Button
            onClick={toggleSidebar}
            variant="ghost"
            className="p-1 mr-4 rounded-md text-gray-400 focus:outline-none hover:bg-surface-light hover:text-white md:hidden"
          >
            <Menu className="h-6 w-6" />
          </Button>
          <h2 className="text-xl font-semibold">{getPageTitle(location)}</h2>
        </div>

        <div className="flex items-center space-x-4">
          <div className="relative hidden md:block">
            <Input
              type="text"
              placeholder="Search..."
              className="w-64 bg-background text-white border-gray-700 focus:border-primary"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <Search className="absolute right-3 top-2.5 h-4 w-4 text-gray-400" />
          </div>

          <ThemeToggle />

          <Button variant="ghost" size="icon" className="text-gray-300 hover:text-white">
            <Bell className="h-5 w-5" />
          </Button>

          <Button className="hidden md:flex items-center bg-primary hover:bg-primary/90">
            <PlusCircle className="h-4 w-4 mr-2" />
            New Project
          </Button>
        </div>
      </div>
    </header>
  );
}
