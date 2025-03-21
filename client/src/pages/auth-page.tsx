import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useAuth } from "@/hooks/use-auth";
import { useLocation } from "wouter";
import { insertUserSchema } from "@shared/schema";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Landmark } from "lucide-react";

const loginSchema = insertUserSchema.pick({
  username: true,
  password: true,
});

const registerSchema = insertUserSchema.extend({
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords do not match",
  path: ["confirmPassword"],
});

export default function AuthPage() {
  const { user, loginMutation, registerMutation } = useAuth();
  const [, navigate] = useLocation();

  // Redirect if already logged in
  useEffect(() => {
    if (user) {
      navigate("/");
    }
  }, [user, navigate]);

  // Login form
  const loginForm = useForm<z.infer<typeof loginSchema>>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      username: "",
      password: "",
    },
  });

  // Register form
  const registerForm = useForm<z.infer<typeof registerSchema>>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      username: "",
      name: "",
      email: "",
      password: "",
      confirmPassword: "",
    },
  });

  // Handle login form submission
  const onLoginSubmit = (values: z.infer<typeof loginSchema>) => {
    loginMutation.mutate(values);
  };

  // Handle register form submission
  const onRegisterSubmit = (values: z.infer<typeof registerSchema>) => {
    const { confirmPassword, ...userDetails } = values;
    registerMutation.mutate(userDetails);
  };

  return (
    <div className="min-h-screen bg-background flex flex-col lg:flex-row">
      {/* Form Side */}
      <div className="flex-1 flex flex-col justify-center items-center p-8">
        <div className="w-full max-w-md mx-auto">
          <div className="flex justify-center mb-8">
            <div className="h-12 w-12 rounded-md bg-gradient-to-br from-primary to-secondary flex items-center justify-center">
              <Landmark className="h-6 w-6 text-white" />
            </div>
          </div>
          
          <Card className="bg-surface border-gray-700">
            <CardHeader className="space-y-1">
              <CardTitle className="text-2xl font-bold text-center">TokenomicsPro</CardTitle>
              <CardDescription className="text-center">
                Your all-in-one platform for Web3 tokenomics and startup building
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Tabs defaultValue="login" className="w-full">
                <TabsList className="grid grid-cols-2 mb-6">
                  <TabsTrigger value="login">Login</TabsTrigger>
                  <TabsTrigger value="register">Register</TabsTrigger>
                </TabsList>
                
                {/* Login Form */}
                <TabsContent value="login">
                  <Form {...loginForm}>
                    <form onSubmit={loginForm.handleSubmit(onLoginSubmit)} className="space-y-4">
                      <FormField
                        control={loginForm.control}
                        name="username"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>Username</FormLabel>
                            <FormControl>
                              <Input 
                                placeholder="Enter your username" 
                                {...field} 
                                className="bg-background border-gray-700"
                              />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                      <FormField
                        control={loginForm.control}
                        name="password"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>Password</FormLabel>
                            <FormControl>
                              <Input 
                                type="password" 
                                placeholder="Enter your password" 
                                {...field} 
                                className="bg-background border-gray-700"
                              />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                      <Button 
                        type="submit" 
                        className="w-full bg-primary" 
                        disabled={loginMutation.isPending}
                      >
                        {loginMutation.isPending ? "Logging in..." : "Login"}
                      </Button>
                    </form>
                  </Form>
                </TabsContent>
                
                {/* Register Form */}
                <TabsContent value="register">
                  <Form {...registerForm}>
                    <form onSubmit={registerForm.handleSubmit(onRegisterSubmit)} className="space-y-4">
                      <FormField
                        control={registerForm.control}
                        name="username"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>Username</FormLabel>
                            <FormControl>
                              <Input 
                                placeholder="Choose a username" 
                                {...field} 
                                className="bg-background border-gray-700"
                              />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                      <FormField
                        control={registerForm.control}
                        name="name"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>Full Name</FormLabel>
                            <FormControl>
                              <Input 
                                placeholder="Enter your full name" 
                                {...field} 
                                className="bg-background border-gray-700"
                              />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                      <FormField
                        control={registerForm.control}
                        name="email"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>Email</FormLabel>
                            <FormControl>
                              <Input 
                                type="email" 
                                placeholder="Enter your email" 
                                {...field} 
                                className="bg-background border-gray-700"
                              />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                      <FormField
                        control={registerForm.control}
                        name="password"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>Password</FormLabel>
                            <FormControl>
                              <Input 
                                type="password" 
                                placeholder="Create a password" 
                                {...field} 
                                className="bg-background border-gray-700"
                              />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                      <FormField
                        control={registerForm.control}
                        name="confirmPassword"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>Confirm Password</FormLabel>
                            <FormControl>
                              <Input 
                                type="password" 
                                placeholder="Confirm your password" 
                                {...field} 
                                className="bg-background border-gray-700"
                              />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                      <Button 
                        type="submit" 
                        className="w-full bg-primary" 
                        disabled={registerMutation.isPending}
                      >
                        {registerMutation.isPending ? "Creating account..." : "Create Account"}
                      </Button>
                    </form>
                  </Form>
                </TabsContent>
              </Tabs>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Hero Side */}
      <div className="hidden lg:flex flex-1 bg-gradient-to-br from-primary/20 to-secondary/20 p-8">
        <div className="max-w-xl mx-auto flex flex-col justify-center">
          <h1 className="text-4xl font-bold mb-6">
            Build Your Web3 Project with{" "}
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-primary to-secondary">
              TokenomicsPro
            </span>
          </h1>
          <p className="text-gray-300 text-lg mb-8">
            The all-in-one platform for designing token economics and launching successful Web3 startups.
          </p>

          <div className="grid grid-cols-2 gap-6">
            <div className="rounded-lg bg-surface p-6 border border-gray-700">
              <Coins className="h-8 w-8 text-primary mb-3" />
              <h3 className="text-xl font-medium mb-2">TokenomicsLabs</h3>
              <p className="text-gray-400">
                Design token models, simulate economic behaviors, and create distribution plans.
              </p>
            </div>
            <div className="rounded-lg bg-surface p-6 border border-gray-700">
              <Building className="h-8 w-8 text-secondary mb-3" />
              <h3 className="text-xl font-medium mb-2">Web3StartupBuild</h3>
              <p className="text-gray-400">
                Plan your Web3 business model, create roadmaps, and build your team.
              </p>
            </div>
          </div>

          <div className="mt-8 flex justify-center space-x-6">
            <div className="text-center">
              <div className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary to-secondary">
                1000+
              </div>
              <div className="text-gray-400 mt-1">Active Projects</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-secondary to-accent">
                500+
              </div>
              <div className="text-gray-400 mt-1">Successful Launches</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-accent to-warning">
                250+
              </div>
              <div className="text-gray-400 mt-1">Resource Guides</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function Coins(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <circle cx="8" cy="8" r="6" />
      <path d="M18.09 10.37A6 6 0 1 1 10.34 18" />
      <path d="M7 6h1v4" />
      <path d="m16.71 13.88.7.71-2.82 2.82" />
    </svg>
  );
}

function Building(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <rect x="4" y="2" width="16" height="20" rx="2" ry="2" />
      <path d="M9 22v-4h6v4" />
      <path d="M8 6h.01" />
      <path d="M16 6h.01" />
      <path d="M12 6h.01" />
      <path d="M12 10h.01" />
      <path d="M12 14h.01" />
      <path d="M16 10h.01" />
      <path d="M16 14h.01" />
      <path d="M8 10h.01" />
      <path d="M8 14h.01" />
    </svg>
  );
}
