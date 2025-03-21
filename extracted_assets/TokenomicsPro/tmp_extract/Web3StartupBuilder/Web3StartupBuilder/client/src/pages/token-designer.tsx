import { useState, useEffect } from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { useLocation } from "wouter";
import { queryClient, apiRequest } from "@/lib/queryClient";
import { useToast } from "@/hooks/use-toast";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { insertTokenSchema } from "@shared/schema";

// Extend the token schema for frontend validation
const tokenFormSchema = z.object({
  name: z.string().min(2, "Token name must be at least 2 characters").max(50),
  symbol: z.string().min(1, "Symbol is required").max(10),
  type: z.string(),
  totalSupply: z.string().min(1, "Total supply is required"),
  initialPrice: z.string().optional(),
  initialMarketCap: z.string().optional(),
  circulatingSupply: z.string().optional(),
  projectId: z.number(),
  utility: z.string().optional(),
  governance: z.string().optional(),
  mechanics: z.string().optional(),
});

type TokenFormValues = z.infer<typeof tokenFormSchema>;

export default function TokenDesigner() {
  const [location, setLocation] = useLocation();
  const { toast } = useToast();
  const [currentTab, setCurrentTab] = useState("basic");
  const [isCreatingProject, setIsCreatingProject] = useState(false);
  
  // Parse URL params
  const params = new URLSearchParams(location.split("?")[1]);
  const projectId = params.get("project") ? parseInt(params.get("project")!) : null;
  const isNewProject = params.get("new") === "true";

  // Form setup
  const form = useForm<TokenFormValues>({
    resolver: zodResolver(tokenFormSchema),
    defaultValues: {
      name: "",
      symbol: "",
      type: "ERC-20",
      totalSupply: "100000000",
      initialPrice: "0.01",
      initialMarketCap: "",
      circulatingSupply: "",
      projectId: 1, // Default project ID, will be updated
      utility: "",
      governance: "",
      mechanics: "",
    }
  });

  // Create project mutation
  const createProjectMutation = useMutation({
    mutationFn: async (projectData: any) => {
      const response = await apiRequest("POST", "/api/projects", projectData);
      return await response.json();
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['/api/projects'] });
      // Navigate to the token designer with the new project ID
      setLocation(`/token-designer?project=${data.id}`);
      toast({
        title: "Project created!",
        description: "Now you can design your token.",
      });
      setIsCreatingProject(false);
    },
    onError: () => {
      toast({
        title: "Error",
        description: "Failed to create the project. Please try again.",
        variant: "destructive",
      });
      setIsCreatingProject(false);
    }
  });

  // Create token mutation
  const createTokenMutation = useMutation({
    mutationFn: async (tokenData: any) => {
      const response = await apiRequest("POST", "/api/tokens", tokenData);
      return await response.json();
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: [`/api/projects/${data.projectId}/token`] });
      toast({
        title: "Token created!",
        description: "Your token has been successfully created.",
      });
      // Navigate to dashboard
      setLocation("/");
    },
    onError: () => {
      toast({
        title: "Error",
        description: "Failed to create the token. Please try again.",
        variant: "destructive",
      });
    }
  });

  // If isNewProject, create a new project
  useEffect(() => {
    if (isNewProject && !isCreatingProject) {
      setIsCreatingProject(true);
      createProjectMutation.mutate({
        name: "New Tokenomics Project",
        status: "draft",
        userId: 1, // Default user ID
        tokenDesignProgress: 10,
        teamMembers: [
          {
            initials: "JS",
            name: "John Smith",
            color: "bg-blue-200 text-blue-800"
          }
        ]
      });
    }
  }, [isNewProject, isCreatingProject]);

  // If projectId is available, fetch the token if it exists
  const tokenQuery = useQuery({
    queryKey: projectId ? [`/api/projects/${projectId}/token`] : null,
    enabled: !!projectId,
    retry: false
  });

  // Update form values when token data is fetched
  useEffect(() => {
    if (tokenQuery.data) {
      const token = tokenQuery.data;
      form.reset({
        name: token.name,
        symbol: token.symbol,
        type: token.type,
        totalSupply: token.totalSupply,
        initialPrice: token.initialPrice || "",
        initialMarketCap: token.initialMarketCap || "",
        circulatingSupply: token.circulatingSupply || "",
        projectId: token.projectId,
        utility: token.distribution?.utility || "",
        governance: token.distribution?.governance || "",
        mechanics: token.distribution?.mechanics || "",
      });
    } else if (projectId) {
      form.setValue("projectId", projectId);
    }
  }, [tokenQuery.data, projectId]);

  // Handle form submission
  const onSubmit = (data: TokenFormValues) => {
    // Calculate initial market cap if not provided
    if (!data.initialMarketCap && data.initialPrice && data.totalSupply) {
      const price = parseFloat(data.initialPrice);
      const supply = parseFloat(data.totalSupply);
      if (!isNaN(price) && !isNaN(supply)) {
        data.initialMarketCap = (price * supply).toString();
      }
    }

    // Prepare token data
    const tokenData = {
      ...data,
      distribution: {
        utility: data.utility,
        governance: data.governance,
        mechanics: data.mechanics,
        // Default distribution (can be changed in Distribution Planner)
        allocation: {
          "Community": 31.5,
          "Team & Advisors": 25,
          "Ecosystem Growth": 15,
          "Private Sale": 20,
          "Liquidity": 8.5
        }
      }
    };

    // Remove extra fields not in the token schema
    delete tokenData.utility;
    delete tokenData.governance;
    delete tokenData.mechanics;

    // Create the token
    createTokenMutation.mutate(tokenData);
  };

  // Calculate initial market cap dynamically
  const calculateMarketCap = () => {
    const price = form.watch("initialPrice");
    const supply = form.watch("totalSupply");
    
    if (price && supply) {
      const numPrice = parseFloat(price);
      const numSupply = parseFloat(supply);
      if (!isNaN(numPrice) && !isNaN(numSupply)) {
        const marketCap = numPrice * numSupply;
        form.setValue("initialMarketCap", marketCap.toFixed(2));
      }
    }
  };

  return (
    <div className="max-w-5xl mx-auto">
      <header className="mb-8">
        <h1 className="text-2xl md:text-3xl font-bold text-dark">Token Designer</h1>
        <p className="text-dark-50 mt-2">Design your token and define its economics</p>
      </header>

      {/* Loading state */}
      {(projectId && tokenQuery.isLoading) || createProjectMutation.isPending ? (
        <div className="flex items-center justify-center p-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        </div>
      ) : (
        <Card>
          <CardHeader>
            <CardTitle>Token Configuration</CardTitle>
          </CardHeader>
          <CardContent>
            <Tabs value={currentTab} onValueChange={setCurrentTab}>
              <TabsList className="mb-6">
                <TabsTrigger value="basic">Basic Info</TabsTrigger>
                <TabsTrigger value="economics">Economics</TabsTrigger>
                <TabsTrigger value="utility">Utility & Governance</TabsTrigger>
              </TabsList>
              
              <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                  <TabsContent value="basic" className="space-y-4">
                    <FormField
                      control={form.control}
                      name="name"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Token Name</FormLabel>
                          <FormControl>
                            <Input placeholder="e.g. Ethereum" {...field} />
                          </FormControl>
                          <FormDescription>
                            The full name of your token.
                          </FormDescription>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                    
                    <FormField
                      control={form.control}
                      name="symbol"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Token Symbol</FormLabel>
                          <FormControl>
                            <Input placeholder="e.g. ETH" {...field} />
                          </FormControl>
                          <FormDescription>
                            A short abbreviation for your token (usually 3-4 characters).
                          </FormDescription>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                    
                    <FormField
                      control={form.control}
                      name="type"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Token Type</FormLabel>
                          <Select onValueChange={field.onChange} defaultValue={field.value}>
                            <FormControl>
                              <SelectTrigger>
                                <SelectValue placeholder="Select token type" />
                              </SelectTrigger>
                            </FormControl>
                            <SelectContent>
                              <SelectItem value="ERC-20">ERC-20 (Fungible Token)</SelectItem>
                              <SelectItem value="ERC-721">ERC-721 (NFT)</SelectItem>
                              <SelectItem value="ERC-1155">ERC-1155 (Multi Token)</SelectItem>
                              <SelectItem value="BEP-20">BEP-20 (Binance Smart Chain)</SelectItem>
                              <SelectItem value="SPL">SPL (Solana)</SelectItem>
                            </SelectContent>
                          </Select>
                          <FormDescription>
                            The token standard your token will implement.
                          </FormDescription>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                    
                    <div className="flex justify-end">
                      <Button 
                        type="button" 
                        onClick={() => setCurrentTab("economics")}
                      >
                        Next
                      </Button>
                    </div>
                  </TabsContent>
                  
                  <TabsContent value="economics" className="space-y-4">
                    <FormField
                      control={form.control}
                      name="totalSupply"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Total Supply</FormLabel>
                          <FormControl>
                            <Input 
                              type="text" 
                              placeholder="e.g. 100000000" 
                              {...field} 
                              onChange={(e) => {
                                field.onChange(e);
                                calculateMarketCap();
                              }}
                            />
                          </FormControl>
                          <FormDescription>
                            The maximum number of tokens that will ever exist.
                          </FormDescription>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                    
                    <FormField
                      control={form.control}
                      name="initialPrice"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Initial Token Price (USD)</FormLabel>
                          <FormControl>
                            <Input 
                              type="text" 
                              placeholder="e.g. 0.01" 
                              {...field}
                              onChange={(e) => {
                                field.onChange(e);
                                calculateMarketCap();
                              }}
                            />
                          </FormControl>
                          <FormDescription>
                            The estimated initial price per token in USD.
                          </FormDescription>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                    
                    <FormField
                      control={form.control}
                      name="initialMarketCap"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Initial Market Cap (USD)</FormLabel>
                          <FormControl>
                            <Input 
                              type="text" 
                              placeholder="Calculated automatically" 
                              {...field}
                              disabled
                            />
                          </FormControl>
                          <FormDescription>
                            Total Supply × Initial Price = Initial Market Cap
                          </FormDescription>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                    
                    <FormField
                      control={form.control}
                      name="circulatingSupply"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Initial Circulating Supply</FormLabel>
                          <FormControl>
                            <Input type="text" placeholder="e.g. 20000000" {...field} />
                          </FormControl>
                          <FormDescription>
                            The number of tokens that will be in circulation at launch.
                          </FormDescription>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                    
                    <div className="flex justify-between">
                      <Button 
                        type="button" 
                        variant="outline" 
                        onClick={() => setCurrentTab("basic")}
                      >
                        Back
                      </Button>
                      <Button 
                        type="button" 
                        onClick={() => setCurrentTab("utility")}
                      >
                        Next
                      </Button>
                    </div>
                  </TabsContent>
                  
                  <TabsContent value="utility" className="space-y-4">
                    <FormField
                      control={form.control}
                      name="utility"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Token Utility</FormLabel>
                          <FormControl>
                            <Textarea 
                              placeholder="Describe how your token will be used within the ecosystem" 
                              className="min-h-[100px]"
                              {...field} 
                            />
                          </FormControl>
                          <FormDescription>
                            Define the primary utility of your token. What can users do with it?
                          </FormDescription>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                    
                    <FormField
                      control={form.control}
                      name="governance"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Governance Model</FormLabel>
                          <FormControl>
                            <Textarea 
                              placeholder="Describe the governance rights of token holders" 
                              className="min-h-[100px]"
                              {...field} 
                            />
                          </FormControl>
                          <FormDescription>
                            Explain how token holders can participate in governance.
                          </FormDescription>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                    
                    <FormField
                      control={form.control}
                      name="mechanics"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Token Mechanics</FormLabel>
                          <FormControl>
                            <Textarea 
                              placeholder="Describe the token burn, staking, or other economic mechanisms" 
                              className="min-h-[100px]"
                              {...field} 
                            />
                          </FormControl>
                          <FormDescription>
                            Define any token burn, staking, or other economic mechanisms.
                          </FormDescription>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                    
                    <div className="flex justify-between">
                      <Button 
                        type="button" 
                        variant="outline" 
                        onClick={() => setCurrentTab("economics")}
                      >
                        Back
                      </Button>
                      <Button 
                        type="submit"
                        disabled={createTokenMutation.isPending}
                      >
                        {createTokenMutation.isPending ? (
                          <>
                            <div className="mr-2 h-4 w-4 animate-spin rounded-full border-b-2 border-white"></div>
                            Saving...
                          </>
                        ) : (
                          "Save Token"
                        )}
                      </Button>
                    </div>
                  </TabsContent>
                </form>
              </Form>
            </Tabs>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
