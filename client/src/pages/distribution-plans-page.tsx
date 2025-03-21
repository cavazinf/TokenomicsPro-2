import { useState } from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { useAuth } from "@/hooks/use-auth";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useToast } from "@/hooks/use-toast";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { DistributionPlan, InsertDistributionPlan, Project, TokenModel } from "@shared/schema";
import { getQueryFn, apiRequest, queryClient } from "@/lib/queryClient";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import Navbar from "@/components/navbar";
import Sidebar from "@/components/sidebar";
import { PieChart, Save, Calendar, Sliders } from "lucide-react";
import { Slider } from "@/components/ui/slider";
import { TokenPieChart, ChartData } from "@/components/ui/chart";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";

const distributionPlanSchema = z.object({
  name: z.string().min(3, { message: "Plan name must be at least 3 characters" }),
  projectId: z.number(),
  tokenModelId: z.number().optional(),
  distribution: z.any(),
  vestingSchedules: z.any(),
});

type DistributionPlanFormValues = z.infer<typeof distributionPlanSchema>;

type VestingCategory = {
  category: string;
  percentage: number;
  color: string;
  cliff: number;
  vesting: number;
  tgeUnlock: number;
};

export default function DistributionPlansPage() {
  const { user } = useAuth();
  const { toast } = useToast();
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [activeTab, setActiveTab] = useState("distribution");
  
  const colors = ['#3b82f6', '#ec4899', '#10b981', '#f59e0b', '#8b5cf6', '#ef4444'];
  
  // Distribution data
  const [distribution, setDistribution] = useState<ChartData[]>([
    { name: "Team", value: 15, color: colors[0] },
    { name: "Investors", value: 25, color: colors[1] },
    { name: "Community", value: 40, color: colors[2] },
    { name: "Reserves", value: 20, color: colors[3] },
  ]);
  
  // Vesting schedule data
  const [vestingCategories, setVestingCategories] = useState<VestingCategory[]>([
    { category: "Team", percentage: 15, color: colors[0], cliff: 6, vesting: 24, tgeUnlock: 0 },
    { category: "Investors", percentage: 25, color: colors[1], cliff: 3, vesting: 18, tgeUnlock: 10 },
    { category: "Community", percentage: 40, color: colors[2], cliff: 0, vesting: 12, tgeUnlock: 20 },
    { category: "Reserves", percentage: 20, color: colors[3], cliff: 12, vesting: 36, tgeUnlock: 0 },
  ]);
  
  // Calculate vesting release data for the chart
  const getVestingData = () => {
    const months = 37; // 3 years + 1 month (for month 0)
    const data = Array(months).fill(0).map((_, i) => ({ month: i === 0 ? 'TGE' : `M${i}` }));
    
    vestingCategories.forEach(category => {
      const { category: cat, percentage, cliff, vesting, tgeUnlock } = category;
      const totalTokens = percentage;
      const tokensAtTGE = (totalTokens * tgeUnlock) / 100;
      const tokensToVest = totalTokens - tokensAtTGE;
      const monthlyRelease = tokensToVest / vesting;
      
      data.forEach((month, index) => {
        if (index === 0) {
          // TGE
          month[cat] = tokensAtTGE;
        } else if (index <= cliff) {
          // During cliff period
          month[cat] = 0;
        } else if (index <= cliff + vesting) {
          // During vesting period
          month[cat] = monthlyRelease;
        } else {
          // After vesting completes
          month[cat] = 0;
        }
      });
    });
    
    // Calculate cumulative amounts
    const cumulativeData = data.map((month, i) => {
      const result = { month: month.month };
      vestingCategories.forEach(({ category }) => {
        result[`${category}_Cumulative`] = data
          .slice(0, i + 1)
          .reduce((sum, m) => sum + (m[category] || 0), 0);
      });
      return result;
    });
    
    return { monthlyData: data, cumulativeData };
  };
  
  const form = useForm<DistributionPlanFormValues>({
    resolver: zodResolver(distributionPlanSchema),
    defaultValues: {
      name: "Token Distribution Plan",
      projectId: 0,
      tokenModelId: undefined,
      distribution: {},
      vestingSchedules: {},
    },
  });

  const { data: projects, isLoading: loadingProjects } = useQuery<Project[]>({
    queryKey: ["/api/projects"],
    queryFn: getQueryFn({ on401: "throw" }),
  });
  
  const { data: tokenModels, isLoading: loadingTokenModels } = useQuery<TokenModel[]>({
    queryKey: ["/api/token-models"],
    queryFn: getQueryFn({ on401: "throw" }),
    enabled: !!form.getValues("projectId"),
  });
  
  const createDistributionPlanMutation = useMutation({
    mutationFn: async (data: DistributionPlanFormValues) => {
      const res = await apiRequest("POST", "/api/distribution-plans", data);
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["/api/distribution-plans"] });
      toast({
        title: "Distribution Plan Created",
        description: "Your distribution plan has been saved successfully",
      });
    },
    onError: (error) => {
      toast({
        title: "Failed to create distribution plan",
        description: error.message,
        variant: "destructive",
      });
    },
  });

  // Update vesting category percentages when distribution changes
  const updateVestingCategoriesFromDistribution = () => {
    const updatedVestingCategories = vestingCategories.map(category => {
      const distributionItem = distribution.find(item => item.name === category.category);
      if (distributionItem) {
        return { ...category, percentage: distributionItem.value };
      }
      return category;
    });
    setVestingCategories(updatedVestingCategories);
  };

  const onSubmit = (data: DistributionPlanFormValues) => {
    // Convert distribution to expected format
    const distributionData = distribution.reduce((acc, item) => {
      acc[item.name.toLowerCase()] = item.value;
      return acc;
    }, {} as Record<string, number>);
    
    // Convert vesting schedules to expected format
    const vestingSchedulesData = vestingCategories.reduce((acc, item) => {
      acc[item.category.toLowerCase()] = {
        cliff: item.cliff,
        vesting: item.vesting,
        tgeUnlock: item.tgeUnlock,
      };
      return acc;
    }, {} as Record<string, any>);
    
    const formData = {
      ...data,
      distribution: distributionData,
      vestingSchedules: vestingSchedulesData,
    };
    
    createDistributionPlanMutation.mutate(formData);
  };

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  const vestingData = getVestingData();

  return (
    <div className="flex h-screen overflow-hidden">
      {/* Sidebar */}
      <Sidebar isOpen={sidebarOpen} toggle={toggleSidebar} />

      {/* Main Content */}
      <div
        className={`flex-1 flex flex-col overflow-hidden transition-all duration-300 ease-in-out ${
          sidebarOpen ? "md:ml-64" : ""
        }`}
      >
        {/* Top Navigation */}
        <Navbar toggleSidebar={toggleSidebar} />

        {/* Page Content */}
        <main className="flex-1 overflow-y-auto bg-background p-6">
          <div className="mb-8">
            <div className="flex flex-col md:flex-row items-start md:items-center justify-between mb-6">
              <div>
                <h1 className="text-2xl font-bold">Distribution Planner</h1>
                <p className="text-gray-400 mt-1">Create token distribution and vesting schedules</p>
              </div>

              <Button 
                className="mt-4 md:mt-0 bg-primary hover:bg-primary/90" 
                onClick={form.handleSubmit(onSubmit)} 
                disabled={createDistributionPlanMutation.isPending}
              >
                <Save className="mr-2 h-4 w-4" />
                {createDistributionPlanMutation.isPending ? "Saving..." : "Save Plan"}
              </Button>
            </div>

            <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
              <TabsList className="bg-surface border border-gray-700 p-1">
                <TabsTrigger value="distribution" className="data-[state=active]:bg-primary data-[state=active]:text-white">
                  Distribution
                </TabsTrigger>
                <TabsTrigger value="vesting" className="data-[state=active]:bg-primary data-[state=active]:text-white">
                  Vesting Schedule
                </TabsTrigger>
                <TabsTrigger value="preview" className="data-[state=active]:bg-primary data-[state=active]:text-white">
                  Preview
                </TabsTrigger>
              </TabsList>

              <TabsContent value="distribution" className="space-y-6">
                <Card className="bg-surface border-gray-700">
                  <CardHeader>
                    <CardTitle>Token Distribution</CardTitle>
                    <CardDescription>Define how your tokens will be allocated</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <Form {...form}>
                      <form className="space-y-6">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                          <div>
                            <div className="space-y-4 mb-6">
                              <FormField
                                control={form.control}
                                name="name"
                                render={({ field }) => (
                                  <FormItem>
                                    <FormLabel>Plan Name</FormLabel>
                                    <FormControl>
                                      <Input
                                        placeholder="Enter plan name"
                                        className="bg-background border-gray-700"
                                        {...field}
                                      />
                                    </FormControl>
                                    <FormMessage />
                                  </FormItem>
                                )}
                              />
                              
                              <FormField
                                control={form.control}
                                name="projectId"
                                render={({ field }) => (
                                  <FormItem>
                                    <FormLabel>Project</FormLabel>
                                    <Select 
                                      onValueChange={(value) => field.onChange(parseInt(value))}
                                      value={field.value.toString()}
                                      disabled={loadingProjects || !projects?.length}
                                    >
                                      <FormControl>
                                        <SelectTrigger className="bg-background border-gray-700">
                                          <SelectValue placeholder="Select project" />
                                        </SelectTrigger>
                                      </FormControl>
                                      <SelectContent className="bg-background border-gray-700">
                                        {projects?.map((project) => (
                                          <SelectItem key={project.id} value={project.id.toString()}>
                                            {project.name}
                                          </SelectItem>
                                        ))}
                                      </SelectContent>
                                    </Select>
                                    <FormMessage />
                                  </FormItem>
                                )}
                              />
                            </div>
                            
                            <h3 className="text-md font-medium mb-4">Distribution Allocation</h3>
                            {distribution.map((item, index) => (
                              <div key={item.name} className="mb-4">
                                <div className="flex justify-between items-center mb-2">
                                  <label className="text-sm font-medium">{item.name}</label>
                                  <div className="flex items-center">
                                    <Input
                                      type="number"
                                      value={item.value}
                                      min="0"
                                      max="100"
                                      onChange={(e) => {
                                        const newValue = parseInt(e.target.value) || 0;
                                        const newDistribution = [...distribution];
                                        newDistribution[index] = { ...item, value: newValue };
                                        setDistribution(newDistribution);
                                        // Update vesting categories when distribution changes
                                        updateVestingCategoriesFromDistribution();
                                      }}
                                      className="w-16 h-8 text-center p-1 bg-background border-gray-700 text-white"
                                    />
                                    <span className="ml-1 text-gray-400">%</span>
                                  </div>
                                </div>
                                <div className="h-2 bg-gray-700 rounded-full overflow-hidden">
                                  <div
                                    className="h-full rounded-full"
                                    style={{ width: `${item.value}%`, backgroundColor: item.color }}
                                  ></div>
                                </div>
                              </div>
                            ))}
                            
                            <div className="mt-6">
                              <div className="flex justify-between items-center text-sm font-medium">
                                <span>Total:</span>
                                <span className={`${
                                  distribution.reduce((sum, item) => sum + item.value, 0) === 100
                                    ? "text-green-500"
                                    : "text-red-500"
                                }`}>
                                  {distribution.reduce((sum, item) => sum + item.value, 0)}%
                                </span>
                              </div>
                              {distribution.reduce((sum, item) => sum + item.value, 0) !== 100 && (
                                <p className="text-red-500 text-xs mt-1">Total allocation must equal 100%</p>
                              )}
                            </div>
                          </div>
                          
                          <div className="flex flex-col items-center justify-center">
                            <div className="h-64 w-64">
                              <TokenPieChart 
                                data={distribution} 
                                innerRadius={60}
                                outerRadius={80}
                                total={100000000}
                                totalLabel="Total Supply"
                              />
                            </div>
                            
                            <Button
                              variant="outline"
                              className="mt-4 border-gray-700 bg-surface-light hover:bg-surface-light/80"
                              onClick={() => setActiveTab("vesting")}
                            >
                              <Calendar className="mr-2 h-4 w-4" />
                              Configure Vesting Schedule
                            </Button>
                          </div>
                        </div>
                      </form>
                    </Form>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="vesting" className="space-y-6">
                <Card className="bg-surface border-gray-700">
                  <CardHeader>
                    <CardTitle>Vesting Schedule</CardTitle>
                    <CardDescription>Define how tokens will be released over time</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="mb-6">
                      <p className="text-sm text-gray-400 mb-4">
                        Configure the vesting parameters for each token allocation category. The cliff is the period before any tokens are released, and the vesting period is the total time until all tokens are unlocked.
                      </p>
                      
                      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        <div className="space-y-6">
                          {vestingCategories.map((category, index) => (
                            <div key={category.category} className="p-4 bg-surface-light rounded-md border border-gray-700">
                              <div className="flex items-center mb-3">
                                <div 
                                  className="w-3 h-3 rounded-full mr-2" 
                                  style={{ backgroundColor: category.color }}
                                ></div>
                                <h4 className="font-medium">{category.category} ({category.percentage}%)</h4>
                              </div>
                              
                              <div className="space-y-4">
                                <div>
                                  <div className="flex justify-between mb-1">
                                    <label className="text-xs font-medium">TGE Unlock</label>
                                    <span className="text-xs">{category.tgeUnlock}%</span>
                                  </div>
                                  <Slider
                                    value={[category.tgeUnlock]}
                                    min={0}
                                    max={100}
                                    step={1}
                                    onValueChange={(value) => {
                                      const updatedCategories = [...vestingCategories];
                                      updatedCategories[index] = { ...category, tgeUnlock: value[0] };
                                      setVestingCategories(updatedCategories);
                                    }}
                                  />
                                </div>
                                
                                <div>
                                  <div className="flex justify-between mb-1">
                                    <label className="text-xs font-medium">Cliff Period</label>
                                    <span className="text-xs">{category.cliff} months</span>
                                  </div>
                                  <Slider
                                    value={[category.cliff]}
                                    min={0}
                                    max={24}
                                    step={1}
                                    onValueChange={(value) => {
                                      const updatedCategories = [...vestingCategories];
                                      updatedCategories[index] = { ...category, cliff: value[0] };
                                      setVestingCategories(updatedCategories);
                                    }}
                                  />
                                </div>
                                
                                <div>
                                  <div className="flex justify-between mb-1">
                                    <label className="text-xs font-medium">Vesting Period</label>
                                    <span className="text-xs">{category.vesting} months</span>
                                  </div>
                                  <Slider
                                    value={[category.vesting]}
                                    min={1}
                                    max={48}
                                    step={1}
                                    onValueChange={(value) => {
                                      const updatedCategories = [...vestingCategories];
                                      updatedCategories[index] = { ...category, vesting: value[0] };
                                      setVestingCategories(updatedCategories);
                                    }}
                                  />
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                        
                        <div className="flex flex-col">
                          <h4 className="font-medium mb-2">Vesting Schedule Preview</h4>
                          <div className="h-80 bg-surface-light bg-opacity-50 rounded-md border border-gray-700 p-2">
                            <ResponsiveContainer width="100%" height="100%">
                              <BarChart
                                data={vestingData.cumulativeData.filter((_, i) => i % 3 === 0 || i === 0)} // Show every 3 months for clarity
                                margin={{ top: 20, right: 30, left: 0, bottom: 5 }}
                              >
                                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                                <XAxis dataKey="month" stroke="#9ca3af" fontSize={10} />
                                <YAxis stroke="#9ca3af" fontSize={10} />
                                <Tooltip
                                  contentStyle={{ backgroundColor: '#1f2937', borderColor: '#4b5563' }}
                                  labelStyle={{ color: '#e5e7eb' }}
                                />
                                <Legend wrapperStyle={{ fontSize: 10 }} />
                                {vestingCategories.map((category) => (
                                  <Bar
                                    key={category.category}
                                    dataKey={`${category.category}_Cumulative`}
                                    stackId="a"
                                    fill={category.color}
                                    name={category.category}
                                  />
                                ))}
                              </BarChart>
                            </ResponsiveContainer>
                          </div>
                          
                          <div className="bg-surface-light rounded-md border border-gray-700 p-3 mt-4">
                            <h4 className="font-medium text-sm mb-2">Summary</h4>
                            <div className="space-y-1 text-xs">
                              {vestingCategories.map((category) => (
                                <div key={category.category} className="flex justify-between">
                                  <span className="text-gray-300">{category.category}</span>
                                  <span className="text-white">
                                    {category.tgeUnlock}% at TGE, 
                                    {category.cliff > 0 ? ` ${category.cliff}m cliff, ` : ' no cliff, '}
                                    {category.vesting}m vesting
                                  </span>
                                </div>
                              ))}
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex justify-between">
                      <Button 
                        variant="outline" 
                        className="border-gray-700 bg-surface-light hover:bg-surface-light/80"
                        onClick={() => setActiveTab("distribution")}
                      >
                        Back to Distribution
                      </Button>
                      <Button
                        className="bg-primary hover:bg-primary/90"
                        onClick={() => setActiveTab("preview")}
                      >
                        Preview Plan
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="preview" className="space-y-6">
                <Card className="bg-surface border-gray-700">
                  <CardHeader>
                    <CardTitle>Plan Preview</CardTitle>
                    <CardDescription>Review your distribution and vesting schedule</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                      <div>
                        <h3 className="text-lg font-medium mb-4">Distribution Summary</h3>
                        <div className="h-64 flex items-center justify-center">
                          <TokenPieChart 
                            data={distribution} 
                            innerRadius={60}
                            outerRadius={80}
                            showLegend={true}
                          />
                        </div>
                        
                        <div className="mt-4 bg-surface-light rounded-md border border-gray-700 p-3">
                          <h4 className="font-medium text-sm mb-2">Details</h4>
                          <div className="space-y-1 text-xs">
                            {distribution.map((item) => (
                              <div key={item.name} className="flex justify-between">
                                <div className="flex items-center">
                                  <div 
                                    className="w-2 h-2 rounded-full mr-2" 
                                    style={{ backgroundColor: item.color }}
                                  ></div>
                                  <span>{item.name}</span>
                                </div>
                                <span>{item.value}%</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>
                      
                      <div>
                        <h3 className="text-lg font-medium mb-4">Vesting Schedule</h3>
                        <div className="h-64 bg-surface-light bg-opacity-50 rounded-md border border-gray-700 p-2">
                          <ResponsiveContainer width="100%" height="100%">
                            <BarChart
                              data={vestingData.cumulativeData.filter((_, i) => i % 6 === 0 || i === 0)} // Show every 6 months
                              margin={{ top: 20, right: 30, left: 0, bottom: 5 }}
                            >
                              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                              <XAxis dataKey="month" stroke="#9ca3af" fontSize={10} />
                              <YAxis stroke="#9ca3af" fontSize={10} />
                              <Tooltip
                                contentStyle={{ backgroundColor: '#1f2937', borderColor: '#4b5563' }}
                                labelStyle={{ color: '#e5e7eb' }}
                              />
                              <Legend wrapperStyle={{ fontSize: 10 }} />
                              {vestingCategories.map((category) => (
                                <Bar
                                  key={category.category}
                                  dataKey={`${category.category}_Cumulative`}
                                  stackId="a"
                                  fill={category.color}
                                  name={category.category}
                                />
                              ))}
                            </BarChart>
                          </ResponsiveContainer>
                        </div>
                        
                        <div className="mt-4 bg-surface-light rounded-md border border-gray-700 p-3">
                          <h4 className="font-medium text-sm mb-2">Vesting Details</h4>
                          <div className="space-y-2 text-xs">
                            {vestingCategories.map((category) => (
                              <div key={category.category} className="pb-2 border-b border-gray-700">
                                <div className="flex items-center justify-between mb-1">
                                  <div className="flex items-center">
                                    <div 
                                      className="w-2 h-2 rounded-full mr-2" 
                                      style={{ backgroundColor: category.color }}
                                    ></div>
                                    <span className="font-medium">{category.category}</span>
                                  </div>
                                  <span>{category.percentage}%</span>
                                </div>
                                <div className="text-gray-400">
                                  {category.tgeUnlock > 0 && `${category.tgeUnlock}% at TGE `}
                                  {category.cliff > 0 && `• ${category.cliff} months cliff `}
                                  {`• ${category.vesting} months linear vesting`}
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex justify-between">
                      <Button 
                        variant="outline" 
                        className="border-gray-700 bg-surface-light hover:bg-surface-light/80"
                        onClick={() => setActiveTab("vesting")}
                      >
                        Back to Vesting
                      </Button>
                      <Button
                        className="bg-primary hover:bg-primary/90"
                        onClick={form.handleSubmit(onSubmit)}
                        disabled={createDistributionPlanMutation.isPending}
                      >
                        <Save className="mr-2 h-4 w-4" />
                        {createDistributionPlanMutation.isPending ? "Saving..." : "Save Distribution Plan"}
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          </div>
        </main>
      </div>
    </div>
  );
}