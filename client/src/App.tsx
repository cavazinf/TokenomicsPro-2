import { Switch, Route } from "wouter";
import { queryClient } from "./lib/queryClient";
import { QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "@/components/ui/toaster";
import { AuthProvider } from "@/hooks/use-auth";
import { ProtectedRoute } from "./lib/protected-route";
import NotFound from "@/pages/not-found";
import HomePage from "@/pages/home-page";
import AuthPage from "@/pages/auth-page";
import ProjectsPage from "@/pages/projects-page";
import TokenDesignerPage from "@/pages/token-designer-page";
import EconomicModelsPage from "@/pages/economic-models-page";
import DistributionPlansPage from "@/pages/distribution-plans-page";
import Dashboard from "@/pages/dashboard"; // Added
import TokenDesign from "@/pages/token-design"; // Added
import EconometricsPage from "@/pages/econometrics"; // Added
import TokenizationModelsPage from "@/pages/tokenization-models"; // Added
import BusinessModelPage from "@/pages/business-model"; // Added
import MarketAnalysisPage from "@/pages/market-analysis"; // Added
import MarketingGrowthPage from "@/pages/marketing-growth"; // Added
import MarketValuationPage from "@/pages/market-valuation"; // Added
import MarketStressTestPage from "@/pages/market-stress-test"; // Added
import CryptoTradingPage from "@/pages/crypto-trading"; // Added
import MarketResearchPage from "@/pages/market-research"; // Added
import ValuationPage from "@/pages/valuation"; // Added
import EconomicEngineeringPage from "@/pages/economic-engineering"; // Added
import ReportsPage from "@/pages/reports"; // Added
import CommunityPage from "@/pages/community"; // Added


function Router() {
  return (
    <Switch>
      <ProtectedRoute path="/" component={HomePage} />
      <ProtectedRoute path="/projects" component={ProjectsPage} />
      <ProtectedRoute path="/profile" component={HomePage} />
      <ProtectedRoute path="/token-designer" component={TokenDesignerPage} />
      <ProtectedRoute path="/economic-models" component={EconomicModelsPage} />
      <ProtectedRoute path="/distribution-plans" component={DistributionPlansPage} />
      <ProtectedRoute path="/vesting-schedules" component={DistributionPlansPage} />
      <ProtectedRoute path="/startup-planner" component={HomePage} />
      <ProtectedRoute path="/business-models" component={BusinessModelPage} />
      <ProtectedRoute path="/project-roadmap" component={HomePage} />
      <ProtectedRoute path="/team-builder" component={HomePage} />
      <ProtectedRoute path="/learning-center" component={HomePage} />
      <ProtectedRoute path="/help" component={HomePage} />
      <ProtectedRoute path="/settings" component={HomePage} />
      <ProtectedRoute path="/dashboard" component={Dashboard} /> {/* Added */}
      <ProtectedRoute path="/token-design" component={TokenDesign} /> {/* Added */}
      <ProtectedRoute path="/econometrics" component={EconometricsPage} /> {/* Added */}
      <ProtectedRoute path="/tokenization-models" component={TokenizationModelsPage} /> {/* Added */}
      <ProtectedRoute path="/business-model" component={BusinessModelPage} /> {/* Added */}
      <ProtectedRoute path="/market-analysis" component={MarketAnalysisPage} /> {/* Added */}
      <ProtectedRoute path="/marketing-growth" component={MarketingGrowthPage} /> {/* Added */}
      <ProtectedRoute path="/market-valuation" component={MarketValuationPage} /> {/* Added */}
      <ProtectedRoute path="/market-stress-test" component={MarketStressTestPage} /> {/* Added */}
      <ProtectedRoute path="/crypto-trading" component={CryptoTradingPage} /> {/* Added */}
      <ProtectedRoute path="/market-research" component={MarketResearchPage} /> {/* Added */}
      <ProtectedRoute path="/valuation" component={ValuationPage} /> {/* Added */}
      <ProtectedRoute path="/economic-engineering" component={EconomicEngineeringPage} /> {/* Added */}
      <ProtectedRoute path="/reports" component={ReportsPage} /> {/* Added */}
      <ProtectedRoute path="/community" component={CommunityPage} /> {/* Added */}
      <Route path="/auth" component={AuthPage} />
      <Route component={NotFound} />
    </Switch>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <Router />
        <Toaster />
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App;