import React, { useState, useEffect } from 'react';
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
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, AreaChart, Area } from 'recharts';
import { 
  TrendingUp, 
  TrendingDown, 
  BarChart as BarChartIcon, 
  LineChart as LineChartIcon, 
  CandlestickChart, 
  Calendar, 
  RefreshCw, 
  Download, 
  Info, 
  AlertTriangle,
  Bell,
  Clock,
  ArrowRight,
  BookOpen,
  Star
} from 'lucide-react';

export default function CryptoTrading() {
  const [activeTab, setActiveTab] = useState("market-overview");
  const [selectedPeriod, setSelectedPeriod] = useState("1m");
  const [selectedCoin, setSelectedCoin] = useState("BTC");
  
  // Dados mockados para simulação
  const cryptoCoins = [
    { id: "BTC", name: "Bitcoin", price: 48372.65, change: 3.42, vol: "12.5B", mcap: "980.5B", supply: "19.5M", iconColor: "text-orange-500" },
    { id: "ETH", name: "Ethereum", price: 2537.18, change: 2.13, vol: "8.7B", mcap: "302.8B", supply: "120.4M", iconColor: "text-purple-500" },
    { id: "BNB", name: "Binance Coin", price: 348.76, change: 1.25, vol: "1.2B", mcap: "58.2B", supply: "166.8M", iconColor: "text-yellow-500" },
    { id: "SOL", name: "Solana", price: 142.32, change: 5.78, vol: "3.1B", mcap: "56.9B", supply: "400.2M", iconColor: "text-blue-500" },
    { id: "ADA", name: "Cardano", price: 0.58, change: -1.02, vol: "0.8B", mcap: "20.3B", supply: "35B", iconColor: "text-cyan-500" },
    { id: "DOGE", name: "Dogecoin", price: 0.085, change: -2.35, vol: "0.5B", mcap: "12.1B", supply: "142B", iconColor: "text-yellow-400" },
    { id: "DOT", name: "Polkadot", price: 6.92, change: 0.87, vol: "0.3B", mcap: "9.8B", supply: "1.4B", iconColor: "text-pink-500" }
  ];

  // Dados mockados para simulação de preços históricos
  const generatePriceData = (coin: string, period: string) => {
    const periodsMap: Record<string, number> = {
      "1d": 24,
      "1w": 7,
      "1m": 30,
      "3m": 90,
      "1y": 12
    };
    
    const count = periodsMap[period] || 30;
    const isIntraday = period === "1d";
    const data = [];
    
    // Preço base para cada moeda
    const basePriceMap: Record<string, number> = {
      "BTC": 48000,
      "ETH": 2500,
      "BNB": 340,
      "SOL": 140,
      "ADA": 0.58,
      "DOGE": 0.085,
      "DOT": 6.80
    };
    
    // Volatilidade para cada moeda (maior = mais volátil)
    const volatilityMap: Record<string, number> = {
      "BTC": 0.03,
      "ETH": 0.04,
      "BNB": 0.04,
      "SOL": 0.06,
      "ADA": 0.05,
      "DOGE": 0.07,
      "DOT": 0.05
    };
    
    const basePrice = basePriceMap[coin] || 100;
    const volatility = volatilityMap[coin] || 0.05;
    
    // Tendência geral (positiva ou negativa)
    const trend = coin === "ADA" || coin === "DOGE" ? -0.0001 : 0.0002;
    
    let currentPrice = basePrice;
    
    for (let i = 0; i < count; i++) {
      const time = isIntraday 
        ? `${i}:00` 
        : period === "1y" 
          ? `Month ${i+1}` 
          : `Day ${i+1}`;
      
      // Simular mudanças de preço mais realistas
      const randomFactor = (Math.random() - 0.5) * volatility;
      const trendFactor = trend * i;
      currentPrice = currentPrice * (1 + randomFactor + trendFactor);
      
      // Adicionar volume com correlação com movimento de preço
      const volume = basePrice * 10000 * (1 + Math.abs(randomFactor) * 5);
      
      // Gerar preços de OHLC (Open, High, Low, Close)
      const openPrice = currentPrice;
      const highPrice = currentPrice * (1 + Math.random() * volatility * 0.5);
      const lowPrice = currentPrice * (1 - Math.random() * volatility * 0.5);
      const closePrice = openPrice * (1 + (randomFactor + trendFactor) * 0.8);
      
      data.push({
        time,
        price: currentPrice,
        open: openPrice,
        high: highPrice,
        low: lowPrice,
        close: closePrice,
        volume
      });
    }
    
    return data;
  };

  const [priceData, setPriceData] = useState<any[]>([]);
  
  useEffect(() => {
    // Gerar dados de preço quando o coin ou período mudar
    const newData = generatePriceData(selectedCoin, selectedPeriod);
    setPriceData(newData);
  }, [selectedCoin, selectedPeriod]);

  // Função para formatar números com prefixos (K, M, B)
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

  // Formatar moeda
  const formatCurrency = (value: number) => {
    if (value < 0.01) {
      return '$' + value.toFixed(6);
    } else if (value < 1) {
      return '$' + value.toFixed(4);
    } else if (value < 10) {
      return '$' + value.toFixed(3);
    } else if (value < 1000) {
      return '$' + value.toFixed(2);
    } else {
      return '$' + formatNumber(value);
    }
  };

  // Dados de análise técnica
  const technicalIndicators = [
    { name: "RSI (14)", value: selectedCoin === "SOL" ? "72.5" : "58.3", signal: selectedCoin === "SOL" ? "Overbought" : "Neutral" },
    { name: "MACD", value: selectedCoin === "ADA" ? "-0.02" : "0.05", signal: selectedCoin === "ADA" ? "Bearish" : "Bullish" },
    { name: "MA (50)", value: formatCurrency(priceData.length > 0 ? priceData[priceData.length-1].price * 0.92 : 0), signal: "Above" },
    { name: "MA (200)", value: formatCurrency(priceData.length > 0 ? priceData[priceData.length-1].price * 0.85 : 0), signal: "Above" },
    { name: "Bollinger", value: "Mid", signal: "Neutral" },
    { name: "Stochastic", value: selectedCoin === "SOL" ? "82.3" : "45.6", signal: selectedCoin === "SOL" ? "Overbought" : "Neutral" }
  ];

  // Notícias de mercado
  const marketNews = [
    { 
      title: "SEC aprova ETF de Bitcoin à vista, mercado reage positivamente", 
      source: "CoinDesk", 
      time: "2h ago", 
      sentiment: "positive"
    },
    { 
      title: "Ethereum completa atualização para reduzir taxas de transação", 
      source: "The Block", 
      time: "5h ago", 
      sentiment: "positive"
    },
    { 
      title: "Banco Central da Coreia do Sul considera CBDC usando tecnologia blockchain", 
      source: "CryptoNews", 
      time: "12h ago", 
      sentiment: "neutral"
    },
    { 
      title: "Reguladores aumentam escrutínio sobre stablecoins após volatilidade", 
      source: "Bloomberg", 
      time: "1d ago", 
      sentiment: "negative"
    },
    { 
      title: "Nova plataforma DeFi atinge $1B em TVL em apenas uma semana", 
      source: "DeFi Pulse", 
      time: "1d ago", 
      sentiment: "positive"
    },
  ];

  // Previsões de mercado
  const marketPredictions = [
    { period: "24h", direction: "up", probability: 68, change: "+2.4%" },
    { period: "7d", direction: "up", probability: 62, change: "+5.1%" },
    { period: "30d", direction: "up", probability: 57, change: "+12.6%" },
  ];

  // Detecção de correlações
  const correlationData = [
    { asset: "S&P 500", correlation: 0.68, trend: "increasing" },
    { asset: "Ouro", correlation: -0.42, trend: "decreasing" },
    { asset: "Dólar (DXY)", correlation: -0.58, trend: "stable" },
    { asset: "Ethereum", correlation: 0.92, trend: "stable" },
    { asset: "Nasdaq", correlation: 0.76, trend: "increasing" },
  ];

  // Dados de volume
  const volumeData = priceData.map(dataPoint => ({
    time: dataPoint.time,
    volume: dataPoint.volume
  }));

  // Encontrar valores mínimos e máximos para Fibonacci
  const findMinMax = () => {
    if (priceData.length === 0) return { min: 0, max: 0 };
    
    let min = priceData[0].price;
    let max = priceData[0].price;
    
    priceData.forEach(point => {
      if (point.price < min) min = point.price;
      if (point.price > max) max = point.price;
    });
    
    return { min, max };
  };

  const { min, max } = findMinMax();
  const fibDiff = max - min;

  // Níveis de Fibonacci
  const fibLevels = [
    { level: "0%", price: min },
    { level: "23.6%", price: min + fibDiff * 0.236 },
    { level: "38.2%", price: min + fibDiff * 0.382 },
    { level: "50%", price: min + fibDiff * 0.5 },
    { level: "61.8%", price: min + fibDiff * 0.618 },
    { level: "78.6%", price: min + fibDiff * 0.786 },
    { level: "100%", price: max }
  ];

  // Suportes e resistências
  const supportResistance = [
    { type: "Resistance", level: formatCurrency(priceData.length > 0 ? priceData[priceData.length-1].price * 1.05 : 0), strength: "Weak" },
    { type: "Resistance", level: formatCurrency(priceData.length > 0 ? priceData[priceData.length-1].price * 1.12 : 0), strength: "Strong" },
    { type: "Support", level: formatCurrency(priceData.length > 0 ? priceData[priceData.length-1].price * 0.95 : 0), strength: "Medium" },
    { type: "Support", level: formatCurrency(priceData.length > 0 ? priceData[priceData.length-1].price * 0.85 : 0), strength: "Strong" },
  ];

  // Tabela de análise
  const signalTable = [
    { timeframe: "1 Hora", signal: "Buy", strength: "Medium" },
    { timeframe: "4 Horas", signal: "Buy", strength: "Strong" },
    { timeframe: "1 Dia", signal: selectedCoin === "ADA" ? "Sell" : "Buy", strength: "Medium" },
    { timeframe: "1 Semana", signal: "Buy", strength: "Strong" },
    { timeframe: "1 Mês", signal: "Buy", strength: "Medium" },
  ];

  const colorSignal = (signal: string) => {
    if (signal === "Buy") return "text-green-500";
    if (signal === "Sell") return "text-red-500";
    return "text-yellow-500";
  };
  
  function colorChange(change: number) {
    return change >= 0 ? "text-green-500" : "text-red-500";
  }

  const renderMarketOverview = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <div>
                <CardTitle className="text-xl">
                  {cryptoCoins.find(c => c.id === selectedCoin)?.name} ({selectedCoin})
                </CardTitle>
                <CardDescription>
                  Preço atualizado em tempo real
                </CardDescription>
              </div>
              <div className="flex items-center space-x-4">
                <div className="text-right">
                  <div className="text-2xl font-bold">
                    {formatCurrency(cryptoCoins.find(c => c.id === selectedCoin)?.price || 0)}
                  </div>
                  <div className={`text-sm font-medium ${
                    (cryptoCoins.find(c => c.id === selectedCoin)?.change || 0) >= 0 
                      ? 'text-green-500' 
                      : 'text-red-500'
                  }`}>
                    {(cryptoCoins.find(c => c.id === selectedCoin)?.change || 0) >= 0 ? '+' : ''}
                    {cryptoCoins.find(c => c.id === selectedCoin)?.change}%
                  </div>
                </div>
                {(cryptoCoins.find(c => c.id === selectedCoin)?.change || 0) >= 0 
                  ? <TrendingUp className="h-8 w-8 text-green-500" /> 
                  : <TrendingDown className="h-8 w-8 text-red-500" />
                }
              </div>
            </CardHeader>
            <CardContent>
              <div className="flex justify-between items-center mb-4">
                <div className="flex space-x-1">
                  <Button 
                    variant={selectedPeriod === "1d" ? "default" : "outline"} 
                    size="sm"
                    onClick={() => setSelectedPeriod("1d")}
                  >
                    1D
                  </Button>
                  <Button 
                    variant={selectedPeriod === "1w" ? "default" : "outline"} 
                    size="sm"
                    onClick={() => setSelectedPeriod("1w")}
                  >
                    1W
                  </Button>
                  <Button 
                    variant={selectedPeriod === "1m" ? "default" : "outline"} 
                    size="sm"
                    onClick={() => setSelectedPeriod("1m")}
                  >
                    1M
                  </Button>
                  <Button 
                    variant={selectedPeriod === "3m" ? "default" : "outline"} 
                    size="sm"
                    onClick={() => setSelectedPeriod("3m")}
                  >
                    3M
                  </Button>
                  <Button 
                    variant={selectedPeriod === "1y" ? "default" : "outline"} 
                    size="sm"
                    onClick={() => setSelectedPeriod("1y")}
                  >
                    1Y
                  </Button>
                </div>
                <div className="flex space-x-1">
                  <Button variant="outline" size="sm">
                    <LineChartIcon className="h-4 w-4 mr-1" />
                    Line
                  </Button>
                  <Button variant="outline" size="sm">
                    <CandlestickChart className="h-4 w-4 mr-1" />
                    Candle
                  </Button>
                </div>
              </div>
              <div className="h-[350px]">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart
                    data={priceData}
                    margin={{
                      top: 5,
                      right: 5,
                      left: 20,
                      bottom: 5,
                    }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      dataKey="time" 
                      tick={{ fontSize: 12 }} 
                    />
                    <YAxis 
                      domain={['dataMin * 0.995', 'dataMax * 1.005']}
                      tickFormatter={(tick) => formatCurrency(tick)}
                      width={80}
                    />
                    <Tooltip 
                      formatter={(value: any) => [formatCurrency(value), 'Preço']}
                      labelFormatter={(label) => `Tempo: ${label}`}
                    />
                    <Line
                      type="monotone"
                      dataKey="price"
                      stroke="#8884d8"
                      strokeWidth={2}
                      dot={false}
                      activeDot={{ r: 5 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
              
              <div className="mt-6 grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="border rounded-lg p-3">
                  <div className="text-sm text-muted-foreground">Volume 24h</div>
                  <div className="text-lg font-semibold">
                    ${cryptoCoins.find(c => c.id === selectedCoin)?.vol}
                  </div>
                </div>
                <div className="border rounded-lg p-3">
                  <div className="text-sm text-muted-foreground">Market Cap</div>
                  <div className="text-lg font-semibold">
                    ${cryptoCoins.find(c => c.id === selectedCoin)?.mcap}
                  </div>
                </div>
                <div className="border rounded-lg p-3">
                  <div className="text-sm text-muted-foreground">Circulating Supply</div>
                  <div className="text-lg font-semibold">
                    {cryptoCoins.find(c => c.id === selectedCoin)?.supply}
                  </div>
                </div>
                <div className="border rounded-lg p-3">
                  <div className="text-sm text-muted-foreground">Rank</div>
                  <div className="text-lg font-semibold">
                    #{cryptoCoins.findIndex(c => c.id === selectedCoin) + 1}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="mt-6">
            <CardHeader>
              <CardTitle>Análise de Volume</CardTitle>
              <CardDescription>
                Volume de negociação ao longo do tempo
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-[200px]">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={volumeData}
                    margin={{
                      top: 5,
                      right: 5,
                      left: 20,
                      bottom: 5,
                    }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="time" tick={{ fontSize: 12 }} />
                    <YAxis 
                      tickFormatter={(tick) => formatNumber(tick)}
                      width={80}
                    />
                    <Tooltip 
                      formatter={(value: any) => ['$' + formatNumber(value), 'Volume']}
                      labelFormatter={(label) => `Tempo: ${label}`}
                    />
                    <Bar 
                      dataKey="volume" 
                      fill="#8884d8" 
                      name="Volume" 
                    />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </div>
        
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Top Moedas</CardTitle>
              <CardDescription>
                Maiores criptomoedas por capitalização
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="rounded-md border">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Moeda</TableHead>
                      <TableHead className="text-right">Preço</TableHead>
                      <TableHead className="text-right">24h</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {cryptoCoins.map((coin) => (
                      <TableRow 
                        key={coin.id}
                        className={`cursor-pointer ${selectedCoin === coin.id ? 'bg-muted/50' : ''}`}
                        onClick={() => setSelectedCoin(coin.id)}
                      >
                        <TableCell className="font-medium">
                          <div className="flex items-center">
                            <div className={`rounded-full w-2 h-2 mr-2 ${coin.iconColor}`} />
                            <span>{coin.name}</span>
                            <span className="text-muted-foreground ml-1">{coin.id}</span>
                          </div>
                        </TableCell>
                        <TableCell className="text-right">
                          {formatCurrency(coin.price)}
                        </TableCell>
                        <TableCell className={`text-right ${colorChange(coin.change)}`}>
                          {coin.change > 0 ? '+' : ''}{coin.change}%
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader>
              <CardTitle>Últimas Notícias</CardTitle>
              <CardDescription>
                Notícias que podem impactar o mercado
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {marketNews.map((news, index) => (
                  <div key={index} className="border-b border-gray-200 dark:border-gray-800 pb-4 last:border-0 last:pb-0">
                    <div className="flex justify-between items-start">
                      <h3 className="font-medium">{news.title}</h3>
                      <div className={`px-2 py-1 rounded-full text-xs ${
                        news.sentiment === 'positive' 
                          ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' 
                          : news.sentiment === 'negative'
                          ? 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
                          : 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400'
                      }`}>
                        {news.sentiment}
                      </div>
                    </div>
                    <div className="flex justify-between items-center mt-2 text-xs text-gray-500">
                      <span>{news.source}</span>
                      <span>{news.time}</span>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );

  const renderTechnicalAnalysis = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Indicadores Técnicos</CardTitle>
              <CardDescription>
                Análise técnica para {cryptoCoins.find(c => c.id === selectedCoin)?.name} ({selectedCoin})
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="mb-4 grid grid-cols-2 md:grid-cols-3 gap-4">
                {technicalIndicators.map((indicator, index) => (
                  <div key={index} className="border rounded-lg p-3">
                    <div className="text-sm text-muted-foreground">{indicator.name}</div>
                    <div className="text-lg font-semibold">{indicator.value}</div>
                    <div className={`text-xs ${
                      indicator.signal === "Bullish" || indicator.signal === "Above" 
                        ? "text-green-500" 
                        : indicator.signal === "Bearish" || indicator.signal === "Below" || indicator.signal === "Overbought"
                        ? "text-red-500"
                        : "text-amber-500"
                    }`}>
                      {indicator.signal}
                    </div>
                  </div>
                ))}
              </div>
              
              <div className="rounded-md border">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Timeframe</TableHead>
                      <TableHead>Sinal</TableHead>
                      <TableHead>Força</TableHead>
                      <TableHead className="text-right">Ação</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {signalTable.map((row, index) => (
                      <TableRow key={index}>
                        <TableCell className="font-medium">{row.timeframe}</TableCell>
                        <TableCell className={colorSignal(row.signal)}>{row.signal}</TableCell>
                        <TableCell>{row.strength}</TableCell>
                        <TableCell className="text-right">
                          <Button variant="outline" size="sm">Detalhes</Button>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader>
              <CardTitle>Níveis de Fibonacci</CardTitle>
              <CardDescription>
                Retrações de Fibonacci calculadas do ponto mais baixo ao mais alto
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="rounded-md border mb-4">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Nível</TableHead>
                      <TableHead className="text-right">Preço</TableHead>
                      <TableHead className="text-right">Status</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {fibLevels.map((level, index) => {
                      const currentPrice = priceData.length > 0 ? priceData[priceData.length-1].price : 0;
                      const isCurrentLevel = index < fibLevels.length - 1 && 
                        currentPrice >= level.price && 
                        currentPrice < fibLevels[index + 1].price;
                      
                      return (
                        <TableRow key={index} className={isCurrentLevel ? "bg-muted/50" : ""}>
                          <TableCell className="font-medium">{level.level}</TableCell>
                          <TableCell className="text-right">{formatCurrency(level.price)}</TableCell>
                          <TableCell className="text-right">
                            {isCurrentLevel ? (
                              <span className="text-green-500">Atual</span>
                            ) : level.price < currentPrice ? (
                              <span className="text-blue-500">Suporte</span>
                            ) : (
                              <span className="text-red-500">Resistência</span>
                            )}
                          </TableCell>
                        </TableRow>
                      );
                    })}
                  </TableBody>
                </Table>
              </div>
              
              <div className="h-[200px]">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart
                    data={priceData}
                    margin={{
                      top: 5,
                      right: 5,
                      left: 20,
                      bottom: 5,
                    }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="time" />
                    <YAxis 
                      domain={[min * 0.98, max * 1.02]}
                      tickFormatter={(tick) => formatCurrency(tick)}
                    />
                    <Tooltip 
                      formatter={(value: any) => [formatCurrency(value), 'Preço']}
                    />
                    <Line
                      type="monotone"
                      dataKey="price"
                      stroke="#8884d8"
                      dot={false}
                    />
                    {/* Linhas para os níveis de Fibonacci */}
                    {fibLevels.map((level, index) => (
                      <ReferenceLine 
                        key={index}
                        y={level.price} 
                        stroke={index === 0 || index === fibLevels.length - 1 ? "#ff0000" : "#ffa500"} 
                        strokeDasharray="3 3"
                        label={{ 
                          value: `${level.level} - ${formatCurrency(level.price)}`, 
                          position: 'right',
                          fill: '#888',
                          fontSize: 10
                        }}
                      />
                    ))}
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </div>
        
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Suporte e Resistência</CardTitle>
              <CardDescription>
                Níveis-chave identificados
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="rounded-md border">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Tipo</TableHead>
                      <TableHead>Nível</TableHead>
                      <TableHead>Força</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {supportResistance.map((level, index) => (
                      <TableRow key={index}>
                        <TableCell className={`font-medium ${
                          level.type === "Resistance" ? "text-red-500" : "text-green-500"
                        }`}>
                          {level.type}
                        </TableCell>
                        <TableCell>{level.level}</TableCell>
                        <TableCell>{level.strength}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader>
              <CardTitle>Previsões de Mercado</CardTitle>
              <CardDescription>
                Baseado em indicadores técnicos
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {marketPredictions.map((prediction, index) => (
                  <div key={index} className="border rounded-lg p-3">
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-sm font-medium">Próximos {prediction.period}</span>
                      <div className={`px-2 py-1 rounded-full text-xs ${
                        prediction.direction === "up" 
                          ? "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400" 
                          : "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400"
                      }`}>
                        {prediction.direction === "up" ? "Alta" : "Baixa"}
                      </div>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
                      <div 
                        className={`h-2.5 rounded-full ${
                          prediction.direction === "up" ? "bg-green-600" : "bg-red-600"
                        }`} 
                        style={{ width: `${prediction.probability}%` }}
                      ></div>
                    </div>
                    <div className="flex justify-between mt-1 text-xs text-gray-500">
                      <span>Probabilidade: {prediction.probability}%</span>
                      <span>Estimativa: {prediction.change}</span>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader>
              <CardTitle>Correlações</CardTitle>
              <CardDescription>
                Correlação com outros ativos
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {correlationData.map((corr, index) => (
                  <div key={index} className="flex items-center justify-between">
                    <span className="text-sm">{corr.asset}</span>
                    <div className="flex items-center">
                      <span className={`mr-2 ${
                        corr.correlation > 0 ? "text-green-500" : "text-red-500"
                      }`}>
                        {corr.correlation.toFixed(2)}
                      </span>
                      <div className="flex items-center">
                        {corr.trend === "increasing" && (
                          <TrendingUp className="h-4 w-4 text-green-500" />
                        )}
                        {corr.trend === "decreasing" && (
                          <TrendingDown className="h-4 w-4 text-red-500" />
                        )}
                        {corr.trend === "stable" && (
                          <LineChartIcon className="h-4 w-4 text-blue-500" />
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );

  const renderTraderEducation = () => (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Recursos para Traders</CardTitle>
          <CardDescription>
            Melhor sua compreensão e habilidades de trading
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card className="border-2 border-blue-200 dark:border-blue-900">
              <CardHeader className="pb-2">
                <CardTitle className="text-lg">Guias para Iniciantes</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="flex items-start gap-2">
                  <BookOpen className="h-4 w-4 text-blue-500 mt-0.5" />
                  <div>
                    <p className="font-medium text-sm">Entendendo Análise Técnica</p>
                    <p className="text-xs text-muted-foreground">Guia completo para traders iniciantes</p>
                  </div>
                </div>
                <div className="flex items-start gap-2">
                  <BookOpen className="h-4 w-4 text-blue-500 mt-0.5" />
                  <div>
                    <p className="font-medium text-sm">Psicologia de Trading</p>
                    <p className="text-xs text-muted-foreground">Como controlar emoções e tomar decisões melhores</p>
                  </div>
                </div>
                <div className="flex items-start gap-2">
                  <BookOpen className="h-4 w-4 text-blue-500 mt-0.5" />
                  <div>
                    <p className="font-medium text-sm">Gerenciamento de Risco</p>
                    <p className="text-xs text-muted-foreground">Estratégias para proteger seu capital</p>
                  </div>
                </div>
                <Button variant="outline" className="w-full mt-2">
                  Ver todos os guias
                </Button>
              </CardContent>
            </Card>
            
            <Card className="border-2 border-amber-200 dark:border-amber-900">
              <CardHeader className="pb-2">
                <CardTitle className="text-lg">Estratégias de Trading</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="flex items-start gap-2">
                  <Star className="h-4 w-4 text-amber-500 mt-0.5" />
                  <div>
                    <p className="font-medium text-sm">Swing Trading</p>
                    <p className="text-xs text-muted-foreground">Capture tendências de médio prazo</p>
                  </div>
                </div>
                <div className="flex items-start gap-2">
                  <Star className="h-4 w-4 text-amber-500 mt-0.5" />
                  <div>
                    <p className="font-medium text-sm">Day Trading</p>
                    <p className="text-xs text-muted-foreground">Técnicas para operações intradiárias</p>
                  </div>
                </div>
                <div className="flex items-start gap-2">
                  <Star className="h-4 w-4 text-amber-500 mt-0.5" />
                  <div>
                    <p className="font-medium text-sm">Scalping</p>
                    <p className="text-xs text-muted-foreground">Movimentos rápidos de curto prazo</p>
                  </div>
                </div>
                <Button variant="outline" className="w-full mt-2">
                  Ver todas estratégias
                </Button>
              </CardContent>
            </Card>
            
            <Card className="border-2 border-green-200 dark:border-green-900">
              <CardHeader className="pb-2">
                <CardTitle className="text-lg">Análise Fundamentalista</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="flex items-start gap-2">
                  <BarChartIcon className="h-4 w-4 text-green-500 mt-0.5" />
                  <div>
                    <p className="font-medium text-sm">Métricas on-chain</p>
                    <p className="text-xs text-muted-foreground">Entenda os dados da blockchain</p>
                  </div>
                </div>
                <div className="flex items-start gap-2">
                  <BarChartIcon className="h-4 w-4 text-green-500 mt-0.5" />
                  <div>
                    <p className="font-medium text-sm">Tokenomics</p>
                    <p className="text-xs text-muted-foreground">Avaliando modelos econômicos</p>
                  </div>
                </div>
                <div className="flex items-start gap-2">
                  <BarChartIcon className="h-4 w-4 text-green-500 mt-0.5" />
                  <div>
                    <p className="font-medium text-sm">Análise de Projeto</p>
                    <p className="text-xs text-muted-foreground">Avaliando equipe, tecnologia e visão</p>
                  </div>
                </div>
                <Button variant="outline" className="w-full mt-2">
                  Ver análises
                </Button>
              </CardContent>
            </Card>
          </div>
          
          <div className="mt-8">
            <h3 className="text-lg font-medium mb-4">Termos importantes para traders</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div className="border rounded-lg p-3">
                <h4 className="font-medium">Suporte e Resistência</h4>
                <p className="text-sm text-muted-foreground mt-1">
                  Níveis de preço onde o ativo tende a encontrar suporte (parar de cair) ou resistência (parar de subir) em sua movimentação.
                </p>
              </div>
              <div className="border rounded-lg p-3">
                <h4 className="font-medium">Indicadores de Momento</h4>
                <p className="text-sm text-muted-foreground mt-1">
                  RSI, MACD e Estocástico são indicadores que medem a velocidade e a magnitude das mudanças de preço.
                </p>
              </div>
              <div className="border rounded-lg p-3">
                <h4 className="font-medium">Médias Móveis</h4>
                <p className="text-sm text-muted-foreground mt-1">
                  Linhas que representam o preço médio de um ativo ao longo de um período específico, suavizando flutuações.
                </p>
              </div>
              <div className="border rounded-lg p-3">
                <h4 className="font-medium">Volume</h4>
                <p className="text-sm text-muted-foreground mt-1">
                  Quantidade de um ativo negociado em um determinado período. Alto volume indica forte interesse.
                </p>
              </div>
              <div className="border rounded-lg p-3">
                <h4 className="font-medium">Fibonacci</h4>
                <p className="text-sm text-muted-foreground mt-1">
                  Níveis de retração baseados na sequência de Fibonacci, usados para identificar possíveis níveis de reversão.
                </p>
              </div>
              <div className="border rounded-lg p-3">
                <h4 className="font-medium">Stop-Loss</h4>
                <p className="text-sm text-muted-foreground mt-1">
                  Ordem para limitar perdas que é executada automaticamente quando o preço atinge um nível predeterminado.
                </p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
      
      <Card>
        <CardHeader>
          <CardTitle>Calendário de Eventos</CardTitle>
          <CardDescription>
            Próximos eventos que podem impactar o mercado
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="rounded-md border">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Data</TableHead>
                  <TableHead>Evento</TableHead>
                  <TableHead>Projeto</TableHead>
                  <TableHead className="text-right">Impacto</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                <TableRow>
                  <TableCell className="font-medium">
                    <div className="flex items-center">
                      <Calendar className="h-4 w-4 mr-2 text-blue-500" />
                      <span>25 Mar 2025</span>
                    </div>
                  </TableCell>
                  <TableCell>Atualização da Rede</TableCell>
                  <TableCell>Ethereum</TableCell>
                  <TableCell className="text-right">
                    <div className="px-2 py-1 rounded-full text-xs bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-400 inline-block">
                      Médio
                    </div>
                  </TableCell>
                </TableRow>
                <TableRow>
                  <TableCell className="font-medium">
                    <div className="flex items-center">
                      <Calendar className="h-4 w-4 mr-2 text-blue-500" />
                      <span>1 Abr 2025</span>
                    </div>
                  </TableCell>
                  <TableCell>Token Burn</TableCell>
                  <TableCell>Binance (BNB)</TableCell>
                  <TableCell className="text-right">
                    <div className="px-2 py-1 rounded-full text-xs bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400 inline-block">
                      Alto
                    </div>
                  </TableCell>
                </TableRow>
                <TableRow>
                  <TableCell className="font-medium">
                    <div className="flex items-center">
                      <Calendar className="h-4 w-4 mr-2 text-blue-500" />
                      <span>10 Abr 2025</span>
                    </div>
                  </TableCell>
                  <TableCell>Audiência Regulatória</TableCell>
                  <TableCell>Mercado Geral</TableCell>
                  <TableCell className="text-right">
                    <div className="px-2 py-1 rounded-full text-xs bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400 inline-block">
                      Muito Alto
                    </div>
                  </TableCell>
                </TableRow>
                <TableRow>
                  <TableCell className="font-medium">
                    <div className="flex items-center">
                      <Calendar className="h-4 w-4 mr-2 text-blue-500" />
                      <span>15 Abr 2025</span>
                    </div>
                  </TableCell>
                  <TableCell>Lançamento de Mainnet</TableCell>
                  <TableCell>Solana</TableCell>
                  <TableCell className="text-right">
                    <div className="px-2 py-1 rounded-full text-xs bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400 inline-block">
                      Alto
                    </div>
                  </TableCell>
                </TableRow>
                <TableRow>
                  <TableCell className="font-medium">
                    <div className="flex items-center">
                      <Calendar className="h-4 w-4 mr-2 text-blue-500" />
                      <span>22 Abr 2025</span>
                    </div>
                  </TableCell>
                  <TableCell>Conferência Blockchain</TableCell>
                  <TableCell>Mercado Geral</TableCell>
                  <TableCell className="text-right">
                    <div className="px-2 py-1 rounded-full text-xs bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400 inline-block">
                      Baixo
                    </div>
                  </TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </div>
          
          <div className="flex justify-end mt-4">
            <Button variant="outline" className="gap-1">
              <Bell className="h-4 w-4" />
              Configurar Alertas de Eventos
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight">Análise de Mercado Crypto</h1>
        <div className="flex space-x-2">
          <Button variant="outline" size="sm">
            <RefreshCw className="h-4 w-4 mr-1" />
            Atualizar Dados
          </Button>
          <Button variant="outline" size="sm">
            <Download className="h-4 w-4 mr-1" />
            Exportar
          </Button>
        </div>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="market-overview" className="flex items-center gap-1">
            <LineChartIcon className="h-4 w-4" />
            <span>Visão Geral</span>
          </TabsTrigger>
          <TabsTrigger value="technical-analysis" className="flex items-center gap-1">
            <CandlestickChart className="h-4 w-4" />
            <span>Análise Técnica</span>
          </TabsTrigger>
          <TabsTrigger value="trader-education" className="flex items-center gap-1">
            <BookOpen className="h-4 w-4" />
            <span>Educação</span>
          </TabsTrigger>
        </TabsList>
        
        <div className="mt-6">
          <TabsContent value="market-overview">
            {renderMarketOverview()}
          </TabsContent>
          
          <TabsContent value="technical-analysis">
            {renderTechnicalAnalysis()}
          </TabsContent>
          
          <TabsContent value="trader-education">
            {renderTraderEducation()}
          </TabsContent>
        </div>
      </Tabs>
    </div>
  );
}

// ReferenceLine personalizada para usar nas análises
function ReferenceLine(props: any) {
  const { x, y, width, height, stroke, label, yAxisMap, orientation = "horizontal" } = props;
  
  if (orientation === "horizontal") {
    const yCoord = yAxisMap[0].scale(y);
    
    return (
      <g>
        <line
          x1={0}
          y1={yCoord}
          x2={width}
          y2={yCoord}
          stroke={stroke}
          strokeDasharray={props.strokeDasharray}
        />
        {label && (
          <text
            x={label.position === 'right' ? width - 5 : 5}
            y={yCoord - 5}
            textAnchor={label.position === 'right' ? 'end' : 'start'}
            fill={label.fill || '#666'}
            fontSize={label.fontSize || 10}
          >
            {label.value}
          </text>
        )}
      </g>
    );
  }
  
  return null;
}