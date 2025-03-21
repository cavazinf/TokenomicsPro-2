import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useToast } from "@/hooks/use-toast";
import { Slider } from "@/components/ui/slider";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";

export default function EconomicModel() {
  const { toast } = useToast();
  const [stakingYield, setStakingYield] = useState(12);
  const [transactionFee, setTransactionFee] = useState(1);
  const [liquidityIncentives, setLiquidityIncentives] = useState(25);
  const [initialPrice, setInitialPrice] = useState("$0.10");
  const [supplyGrowth, setSupplyGrowth] = useState("5% yearly");
  const [simulationData, setSimulationData] = useState<any[]>([]);

  // Generate simulation data when parameters change
  useEffect(() => {
    generateSimulationData();
  }, [stakingYield, transactionFee, liquidityIncentives]);

  const generateSimulationData = () => {
    // Parse initial price to get a starting value
    const startPrice = parseFloat(initialPrice.replace('$', '')) || 0.1;
    
    // Generate simulation data based on parameters
    const data = [];
    let price = startPrice;
    
    for (let month = 1; month <= 24; month++) {
      // Simple simulation algorithm:
      // - Higher staking yield increases price over time
      // - Transaction fees slightly decrease growth
      // - Liquidity incentives help stabilize volatility
      const stakingEffect = (stakingYield / 100) * 0.01 * month;
      const feeEffect = (transactionFee / 100) * 0.005 * month;
      const liquidityEffect = (liquidityIncentives / 200) * (Math.random() > 0.5 ? 1 : -0.5);
      
      // Add some randomness for realistic simulation
      const randomFactor = Math.random() * 0.05 - 0.025;
      
      // Calculate new price with effects
      price = price * (1 + stakingEffect - feeEffect + liquidityEffect + randomFactor);
      
      // Add some volatility but keep the trend
      const volatility = Math.random() * 0.1 - 0.05;
      const marketPrice = price * (1 + volatility);
      
      data.push({
        month: `M${month}`,
        price: parseFloat(marketPrice.toFixed(4)),
        // Add predictive high/low bounds
        predicted: parseFloat((marketPrice * (1 + 0.1)).toFixed(4)),
        lower: parseFloat((marketPrice * (1 - 0.1)).toFixed(4))
      });
    }
    
    setSimulationData(data);
  };

  const handleRunSimulation = () => {
    generateSimulationData();
    
    toast({
      title: "Simulation Running",
      description: "Your economic model simulation is being processed.",
    });
  };

  return (
    <Card className="bg-surface border-gray-700">
      <CardHeader className="border-b border-gray-700">
        <CardTitle>Economic Simulation</CardTitle>
        <CardDescription className="text-gray-400">Model token economics and simulate behavior</CardDescription>
      </CardHeader>
      <CardContent className="p-5 space-y-4">
        <div>
          <Label className="text-sm font-medium mb-1">Staking Yield</Label>
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
          <Label className="text-sm font-medium mb-1">Transaction Fee</Label>
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
          <Label className="text-sm font-medium mb-1">Liquidity Incentives</Label>
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

        <div>
          <Label className="text-sm font-medium mb-1">Market Parameters</Label>
          <div className="grid grid-cols-2 gap-2">
            <div>
              <Label className="block text-xs text-gray-400 mb-1">Initial Price</Label>
              <Input
                type="text"
                value={initialPrice}
                onChange={(e) => setInitialPrice(e.target.value)}
                className="w-full bg-background text-white border-gray-700 text-sm"
              />
            </div>
            <div>
              <Label className="block text-xs text-gray-400 mb-1">Supply Growth</Label>
              <Input
                type="text"
                value={supplyGrowth}
                onChange={(e) => setSupplyGrowth(e.target.value)}
                className="w-full bg-background text-white border-gray-700 text-sm"
              />
            </div>
          </div>
        </div>

        <div className="h-64 rounded-lg bg-surface-light bg-opacity-50 border border-gray-700">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={simulationData}
              margin={{
                top: 10,
                right: 30,
                left: 0,
                bottom: 10,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis dataKey="month" tick={{ fontSize: 10, fill: "#9ca3af" }} />
              <YAxis tick={{ fontSize: 10, fill: "#9ca3af" }} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#1f2937', borderColor: '#4b5563' }}
                labelStyle={{ color: '#e5e7eb' }}
                formatter={(value) => [`$${value}`, 'Price']}
              />
              <Legend />
              <Line
                type="monotone"
                dataKey="price"
                stroke="#3b82f6"
                activeDot={{ r: 8 }}
                name="Token Price"
              />
              <Line 
                type="monotone" 
                dataKey="predicted" 
                stroke="#10b981" 
                strokeDasharray="5 5" 
                name="Predicted Ceiling" 
              />
              <Line 
                type="monotone" 
                dataKey="lower" 
                stroke="#f59e0b" 
                strokeDasharray="5 5" 
                name="Predicted Floor" 
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <Button onClick={handleRunSimulation} className="w-full bg-secondary hover:bg-secondary/90">
          Run Simulation
        </Button>
      </CardContent>
    </Card>
  );
}
