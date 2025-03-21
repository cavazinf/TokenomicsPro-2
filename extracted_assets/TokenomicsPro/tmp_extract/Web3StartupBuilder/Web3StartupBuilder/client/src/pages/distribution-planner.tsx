import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Slider } from "@/components/ui/slider";
import { ChartData, TokenPieChart } from "@/components/ui/chart";
import { PlusIcon, TrashIcon } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

export default function DistributionPlanner() {
  const { toast } = useToast();
  const [totalSupply, setTotalSupply] = useState("100M");
  
  // Define default colors for the chart
  const colorMap: Record<string, string> = {
    "Community": "#5E8CFF",
    "Team & Advisors": "#4CAF98",
    "Ecosystem Growth": "#8A63E8",
    "Private Sale": "#FF9966",
    "Liquidity": "#FF6B6B",
    "Marketing": "#6CE5E8",
    "Development": "#9B51E0",
    "Foundation": "#F2C94C",
    "Reserves": "#56CCF2",
    "Partnerships": "#BB6BD9",
    "Staking Rewards": "#27AE60",
    "Airdrops": "#F2994A",
  };

  // Initial distribution data
  const [distribution, setDistribution] = useState([
    { name: "Community", value: 31.5, color: colorMap["Community"] },
    { name: "Team & Advisors", value: 25, color: colorMap["Team & Advisors"] },
    { name: "Ecosystem Growth", value: 15, color: colorMap["Ecosystem Growth"] },
    { name: "Private Sale", value: 20, color: colorMap["Private Sale"] },
    { name: "Liquidity", value: 8.5, color: colorMap["Liquidity"] }
  ]);

  // Add a new category
  const addCategory = () => {
    // Check if we already have 12 categories (limit to prevent UI overload)
    if (distribution.length >= 12) {
      toast({
        title: "Maximum categories reached",
        description: "You can have a maximum of 12 token distribution categories.",
        variant: "destructive",
      });
      return;
    }
    
    // Find a color that isn't used
    const usedColors = distribution.map(item => item.color);
    const availableColors = Object.values(colorMap).filter(color => !usedColors.includes(color));
    
    // Get available categories
    const usedCategories = distribution.map(item => item.name);
    const availableCategories = Object.keys(colorMap).filter(name => !usedCategories.includes(name));
    
    // Default to first available or use a generic one
    const newCategoryName = availableCategories[0] || "New Category";
    const newColor = availableColors[0] || "#CCCCCC";
    
    // Calculate default value for new category - distribute from existing
    const existingTotal = distribution.reduce((sum, item) => sum + item.value, 0);
    let newValue = 0;
    let updatedDistribution = [...distribution];
    
    if (existingTotal >= 100) {
      // Take some percentage from other categories
      newValue = 5;
      const reductionFactor = (existingTotal - newValue) / existingTotal;
      updatedDistribution = distribution.map(item => ({
        ...item,
        value: parseFloat((item.value * reductionFactor).toFixed(1))
      }));
    } else {
      // Use remaining percentage
      newValue = parseFloat((100 - existingTotal).toFixed(1));
    }
    
    setDistribution([
      ...updatedDistribution,
      { name: newCategoryName, value: newValue, color: newColor }
    ]);
  };

  // Remove a category
  const removeCategory = (index: number) => {
    if (distribution.length <= 1) {
      toast({
        title: "Cannot remove category",
        description: "You must have at least one category in your distribution.",
        variant: "destructive",
      });
      return;
    }
    
    const removedValue = distribution[index].value;
    const newDistribution = distribution.filter((_, i) => i !== index);
    
    // Redistribute the removed value proportionally
    const remainingTotal = newDistribution.reduce((sum, item) => sum + item.value, 0);
    
    if (remainingTotal > 0) {
      const redistributeFactor = (remainingTotal + removedValue) / remainingTotal;
      const updatedDistribution = newDistribution.map(item => ({
        ...item,
        value: parseFloat((item.value * redistributeFactor).toFixed(1))
      }));
      setDistribution(updatedDistribution);
    } else {
      // If all categories had 0, just give the removed value to the first category
      if (newDistribution.length > 0) {
        newDistribution[0].value = removedValue;
      }
      setDistribution(newDistribution);
    }
  };

  // Update category name
  const updateCategoryName = (index: number, newName: string) => {
    const newDistribution = [...distribution];
    newDistribution[index].name = newName;
    setDistribution(newDistribution);
  };

  // Update category percentage using slider
  const updateCategoryValue = (index: number, newValue: number) => {
    const currentTotal = distribution.reduce((sum, item, i) => sum + (i === index ? 0 : item.value), 0);
    const maxPossibleValue = 100 - currentTotal;
    
    // Ensure the new value doesn't exceed what's available
    const adjustedValue = Math.min(newValue, maxPossibleValue);
    
    const newDistribution = [...distribution];
    newDistribution[index].value = adjustedValue;
    setDistribution(newDistribution);
  };

  // Calculate the current total
  const currentTotal = distribution.reduce((sum, item) => sum + item.value, 0);
  const isValid = Math.abs(currentTotal - 100) < 0.1; // Allow for small floating point errors

  // Save distribution plan
  const saveDistribution = () => {
    if (!isValid) {
      toast({
        title: "Invalid distribution",
        description: "Your distribution must add up to exactly 100%.",
        variant: "destructive",
      });
      return;
    }
    
    toast({
      title: "Distribution saved",
      description: "Your token distribution plan has been saved successfully."
    });
    
    // Here you would typically save to the backend
    // For now we just show a success message
  };

  return (
    <div className="max-w-5xl mx-auto">
      <header className="mb-8">
        <h1 className="text-2xl md:text-3xl font-bold text-dark">Distribution Planner</h1>
        <p className="text-dark-50 mt-2">Plan how your tokens will be distributed across different stakeholder groups</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Token Allocation</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="mb-4">
              <Label htmlFor="totalSupply">Total Token Supply</Label>
              <Input 
                id="totalSupply" 
                value={totalSupply}
                onChange={(e) => setTotalSupply(e.target.value)}
                className="mt-1"
              />
            </div>
            
            <div className="mb-4 text-sm text-muted-foreground">
              Allocate percentages to different stakeholder groups. The total must equal 100%.
            </div>
            
            <div className="space-y-6 max-h-[400px] overflow-y-auto pr-2">
              {distribution.map((category, index) => (
                <div key={index} className="space-y-2 pb-4 border-b">
                  <div className="flex justify-between items-center">
                    <div className="flex items-center gap-2">
                      <div 
                        className="w-3 h-3 rounded-sm" 
                        style={{ backgroundColor: category.color }}
                      ></div>
                      <Input 
                        value={category.name}
                        onChange={(e) => updateCategoryName(index, e.target.value)}
                        className="w-full max-w-[200px]"
                      />
                    </div>
                    <Button 
                      variant="ghost" 
                      size="sm" 
                      onClick={() => removeCategory(index)}
                      className="h-8 w-8 p-0"
                    >
                      <TrashIcon className="h-4 w-4" />
                    </Button>
                  </div>
                  <div className="flex items-center gap-4">
                    <Slider 
                      value={[category.value]} 
                      min={0} 
                      max={100} 
                      step={0.1}
                      className="flex-1"
                      onValueChange={(vals) => updateCategoryValue(index, vals[0])}
                    />
                    <div className="w-12 text-right">
                      {category.value.toFixed(1)}%
                    </div>
                  </div>
                </div>
              ))}
            </div>
            
            <div className="mt-6 flex justify-between items-center">
              <Button 
                onClick={addCategory} 
                variant="outline" 
                className="flex items-center gap-1"
              >
                <PlusIcon className="h-4 w-4" /> Add Category
              </Button>
              <div className={`font-medium ${isValid ? 'text-green-600' : 'text-red-600'}`}>
                Total: {currentTotal.toFixed(1)}%
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader>
            <CardTitle>Distribution Visualization</CardTitle>
          </CardHeader>
          <CardContent>
            <TokenPieChart 
              data={distribution}
              total={totalSupply}
              height={350}
            />
            
            <Button 
              className="w-full mt-6"
              onClick={saveDistribution}
              disabled={!isValid}
            >
              Save Distribution Plan
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
