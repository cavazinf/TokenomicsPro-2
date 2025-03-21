import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useToast } from "@/hooks/use-toast";
import { Progress } from "@/components/ui/progress";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend, BarChart, Bar, XAxis, YAxis } from "recharts";

type DistributionItem = {
  name: string;
  percentage: number;
  color: string;
};

type VestingSchedule = {
  group: string;
  schedule: string;
};

export default function DistributionVesting() {
  const { toast } = useToast();
  
  // Colors for the charts
  const COLORS = ['#3b82f6', '#ec4899', '#10b981', '#f59e0b'];
  
  const [distribution, setDistribution] = useState<DistributionItem[]>([
    { name: "Team", percentage: 15, color: COLORS[0] },
    { name: "Investors", percentage: 25, color: COLORS[1] },
    { name: "Community", percentage: 40, color: COLORS[2] },
    { name: "Reserves", percentage: 20, color: COLORS[3] },
  ]);

  const [vestingSchedules, setVestingSchedules] = useState<VestingSchedule[]>([
    { group: "Team", schedule: "6 months cliff, 24 months linear" },
    { group: "Investors", schedule: "3 months cliff, 18 months linear" },
    { group: "Community", schedule: "No cliff, 12 months linear" },
  ]);
  
  // Data for the vesting chart
  const vestingData = [
    { month: 'M1', Team: 0, Investors: 0, Community: 5, Reserves: 0 },
    { month: 'M3', Team: 0, Investors: 5, Community: 5, Reserves: 0 },
    { month: 'M6', Team: 5, Investors: 5, Community: 10, Reserves: 5 },
    { month: 'M9', Team: 0, Investors: 5, Community: 5, Reserves: 5 },
    { month: 'M12', Team: 5, Investors: 5, Community: 10, Reserves: 5 },
    { month: 'M18', Team: 5, Investors: 5, Community: 5, Reserves: 5 },
  ];

  const handleCreateSchedule = () => {
    toast({
      title: "Schedule Created",
      description: "Your distribution and vesting schedule has been created.",
    });
  };

  const handleExport = () => {
    toast({
      title: "Export Complete",
      description: "Your distribution and vesting schedule has been exported.",
    });
  };

  return (
    <Card className="bg-surface border-gray-700">
      <CardHeader className="border-b border-gray-700">
        <CardTitle>Distribution & Vesting</CardTitle>
        <CardDescription className="text-gray-400">Plan token distribution and vesting schedules</CardDescription>
      </CardHeader>
      <CardContent className="p-5 space-y-6">
        <div>
          <Label className="text-sm font-medium mb-3 block">Token Distribution</Label>
          <div className="h-64 rounded-lg overflow-hidden bg-surface-light bg-opacity-50 border border-gray-700 mb-4">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={distribution}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  outerRadius={80}
                  dataKey="percentage"
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                >
                  {distribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip formatter={(value) => `${value}%`} />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
          
          {distribution.map((item) => (
            <div key={item.name} className="space-y-2 mb-3">
              <div className="flex justify-between items-center">
                <Label className="text-sm font-medium">{item.name}</Label>
                <span className="text-sm text-gray-300">{item.percentage}%</span>
              </div>
              <Progress 
                value={item.percentage} 
                className="h-2.5" 
                style={{ backgroundColor: 'rgba(255,255,255,0.1)' }}
              >
                <div 
                  className="h-full rounded-full" 
                  style={{ width: `${item.percentage}%`, backgroundColor: item.color }}
                />
              </Progress>
            </div>
          ))}
        </div>

        <div>
          <Label className="text-sm font-medium mb-3 block">Vesting Schedule</Label>
          <div className="h-64 rounded-lg overflow-hidden bg-surface-light bg-opacity-50 border border-gray-700 mb-4">
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
          
          <div className="bg-background rounded-md border border-gray-700 p-3 space-y-2">
            {vestingSchedules.map((schedule, index) => (
              <div key={schedule.group} className="flex justify-between items-center">
                <div className="flex items-center">
                  <div 
                    className="h-3 w-3 rounded-full mr-2" 
                    style={{ backgroundColor: COLORS[index % COLORS.length] }}
                  ></div>
                  <span className="text-xs">{schedule.group}</span>
                </div>
                <span className="text-xs text-gray-400">{schedule.schedule}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="flex space-x-2">
          <Button onClick={handleCreateSchedule} className="flex-1 bg-accent hover:bg-accent/90">
            Create Schedule
          </Button>
          <Button onClick={handleExport} variant="outline" className="flex-1 bg-surface-light text-white border-gray-700">
            Export
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}

function Label(props: React.HTMLAttributes<HTMLDivElement>) {
  return <div {...props} />;
}
