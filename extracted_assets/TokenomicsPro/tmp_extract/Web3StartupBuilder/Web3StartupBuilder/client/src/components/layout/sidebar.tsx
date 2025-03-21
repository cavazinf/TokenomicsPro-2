import { Link, useLocation } from "wouter";
import { cn } from "@/lib/utils";

interface NavLinkProps {
  href: string;
  icon: React.ReactNode;
  children: React.ReactNode;
  isActive?: boolean;
}

const NavLink: React.FC<NavLinkProps> = ({ href, icon, children, isActive }) => {
  return (
    <div className="w-full">
      <Link href={href}>
        <div
          className={cn(
            "flex items-center gap-3 px-3 py-2 rounded-lg transition-colors cursor-pointer",
            isActive
              ? "bg-sidebar-accent text-sidebar-foreground"
              : "text-sidebar-foreground opacity-70 hover:bg-sidebar-accent hover:opacity-100"
          )}
        >
          {icon}
          <span>{children}</span>
        </div>
      </Link>
    </div>
  );
};

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ isOpen, onClose }) => {
  const [location] = useLocation();

  const isActive = (path: string) => {
    return location === path;
  };

  return (
    <>
      {/* Mobile sidebar backdrop */}
      {isOpen && (
        <div 
          className="md:hidden fixed inset-0 bg-background/80 backdrop-blur-sm z-30"
          onClick={onClose}
        ></div>
      )}

      {/* Sidebar */}
      <aside 
        className={cn(
          "flex flex-col w-64 bg-sidebar p-4 shrink-0 z-40 text-sidebar-foreground",
          "md:static md:flex",
          isOpen ? "fixed inset-y-0 left-0" : "hidden"
        )}
      >
        <div className="flex items-center gap-3 mb-8 pl-2">
          <div className="h-8 w-8 rounded-lg bg-primary flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-5 w-5 text-white">
              <path d="M20.24 12.24a6 6 0 0 0-8.49-8.49L5 10.5V19h8.5l6.74-6.76z"></path>
              <line x1="16" y1="8" x2="2" y2="22"></line>
              <line x1="17.5" y1="15" x2="9" y2="15"></line>
            </svg>
          </div>
          <span className="text-lg font-semibold">TokenomicsLab</span>

          {/* Close button for mobile */}
          <button 
            className="md:hidden ml-auto p-1 rounded-lg hover:bg-sidebar-accent"
            onClick={onClose}
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-5 w-5 text-sidebar-foreground">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        
        <nav className="flex-1 space-y-2">
          <div className="px-2 py-2 text-sidebar-foreground/60 text-xs uppercase tracking-wider">Main</div>
          <NavLink 
            href="/" 
            isActive={isActive("/")}
            icon={
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-5 w-5">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                <line x1="3" y1="9" x2="21" y2="9"></line>
                <line x1="9" y1="21" x2="9" y2="9"></line>
              </svg>
            }
          >
            Dashboard
          </NavLink>
          <NavLink 
            href="/projects" 
            isActive={isActive("/projects")}
            icon={
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-5 w-5">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
              </svg>
            }
          >
            My Projects
          </NavLink>
          
          <div className="px-2 py-2 mt-6 text-sidebar-foreground/60 text-xs uppercase tracking-wider">Tokenomics</div>
          <NavLink 
            href="/token-designer" 
            isActive={isActive("/token-designer")}
            icon={
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-5 w-5">
                <circle cx="12" cy="12" r="10"></circle>
                <path d="M12 6v6l4 2"></path>
              </svg>
            }
          >
            Token Designer
          </NavLink>
          <NavLink 
            href="/distribution-planner" 
            isActive={isActive("/distribution-planner")}
            icon={
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-5 w-5">
                <line x1="18" y1="20" x2="18" y2="10"></line>
                <line x1="12" y1="20" x2="12" y2="4"></line>
                <line x1="6" y1="20" x2="6" y2="14"></line>
              </svg>
            }
          >
            Distribution Planner
          </NavLink>
          <NavLink 
            href="/economic-simulator" 
            isActive={isActive("/economic-simulator")}
            icon={
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-5 w-5">
                <path d="M2 12h5l2 3h6l2-6h5"></path>
              </svg>
            }
          >
            Economic Simulator
          </NavLink>
          
          <div className="px-2 py-2 mt-6 text-sidebar-foreground/60 text-xs uppercase tracking-wider">Resources</div>
          <NavLink 
            href="/learning-hub" 
            isActive={isActive("/learning-hub")}
            icon={
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-5 w-5">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
              </svg>
            }
          >
            Learning Hub
          </NavLink>
          <NavLink 
            href="/best-practices" 
            isActive={isActive("/best-practices")}
            icon={
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-5 w-5">
                <circle cx="12" cy="12" r="4"></circle>
                <path d="M12 20v-2"></path>
                <path d="M4.9 4.9l1.4 1.4"></path>
                <path d="M2 12h2"></path>
                <path d="M20 12h2"></path>
                <path d="M17.7 6.3l-1.4 1.4"></path>
                <path d="M12 2v2"></path>
              </svg>
            }
          >
            Best Practices
          </NavLink>
        </nav>
        
        <div className="mt-auto pt-6">
          <div className="flex items-center gap-3 px-3 py-2">
            <div className="h-8 w-8 rounded-full bg-sidebar-primary flex items-center justify-center text-sidebar-primary-foreground font-medium">JS</div>
            <div>
              <div className="text-sm font-medium text-sidebar-foreground">John Smith</div>
              <div className="text-xs text-sidebar-foreground/60">Free Plan</div>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
};
