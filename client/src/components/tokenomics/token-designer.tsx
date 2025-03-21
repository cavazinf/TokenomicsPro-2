import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { useToast } from "@/hooks/use-toast";

const TOKEN_TYPES = [
  { value: "utility", label: "Utility Token" },
  { value: "governance", label: "Governance Token" },
  { value: "security", label: "Security Token" },
  { value: "nft", label: "NFT" },
];

const SUPPLY_MODELS = [
  { value: "fixed", label: "Fixed Supply" },
  { value: "capped", label: "Capped Supply" },
  { value: "inflationary", label: "Inflationary" },
  { value: "deflationary", label: "Deflationary" },
];

const TOKEN_STANDARDS = ["ERC-20", "ERC-721", "ERC-1155"];

export default function TokenDesigner() {
  const { toast } = useToast();
  const [tokenType, setTokenType] = useState("utility");
  const [supplyModel, setSupplyModel] = useState("fixed");
  const [initialSupply, setInitialSupply] = useState("100,000,000");
  const [tokenStandard, setTokenStandard] = useState("ERC-20");

  const handleDesignToken = () => {
    toast({
      title: "Token Design Saved",
      description: "Your token design has been created successfully.",
    });
  };

  return (
    <Card className="bg-surface border-gray-700">
      <CardHeader className="border-b border-gray-700">
        <CardTitle>Token Designer</CardTitle>
        <CardDescription className="text-gray-400">Create and customize your token model</CardDescription>
      </CardHeader>
      <CardContent className="p-5 space-y-4">
        <div>
          <Label className="text-sm font-medium mb-1">Token Type</Label>
          <Select value={tokenType} onValueChange={setTokenType}>
            <SelectTrigger className="w-full bg-background text-white border-gray-700">
              <SelectValue placeholder="Select token type" />
            </SelectTrigger>
            <SelectContent className="bg-background border-gray-700">
              {TOKEN_TYPES.map((type) => (
                <SelectItem key={type.value} value={type.value} className="text-white hover:bg-surface-light">
                  {type.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div>
          <Label className="text-sm font-medium mb-1">Supply Model</Label>
          <Select value={supplyModel} onValueChange={setSupplyModel}>
            <SelectTrigger className="w-full bg-background text-white border-gray-700">
              <SelectValue placeholder="Select supply model" />
            </SelectTrigger>
            <SelectContent className="bg-background border-gray-700">
              {SUPPLY_MODELS.map((model) => (
                <SelectItem key={model.value} value={model.value} className="text-white hover:bg-surface-light">
                  {model.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div>
          <Label className="text-sm font-medium mb-1">Initial Supply</Label>
          <Input
            type="text"
            value={initialSupply}
            onChange={(e) => setInitialSupply(e.target.value)}
            className="w-full bg-background text-white border-gray-700"
          />
        </div>

        <div>
          <Label className="text-sm font-medium mb-1">Token Standard</Label>
          <div className="flex space-x-2">
            {TOKEN_STANDARDS.map((standard) => (
              <Button
                key={standard}
                type="button"
                className={`flex-1 ${
                  tokenStandard === standard
                    ? "bg-primary/10 border-primary/30 text-white"
                    : "bg-background border-gray-700 text-gray-300"
                }`}
                variant="outline"
                onClick={() => setTokenStandard(standard)}
              >
                {standard}
              </Button>
            ))}
          </div>
        </div>

        <Button onClick={handleDesignToken} className="w-full bg-primary hover:bg-primary/90">
          Design Token
        </Button>
      </CardContent>
    </Card>
  );
}
