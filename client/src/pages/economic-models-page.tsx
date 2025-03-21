import { useState, useEffect } from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { useAuth } from "@/hooks/use-auth";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useToast } from "@/hooks/use-toast";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Slider } from "@/components/ui/slider";
import { Switch } from "@/components/ui/switch";
import { Textarea } from "@/components/ui/textarea";
import { Project, TokenModel } from "@shared/schema";
import { getQueryFn, apiRequest, queryClient } from "@/lib/queryClient";
import Navbar from "@/components/navbar";
import Sidebar from "@/components/sidebar";
import { Save, PlayCircle, Sliders, RefreshCw, DollarSign, PieChart, LineChart as LineChartIcon } from "lucide-react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, AreaChart, Area } from "recharts";

export default function EconomicModelsPage() {
  const { user } = useAuth();
  const { toast } = useToast();
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [activeTab, setActiveTab] = useState("parameters");
  
  // Economic parameters
  const [stakingYield, setStakingYield] = useState(12);
  const [transactionFee, setTransactionFee] = useState(1);
  const [liquidityIncentives, setLiquidityIncentives] = useState(25);
  const [burnRate, setBurnRate] = useState(2);
  const [initialPrice, setInitialPrice] = useState(0.1);
  const [initialHolders, setInitialHolders] = useState(1000);
  const [supplyGrowth, setSupplyGrowth] = useState(5);
  const [demandGrowth, setDemandGrowth] = useState(20);
  const [volatility, setVolatility] = useState(30);
  const [enableBurning, setEnableBurning] = useState(true);
  const [simulationYears, setSimulationYears] = useState(5);
  
  // Simulation results
  const [simulationData, setSimulationData] = useState<any[]>([]);
  const [marketMetrics, setMarketMetrics] = useState({
    averagePrice: 0,
    maxPrice: 0,
    minPrice: 0,
    finalPrice: 0,
    priceGrowth: 0,
    marketCap: 0,
  });
  const [isSimulating, setIsSimulating] = useState(false);
  
  // Generate simulation data when parameters change or when run simulation is clicked
  const generateSimulationData = () => {
    setIsSimulating(true);
    
    // Create simulation data array
    const data = [];
    const months = simulationYears * 12;
    let price = initialPrice;
    let supply = 100000000; // Initial supply
    let demand = initialHolders * 1000; // Initial demand (average 1000 tokens per holder)
    let marketCap = price * supply;
    let circulatingSupply = supply * 0.2; // Assume 20% initially circulating
    
    for (let month = 0; month <= months; month++) {
      // Apply simulation effects
      const stakingEffect = (stakingYield / 100) * 0.01 * price;
      const feeEffect = (transactionFee / 100) * 0.005 * price;
      const liquidityEffect = (liquidityIncentives / 100) * 0.01 * (Math.random() * 2 - 1); // Random between -1% and 1%
      
      // Apply burning if enabled
      const burnEffect = enableBurning ? (burnRate / 100) * 0.01 * price : 0;
      
      // Apply growth rates
      const supplyGrowthEffect = (supplyGrowth / 100) / 12; // Monthly growth rate
      const demandGrowthEffect = (demandGrowth / 100) / 12; // Monthly growth rate
      
      // Apply volatility
      const volatilityEffect = ((Math.random() * 2 - 1) * volatility / 100) * price;
      
      // Calculate new values
      circulatingSupply = circulatingSupply * (1 + supplyGrowthEffect);
      demand = demand * (1 + demandGrowthEffect);
      
      // Calculate price based on supply/demand dynamics and effects
      const supplyDemandEffect = ((demand / circulatingSupply) - 1) * 0.01;
      price = price * (1 + stakingEffect - feeEffect + liquidityEffect + burnEffect + supplyDemandEffect) + volatilityEffect;
      price = Math.max(0.0001, price); // Ensure price doesn't go below a minimum
      
      // Calculate market cap
      marketCap = price * circulatingSupply;
      
      // Add data point
      data.push({
        month: month === 0 ? 'Start' : `M${month}`,
        price: parseFloat(price.toFixed(4)),
        marketCap: parseFloat((marketCap / 1000000).toFixed(2)), // In millions
        circulatingSupply: parseFloat((circulatingSupply / 1000000).toFixed(2)), // In millions
        // Add upper and lower bounds for price prediction
        upperBound: parseFloat((price * (1 + volatility / 100)).toFixed(4)),
        lowerBound: parseFloat((price * (1 - volatility / 100)).toFixed(4))
      });
    }
    
    // Calculate market metrics
    const prices = data.map(d => d.price);
    const marketCaps = data.map(d => d.marketCap);
    
    setMarketMetrics({
      averagePrice: parseFloat((prices.reduce((a, b) => a + b, 0) / prices.length).toFixed(4)),
      maxPrice: parseFloat(Math.max(...prices).toFixed(4)),
      minPrice: parseFloat(Math.min(...prices).toFixed(4)),
      finalPrice: parseFloat(prices[prices.length - 1].toFixed(4)),
      priceGrowth: parseFloat((((prices[prices.length - 1] - prices[0]) / prices[0]) * 100).toFixed(2)),
      marketCap: parseFloat(marketCaps[marketCaps.length - 1].toFixed(2))
    });
    
    setSimulationData(data);
    setIsSimulating(false);
    
    toast({
      title: "Simulation Complete",
      description: "The economic model simulation has been generated successfully.",
    });
  };

  // Effect to run simulation when component mounts
  useEffect(() => {
    generateSimulationData();
  }, []);

  const handleRunSimulation = () => {
    generateSimulationData();
  };
  
  const handleSaveModel = () => {
    // Logic to save the economic model
    toast({
      title: "Model Saved",
      description: "Your economic model has been saved successfully.",
    });
  };

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  return (
    <div className="flex h-screen overflow-hidden">
      {/* Sidebar */}
      <Sidebar isOpen={sidebarOpen} toggle={toggleSidebar} />

      {/* Main Content */}
      <div
        className={`flex-1 flex flex-col overflow-hidden transition-all duration-300 ease-in-out ${
          sidebarOpen ? "md:ml-64" : ""
        }`}
      >
        {/* Top Navigation */}
        <Navbar toggleSidebar={toggleSidebar} />

        {/* Page Content */}
        <main className="flex-1 overflow-y-auto bg-background p-6">
          <div className="mb-8">
            <div className="flex flex-col md:flex-row items-start md:items-center justify-between mb-6">
              <div>
                <h1 className="text-2xl font-bold">Economic Models</h1>
                <p className="text-gray-400 mt-1">Simulate and analyze token economics</p>
              </div>

              <div className="mt-4 md:mt-0 flex space-x-2">
                <Button 
                  className="bg-secondary hover:bg-secondary/90"
                  onClick={handleRunSimulation}
                  disabled={isSimulating}
                >
                  <PlayCircle className="mr-2 h-4 w-4" />
                  {isSimulating ? "Simulating..." : "Run Simulation"}
                </Button>
                <Button 
                  className="bg-primary hover:bg-primary/90"
                  onClick={handleSaveModel}
                >
                  <Save className="mr-2 h-4 w-4" />
                  Save Model
                </Button>
              </div>
            </div>

            <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
              <TabsList className="bg-surface border border-gray-700 p-1">
                <TabsTrigger value="parameters" className="data-[state=active]:bg-primary data-[state=active]:text-white">
                  Parameters
                </TabsTrigger>
                <TabsTrigger value="results" className="data-[state=active]:bg-primary data-[state=active]:text-white">
                  Simulation Results
                </TabsTrigger>
                <TabsTrigger value="analysis" className="data-[state=active]:bg-primary data-[state=active]:text-white">
                  Analysis
                </TabsTrigger>
              </TabsList>

              <TabsContent value="parameters" className="space-y-6">
                <Card className="bg-surface border-gray-700">
                  <CardHeader>
                    <CardTitle>Economic Parameters</CardTitle>
                    <CardDescription>Configure tokenomics parameters for simulation</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div className="space-y-4">
                        <h3 className="text-lg font-medium">Market Dynamics</h3>
                        
                        <div>
                          <Label className="text-sm font-medium mb-1">Initial Price ($)</Label>
                          <div className="flex items-center">
                            <Input
                              type="number"
                              value={initialPrice}
                              step="0.01"
                              onChange={(e) => setInitialPrice(parseFloat(e.target.value) || 0.01)}
                              className="bg-background border-gray-700 text-white"
                            />
                          </div>
                        </div>
                        
                        <div>
                          <Label className="text-sm font-medium mb-1">Initial Token Holders</Label>
                          <div className="flex items-center">
                            <Input
                              type="number"
                              value={initialHolders}
                              onChange={(e) => setInitialHolders(parseInt(e.target.value) || 100)}
                              className="bg-background border-gray-700 text-white"
                            />
                          </div>
                        </div>
                        
                        <div>
                          <Label className="text-sm font-medium mb-1">Supply Growth (% yearly)</Label>
                          <div className="flex items-center">
                            <Slider
                              value={[supplyGrowth]}
                              min={0}
                              max={50}
                              step={0.5}
                              onValueChange={(value) => setSupplyGrowth(value[0])}
                              className="flex-1"
                            />
                            <span className="ml-2 text-sm text-gray-300">{supplyGrowth}%</span>
                          </div>
                        </div>
                        
                        <div>
                          <Label className="text-sm font-medium mb-1">Demand Growth (% yearly)</Label>
                          <div className="flex items-center">
                            <Slider
                              value={[demandGrowth]}
                              min={0}
                              max={100}
                              step={1}
                              onValueChange={(value) => setDemandGrowth(value[0])}
                              className="flex-1"
                            />
                            <span className="ml-2 text-sm text-gray-300">{demandGrowth}%</span>
                          </div>
                        </div>
                        
                        <div>
                          <Label className="text-sm font-medium mb-1">Market Volatility (%)</Label>
                          <div className="flex items-center">
                            <Slider
                              value={[volatility]}
                              min={0}
                              max={100}
                              step={1}
                              onValueChange={(value) => setVolatility(value[0])}
                              className="flex-1"
                            />
                            <span className="ml-2 text-sm text-gray-300">{volatility}%</span>
                          </div>
                        </div>
                      </div>
                      
                      <div className="space-y-4">
                        <h3 className="text-lg font-medium">Tokenomics Mechanisms</h3>
                        
                        <div>
                          <Label className="text-sm font-medium mb-1">Staking Yield (% APY)</Label>
                          <div className="flex items-center">
                            <Slider
                              value={[stakingYield]}
                              min={0}
                              max={100}
                              step={1}
                              onValueChange={(value) => setStakingYield(value[0])}
                              className="flex-1"
                            />
                            <span className="ml-2 text-sm text-gray-300">{stakingYield}%</span>
                          </div>
                        </div>
                        
                        <div>
                          <Label className="text-sm font-medium mb-1">Transaction Fee (%)</Label>
                          <div className="flex items-center">
                            <Slider
                              value={[transactionFee]}
                              min={0}
                              max={10}
                              step={0.1}
                              onValueChange={(value) => setTransactionFee(value[0])}
                              className="flex-1"
                            />
                            <span className="ml-2 text-sm text-gray-300">{transactionFee}%</span>
                          </div>
                        </div>
                        
                        <div>
                          <Label className="text-sm font-medium mb-1">Liquidity Incentives (%)</Label>
                          <div className="flex items-center">
                            <Slider
                              value={[liquidityIncentives]}
                              min={0}
                              max={100}
                              step={1}
                              onValueChange={(value) => setLiquidityIncentives(value[0])}
                              className="flex-1"
                            />
                            <span className="ml-2 text-sm text-gray-300">{liquidityIncentives}%</span>
                          </div>
                        </div>
                        
                        <div className="flex items-center justify-between">
                          <Label className="text-sm font-medium">Enable Token Burning</Label>
                          <Switch
                            checked={enableBurning}
                            onCheckedChange={setEnableBurning}
                          />
                        </div>
                        
                        {enableBurning && (
                          <div>
                            <Label className="text-sm font-medium mb-1">Burn Rate (% of fees)</Label>
                            <div className="flex items-center">
                              <Slider
                                value={[burnRate]}
                                min={0}
                                max={100}
                                step={1}
                                onValueChange={(value) => setBurnRate(value[0])}
                                className="flex-1"
                              />
                              <span className="ml-2 text-sm text-gray-300">{burnRate}%</span>
                            </div>
                          </div>
                        )}
                        
                        <div>
                          <Label className="text-sm font-medium mb-1">Simulation Period (years)</Label>
                          <div className="flex items-center">
                            <Slider
                              value={[simulationYears]}
                              min={1}
                              max={10}
                              step={1}
                              onValueChange={(value) => setSimulationYears(value[0])}
                              className="flex-1"
                            />
                            <span className="ml-2 text-sm text-gray-300">{simulationYears} years</span>
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <div className="pt-4 border-t border-gray-700">
                      <Button 
                        className="w-full bg-secondary hover:bg-secondary/90"
                        onClick={handleRunSimulation}
                        disabled={isSimulating}
                      >
                        <PlayCircle className="mr-2 h-4 w-4" />
                        {isSimulating ? "Simulating..." : "Run Simulation"}
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="results" className="space-y-6">
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                  <Card className="bg-surface border-gray-700 lg:col-span-2">
                    <CardHeader>
                      <CardTitle>Token Price Simulation</CardTitle>
                      <CardDescription>Projected token price over time with volatility bounds</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="h-80">
                        <ResponsiveContainer width="100%" height="100%">
                          <LineChart
                            data={simulationData.filter((_, i) => i % 3 === 0 || i === 0)} // Show every 3 months for clarity
                            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                          >
                            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                            <XAxis dataKey="month" stroke="#9ca3af" fontSize={10} />
                            <YAxis stroke="#9ca3af" fontSize={10} />
                            <Tooltip
                              contentStyle={{ backgroundColor: '#1f2937', borderColor: '#4b5563', color: '#e5e7eb' }}
                              formatter={(value: any) => [`$${value}`, 'Price']}
                            />
                            <Legend wrapperStyle={{ fontSize: 10 }} />
                            <Line
                              type="monotone"
                              dataKey="price"
                              stroke="#3b82f6"
                              strokeWidth={2}
                              dot={false}
                              activeDot={{ r: 8 }}
                              name="Token Price"
                            />
                            <Line
                              type="monotone"
                              dataKey="upperBound"
                              stroke="#10b981"
                              strokeDasharray="3 3"
                              strokeWidth={1}
                              dot={false}
                              name="Upper Bound"
                            />
                            <Line
                              type="monotone"
                              dataKey="lowerBound"
                              stroke="#f59e0b"
                              strokeDasharray="3 3"
                              strokeWidth={1}
                              dot={false}
                              name="Lower Bound"
                            />
                          </LineChart>
                        </ResponsiveContainer>
                      </div>
                    </CardContent>
                  </Card>
                  
                  <Card className="bg-surface border-gray-700">
                    <CardHeader>
                      <CardTitle>Market Metrics</CardTitle>
                      <CardDescription>Key performance indicators</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-4">
                        <div className="bg-background rounded-md border border-gray-700 p-3">
                          <div className="flex justify-between items-center">
                            <div className="flex items-center">
                              <div className="h-8 w-8 rounded-full bg-blue-500/20 flex items-center justify-center mr-3">
                                <DollarSign className="h-4 w-4 text-blue-500" />
                              </div>
                              <div>
                                <p className="text-xs text-gray-400">Final Price</p>
                                <p className="text-lg font-semibold">${marketMetrics.finalPrice}</p>
                              </div>
                            </div>
                            <span className={`text-sm font-medium px-2 py-1 rounded-full ${
                              marketMetrics.priceGrowth >= 0 
                                ? 'bg-green-500/20 text-green-500' 
                                : 'bg-red-500/20 text-red-500'
                            }`}>
                              {marketMetrics.priceGrowth >= 0 ? '+' : ''}{marketMetrics.priceGrowth}%
                            </span>
                          </div>
                        </div>
                        
                        <div className="bg-background rounded-md border border-gray-700 p-3">
                          <div className="flex items-center">
                            <div className="h-8 w-8 rounded-full bg-purple-500/20 flex items-center justify-center mr-3">
                              <PieChart className="h-4 w-4 text-purple-500" />
                            </div>
                            <div>
                              <p className="text-xs text-gray-400">Market Cap</p>
                              <p className="text-lg font-semibold">${marketMetrics.marketCap}M</p>
                            </div>
                          </div>
                        </div>
                        
                        <div className="grid grid-cols-2 gap-3">
                          <div className="bg-background rounded-md border border-gray-700 p-3">
                            <p className="text-xs text-gray-400">Max Price</p>
                            <p className="text-lg font-semibold">${marketMetrics.maxPrice}</p>
                          </div>
                          
                          <div className="bg-background rounded-md border border-gray-700 p-3">
                            <p className="text-xs text-gray-400">Min Price</p>
                            <p className="text-lg font-semibold">${marketMetrics.minPrice}</p>
                          </div>
                          
                          <div className="bg-background rounded-md border border-gray-700 p-3">
                            <p className="text-xs text-gray-400">Avg Price</p>
                            <p className="text-lg font-semibold">${marketMetrics.averagePrice}</p>
                          </div>
                          
                          <div className="bg-background rounded-md border border-gray-700 p-3">
                            <p className="text-xs text-gray-400">Volatility</p>
                            <p className="text-lg font-semibold">{volatility}%</p>
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </div>
                
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <Card className="bg-surface border-gray-700">
                    <CardHeader>
                      <CardTitle>Market Cap Growth</CardTitle>
                      <CardDescription>Projected market capitalization over time</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="h-64">
                        <ResponsiveContainer width="100%" height="100%">
                          <AreaChart
                            data={simulationData.filter((_, i) => i % 3 === 0 || i === 0)} // Show every 3 months for clarity
                            margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
                          >
                            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                            <XAxis dataKey="month" stroke="#9ca3af" fontSize={10} />
                            <YAxis stroke="#9ca3af" fontSize={10} />
                            <Tooltip
                              contentStyle={{ backgroundColor: '#1f2937', borderColor: '#4b5563' }}
                              formatter={(value: any) => [`$${value}M`, 'Market Cap']}
                            />
                            <Area
                              type="monotone"
                              dataKey="marketCap"
                              stroke="#8b5cf6"
                              fill="#8b5cf6"
                              fillOpacity={0.3}
                              name="Market Cap"
                            />
                          </AreaChart>
                        </ResponsiveContainer>
                      </div>
                    </CardContent>
                  </Card>
                  
                  <Card className="bg-surface border-gray-700">
                    <CardHeader>
                      <CardTitle>Circulating Supply</CardTitle>
                      <CardDescription>Projected token supply in circulation</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="h-64">
                        <ResponsiveContainer width="100%" height="100%">
                          <AreaChart
                            data={simulationData.filter((_, i) => i % 3 === 0 || i === 0)} // Show every 3 months for clarity
                            margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
                          >
                            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                            <XAxis dataKey="month" stroke="#9ca3af" fontSize={10} />
                            <YAxis stroke="#9ca3af" fontSize={10} />
                            <Tooltip
                              contentStyle={{ backgroundColor: '#1f2937', borderColor: '#4b5563' }}
                              formatter={(value: any) => [`${value}M tokens`, 'Supply']}
                            />
                            <Area
                              type="monotone"
                              dataKey="circulatingSupply"
                              stroke="#ec4899"
                              fill="#ec4899"
                              fillOpacity={0.3}
                              name="Circulating Supply"
                            />
                          </AreaChart>
                        </ResponsiveContainer>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              </TabsContent>

              <TabsContent value="analysis" className="space-y-6">
                <Card className="bg-surface border-gray-700">
                  <CardHeader>
                    <CardTitle>Economic Analysis</CardTitle>
                    <CardDescription>Analysis and insights from the simulation</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <h3 className="text-lg font-medium mb-4">Simulation Insights</h3>
                        <div className="space-y-4 text-sm">
                          <div className="bg-background rounded-md border border-gray-700 p-4">
                            <h4 className="font-medium text-blue-400 mb-2">Price Trajectory</h4>
                            <p className="text-gray-300">
                              The token price {marketMetrics.priceGrowth >= 0 ? 'increased' : 'decreased'} by {Math.abs(marketMetrics.priceGrowth)}% over {simulationYears} years, with a final price of ${marketMetrics.finalPrice}. 
                              {marketMetrics.priceGrowth > 50 
                                ? ' This represents significant growth potential.'
                                : marketMetrics.priceGrowth > 0
                                  ? ' This indicates moderate growth.'
                                  : ' This suggests the model may need optimization.'
                              }
                            </p>
                          </div>
                          
                          <div className="bg-background rounded-md border border-gray-700 p-4">
                            <h4 className="font-medium text-green-400 mb-2">Supply and Demand</h4>
                            <p className="text-gray-300">
                              {supplyGrowth > demandGrowth 
                                ? 'Supply growth exceeds demand growth, which may create inflationary pressure. Consider reducing supply growth or implementing more aggressive burning mechanisms.'
                                : 'Demand growth exceeds supply growth, which should create upward price pressure over time, assuming the model parameters remain stable.'
                              }
                            </p>
                          </div>
                          
                          <div className="bg-background rounded-md border border-gray-700 p-4">
                            <h4 className="font-medium text-yellow-400 mb-2">Volatility Impact</h4>
                            <p className="text-gray-300">
                              With {volatility}% volatility, price fluctuations are 
                              {volatility > 50 
                                ? ' severe and may deter conservative investors.' 
                                : volatility > 20
                                  ? ' moderate and typical for crypto assets.'
                                  : ' relatively low compared to typical crypto assets.'
                              }
                            </p>
                          </div>
                        </div>
                      </div>
                      
                      <div>
                        <h3 className="text-lg font-medium mb-4">Recommendations</h3>
                        <div className="space-y-4 text-sm">
                          <div className="bg-background rounded-md border border-gray-700 p-4">
                            <h4 className="font-medium text-blue-400 mb-2">Tokenomics Tuning</h4>
                            {stakingYield > 20 ? (
                              <p className="text-gray-300">
                                The staking yield of {stakingYield}% is relatively high. Consider lowering it to create a more sustainable model long-term.
                              </p>
                            ) : stakingYield < 5 ? (
                              <p className="text-gray-300">
                                The staking yield of {stakingYield}% may be too low to attract stakers. Consider increasing it to improve token utility.
                              </p>
                            ) : (
                              <p className="text-gray-300">
                                The staking yield of {stakingYield}% is within a reasonable range to attract stakers while maintaining sustainability.
                              </p>
                            )}
                          </div>
                          
                          <div className="bg-background rounded-md border border-gray-700 p-4">
                            <h4 className="font-medium text-green-400 mb-2">Burning Mechanics</h4>
                            {enableBurning ? (
                              <p className="text-gray-300">
                                Token burning is enabled with {burnRate}% of fees being burned. 
                                {burnRate < 10 
                                  ? ' Consider increasing the burn rate to create stronger deflationary pressure.'
                                  : ' This should create effective deflationary pressure over time.'
                                }
                              </p>
                            ) : (
                              <p className="text-gray-300">
                                Token burning is disabled. Consider enabling burning to create deflationary pressure, especially if supply growth is high.
                              </p>
                            )}
                          </div>
                          
                          <div className="bg-background rounded-md border border-gray-700 p-4">
                            <h4 className="font-medium text-purple-400 mb-2">Liquidity Strategy</h4>
                            <p className="text-gray-300">
                              {liquidityIncentives < 10 
                                ? 'Liquidity incentives are low, which may result in lower liquidity and higher volatility. Consider increasing incentives to improve market stability.'
                                : 'Liquidity incentives are at a good level to maintain market liquidity and reduce volatility.'
                              }
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <div className="pt-4 border-t border-gray-700">
                      <h3 className="text-lg font-medium mb-4">Economic Model Notes</h3>
                      <Textarea 
                        placeholder="Add your notes about this economic model here..."
                        className="h-24 bg-background border-gray-700"
                      />
                    </div>
                    
                    <div className="flex justify-end">
                      <Button 
                        className="bg-primary hover:bg-primary/90"
                        onClick={handleSaveModel}
                      >
                        <Save className="mr-2 h-4 w-4" />
                        Save Economic Model
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          </div>
        </main>
      </div>
    </div>
  );
}