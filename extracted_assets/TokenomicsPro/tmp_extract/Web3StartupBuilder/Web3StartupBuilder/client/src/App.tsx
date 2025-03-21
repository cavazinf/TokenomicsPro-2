import { Switch, Route } from "wouter";
import { Toaster } from "@/components/ui/toaster";
import NotFound from "@/pages/not-found";
import Dashboard from "@/pages/dashboard";
import TokenDesigner from "@/pages/token-designer";
import DistributionPlanner from "@/pages/distribution-planner";
import EconomicSimulator from "@/pages/economic-simulator";
import LearningHub from "@/pages/learning-hub";
import { Sidebar } from "@/components/layout/sidebar";
import { useState } from "react";

function App() {
  // State to control mobile sidebar visibility
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  return (
    <div className="flex min-h-screen bg-light-200">
      <Sidebar isOpen={isSidebarOpen} onClose={() => setIsSidebarOpen(false)} />
      
      <div className="flex flex-col flex-1">
        {/* Mobile header */}
        <div className="md:hidden flex items-center justify-between p-4 bg-white border-b border-light-300 w-full">
          <div className="flex items-center gap-3">
            <div className="h-8 w-8 rounded-lg bg-primary flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-5 w-5 text-white">
                <path d="M20.24 12.24a6 6 0 0 0-8.49-8.49L5 10.5V19h8.5l6.74-6.76z"></path>
                <line x1="16" y1="8" x2="2" y2="22"></line>
                <line x1="17.5" y1="15" x2="9" y2="15"></line>
              </svg>
            </div>
            <span className="text-lg font-semibold">TokenomicsLab</span>
          </div>
          
          <button 
            className="p-2 rounded-lg hover:bg-light-200"
            onClick={() => setIsSidebarOpen(true)}
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-6 w-6">
              <line x1="3" y1="12" x2="21" y2="12"></line>
              <line x1="3" y1="6" x2="21" y2="6"></line>
              <line x1="3" y1="18" x2="21" y2="18"></line>
            </svg>
          </button>
        </div>
        
        <main className="flex-1 p-4 md:p-8 overflow-auto">
          <Switch>
            <Route path="/" component={Dashboard} />
            <Route path="/token-designer" component={TokenDesigner} />
            <Route path="/distribution-planner" component={DistributionPlanner} />
            <Route path="/economic-simulator" component={EconomicSimulator} />
            <Route path="/learning-hub" component={LearningHub} />
            <Route component={NotFound} />
          </Switch>
        </main>
      </div>
      
      <Toaster />
    </div>
  );
}

export default App;
