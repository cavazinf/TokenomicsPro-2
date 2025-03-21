import { useState } from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { useAuth } from "@/hooks/use-auth";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useToast } from "@/hooks/use-toast";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { InsertTokenModel, Project, TokenModel } from "@shared/schema";
import { getQueryFn, apiRequest, queryClient } from "@/lib/queryClient";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import Navbar from "@/components/navbar";
import Sidebar from "@/components/sidebar";
import { Coins, Save, FileText, HelpCircle } from "lucide-react";
import { TokenPieChart, ChartData } from "@/components/ui/chart";

const tokenModelSchema = z.object({
  name: z.string().min(3, { message: "Token name must be at least 3 characters" }),
  projectId: z.number(),
  tokenType: z.string(),
  supplyModel: z.string(),
  initialSupply: z.string().min(1, { message: "Initial supply is required" }),
  tokenStandard: z.string(),
  configuration: z.any().optional(),
});

type TokenModelFormValues = z.infer<typeof tokenModelSchema>;

const TOKEN_TYPES = [
  { value: "utility", label: "Utility Token", description: "Provides access to a product or service" },
  { value: "governance", label: "Governance Token", description: "Gives voting power in a protocol" },
  { value: "security", label: "Security Token", description: "Represents ownership in an asset" },
  { value: "payment", label: "Payment Token", description: "Used for payments and transactions" },
  { value: "nft", label: "NFT", description: "Non-fungible, unique digital assets" },
];

const SUPPLY_MODELS = [
  { value: "fixed", label: "Fixed Supply", description: "Total supply is fixed forever" },
  { value: "capped", label: "Capped Supply", description: "Supply can grow but has a maximum cap" },
  { value: "inflationary", label: "Inflationary", description: "Supply increases over time with no cap" },
  { value: "deflationary", label: "Deflationary", description: "Supply decreases over time through burning" },
  { value: "rebase", label: "Rebase", description: "Supply adjusts automatically based on price" },
];

const TOKEN_STANDARDS = ["ERC-20", "ERC-721", "ERC-1155", "ERC-777", "BEP-20"];

