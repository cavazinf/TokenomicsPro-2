import { useState } from "react";
import { useAuth } from "@/hooks/use-auth";
import Navbar from "@/components/navbar";
import Sidebar from "@/components/sidebar";
import StatsCard from "@/components/dashboard/stats-card";
import RecentProjects from "@/components/dashboard/recent-projects";
import TokenomicsOverview from "@/components/dashboard/tokenomics-overview";
import TokenDesigner from "@/components/tokenomics/token-designer";
import EconomicModel from "@/components/tokenomics/economic-model";
import DistributionVesting from "@/components/tokenomics/distribution-vesting";
import StartupPlanner from "@/components/startup/startup-planner";
import RoadmapBuilder from "@/components/startup/roadmap-builder";
import TeamBuilder from "@/components/startup/team-builder";
import BusinessModels from "@/components/startup/business-models";
import ResourceLibrary from "@/components/resources/resource-library";
import { Folder, Coins, Users, BookOpen } from "lucide-react";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";

export default function HomePage() {
  const { user } = useAuth();
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [activeTab, setActiveTab] = useState("overview");

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
          {/* Dashboard Overview */}
          <div className="mb-8">
            <div className="flex flex-col md:flex-row items-start md:items-center justify-between mb-6">
              <div>
                <h1 className="text-2xl font-bold">Welcome back, {user?.name || user?.username}!</h1>
                <p className="text-gray-400 mt-1">Here's what's happening with your projects</p>
              </div>

              <div className="mt-4 md:mt-0 flex space-x-2">
                <button className="px-3 py-1.5 bg-surface rounded-md text-sm flex items-center text-gray-300 hover:bg-surface-light transition">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-4 w-4 mr-1"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fillRule="evenodd"
                      d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z"
                      clipRule="evenodd"
                    />
                  </svg>
                  Export
                </button>
                <button className="px-3 py-1.5 bg-surface rounded-md text-sm flex items-center text-gray-300 hover:bg-surface-light transition">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-4 w-4 mr-1"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fillRule="evenodd"
                      d="M3 3a1 1 0 011-1h12a1 1 0 011 1v3a1 1 0 01-.293.707L12 11.414V15a1 1 0 01-.293.707l-2 2A1 1 0 018 17v-5.586L3.293 6.707A1 1 0 013 6V3z"
                      clipRule="evenodd"
                    />
                  </svg>
                  Filter
                </button>
                <button className="px-3 py-1.5 bg-surface rounded-md text-sm flex items-center text-gray-300 hover:bg-surface-light transition">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-4 w-4 mr-1"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fillRule="evenodd"
                      d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z"
                      clipRule="evenodd"
                    />
                  </svg>
                  Last 30 days
                </button>
              </div>
            </div>

            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
              <StatsCard
                title="Active Projects"
                value={5}
                change="+2 from last month"
                changeType="positive"
                icon={<Folder className="h-5 w-5" />}
                iconColor="text-primary"
                iconBgColor="bg-primary/10"
              />
              <StatsCard
                title="Token Models"
                value={12}
                change="+3 from last month"
                changeType="positive"
                icon={<Coins className="h-5 w-5" />}
                iconColor="text-secondary"
                iconBgColor="bg-secondary/10"
              />
              <StatsCard
                title="Team Members"
                value={8}
                change="+1 from last month"
                changeType="positive"
                icon={<Users className="h-5 w-5" />}
                iconColor="text-info"
                iconBgColor="bg-info/10"
              />
              <StatsCard
                title="Resources Used"
                value={24}
                change="+8 from last month"
                changeType="warning"
                icon={<BookOpen className="h-5 w-5" />}
                iconColor="text-accent"
                iconBgColor="bg-accent/10"
              />
            </div>

            {/* Recent Activity & Tokenomics Overview */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Recent Projects */}
              <div className="lg:col-span-1">
                <RecentProjects />
              </div>

              {/* Tokenomics Overview */}
              <div className="lg:col-span-2">
                <TokenomicsOverview />
              </div>
            </div>
          </div>

          {/* Main Content Tabs */}
          <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
            <TabsList className="border-b border-gray-700 bg-transparent w-full justify-start rounded-none p-0">
              <TabsTrigger
                value="tokenomics"
                className="text-sm py-4 px-6 data-[state=active]:border-b-2 data-[state=active]:border-accent data-[state=active]:text-white data-[state=active]:shadow-none rounded-none bg-transparent text-gray-400 hover:text-white"
              >
                TokenomicsLabs
              </TabsTrigger>
              <TabsTrigger
                value="startup"
                className="text-sm py-4 px-6 data-[state=active]:border-b-2 data-[state=active]:border-accent data-[state=active]:text-white data-[state=active]:shadow-none rounded-none bg-transparent text-gray-400 hover:text-white"
              >
                Web3StartupBuild
              </TabsTrigger>
              <TabsTrigger
                value="resources"
                className="text-sm py-4 px-6 data-[state=active]:border-b-2 data-[state=active]:border-accent data-[state=active]:text-white data-[state=active]:shadow-none rounded-none bg-transparent text-gray-400 hover:text-white"
              >
                Resource Library
              </TabsTrigger>
            </TabsList>

            {/* TokenomicsLabs Tab Content */}
            <TabsContent value="tokenomics" className="mb-8">
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Token Designer */}
                <TokenDesigner />

                {/* Economic Model */}
                <EconomicModel />

                {/* Distribution & Vesting */}
                <DistributionVesting />
              </div>
            </TabsContent>

            {/* Web3StartupBuild Tab Content */}
            <TabsContent value="startup" className="mb-8">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Startup Planner */}
                <StartupPlanner />

                {/* Roadmap Builder */}
                <RoadmapBuilder />

                {/* Team Building & Business Models */}
                <div className="lg:col-span-2 grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* Team Building */}
                  <TeamBuilder />

                  {/* Business Models */}
                  <BusinessModels />
                </div>
              </div>
            </TabsContent>

            {/* Resource Library Tab Content */}
            <TabsContent value="resources" className="mb-8">
              <ResourceLibrary />
            </TabsContent>
          </Tabs>
        </main>
      </div>
    </div>
  );
}
