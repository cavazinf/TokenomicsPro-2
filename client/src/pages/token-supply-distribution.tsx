import React, { useState } from 'react';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Slider } from "@/components/ui/slider";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  PieChart,
  Pie,
  Cell,
  Legend,
  ResponsiveContainer,
  Tooltip,
} from 'recharts';
import { X, Plus, Copy, CheckCircle2 } from 'lucide-react';
import { useToast } from "@/hooks/use-toast";

interface TokenCategory {
  id: string;
  name: string;
  percentage: number;
  color: string;
}

export default function TokenSupplyDistribution() {
  const [totalSupply, setTotalSupply] = useState(100000000);
  const [categories, setCategories] = useState<TokenCategory[]>([
    { id: "1", name: "Team", percentage: 15, color: "#4f46e5" },
    { id: "2", name: "Private Sale", percentage: 20, color: "#0ea5e9" },
    { id: "3", name: "Public Sale", percentage: 10, color: "#10b981" },
    { id: "4", name: "Marketing", percentage: 15, color: "#f59e0b" },
    { id: "5", name: "Ecosystem", percentage: 20, color: "#ef4444" },
    { id: "6", name: "Treasury", percentage: 20, color: "#8b5cf6" },
  ]);
  const [newCategoryName, setNewCategoryName] = useState("");
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

  const { toast } = useToast();
  
  const totalPercentage = categories.reduce((sum, cat) => sum + cat.percentage, 0);
  const isValidDistribution = totalPercentage === 100;

  const handleTotalSupplyChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseInt(e.target.value);
    if (!isNaN(value) && value > 0) {
      setTotalSupply(value);
    }
  };

  const handleCategorySelect = (id: string) => {
    setSelectedCategory(id === selectedCategory ? null : id);
  };

  const handleCategoryChange = (id: string, percentage: number) => {
    setCategories(
      categories.map((cat) =>
        cat.id === id ? { ...cat, percentage } : cat
      )
    );
  };

  const handleCategoryNameChange = (id: string, name: string) => {
    setCategories(
      categories.map((cat) =>
        cat.id === id ? { ...cat, name } : cat
      )
    );
  };

  const handleAddCategory = () => {
    if (!newCategoryName.trim()) {
      toast({
        title: "Nome inválido",
        description: "Por favor, insira um nome para a categoria.",
        variant: "destructive",
      });
      return;
    }

    const colors = [
      "#4f46e5", "#0ea5e9", "#10b981", "#f59e0b", "#ef4444", 
      "#8b5cf6", "#ec4899", "#06b6d4", "#84cc16", "#14b8a6"
    ];
    
    const newId = (parseInt(categories[categories.length - 1]?.id || "0") + 1).toString();
    const colorIndex = categories.length % colors.length;
    
    setCategories([
      ...categories,
      {
        id: newId,
        name: newCategoryName,
        percentage: 0,
        color: colors[colorIndex],
      },
    ]);
    
    setNewCategoryName("");
    setSelectedCategory(newId);
  };

  const handleRemoveCategory = (id: string) => {
    setCategories(categories.filter((cat) => cat.id !== id));
    if (selectedCategory === id) {
      setSelectedCategory(null);
    }
  };

  const balanceDistribution = () => {
    const deficit = 100 - totalPercentage;
    if (deficit === 0) return;

    const updatedCategories = [...categories];
    
    // Se for um déficit positivo (total < 100%), adiciona ao primeiro item
    if (deficit > 0 && updatedCategories.length > 0) {
      updatedCategories[0].percentage += deficit;
    } 
    // Se for um déficit negativo (total > 100%), reduz proporcionalmente
    else if (deficit < 0) {
      const excess = -deficit;
      let remaining = excess;
      
      // Primeiro tenta reduzir proporcionalmente
      for (let i = 0; i < updatedCategories.length && remaining > 0; i++) {
        const cat = updatedCategories[i];
        const reduction = Math.min(cat.percentage, Math.ceil(cat.percentage / totalPercentage * excess));
        cat.percentage -= reduction;
        remaining -= reduction;
      }
      
      // Se ainda houver excesso, reduz do último
      if (remaining > 0 && updatedCategories.length > 0) {
        const lastCat = updatedCategories[updatedCategories.length - 1];
        lastCat.percentage = Math.max(0, lastCat.percentage - remaining);
      }
    }
    
    setCategories(updatedCategories);
  };

  const copyToClipboard = () => {
    const distributionData = categories.map(cat => 
      `${cat.name}: ${cat.percentage}% (${(totalSupply * cat.percentage / 100).toLocaleString()} tokens)`
    ).join('\n');
    
    const fullText = `Token Distribution for ${totalSupply.toLocaleString()} tokens\n\n${distributionData}`;
    
    navigator.clipboard.writeText(fullText).then(() => {
      toast({
        title: "Copiado para a área de transferência",
        description: "A distribuição de tokens foi copiada com sucesso.",
      });
    });
  };

  const distributionData = categories.map((cat) => ({
    name: cat.name,
    value: cat.percentage,
    tokens: totalSupply * (cat.percentage / 100),
    color: cat.color,
  }));

  const formatNumber = (num: number) => {
    if (num >= 1000000000) {
      return (num / 1000000000).toFixed(1) + 'B';
    }
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M';
    }
    if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K';
    }
    return num.toFixed(2);
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight">Token Supply & Distribution</h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-1">
          <CardHeader>
            <CardTitle>Supply Configuration</CardTitle>
            <CardDescription>Define your token's total supply and distribution</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="totalSupply">Total Supply</Label>
              <Input
                id="totalSupply"
                type="number"
                value={totalSupply}
                onChange={handleTotalSupplyChange}
                min={1}
              />
              <p className="text-sm text-muted-foreground">
                {totalSupply.toLocaleString()} tokens
              </p>
            </div>

            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <Label>Token Distribution</Label>
                <span className={`text-sm font-medium ${isValidDistribution ? 'text-green-500' : 'text-red-500'}`}>
                  {totalPercentage}%
                </span>
              </div>
              
              <div className="space-y-3 max-h-[360px] overflow-y-auto pr-2">
                {categories.map((category) => (
                  <div
                    key={category.id}
                    className={`p-3 border rounded-md cursor-pointer transition-colors ${
                      selectedCategory === category.id ? 'border-primary' : ''
                    }`}
                    onClick={() => handleCategorySelect(category.id)}
                  >
                    <div className="flex items-start">
                      <div 
                        className="w-4 h-4 rounded-full mt-1 mr-2" 
                        style={{ backgroundColor: category.color }}
                      />
                      <div className="flex-1">
                        {selectedCategory === category.id ? (
                          <Input
                            value={category.name}
                            onChange={(e) => handleCategoryNameChange(category.id, e.target.value)}
                            className="mb-2"
                            autoFocus
                          />
                        ) : (
                          <div className="font-medium mb-2">{category.name}</div>
                        )}

                        <div className="flex items-center gap-2">
                          <div className="flex-1">
                            <Slider
                              value={[category.percentage]}
                              max={100}
                              step={1}
                              onValueChange={(values) => handleCategoryChange(category.id, values[0])}
                            />
                          </div>
                          <div className="text-sm font-medium w-12 text-right">
                            {category.percentage}%
                          </div>
                        </div>
                        <div className="mt-1 text-xs text-muted-foreground">
                          {(totalSupply * category.percentage / 100).toLocaleString()} tokens
                        </div>
                      </div>
                      
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-6 w-6 text-muted-foreground hover:text-foreground"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleRemoveCategory(category.id);
                        }}
                      >
                        <X className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="flex gap-2">
              <Input
                placeholder="Nova categoria"
                value={newCategoryName}
                onChange={(e) => setNewCategoryName(e.target.value)}
                className="flex-1"
              />
              <Button variant="outline" onClick={handleAddCategory}>
                <Plus className="h-4 w-4 mr-1" />
                Adicionar
              </Button>
            </div>
            
            <div className="flex gap-2">
              <Button
                variant="outline" 
                className="flex-1"
                disabled={isValidDistribution}
                onClick={balanceDistribution}
              >
                {isValidDistribution ? (
                  <>
                    <CheckCircle2 className="h-4 w-4 mr-1 text-green-500" />
                    Distribuição balanceada
                  </>
                ) : (
                  "Balancear para 100%"
                )}
              </Button>
              
              <Button
                variant="outline"
                onClick={copyToClipboard}
                className="flex-1"
              >
                <Copy className="h-4 w-4 mr-1" />
                Copiar
              </Button>
            </div>
          </CardContent>
        </Card>

        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Token Distribution Overview</CardTitle>
            <CardDescription>
              Visual representation of your token's allocation
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[400px]">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={distributionData}
                    dataKey="value"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    outerRadius={150}
                    labelLine={true}
                    label={(entry) => `${entry.name}: ${entry.value}%`}
                  >
                    {distributionData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip 
                    formatter={(value: number, name: string, props: any) => [
                      `${value}% (${formatNumber(props.payload.tokens)} tokens)`,
                      name
                    ]}
                  />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>

            <div className="mt-4">
              <h3 className="text-lg font-medium mb-2">Detailed Allocation</h3>
              <div className="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Category</TableHead>
                      <TableHead className="text-right">Percentage</TableHead>
                      <TableHead className="text-right">Token Amount</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {categories.map((category) => (
                      <TableRow key={category.id}>
                        <TableCell className="flex items-center">
                          <div 
                            className="w-3 h-3 rounded-full mr-2" 
                            style={{ backgroundColor: category.color }}
                          />
                          {category.name}
                        </TableCell>
                        <TableCell className="text-right">{category.percentage}%</TableCell>
                        <TableCell className="text-right">
                          {(totalSupply * category.percentage / 100).toLocaleString()}
                        </TableCell>
                      </TableRow>
                    ))}
                    <TableRow>
                      <TableCell className="font-medium">Total</TableCell>
                      <TableCell className={`text-right font-medium ${isValidDistribution ? 'text-green-500' : 'text-red-500'}`}>
                        {totalPercentage}%
                      </TableCell>
                      <TableCell className="text-right font-medium">
                        {(totalSupply * totalPercentage / 100).toLocaleString()}
                      </TableCell>
                    </TableRow>
                  </TableBody>
                </Table>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}