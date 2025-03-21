
import React from 'react';
import { Route, Switch } from 'wouter';
import { Toaster } from '@/components/ui/toaster';
import { QueryClientProvider } from '@tanstack/react-query';
import { queryClient } from '@/lib/queryClient';

// Páginas
import Dashboard from './pages/dashboard';
import TokenSupplyDistribution from './pages/token-supply-distribution';
import EconomicSimulation from './pages/economic-simulation';
import VestingSchedule from './pages/vesting-schedule';
import PriceMarketCap from './pages/price-market-cap';
import NotFound from './pages/not-found';
import AuthPage from './pages/auth-page';

// Componentes
import AppLayout from '@/components/layout/app-layout';

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = React.useState(true);

  // Se não estiver autenticado, mostrar a página de login
  if (!isAuthenticated) {
    return (
      <QueryClientProvider client={queryClient}>
        <AuthPage onLogin={() => setIsAuthenticated(true)} />
        <Toaster />
      </QueryClientProvider>
    );
  }

  return (
    <QueryClientProvider client={queryClient}>
      <AppLayout>
        <Switch>
          <Route path="/" component={Dashboard} />
          <Route path="/token-supply-distribution" component={TokenSupplyDistribution} />
          <Route path="/economic-simulation" component={EconomicSimulation} />
          <Route path="/vesting-schedule" component={VestingSchedule} />
          <Route path="/price-market-cap" component={PriceMarketCap} />
          <Route component={NotFound} />
        </Switch>
      </AppLayout>
      <Toaster />
    </QueryClientProvider>
  );
}
