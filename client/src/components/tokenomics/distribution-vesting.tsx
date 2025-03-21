import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useToast } from "@/hooks/use-toast";
import { Progress } from "@/components/ui/progress";

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
  
  const [distribution, setDistribution] = useState<DistributionItem[]>([
    { name: "Team", percentage: 15, color: "bg-primary" },
    { name: "Investors", percentage: 25, color: "bg-secondary" },
    { name: "Community", percentage: 40, color: "bg-accent" },
    { name: "Reserves", percentage: 20, color: "bg-warning" },
  ]);

  const [vestingSchedules, setVestingSchedules] = useState<VestingSchedule[]>([
    { group: "Team", schedule: "6 months cliff, 24 months linear" },
    { group: "Investors", schedule: "3 months cliff, 18 months linear" },
    { group: "Community", schedule: "No cliff, 12 months linear" },
  ]);

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
      <CardContent className="p-5 space-y-4">
        {distribution.map((item) => (
          <div key={item.name} className="space-y-3">
            <div className="flex justify-between items-center">
              <Label className="text-sm font-medium">{item.name}</Label>
              <span className="text-sm text-gray-300">{item.percentage}%</span>
            </div>
            <Progress value={item.percentage} className={`h-2.5 ${item.color}`} />
          </div>
        ))}

        <div className="pt-2">
          <Label className="text-sm font-medium mb-2">Vesting Schedule</Label>
          <div className="bg-background rounded-md border border-gray-700 p-3 space-y-2">
            {vestingSchedules.map((schedule) => (
              <div key={schedule.group} className="flex justify-between items-center">
                <span className="text-xs">{schedule.group}</span>
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
