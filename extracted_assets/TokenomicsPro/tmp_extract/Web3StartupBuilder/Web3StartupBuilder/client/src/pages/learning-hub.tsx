import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ResourceCard } from "@/components/dashboard/resource-card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Input } from "@/components/ui/input";
import { Resource } from "@shared/schema";
import { Button } from "@/components/ui/button";
import { SearchIcon } from "lucide-react";

export default function LearningHub() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedTab, setSelectedTab] = useState("all");

  // Fetch resources
  const resourcesQuery = useQuery({
    queryKey: ['/api/resources'],
    staleTime: 300000, // 5 minutes
  });

  // Filter resources based on search query and selected tab
  const getFilteredResources = () => {
    if (!resourcesQuery.data) return [];
    
    const resources = resourcesQuery.data as Resource[];
    
    return resources.filter(resource => {
      // Filter by search query
      const matchesSearch = 
        searchQuery === "" || 
        resource.title.toLowerCase().includes(searchQuery.toLowerCase()) || 
        resource.description.toLowerCase().includes(searchQuery.toLowerCase());
      
      // Filter by tab
      const matchesTab = 
        selectedTab === "all" || 
        resource.type === selectedTab;
      
      return matchesSearch && matchesTab;
    });
  };

  const filteredResources = getFilteredResources();

  // Function to render resource icon based on type
  const renderResourceIcon = (iconName: string) => {
    return (
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-16 w-16">
        {iconName === 'polygon' && (
          <polygon points="12 2 22 8.5 22 15.5 12 22 2 15.5 2 8.5 12 2"></polygon>
        )}
        {iconName === 'monitor' && (
          <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
        )}
        {iconName === 'file-text' && (
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
        )}
      </svg>
    );
  };

  // Featured resource - just picks the first one for now
  const featuredResource = resourcesQuery.data && (resourcesQuery.data as Resource[])[0];

  return (
    <div className="max-w-7xl mx-auto">
      <header className="mb-8">
        <h1 className="text-2xl md:text-3xl font-bold text-dark">Learning Hub</h1>
        <p className="text-dark-50 mt-2">Learn about tokenomics, token distribution, and economic models</p>
      </header>

      {/* Featured Resource */}
      {featuredResource && (
        <section className="mb-10">
          <Card className="overflow-hidden">
            <div className="flex flex-col md:flex-row">
              <div className={`md:w-1/3 h-40 md:h-auto bg-${featuredResource.imageBackground} relative flex items-center justify-center`}>
                <div className="h-16 w-16 text-white opacity-40">
                  {renderResourceIcon(featuredResource.imageIcon)}
                </div>
              </div>
              <div className="md:w-2/3 p-6">
                <h2 className="text-xl font-bold mb-2">{featuredResource.title}</h2>
                <p className="text-dark-50 mb-4">{featuredResource.description}</p>
                <p className="text-dark-50 mb-6">
                  Explore this comprehensive guide to understand the fundamental principles of designing a token economy
                  that delivers real utility and sustainable value over time.
                </p>
                <Button>
                  {featuredResource.linkText}
                </Button>
              </div>
            </div>
          </Card>
        </section>
      )}

      {/* Search and Filtering */}
      <section className="mb-8">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="relative w-full md:w-96">
            <SearchIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
            <Input
              placeholder="Search resources..."
              className="pl-10"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
          
          <Tabs value={selectedTab} onValueChange={setSelectedTab}>
            <TabsList>
              <TabsTrigger value="all">All</TabsTrigger>
              <TabsTrigger value="guide">Guides</TabsTrigger>
              <TabsTrigger value="tutorial">Tutorials</TabsTrigger>
              <TabsTrigger value="case_study">Case Studies</TabsTrigger>
            </TabsList>
          </Tabs>
        </div>
      </section>

      {/* Resources Grid */}
      <section>
        {/* Loading state */}
        {resourcesQuery.isLoading && (
          <div className="flex items-center justify-center p-12">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
          </div>
        )}

        {/* Empty state */}
        {!resourcesQuery.isLoading && filteredResources.length === 0 && (
          <Card className="p-12 text-center">
            <div className="flex flex-col items-center">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-12 w-12 text-dark-50 mb-4">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
              </svg>
              <h3 className="text-lg font-semibold mb-2">No resources found</h3>
              <p className="text-dark-50">Try adjusting your search or filter criteria</p>
            </div>
          </Card>
        )}

        {/* Resources display */}
        {!resourcesQuery.isLoading && filteredResources.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredResources.map((resource) => (
              <ResourceCard 
                key={resource.id}
                title={resource.title}
                description={resource.description}
                backgroundClass={`bg-${resource.imageBackground}`}
                icon={renderResourceIcon(resource.imageIcon)}
                linkText={resource.linkText}
                linkUrl={resource.link}
              />
            ))}
          </div>
        )}
      </section>

      {/* Token Economic Learning Section */}
      <section className="mt-16">
        <h2 className="text-xl font-semibold text-dark mb-6">Learn By Topic</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>Token Economic Models</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-4">
                <li className="flex items-start gap-3">
                  <div className="h-6 w-6 rounded-full bg-primary-100 flex items-center justify-center text-primary">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-4 w-4">
                      <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                      <polyline points="22 4 12 14.01 9 11.01"></polyline>
                    </svg>
                  </div>
                  <div>
                    <h3 className="font-medium">Utility Token Models</h3>
                    <p className="text-sm text-dark-50">Tokens that provide access to services or products within the platform.</p>
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <div className="h-6 w-6 rounded-full bg-primary-100 flex items-center justify-center text-primary">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-4 w-4">
                      <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                      <polyline points="22 4 12 14.01 9 11.01"></polyline>
                    </svg>
                  </div>
                  <div>
                    <h3 className="font-medium">Governance Token Models</h3>
                    <p className="text-sm text-dark-50">Tokens that grant voting rights in the protocol decision-making process.</p>
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <div className="h-6 w-6 rounded-full bg-primary-100 flex items-center justify-center text-primary">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-4 w-4">
                      <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                      <polyline points="22 4 12 14.01 9 11.01"></polyline>
                    </svg>
                  </div>
                  <div>
                    <h3 className="font-medium">Security Token Models</h3>
                    <p className="text-sm text-dark-50">Tokens that represent ownership in an asset or business.</p>
                  </div>
                </li>
              </ul>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Token Distribution Strategies</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-4">
                <li className="flex items-start gap-3">
                  <div className="h-6 w-6 rounded-full bg-secondary-100 flex items-center justify-center text-secondary">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-4 w-4">
                      <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                      <polyline points="22 4 12 14.01 9 11.01"></polyline>
                    </svg>
                  </div>
                  <div>
                    <h3 className="font-medium">Fair Launch Models</h3>
                    <p className="text-sm text-dark-50">Distribution models that aim to give equal opportunity to all participants.</p>
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <div className="h-6 w-6 rounded-full bg-secondary-100 flex items-center justify-center text-secondary">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-4 w-4">
                      <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                      <polyline points="22 4 12 14.01 9 11.01"></polyline>
                    </svg>
                  </div>
                  <div>
                    <h3 className="font-medium">Vesting Schedules</h3>
                    <p className="text-sm text-dark-50">Time-based release of tokens to align incentives and ensure long-term commitment.</p>
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <div className="h-6 w-6 rounded-full bg-secondary-100 flex items-center justify-center text-secondary">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-4 w-4">
                      <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                      <polyline points="22 4 12 14.01 9 11.01"></polyline>
                    </svg>
                  </div>
                  <div>
                    <h3 className="font-medium">Airdrops & Incentives</h3>
                    <p className="text-sm text-dark-50">Distribution mechanisms to reward early adopters and build community.</p>
                  </div>
                </li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Newsletter Section */}
      <section className="mt-16 mb-10">
        <Card className="bg-gradient-to-r from-primary-500 to-primary-700 text-white">
          <CardContent className="p-8">
            <div className="flex flex-col md:flex-row items-center justify-between gap-6">
              <div>
                <h2 className="text-xl font-semibold mb-2">Stay Updated with Tokenomics Trends</h2>
                <p className="text-primary-100">Subscribe to our newsletter for the latest insights and best practices.</p>
              </div>
              <div className="flex w-full md:w-auto gap-2">
                <Input 
                  placeholder="Your email address" 
                  className="bg-white text-dark border-none"
                />
                <Button variant="secondary">
                  Subscribe
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </section>
    </div>
  );
}
