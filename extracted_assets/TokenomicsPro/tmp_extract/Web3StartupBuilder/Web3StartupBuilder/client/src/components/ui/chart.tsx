import React from "react";
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
  Legend,
} from "recharts";

export interface ChartData {
  name: string;
  value: number;
  color: string;
}

interface PieChartProps {
  data: ChartData[];
  innerRadius?: number;
  outerRadius?: number;
  cx?: string | number;
  cy?: string | number;
  labelLine?: boolean;
  total?: number;
  totalLabel?: string;
  showLegend?: boolean;
  width?: number | string;
  height?: number | string;
}

export const TokenPieChart: React.FC<PieChartProps> = ({
  data,
  innerRadius = "45%",
  outerRadius = "80%",
  cx = "50%",
  cy = "50%",
  labelLine = false,
  total,
  totalLabel = "Total Supply",
  showLegend = true,
  width = "100%",
  height = 400,
}) => {
  return (
    <div className="w-full chart-container relative" style={{ height }}>
      <ResponsiveContainer width={width} height="100%">
        <PieChart>
          <Pie
            data={data}
            cx={cx}
            cy={cy}
            innerRadius={innerRadius}
            outerRadius={outerRadius}
            paddingAngle={1}
            dataKey="value"
            labelLine={labelLine}
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip
            formatter={(value, name) => [`${value}%`, name]}
            contentStyle={{
              backgroundColor: "white",
              border: "1px solid #f0f0f0",
              borderRadius: "8px",
              padding: "8px 12px",
            }}
          />
          {showLegend && (
            <Legend
              layout="vertical"
              verticalAlign="middle"
              align="right"
              wrapperStyle={{ paddingLeft: "20px" }}
            />
          )}
        </PieChart>
      </ResponsiveContainer>
      {total && (
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
          <div className="text-center bg-white rounded-full p-4">
            <div className="text-lg font-bold text-dark">{total}</div>
            <div className="text-xs text-dark-50">{totalLabel}</div>
          </div>
        </div>
      )}
    </div>
  );
};

export interface BarChartData {
  name: string;
  value: number;
  color: string;
}

export const TokenBarChart = () => {
  // This is just a placeholder to satisfy the import
  // Will be implemented when needed for specific features
  return <div>Bar Chart Component</div>;
};

export interface LineChartData {
  name: string;
  value: number;
}

export const TokenLineChart = () => {
  // This is just a placeholder to satisfy the import
  // Will be implemented when needed for specific features
  return <div>Line Chart Component</div>;
};
