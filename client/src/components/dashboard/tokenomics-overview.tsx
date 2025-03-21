import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { BarChart2, PieChart, RefreshCw, MoreHorizontal } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function TokenomicsOverview() {
  const distributionData = [
    { category: "Team", percentage: 15, color: "bg-primary" },
    { category: "Investors", percentage: 25, color: "bg-secondary" },
    { category: "Community", percentage: 40, color: "bg-accent" },
    { category: "Reserves", percentage: 20, color: "bg-warning" },
  ];

  return (
    <Card className="bg-surface rounded-lg border border-gray-700">
      <CardHeader className="p-5 border-b border-gray-700">
        <div className="flex justify-between">
          <CardTitle>Tokenomics Overview</CardTitle>
          <div className="flex space-x-2">
            <Button variant="ghost" size="sm" className="text-sm text-gray-400 hover:bg-surface-light">
              <RefreshCw className="h-4 w-4 mr-1" />
              Refresh
            </Button>
            <Button variant="ghost" size="sm" className="text-sm text-gray-400 hover:bg-surface-light">
              <MoreHorizontal className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </CardHeader>

      <CardContent className="p-5">
        <div className="flex flex-col lg:flex-row">
          <div className="w-full lg:w-1/2 mb-4 lg:mb-0">
            <h3 className="text-sm font-medium mb-3">Token Distribution</h3>
            <div className="h-48 rounded-lg overflow-hidden flex items-center justify-center bg-surface-light bg-opacity-50 border border-gray-700">
              <div className="text-center">
                <div className="p-2 rounded-full bg-background/40 inline-block mb-2">
                  <PieChart className="h-6 w-6 text-gray-300" />
                </div>
                <p className="text-sm text-gray-400">Interactive pie chart showing token distribution</p>
              </div>
            </div>
            <div className="mt-4 grid grid-cols-2 gap-2">
              {distributionData.map((item) => (
                <div key={item.category} className="flex items-center">
                  <div className={`h-3 w-3 rounded-full ${item.color} mr-2`}></div>
                  <span className="text-xs">
                    {item.category} ({item.percentage}%)
                  </span>
                </div>
              ))}
            </div>
          </div>

          <div className="w-full lg:w-1/2 lg:pl-4">
            <h3 className="text-sm font-medium mb-3">Vesting Schedule</h3>
            <div className="h-48 rounded-lg overflow-hidden flex items-center justify-center bg-surface-light bg-opacity-50 border border-gray-700">
              <div className="text-center">
                <div className="p-2 rounded-full bg-background/40 inline-block mb-2">
                  <BarChart2 className="h-6 w-6 text-gray-300" />
                </div>
                <p className="text-sm text-gray-400">Interactive bar chart showing vesting timeline</p>
              </div>
            </div>
            <div className="mt-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs">Total Supply</span>
                <span className="text-xs font-medium">100,000,000 Tokens</span>
              </div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs">Circulating Supply</span>
                <span className="text-xs font-medium">23,500,000 Tokens (23.5%)</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-xs">Next Token Release</span>
                <span className="text-xs font-medium">5,000,000 in 14 days</span>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
