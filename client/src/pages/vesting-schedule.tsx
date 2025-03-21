import React, { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Slider } from "@/components/ui/slider";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';

interface VestingCategory {
  name: string;
  percentage: number;
  color: string;
  cliff: number; // in months
  vesting: number; // in months
  tgeUnlock: number; // percentage unlocked at Token Generation Event
}

export default function VestingSchedule() {
  const [totalSupply, setTotalSupply] = useState(100000000);
  const [categories, setCategories] = useState<VestingCategory[]>([
    { name: "Team", percentage: 15, color: "#4f46e5", cliff: 12, vesting: 36, tgeUnlock: 0 },
    { name: "Investors", percentage: 25, color: "#0ea5e9", cliff: 6, vesting: 24, tgeUnlock: 10 },
    { name: "Community", percentage: 20, color: "#10b981", cliff: 0, vesting: 12, tgeUnlock: 20 },
    { name: "Treasury", percentage: 15, color: "#f59e0b", cliff: 3, vesting: 36, tgeUnlock: 5 },
    { name: "Ecosystem", percentage: 25, color: "#ef4444", cliff: 0, vesting: 48, tgeUnlock: 15 },
  ]);
  const [vestingData, setVestingData] = useState<any[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<number | null>(null);

  useEffect(() => {
    calculateVestingSchedule();
  }, [categories, totalSupply]);

  const calculateVestingSchedule = () => {
    // Find the longest vesting period to determine total months to simulate
    const maxVestingPeriod = Math.max(...categories.map(cat => cat.cliff + cat.vesting)) + 1;
    
    // Initialize data structure for each month
    const monthlyData = Array(maxVestingPeriod).fill(0).map((_, month) => ({
      month,
      totalReleased: 0,
      totalUnlocked: 0,
      ...categories.reduce((acc, cat) => {
        acc[`${cat.name}_released`] = 0;
        acc[`${cat.name}_unlocked`] = 0;
        acc[`${cat.name}_cumulative`] = 0;
        return acc;
      }, {} as Record<string, number>),
    }));

    // Calculate tokens released per month for each category
    categories.forEach(category => {
      const { name, percentage, cliff, vesting, tgeUnlock } = category;
      const totalTokens = totalSupply * (percentage / 100);
      
      // Tokens released at TGE (month 0)
      const tgeTokens = totalTokens * (tgeUnlock / 100);
      monthlyData[0][`${name}_released`] = tgeTokens;
      monthlyData[0][`${name}_unlocked`] = tgeTokens;
      monthlyData[0][`${name}_cumulative`] = tgeTokens;
      monthlyData[0].totalReleased += tgeTokens;
      monthlyData[0].totalUnlocked += tgeTokens;

      // Remaining tokens to be vested
      const remainingTokens = totalTokens - tgeTokens;
      
      // If there's no vesting period, all tokens are released after cliff
      if (vesting === 0) {
        if (cliff > 0 && cliff < monthlyData.length) {
          monthlyData[cliff][`${name}_released`] = remainingTokens;
          monthlyData[cliff][`${name}_unlocked`] = remainingTokens;
          monthlyData[cliff][`${name}_cumulative`] = totalTokens;
          monthlyData[cliff].totalReleased += remainingTokens;
          monthlyData[cliff].totalUnlocked += remainingTokens;
        }
        return;
      }

      // Calculate linear vesting after cliff period
      const monthlyRelease = remainingTokens / vesting;
      
      for (let month = cliff + 1; month <= cliff + vesting && month < monthlyData.length; month++) {
        monthlyData[month][`${name}_released`] = monthlyRelease;
        monthlyData[month][`${name}_unlocked`] = monthlyRelease;
        
        // Update cumulative amounts
        monthlyData[month][`${name}_cumulative`] = 
          monthlyData[month-1][`${name}_cumulative`] + monthlyRelease;
        
        monthlyData[month].totalReleased += monthlyRelease;
        monthlyData[month].totalUnlocked += monthlyRelease;
      }
    });

    // Calculate cumulative totals
    for (let month = 1; month < monthlyData.length; month++) {
      monthlyData[month].totalReleased += monthlyData[month-1].totalReleased;
    }

    setVestingData(monthlyData);
  };

  const handleCategorySelect = (index: number) => {
    setSelectedCategory(selectedCategory === index ? null : index);
  };

  const handleCategoryChange = (index: number, field: keyof VestingCategory, value: number | string) => {
    const newCategories = [...categories];
    
    if (field === 'name') {
      newCategories[index][field] = value as string;
    } else {
      newCategories[index][field] = value as number;
    }
    
    setCategories(newCategories);
  };

  // Format number with appropriate prefix (K, M, B)
  const formatNumber = (num: number) => {
    if (num >= 1000000000) {
      return (num / 1000000000).toFixed(1) + 'B';
    }
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M';
    }
    if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K';
    }
    return num.toFixed(2);
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight">Vesting Schedule</h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-1">
          <CardHeader>
            <CardTitle>Vesting Configuration</CardTitle>
            <CardDescription>Configure token release schedules</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="totalSupply">Total Supply</Label>
              <Input 
                id="totalSupply" 
                type="number" 
                value={totalSupply} 
                onChange={(e) => setTotalSupply(Number(e.target.value))}
              />
            </div>

            <div className="space-y-3">
              <Label>Token Categories</Label>
              {categories.map((category, index) => (
                <div 
                  key={index} 
                  className={`p-3 border rounded-md cursor-pointer ${
                    selectedCategory === index ? 'border-primary' : ''
                  }`}
                  onClick={() => handleCategorySelect(index)}
                >
                  <div className="flex items-center mb-2">
                    <div 
                      className="w-4 h-4 rounded-full mr-2" 
                      style={{ backgroundColor: category.color }}
                    />
                    <div className="flex-1 font-medium">{category.name}</div>
                    <div className="text-sm">{category.percentage}%</div>
                  </div>
                  <div className="text-sm text-gray-400">
                    {(totalSupply * category.percentage / 100).toLocaleString()} tokens
                  </div>
                  {selectedCategory === index && (
                    <div className="mt-3 space-y-3 pt-3 border-t">
                      <div className="space-y-2">
                        <Label>Category Name</Label>
                        <Input 
                          value={category.name} 
                          onChange={(e) => handleCategoryChange(index, 'name', e.target.value)}
                        />
                      </div>

                      <div className="space-y-2">
                        <div className="flex justify-between">
                          <Label>Allocation (%)</Label>
                          <span>{category.percentage}%</span>
                        </div>
                        <Slider 
                          value={[category.percentage]} 
                          max={100} 
                          step={1}
                          onValueChange={(values) => handleCategoryChange(index, 'percentage', values[0])}
                        />
                      </div>

                      <div className="space-y-2">
                        <div className="flex justify-between">
                          <Label>Cliff Period (months)</Label>
                          <span>{category.cliff}</span>
                        </div>
                        <Slider 
                          value={[category.cliff]} 
                          max={36} 
                          step={1}
                          onValueChange={(values) => handleCategoryChange(index, 'cliff', values[0])}
                        />
                      </div>

                      <div className="space-y-2">
                        <div className="flex justify-between">
                          <Label>Vesting Period (months)</Label>
                          <span>{category.vesting}</span>
                        </div>
                        <Slider 
                          value={[category.vesting]} 
                          max={60} 
                          step={1}
                          onValueChange={(values) => handleCategoryChange(index, 'vesting', values[0])}
                        />
                      </div>

                      <div className="space-y-2">
                        <div className="flex justify-between">
                          <Label>TGE Unlock (%)</Label>
                          <span>{category.tgeUnlock}%</span>
                        </div>
                        <Slider 
                          value={[category.tgeUnlock]} 
                          max={100} 
                          step={1}
                          onValueChange={(values) => handleCategoryChange(index, 'tgeUnlock', values[0])}
                        />
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Token Release Schedule</CardTitle>
            <CardDescription>Projected token unlocks over time</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[400px]">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart
                  data={vestingData}
                  margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="month" 
                    label={{ value: 'Month', position: 'insideBottom', offset: -5 }}
                  />
                  <YAxis 
                    tickFormatter={(value) => formatNumber(value)}
                    label={{ value: 'Tokens Released', angle: -90, position: 'insideLeft' }}
                  />
                  <Tooltip 
                    formatter={(value: number, name: string) => {
                      if (name === 'totalReleased') return [formatNumber(value), 'Total Released'];
                      const catName = name.split('_')[0];
                      return [formatNumber(value), `${catName} Cumulative`];
                    }}
                    labelFormatter={(label) => `Month ${label}`}
                  />
                  <Legend />
                  {categories.map((category, index) => (
                    <Area
                      key={index}
                      type="monotone"
                      dataKey={`${category.name}_cumulative`}
                      name={`${category.name} Cumulative`}
                      stroke={category.color}
                      fill={category.color}
                      stackId="1"
                      fillOpacity={0.6}
                    />
                  ))}
                  <Line
                    type="monotone"
                    dataKey="totalReleased"
                    name="Total Released"
                    stroke="#111827"
                    activeDot={{ r: 8 }}
                    dot={false}
                    strokeWidth={2}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>

            <div className="mt-6">
              <h3 className="text-lg font-medium mb-2">Release Schedule Table</h3>
              <div className="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Month</TableHead>
                      {categories.map((cat, index) => (
                        <TableHead key={index}>{cat.name}</TableHead>
                      ))}
                      <TableHead>Total Released</TableHead>
                      <TableHead>% of Supply</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {vestingData.filter((_, i) => i % 3 === 0 || i === vestingData.length - 1).map((data, index) => (
                      <TableRow key={index}>
                        <TableCell>{data.month}</TableCell>
                        {categories.map((cat, catIndex) => (
                          <TableCell key={catIndex}>
                            {formatNumber(data[`${cat.name}_cumulative`])}
                          </TableCell>
                        ))}
                        <TableCell className="font-medium">
                          {formatNumber(data.totalReleased)}
                        </TableCell>
                        <TableCell>
                          {((data.totalReleased / totalSupply) * 100).toFixed(1)}%
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}