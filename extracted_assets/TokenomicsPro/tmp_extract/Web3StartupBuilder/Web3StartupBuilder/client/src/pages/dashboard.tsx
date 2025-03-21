import { useState, useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { Link } from "wouter";
import { QuickStartCard } from "@/components/dashboard/quick-start-card";
import { ProjectCard } from "@/components/dashboard/project-card";
import { ResourceCard } from "@/components/dashboard/resource-card";
import { TokenDistributionChart } from "@/components/dashboard/token-distribution-chart";
import { TokenMetrics } from "@/components/dashboard/token-metrics";
import { Button } from "@/components/ui/button";
import { Project, Resource } from "@shared/schema";
import { apiRequest } from "@/lib/queryClient";
import { useToast } from "@/hooks/use-toast";

export default function Dashboard() {
  const { toast } = useToast();

  // Fetch projects - we'll use a dummy user ID for now
  const projectsQuery = useQuery({
    queryKey: ['/api/projects?userId=1'],
    staleTime: 60000, // 1 minute
  });

  // Fetch resources
  const resourcesQuery = useQuery({
    queryKey: ['/api/resources'],
    staleTime: 300000, // 5 minutes
  });

  // Handle project deletion
  const handleDeleteProject = async (id: number) => {
    try {
      await apiRequest('DELETE', `/api/projects/${id}`);
      toast({
        title: "Project deleted",
        description: "The project has been successfully deleted.",
      });
      // Force refetch of projects
      projectsQuery.refetch();
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to delete the project. Please try again.",
        variant: "destructive",
      });
    }
  };

  return (
    <div className="max-w-7xl mx-auto">
      {/* Dashboard Header */}
      <header className="mb-8">
        <h1 className="text-2xl md:text-3xl font-bold text-dark">Web3 Startup Builder</h1>
        <p className="text-dark-50 mt-2">Design, plan and simulate your tokenomics with ease</p>
      </header>

      {/* Quick Start Cards */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
        <QuickStartCard 
          title="Token Designer"
          description="Create your token and define its basic properties, utility, and economic model."
          buttonText="Start Creating"
          buttonLink="/token-designer"
          buttonColor="text-primary-600"
          gradient="bg-gradient-to-br from-primary-500 to-primary-700"
          shadowColor="shadow-primary-500/20"
          icon={
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-5 w-5">
              <circle cx="12" cy="12" r="10"></circle>
              <path d="M8 12h8"></path>
              <path d="M12 8v8"></path>
            </svg>
          }
        />

        <QuickStartCard 
          title="Distribution Planner"
          description="Plan how your tokens will be distributed across different stakeholders and vesting schedules."
          buttonText="Plan Distribution"
          buttonLink="/distribution-planner"
          buttonColor="text-secondary-600"
          gradient="bg-gradient-to-br from-secondary-500 to-secondary-700"
          shadowColor="shadow-secondary-500/20"
          icon={
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-5 w-5">
              <path d="M21.21 15.89A10 10 0 1 1 8 2.83"></path>
              <path d="M22 12A10 10 0 0 0 12 2v10z"></path>
            </svg>
          }
        />

        <QuickStartCard 
          title="Economic Simulator"
          description="Simulate how your token will perform under different economic scenarios and market conditions."
          buttonText="Run Simulation"
          buttonLink="/economic-simulator"
          buttonColor="text-green-600"
          gradient="bg-gradient-to-br from-green-500 to-green-700"
          shadowColor="shadow-green-500/20"
          icon={
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-5 w-5">
              <path d="M3 3v18h18"></path>
              <path d="M18.7 8l-5.1 5.2-2.8-2.7L7 14.3"></path>
            </svg>
          }
        />
      </section>

      {/* Recent Projects Section */}
      <section className="mb-10">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-semibold text-dark">Recent Projects</h2>
          <Link href="/token-designer?new=true">
            <Button className="text-sm py-2 px-4 bg-dark text-white rounded-lg font-medium hover:bg-dark-50 transition-colors">
              New Project
            </Button>
          </Link>
        </div>

        {/* Projects loading state */}
        {projectsQuery.isLoading && (
          <div className="flex items-center justify-center p-12">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
          </div>
        )}

        {/* Projects empty state */}
        {!projectsQuery.isLoading && projectsQuery.data?.length === 0 && (
          <div className="bg-white rounded-xl shadow-md p-12 text-center border border-light-300">
            <div className="flex flex-col items-center">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-12 w-12 text-dark-50 mb-4">
                <circle cx="12" cy="12" r="10"></circle>
                <path d="M8 12h8"></path>
                <path d="M12 8v8"></path>
              </svg>
              <h3 className="text-lg font-semibold mb-2">No Projects Yet</h3>
              <p className="text-dark-50 mb-6">Start building your web3 project and design your tokenomics</p>
              <Link href="/token-designer?new=true">
                <Button className="bg-primary text-white hover:bg-primary-600">Create Your First Project</Button>
              </Link>
            </div>
          </div>
        )}

        {/* Project Cards */}
        {!projectsQuery.isLoading && projectsQuery.data?.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {(projectsQuery.data as Project[]).map((project) => (
              <ProjectCard 
                key={project.id}
                name={project.name}
                lastEdited={new Date(project.lastEdited)}
                status={project.status as any}
                progress={project.tokenDesignProgress}
                teamMembers={(project.teamMembers as any[]).map(member => ({
                  initials: member.initials,
                  name: member.name,
                  color: member.color
                }))}
                onEdit={() => window.location.href = `/token-designer?project=${project.id}`}
                onDelete={() => handleDeleteProject(project.id)}
                onShare={() => {
                  toast({
                    title: "Share feature",
                    description: "Sharing functionality will be available soon!",
                  });
                }}
              />
            ))}
          </div>
        )}
      </section>

      {/* Token Distribution & Analytics */}
      <section className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-10">
        {/* Token Distribution Chart */}
        <div className="lg:col-span-2">
          <TokenDistributionChart 
            onEdit={() => window.location.href = '/distribution-planner'}
          />
        </div>

        {/* Tokenomics Stats */}
        <div>
          <TokenMetrics 
            onAddMetric={() => {
              toast({
                title: "Custom metrics",
                description: "Custom metrics functionality will be available soon!",
              });
            }}
          />
        </div>
      </section>

      {/* Learning Resources */}
      <section className="mb-10">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-semibold text-dark">Learning Resources</h2>
          <Link href="/learning-hub" className="text-sm text-primary flex items-center gap-1 hover:underline">
            <span>View All</span>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-4 w-4">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
          </Link>
        </div>
        
        {/* Resources loading state */}
        {resourcesQuery.isLoading && (
          <div className="flex items-center justify-center p-12">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
          </div>
        )}

        {/* Resources display */}
        {!resourcesQuery.isLoading && resourcesQuery.data && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {(resourcesQuery.data as Resource[]).map((resource) => (
              <ResourceCard 
                key={resource.id}
                title={resource.title}
                description={resource.description}
                backgroundClass={`bg-${resource.imageBackground}`}
                icon={
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-16 w-16">
                    {resource.imageIcon === 'polygon' && (
                      <polygon points="12 2 22 8.5 22 15.5 12 22 2 15.5 2 8.5 12 2"></polygon>
                    )}
                    {resource.imageIcon === 'monitor' && (
                      <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
                    )}
                    {resource.imageIcon === 'file-text' && (
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                    )}
                  </svg>
                }
                linkText={resource.linkText}
                linkUrl={resource.link}
              />
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
