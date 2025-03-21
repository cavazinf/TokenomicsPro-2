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
import Dashboard from "@/pages/dashboard";
import TokenDesign from "@/pages/token-design";
import EconometricsPage from "@/pages/econometrics";
import TokenizationModelsPage from "@/pages/tokenization-models";
import BusinessModelPage from "@/pages/business-model";
import MarketAnalysisPage from "@/pages/market-analysis";
import MarketingGrowthPage from "@/pages/marketing-growth";
import MarketValuationPage from "@/pages/market-valuation";
import MarketStressTestPage from "@/pages/market-stress-test";
import CryptoTradingPage from "@/pages/crypto-trading";
import MarketResearchPage from "@/pages/market-research";
import ValuationPage from "@/pages/valuation";
import EconomicEngineeringPage from "@/pages/economic-engineering";
import ReportsPage from "@/pages/reports";
import CommunityPage from "@/pages/community";


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
      <ProtectedRoute path="/dashboard" component={Dashboard} />
      <ProtectedRoute path="/token-design" component={TokenDesign} />
      <ProtectedRoute path="/econometrics" component={EconometricsPage} />
      <ProtectedRoute path="/tokenization-models" component={TokenizationModelsPage} />
      <ProtectedRoute path="/business-model" component={BusinessModelPage} />
      <ProtectedRoute path="/market-analysis" component={MarketAnalysisPage} />
      <ProtectedRoute path="/marketing-growth" component={MarketingGrowthPage} />
      <ProtectedRoute path="/market-valuation" component={MarketValuationPage} />
      <ProtectedRoute path="/market-stress-test" component={MarketStressTestPage} />
      <ProtectedRoute path="/crypto-trading" component={CryptoTradingPage} />
      <ProtectedRoute path="/market-research" component={MarketResearchPage} />
      <ProtectedRoute path="/valuation" component={ValuationPage} />
      <ProtectedRoute path="/economic-engineering" component={EconomicEngineeringPage} />
      <ProtectedRoute path="/reports" component={ReportsPage} />
      <ProtectedRoute path="/community" component={CommunityPage} />
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