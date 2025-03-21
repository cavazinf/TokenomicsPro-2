import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useToast } from "@/hooks/use-toast";

type BusinessModel = {
  id: string;
  name: string;
  description: string;
  revenue: string;
  complexity: "High" | "Medium" | "Low";
  selected: boolean;
};

export default function BusinessModels() {
  const { toast } = useToast();
  
  const [models, setModels] = useState<BusinessModel[]>([
    {
      id: "defi",
      name: "DeFi Protocol",
      description: "Decentralized finance platform with lending, borrowing, and yield optimization features",
      revenue: "Transaction fees, protocol fees",
      complexity: "High",
      selected: true,
    },
    {
      id: "nft",
      name: "NFT Marketplace",
      description: "Platform for creating, buying, and selling non-fungible tokens",
      revenue: "Sales fees, minting fees",
      complexity: "Medium",
      selected: false,
    },
    {
      id: "dao",
      name: "DAO Framework",
      description: "Governance platform enabling decentralized voting and treasury management",
      revenue: "Subscription, services",
      complexity: "Medium",
      selected: false,
    },
    {
      id: "gamefi",
      name: "GameFi Platform",
      description: "Gaming ecosystem with play-to-earn mechanics and in-game economies",
      revenue: "Item sales, subscriptions",
      complexity: "High",
      selected: false,
    },
  ]);

  const handleSelectModel = (id: string) => {
    setModels(
      models.map((model) => ({
        ...model,
        selected: model.id === id,
      }))
    );
  };

  const handleAnalyzeModel = () => {
    const selectedModel = models.find((model) => model.selected);
    toast({
      title: "Model Analysis Started",
      description: `Analyzing fit for ${selectedModel?.name}`,
    });
  };

  return (
    <Card className="bg-surface border-gray-700">
      <CardHeader className="border-b border-gray-700">
        <CardTitle>Web3 Business Models</CardTitle>
        <CardDescription className="text-gray-400">Select and customize your business model</CardDescription>
      </CardHeader>
      <CardContent className="p-5 space-y-4">
        {models.map((model) => (
          <div
            key={model.id}
            className={`${
              model.selected ? "bg-primary/10 border-primary/30" : "bg-background border-gray-700"
            } rounded-lg p-4 border`}
          >
            <div className="flex items-center justify-between mb-2">
              <h3 className="font-medium">{model.name}</h3>
              {model.selected ? (
                <span className="text-xs bg-primary/20 text-primary px-2 py-0.5 rounded">Selected</span>
              ) : (
                <button
                  onClick={() => handleSelectModel(model.id)}
                  className="text-xs text-primary"
                >
                  Select
                </button>
              )}
            </div>
            <p className="text-sm text-gray-400 mb-3">{model.description}</p>
            <div className="flex justify-between text-xs text-gray-400">
              <span>Revenue: {model.revenue}</span>
              <span>Complexity: {model.complexity}</span>
            </div>
          </div>
        ))}

        <Button onClick={handleAnalyzeModel} className="w-full bg-accent hover:bg-accent/90">
          Analyze Model Fit
        </Button>
      </CardContent>
    </Card>
  );
}
