import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Slider } from "@/components/ui/slider";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { useToast } from "@/hooks/use-toast";

export default function EconomicSimulator() {
  const { toast } = useToast();
  
  // Simulation parameters
  const [initialParams, setInitialParams] = useState({
    totalSupply: 100000000,
    initialPrice: 0.01,
    burnRate: 2,
    inflationRate: 5,
    stakingYield: 8,
    adoptionGrowth: 30,
    marketSentiment: 0,
    simulationYears: 5
  });
  
  // Simulation results
  const [simulationResults, setSimulationResults] = useState<any[]>([]);
  
  // Update parameter
  const updateParam = (param: string, value: number) => {
    setInitialParams({
      ...initialParams,
      [param]: value
    });
  };
  
  // Run the simulation
  const runSimulation = () => {
    const {
      totalSupply,
      initialPrice,
      burnRate,
      inflationRate,
      stakingYield,
      adoptionGrowth,
      marketSentiment,
      simulationYears
    } = initialParams;
    
    const results = [];
    let currentPrice = initialPrice;
    let currentSupply = totalSupply;
    let currentMarketCap = currentPrice * currentSupply;
    let currentDemand = 1;
    
    // Simulation variables
    const sentimentMultiplier = 1 + (marketSentiment / 100);
    const monthlyBurnRate = burnRate / 1200; // Monthly rate
    const monthlyInflationRate = inflationRate / 1200; // Monthly rate
    const monthlyStakingYield = stakingYield / 1200; // Monthly rate
    const monthlyAdoptionGrowth = adoptionGrowth / 1200; // Monthly rate
    
    // Run monthly simulation for the specified years
    for (let month = 0; month <= simulationYears * 12; month++) {
      // Calculate supply changes
      const burnAmount = currentSupply * monthlyBurnRate;
      const inflationAmount = currentSupply * monthlyInflationRate;
      const netSupplyChange = inflationAmount - burnAmount;
      
      // Update supply
      currentSupply += netSupplyChange;
      
      // Calculate demand changes (adoption growth + staking)
      const stakedTokens = currentSupply * (monthlyStakingYield * 10); // Rough approximation
      const adoptionIncrease = currentDemand * monthlyAdoptionGrowth;
      currentDemand += adoptionIncrease;
      
      // Apply market sentiment
      const sentimentEffect = ((month % 3 === 0) ? Math.random() * 0.1 - 0.05 : 0) * sentimentMultiplier;
      
      // Calculate new price based on supply/demand dynamics
      const supplyDemandEffect = (currentDemand / currentSupply) * 0.01;
      const stakingEffect = (stakedTokens / currentSupply) * 0.005;
      
      currentPrice *= (1 + supplyDemandEffect + stakingEffect + sentimentEffect);
      currentMarketCap = currentPrice * currentSupply;
      
      // Only add every quarter to keep the data manageable
      if (month % 3 === 0) {
        results.push({
          month,
          price: currentPrice,
          marketCap: currentMarketCap,
          supply: currentSupply,
          stakedTokens
        });
      }
    }
    
    setSimulationResults(results);
    
    toast({
      title: "Simulation completed",
      description: "The economic simulation has been run successfully."
    });
  };
  
  // Format large numbers for display
  const formatLargeNumber = (num: number) => {
    if (num >= 1000000000) {
      return (num / 1000000000).toFixed(2) + 'B';
    }
    if (num >= 1000000) {
      return (num / 1000000).toFixed(2) + 'M';
    }
    if (num >= 1000) {
      return (num / 1000).toFixed(2) + 'K';
    }
    return num.toFixed(2);
  };
  
  // Format price for display
  const formatPrice = (price: number) => {
    if (price < 0.0001) {
      return price.toExponential(2);
    }
    return price.toFixed(price < 0.01 ? 6 : price < 1 ? 4 : 2);
  };

  return (
    <div className="max-w-6xl mx-auto">
      <header className="mb-8">
        <h1 className="text-2xl md:text-3xl font-bold text-dark">Economic Simulator</h1>
        <p className="text-dark-50 mt-2">Simulate how your token will perform under different economic scenarios</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-1">
          <CardHeader>
            <CardTitle>Simulation Parameters</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-2">
              <div className="flex justify-between">
                <Label htmlFor="totalSupply">Total Supply</Label>
                <span className="text-sm">{initialParams.totalSupply.toLocaleString()}</span>
              </div>
              <Input 
                id="totalSupply" 
                type="number" 
                value={initialParams.totalSupply}
                onChange={(e) => updateParam('totalSupply', parseFloat(e.target.value) || 0)}
              />
            </div>
            
            <div className="space-y-2">
              <div className="flex justify-between">
                <Label htmlFor="initialPrice">Initial Price (USD)</Label>
                <span className="text-sm">${initialParams.initialPrice}</span>
              </div>
              <Input 
                id="initialPrice" 
                type="number" 
                value={initialParams.initialPrice}
                onChange={(e) => updateParam('initialPrice', parseFloat(e.target.value) || 0)}
                step="0.001"
              />
            </div>
            
            <div className="space-y-2">
              <div className="flex justify-between">
                <Label>Token Burn Rate (% per year)</Label>
                <span className="text-sm">{initialParams.burnRate}%</span>
              </div>
              <Slider 
                value={[initialParams.burnRate]} 
                min={0} 
                max={10} 
                step={0.1}
                onValueChange={(vals) => updateParam('burnRate', vals[0])}
              />
            </div>
            
            <div className="space-y-2">
              <div className="flex justify-between">
                <Label>Inflation Rate (% per year)</Label>
                <span className="text-sm">{initialParams.inflationRate}%</span>
              </div>
              <Slider 
                value={[initialParams.inflationRate]} 
                min={0} 
                max={20} 
                step={0.5}
                onValueChange={(vals) => updateParam('inflationRate', vals[0])}
              />
            </div>
            
            <div className="space-y-2">
              <div className="flex justify-between">
                <Label>Staking Yield (% per year)</Label>
                <span className="text-sm">{initialParams.stakingYield}%</span>
              </div>
              <Slider 
                value={[initialParams.stakingYield]} 
                min={0} 
                max={30} 
                step={0.5}
                onValueChange={(vals) => updateParam('stakingYield', vals[0])}
              />
            </div>
            
            <div className="space-y-2">
              <div className="flex justify-between">
                <Label>Adoption Growth (% per year)</Label>
                <span className="text-sm">{initialParams.adoptionGrowth}%</span>
              </div>
              <Slider 
                value={[initialParams.adoptionGrowth]} 
                min={0} 
                max={200} 
                step={5}
                onValueChange={(vals) => updateParam('adoptionGrowth', vals[0])}
              />
            </div>
            
            <div className="space-y-2">
              <div className="flex justify-between">
                <Label>Market Sentiment Factor</Label>
                <span className="text-sm">{initialParams.marketSentiment > 0 ? "+" : ""}{initialParams.marketSentiment}%</span>
              </div>
              <Slider 
                value={[initialParams.marketSentiment]} 
                min={-50} 
                max={50} 
                step={5}
                onValueChange={(vals) => updateParam('marketSentiment', vals[0])}
              />
            </div>
            
            <div className="space-y-2">
              <div className="flex justify-between">
                <Label>Simulation Years</Label>
                <span className="text-sm">{initialParams.simulationYears}</span>
              </div>
              <Slider 
                value={[initialParams.simulationYears]} 
                min={1} 
                max={10} 
                step={1}
                onValueChange={(vals) => updateParam('simulationYears', vals[0])}
              />
            </div>
            
            <Button 
              className="w-full mt-6"
              onClick={runSimulation}
            >
              Run Simulation
            </Button>
          </CardContent>
        </Card>
        
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Simulation Results</CardTitle>
          </CardHeader>
          <CardContent>
            {simulationResults.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-80 text-center">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-16 w-16 text-muted-foreground mb-4">
                  <path d="M3 3v18h18"></path>
                  <path d="M18.7 8l-5.1 5.2-2.8-2.7L7 14.3"></path>
                </svg>
                <h3 className="text-lg font-medium mb-2">No simulation data yet</h3>
                <p className="text-muted-foreground">Adjust the parameters and run the simulation to see results.</p>
              </div>
            ) : (
              <Tabs defaultValue="price">
                <TabsList className="mb-4">
                  <TabsTrigger value="price">Price</TabsTrigger>
                  <TabsTrigger value="marketCap">Market Cap</TabsTrigger>
                  <TabsTrigger value="supply">Token Supply</TabsTrigger>
                </TabsList>
                
                <TabsContent value="price">
                  <div className="h-80">
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={simulationResults}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis 
                          dataKey="month" 
                          label={{ value: 'Months', position: 'insideBottomRight', offset: -5 }}
                          tickFormatter={(month) => `${Math.floor(month/12)}y${month%12}m`}
                        />
                        <YAxis 
                          tickFormatter={(price) => `$${formatPrice(price)}`}
                          label={{ value: 'Price (USD)', angle: -90, position: 'insideLeft' }}
                        />
                        <Tooltip 
                          formatter={(value: number) => [`$${formatPrice(value)}`, 'Price']}
                          labelFormatter={(month) => `Month ${month} (Year ${Math.floor(month/12)}, Month ${month%12})`}
                        />
                        <Legend />
                        <Line 
                          type="monotone" 
                          dataKey="price" 
                          stroke="#5E8CFF" 
                          name="Token Price" 
                          dot={false}
                          activeDot={{ r: 4 }}
                        />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                  
                  <div className="mt-8 grid grid-cols-2 md:grid-cols-3 gap-4">
                    <div className="bg-light-100 p-4 rounded-lg">
                      <div className="text-sm text-muted-foreground">Initial Price</div>
                      <div className="font-semibold">${formatPrice(initialParams.initialPrice)}</div>
                    </div>
                    <div className="bg-light-100 p-4 rounded-lg">
                      <div className="text-sm text-muted-foreground">Final Price</div>
                      <div className="font-semibold">${formatPrice(simulationResults[simulationResults.length - 1].price)}</div>
                    </div>
                    <div className="bg-light-100 p-4 rounded-lg">
                      <div className="text-sm text-muted-foreground">Price Change</div>
                      <div className={`font-semibold ${simulationResults[simulationResults.length - 1].price > initialParams.initialPrice ? 'text-green-600' : 'text-red-600'}`}>
                        {(((simulationResults[simulationResults.length - 1].price / initialParams.initialPrice) - 1) * 100).toFixed(2)}%
                      </div>
                    </div>
                  </div>
                </TabsContent>
                
                <TabsContent value="marketCap">
                  <div className="h-80">
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={simulationResults}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis 
                          dataKey="month" 
                          label={{ value: 'Months', position: 'insideBottomRight', offset: -5 }}
                          tickFormatter={(month) => `${Math.floor(month/12)}y${month%12}m`}
                        />
                        <YAxis 
                          tickFormatter={(value) => `$${formatLargeNumber(value)}`}
                          label={{ value: 'Market Cap (USD)', angle: -90, position: 'insideLeft' }}
                        />
                        <Tooltip 
                          formatter={(value: number) => [`$${formatLargeNumber(value)}`, 'Market Cap']}
                          labelFormatter={(month) => `Month ${month} (Year ${Math.floor(month/12)}, Month ${month%12})`}
                        />
                        <Legend />
                        <Line 
                          type="monotone" 
                          dataKey="marketCap" 
                          stroke="#4CAF98" 
                          name="Market Cap" 
                          dot={false}
                          activeDot={{ r: 4 }}
                        />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                  
                  <div className="mt-8 grid grid-cols-2 md:grid-cols-3 gap-4">
                    <div className="bg-light-100 p-4 rounded-lg">
                      <div className="text-sm text-muted-foreground">Initial Market Cap</div>
                      <div className="font-semibold">${formatLargeNumber(initialParams.initialPrice * initialParams.totalSupply)}</div>
                    </div>
                    <div className="bg-light-100 p-4 rounded-lg">
                      <div className="text-sm text-muted-foreground">Final Market Cap</div>
                      <div className="font-semibold">${formatLargeNumber(simulationResults[simulationResults.length - 1].marketCap)}</div>
                    </div>
                    <div className="bg-light-100 p-4 rounded-lg">
                      <div className="text-sm text-muted-foreground">Market Cap Growth</div>
                      <div className={`font-semibold ${simulationResults[simulationResults.length - 1].marketCap > (initialParams.initialPrice * initialParams.totalSupply) ? 'text-green-600' : 'text-red-600'}`}>
                        {(((simulationResults[simulationResults.length - 1].marketCap / (initialParams.initialPrice * initialParams.totalSupply)) - 1) * 100).toFixed(2)}%
                      </div>
                    </div>
                  </div>
                </TabsContent>
                
                <TabsContent value="supply">
                  <div className="h-80">
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={simulationResults}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis 
                          dataKey="month" 
                          label={{ value: 'Months', position: 'insideBottomRight', offset: -5 }}
                          tickFormatter={(month) => `${Math.floor(month/12)}y${month%12}m`}
                        />
                        <YAxis 
                          tickFormatter={(value) => formatLargeNumber(value)}
                          label={{ value: 'Token Supply', angle: -90, position: 'insideLeft' }}
                        />
                        <Tooltip 
                          formatter={(value: number) => [formatLargeNumber(value), 'Supply']}
                          labelFormatter={(month) => `Month ${month} (Year ${Math.floor(month/12)}, Month ${month%12})`}
                        />
                        <Legend />
                        <Line 
                          type="monotone" 
                          dataKey="supply" 
                          stroke="#8A63E8" 
                          name="Total Supply" 
                          dot={false}
                          activeDot={{ r: 4 }}
                        />
                        <Line 
                          type="monotone" 
                          dataKey="stakedTokens" 
                          stroke="#FF9966" 
                          name="Staked Tokens" 
                          dot={false}
                          activeDot={{ r: 4 }}
                        />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                  
                  <div className="mt-8 grid grid-cols-2 md:grid-cols-3 gap-4">
                    <div className="bg-light-100 p-4 rounded-lg">
                      <div className="text-sm text-muted-foreground">Initial Supply</div>
                      <div className="font-semibold">{formatLargeNumber(initialParams.totalSupply)}</div>
                    </div>
                    <div className="bg-light-100 p-4 rounded-lg">
                      <div className="text-sm text-muted-foreground">Final Supply</div>
                      <div className="font-semibold">{formatLargeNumber(simulationResults[simulationResults.length - 1].supply)}</div>
                    </div>
                    <div className="bg-light-100 p-4 rounded-lg">
                      <div className="text-sm text-muted-foreground">Supply Change</div>
                      <div className={`font-semibold ${simulationResults[simulationResults.length - 1].supply > initialParams.totalSupply ? 'text-green-600' : 'text-red-600'}`}>
                        {(((simulationResults[simulationResults.length - 1].supply / initialParams.totalSupply) - 1) * 100).toFixed(2)}%
                      </div>
                    </div>
                  </div>
                </TabsContent>
              </Tabs>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
