import React, { useState } from 'react';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
  CardFooter
} from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Slider } from "@/components/ui/slider";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { Separator } from "@/components/ui/separator";
import { ScrollArea } from "@/components/ui/scroll-area";
import { 
  TrendingUp, 
  TrendingDown,
  BarChart as BarChartIcon, 
  PieChart as PieChartIcon, 
  AlertTriangle, 
  Download, 
  RefreshCw, 
  Activity,
  ArrowDownRight,
  ArrowUpRight,
  Play,
  Pause,
  Save
} from 'lucide-react';

export default function MarketStressTest() {
  const [activeTab, setActiveTab] = useState("simulation");
  const [simulationRunning, setSimulationRunning] = useState(false);
  const [simulationSpeed, setSimulationSpeed] = useState(1);
  const [currentDay, setCurrentDay] = useState(0);
  const [marketSentiment, setMarketSentiment] = useState(50); // 0-100 scale
  const [volatility, setVolatility] = useState(25); // 0-100 scale
  const [crashChance, setCrashChance] = useState(5); // 0-100 scale
  const [stressScenario, setStressScenario] = useState("market_crash");
  const [initialPrice, setInitialPrice] = useState(100);
  
  // Dados simulados de preço
  const [priceData, setPriceData] = useState([
    { day: 0, price: 100, volume: 1000000, holders: 10000, market_cap: 100000000 }
  ]);
  
  // Definindo o tipo para o evento
  type MarketEvent = {
    id: string;
    name: string;
    description: string;
    impact: number;
    duration: number;
    probability: number;
  };
  
  // Evento atual
  const [currentEvent, setCurrentEvent] = useState<MarketEvent | null>(null);

  // Cenários de estresse disponíveis
  const stressScenarios = [
    { id: "market_crash", name: "Crash de Mercado", description: "Simulação de queda acentuada de preços no mercado geral" },
    { id: "liquidity_crisis", name: "Crise de Liquidez", description: "Simulação de escassez de liquidez e aumento da volatilidade" },
    { id: "regulatory_shock", name: "Choque Regulatório", description: "Simulação de impacto de novas regulamentações restritivas" },
    { id: "security_breach", name: "Falha de Segurança", description: "Simulação de hack ou vulnerabilidade de segurança" },
    { id: "whale_dump", name: "Venda Massiva de Whales", description: "Simulação de grandes investidores vendendo simultaneamente" },
  ];

  // Eventos de mercado que podem ocorrer durante a simulação
  const marketEvents = [
    { 
      id: "crash", 
      name: "Crash de Mercado", 
      description: "Queda súbita nos preços dos ativos criptográficos",
      impact: -25, // Porcentagem de impacto no preço
      duration: 7, // Duração em dias
      probability: 0.02 // Probabilidade por dia
    },
    { 
      id: "recovery", 
      name: "Recuperação de Mercado", 
      description: "Recuperação do preço após um período de queda",
      impact: 15,
      duration: 14,
      probability: 0.03
    },
    { 
      id: "regulatory_news", 
      name: "Notícias Regulatórias", 
      description: "Anúncio de novas regulamentações para criptomoedas",
      impact: -12,
      duration: 5,
      probability: 0.04
    },
    { 
      id: "adoption_news", 
      name: "Notícias de Adoção", 
      description: "Grande empresa ou país anuncia adoção de criptomoedas",
      impact: 18,
      duration: 10,
      probability: 0.03
    },
    { 
      id: "security_breach", 
      name: "Falha de Segurança", 
      description: "Hack ou vulnerabilidade descoberta em protocolo importante",
      impact: -20,
      duration: 8,
      probability: 0.02
    }
  ];

  // Resultados do teste de estresse
  const stressTestResults = {
    maxDrawdown: "43.8%",
    recoveryTime: "87 dias",
    volatilityIncrease: "148%",
    liquidityDecrease: "65%",
    holdersDecrease: "28%",
    failedScenarios: 2,
    passedScenarios: 3,
    recommendation: "Implementar reservas de liquidez e melhorar mecanismos de estabilidade de preço"
  };

  // Função para iniciar ou pausar a simulação
  const toggleSimulation = () => {
    setSimulationRunning(!simulationRunning);
  };

  // Função para resetar a simulação
  const resetSimulation = () => {
    setSimulationRunning(false);
    setCurrentDay(0);
    setPriceData([
      { day: 0, price: initialPrice, volume: 1000000, holders: 10000, market_cap: initialPrice * 1000000 }
    ]);
    setCurrentEvent(null);
  };

  // Função para aplicar o cenário de estresse selecionado
  const applyStressScenario = () => {
    resetSimulation();
    // Aqui aplicaríamos configurações específicas para o cenário selecionado
    switch(stressScenario) {
      case 'market_crash':
        setVolatility(75);
        setMarketSentiment(20);
        break;
      case 'liquidity_crisis':
        setVolatility(60);
        setMarketSentiment(35);
        break;
      case 'regulatory_shock':
        setVolatility(50);
        setMarketSentiment(25);
        break;
      case 'security_breach':
        setVolatility(65);
        setMarketSentiment(15);
        break;
      case 'whale_dump':
        setVolatility(70);
        setMarketSentiment(30);
        break;
      default:
        setVolatility(25);
        setMarketSentiment(50);
    }
  };

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#9370DB', '#FF6B6B'];

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight">Market Stress Test</h1>
        <div className="flex items-center space-x-2">
          <Button variant="outline" onClick={resetSimulation}>Resetar</Button>
          <Button onClick={toggleSimulation}>
            {simulationRunning ? 
              <><Pause className="h-4 w-4 mr-2" /> Pausar</> : 
              <><Play className="h-4 w-4 mr-2" /> Iniciar</>}
          </Button>
        </div>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="grid grid-cols-3 w-full max-w-2xl">
          <TabsTrigger value="simulation">Simulação</TabsTrigger>
          <TabsTrigger value="scenarios">Cenários</TabsTrigger>
          <TabsTrigger value="results">Resultados</TabsTrigger>
        </TabsList>
        
        <TabsContent value="simulation" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-base font-medium">Preço Atual</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">${priceData[priceData.length - 1].price.toFixed(2)}</div>
                <p className="text-xs text-muted-foreground">
                  Dia: {currentDay} | 
                  {priceData.length > 1 ? 
                    (priceData[priceData.length - 1].price > priceData[priceData.length - 2].price ? 
                      <span className="text-green-500 flex items-center"><ArrowUpRight className="h-3 w-3 mr-1" />+{((priceData[priceData.length - 1].price / priceData[priceData.length - 2].price - 1) * 100).toFixed(2)}%</span> : 
                      <span className="text-red-500 flex items-center"><ArrowDownRight className="h-3 w-3 mr-1" />{((priceData[priceData.length - 1].price / priceData[priceData.length - 2].price - 1) * 100).toFixed(2)}%</span>
                    ) : 
                    <span>-</span>
                  }
                </p>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-base font-medium">Volume 24h</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{(priceData[priceData.length - 1].volume / 1000000).toFixed(2)}M</div>
                <p className="text-xs text-muted-foreground">Holders: {priceData[priceData.length - 1].holders.toLocaleString()}</p>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-base font-medium">Market Cap</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">${(priceData[priceData.length - 1].market_cap / 1000000).toFixed(2)}M</div>
                <p className="text-xs text-muted-foreground">Sentimento: {marketSentiment < 30 ? "Bearish" : marketSentiment > 70 ? "Bullish" : "Neutral"}</p>
              </CardContent>
            </Card>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card className="col-span-2">
              <CardHeader>
                <CardTitle className="text-base font-medium">Simulação de Preço</CardTitle>
                {currentEvent && (
                  <div className="mt-2 p-2 border rounded-md bg-yellow-50 text-yellow-700 text-sm flex items-center">
                    <AlertTriangle className="h-4 w-4 mr-2" />
                    <div>
                      <strong>{currentEvent.name}</strong>: {currentEvent.description}
                      <div className="text-xs mt-1">Impacto: {currentEvent.impact > 0 ? "+" : ""}{currentEvent.impact}% | Duração: {currentEvent.duration} dias</div>
                    </div>
                  </div>
                )}
              </CardHeader>
              <CardContent>
                <div className="h-80">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={priceData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="day" label={{ value: 'Dia', position: 'insideBottomRight', offset: -5 }} />
                      <YAxis label={{ value: 'Preço ($)', angle: -90, position: 'insideLeft' }} />
                      <Tooltip formatter={(value) => [`$${value}`, 'Preço']} />
                      <Legend />
                      <Line type="monotone" dataKey="price" stroke="#8884d8" activeDot={{ r: 8 }} name="Preço ($)" />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="text-base font-medium">Parâmetros de Simulação</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <Label htmlFor="initialPrice">Preço Inicial ($)</Label>
                      <span>${initialPrice}</span>
                    </div>
                    <Input 
                      id="initialPrice" 
                      type="number" 
                      value={initialPrice.toString()} 
                      onChange={(e) => setInitialPrice(parseFloat(e.target.value))}
                      min="1"
                      max="10000"
                    />
                  </div>
                
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <Label htmlFor="volatility">Volatilidade</Label>
                      <span>{volatility}%</span>
                    </div>
                    <Slider 
                      id="volatility" 
                      value={[volatility]} 
                      onValueChange={(values) => setVolatility(values[0])} 
                      min={1} 
                      max={100} 
                      step={1}
                    />
                  </div>
                
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <Label htmlFor="sentiment">Sentimento de Mercado</Label>
                      <span>{marketSentiment < 30 ? "Bearish" : marketSentiment > 70 ? "Bullish" : "Neutral"} ({marketSentiment})</span>
                    </div>
                    <Slider 
                      id="sentiment" 
                      value={[marketSentiment]} 
                      onValueChange={(values) => setMarketSentiment(values[0])} 
                      min={1} 
                      max={100} 
                      step={1}
                    />
                  </div>
                
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <Label htmlFor="speed">Velocidade de Simulação</Label>
                      <span>{simulationSpeed}x</span>
                    </div>
                    <Slider 
                      id="speed" 
                      value={[simulationSpeed]} 
                      onValueChange={(values) => setSimulationSpeed(values[0])} 
                      min={1} 
                      max={10} 
                      step={1}
                    />
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader>
                <CardTitle className="text-base font-medium">Eventos de Mercado</CardTitle>
              </CardHeader>
              <CardContent>
                <ScrollArea className="h-[300px] pr-4">
                  <div className="space-y-4">
                    {marketEvents.map((event) => (
                      <div key={event.id} className="border rounded-md p-3 space-y-2">
                        <div className="flex justify-between items-center">
                          <h4 className="font-medium text-sm">{event.name}</h4>
                          <span className={`text-xs px-2 py-1 rounded-full ${event.impact > 0 ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                            {event.impact > 0 ? `+${event.impact}%` : `${event.impact}%`}
                          </span>
                        </div>
                        <p className="text-xs text-muted-foreground">{event.description}</p>
                        <div className="flex justify-between text-xs text-muted-foreground">
                          <span>Duração: {event.duration} dias</span>
                          <span>Prob: {(event.probability * 100).toFixed(1)}%</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </ScrollArea>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
        
        <TabsContent value="scenarios" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Cenários de Teste de Estresse</CardTitle>
              <CardDescription>
                Selecione um cenário para testar a resiliência do seu token em diferentes condições de mercado
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="scenario">Cenário de Estresse</Label>
                  <Select value={stressScenario} onValueChange={setStressScenario}>
                    <SelectTrigger>
                      <SelectValue placeholder="Selecione um cenário" />
                    </SelectTrigger>
                    <SelectContent>
                      {stressScenarios.map((scenario) => (
                        <SelectItem key={scenario.id} value={scenario.id}>
                          {scenario.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                
                <div className="border rounded-md p-4 bg-muted/30">
                  <h4 className="font-medium mb-2">
                    {stressScenarios.find(s => s.id === stressScenario)?.name}
                  </h4>
                  <p className="text-sm text-muted-foreground mb-4">
                    {stressScenarios.find(s => s.id === stressScenario)?.description}
                  </p>
                  
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <p className="font-medium mb-1">Parâmetros de Simulação</p>
                      <ul className="list-disc list-inside text-muted-foreground space-y-1">
                        <li>Alta volatilidade</li>
                        <li>Sentimento de mercado negativo</li>
                        <li>Probabilidade aumentada de eventos negativos</li>
                      </ul>
                    </div>
                    
                    <div>
                      <p className="font-medium mb-1">Fatores de Risco</p>
                      <ul className="list-disc list-inside text-muted-foreground space-y-1">
                        <li>Queda acentuada de preço</li>
                        <li>Perda de liquidez</li>
                        <li>Redução no número de holders</li>
                      </ul>
                    </div>
                  </div>
                </div>
                
                <Button onClick={applyStressScenario} className="w-full">
                  Aplicar Cenário
                </Button>
              </div>
            </CardContent>
          </Card>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-base">Métricas de Avaliação</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2 border rounded-md p-3">
                      <Label className="text-xs">Drawdown Máximo</Label>
                      <div className="text-xl font-bold">-43.8%</div>
                    </div>
                    
                    <div className="space-y-2 border rounded-md p-3">
                      <Label className="text-xs">Tempo de Recuperação</Label>
                      <div className="text-xl font-bold">87 dias</div>
                    </div>
                    
                    <div className="space-y-2 border rounded-md p-3">
                      <Label className="text-xs">Impacto na Liquidez</Label>
                      <div className="text-xl font-bold">-65%</div>
                    </div>
                    
                    <div className="space-y-2 border rounded-md p-3">
                      <Label className="text-xs">Perda de Holders</Label>
                      <div className="text-xl font-bold">-28%</div>
                    </div>
                  </div>
                  
                  <div className="border-t pt-4">
                    <Label className="text-xs mb-2 block">Critérios de Aprovação</Label>
                    <ul className="space-y-2">
                      <li className="flex items-center text-sm">
                        <div className="w-5 h-5 rounded-full bg-green-500 flex items-center justify-center mr-2">
                          <span className="text-white text-xs">✓</span>
                        </div>
                        Drawdown máximo &lt; 50%
                      </li>
                      <li className="flex items-center text-sm">
                        <div className="w-5 h-5 rounded-full bg-red-500 flex items-center justify-center mr-2">
                          <span className="text-white text-xs">✗</span>
                        </div>
                        Tempo de recuperação &lt; 60 dias
                      </li>
                      <li className="flex items-center text-sm">
                        <div className="w-5 h-5 rounded-full bg-red-500 flex items-center justify-center mr-2">
                          <span className="text-white text-xs">✗</span>
                        </div>
                        Perda de liquidez &lt; 40%
                      </li>
                      <li className="flex items-center text-sm">
                        <div className="w-5 h-5 rounded-full bg-green-500 flex items-center justify-center mr-2">
                          <span className="text-white text-xs">✓</span>
                        </div>
                        Perda de holders &lt; 30%
                      </li>
                    </ul>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader>
                <CardTitle className="text-base">Resultados dos Cenários</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="h-[250px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                      data={[
                        { name: 'Crash de Mercado', resultado: -45 },
                        { name: 'Crise de Liquidez', resultado: -38 },
                        { name: 'Choque Regulatório', resultado: -32 },
                        { name: 'Falha de Segurança', resultado: -58 },
                        { name: 'Venda de Whales', resultado: -42 }
                      ]}
                      margin={{ top: 20, right: 30, left: 20, bottom: 60 }}
                    >
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" angle={-45} textAnchor="end" height={60} />
                      <YAxis />
                      <Tooltip formatter={(value) => [`${value}%`, 'Impacto no Preço']} />
                      <Bar dataKey="resultado" fill="#8884d8">
                        {stressScenarios.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
        
        <TabsContent value="results" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Resultados do Teste de Estresse</CardTitle>
              <CardDescription>
                Resumo dos resultados e recomendações para melhorar a resiliência do seu token
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                  <Card className="bg-muted/20">
                    <CardHeader className="p-3 pb-0">
                      <CardTitle className="text-xs text-muted-foreground">Drawdown Máximo</CardTitle>
                    </CardHeader>
                    <CardContent className="p-3 pt-0">
                      <div className="text-2xl font-bold text-red-500">
                        {stressTestResults.maxDrawdown}
                      </div>
                    </CardContent>
                  </Card>
                  
                  <Card className="bg-muted/20">
                    <CardHeader className="p-3 pb-0">
                      <CardTitle className="text-xs text-muted-foreground">Tempo de Recuperação</CardTitle>
                    </CardHeader>
                    <CardContent className="p-3 pt-0">
                      <div className="text-2xl font-bold">
                        {stressTestResults.recoveryTime}
                      </div>
                    </CardContent>
                  </Card>
                  
                  <Card className="bg-muted/20">
                    <CardHeader className="p-3 pb-0">
                      <CardTitle className="text-xs text-muted-foreground">Aumento de Volatilidade</CardTitle>
                    </CardHeader>
                    <CardContent className="p-3 pt-0">
                      <div className="text-2xl font-bold text-orange-500">
                        {stressTestResults.volatilityIncrease}
                      </div>
                    </CardContent>
                  </Card>
                  
                  <Card className="bg-muted/20">
                    <CardHeader className="p-3 pb-0">
                      <CardTitle className="text-xs text-muted-foreground">Redução de Liquidez</CardTitle>
                    </CardHeader>
                    <CardContent className="p-3 pt-0">
                      <div className="text-2xl font-bold text-red-500">
                        {stressTestResults.liquidityDecrease}
                      </div>
                    </CardContent>
                  </Card>
                </div>
                
                <div className="flex flex-col sm:flex-row gap-6">
                  <div className="flex-1">
                    <h3 className="text-lg font-medium mb-3">Resumo dos Resultados</h3>
                    <div className="border rounded-md p-4 text-sm space-y-2">
                      <p>O token demonstrou <strong>resiliência moderada</strong> aos cenários de estresse, com:
                      </p>
                      <ul className="list-disc list-inside space-y-1 text-muted-foreground">
                        <li>Drawdown significativo durante eventos de mercado negativos</li>
                        <li>Tempo de recuperação acima da média do mercado</li>
                        <li>Alta volatilidade durante períodos de estresse</li>
                        <li>Perda considerável de liquidez em cenários extremos</li>
                      </ul>
                      
                      <div className="pt-2">
                        <div className="flex items-center justify-between text-sm border-t pt-2">
                          <span>Status:</span>
                          <span className="bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full text-xs font-medium">
                            Aprovado com Ressalvas
                          </span>
                        </div>
                        <div className="flex items-center justify-between text-sm border-t pt-2 mt-2">
                          <span>Cenários aprovados:</span>
                          <span className="font-medium">{stressTestResults.passedScenarios}/{stressTestResults.passedScenarios + stressTestResults.failedScenarios}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex-1">
                    <h3 className="text-lg font-medium mb-3">Recomendações</h3>
                    <div className="border rounded-md p-4 bg-muted/20 text-sm space-y-3">
                      <p>Para melhorar a resiliência do token em cenários de estresse:</p>
                      
                      <div className="space-y-2">
                        <div className="flex items-start">
                          <div className="w-5 h-5 rounded-full bg-green-100 flex items-center justify-center mr-2 mt-0.5">
                            <span className="text-green-800 text-xs">1</span>
                          </div>
                          <div>
                            <p className="font-medium">Implemente reservas de liquidez</p>
                            <p className="text-xs text-muted-foreground">Crie um fundo de reserva para estabilizar o preço durante quedas de mercado</p>
                          </div>
                        </div>
                        
                        <div className="flex items-start">
                          <div className="w-5 h-5 rounded-full bg-green-100 flex items-center justify-center mr-2 mt-0.5">
                            <span className="text-green-800 text-xs">2</span>
                          </div>
                          <div>
                            <p className="font-medium">Reduza a concentração de tokens</p>
                            <p className="text-xs text-muted-foreground">Distribua melhor os tokens para evitar impacto de vendas por grandes holders</p>
                          </div>
                        </div>
                        
                        <div className="flex items-start">
                          <div className="w-5 h-5 rounded-full bg-green-100 flex items-center justify-center mr-2 mt-0.5">
                            <span className="text-green-800 text-xs">3</span>
                          </div>
                          <div>
                            <p className="font-medium">Implemente mecanismos de estabilidade</p>
                            <p className="text-xs text-muted-foreground">Considere taxas variáveis ou recompras automáticas para controlar volatilidade</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="flex justify-end space-x-2">
                  <Button variant="outline">
                    <Download className="h-4 w-4 mr-2" />
                    Exportar Relatório
                  </Button>
                  <Button>
                    <Save className="h-4 w-4 mr-2" />
                    Salvar Resultados
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="text-base">Comparação com Benchmarks</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="h-[300px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                      layout="vertical"
                      data={[
                        { name: 'Drawdown Máximo', token: 43.8, benchmark: 38.5 },
                        { name: 'Tempo de Recuperação', token: 87, benchmark: 62 },
                        { name: 'Perda de Liquidez', token: 65, benchmark: 45 },
                        { name: 'Perda de Holders', token: 28, benchmark: 32 }
                      ]}
                      margin={{ top: 20, right: 30, left: 100, bottom: 20 }}
                    >
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis type="number" />
                      <YAxis dataKey="name" type="category" />
                      <Tooltip />
                      <Legend />
                      <Bar dataKey="token" fill="#8884d8" name="Seu Token" />
                      <Bar dataKey="benchmark" fill="#82ca9d" name="Média do Mercado" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader>
                <CardTitle className="text-base">Correlação com Mercado</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-6">
                  <div className="space-y-2">
                    <Label className="text-xs">Correlação com Bitcoin</Label>
                    <div className="h-4 bg-muted rounded-full overflow-hidden">
                      <div className="h-full bg-primary" style={{ width: '78%' }}></div>
                    </div>
                    <div className="flex justify-between text-xs text-muted-foreground">
                      <span>0</span>
                      <span>0.78</span>
                      <span>1</span>
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <Label className="text-xs">Correlação com Ethereum</Label>
                    <div className="h-4 bg-muted rounded-full overflow-hidden">
                      <div className="h-full bg-primary" style={{ width: '85%' }}></div>
                    </div>
                    <div className="flex justify-between text-xs text-muted-foreground">
                      <span>0</span>
                      <span>0.85</span>
                      <span>1</span>
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <Label className="text-xs">Correlação com Altcoins</Label>
                    <div className="h-4 bg-muted rounded-full overflow-hidden">
                      <div className="h-full bg-primary" style={{ width: '92%' }}></div>
                    </div>
                    <div className="flex justify-between text-xs text-muted-foreground">
                      <span>0</span>
                      <span>0.92</span>
                      <span>1</span>
                    </div>
                  </div>
                  
                  <div className="pt-4 border-t">
                    <p className="text-sm text-muted-foreground">
                      Seu token tem <strong>alta correlação</strong> com o mercado geral de criptomoedas, tornando-o vulnerável a movimentos de mercado. Considere implementar mecanismos de descorrelação para melhorar a resiliência.
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}