import React from "react";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from "recharts";

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
  innerRadius = 0,
  outerRadius = 80,
  cx = "50%",
  cy = "50%",
  labelLine = false,
  total,
  totalLabel = "Total",
  showLegend = false,
  width = "100%",
  height = "100%",
}) => {
  const renderCustomizedLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent, index }: any) => {
    const RADIAN = Math.PI / 180;
    const radius = 25 + innerRadius + (outerRadius - innerRadius) * 0.5;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);

    return (
      <text
        x={x}
        y={y}
        fill="white"
        textAnchor={x > cx ? "start" : "end"}
        dominantBaseline="central"
        fontSize={12}
      >
        {`${(percent * 100).toFixed(0)}%`}
      </text>
    );
  };

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const dataItem = payload[0].payload;
      return (
        <div className="custom-tooltip bg-background p-2 border border-gray-700 rounded-md shadow-md">
          <p className="label text-sm font-medium">{dataItem.name}</p>
          <p className="value text-sm">
            {dataItem.value} ({((dataItem.value / data.reduce((sum, item) => sum + item.value, 0)) * 100).toFixed(1)}%)
          </p>
          {total && (
            <p className="absolute-value text-xs text-gray-400">
              {total ? ((dataItem.value / 100) * total).toLocaleString() : "-"}
            </p>
          )}
        </div>
      );
    }
    return null;
  };

  return (
    <ResponsiveContainer width={width} height={height}>
      <PieChart>
        <Pie
          data={data}
          cx={cx}
          cy={cy}
          labelLine={labelLine}
          label={renderCustomizedLabel}
          outerRadius={outerRadius}
          innerRadius={innerRadius}
          dataKey="value"
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={entry.color} />
          ))}
        </Pie>
        <Tooltip content={<CustomTooltip />} />
        {showLegend && (
          <Legend
            layout="vertical"
            verticalAlign="middle"
            align="right"
            wrapperStyle={{ fontSize: "12px" }}
          />
        )}
        {innerRadius > 0 && total && (
          <text
            x={typeof cx === "string" ? "50%" : cx}
            y={typeof cy === "string" ? "50%" : cy}
            textAnchor="middle"
            dominantBaseline="middle"
          >
            <tspan x={typeof cx === "string" ? "50%" : cx} dy="-0.5em" fontSize="12" fill="#9ca3af">
              {totalLabel}
            </tspan>
            <tspan x={typeof cx === "string" ? "50%" : cx} dy="1.2em" fontSize="14" fontWeight="bold" fill="white">
              {total.toLocaleString()}
            </tspan>
          </text>
        )}
      </PieChart>
    </ResponsiveContainer>
  );
};

export interface BarChartData {
  name: string;
  value: number;
  color: string;
}

export interface LineChartData {
  name: string;
  value: number;
}