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
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

export default function PriceMarketCap() {
  const [supplyParams, setSupplyParams] = useState({
    totalSupply: 100000000,
    initialCirculating: 15, // % of total
    unlockPeriod: 48, // months
    inflationRate: 2, // % per year
  });

  const [priceParams, setPriceParams] = useState({
    initialPrice: 0.1, // $
    initialLiquidity: 500000, // $
    growthScenario: 'moderate', // conservative, moderate, aggressive
  });

  const [simulationMonths, setSimulationMonths] = useState(36);
  const [data, setData] = useState<any[]>([]);

  useEffect(() => {
    simulatePriceAndMarketCap();
  }, [supplyParams, priceParams, simulationMonths]);

  const handleSupplyParamChange = (param: string, value: number) => {
    setSupplyParams({
      ...supplyParams,
      [param]: value,
    });
  };

  const handlePriceParamChange = (param: string, value: number | string) => {
    setPriceParams({
      ...priceParams,
      [param]: value,
    });
  };

  const calculateCirculatingSupply = (month: number) => {
    const { totalSupply, initialCirculating, unlockPeriod, inflationRate } = supplyParams;
    
    // Initial circulating supply
    let initialAmount = totalSupply * (initialCirculating / 100);
    
    // Linear unlock over the unlock period
    const lockedSupply = totalSupply - initialAmount;
    const monthlyUnlock = unlockPeriod > 0 ? lockedSupply / unlockPeriod : 0;
    
    // Calculate unlocked amount based on month
    const unlockAmount = Math.min(monthlyUnlock * month, lockedSupply);
    
    // Calculate inflation
    const yearlyInflation = totalSupply * (inflationRate / 100);
    const monthlyInflation = yearlyInflation / 12;
    const inflationAmount = monthlyInflation * month;
    
    return initialAmount + unlockAmount + inflationAmount;
  };

  const simulatePriceAndMarketCap = () => {
    const { initialPrice, initialLiquidity, growthScenario } = priceParams;
    
    // Growth rates for different scenarios (monthly)
    const growthRates: Record<string, number> = {
      conservative: 0.015, // 1.5% monthly (about 20% annually)
      moderate: 0.03,     // 3% monthly (about 40% annually)
      aggressive: 0.05,   // 5% monthly (about 80% annually)
    };
    
    const monthlyRate = growthRates[growthScenario];
    const volatilityFactor = {
      conservative: 0.03,
      moderate: 0.05,
      aggressive: 0.08,
    }[growthScenario];
    
    const simulationData = [];
    
    for (let month = 0; month <= simulationMonths; month++) {
      const circulatingSupply = calculateCirculatingSupply(month);
      
      // Calculate price with some randomness for volatility
      const growthComponent = Math.pow(1 + monthlyRate, month);
      const volatility = 1 + (Math.random() - 0.5) * volatilityFactor;
      const price = initialPrice * growthComponent * volatility;
      
      // Calculate market metrics
      const marketCap = price * circulatingSupply;
      const fullyDilutedValuation = price * supplyParams.totalSupply;
      
      // Calculate liquidity
      const liquidity = initialLiquidity * Math.pow(1 + monthlyRate / 2, month);
      
      simulationData.push({
        month,
        price,
        circulatingSupply,
        marketCap,
        fullyDilutedValuation,
        liquidity,
        liquidityRatio: liquidity / marketCap,
      });
    }
    
    setData(simulationData);
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

  // Format percentage
  const formatPercent = (num: number) => {
    return (num * 100).toFixed(1) + '%';
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight">Price & Market Cap Simulator</h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Supply Parameters</CardTitle>
              <CardDescription>Configure token supply metrics</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="totalSupply">Total Supply</Label>
                <Input
                  id="totalSupply"
                  type="number"
                  value={supplyParams.totalSupply}
                  onChange={(e) => handleSupplyParamChange('totalSupply', Number(e.target.value))}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="initialCirculating">Initial Circulating Supply (%)</Label>
                <Input
                  id="initialCirculating"
                  type="number"
                  value={supplyParams.initialCirculating}
                  onChange={(e) => handleSupplyParamChange('initialCirculating', Number(e.target.value))}
                  min={0}
                  max={100}
                />
                <div className="text-sm text-gray-400">
                  {formatNumber(supplyParams.totalSupply * (supplyParams.initialCirculating / 100))} tokens
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="unlockPeriod">Unlock Period (months)</Label>
                <Input
                  id="unlockPeriod"
                  type="number"
                  value={supplyParams.unlockPeriod}
                  onChange={(e) => handleSupplyParamChange('unlockPeriod', Number(e.target.value))}
                  min={0}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="inflationRate">Annual Inflation Rate (%)</Label>
                <Input
                  id="inflationRate"
                  type="number"
                  value={supplyParams.inflationRate}
                  onChange={(e) => handleSupplyParamChange('inflationRate', Number(e.target.value))}
                  min={0}
                />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Price Parameters</CardTitle>
              <CardDescription>Configure token price metrics</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="initialPrice">Initial Token Price (USD)</Label>
                <div className="flex items-center space-x-2">
                  <span>$</span>
                  <Input
                    id="initialPrice"
                    type="number"
                    value={priceParams.initialPrice}
                    onChange={(e) => handlePriceParamChange('initialPrice', Number(e.target.value))}
                    step={0.01}
                    min={0.0001}
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="initialLiquidity">Initial Liquidity (USD)</Label>
                <div className="flex items-center space-x-2">
                  <span>$</span>
                  <Input
                    id="initialLiquidity"
                    type="number"
                    value={priceParams.initialLiquidity}
                    onChange={(e) => handlePriceParamChange('initialLiquidity', Number(e.target.value))}
                    min={0}
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="growthScenario">Growth Scenario</Label>
                <Select
                  value={priceParams.growthScenario}
                  onValueChange={(value) => handlePriceParamChange('growthScenario', value)}
                >
                  <SelectTrigger id="growthScenario">
                    <SelectValue placeholder="Select growth scenario" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="conservative">Conservative (~20% yearly)</SelectItem>
                    <SelectItem value="moderate">Moderate (~40% yearly)</SelectItem>
                    <SelectItem value="aggressive">Aggressive (~80% yearly)</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="simulationMonths">Simulation Duration (months)</Label>
                <Input
                  id="simulationMonths"
                  type="number"
                  value={simulationMonths}
                  onChange={(e) => setSimulationMonths(Number(e.target.value))}
                  min={12}
                  max={120}
                />
              </div>

              <Button className="w-full" onClick={simulatePriceAndMarketCap}>
                Run Simulation
              </Button>
            </CardContent>
          </Card>
        </div>

        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Market Metrics Projection</CardTitle>
            <CardDescription>
              Projected token metrics over {simulationMonths} months
            </CardDescription>
            <Tabs defaultValue="price">
              <TabsList className="grid grid-cols-4 w-full">
                <TabsTrigger value="price">Price</TabsTrigger>
                <TabsTrigger value="marketCap">Market Cap</TabsTrigger>
                <TabsTrigger value="supply">Circulating Supply</TabsTrigger>
                <TabsTrigger value="liquidity">Liquidity</TabsTrigger>
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

              <TabsContent value="marketCap" className="h-[400px] mt-4">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={data}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      dataKey="month" 
                      label={{ value: 'Month', position: 'insideBottom', offset: -5 }}
                    />
                    <YAxis 
                      tickFormatter={(value) => formatDollar(value)}
                      label={{ value: 'USD Value', angle: -90, position: 'insideLeft' }}
                    />
                    <Tooltip 
                      formatter={(value: number, name: string) => [
                        formatDollar(value), 
                        name === 'marketCap' ? 'Market Cap' : 'Fully Diluted Valuation'
                      ]}
                      labelFormatter={(label) => `Month ${label}`}
                    />
                    <Legend />
                    <Area 
                      type="monotone" 
                      dataKey="marketCap" 
                      name="Market Cap"
                      stroke="#0ea5e9" 
                      fill="#0ea5e9" 
                      fillOpacity={0.3} 
                    />
                    <Area 
                      type="monotone" 
                      dataKey="fullyDilutedValuation" 
                      name="Fully Diluted Valuation"
                      stroke="#8b5cf6" 
                      fill="#8b5cf6" 
                      fillOpacity={0.3} 
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </TabsContent>

              <TabsContent value="supply" className="h-[400px] mt-4">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={data}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      dataKey="month" 
                      label={{ value: 'Month', position: 'insideBottom', offset: -5 }}
                    />
                    <YAxis 
                      tickFormatter={(value) => formatNumber(value)}
                      label={{ value: 'Tokens', angle: -90, position: 'insideLeft' }}
                    />
                    <Tooltip 
                      formatter={(value: number) => [formatNumber(value), 'Circulating Supply']}
                      labelFormatter={(label) => `Month ${label}`}
                    />
                    <Area 
                      type="monotone" 
                      dataKey="circulatingSupply" 
                      name="Circulating Supply"
                      stroke="#10b981" 
                      fill="#10b981" 
                      fillOpacity={0.3} 
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </TabsContent>

              <TabsContent value="liquidity" className="h-[400px] mt-4">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={data}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      dataKey="month" 
                      label={{ value: 'Month', position: 'insideBottom', offset: -5 }}
                    />
                    <YAxis 
                      yAxisId="left"
                      tickFormatter={(value) => formatDollar(value)}
                      label={{ value: 'Liquidity (USD)', angle: -90, position: 'insideLeft' }}
                    />
                    <YAxis 
                      yAxisId="right"
                      orientation="right"
                      tickFormatter={(value) => formatPercent(value)}
                      label={{ value: 'Liquidity Ratio', angle: 90, position: 'insideRight' }}
                    />
                    <Tooltip 
                      formatter={(value: number, name: string) => [
                        name === 'liquidity' ? formatDollar(value) : formatPercent(value),
                        name === 'liquidity' ? 'Liquidity' : 'Liquidity Ratio'
                      ]}
                      labelFormatter={(label) => `Month ${label}`}
                    />
                    <Legend />
                    <Line 
                      type="monotone" 
                      dataKey="liquidity" 
                      name="Liquidity"
                      yAxisId="left"
                      stroke="#f59e0b" 
                      dot={false} 
                    />
                    <Line 
                      type="monotone" 
                      dataKey="liquidityRatio" 
                      name="Liquidity Ratio"
                      yAxisId="right"
                      stroke="#ef4444" 
                      dot={false} 
                    />
                  </LineChart>
                </ResponsiveContainer>
              </TabsContent>
            </Tabs>

            {data.length > 0 && (
              <div className="mt-6 grid grid-cols-2 gap-4">
                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-lg">Price Metrics</CardTitle>
                  </CardHeader>
                  <CardContent className="pt-0">
                    <dl className="space-y-2">
                      <div className="flex justify-between">
                        <dt className="text-sm text-gray-400">Initial Price:</dt>
                        <dd className="text-sm font-medium">${priceParams.initialPrice.toFixed(4)}</dd>
                      </div>
                      <div className="flex justify-between">
                        <dt className="text-sm text-gray-400">Final Price:</dt>
                        <dd className="text-sm font-medium">${data[data.length - 1].price.toFixed(4)}</dd>
                      </div>
                      <div className="flex justify-between">
                        <dt className="text-sm text-gray-400">Price Change:</dt>
                        <dd className={`text-sm font-medium ${data[data.length - 1].price > data[0].price ? 'text-green-500' : 'text-red-500'}`}>
                          {((data[data.length - 1].price / data[0].price - 1) * 100).toFixed(1)}%
                        </dd>
                      </div>
                      <div className="flex justify-between">
                        <dt className="text-sm text-gray-400">Market Cap (Final):</dt>
                        <dd className="text-sm font-medium">{formatDollar(data[data.length - 1].marketCap)}</dd>
                      </div>
                      <div className="flex justify-between">
                        <dt className="text-sm text-gray-400">FDV (Final):</dt>
                        <dd className="text-sm font-medium">{formatDollar(data[data.length - 1].fullyDilutedValuation)}</dd>
                      </div>
                    </dl>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-lg">Supply Metrics</CardTitle>
                  </CardHeader>
                  <CardContent className="pt-0">
                    <dl className="space-y-2">
                      <div className="flex justify-between">
                        <dt className="text-sm text-gray-400">Total Supply:</dt>
                        <dd className="text-sm font-medium">{formatNumber(supplyParams.totalSupply)}</dd>
                      </div>
                      <div className="flex justify-between">
                        <dt className="text-sm text-gray-400">Initial Circulating:</dt>
                        <dd className="text-sm font-medium">
                          {formatNumber(data[0].circulatingSupply)} ({supplyParams.initialCirculating}%)
                        </dd>
                      </div>
                      <div className="flex justify-between">
                        <dt className="text-sm text-gray-400">Final Circulating:</dt>
                        <dd className="text-sm font-medium">
                          {formatNumber(data[data.length - 1].circulatingSupply)} 
                          ({(data[data.length - 1].circulatingSupply / supplyParams.totalSupply * 100).toFixed(1)}%)
                        </dd>
                      </div>
                      <div className="flex justify-between">
                        <dt className="text-sm text-gray-400">Final Liquidity:</dt>
                        <dd className="text-sm font-medium">{formatDollar(data[data.length - 1].liquidity)}</dd>
                      </div>
                      <div className="flex justify-between">
                        <dt className="text-sm text-gray-400">Liquidity Ratio:</dt>
                        <dd className="text-sm font-medium">
                          {formatPercent(data[data.length - 1].liquidityRatio)}
                        </dd>
                      </div>
                    </dl>
                  </CardContent>
                </Card>
              </div>
            )}
          </CardHeader>
        </Card>
      </div>
    </div>
  );
}