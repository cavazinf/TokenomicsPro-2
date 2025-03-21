import { TokenPieChart, ChartData } from "@/components/ui/chart";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface TokenDistributionProps {
  distribution?: Record<string, number>;
  totalSupply?: string;
  onEdit?: () => void;
}

export const TokenDistributionChart: React.FC<TokenDistributionProps> = ({
  distribution = {
    "Community": 31.5,
    "Team & Advisors": 25,
    "Ecosystem Growth": 15,
    "Private Sale": 20,
    "Liquidity": 8.5
  },
  totalSupply = "100M",
  onEdit
}) => {
  // Define default colors for the chart
  const colorMap: Record<string, string> = {
    "Community": "#5E8CFF",
    "Team & Advisors": "#4CAF98",
    "Ecosystem Growth": "#8A63E8",
    "Private Sale": "#FF9966",
    "Liquidity": "#FF6B6B",
    // Add fallback colors for custom categories
    "Marketing": "#6CE5E8",
    "Development": "#9B51E0",
    "Foundation": "#F2C94C",
    "Reserves": "#56CCF2",
    "Partnerships": "#BB6BD9",
    "Staking Rewards": "#27AE60",
    "Airdrops": "#F2994A",
  };

  // Convert distribution object to chart data array
  const chartData: ChartData[] = Object.entries(distribution).map(([name, value]) => ({
    name,
    value,
    color: colorMap[name] || "#CCCCCC" // Use gray for any unlisted category
  }));

  return (
    <Card>
      <CardHeader className="pb-2">
        <CardTitle className="text-xl font-semibold text-dark">Token Distribution Visualization</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex flex-col md:flex-row items-center">
          <div className="w-full md:w-1/2 p-4 flex items-center justify-center">
            <TokenPieChart 
              data={chartData}
              total={totalSupply}
              showLegend={false}
              height={300}
            />
          </div>
          
          <div className="w-full md:w-1/2 p-4">
            <div className="space-y-3">
              {chartData.map((item, index) => (
                <div key={index} className="flex items-center gap-2">
                  <span className="h-3 w-3 rounded-sm" style={{ backgroundColor: item.color }}></span>
                  <span className="text-sm">{item.name} ({item.value}%)</span>
                </div>
              ))}
            </div>
          </div>
        </div>
        
        <div className="mt-4 flex justify-end">
          <Button 
            variant="ghost" 
            className="text-sm text-primary flex items-center gap-1 hover:bg-primary-50"
            onClick={onEdit}
          >
            <span>Edit Distribution</span>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-4 w-4">
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
              <polyline points="15 3 21 3 21 9"></polyline>
              <line x1="10" y1="14" x2="21" y2="3"></line>
            </svg>
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};
