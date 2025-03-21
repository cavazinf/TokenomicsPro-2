import React, { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Slider } from "@/components/ui/slider";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

export default function EconomicSimulation() {
  const [simulationParams, setSimulationParams] = useState({
    initialPrice: 0.1,
    initialUsers: 1000,
    userGrowthRate: 15, // % per month
    marketSentiment: 0, // -10 to 10
    stakingRatio: 20, // % of supply
    inflationRate: 2, // % per month
    volatilityFactor: 5, // 1-10 scale
    simulationMonths: 24,
  });

  const [data, setData] = useState<any[]>([]);
  const [activeMetric, setActiveMetric] = useState("price");

  useEffect(() => {
    simulateTokenEconomics();
  }, [simulationParams]);

  const handleParamChange = (param: string, value: number) => {
    setSimulationParams({
      ...simulationParams,
      [param]: value,
    });
  };

  const simulateTokenEconomics = () => {
    const totalSupply = 100000000;
    const monthlyData = [];
    let currentPrice = simulationParams.initialPrice;
    let marketCap = totalSupply * currentPrice;
    let circulatingSupply = totalSupply * 0.15; // Initial circulating supply is 15%
    let currentUsers = simulationParams.initialUsers;
    let stakedTokens = circulatingSupply * (simulationParams.stakingRatio / 100);

    // Base unlock schedule (simplified)
    const monthlyUnlock = totalSupply * 0.85 / simulationParams.simulationMonths;

    for (let month = 0; month <= simulationParams.simulationMonths; month++) {
      // Calculate new users
      const userGrowth = currentUsers * (simulationParams.userGrowthRate / 100);
      currentUsers += userGrowth;

      // Calculate token demand based on users
      const tokenDemand = currentUsers * 5 * (1 + simulationParams.marketSentiment / 20);

      // Add new tokens to circulation based on vesting
      circulatingSupply = Math.min(totalSupply, circulatingSupply + monthlyUnlock);
      
      // Account for inflation
      const newTokens = circulatingSupply * (simulationParams.inflationRate / 100);
      circulatingSupply += newTokens;

      // Update staked tokens
      stakedTokens = circulatingSupply * (simulationParams.stakingRatio / 100);
      
      // Token price based on demand/supply dynamics
      const effectiveSupply = circulatingSupply - stakedTokens;
      
      // Add volatility based on the volatility factor
      const volatility = (Math.random() - 0.5) * (simulationParams.volatilityFactor / 10);
      
      // Calculate new price based on demand/supply and volatility
      const demandFactor = tokenDemand / effectiveSupply;
      const sentimentFactor = 1 + (simulationParams.marketSentiment / 100);
      currentPrice = currentPrice * demandFactor * sentimentFactor * (1 + volatility);
      
      // Update market cap
      marketCap = currentPrice * circulatingSupply;

      monthlyData.push({
        month,
        price: currentPrice,
        marketCap,
        circulatingSupply,
        stakedTokens,
        users: currentUsers,
        tokenDemand,
      });
    }

    setData(monthlyData);
  };

  // Format number with appropriate prefix (K, M, B)
  const formatNumber = (num: number) => {
    if (num >= 1000000000) {
      return (num / 1000000000).toFixed(1) + 'B';
    }
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M';
    }
    if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K';
    }
    return num.toFixed(2);
  };

  // Format dollar amounts
  const formatDollar = (num: number) => {
    return '$' + formatNumber(num);
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight">Token Economic Simulation</h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-1">
          <CardHeader>
            <CardTitle>Simulation Parameters</CardTitle>
            <CardDescription>Adjust parameters to see their impact</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label>Initial Token Price</Label>
              <div className="flex items-center space-x-2">
                <span>$</span>
                <Input
                  type="number"
                  value={simulationParams.initialPrice}
                  onChange={(e) => handleParamChange('initialPrice', parseFloat(e.target.value))}
                  step={0.01}
                  min={0.001}
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label>Initial Users</Label>
              <Input
                type="number"
                value={simulationParams.initialUsers}
                onChange={(e) => handleParamChange('initialUsers', parseInt(e.target.value))}
                min={100}
              />
            </div>

            <div className="space-y-2">
              <div className="flex justify-between">
                <Label>User Growth Rate (%/month)</Label>
                <span>{simulationParams.userGrowthRate}%</span>
              </div>
              <Slider
                value={[simulationParams.userGrowthRate]}
                min={0}
                max={50}
                step={1}
                onValueChange={(value) => handleParamChange('userGrowthRate', value[0])}
              />
            </div>

            <div className="space-y-2">
              <div className="flex justify-between">
                <Label>Market Sentiment</Label>
                <span>{simulationParams.marketSentiment > 0 ? '+' : ''}{simulationParams.marketSentiment}</span>
              </div>
              <Slider
                value={[simulationParams.marketSentiment]}
                min={-10}
                max={10}
                step={1}
                onValueChange={(value) => handleParamChange('marketSentiment', value[0])}
              />
              <div className="flex justify-between text-xs text-gray-400">
                <span>Bearish</span>
                <span>Neutral</span>
                <span>Bullish</span>
              </div>
            </div>

            <div className="space-y-2">
              <div className="flex justify-between">
                <Label>Staking Ratio (%)</Label>
                <span>{simulationParams.stakingRatio}%</span>
              </div>
              <Slider
                value={[simulationParams.stakingRatio]}
                min={0}
                max={80}
                step={1}
                onValueChange={(value) => handleParamChange('stakingRatio', value[0])}
              />
            </div>

            <div className="space-y-2">
              <div className="flex justify-between">
                <Label>Monthly Inflation Rate (%)</Label>
                <span>{simulationParams.inflationRate}%</span>
              </div>
              <Slider
                value={[simulationParams.inflationRate]}
                min={0}
                max={10}
                step={0.1}
                onValueChange={(value) => handleParamChange('inflationRate', value[0])}
              />
            </div>

            <div className="space-y-2">
              <div className="flex justify-between">
                <Label>Volatility Factor</Label>
                <span>{simulationParams.volatilityFactor}</span>
              </div>
              <Slider
                value={[simulationParams.volatilityFactor]}
                min={1}
                max={10}
                step={1}
                onValueChange={(value) => handleParamChange('volatilityFactor', value[0])}
              />
              <div className="flex justify-between text-xs text-gray-400">
                <span>Low</span>
                <span>Medium</span>
                <span>High</span>
              </div>
            </div>

            <div className="space-y-2">
              <div className="flex justify-between">
                <Label>Simulation Duration (months)</Label>
                <span>{simulationParams.simulationMonths}</span>
              </div>
              <Slider
                value={[simulationParams.simulationMonths]}
                min={12}
                max={60}
                step={6}
                onValueChange={(value) => handleParamChange('simulationMonths', value[0])}
              />
            </div>

            <Button className="w-full" onClick={simulateTokenEconomics}>
              Run Simulation
            </Button>
          </CardContent>
        </Card>

        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Simulation Results</CardTitle>
            <CardDescription>
              Projected token metrics over {simulationParams.simulationMonths} months
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Tabs defaultValue="price" onValueChange={setActiveMetric} value={activeMetric}>
              <TabsList className="grid grid-cols-5 w-full">
                <TabsTrigger value="price">Price</TabsTrigger>
                <TabsTrigger value="marketCap">Market Cap</TabsTrigger>
                <TabsTrigger value="supply">Supply</TabsTrigger>
                <TabsTrigger value="users">Users</TabsTrigger>
                <TabsTrigger value="staking">Staking</TabsTrigger>
              </TabsList>
                
              <TabsContent value="price" className="h-[400px] mt-4">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={data}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      dataKey="month" 
                      label={{ value: 'Month', position: 'insideBottom', offset: -5 }}
                    />
                    <YAxis 
                      tickFormatter={(value) => '$' + value.toFixed(4)} 
                      label={{ value: 'Price (USD)', angle: -90, position: 'insideLeft' }}
                    />
                    <Tooltip 
                      formatter={(value: number) => ['$' + value.toFixed(4), 'Price']}
                      labelFormatter={(label) => `Month ${label}`}
                    />
                    <Line 
                      type="monotone" 
                      dataKey="price" 
                      stroke="#4f46e5" 
                      dot={false} 
                      activeDot={{ r: 8 }} 
                    />
                  </LineChart>
                </ResponsiveContainer>
              </TabsContent>

              <TabsContent value="marketCap" className="h-full">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={data}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      dataKey="month" 
                      label={{ value: 'Month', position: 'insideBottom', offset: -5 }}
                    />
                    <YAxis 
                      tickFormatter={(value) => formatDollar(value)}
                      label={{ value: 'Market Cap (USD)', angle: -90, position: 'insideLeft' }}
                    />
                    <Tooltip 
                      formatter={(value: number) => [formatDollar(value), 'Market Cap']}
                      labelFormatter={(label) => `Month ${label}`}
                    />
                    <Area 
                      type="monotone" 
                      dataKey="marketCap" 
                      stroke="#0ea5e9" 
                      fill="#0ea5e9" 
                      fillOpacity={0.3} 
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </TabsContent>

              <TabsContent value="supply" className="h-full">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={data}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      dataKey="month" 
                      label={{ value: 'Month', position: 'insideBottom', offset: -5 }}
                    />
                    <YAxis 
                      tickFormatter={(value) => formatNumber(value)}
                      label={{ value: 'Token Supply', angle: -90, position: 'insideLeft' }}
                    />
                    <Tooltip 
                      formatter={(value: number, name: string) => [
                        formatNumber(value), 
                        name === 'circulatingSupply' ? 'Circulating Supply' : 'Staked Tokens'
                      ]}
                      labelFormatter={(label) => `Month ${label}`}
                    />
                    <Legend />
                    <Line 
                      type="monotone" 
                      dataKey="circulatingSupply" 
                      name="Circulating Supply"
                      stroke="#10b981" 
                      dot={false} 
                    />
                    <Line 
                      type="monotone" 
                      dataKey="stakedTokens" 
                      name="Staked Tokens"
                      stroke="#8b5cf6" 
                      dot={false} 
                    />
                  </LineChart>
                </ResponsiveContainer>
              </TabsContent>

              <TabsContent value="users" className="h-full">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={data}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      dataKey="month" 
                      label={{ value: 'Month', position: 'insideBottom', offset: -5 }}
                    />
                    <YAxis 
                      tickFormatter={(value) => formatNumber(value)}
                      label={{ value: 'User Count', angle: -90, position: 'insideLeft' }}
                    />
                    <Tooltip 
                      formatter={(value: number) => [formatNumber(value), 'Users']}
                      labelFormatter={(label) => `Month ${label}`}
                    />
                    <Area 
                      type="monotone" 
                      dataKey="users" 
                      stroke="#f59e0b" 
                      fill="#f59e0b" 
                      fillOpacity={0.3} 
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </TabsContent>

              <TabsContent value="staking" className="h-full">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={data}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      dataKey="month" 
                      label={{ value: 'Month', position: 'insideBottom', offset: -5 }}
                    />
                    <YAxis 
                      tickFormatter={(value) => formatNumber(value)}
                      yAxisId="left"
                      label={{ value: 'Staked Tokens', angle: -90, position: 'insideLeft' }}
                    />
                    <YAxis 
                      tickFormatter={(value) => (value * 100).toFixed(0) + '%'}
                      yAxisId="right"
                      orientation="right"
                      label={{ value: 'Staking %', angle: 90, position: 'insideRight' }}
                    />
                    <Tooltip 
                      formatter={(value: number, name: string) => [
                        name === 'stakedTokens' ? formatNumber(value) : (value * 100).toFixed(1) + '%',
                        name === 'stakedTokens' ? 'Staked Tokens' : 'Staking Ratio'
                      ]}
                      labelFormatter={(label) => `Month ${label}`}
                    />
                    <Legend />
                    <Line 
                      type="monotone" 
                      dataKey="stakedTokens" 
                      yAxisId="left"
                      name="Staked Tokens"
                      stroke="#8b5cf6" 
                      dot={false} 
                    />
                    <Line 
                      type="monotone" 
                      dataKey={(entry) => entry.stakedTokens / entry.circulatingSupply} 
                      yAxisId="right"
                      name="Staking Ratio"
                      stroke="#ec4899" 
                      dot={false} 
                    />
                  </LineChart>
                </ResponsiveContainer>
              </TabsContent>
              
              {data.length > 0 && (
                <div className="mt-4 grid grid-cols-3 gap-4">
                  <div className="border rounded-lg p-3 text-center">
                    <div className="text-sm text-gray-400">Final Price</div>
                    <div className="text-lg font-semibold">${data[data.length - 1].price.toFixed(4)}</div>
                    <div className="text-xs text-gray-400">
                      {(data[data.length - 1].price / data[0].price > 1 ? '+' : '')}
                      {((data[data.length - 1].price / data[0].price - 1) * 100).toFixed(1)}%
                    </div>
                  </div>
                  <div className="border rounded-lg p-3 text-center">
                    <div className="text-sm text-gray-400">Final Market Cap</div>
                    <div className="text-lg font-semibold">{formatDollar(data[data.length - 1].marketCap)}</div>
                    <div className="text-xs text-gray-400">
                      {(data[data.length - 1].marketCap / data[0].marketCap > 1 ? '+' : '')}
                      {((data[data.length - 1].marketCap / data[0].marketCap - 1) * 100).toFixed(1)}%
                    </div>
                  </div>
                  <div className="border rounded-lg p-3 text-center">
                    <div className="text-sm text-gray-400">Final Users</div>
                    <div className="text-lg font-semibold">{formatNumber(data[data.length - 1].users)}</div>
                    <div className="text-xs text-gray-400">
                      {(data[data.length - 1].users / data[0].users > 1 ? '+' : '')}
                      {((data[data.length - 1].users / data[0].users - 1) * 100).toFixed(1)}%
                    </div>
                  </div>
                </div>
              )}
            </Tabs>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}