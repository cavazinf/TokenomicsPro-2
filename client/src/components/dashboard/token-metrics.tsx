import React from 'react';
import { Button } from "@/components/ui/button";
import { Plus } from 'lucide-react';

interface TokenMetric {
  label: string;
  value: string;
  icon: React.ReactNode;
  bgColor: string;
  iconColor: string;
}

interface TokenMetricsProps {
  metrics?: TokenMetric[];
  onAddMetric?: () => void;
}

export const TokenMetrics: React.FC<TokenMetricsProps> = ({
  metrics = [],
  onAddMetric,
}) => {
  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {metrics.map((metric, index) => (
          <div
            key={index}
            className="p-4 rounded-md border border-surface-border flex items-center space-x-4"
          >
            <div className={`p-2 rounded-full ${metric.bgColor}`}>
              <div className={`${metric.iconColor}`}>{metric.icon}</div>
            </div>
            <div>
              <div className="text-sm text-gray-400">{metric.label}</div>
              <div className="font-semibold">{metric.value}</div>
            </div>
          </div>
        ))}

        {onAddMetric && (
          <Button
            variant="outline"
            className="border-dashed h-full min-h-[80px] flex-col"
            onClick={onAddMetric}
          >
            <Plus className="h-5 w-5 mb-1" />
            Add Metric
          </Button>
        )}

        {metrics.length === 0 && !onAddMetric && (
          <div className="col-span-3 p-4 text-center text-gray-400 text-sm">
            No token metrics available
          </div>
        )}
      </div>
    </div>
  );
};