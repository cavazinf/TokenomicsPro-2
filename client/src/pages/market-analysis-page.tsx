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
import { Textarea } from "@/components/ui/textarea";
import { Separator } from "@/components/ui/separator";
import { ScrollArea } from "@/components/ui/scroll-area";
import { 
  TrendingUp, 
  BarChart as BarChartIcon, 
  PieChart as PieChartIcon, 
  Search, 
  Download, 
  Layers, 
  Globe,
  RefreshCcw,
  FileText,
  CopyCheck
} from 'lucide-react';

export default function MarketAnalysis() {
  const [activeTab, setActiveTab] = useState("market-overview");
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedToken, setSelectedToken] = useState<string | null>(null);
  const [timeframe, setTimeframe] = useState("1m");

  // Dados de exemplo para as visualizações
  const marketOverviewData = {
    marketCap: "$1.23T",
    volume24h: "$58.4B",
    btcDominance: "45.2%",
    totalMarkets: "23,456",
    activeTokens: "1,893",
    avgMarketSentiment: "Neutral",
    trendingTokens: [
      { id: "btc", name: "Bitcoin", symbol: "BTC", change24h: 2.3, marketCap: "$608B", price: "$31,245" },
      { id: "eth", name: "Ethereum", symbol: "ETH", change24h: 3.1, marketCap: "$218B", price: "$1,814" },
      { id: "bnb", name: "Binance Coin", symbol: "BNB", change24h: 1.7, marketCap: "$38B", price: "$241" },
      { id: "sol", name: "Solana", symbol: "SOL", change24h: 5.4, marketCap: "$35B", price: "$84" },
      { id: "xrp", name: "XRP", symbol: "XRP", change24h: -1.2, marketCap: "$29B", price: "$0.53" }
    ],
    marketCapData: [
      { name: "Jan", value: 980 },
      { name: "Feb", value: 1080 },
      { name: "Mar", value: 890 },
      { name: "Apr", value: 1300 },
      { name: "May", value: 1200 },
      { name: "Jun", value: 1100 },
      { name: "Jul", value: 1400 },
      { name: "Aug", value: 1500 },
      { name: "Sep", value: 1200 },
      { name: "Oct", value: 1300 },
      { name: "Nov", value: 1450 },
      { name: "Dec", value: 1230 }
    ],
    dominanceData: [
      { name: "Bitcoin", value: 45 },
      { name: "Ethereum", value: 19 },
      { name: "Stablecoins", value: 12 },
      { name: "BNB", value: 3 },
      { name: "Solana", value: 3 },
      { name: "XRP", value: 2 },
      { name: "Others", value: 16 }
    ]
  };

  const competitiveAnalysisData = {
    sectors: [
      { name: "DeFi", marketCap: "$43B", dominantToken: "UNI", projects: 342, growth: 8.2 },
      { name: "NFTs", marketCap: "$18B", dominantToken: "APE", projects: 283, growth: 3.7 },
      { name: "Smart Contract Platforms", marketCap: "$390B", dominantToken: "ETH", projects: 62, growth: 4.5 },
      { name: "Web3", marketCap: "$31B", dominantToken: "LINK", projects: 178, growth: 6.9 },
      { name: "Gaming", marketCap: "$12B", dominantToken: "AXS", projects: 156, growth: 9.8 },
      { name: "Metaverse", marketCap: "$14B", dominantToken: "SAND", projects: 98, growth: 7.3 }
    ],
    sectorGrowthData: [
      { name: "DeFi", q1: 5.2, q2: 6.1, q3: 7.5, q4: 8.2 },
      { name: "NFTs", q1: 12.3, q2: 9.8, q3: 6.1, q4: 3.7 },
      { name: "Smart Contract", q1: 3.9, q2: 4.1, q3: 4.3, q4: 4.5 },
      { name: "Web3", q1: 4.2, q2: 5.1, q3: 6.0, q4: 6.9 },
      { name: "Gaming", q1: 6.3, q2: 7.8, q3: 8.9, q4: 9.8 },
      { name: "Metaverse", q1: 9.1, q2: 8.7, q3: 7.9, q4: 7.3 }
    ],
    competitorsData: [
      { 
        sector: "DeFi", 
        projects: [
          { name: "Uniswap", symbol: "UNI", marketCap: "$3.8B", volume: "$124M", dominance: "8.9%" },
          { name: "Aave", symbol: "AAVE", marketCap: "$1.2B", volume: "$89M", dominance: "2.8%" },
          { name: "Compound", symbol: "COMP", marketCap: "$430M", volume: "$42M", dominance: "1.0%" },
          { name: "Curve DAO", symbol: "CRV", marketCap: "$550M", volume: "$64M", dominance: "1.3%" },
          { name: "MakerDAO", symbol: "MKR", marketCap: "$910M", volume: "$39M", dominance: "2.1%" }
        ]
      },
      { 
        sector: "NFTs", 
        projects: [
          { name: "ApeCoin", symbol: "APE", marketCap: "$1.5B", volume: "$98M", dominance: "8.3%" },
          { name: "Decentraland", symbol: "MANA", marketCap: "$840M", volume: "$62M", dominance: "4.7%" },
          { name: "The Sandbox", symbol: "SAND", marketCap: "$910M", volume: "$71M", dominance: "5.1%" },
          { name: "Flow", symbol: "FLOW", marketCap: "$700M", volume: "$35M", dominance: "3.9%" },
          { name: "Render", symbol: "RNDR", marketCap: "$650M", volume: "$48M", dominance: "3.6%" }
        ]
      }
    ]
  };

  const tokenSearchData = [
    { id: "btc", name: "Bitcoin", symbol: "BTC", price: "$31,245", change24h: 2.3, marketCap: "$608B", category: "Currency" },
    { id: "eth", name: "Ethereum", symbol: "ETH", price: "$1,814", change24h: 3.1, marketCap: "$218B", category: "Smart Contract Platform" },
    { id: "bnb", name: "Binance Coin", symbol: "BNB", price: "$241", change24h: 1.7, marketCap: "$38B", category: "Exchange Token" },
    { id: "sol", name: "Solana", symbol: "SOL", price: "$84", change24h: 5.4, marketCap: "$35B", category: "Smart Contract Platform" },
    { id: "xrp", name: "XRP", symbol: "XRP", price: "$0.53", change24h: -1.2, marketCap: "$29B", category: "Currency" },
    { id: "ada", name: "Cardano", symbol: "ADA", price: "$0.38", change24h: 0.8, marketCap: "$13B", category: "Smart Contract Platform" },
    { id: "avax", name: "Avalanche", symbol: "AVAX", price: "$21.50", change24h: 4.1, marketCap: "$7B", category: "Smart Contract Platform" },
    { id: "link", name: "Chainlink", symbol: "LINK", price: "$14.20", change24h: 3.9, marketCap: "$7.5B", category: "Oracle" },
    { id: "uni", name: "Uniswap", symbol: "UNI", price: "$5.10", change24h: 1.3, marketCap: "$3.8B", category: "DeFi" },
    { id: "aave", name: "Aave", symbol: "AAVE", price: "$86.30", change24h: 2.8, marketCap: "$1.2B", category: "DeFi" }
  ];

  const tokenMarketData = {
    btc: {
      name: "Bitcoin",
      symbol: "BTC",
      price: "$31,245",
      ath: "$69,000",
      atl: "$67",
      marketCap: "$608B",
      volume24h: "$23.4B",
      circulatingSupply: "19.43M",
      totalSupply: "21M",
      dilutedValuation: "$656B",
      launchDate: "January 3, 2009",
      category: "Store of Value, Currency, Asset",
      roi: "27,384%",
      priceData: [
        { date: "Jan", price: 16500 },
        { date: "Feb", price: 23400 },
        { date: "Mar", price: 28300 },
        { date: "Apr", price: 30100 },
        { date: "May", price: 27200 },
        { date: "Jun", price: 29800 },
        { date: "Jul", price: 31100 },
        { date: "Aug", price: 29400 },
        { date: "Sep", price: 28900 },
        { date: "Oct", price: 30500 },
        { date: "Nov", price: 35100 },
        { date: "Dec", price: 31245 }
      ],
      volumeData: [
        { date: "Jan", volume: 18.2 },
        { date: "Feb", volume: 25.7 },
        { date: "Mar", volume: 21.3 },
        { date: "Apr", volume: 19.8 },
        { date: "May", volume: 22.4 },
        { date: "Jun", volume: 20.9 },
        { date: "Jul", volume: 24.3 },
        { date: "Aug", volume: 21.7 },
        { date: "Sep", volume: 19.6 },
        { date: "Oct", volume: 22.8 },
        { date: "Nov", volume: 28.3 },
        { date: "Dec", volume: 23.4 }
      ],
      holdersData: [
        { category: "Large Holders", value: 62 },
        { category: "Medium Holders", value: 21 },
        { category: "Small Holders", value: 17 }
      ]
    },
    eth: {
      name: "Ethereum",
      symbol: "ETH",
      price: "$1,814",
      ath: "$4,891",
      atl: "$0.42",
      marketCap: "$218B",
      volume24h: "$8.7B",
      circulatingSupply: "120.1M",
      totalSupply: "∞",
      dilutedValuation: "N/A",
      launchDate: "July 30, 2015",
      category: "Smart Contract Platform, Web3",
      roi: "87,982%",
      priceData: [
        { date: "Jan", price: 1250 },
        { date: "Feb", price: 1650 },
        { date: "Mar", price: 1750 },
        { date: "Apr", price: 1890 },
        { date: "May", price: 1820 },
        { date: "Jun", price: 1910 },
        { date: "Jul", price: 1930 },
        { date: "Aug", price: 1840 },
        { date: "Sep", price: 1780 },
        { date: "Oct", price: 1830 },
        { date: "Nov", price: 1980 },
        { date: "Dec", price: 1814 }
      ],
      volumeData: [
        { date: "Jan", volume: 6.8 },
        { date: "Feb", volume: 9.2 },
        { date: "Mar", volume: 7.9 },
        { date: "Apr", volume: 8.3 },
        { date: "May", volume: 7.4 },
        { date: "Jun", volume: 8.1 },
        { date: "Jul", volume: 9.8 },
        { date: "Aug", volume: 8.4 },
        { date: "Sep", volume: 7.2 },
        { date: "Oct", volume: 8.9 },
        { date: "Nov", volume: 10.3 },
        { date: "Dec", volume: 8.7 }
      ],
      holdersData: [
        { category: "Large Holders", value: 41 },
        { category: "Medium Holders", value: 34 },
        { category: "Small Holders", value: 25 }
      ]
    }
  };

  const filterTokens = () => {
    if (!searchTerm) return tokenSearchData;
    
    const term = searchTerm.toLowerCase();
    return tokenSearchData.filter(token => 
      token.name.toLowerCase().includes(term) || 
      token.symbol.toLowerCase().includes(term) ||
      token.category.toLowerCase().includes(term)
    );
  };

  const renderMarketOverview = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-base font-medium">Capitalização de Mercado Total</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{marketOverviewData.marketCap}</div>
            <p className="text-xs text-muted-foreground">Volume 24h: {marketOverviewData.volume24h}</p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-base font-medium">Dominância do Bitcoin</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{marketOverviewData.btcDominance}</div>
            <p className="text-xs text-muted-foreground">Total de Mercados: {marketOverviewData.totalMarkets}</p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-base font-medium">Tokens Ativos</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{marketOverviewData.activeTokens}</div>
            <p className="text-xs text-muted-foreground">Sentimento: {marketOverviewData.avgMarketSentiment}</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="col-span-1">
          <CardHeader>
            <CardTitle className="text-base font-medium">Capitalização de Mercado (2023)</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={marketOverviewData.marketCapData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis tickFormatter={(value) => `${value}B`} />
                  <Tooltip formatter={(value) => [`$${value}B`, 'Capitalização de Mercado']} />
                  <Legend />
                  <Line type="monotone" dataKey="value" stroke="#8884d8" activeDot={{ r: 8 }} name="Capitalização de Mercado ($B)" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card className="col-span-1">
          <CardHeader>
            <CardTitle className="text-base font-medium">Distribuição de Dominância</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={marketOverviewData.dominanceData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    outerRadius={100}
                    fill="#8884d8"
                    dataKey="value"
                    nameKey="name"
                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  >
                    {marketOverviewData.dominanceData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={`hsl(${index * 45}, 70%, 60%)`} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value) => [`${value}%`, 'Dominância']} />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base font-medium">Tokens em Destaque</CardTitle>
          <CardDescription>Tokens com melhor performance nas últimas 24 horas</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="rounded-md border">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Nome</TableHead>
                  <TableHead>Preço</TableHead>
                  <TableHead>24h</TableHead>
                  <TableHead className="hidden md:table-cell">Capitalização</TableHead>
                  <TableHead className="text-right"></TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {marketOverviewData.trendingTokens.map((token) => (
                  <TableRow key={token.id}>
                    <TableCell className="font-medium">
                      {token.name} <span className="text-muted-foreground">{token.symbol}</span>
                    </TableCell>
                    <TableCell>{token.price}</TableCell>
                    <TableCell className={token.change24h >= 0 ? "text-green-500" : "text-red-500"}>
                      {token.change24h > 0 ? "+" : ""}{token.change24h}%
                    </TableCell>
                    <TableCell className="hidden md:table-cell">{token.marketCap}</TableCell>
                    <TableCell className="text-right">
                      <Button variant="ghost" size="sm" onClick={() => setSelectedToken(token.id)}>
                        Detalhes
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>
    </div>
  );

  const renderCompetitiveAnalysis = () => (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Análise de Setores</CardTitle>
          <CardDescription>Visão geral dos principais setores do mercado de criptomoedas</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="rounded-md border">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Setor</TableHead>
                  <TableHead>Capitalização</TableHead>
                  <TableHead>Token Dominante</TableHead>
                  <TableHead>Projetos</TableHead>
                  <TableHead>Crescimento (%)</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {competitiveAnalysisData.sectors.map((sector) => (
                  <TableRow key={sector.name}>
                    <TableCell className="font-medium">{sector.name}</TableCell>
                    <TableCell>{sector.marketCap}</TableCell>
                    <TableCell>{sector.dominantToken}</TableCell>
                    <TableCell>{sector.projects}</TableCell>
                    <TableCell className="text-green-500">+{sector.growth}%</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Crescimento Trimestral por Setor</CardTitle>
          <CardDescription>Análise de crescimento (%) por setor nos últimos 4 trimestres</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-96">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={competitiveAnalysisData.sectorGrowthData}
                margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis tickFormatter={(value) => `${value}%`} />
                <Tooltip formatter={(value) => [`${value}%`, 'Crescimento']} />
                <Legend />
                <Bar dataKey="q1" fill="#8884d8" name="Q1 2023" />
                <Bar dataKey="q2" fill="#82ca9d" name="Q2 2023" />
                <Bar dataKey="q3" fill="#ffc658" name="Q3 2023" />
                <Bar dataKey="q4" fill="#ff8042" name="Q4 2023" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Análise de Competidores - DeFi</CardTitle>
          <CardDescription>Principais competidores no setor de Finanças Descentralizadas</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="rounded-md border">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Projeto</TableHead>
                  <TableHead>Token</TableHead>
                  <TableHead>Capitalização</TableHead>
                  <TableHead>Volume 24h</TableHead>
                  <TableHead>Dominância</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {competitiveAnalysisData.competitorsData[0].projects.map((project) => (
                  <TableRow key={project.symbol}>
                    <TableCell className="font-medium">{project.name}</TableCell>
                    <TableCell>{project.symbol}</TableCell>
                    <TableCell>{project.marketCap}</TableCell>
                    <TableCell>{project.volume}</TableCell>
                    <TableCell>{project.dominance}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>

          <div className="mt-6 flex justify-end">
            <Button variant="outline" size="sm">
              Ver mais setores
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );

  const renderTokenDetails = () => {
    const token = selectedToken ? tokenMarketData[selectedToken as keyof typeof tokenMarketData] : null;
    
    if (!token) {
      return (
        <div className="text-center py-12">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-muted mb-4">
            <Search className="h-8 w-8 text-muted-foreground" />
          </div>
          <h3 className="text-lg font-medium">Selecione um token para ver detalhes</h3>
          <p className="text-muted-foreground mt-2">
            Busque um token ou selecione um da lista para visualizar informações detalhadas
          </p>
        </div>
      );
    }
    
    return (
      <div className="space-y-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h2 className="text-2xl font-bold">{token.name} ({token.symbol})</h2>
            <div className="text-muted-foreground">{token.category}</div>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-right">
              <div className="text-xl font-semibold">{token.price}</div>
              <div className="text-xs text-muted-foreground">ATH: {token.ath} | ATL: {token.atl}</div>
            </div>
            <Button variant="outline" size="sm">
              <Download className="mr-2 h-4 w-4" />
              Relatório
            </Button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Capitalização de Mercado</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-lg font-bold">{token.marketCap}</div>
              <p className="text-xs text-muted-foreground">Avaliação Diluída: {token.dilutedValuation}</p>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Volume (24h)</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-lg font-bold">{token.volume24h}</div>
              <p className="text-xs text-muted-foreground">Lançamento: {token.launchDate}</p>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Oferta</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-lg font-bold">{token.circulatingSupply}</div>
              <p className="text-xs text-muted-foreground">Total: {token.totalSupply} | ROI: {token.roi}</p>
            </CardContent>
          </Card>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Card className="col-span-1">
            <CardHeader>
              <CardTitle className="text-base font-medium">Histórico de Preço</CardTitle>
              <div className="flex space-x-2">
                {["1w", "1m", "3m", "6m", "1y", "all"].map((time) => (
                  <Button
                    key={time}
                    variant={timeframe === time ? "default" : "outline"}
                    size="sm"
                    onClick={() => setTimeframe(time)}
                    className="h-7 px-2 text-xs"
                  >
                    {time.toUpperCase()}
                  </Button>
                ))}
              </div>
            </CardHeader>
            <CardContent>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={token.priceData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis domain={['auto', 'auto']} />
                    <Tooltip formatter={(value) => [`$${value}`, 'Preço']} />
                    <Line type="monotone" dataKey="price" stroke="#8884d8" activeDot={{ r: 8 }} name="Preço" />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>

          <Card className="col-span-1">
            <CardHeader>
              <CardTitle className="text-base font-medium">Volume de Negociação</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={token.volumeData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis tickFormatter={(value) => `${value}B`} />
                    <Tooltip formatter={(value) => [`$${value}B`, 'Volume']} />
                    <Bar dataKey="volume" fill="#82ca9d" name="Volume ($B)" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </div>

        <Card>
          <CardHeader>
            <CardTitle className="text-base font-medium">Distribuição de Holders</CardTitle>
          </CardHeader>
          <CardContent className="flex flex-col md:flex-row items-center gap-6">
            <div className="w-full md:w-1/3 h-64">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={token.holdersData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                    nameKey="category"
                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  >
                    {token.holdersData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={`hsl(${index * 120}, 70%, 60%)`} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value) => [`${value}%`, 'Porcentagem']} />
                </PieChart>
              </ResponsiveContainer>
            </div>
            
            <div className="w-full md:w-2/3">
              <div className="space-y-4">
                <div>
                  <h3 className="font-medium mb-2">Grandes Holders (Baleias)</h3>
                  <p className="text-sm text-muted-foreground">
                    Os grandes holders controlam a maior parte do suprimento, com {token.holdersData[0].value}% concentrado em carteiras que possuem mais de 1% do suprimento circulante cada. Essa concentração pode criar riscos de volatilidade em caso de vendas significativas.
                  </p>
                </div>
                
                <div>
                  <h3 className="font-medium mb-2">Distribuição Institucional vs. Varejo</h3>
                  <p className="text-sm text-muted-foreground">
                    Aproximadamente 45% dos tokens estão em endereços identificados como institucionais, incluindo exchanges, fundos e entidades corporativas. Os outros 55% estão distribuídos entre endereços de varejo.
                  </p>
                </div>
                
                <div className="pt-2">
                  <Button variant="outline" size="sm">
                    <FileText className="mr-2 h-4 w-4" />
                    Relatório de Distribuição Completo
                  </Button>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  };

  const renderTokenSearch = () => (
    <div className="space-y-6">
      <div className="flex items-center space-x-2">
        <div className="relative flex-1">
          <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            type="search"
            placeholder="Buscar por nome, símbolo ou categoria..."
            className="pl-8"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <Button variant="outline" size="icon" onClick={() => setSearchTerm("")}>
          <RefreshCcw className="h-4 w-4" />
        </Button>
      </div>

      <div className="border rounded-md">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Nome</TableHead>
              <TableHead>Preço</TableHead>
              <TableHead>24h</TableHead>
              <TableHead className="hidden md:table-cell">Capitalização</TableHead>
              <TableHead className="hidden md:table-cell">Categoria</TableHead>
              <TableHead className="text-right"></TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filterTokens().map((token) => (
              <TableRow key={token.id}>
                <TableCell className="font-medium">
                  {token.name} <span className="text-muted-foreground">{token.symbol}</span>
                </TableCell>
                <TableCell>{token.price}</TableCell>
                <TableCell className={token.change24h >= 0 ? "text-green-500" : "text-red-500"}>
                  {token.change24h > 0 ? "+" : ""}{token.change24h}%
                </TableCell>
                <TableCell className="hidden md:table-cell">{token.marketCap}</TableCell>
                <TableCell className="hidden md:table-cell">{token.category}</TableCell>
                <TableCell className="text-right">
                  <Button 
                    variant={selectedToken === token.id ? "default" : "outline"} 
                    size="sm"
                    onClick={() => setSelectedToken(token.id)}
                  >
                    {selectedToken === token.id ? (
                      <CopyCheck className="mr-1 h-4 w-4" />
                    ) : null}
                    {selectedToken === token.id ? "Selecionado" : "Selecionar"}
                  </Button>
                </TableCell>
              </TableRow>
            ))}
            {filterTokens().length === 0 && (
              <TableRow>
                <TableCell colSpan={6} className="h-24 text-center">
                  Nenhum resultado encontrado.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>

      <Separator />

      <div className="pt-4">
        <h2 className="text-xl font-bold mb-6">Análise de Token</h2>
        {renderTokenDetails()}
      </div>
    </div>
  );

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight">Análise de Mercado</h1>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="market-overview" className="flex items-center gap-1">
            <Globe className="h-4 w-4" />
            <span>Visão Geral</span>
          </TabsTrigger>
          <TabsTrigger value="competitive-analysis" className="flex items-center gap-1">
            <BarChartIcon className="h-4 w-4" />
            <span>Análise Competitiva</span>
          </TabsTrigger>
          <TabsTrigger value="token-search" className="flex items-center gap-1">
            <Search className="h-4 w-4" />
            <span>Pesquisa de Tokens</span>
          </TabsTrigger>
        </TabsList>
        
        <div className="mt-6">
          <TabsContent value="market-overview">
            {renderMarketOverview()}
          </TabsContent>
          
          <TabsContent value="competitive-analysis">
            {renderCompetitiveAnalysis()}
          </TabsContent>
          
          <TabsContent value="token-search">
            {renderTokenSearch()}
          </TabsContent>
        </div>
      </Tabs>
    </div>
  );
}