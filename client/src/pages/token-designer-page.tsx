import React, { useState } from 'react';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Textarea } from "@/components/ui/textarea";
import { Slider } from "@/components/ui/slider";
import { Check, HelpCircle } from "lucide-react";

export default function TokenDesigner() {
  const [activeTab, setActiveTab] = useState("basics");
  const [formData, setFormData] = useState({
    name: "",
    symbol: "",
    totalSupply: "100000000",
    tokenType: "utility",
    tokenStandard: "erc20",
    initialPrice: "0.1",
    description: "",
    customFeatures: [] as string[],
    supplyModel: "fixed",
    inflationRate: 0,
    maxSupply: "100000000",
    utility: [] as string[],
    governance: false,
    transferRestrictions: false,
  });

  const handleInputChange = (field: string, value: string | number | boolean) => {
    setFormData({
      ...formData,
      [field]: value,
    });
  };

  const handleFeatureToggle = (feature: string) => {
    setFormData((prev) => {
      const features = [...prev.customFeatures];
      if (features.includes(feature)) {
        return {
          ...prev,
          customFeatures: features.filter(f => f !== feature),
        };
      } else {
        return {
          ...prev,
          customFeatures: [...features, feature],
        };
      }
    });
  };

  const handleUtilityToggle = (utility: string) => {
    setFormData((prev) => {
      const utilities = [...prev.utility];
      if (utilities.includes(utility)) {
        return {
          ...prev,
          utility: utilities.filter(u => u !== utility),
        };
      } else {
        return {
          ...prev,
          utility: [...utilities, utility],
        };
      }
    });
  };

  const isFeatureSelected = (feature: string) => {
    return formData.customFeatures.includes(feature);
  };

  const isUtilitySelected = (utility: string) => {
    return formData.utility.includes(utility);
  };

  const tokenTypes = [
    { value: "utility", label: "Utility Token" },
    { value: "security", label: "Security Token" },
    { value: "governance", label: "Governance Token" },
    { value: "stablecoin", label: "Stablecoin" },
    { value: "nft", label: "Non-Fungible Token (NFT)" },
  ];

  const tokenStandards = [
    { value: "erc20", label: "ERC-20 (Ethereum)" },
    { value: "bep20", label: "BEP-20 (Binance Smart Chain)" },
    { value: "erc721", label: "ERC-721 (NFT)" },
    { value: "erc1155", label: "ERC-1155 (Multi Token)" },
    { value: "spl", label: "SPL (Solana)" },
  ];

  const supplyModels = [
    { value: "fixed", label: "Fixed Supply" },
    { value: "inflationary", label: "Inflationary" },
    { value: "deflationary", label: "Deflationary" },
    { value: "elastic", label: "Elastic Supply" },
  ];

  const customFeatures = [
    { id: "staking", label: "Staking Mechanism" },
    { id: "burn", label: "Token Burning" },
    { id: "vesting", label: "Vesting Schedule" },
    { id: "voting", label: "Governance Voting" },
    { id: "fees", label: "Transaction Fees" },
    { id: "rewards", label: "Rewards System" },
  ];

  const utilityOptions = [
    { id: "access", label: "Access to Service/Platform" },
    { id: "payment", label: "Payment Token" },
    { id: "discounts", label: "Discounts and Benefits" },
    { id: "staking_rewards", label: "Staking Rewards" },
    { id: "nft_access", label: "NFT Access/Purchase" },
  ];

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight">Token Design</h1>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Token Designer</CardTitle>
          <CardDescription>Design your token from scratch or use a template</CardDescription>
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid grid-cols-4 w-full">
              <TabsTrigger value="basics">Basic Details</TabsTrigger>
              <TabsTrigger value="economics">Economics</TabsTrigger>
              <TabsTrigger value="utility">Utility & Features</TabsTrigger>
              <TabsTrigger value="review">Review & Export</TabsTrigger>
            </TabsList>
          </Tabs>
        </CardHeader>
        <CardContent>
          <TabsContent value="basics" className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="tokenName">Token Name</Label>
                <Input 
                  id="tokenName" 
                  placeholder="e.g. My Token" 
                  value={formData.name}
                  onChange={(e) => handleInputChange("name", e.target.value)}
                />
                <p className="text-sm text-muted-foreground">
                  Full name of your token (e.g. "Ethereum")
                </p>
              </div>
              <div className="space-y-2">
                <Label htmlFor="tokenSymbol">Token Symbol</Label>
                <Input 
                  id="tokenSymbol" 
                  placeholder="e.g. MTK" 
                  maxLength={5}
                  value={formData.symbol}
                  onChange={(e) => handleInputChange("symbol", e.target.value)}
                />
                <p className="text-sm text-muted-foreground">
                  Short symbol for your token (e.g. "ETH")
                </p>
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="tokenType">Token Type</Label>
              <Select 
                value={formData.tokenType}
                onValueChange={(value) => handleInputChange("tokenType", value)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select token type" />
                </SelectTrigger>
                <SelectContent>
                  {tokenTypes.map((type) => (
                    <SelectItem key={type.value} value={type.value}>
                      {type.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <p className="text-sm text-muted-foreground">
                The primary classification of your token
              </p>
            </div>

            <div className="space-y-2">
              <Label htmlFor="tokenStandard">Token Standard</Label>
              <Select 
                value={formData.tokenStandard}
                onValueChange={(value) => handleInputChange("tokenStandard", value)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select token standard" />
                </SelectTrigger>
                <SelectContent>
                  {tokenStandards.map((standard) => (
                    <SelectItem key={standard.value} value={standard.value}>
                      {standard.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <p className="text-sm text-muted-foreground">
                The technical standard your token will implement
              </p>
            </div>

            <div className="space-y-2">
              <Label htmlFor="tokenDescription">Token Description</Label>
              <Textarea 
                id="tokenDescription" 
                placeholder="Describe your token's purpose and value proposition..."
                value={formData.description}
                onChange={(e) => handleInputChange("description", e.target.value)}
                rows={4}
              />
              <p className="text-sm text-muted-foreground">
                A clear description of your token's purpose and utility
              </p>
            </div>

            <div className="flex justify-end">
              <Button onClick={() => setActiveTab("economics")}>
                Next: Economics
              </Button>
            </div>
          </TabsContent>

          <TabsContent value="economics" className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="supplyModel">Supply Model</Label>
              <RadioGroup 
                value={formData.supplyModel} 
                onValueChange={(value) => handleInputChange("supplyModel", value)}
                className="grid grid-cols-2 gap-4"
              >
                {supplyModels.map((model) => (
                  <div key={model.value} className="flex items-center space-x-2 border rounded-lg p-4">
                    <RadioGroupItem value={model.value} id={`supplyModel-${model.value}`} />
                    <Label htmlFor={`supplyModel-${model.value}`} className="cursor-pointer font-medium">
                      {model.label}
                    </Label>
                  </div>
                ))}
              </RadioGroup>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="totalSupply">
                  {formData.supplyModel === "fixed" ? "Total Supply" : "Initial Supply"}
                </Label>
                <Input 
                  id="totalSupply" 
                  type="text"
                  value={formData.totalSupply}
                  onChange={(e) => handleInputChange("totalSupply", e.target.value)}
                />
                <p className="text-sm text-muted-foreground">
                  {formData.supplyModel === "fixed" 
                    ? "The fixed total supply of tokens" 
                    : "The initial amount of tokens at launch"}
                </p>
              </div>

              {formData.supplyModel === "inflationary" && (
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <Label htmlFor="inflationRate">Inflation Rate (%/year)</Label>
                    <span>{formData.inflationRate}%</span>
                  </div>
                  <Slider
                    id="inflationRate"
                    min={0}
                    max={20}
                    step={0.1}
                    value={[formData.inflationRate as number]}
                    onValueChange={(value) => handleInputChange("inflationRate", value[0])}
                  />
                  <p className="text-sm text-muted-foreground">
                    Annual rate at which new tokens are created
                  </p>
                </div>
              )}

              {formData.supplyModel !== "fixed" && (
                <div className="space-y-2">
                  <Label htmlFor="maxSupply">Maximum Supply (Optional)</Label>
                  <Input 
                    id="maxSupply" 
                    type="text"
                    value={formData.maxSupply}
                    onChange={(e) => handleInputChange("maxSupply", e.target.value)}
                  />
                  <p className="text-sm text-muted-foreground">
                    Hard cap on the total tokens that can ever exist
                  </p>
                </div>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="initialPrice">Initial Token Price (USD)</Label>
              <div className="flex items-center space-x-2">
                <span>$</span>
                <Input 
                  id="initialPrice" 
                  type="text"
                  value={formData.initialPrice}
                  onChange={(e) => handleInputChange("initialPrice", e.target.value)}
                />
              </div>
              <p className="text-sm text-muted-foreground">
                Estimated initial price in USD at token launch
              </p>
            </div>

            <div className="space-y-2 pt-4">
              <Label className="text-base font-medium">Custom Economic Features</Label>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-2">
                {customFeatures.map((feature) => (
                  <div 
                    key={feature.id}
                    className={`flex items-center p-3 border rounded-lg cursor-pointer transition-colors ${
                      isFeatureSelected(feature.id) ? 'bg-primary/10 border-primary' : ''
                    }`}
                    onClick={() => handleFeatureToggle(feature.id)}
                  >
                    <div className={`w-5 h-5 rounded-full flex items-center justify-center mr-2 ${
                      isFeatureSelected(feature.id) ? 'bg-primary text-primary-foreground' : 'bg-muted'
                    }`}>
                      {isFeatureSelected(feature.id) && <Check className="h-3 w-3" />}
                    </div>
                    <span>{feature.label}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="flex justify-between">
              <Button variant="outline" onClick={() => setActiveTab("basics")}>
                Back
              </Button>
              <Button onClick={() => setActiveTab("utility")}>
                Next: Utility & Features
              </Button>
            </div>
          </TabsContent>

          <TabsContent value="utility" className="space-y-4">
            <div className="space-y-2">
              <Label className="text-base font-medium">Token Utility</Label>
              <p className="text-sm text-muted-foreground">
                Select all the utilities your token will provide:
              </p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-2">
                {utilityOptions.map((utility) => (
                  <div 
                    key={utility.id}
                    className={`flex items-center p-3 border rounded-lg cursor-pointer transition-colors ${
                      isUtilitySelected(utility.id) ? 'bg-primary/10 border-primary' : ''
                    }`}
                    onClick={() => handleUtilityToggle(utility.id)}
                  >
                    <div className={`w-5 h-5 rounded-full flex items-center justify-center mr-2 ${
                      isUtilitySelected(utility.id) ? 'bg-primary text-primary-foreground' : 'bg-muted'
                    }`}>
                      {isUtilitySelected(utility.id) && <Check className="h-3 w-3" />}
                    </div>
                    <span>{utility.label}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="space-y-2 pt-4">
              <div className="flex items-center justify-between">
                <Label className="text-base font-medium">Governance Features</Label>
                <div
                  className={`w-12 h-6 flex items-center rounded-full p-1 cursor-pointer ${
                    formData.governance ? 'bg-primary justify-end' : 'bg-muted justify-start'
                  }`}
                  onClick={() => handleInputChange("governance", !formData.governance)}
                >
                  <div className="bg-white w-4 h-4 rounded-full shadow-md" />
                </div>
              </div>
              <p className="text-sm text-muted-foreground">
                Enable governance features (voting, proposals, etc.)
              </p>
            </div>

            <div className="space-y-2 pt-4">
              <div className="flex items-center justify-between">
                <Label className="text-base font-medium">Transfer Restrictions</Label>
                <div
                  className={`w-12 h-6 flex items-center rounded-full p-1 cursor-pointer ${
                    formData.transferRestrictions ? 'bg-primary justify-end' : 'bg-muted justify-start'
                  }`}
                  onClick={() => handleInputChange("transferRestrictions", !formData.transferRestrictions)}
                >
                  <div className="bg-white w-4 h-4 rounded-full shadow-md" />
                </div>
              </div>
              <p className="text-sm text-muted-foreground">
                Implement transfer restrictions (for regulatory compliance)
              </p>
            </div>

            <div className="flex justify-between">
              <Button variant="outline" onClick={() => setActiveTab("economics")}>
                Back
              </Button>
              <Button onClick={() => setActiveTab("review")}>
                Next: Review & Export
              </Button>
            </div>
          </TabsContent>

          <TabsContent value="review" className="space-y-4">
            <div className="border rounded-lg p-6 space-y-4">
              <div className="space-y-2">
                <h3 className="text-xl font-bold">{formData.name || "My Token"}</h3>
                <div className="flex items-center space-x-2">
                  <span className="bg-primary/20 text-primary px-2 py-1 rounded-md font-medium">
                    {formData.symbol || "TKN"}
                  </span>
                  <span className="bg-secondary/20 text-secondary px-2 py-1 rounded-md text-xs">
                    {tokenTypes.find(t => t.value === formData.tokenType)?.label || "Utility Token"}
                  </span>
                  <span className="bg-muted px-2 py-1 rounded-md text-xs">
                    {tokenStandards.find(s => s.value === formData.tokenStandard)?.label || "ERC-20"}
                  </span>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-medium mb-2">Token Economics</h4>
                  <div className="space-y-1">
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Supply Model:</span>
                      <span>{supplyModels.find(m => m.value === formData.supplyModel)?.label}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Total Supply:</span>
                      <span>{parseInt(formData.totalSupply).toLocaleString()} tokens</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Initial Price:</span>
                      <span>${formData.initialPrice} USD</span>
                    </div>
                    {formData.supplyModel === "inflationary" && (
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">Inflation Rate:</span>
                        <span>{formData.inflationRate}% per year</span>
                      </div>
                    )}
                    {formData.supplyModel !== "fixed" && parseInt(formData.maxSupply) > 0 && (
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">Maximum Supply:</span>
                        <span>{parseInt(formData.maxSupply).toLocaleString()} tokens</span>
                      </div>
                    )}
                  </div>
                </div>

                <div>
                  <h4 className="font-medium mb-2">Token Features</h4>
                  <div className="space-y-1">
                    {formData.customFeatures.length > 0 ? (
                      formData.customFeatures.map((feature: string) => (
                        <div key={feature} className="flex items-center">
                          <Check className="h-4 w-4 mr-2 text-green-500" />
                          <span>
                            {customFeatures.find(f => f.id === feature)?.label}
                          </span>
                        </div>
                      ))
                    ) : (
                      <div className="text-muted-foreground">No special features selected</div>
                    )}
                  </div>

                  <h4 className="font-medium mb-2 mt-4">Token Utility</h4>
                  <div className="space-y-1">
                    {formData.utility.length > 0 ? (
                      formData.utility.map((utility: string) => (
                        <div key={utility} className="flex items-center">
                          <Check className="h-4 w-4 mr-2 text-green-500" />
                          <span>
                            {utilityOptions.find(u => u.id === utility)?.label}
                          </span>
                        </div>
                      ))
                    ) : (
                      <div className="text-muted-foreground">No utilities selected</div>
                    )}
                  </div>

                  {formData.governance && (
                    <div className="mt-2">
                      <div className="flex items-center">
                        <Check className="h-4 w-4 mr-2 text-green-500" />
                        <span>Governance Features Enabled</span>
                      </div>
                    </div>
                  )}

                  {formData.transferRestrictions && (
                    <div className="mt-2">
                      <div className="flex items-center">
                        <Check className="h-4 w-4 mr-2 text-green-500" />
                        <span>Transfer Restrictions Enabled</span>
                      </div>
                    </div>
                  )}
                </div>
              </div>

              {formData.description && (
                <div>
                  <h4 className="font-medium mb-2">Token Description</h4>
                  <p className="text-muted-foreground">{formData.description}</p>
                </div>
              )}
            </div>

            <div className="flex justify-between">
              <Button variant="outline" onClick={() => setActiveTab("utility")}>
                Back
              </Button>
              <div className="space-x-2">
                <Button variant="outline">Download JSON</Button>
                <Button>Save Token Model</Button>
              </div>
            </div>
          </TabsContent>
        </CardContent>
      </Card>
    </div>
  );
}