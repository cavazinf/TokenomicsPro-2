import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Search, FileText, Presentation, Film, Calculator, BookOpen, PieChart } from "lucide-react";
import { Button } from "@/components/ui/button";

type ResourceCategory = {
  id: string;
  name: string;
  icon: React.ReactNode;
  count: number;
};

type FeaturedResource = {
  id: string;
  type: string;
  title: string;
  description: string;
  meta: string;
  gradient: string;
  icon: React.ReactNode;
  action: string;
  color: string;
};

type Article = {
  id: string;
  title: string;
  date: string;
  description: string;
  tags: string[];
  icon: React.ReactNode;
  color: string;
};

export default function ResourceLibrary() {
  const [searchQuery, setSearchQuery] = useState("");

  const categories: ResourceCategory[] = [
    { id: "tokenomics", name: "Tokenomics Fundamentals", icon: <PieChart className="text-primary" />, count: 12 },
    { id: "whitepaper", name: "Whitepaper Templates", icon: <FileText className="text-secondary" />, count: 8 },
    { id: "business", name: "Web3 Business Models", icon: <BookOpen className="text-accent" />, count: 15 },
    { id: "security", name: "Security Best Practices", icon: <FileText className="text-warning" />, count: 10 },
    { id: "community", name: "Community Building", icon: <BookOpen className="text-info" />, count: 9 },
    { id: "fundraising", name: "Fundraising Strategies", icon: <PieChart className="text-error" />, count: 11 },
  ];

  const featuredResources: FeaturedResource[] = [
    {
      id: "tokenomics-guide",
      type: "Guide",
      title: "Tokenomics Fundamentals Guide",
      description: "Learn the core principles of designing effective token economics",
      meta: "10 min read",
      gradient: "from-primary to-secondary",
      icon: <FileText className="h-10 w-10 text-white" />,
      action: "Read Guide",
      color: "bg-primary",
    },
    {
      id: "pitch-deck",
      type: "Template",
      title: "Web3 Pitch Deck Template",
      description: "Professional templates designed for Web3 startups to pitch investors",
      meta: "5 files",
      gradient: "from-secondary to-accent",
      icon: <Presentation className="h-10 w-10 text-white" />,
      action: "Download",
      color: "bg-secondary",
    },
    {
      id: "vesting-video",
      type: "Video",
      title: "Token Vesting Strategies Explained",
      description: "A comprehensive video guide to optimal token vesting schedules",
      meta: "32 minutes",
      gradient: "from-accent to-warning",
      icon: <Film className="h-10 w-10 text-white" />,
      action: "Watch Video",
      color: "bg-accent",
    },
    {
      id: "calculator",
      type: "Tool",
      title: "Token Distribution Calculator",
      description: "Calculate optimal token allocations for different stakeholders",
      meta: "Interactive",
      gradient: "from-warning to-error",
      icon: <Calculator className="h-10 w-10 text-white" />,
      action: "Open Tool",
      color: "bg-warning",
    },
  ];

  const articles: Article[] = [
    {
      id: "governance-tokens",
      title: "The Rise of Governance Tokens in DeFi",
      date: "2 days ago",
      description: "Exploring how governance tokens are shaping the future of decentralized finance protocols.",
      tags: ["DeFi", "Governance", "Tokens"],
      icon: <BookOpen className="text-primary" />,
      color: "bg-primary/20",
    },
    {
      id: "smart-contracts",
      title: "Best Practices for Smart Contract Security",
      date: "1 week ago",
      description: "A comprehensive guide to securing your smart contracts against common vulnerabilities.",
      tags: ["Security", "Smart Contracts", "Development"],
      icon: <BookOpen className="text-secondary" />,
      color: "bg-secondary/20",
    },
  ];

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <Card className="lg:col-span-1 bg-surface border-gray-700">
        <CardHeader className="border-b border-gray-700">
          <CardTitle>Resource Categories</CardTitle>
          <p className="text-sm text-gray-400 mt-1">Explore our Web3 knowledge base</p>
        </CardHeader>
        <CardContent className="p-0">
          {categories.map((category, index) => (
            <div key={category.id} className={index < categories.length - 1 ? "border-b border-gray-700" : ""}>
              <a href="#" className="flex items-center p-4 hover:bg-surface-light transition">
                <div className="w-8 h-8 rounded bg-surface-light flex items-center justify-center mr-3">
                  {category.icon}
                </div>
                <div>
                  <h3 className="font-medium">{category.name}</h3>
                  <p className="text-sm text-gray-400 mt-0.5">{category.count} resources</p>
                </div>
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-5 w-5 ml-auto text-gray-400"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fillRule="evenodd"
                    d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                    clipRule="evenodd"
                  />
                </svg>
              </a>
            </div>
          ))}
        </CardContent>
      </Card>

      <Card className="lg:col-span-2 bg-surface border-gray-700">
        <CardHeader className="border-b border-gray-700">
          <div className="flex justify-between items-center">
            <CardTitle>Featured Resources</CardTitle>
            <div className="relative">
              <Input
                type="text"
                placeholder="Search resources..."
                className="w-64 bg-background text-white border-gray-700"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
              <Search className="absolute right-3 top-2.5 h-4 w-4 text-gray-400" />
            </div>
          </div>
        </CardHeader>
        <CardContent className="p-5">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {featuredResources.map((resource) => (
              <div key={resource.id} className="bg-background rounded-lg border border-gray-700 overflow-hidden">
                <div className={`h-32 bg-gradient-to-r ${resource.gradient} flex items-center justify-center`}>
                  {resource.icon}
                </div>
                <div className="p-4">
                  <div className="flex justify-between items-center mb-2">
                    <span className={`text-xs ${resource.color}/20 text-${resource.color.replace('bg-', '')} px-2 py-0.5 rounded`}>
                      {resource.type}
                    </span>
                    <span className="text-xs text-gray-400">{resource.meta}</span>
                  </div>
                  <h3 className="font-medium mb-1">{resource.title}</h3>
                  <p className="text-sm text-gray-400 mb-3">{resource.description}</p>
                  <Button
                    className={`w-full bg-surface-light hover:${resource.color} text-white transition`}
                    variant="outline"
                  >
                    {resource.action}
                  </Button>
                </div>
              </div>
            ))}
          </div>

          <div className="mt-6">
            <h3 className="text-lg font-medium mb-4">Latest Articles</h3>

            <div className="space-y-4">
              {articles.map((article) => (
                <div key={article.id} className="bg-background rounded-lg border border-gray-700 p-4">
                  <div className="flex items-start">
                    <div className={`w-12 h-12 rounded ${article.color} flex items-center justify-center mr-4 flex-shrink-0`}>
                      {article.icon}
                    </div>
                    <div className="flex-1">
                      <div className="flex justify-between mb-1">
                        <h3 className="font-medium">{article.title}</h3>
                        <span className="text-xs text-gray-400">{article.date}</span>
                      </div>
                      <p className="text-sm text-gray-400 mb-2">{article.description}</p>
                      <div className="flex items-center">
                        {article.tags.map((tag, index) => (
                          <span
                            key={index}
                            className="text-xs px-2 py-0.5 rounded bg-surface-light text-gray-300 mr-2"
                          >
                            {tag}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
