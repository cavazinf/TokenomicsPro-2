import React from 'react';
import { Link, useLocation } from 'wouter';
import { cn } from '@/lib/utils';
import { useIsMobile } from '@/hooks/use-mobile';
import { Button } from '@/components/ui/button';
import {
  LayoutDashboard,
  Coins,
  BarChart3,
  Calendar,
  TrendingUp,
  FileText,
  Settings,
  Menu,
  X,
  LogOut,
} from 'lucide-react';

interface SidebarItemProps {
  href: string;
  icon: React.ReactNode;
  children: React.ReactNode;
  active?: boolean;
  onClick?: () => void;
}

const SidebarItem: React.FC<SidebarItemProps> = ({
  href,
  icon,
  children,
  active,
  onClick,
}) => {
  return (
    <Link href={href}>
      <div
        className={cn(
          'flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-all hover:text-primary cursor-pointer',
          active ? 'bg-secondary text-primary' : 'text-muted-foreground'
        )}
        onClick={onClick}
      >
        {icon}
        <span>{children}</span>
      </div>
    </Link>
  );
};

interface AppLayoutProps {
  children: React.ReactNode;
}

const AppLayout: React.FC<AppLayoutProps> = ({ children }) => {
  const [location] = useLocation();
  const isMobile = useIsMobile();
  const [sidebarOpen, setSidebarOpen] = React.useState(false);

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  const closeSidebar = () => {
    if (isMobile) {
      setSidebarOpen(false);
    }
  };

  const menuItems = [
    {
      href: '/',
      icon: <LayoutDashboard className="h-4 w-4" />,
      label: 'Dashboard',
    },
    {
      href: '/token-supply-distribution',
      icon: <Coins className="h-4 w-4" />,
      label: 'Token Distribution',
    },
    {
      href: '/token-design',
      icon: <Settings className="h-4 w-4" />,
      label: 'Token Design',
    },
    {
      href: '/economic-simulation',
      icon: <BarChart3 className="h-4 w-4" />,
      label: 'Economic Simulation',
    },
    {
      href: '/vesting-schedule',
      icon: <Calendar className="h-4 w-4" />,
      label: 'Vesting Schedule',
    },
    {
      href: '/price-market-cap',
      icon: <TrendingUp className="h-4 w-4" />,
      label: 'Price & Market Cap',
    },
    {
      href: '/econometrics',
      icon: <BarChart3 className="h-4 w-4" />,
      label: 'Econometrics',
    },
    {
      href: '/tokenization-models',
      icon: <FileText className="h-4 w-4" />,
      label: 'Tokenization Models',
    },
    {
      href: '/business-model',
      icon: <LayoutDashboard className="h-4 w-4" />,
      label: 'Business Model',
    },
    {
      href: '/market-analysis',
      icon: <BarChart3 className="h-4 w-4" />,
      label: 'Market Analysis',
    },
    {
      href: '/marketing-growth',
      icon: <TrendingUp className="h-4 w-4" />,
      label: 'Marketing & Growth',
    },
    {
      href: '/market-stress-test',
      icon: <BarChart3 className="h-4 w-4" />,
      label: 'Market Stress Test',
    },
    {
      href: '/crypto-trading',
      icon: <Coins className="h-4 w-4" />,
      label: 'Crypto Trading',
    },
  ];

  return (
    <div className="flex h-screen overflow-hidden">
      {/* Sidebar para mobile com overlay quando aberta */}
      {isMobile && sidebarOpen && (
        <div 
          className="fixed inset-0 z-40 bg-background/80 backdrop-blur-sm"
          onClick={closeSidebar}
        />
      )}
      
      {/* Sidebar */}
      <aside
        className={cn(
          'fixed inset-y-0 left-0 z-50 flex w-64 flex-col border-r bg-background transition-transform duration-300 ease-in-out',
          isMobile ? (sidebarOpen ? 'translate-x-0' : '-translate-x-full') : 'translate-x-0'
        )}
      >
        <div className="flex h-14 items-center border-b px-4">
          <div className="flex items-center gap-2">
            <div className="h-6 w-6 rounded-full bg-primary" />
            <span className="text-lg font-semibold">TokenomicsPro</span>
          </div>
          {isMobile && (
            <Button
              variant="ghost"
              size="icon"
              className="ml-auto"
              onClick={toggleSidebar}
            >
              <X className="h-4 w-4" />
            </Button>
          )}
        </div>
        <nav className="flex-1 overflow-auto p-3">
          <div className="space-y-1">
            {menuItems.map((item) => (
              <SidebarItem
                key={item.href}
                href={item.href}
                icon={item.icon}
                active={location === item.href}
                onClick={closeSidebar}
              >
                {item.label}
              </SidebarItem>
            ))}
          </div>

          <div className="mt-6 space-y-1">
            <div className="px-3 text-xs font-medium text-muted-foreground">
              Resources
            </div>
            <SidebarItem
              href="/resources"
              icon={<FileText className="h-4 w-4" />}
              onClick={closeSidebar}
            >
              Resource Library
            </SidebarItem>
            <SidebarItem
              href="/settings"
              icon={<Settings className="h-4 w-4" />}
              onClick={closeSidebar}
            >
              Settings
            </SidebarItem>
          </div>
        </nav>
        <div className="border-t p-3">
          <Button variant="outline" className="w-full justify-start gap-2">
            <LogOut className="h-4 w-4" />
            <span>Logout</span>
          </Button>
        </div>
      </aside>
      
      {/* Main content */}
      <div className={cn(
        'flex flex-1 flex-col transition-all duration-300 ease-in-out',
        isMobile ? 'ml-0' : 'ml-64'
      )}>
        {/* Header */}
        <header className="flex h-14 items-center border-b px-4">
          {isMobile && (
            <Button
              variant="ghost"
              size="icon"
              onClick={toggleSidebar}
            >
              <Menu className="h-4 w-4" />
            </Button>
          )}
          <div className="ml-auto flex items-center gap-4">
            <div className="flex items-center gap-2">
              <div className="h-8 w-8 rounded-full bg-muted flex items-center justify-center">
                <span className="text-xs font-medium">JD</span>
              </div>
            </div>
          </div>
        </header>
        
        {/* Main content area */}
        <main className="flex-1 overflow-auto">
          {children}
        </main>
      </div>
    </div>
  );
};

export default AppLayout;