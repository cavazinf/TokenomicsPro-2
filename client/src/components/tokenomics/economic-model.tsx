import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useToast } from "@/hooks/use-toast";
import { BarChart3 } from "lucide-react";
import { Slider } from "@/components/ui/slider";

export default function EconomicModel() {
  const { toast } = useToast();
  const [stakingYield, setStakingYield] = useState(12);
  const [transactionFee, setTransactionFee] = useState(1);
  const [liquidityIncentives, setLiquidityIncentives] = useState(25);
  const [initialPrice, setInitialPrice] = useState("$0.10");
  const [supplyGrowth, setSupplyGrowth] = useState("5% yearly");

  const handleRunSimulation = () => {
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

        <div className="h-32 rounded-lg flex items-center justify-center bg-surface-light bg-opacity-50 border border-gray-700">
          <div className="text-center">
            <BarChart3 className="h-8 w-8 mx-auto text-gray-400 mb-2" />
            <p className="text-sm text-gray-400">Token price simulation graph</p>
          </div>
        </div>

        <Button onClick={handleRunSimulation} className="w-full bg-secondary hover:bg-secondary/90">
          Run Simulation
        </Button>
      </CardContent>
    </Card>
  );
}
