import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { RefreshCw, MoreHorizontal } from "lucide-react";
import { Button } from "@/components/ui/button";
import { PieChart, Pie, BarChart, Bar, XAxis, YAxis, Tooltip, Cell, ResponsiveContainer, Legend } from "recharts";

export default function TokenomicsOverview() {
  const COLORS = ['#3b82f6', '#ec4899', '#10b981', '#f59e0b'];

  const distributionData = [
    { name: "Team", value: 15, color: COLORS[0] },
    { name: "Investors", value: 25, color: COLORS[1] },
    { name: "Community", value: 40, color: COLORS[2] },
    { name: "Reserves", value: 20, color: COLORS[3] },
  ];

  const vestingData = [
    { month: 'M1', Team: 0, Investors: 0, Community: 5, Reserves: 0 },
    { month: 'M3', Team: 0, Investors: 5, Community: 5, Reserves: 0 },
    { month: 'M6', Team: 5, Investors: 5, Community: 10, Reserves: 5 },
    { month: 'M9', Team: 0, Investors: 5, Community: 5, Reserves: 5 },
    { month: 'M12', Team: 5, Investors: 5, Community: 10, Reserves: 5 },
    { month: 'M18', Team: 5, Investors: 5, Community: 5, Reserves: 5 },
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
            <div className="h-48 rounded-lg overflow-hidden bg-surface-light bg-opacity-50 border border-gray-700">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={distributionData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    outerRadius={60}
                    dataKey="value"
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  >
                    {distributionData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value) => `${value}%`} />
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div className="mt-4 grid grid-cols-2 gap-2">
              {distributionData.map((item) => (
                <div key={item.name} className="flex items-center">
                  <div style={{ backgroundColor: item.color }} className="h-3 w-3 rounded-full mr-2"></div>
                  <span className="text-xs">
                    {item.name} ({item.value}%)
                  </span>
                </div>
              ))}
            </div>
          </div>

          <div className="w-full lg:w-1/2 lg:pl-4">
            <h3 className="text-sm font-medium mb-3">Vesting Schedule</h3>
            <div className="h-48 rounded-lg overflow-hidden bg-surface-light bg-opacity-50 border border-gray-700">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={vestingData}>
                  <XAxis dataKey="month" tick={{ fontSize: 10 }} />
                  <YAxis tick={{ fontSize: 10 }} />
                  <Tooltip />
                  <Legend wrapperStyle={{ fontSize: '9px' }} />
                  <Bar dataKey="Team" stackId="a" fill={COLORS[0]} />
                  <Bar dataKey="Investors" stackId="a" fill={COLORS[1]} />
                  <Bar dataKey="Community" stackId="a" fill={COLORS[2]} />
                  <Bar dataKey="Reserves" stackId="a" fill={COLORS[3]} />
                </BarChart>
              </ResponsiveContainer>
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
