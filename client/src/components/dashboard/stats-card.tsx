import { Card } from "@/components/ui/card";
import { ArrowUp } from "lucide-react";

type StatsCardProps = {
  title: string;
  value: string | number;
  change: string;
  changeType: "positive" | "warning";
  icon: React.ReactNode;
  iconColor: string;
  iconBgColor: string;
};

export default function StatsCard({
  title,
  value,
  change,
  changeType,
  icon,
  iconColor,
  iconBgColor,
}: StatsCardProps) {
  return (
    <Card className="bg-surface rounded-lg p-5 border border-gray-700">
      <div className="flex justify-between items-start">
        <div>
          <p className="text-gray-400 text-sm">{title}</p>
          <h3 className="text-2xl font-bold mt-2">{value}</h3>
          <p className={`flex items-center text-xs ${changeType === "positive" ? "text-success" : "text-warning"} mt-1`}>
            <ArrowUp className="h-3 w-3 mr-1" />
            {change}
          </p>
        </div>
        <div className={`p-2 ${iconBgColor} rounded-md`}>
          <div className={`text-xl ${iconColor}`}>{icon}</div>
        </div>
      </div>
    </Card>
  );
}
