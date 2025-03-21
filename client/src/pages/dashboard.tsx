
import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { ProjectCard } from "@/components/dashboard/project-card";
import { TokenDistributionChart } from "@/components/dashboard/token-distribution-chart";
import { TokenMetrics } from "@/components/dashboard/token-metrics";
import { QuickStartCard } from "@/components/dashboard/quick-start-card";
import { Lightbulb, Rocket, Coins, Users } from "lucide-react";

export default function Dashboard() {
  // Sample data
  const projects = [
    {
      name: "Decentralized Finance App",
      lastEdited: new Date(2023, 3, 15),
      status: "in_progress" as const,
      progress: 65,
      teamMembers: [
        { initials: "JD", name: "John Doe", color: "bg-blue-500" },
        { initials: "AS", name: "Alice Smith", color: "bg-green-500" },
      ],
    },
    {
      name: "NFT Marketplace",
      lastEdited: new Date(2023, 4, 10),
      status: "draft" as const,
      progress: 30,
      teamMembers: [
        { initials: "JD", name: "John Doe", color: "bg-blue-500" },
      ],
    }
  ];

  const tokenDistribution = {
    "Team": 20,
    "Investors": 15,
    "Community": 25,
    "Treasury": 15,
    "Ecosystem": 25
  };

  const metrics = [
    {
      label: "Total Supply",
      value: "100,000,000",
      icon: <Coins className="h-4 w-4" />,
      bgColor: "bg-primary/10",
      iconColor: "text-primary"
    },
    {
      label: "Initial Market Cap",
      value: "$2,000,000",
      icon: <Coins className="h-4 w-4" />,
      bgColor: "bg-secondary/10",
      iconColor: "text-secondary"
    },
    {
      label: "Community",
      value: "5,000+",
      icon: <Users className="h-4 w-4" />,
      bgColor: "bg-accent/10",
      iconColor: "text-accent"
    }
  ];

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <QuickStartCard
          title="Design Token"
          description="Create your token economics model and distribution"
          icon={<Coins className="h-5 w-5 text-white" />}
          gradient="bg-gradient-to-br from-primary to-primary-light"
          buttonText="Start designing"
          buttonLink="/token-designer"
          buttonColor="text-primary"
          shadowColor="shadow-primary/20"
        />
        <QuickStartCard
          title="Distribution Plan"
          description="Plan your token distribution and vesting schedule"
          icon={<Lightbulb className="h-5 w-5 text-white" />}
          gradient="bg-gradient-to-br from-secondary to-secondary-light"
          buttonText="Create plan"
          buttonLink="/distribution-plans"
          buttonColor="text-secondary"
          shadowColor="shadow-secondary/20"
        />
        <QuickStartCard
          title="Startup Builder"
          description="Create your Web3 business plan and structure"
          icon={<Rocket className="h-5 w-5 text-white" />}
          gradient="bg-gradient-to-br from-accent to-accent-light"
          buttonText="Build startup"
          buttonLink="/startup-plans"
          buttonColor="text-accent"
          shadowColor="shadow-accent/20"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="md:col-span-2">
          <CardHeader>
            <CardTitle>Recent Projects</CardTitle>
            <CardDescription>Your recently updated projects</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {projects.map((project, index) => (
              <ProjectCard key={index} {...project} />
            ))}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Token Distribution</CardTitle>
            <CardDescription>Current allocation model</CardDescription>
          </CardHeader>
          <CardContent>
            <TokenDistributionChart distribution={tokenDistribution} />
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Token Metrics</CardTitle>
          <CardDescription>Key metrics for your token</CardDescription>
        </CardHeader>
        <CardContent>
          <TokenMetrics metrics={metrics} />
        </CardContent>
      </Card>
    </div>
  );
}