export default function TokenDesignerPage() {
  const { user } = useAuth();
  const { toast } = useToast();
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [activeTab, setActiveTab] = useState("design");
  
  // Distribution data for preview
  const [distribution, setDistribution] = useState<ChartData[]>([
    { name: "Team", value: 15, color: "#3b82f6" },
    { name: "Investors", value: 25, color: "#ec4899" },
    { name: "Community", value: 40, color: "#10b981" },
    { name: "Reserves", value: 20, color: "#f59e0b" },
  ]);
  
  const { data: projects, isLoading: loadingProjects } = useQuery<Project[]>({
    queryKey: ["/api/projects"],
    queryFn: getQueryFn({ on401: "throw" }),
  });
  
  const form = useForm<TokenModelFormValues>({
    resolver: zodResolver(tokenModelSchema),
    defaultValues: {
      name: "",
      projectId: 0,
      tokenType: "utility",
      supplyModel: "fixed",
      initialSupply: "100000000",
      tokenStandard: "ERC-20",
      configuration: {
        distribution: {
          team: 15,
          investors: 25,
          community: 40,
          reserves: 20,
        },
      },
    },
  });
  
  const createTokenModelMutation = useMutation({
    mutationFn: async (data: TokenModelFormValues) => {
      const res = await apiRequest("POST", "/api/token-models", data);
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["/api/token-models"] });
      toast({
        title: "Token Model Created",
        description: "Your token model has been saved successfully",
      });
    },
    onError: (error) => {
      toast({
        title: "Failed to create token model",
        description: error.message,
        variant: "destructive",
      });
    },
  });

  const onSubmit = (data: TokenModelFormValues) => {
    // Update distribution in the configuration
    const updatedData = {
      ...data,
      configuration: {
        ...data.configuration,
        distribution: {
          team: distribution.find(d => d.name === "Team")?.value || 15,
          investors: distribution.find(d => d.name === "Investors")?.value || 25,
          community: distribution.find(d => d.name === "Community")?.value || 40,
          reserves: distribution.find(d => d.name === "Reserves")?.value || 20,
        }
      }
    };
    createTokenModelMutation.mutate(updatedData);
  };

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

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
                <h1 className="text-2xl font-bold">Token Designer</h1>
                <p className="text-gray-400 mt-1">Design and configure your token model</p>
              </div>

              <Button className="mt-4 md:mt-0 bg-primary hover:bg-primary/90" onClick={form.handleSubmit(onSubmit)}>
                <Save className="mr-2 h-4 w-4" />
                Save Token Model
              </Button>
            </div>

            <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
              <TabsList className="bg-surface border border-gray-700 p-1">
                <TabsTrigger value="design" className="data-[state=active]:bg-primary data-[state=active]:text-white">
                  Design
                </TabsTrigger>
                <TabsTrigger value="distribution" className="data-[state=active]:bg-primary data-[state=active]:text-white">
                  Distribution
                </TabsTrigger>
                <TabsTrigger value="economics" className="data-[state=active]:bg-primary data-[state=active]:text-white">
                  Economics
                </TabsTrigger>
                <TabsTrigger value="preview" className="data-[state=active]:bg-primary data-[state=active]:text-white">
                  Preview
                </TabsTrigger>
              </TabsList>

              <TabsContent value="design" className="space-y-6">
                <Card className="bg-surface border-gray-700">
                  <CardHeader>
                    <CardTitle>Basic Token Information</CardTitle>
                    <CardDescription>Configure the fundamental properties of your token</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <Form {...form}>
                      <form className="space-y-6">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                          <FormField
                            control={form.control}
                            name="name"
                            render={({ field }) => (
                              <FormItem>
                                <FormLabel>Token Name</FormLabel>
                                <FormControl>
                                  <Input
                                    placeholder="Enter token name"
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
                                <FormDescription>
                                  {loadingProjects ? "Loading projects..." : !projects?.length ? "No projects available, please create a project first" : "Select the project this token belongs to"}
                                </FormDescription>
                                <FormMessage />
                              </FormItem>
                            )}
                          />
                        </div>
                        
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                          <FormField
                            control={form.control}
                            name="tokenType"
                            render={({ field }) => (
                              <FormItem>
                                <FormLabel>Token Type</FormLabel>
                                <Select onValueChange={field.onChange} value={field.value}>
                                  <FormControl>
                                    <SelectTrigger className="bg-background border-gray-700">
                                      <SelectValue placeholder="Select token type" />
                                    </SelectTrigger>
                                  </FormControl>
                                  <SelectContent className="bg-background border-gray-700">
                                    {TOKEN_TYPES.map((type) => (
                                      <SelectItem key={type.value} value={type.value}>
                                        {type.label} - <span className="text-xs text-gray-400">{type.description}</span>
                                      </SelectItem>
                                    ))}
                                  </SelectContent>
                                </Select>
                                <FormMessage />
                              </FormItem>
                            )}
                          />
                          
                          <FormField
                            control={form.control}
                            name="supplyModel"
                            render={({ field }) => (
                              <FormItem>
                                <FormLabel>Supply Model</FormLabel>
                                <Select onValueChange={field.onChange} value={field.value}>
                                  <FormControl>
                                    <SelectTrigger className="bg-background border-gray-700">
                                      <SelectValue placeholder="Select supply model" />
                                    </SelectTrigger>
                                  </FormControl>
                                  <SelectContent className="bg-background border-gray-700">
                                    {SUPPLY_MODELS.map((model) => (
                                      <SelectItem key={model.value} value={model.value}>
                                        {model.label} - <span className="text-xs text-gray-400">{model.description}</span>
                                      </SelectItem>
                                    ))}
                                  </SelectContent>
                                </Select>
                                <FormMessage />
                              </FormItem>
                            )}
                          />
                        </div>
                        
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                          <FormField
                            control={form.control}
                            name="initialSupply"
                            render={({ field }) => (
                              <FormItem>
                                <FormLabel>Initial Supply</FormLabel>
                                <FormControl>
                                  <Input
                                    placeholder="Enter initial supply"
                                    className="bg-background border-gray-700"
                                    {...field}
                                  />
                                </FormControl>
                                <FormDescription>
                                  Total number of tokens that will be created
                                </FormDescription>
                                <FormMessage />
                              </FormItem>
                            )}
                          />
                          
                          <FormField
                            control={form.control}
                            name="tokenStandard"
                            render={({ field }) => (
                              <FormItem>
                                <FormLabel>Token Standard</FormLabel>
                                <div className="flex flex-wrap gap-2">
                                  {TOKEN_STANDARDS.map((standard) => (
                                    <Button
                                      key={standard}
                                      type="button"
                                      className={`${
                                        field.value === standard
                                          ? "bg-primary/20 border-primary/50 text-white"
                                          : "bg-background border-gray-700 text-gray-300"
                                      }`}
                                      variant="outline"
                                      onClick={() => field.onChange(standard)}
                                    >
                                      {standard}
                                    </Button>
                                  ))}
                                </div>
                                <FormMessage />
                              </FormItem>
                            )}
                          />
                        </div>
                      </form>
                    </Form>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="distribution" className="space-y-6">
                <Card className="bg-surface border-gray-700">
                  <CardHeader>
                    <CardTitle>Token Distribution</CardTitle>
                    <CardDescription>Configure how tokens will be distributed</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <h3 className="text-lg font-medium mb-4">Distribution Allocation</h3>
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
                            total={form.getValues("initialSupply")}
                            totalLabel="Total Supply"
                          />
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="economics" className="space-y-6">
                <Card className="bg-surface border-gray-700">
                  <CardHeader>
                    <CardTitle>Token Economics</CardTitle>
                    <CardDescription>Configure economic parameters for your token</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <h3 className="text-lg font-medium mb-4">Monetary Policy</h3>
                        <div className="space-y-4">
                          <div>
                            <label className="text-sm font-medium block mb-2">Inflation Rate</label>
                            <div className="flex items-center">
                              <Input
                                type="number"
                                value="5"
                                className="bg-background border-gray-700 text-white"
                              />
                              <span className="ml-2 text-gray-400">% per year</span>
                            </div>
                            <p className="text-xs text-gray-400 mt-1">Annual rate at which new tokens are created</p>
                          </div>
                          
                          <div>
                            <label className="text-sm font-medium block mb-2">Transaction Fee</label>
                            <div className="flex items-center">
                              <Input
                                type="number"
                                value="0.5"
                                step="0.1"
                                className="bg-background border-gray-700 text-white"
                              />
                              <span className="ml-2 text-gray-400">%</span>
                            </div>
                            <p className="text-xs text-gray-400 mt-1">Fee charged on each transaction</p>
                          </div>
                          
                          <div>
                            <label className="text-sm font-medium block mb-2">Burn Rate</label>
                            <div className="flex items-center">
                              <Input
                                type="number"
                                value="1"
                                step="0.1"
                                className="bg-background border-gray-700 text-white"
                              />
                              <span className="ml-2 text-gray-400">%</span>
                            </div>
                            <p className="text-xs text-gray-400 mt-1">Percentage of fees that are burned</p>
                          </div>
                        </div>
                      </div>
                      
                      <div>
                        <h3 className="text-lg font-medium mb-4">Utility Mechanisms</h3>
                        <div className="space-y-4">
                          <div>
                            <label className="text-sm font-medium block mb-2">Staking APY</label>
                            <div className="flex items-center">
                              <Input
                                type="number"
                                value="12"
                                className="bg-background border-gray-700 text-white"
                              />
                              <span className="ml-2 text-gray-400">% per year</span>
                            </div>
                            <p className="text-xs text-gray-400 mt-1">Annual yield for staking tokens</p>
                          </div>
                          
                          <div>
                            <label className="text-sm font-medium block mb-2">Governance Power</label>
                            <Select defaultValue="linear">
                              <SelectTrigger className="bg-background border-gray-700">
                                <SelectValue placeholder="Select governance model" />
                              </SelectTrigger>
                              <SelectContent className="bg-background border-gray-700">
                                <SelectItem value="linear">Linear (1 token = 1 vote)</SelectItem>
                                <SelectItem value="quadratic">Quadratic (vote power = √tokens)</SelectItem>
                                <SelectItem value="time-weighted">Time-Weighted (based on holding period)</SelectItem>
                              </SelectContent>
                            </Select>
                            <p className="text-xs text-gray-400 mt-1">How voting power is calculated</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="preview" className="space-y-6">
                <Card className="bg-surface border-gray-700">
                  <CardHeader>
                    <CardTitle>Token Model Preview</CardTitle>
                    <CardDescription>Review your token design before finalizing</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <h3 className="text-lg font-medium mb-4">Token Summary</h3>
                        <dl className="space-y-4">
                          <div>
                            <dt className="text-sm font-medium text-gray-400">Token Name</dt>
                            <dd className="text-white">{form.getValues("name") || "My Token"}</dd>
                          </div>
                          <div>
                            <dt className="text-sm font-medium text-gray-400">Token Type</dt>
                            <dd className="text-white capitalize">
                              {TOKEN_TYPES.find(t => t.value === form.getValues("tokenType"))?.label || "Utility Token"}
                            </dd>
                          </div>
                          <div>
                            <dt className="text-sm font-medium text-gray-400">Supply Model</dt>
                            <dd className="text-white capitalize">
                              {SUPPLY_MODELS.find(m => m.value === form.getValues("supplyModel"))?.label || "Fixed Supply"}
                            </dd>
                          </div>
                          <div>
                            <dt className="text-sm font-medium text-gray-400">Initial Supply</dt>
                            <dd className="text-white">
                              {parseFloat(form.getValues("initialSupply")).toLocaleString()} tokens
                            </dd>
                          </div>
                          <div>
                            <dt className="text-sm font-medium text-gray-400">Token Standard</dt>
                            <dd className="text-white">{form.getValues("tokenStandard")}</dd>
                          </div>
                        </dl>
                      </div>
                      
                      <div>
                        <h3 className="text-lg font-medium mb-4">Distribution Summary</h3>
                        <div className="h-64 w-full flex items-center justify-center">
                          <TokenPieChart 
                            data={distribution} 
                            innerRadius={60}
                            outerRadius={80}
                            showLegend={true}
                          />
                        </div>
                      </div>
                    </div>
                    
                    <div className="mt-8 flex justify-end space-x-4">
                      <Button variant="outline" className="border-gray-700 text-white">
                        <FileText className="mr-2 h-4 w-4" />
                        Export as PDF
                      </Button>
                      <Button className="bg-primary hover:bg-primary/90" onClick={form.handleSubmit(onSubmit)} disabled={createTokenModelMutation.isPending}>
                        <Save className="mr-2 h-4 w-4" />
                        {createTokenModelMutation.isPending ? "Saving..." : "Save Token Model"}
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