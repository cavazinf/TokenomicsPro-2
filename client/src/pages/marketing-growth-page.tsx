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
import { Textarea } from "@/components/ui/textarea";
import { Separator } from "@/components/ui/separator";
import { Slider } from "@/components/ui/slider";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Checkbox } from "@/components/ui/checkbox";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { 
  TrendingUp, 
  Users, 
  Target, 
  Award,
  BarChart as BarChartIcon,
  Download,
  Share2,
  FileText,
  CheckCircle2,
  ArrowRight,
  Zap,
  Hash,
  Bell,
  MessageCircle,
  Flag,
  Rocket,
  Heart,
  Megaphone,
  Globe,
  Clock,
  UserCheck
} from 'lucide-react';

export default function MarketingGrowth() {
  const [activeTab, setActiveTab] = useState("growth-strategy");
  const [selectedChannel, setSelectedChannel] = useState<string | null>(null);
  
  // Estratégia de Crescimento
  const [growthForm, setGrowthForm] = useState({
    productMarketFit: "",
    targetAudience: "",
    valueProposition: "",
    channels: "",
    growthMetrics: "",
    northStar: "",
    keyHypothesis: ""
  });

  // Dados do funil de aquisição
  const acquisitionData = [
    { name: 'Awareness', users: 10000, conversion: 100 },
    { name: 'Interest', users: 3500, conversion: 35 },
    { name: 'Evaluation', users: 1200, conversion: 34.3 },
    { name: 'Trial', users: 800, conversion: 66.7 },
    { name: 'Activation', users: 500, conversion: 62.5 },
    { name: 'Retention', users: 300, conversion: 60 },
    { name: 'Referral', users: 120, conversion: 40 },
    { name: 'Revenue', users: 80, conversion: 66.7 }
  ];

  // Dados de crescimento de usuários
  const userGrowthData = [
    { month: 'Jan', users: 100, activeUsers: 80, referrals: 5 },
    { month: 'Feb', users: 250, activeUsers: 180, referrals: 15 },
    { month: 'Mar', users: 400, activeUsers: 300, referrals: 30 },
    { month: 'Apr', users: 700, activeUsers: 500, referrals: 60 },
    { month: 'May', users: 1200, activeUsers: 800, referrals: 100 },
    { month: 'Jun', users: 2000, activeUsers: 1400, referrals: 180 },
  ];

  // Canais de Marketing Web3
  const marketingChannels = [
    {
      id: "community",
      name: "Community Building",
      icon: <Users className="h-5 w-5 text-blue-500" />,
      description: "Estratégias para construir e engajar uma comunidade forte de usuários e defensores.",
      tactics: [
        "Programa de embaixadores com recompensas tokenizadas",
        "Estrutura de DAO para decisões comunitárias",
        "Eventos virtuais e AMAs regulares",
        "Grupos de discussão em Discord/Telegram",
        "Hackathons e desafios de desenvolvimento"
      ],
      metrics: [
        "Membros ativos diários",
        "Taxa de engajamento em canais comunitários",
        "Número de propostas da comunidade",
        "NPS da comunidade",
        "Retenção de membros"
      ],
      effectiveness: 90,
      investmentLevel: "Médio a Alto",
      timeToResults: "Médio a Longo prazo"
    },
    {
      id: "content",
      name: "Marketing de Conteúdo",
      icon: <FileText className="h-5 w-5 text-purple-500" />,
      description: "Criação e distribuição de conteúdo educacional e informativo sobre o projeto.",
      tactics: [
        "Artigos técnicos e explicativos (Medium/Mirror)",
        "Videos educacionais e tutoriais",
        "Documentação detalhada e guias de usuário",
        "Whitepapers e tokenomics papers",
        "Estudos de caso e comparações"
      ],
      metrics: [
        "Visualizações e tempo de leitura",
        "Compartilhamentos e menções",
        "Conversões a partir de conteúdo",
        "Autoridade em keywords",
        "Backlinks gerados"
      ],
      effectiveness: 85,
      investmentLevel: "Baixo a Médio",
      timeToResults: "Médio prazo"
    },
    {
      id: "incentives",
      name: "Incentivos & Airdrops",
      icon: <Award className="h-5 w-5 text-amber-500" />,
      description: "Uso de incentivos econômicos para atrair e reter usuários na plataforma.",
      tactics: [
        "Airdrops estratégicos para early adopters",
        "Programas de referência com recompensas",
        "Incentivos de liquidez (liquidity mining)",
        "Recompensas por tarefas de crescimento (growth mining)",
        "Bônus de aquisição para novos usuários"
      ],
      metrics: [
        "CAC (Custo de Aquisição por Cliente)",
        "Taxa de retenção pós-incentivo",
        "ROI dos programas de incentivo",
        "Valor lifetime vs. custo de incentivo",
        "Efeito viral (K-factor)"
      ],
      effectiveness: 80,
      investmentLevel: "Alto",
      timeToResults: "Rápido a Médio"
    },
    {
      id: "influencers",
      name: "Influenciadores & KOLs",
      icon: <Megaphone className="h-5 w-5 text-red-500" />,
      description: "Parcerias com líderes de opinião do espaço Web3 para ampliar alcance e credibilidade.",
      tactics: [
        "Embaixadores de longo prazo com tokens/equity",
        "Reviews de produtos por criadores Web3",
        "Takeovers de canais/streams",
        "Parcerias com influenciadores técnicos",
        "Demonstrações ao vivo e entrevistas"
      ],
      metrics: [
        "Novos usuários atribuíveis",
        "Engajamento nas menções",
        "Sentimento das menções",
        "ROI por influenciador",
        "Retenção de usuários via influenciadores"
      ],
      effectiveness: 75,
      investmentLevel: "Médio a Alto",
      timeToResults: "Rápido"
    },
    {
      id: "partnerships",
      name: "Parcerias Estratégicas",
      icon: <Handshake className="h-5 w-5 text-green-500" />,
      description: "Colaborações com outros projetos Web3 e empresas tradicionais para expansão.",
      tactics: [
        "Integrações tecnológicas com outros protocolos",
        "Co-marketing com projetos complementares",
        "Programas de aceleração e incubação",
        "Ecossistema de parceiros com incentivos mútuos",
        "Parcerias de liquidez cruzada"
      ],
      metrics: [
        "Novos usuários via parceiros",
        "Aumento de TVL via integrações",
        "Expansão para novos mercados",
        "Valor gerado por parceria",
        "Cross-selling entre comunidades"
      ],
      effectiveness: 85,
      investmentLevel: "Médio",
      timeToResults: "Médio prazo"
    },
    {
      id: "events",
      name: "Eventos & Conferências",
      icon: <Users className="h-5 w-5 text-indigo-500" />,
      description: "Participação em eventos do setor e organização de meetups para networking e aquisição.",
      tactics: [
        "Presença em conferências premium (ETHDenver, Consensus)",
        "Organização de hackathons temáticos",
        "Workshops educacionais presenciais",
        "Meetups comunitários regionais",
        "Eventos exclusivos para holders de tokens"
      ],
      metrics: [
        "Leads gerados por evento",
        "Custo por lead qualificado",
        "Conversões pós-evento",
        "Cobertura midiática gerada",
        "Parcerias iniciadas em eventos"
      ],
      effectiveness: 70,
      investmentLevel: "Alto",
      timeToResults: "Médio prazo"
    }
  ];

  // Experimentos de Crescimento
  const growthExperiments = [
    {
      id: 1,
      name: "Programa de Referral com Recompensas Duplas",
      hypothesis: "Oferecer recompensas tanto para o referente quanto para o indicado aumentará significativamente nossa taxa de aquisição viral.",
      metrics: "Número de referências, taxa de conversão, CAC, K-factor",
      effort: "Médio",
      impact: "Alto",
      status: "Em andamento"
    },
    {
      id: 2,
      name: "Conteúdo Simplificado para Onboarding",
      hypothesis: "Simplificar as explicações técnicas com analogias e visuais reduzirá a taxa de abandono durante o onboarding.",
      metrics: "Taxa de conclusão de onboarding, tempo para ativação, feedback de usuários",
      effort: "Baixo",
      impact: "Médio",
      status: "Planejado"
    },
    {
      id: 3,
      name: "Embaixadores Especializados por Nicho",
      hypothesis: "Criar programas de embaixadores específicos para diferentes nichos (traders, artistas, desenvolvedores) aumentará a penetração nesses segmentos.",
      metrics: "Aquisição por nicho, engajamento da comunidade, conteúdo gerado",
      effort: "Alto",
      impact: "Alto",
      status: "Planejado"
    },
    {
      id: 4,
      name: "Quiz Interativo com Airdrop",
      hypothesis: "Um quiz educacional com pequenas recompensas em tokens aumentará o conhecimento do usuário e a retenção a longo prazo.",
      metrics: "Conhecimento do produto, retenção, engajamento com documentação",
      effort: "Médio",
      impact: "Médio",
      status: "Concluído"
    },
    {
      id: 5,
      name: "Gamificação de Tarefas de Aquisição",
      hypothesis: "Gamificar o processo de aquisição com missões e recompensas escalonadas incentivará os usuários a completar mais ações.",
      metrics: "Conclusão de tarefas, profundidade de uso, ativações",
      effort: "Alto",
      impact: "Alto",
      status: "Em andamento"
    }
  ];

  const handleGrowthFormChange = (field: keyof typeof growthForm, value: string) => {
    setGrowthForm(prev => ({
      ...prev,
      [field]: value
    }));
  };
  
  function Handshake(props: React.SVGProps<SVGSVGElement>) {
    return (
      <svg
        {...props}
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        <path d="M20.42 4.58a5.4 5.4 0 0 0-7.65 0l-.77.78-.77-.78a5.4 5.4 0 0 0-7.65 0C1.46 6.7 1.33 10.28 4 13l8 8 8-8c2.67-2.72 2.54-6.3.42-8.42z"></path>
        <path d="M12 5.36 8.87 8.5a2.13 2.13 0 0 0 0 3h0a2.13 2.13 0 0 0 3 0l2.26-2.21a2.13 2.13 0 0 1 3 0h0a2.13 2.13 0 0 1 0 3l-2.26 2.21"></path>
      </svg>
    );
  }

  const renderGrowthStrategy = () => (
    <div className="space-y-6">
      <div className="bg-muted/30 p-4 rounded-lg">
        <h3 className="font-medium text-lg mb-2">Estratégia de Crescimento</h3>
        <p className="text-muted-foreground">
          Defina sua estratégia de crescimento para atrair e reter usuários para seu projeto Web3.
          Uma estratégia clara ajuda a focar recursos e mensurar progresso.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Fundamentos da Estratégia</CardTitle>
              <CardDescription>
                Defina os componentes-chave da sua estratégia de crescimento
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="productMarketFit">Product-Market Fit</Label>
                  <Textarea 
                    id="productMarketFit" 
                    placeholder="Descreva como seu produto resolve um problema real no mercado..."
                    rows={4}
                    value={growthForm.productMarketFit}
                    onChange={(e) => handleGrowthFormChange('productMarketFit', e.target.value)}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="targetAudience">Público-Alvo</Label>
                  <Textarea 
                    id="targetAudience" 
                    placeholder="Defina claramente quem são seus usuários ideais..."
                    rows={4}
                    value={growthForm.targetAudience}
                    onChange={(e) => handleGrowthFormChange('targetAudience', e.target.value)}
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="valueProposition">Proposta de Valor (USP)</Label>
                <Textarea 
                  id="valueProposition" 
                  placeholder="Qual é a proposta de valor única do seu projeto? Por que os usuários escolherão você?"
                  rows={3}
                  value={growthForm.valueProposition}
                  onChange={(e) => handleGrowthFormChange('valueProposition', e.target.value)}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="channels">Canais de Aquisição</Label>
                <Textarea 
                  id="channels" 
                  placeholder="Quais canais você utilizará para adquirir usuários? (ex: comunidade, conteúdo, parcerias)"
                  rows={3}
                  value={growthForm.channels}
                  onChange={(e) => handleGrowthFormChange('channels', e.target.value)}
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="growthMetrics">Métricas de Crescimento</Label>
                  <Textarea 
                    id="growthMetrics" 
                    placeholder="Quais métricas você acompanhará? (ex: DAU, retenção, volume)"
                    rows={4}
                    value={growthForm.growthMetrics}
                    onChange={(e) => handleGrowthFormChange('growthMetrics', e.target.value)}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="northStar">Métrica North Star</Label>
                  <Textarea 
                    id="northStar" 
                    placeholder="Qual é a principal métrica que guia o crescimento do seu projeto?"
                    rows={4}
                    value={growthForm.northStar}
                    onChange={(e) => handleGrowthFormChange('northStar', e.target.value)}
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="keyHypothesis">Hipóteses-Chave</Label>
                <Textarea 
                  id="keyHypothesis" 
                  placeholder="Quais são suas principais hipóteses de crescimento que precisam ser validadas?"
                  rows={3}
                  value={growthForm.keyHypothesis}
                  onChange={(e) => handleGrowthFormChange('keyHypothesis', e.target.value)}
                />
              </div>
            </CardContent>
            <CardFooter className="flex justify-end space-x-2">
              <Button variant="outline">
                Limpar
              </Button>
              <Button>
                Salvar Estratégia
              </Button>
            </CardFooter>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Funil de Aquisição</CardTitle>
              <CardDescription>
                Visualize e analise o funil de conversão do seu projeto
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={acquisitionData}
                    layout="vertical"
                    margin={{ top: 20, right: 30, left: 40, bottom: 5 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number" />
                    <YAxis dataKey="name" type="category" width={100} />
                    <Tooltip 
                      formatter={(value, name) => {
                        if (name === "users") return [value, "Usuários"];
                        if (name === "conversion") return [value + "%", "Taxa de Conversão"];
                        return [value, name];
                      }}
                    />
                    <Legend />
                    <Bar dataKey="users" fill="#8884d8" name="Usuários" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
              
              <div className="mt-6">
                <h3 className="text-sm font-medium mb-2">Análise de Conversão</h3>
                <div className="rounded-md border">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Estágio</TableHead>
                        <TableHead>Usuários</TableHead>
                        <TableHead>Conversão</TableHead>
                        <TableHead>Ação Recomendada</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {acquisitionData.map((stage, i) => (
                        <TableRow key={i}>
                          <TableCell className="font-medium">{stage.name}</TableCell>
                          <TableCell>{stage.users.toLocaleString()}</TableCell>
                          <TableCell>{stage.conversion}%</TableCell>
                          <TableCell className="text-xs">
                            {i === 2 ? (
                              <span className="text-amber-500">Melhorar materiais educacionais</span>
                            ) : i === 6 ? (
                              <span className="text-red-500">Implementar programa de referral</span>
                            ) : (
                              <span className="text-green-500">Manter estratégia atual</span>
                            )}
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="lg:col-span-1 space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <TrendingUp className="h-5 w-5 mr-2 text-green-500" />
                <span>Crescimento de Usuários</span>
              </CardTitle>
              <CardDescription>
                Evolução mensal de usuários
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-60">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart
                    data={userGrowthData}
                    margin={{ top: 5, right: 10, left: 10, bottom: 5 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="users" stroke="#8884d8" name="Usuários Totais" />
                    <Line type="monotone" dataKey="activeUsers" stroke="#82ca9d" name="Usuários Ativos" />
                  </LineChart>
                </ResponsiveContainer>
              </div>

              <div className="mt-4 space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium">Crescimento Mensal</span>
                  <span className="text-green-500 font-bold">67%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium">Retenção D30</span>
                  <span className="text-amber-500 font-bold">42%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium">Taxa de Referral</span>
                  <span className="text-green-500 font-bold">9%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium">Custo de Aquisição</span>
                  <span className="text-green-500 font-bold">$12.40</span>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Pilares de Crescimento Web3</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <Label htmlFor="communityPillar" className="flex items-center">
                    <Users className="w-4 h-4 mr-2 text-blue-500" />
                    <span>Comunidade</span>
                  </Label>
                  <span className="text-sm font-medium">90%</span>
                </div>
                <Slider
                  id="communityPillar"
                  defaultValue={[90]}
                  max={100}
                  step={1}
                  disabled
                />
                <p className="text-xs text-muted-foreground">
                  Foco em construir uma comunidade engajada e autêntica
                </p>
              </div>

              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <Label htmlFor="tokenPillar" className="flex items-center">
                    <Zap className="w-4 h-4 mr-2 text-amber-500" />
                    <span>Incentivos de Token</span>
                  </Label>
                  <span className="text-sm font-medium">85%</span>
                </div>
                <Slider
                  id="tokenPillar"
                  defaultValue={[85]}
                  max={100}
                  step={1}
                  disabled
                />
                <p className="text-xs text-muted-foreground">
                  Alinhar incentivos econômicos com comportamentos desejados
                </p>
              </div>

              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <Label htmlFor="contentPillar" className="flex items-center">
                    <FileText className="w-4 h-4 mr-2 text-purple-500" />
                    <span>Conteúdo Educativo</span>
                  </Label>
                  <span className="text-sm font-medium">75%</span>
                </div>
                <Slider
                  id="contentPillar"
                  defaultValue={[75]}
                  max={100}
                  step={1}
                  disabled
                />
                <p className="text-xs text-muted-foreground">
                  Educar usuários para reduzir barreiras de adoção
                </p>
              </div>

              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <Label htmlFor="partnershipsPillar" className="flex items-center">
                    <Handshake className="w-4 h-4 mr-2 text-green-500" />
                    <span>Parcerias</span>
                  </Label>
                  <span className="text-sm font-medium">80%</span>
                </div>
                <Slider
                  id="partnershipsPillar"
                  defaultValue={[80]}
                  max={100}
                  step={1}
                  disabled
                />
                <p className="text-xs text-muted-foreground">
                  Construir um ecossistema através de colaborações estratégicas
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );

  const renderMarketingChannels = () => (
    <div className="space-y-6">
      <div className="bg-muted/30 p-4 rounded-lg">
        <h3 className="font-medium text-lg mb-2">Canais de Marketing Web3</h3>
        <p className="text-muted-foreground">
          Explore e selecione os canais de marketing mais eficazes para projetos Web3.
          Cada canal tem suas próprias táticas, métricas e considerações específicas.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-4">
          {marketingChannels.map((channel) => (
            <div
              key={channel.id}
              className={`border rounded-lg p-4 cursor-pointer transition-colors ${
                selectedChannel === channel.id 
                  ? 'border-primary bg-primary/5' 
                  : 'hover:bg-muted/50'
              }`}
              onClick={() => setSelectedChannel(channel.id)}
            >
              <div className="flex items-start justify-between">
                <div className="flex items-center">
                  {channel.icon}
                  <div className="ml-3">
                    <h3 className="font-medium">{channel.name}</h3>
                    <p className="text-xs text-muted-foreground">{channel.description}</p>
                  </div>
                </div>
                {selectedChannel === channel.id && <CheckCircle2 className="h-5 w-5 text-primary" />}
              </div>
            </div>
          ))}
        </div>

        <div className="lg:col-span-2">
          {selectedChannel ? (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  {marketingChannels.find(c => c.id === selectedChannel)?.icon}
                  <span>{marketingChannels.find(c => c.id === selectedChannel)?.name}</span>
                </CardTitle>
                <CardDescription>
                  {marketingChannels.find(c => c.id === selectedChannel)?.description}
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div>
                  <h3 className="text-sm font-medium mb-2">Táticas Principais</h3>
                  <ul className="space-y-1">
                    {marketingChannels
                      .find(c => c.id === selectedChannel)
                      ?.tactics.map((tactic, i) => (
                        <li key={i} className="flex items-start gap-2 text-sm">
                          <ArrowRight className="h-4 w-4 text-primary mt-0.5" />
                          <span>{tactic}</span>
                        </li>
                      ))}
                  </ul>
                </div>

                <Separator />

                <div>
                  <h3 className="text-sm font-medium mb-2">Métricas de Desempenho</h3>
                  <ul className="space-y-1">
                    {marketingChannels
                      .find(c => c.id === selectedChannel)
                      ?.metrics.map((metric, i) => (
                        <li key={i} className="flex items-start gap-2 text-sm">
                          <Target className="h-4 w-4 text-blue-500 mt-0.5" />
                          <span>{metric}</span>
                        </li>
                      ))}
                  </ul>
                </div>

                <div className="pt-2 grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="space-y-2">
                    <h3 className="text-sm font-medium">Efetividade</h3>
                    <div className="flex items-center">
                      <div className="w-full bg-muted rounded-full h-2.5 mr-2">
                        <div 
                          className="bg-primary h-2.5 rounded-full" 
                          style={{ width: `${marketingChannels.find(c => c.id === selectedChannel)?.effectiveness}%` }}
                        ></div>
                      </div>
                      <span className="text-sm font-medium">
                        {marketingChannels.find(c => c.id === selectedChannel)?.effectiveness}%
                      </span>
                    </div>
                  </div>
                  
                  <div>
                    <h3 className="text-sm font-medium">Nível de Investimento</h3>
                    <p className="text-sm mt-1">
                      {marketingChannels.find(c => c.id === selectedChannel)?.investmentLevel}
                    </p>
                  </div>
                  
                  <div>
                    <h3 className="text-sm font-medium">Tempo até Resultados</h3>
                    <p className="text-sm mt-1">
                      {marketingChannels.find(c => c.id === selectedChannel)?.timeToResults}
                    </p>
                  </div>
                </div>

                <div className="bg-muted/50 p-4 rounded-lg mt-4">
                  <h3 className="font-medium mb-2">Melhores Práticas</h3>
                  
                  {selectedChannel === "community" && (
                    <div className="space-y-2 text-sm">
                      <p>1. <strong>Estabeleça propósito claro:</strong> Defina a missão e valores da comunidade para atrair membros alinhados.</p>
                      <p>2. <strong>Crie estrutura de governança:</strong> Permita que a comunidade participe de decisões importantes através de votações e propostas.</p>
                      <p>3. <strong>Diversifique canais:</strong> Utilize diferentes plataformas (Discord, Telegram, fóruns) para diferentes tipos de interações.</p>
                      <p>4. <strong>Incentive contribuidores:</strong> Desenvolva sistemas para reconhecer e recompensar os membros mais ativos e valiosos.</p>
                      <p>5. <strong>Transparência constante:</strong> Comunique abertamente sobre o desenvolvimento, desafios e sucessos do projeto.</p>
                    </div>
                  )}

                  {selectedChannel === "content" && (
                    <div className="space-y-2 text-sm">
                      <p>1. <strong>Desenvolva conteúdo em camadas:</strong> Do básico ao avançado para diferentes níveis de conhecimento.</p>
                      <p>2. <strong>Utilize múltiplos formatos:</strong> Combine texto, vídeo, infográficos e áudio para diferentes preferências.</p>
                      <p>3. <strong>SEO para conteúdo Web3:</strong> Otimize para termos de busca relevantes no espaço crypto/blockchain.</p>
                      <p>4. <strong>Direcione para ação:</strong> Cada conteúdo deve ter um próximo passo claro para o usuário.</p>
                      <p>5. <strong>Curadoria comunitária:</strong> Permita que a comunidade vote e destaque conteúdos valiosos.</p>
                    </div>
                  )}

                  {selectedChannel === "incentives" && (
                    <div className="space-y-2 text-sm">
                      <p>1. <strong>Alinhamento com objetivos:</strong> Incentivos devem promover comportamentos que criam valor para o ecossistema.</p>
                      <p>2. <strong>Sustentabilidade de longo prazo:</strong> Evite insustentáveis "mercenários de yield" com incentivos decrescentes.</p>
                      <p>3. <strong>Targeting estratégico:</strong> Distribua incentivos para usuários e mercados específicos de alto valor.</p>
                      <p>4. <strong>Vesting gradual:</strong> Implementar períodos de lock para garantir alinhamento de longo prazo.</p>
                      <p>5. <strong>Anti-Sybil:</strong> Proteja contra ataques de identidades falsas com verificação adequada.</p>
                    </div>
                  )}

                  {selectedChannel === "influencers" && (
                    <div className="space-y-2 text-sm">
                      <p>1. <strong>Autenticidade acima de tudo:</strong> Priorize influenciadores que genuinamente acreditam no projeto.</p>
                      <p>2. <strong>Incentivos de longo prazo:</strong> Ofereça tokens/equity com vesting para alinhar interesses.</p>
                      <p>3. <strong>Foco na qualidade:</strong> Priorize engajamento e qualificação da audiência sobre números brutos.</p>
                      <p>4. <strong>Educação detalhada:</strong> Forneça materiais educativos profundos sobre o projeto para o influenciador.</p>
                      <p>5. <strong>Diversidade de perfis:</strong> Combine influenciadores técnicos, comunitários e de investimento.</p>
                    </div>
                  )}

                  {selectedChannel === "partnerships" && (
                    <div className="space-y-2 text-sm">
                      <p>1. <strong>Complementaridade:</strong> Busque parceiros cujos produtos complementem os seus, não competidores.</p>
                      <p>2. <strong>Integrações técnicas:</strong> Priorize parcerias com integração real sobre simples co-marketing.</p>
                      <p>3. <strong>Alinhamento de incentivos:</strong> Estruture parcerias com benefícios mútuos e mensuráveis.</p>
                      <p>4. <strong>Crescimento conjunto:</strong> Compartilhe dados e insights para otimizar a colaboração.</p>
                      <p>5. <strong>Expansão estratégica:</strong> Use parcerias para entrar em novos mercados ou segmentos estratégicos.</p>
                    </div>
                  )}

                  {selectedChannel === "events" && (
                    <div className="space-y-2 text-sm">
                      <p>1. <strong>Qualidade sobre quantidade:</strong> Foque em eventos de alta relevância para seu nicho específico.</p>
                      <p>2. <strong>Preparação completa:</strong> Desenvolva materiais, demos e pitches específicos para cada evento.</p>
                      <p>3. <strong>Follow-up sistemático:</strong> Implemente processo para acompanhar todos os contatos pós-evento.</p>
                      <p>4. <strong>Conteúdo exclusivo:</strong> Crie conteúdo ou anúncios exclusivos para gerar mais impacto.</p>
                      <p>5. <strong>Hackathons estratégicos:</strong> Organize desafios focados em construir sobre sua plataforma/protocolo.</p>
                    </div>
                  )}
                </div>
              </CardContent>
              <CardFooter className="flex justify-between">
                <Button variant="outline">
                  <FileText className="mr-2 h-4 w-4" />
                  Manual Completo
                </Button>
                <Button>
                  Adicionar ao Plano
                </Button>
              </CardFooter>
            </Card>
          ) : (
            <div className="flex items-center justify-center h-full border rounded-lg p-8">
              <div className="text-center">
                <Target className="h-12 w-12 text-muted-foreground mx-auto mb-4 opacity-50" />
                <h3 className="text-lg font-medium">Selecione um Canal</h3>
                <p className="text-muted-foreground mt-2 max-w-md">
                  Escolha um canal de marketing à esquerda para visualizar táticas, 
                  métricas de desempenho e melhores práticas.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );

  const renderCommunityBuilding = () => (
    <div className="space-y-6">
      <div className="bg-muted/30 p-4 rounded-lg">
        <h3 className="font-medium text-lg mb-2">Construção de Comunidade</h3>
        <p className="text-muted-foreground">
          Uma comunidade forte é o ativo mais valioso de um projeto Web3. 
          Planeje, construa e gerencie sua comunidade para crescimento sustentável.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-8">
          <Card>
            <CardHeader>
              <CardTitle>Plano de Comunidade</CardTitle>
              <CardDescription>
                Desenvolva uma estratégia completa de construção de comunidade
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <div>
                  <Label className="text-base">Plataformas de Comunidade</Label>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-2">
                    <div className="flex items-start space-x-2">
                      <Checkbox id="platform-discord" defaultChecked />
                      <div className="grid gap-1.5">
                        <Label htmlFor="platform-discord" className="font-medium">
                          Discord
                        </Label>
                        <p className="text-sm text-muted-foreground">
                          Comunidade principal com canais para discussão, suporte e governança
                        </p>
                      </div>
                    </div>
                    <div className="flex items-start space-x-2">
                      <Checkbox id="platform-telegram" defaultChecked />
                      <div className="grid gap-1.5">
                        <Label htmlFor="platform-telegram" className="font-medium">
                          Telegram
                        </Label>
                        <p className="text-sm text-muted-foreground">
                          Anúncios oficiais e comunicações diretas
                        </p>
                      </div>
                    </div>
                    <div className="flex items-start space-x-2">
                      <Checkbox id="platform-forum" defaultChecked />
                      <div className="grid gap-1.5">
                        <Label htmlFor="platform-forum" className="font-medium">
                          Fórum de Governança
                        </Label>
                        <p className="text-sm text-muted-foreground">
                          Discussões detalhadas de governança e propostas
                        </p>
                      </div>
                    </div>
                    <div className="flex items-start space-x-2">
                      <Checkbox id="platform-twitter" defaultChecked />
                      <div className="grid gap-1.5">
                        <Label htmlFor="platform-twitter" className="font-medium">
                          Twitter
                        </Label>
                        <p className="text-sm text-muted-foreground">
                          Updates, amplificação e engajamento com a comunidade Web3
                        </p>
                      </div>
                    </div>
                  </div>
                </div>

                <Separator />

                <div className="space-y-3">
                  <Label className="text-base">Estrutura de Comunidade</Label>
                  
                  <div className="rounded-md border">
                    <table className="min-w-full divide-y divide-border">
                      <thead className="bg-muted/50">
                        <tr>
                          <th className="px-4 py-2 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                            Nível
                          </th>
                          <th className="px-4 py-2 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                            Requisitos
                          </th>
                          <th className="px-4 py-2 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                            Benefícios/Acesso
                          </th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-border">
                        <tr>
                          <td className="px-4 py-2 text-sm font-medium">Visitante</td>
                          <td className="px-4 py-2 text-sm">Verificação básica anti-bot</td>
                          <td className="px-4 py-2 text-sm">Canais de informação geral e suporte</td>
                        </tr>
                        <tr>
                          <td className="px-4 py-2 text-sm font-medium">Membro</td>
                          <td className="px-4 py-2 text-sm">Concordar com regras, completar onboarding</td>
                          <td className="px-4 py-2 text-sm">Todos os canais públicos de discussão</td>
                        </tr>
                        <tr>
                          <td className="px-4 py-2 text-sm font-medium">Contribuidor</td>
                          <td className="px-4 py-2 text-sm">Participação ativa por 2+ semanas</td>
                          <td className="px-4 py-2 text-sm">Canais de contribuidores e betas</td>
                        </tr>
                        <tr>
                          <td className="px-4 py-2 text-sm font-medium">Embaixador</td>
                          <td className="px-4 py-2 text-sm">Aplicação aprovada, staking de tokens</td>
                          <td className="px-4 py-2 text-sm">Programa de recompensas, reuniões com time</td>
                        </tr>
                        <tr>
                          <td className="px-4 py-2 text-sm font-medium">Conselho</td>
                          <td className="px-4 py-2 text-sm">Eleito pela DAO, contribuições significativas</td>
                          <td className="px-4 py-2 text-sm">Decisões estratégicas, representação oficial</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>

                <Separator />

                <div className="space-y-3">
                  <Label className="text-base">Programa de Embaixadores</Label>
                  
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <Card className="border-blue-200 dark:border-blue-800">
                      <CardHeader className="py-3">
                        <CardTitle className="text-sm flex items-center text-blue-700 dark:text-blue-400">
                          <Flag className="h-4 w-4 mr-1" />
                          Embaixador de Conteúdo
                        </CardTitle>
                      </CardHeader>
                      <CardContent className="py-3">
                        <ul className="text-xs space-y-1">
                          <li>• Criar conteúdo educacional</li>
                          <li>• Produzir tutoriais e análises</li>
                          <li>• Traduzir materiais</li>
                        </ul>
                      </CardContent>
                      <CardFooter className="py-3 text-xs text-muted-foreground">
                        Recompensa: 500 tokens/mês + bônus
                      </CardFooter>
                    </Card>

                    <Card className="border-green-200 dark:border-green-800">
                      <CardHeader className="py-3">
                        <CardTitle className="text-sm flex items-center text-green-700 dark:text-green-400">
                          <MessageCircle className="h-4 w-4 mr-1" />
                          Embaixador de Comunidade
                        </CardTitle>
                      </CardHeader>
                      <CardContent className="py-3">
                        <ul className="text-xs space-y-1">
                          <li>• Moderar canais comunitários</li>
                          <li>• Organizar eventos e AMAs</li>
                          <li>• Acolher novos membros</li>
                        </ul>
                      </CardContent>
                      <CardFooter className="py-3 text-xs text-muted-foreground">
                        Recompensa: 400 tokens/mês + bônus
                      </CardFooter>
                    </Card>

                    <Card className="border-purple-200 dark:border-purple-800">
                      <CardHeader className="py-3">
                        <CardTitle className="text-sm flex items-center text-purple-700 dark:text-purple-400">
                          <Globe className="h-4 w-4 mr-1" />
                          Embaixador Regional
                        </CardTitle>
                      </CardHeader>
                      <CardContent className="py-3">
                        <ul className="text-xs space-y-1">
                          <li>• Representar em regiões específicas</li>
                          <li>• Construir comunidades locais</li>
                          <li>• Adaptar estratégias para mercados locais</li>
                        </ul>
                      </CardContent>
                      <CardFooter className="py-3 text-xs text-muted-foreground">
                        Recompensa: 600 tokens/mês + bônus
                      </CardFooter>
                    </Card>
                  </div>
                </div>

                <div className="space-y-3">
                  <Label className="text-base">Calendário de Engajamento</Label>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <h3 className="text-sm font-medium">Eventos Regulares</h3>
                      <ul className="text-sm space-y-2">
                        <li className="flex items-start gap-2">
                          <Clock className="h-4 w-4 text-blue-500 mt-0.5" />
                          <div>
                            <span className="font-medium">AMA com Fundadores</span>
                            <p className="text-xs text-muted-foreground">Quinzenal, alternando timezones</p>
                          </div>
                        </li>
                        <li className="flex items-start gap-2">
                          <Clock className="h-4 w-4 text-green-500 mt-0.5" />
                          <div>
                            <span className="font-medium">Community Call</span>
                            <p className="text-xs text-muted-foreground">Semanal, updates e feedback</p>
                          </div>
                        </li>
                        <li className="flex items-start gap-2">
                          <Clock className="h-4 w-4 text-purple-500 mt-0.5" />
                          <div>
                            <span className="font-medium">Tech Workshops</span>
                            <p className="text-xs text-muted-foreground">Mensal, aprofundamento técnico</p>
                          </div>
                        </li>
                        <li className="flex items-start gap-2">
                          <Clock className="h-4 w-4 text-amber-500 mt-0.5" />
                          <div>
                            <span className="font-medium">Governance Forum</span>
                            <p className="text-xs text-muted-foreground">Bi-semanal, discussão de propostas</p>
                          </div>
                        </li>
                      </ul>
                    </div>

                    <div className="space-y-2">
                      <h3 className="text-sm font-medium">Iniciativas de Engajamento</h3>
                      <ul className="text-sm space-y-2">
                        <li className="flex items-start gap-2">
                          <Rocket className="h-4 w-4 text-red-500 mt-0.5" />
                          <div>
                            <span className="font-medium">Desafios da Comunidade</span>
                            <p className="text-xs text-muted-foreground">Tarefas com recompensas em tokens</p>
                          </div>
                        </li>
                        <li className="flex items-start gap-2">
                          <Heart className="h-4 w-4 text-pink-500 mt-0.5" />
                          <div>
                            <span className="font-medium">Programa de Reconhecimento</span>
                            <p className="text-xs text-muted-foreground">Membro do mês, Hall da Fama</p>
                          </div>
                        </li>
                        <li className="flex items-start gap-2">
                          <Hash className="h-4 w-4 text-blue-500 mt-0.5" />
                          <div>
                            <span className="font-medium">Meme & Art Contests</span>
                            <p className="text-xs text-muted-foreground">Competições criativas mensais</p>
                          </div>
                        </li>
                        <li className="flex items-start gap-2">
                          <Bell className="h-4 w-4 text-amber-500 mt-0.5" />
                          <div>
                            <span className="font-medium">Beta Testers Program</span>
                            <p className="text-xs text-muted-foreground">Acesso antecipado a novos recursos</p>
                          </div>
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
            <CardFooter className="flex justify-end space-x-2">
              <Button variant="outline">
                <FileText className="mr-2 h-4 w-4" />
                Salvar Rascunho
              </Button>
              <Button>
                Implementar Plano
              </Button>
            </CardFooter>
          </Card>
        </div>

        <div className="lg:col-span-4 space-y-4">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-base">Métricas de Comunidade</CardTitle>
              <CardDescription>Principais indicadores de saúde</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <div className="flex justify-between items-center text-sm">
                  <span className="flex items-center">
                    <Users className="h-4 w-4 mr-1 text-blue-500" />
                    <span>Membros Totais</span>
                  </span>
                  <span className="font-bold">12,458</span>
                </div>
                <div className="flex justify-between items-center text-sm">
                  <span className="flex items-center">
                    <MessageCircle className="h-4 w-4 mr-1 text-green-500" />
                    <span>Mensagens/Dia</span>
                  </span>
                  <span className="font-bold">824</span>
                </div>
                <div className="flex justify-between items-center text-sm">
                  <span className="flex items-center">
                    <UserCheck className="h-4 w-4 mr-1 text-purple-500" />
                    <span>Membros Ativos (DAU)</span>
                  </span>
                  <span className="font-bold">1,275</span>
                </div>
                <div className="flex justify-between items-center text-sm">
                  <span className="flex items-center">
                    <Zap className="h-4 w-4 mr-1 text-amber-500" />
                    <span>Taxa de Engajamento</span>
                  </span>
                  <span className="font-bold">9.2%</span>
                </div>
                <div className="flex justify-between items-center text-sm">
                  <span className="flex items-center">
                    <Flag className="h-4 w-4 mr-1 text-red-500" />
                    <span>Embaixadores Ativos</span>
                  </span>
                  <span className="font-bold">42</span>
                </div>
              </div>

              <Separator />

              <div>
                <h3 className="text-sm font-medium mb-2">Crescimento da Comunidade</h3>
                <div className="h-40">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                      data={[
                        { name: 'Jan', members: 3200 },
                        { name: 'Feb', members: 4800 },
                        { name: 'Mar', members: 6500 },
                        { name: 'Apr', members: 8300 },
                        { name: 'May', members: 10100 },
                        { name: 'Jun', members: 12458 }
                      ]}
                      margin={{ top: 5, right: 5, left: 5, bottom: 5 }}
                    >
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis tickFormatter={(value) => value >= 1000 ? `${value/1000}k` : value} />
                      <Tooltip formatter={(value) => [`${value.toLocaleString()} membros`, 'Total']} />
                      <Bar dataKey="members" fill="#8884d8" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-base">Ferramentas de Comunidade</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="p-3 bg-blue-50 dark:bg-blue-950/30 rounded-lg flex items-start space-x-3">
                <div className="rounded-full bg-blue-100 dark:bg-blue-900 p-1.5">
                  <MessageCircle className="h-4 w-4 text-blue-600 dark:text-blue-400" />
                </div>
                <div>
                  <h3 className="text-sm font-medium">Discord & Collab.Land</h3>
                  <p className="text-xs text-muted-foreground mt-1">
                    Gestão de comunidade com verificação de tokens
                  </p>
                </div>
              </div>

              <div className="p-3 bg-purple-50 dark:bg-purple-950/30 rounded-lg flex items-start space-x-3">
                <div className="rounded-full bg-purple-100 dark:bg-purple-900 p-1.5">
                  <Globe className="h-4 w-4 text-purple-600 dark:text-purple-400" />
                </div>
                <div>
                  <h3 className="text-sm font-medium">Snapshot & Commonwealth</h3>
                  <p className="text-xs text-muted-foreground mt-1">
                    Votação e discussão de propostas de governança
                  </p>
                </div>
              </div>

              <div className="p-3 bg-amber-50 dark:bg-amber-950/30 rounded-lg flex items-start space-x-3">
                <div className="rounded-full bg-amber-100 dark:bg-amber-900 p-1.5">
                  <Award className="h-4 w-4 text-amber-600 dark:text-amber-400" />
                </div>
                <div>
                  <h3 className="text-sm font-medium">Questbook & Dework</h3>
                  <p className="text-xs text-muted-foreground mt-1">
                    Gestão de tarefas, bounties e recompensas
                  </p>
                </div>
              </div>

              <div className="p-3 bg-green-50 dark:bg-green-950/30 rounded-lg flex items-start space-x-3">
                <div className="rounded-full bg-green-100 dark:bg-green-900 p-1.5">
                  <Users className="h-4 w-4 text-green-600 dark:text-green-400" />
                </div>
                <div>
                  <h3 className="text-sm font-medium">Guild.xyz & Coordinape</h3>
                  <p className="text-xs text-muted-foreground mt-1">
                    Alocação comunitária de recursos e acesso
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );

  const renderGrowthExperiments = () => (
    <div className="space-y-6">
      <div className="bg-muted/30 p-4 rounded-lg">
        <h3 className="font-medium text-lg mb-2">Experimentos de Crescimento</h3>
        <p className="text-muted-foreground">
          Planeje, execute e meça experimentos de crescimento para seu projeto.
          Uma abordagem científica e orientada por dados para encontrar alavancas de crescimento.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Matriz de Experimentos</CardTitle>
          <CardDescription>
            Priorize experimentos com base em esforço e impacto potencial
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="rounded-md border">
            <table className="min-w-full divide-y divide-border">
              <thead className="bg-muted/50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                    Experimento
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                    Hipótese
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider hidden md:table-cell">
                    Métricas
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                    Esforço
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                    Impacto
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                    Status
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                {growthExperiments.map((experiment) => (
                  <tr key={experiment.id}>
                    <td className="px-4 py-3 text-sm font-medium">
                      {experiment.name}
                    </td>
                    <td className="px-4 py-3 text-sm">
                      {experiment.hypothesis}
                    </td>
                    <td className="px-4 py-3 text-sm hidden md:table-cell">
                      {experiment.metrics}
                    </td>
                    <td className="px-4 py-3 text-sm">
                      <span 
                        className={`px-2 py-1 rounded-full text-xs font-medium ${
                          experiment.effort === "Baixo" 
                            ? "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400" 
                            : experiment.effort === "Médio"
                            ? "bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-400"
                            : "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400"
                        }`}
                      >
                        {experiment.effort}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-sm">
                      <span 
                        className={`px-2 py-1 rounded-full text-xs font-medium ${
                          experiment.impact === "Baixo" 
                            ? "bg-slate-100 text-slate-800 dark:bg-slate-900/30 dark:text-slate-400" 
                            : experiment.impact === "Médio"
                            ? "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400"
                            : "bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-400"
                        }`}
                      >
                        {experiment.impact}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-sm">
                      <span 
                        className={`px-2 py-1 rounded-full text-xs font-medium ${
                          experiment.status === "Concluído" 
                            ? "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400" 
                            : experiment.status === "Em andamento"
                            ? "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400"
                            : "bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-400"
                        }`}
                      >
                        {experiment.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
        <CardFooter className="flex justify-between">
          <div></div>
          <Button>
            Adicionar Experimento
          </Button>
        </CardFooter>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Aprendizados-Chave</CardTitle>
            <CardDescription>
              Insights dos experimentos concluídos
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="p-3 border rounded-lg space-y-2">
              <div className="flex items-center justify-between">
                <h3 className="font-medium text-sm">Quiz Interativo com Airdrop</h3>
                <span className="text-xs text-green-500 font-semibold">+42% Retenção</span>
              </div>
              <p className="text-sm text-muted-foreground">
                Usuários que completaram o quiz educacional tiveram 42% maior taxa de retenção 
                após 30 dias comparado ao grupo de controle.
              </p>
              <div className="flex space-x-2 text-xs">
                <div className="px-2 py-0.5 bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400 rounded-full">
                  Educação
                </div>
                <div className="px-2 py-0.5 bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400 rounded-full">
                  Incentivos
                </div>
                <div className="px-2 py-0.5 bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-400 rounded-full">
                  Ativação
                </div>
              </div>
            </div>

            <div className="space-y-2">
              <div className="text-sm font-medium">Próximo Experimento Prioritário</div>
              
              <div className="p-3 border border-amber-200 dark:border-amber-800 bg-amber-50/50 dark:bg-amber-900/20 rounded-lg space-y-2">
                <h3 className="font-medium text-sm flex items-center">
                  <Rocket className="h-4 w-4 mr-1 text-amber-500" />
                  <span>Conteúdo Simplificado para Onboarding</span>
                </h3>
                <p className="text-sm text-muted-foreground">
                  Foco em reduzir a complexidade das explicações técnicas durante o onboarding.
                  Objetivo: Aumentar a taxa de conclusão de onboarding em 25%.
                </p>
                <div className="flex justify-between text-xs">
                  <span className="text-muted-foreground">Início: 15/04/2025</span>
                  <span className="text-muted-foreground">Duração: 2 semanas</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-base">Framework North Star</CardTitle>
            <CardDescription>
              Métricas principais e fatores de influência
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="p-4 border rounded-lg bg-blue-50/50 dark:bg-blue-900/20 text-center space-y-2">
              <h3 className="font-bold text-lg">TVL (Valor Total Bloqueado)</h3>
              <div className="text-3xl font-bold text-blue-600 dark:text-blue-400">$12.4M</div>
              <p className="text-sm text-muted-foreground">
                Métrica principal que mede a saúde econômica do protocolo
              </p>
            </div>

            <div className="text-sm font-medium">Fatores de Influência</div>
            
            <div className="grid grid-cols-2 gap-3">
              <div className="p-3 border rounded-lg space-y-1">
                <div className="flex justify-between items-center">
                  <h3 className="text-sm font-medium flex items-center">
                    <Users className="h-3 w-3 mr-1" />
                    <span>Usuários Ativos</span>
                  </h3>
                  <span className="text-xs font-bold">5,240</span>
                </div>
                <div className="flex items-center space-x-1 text-xs">
                  <ArrowRight className="h-3 w-3 text-green-500" />
                  <span className="text-green-500">+12% esta semana</span>
                </div>
              </div>

              <div className="p-3 border rounded-lg space-y-1">
                <div className="flex justify-between items-center">
                  <h3 className="text-sm font-medium flex items-center">
                    <Zap className="h-3 w-3 mr-1" />
                    <span>Valor/Transação</span>
                  </h3>
                  <span className="text-xs font-bold">$842</span>
                </div>
                <div className="flex items-center space-x-1 text-xs">
                  <ArrowRight className="h-3 w-3 text-green-500" />
                  <span className="text-green-500">+3.5% esta semana</span>
                </div>
              </div>

              <div className="p-3 border rounded-lg space-y-1">
                <div className="flex justify-between items-center">
                  <h3 className="text-sm font-medium flex items-center">
                    <Clock className="h-3 w-3 mr-1" />
                    <span>Tempo Médio de Lock</span>
                  </h3>
                  <span className="text-xs font-bold">64 dias</span>
                </div>
                <div className="flex items-center space-x-1 text-xs">
                  <ArrowRight className="h-3 w-3 text-amber-500" />
                  <span className="text-amber-500">-2% esta semana</span>
                </div>
              </div>

              <div className="p-3 border rounded-lg space-y-1">
                <div className="flex justify-between items-center">
                  <h3 className="text-sm font-medium flex items-center">
                    <Heart className="h-3 w-3 mr-1" />
                    <span>Taxa de Retenção</span>
                  </h3>
                  <span className="text-xs font-bold">68%</span>
                </div>
                <div className="flex items-center space-x-1 text-xs">
                  <ArrowRight className="h-3 w-3 text-green-500" />
                  <span className="text-green-500">+5% esta semana</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight">Marketing & Crescimento</h1>
        <div className="flex space-x-2">
          <Button variant="outline">
            <Download className="mr-2 h-4 w-4" />
            Exportar Plano
          </Button>
          <Button>
            <Share2 className="mr-2 h-4 w-4" />
            Compartilhar
          </Button>
        </div>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="growth-strategy" className="flex items-center gap-1">
            <TrendingUp className="h-4 w-4" />
            <span>Estratégia</span>
          </TabsTrigger>
          <TabsTrigger value="marketing-channels" className="flex items-center gap-1">
            <Megaphone className="h-4 w-4" />
            <span>Canais de Marketing</span>
          </TabsTrigger>
          <TabsTrigger value="community-building" className="flex items-center gap-1">
            <Users className="h-4 w-4" />
            <span>Comunidade</span>
          </TabsTrigger>
          <TabsTrigger value="growth-experiments" className="flex items-center gap-1">
            <BarChartIcon className="h-4 w-4" />
            <span>Experimentos</span>
          </TabsTrigger>
        </TabsList>
        
        <div className="mt-6">
          <TabsContent value="growth-strategy">
            {renderGrowthStrategy()}
          </TabsContent>
          
          <TabsContent value="marketing-channels">
            {renderMarketingChannels()}
          </TabsContent>
          
          <TabsContent value="community-building">
            {renderCommunityBuilding()}
          </TabsContent>
          
          <TabsContent value="growth-experiments">
            {renderGrowthExperiments()}
          </TabsContent>
        </div>
      </Tabs>
    </div>
  );
}