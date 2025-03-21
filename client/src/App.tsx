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
      <ProtectedRoute path="/business-models" component={HomePage} />
      <ProtectedRoute path="/project-roadmap" component={HomePage} />
      <ProtectedRoute path="/team-builder" component={HomePage} />
      <ProtectedRoute path="/learning-center" component={HomePage} />
      <ProtectedRoute path="/help" component={HomePage} />
      <ProtectedRoute path="/settings" component={HomePage} />
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
