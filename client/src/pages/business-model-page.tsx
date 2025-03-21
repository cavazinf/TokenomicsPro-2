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
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";
import { 
  CheckCircle2, 
  XCircle, 
  Download, 
  FileText, 
  Share2, 
  Users, 
  Layers, 
  ArrowRight,
  DollarSign,
  Rocket,
  Building2,
  PieChart,
  UserCheck
} from "lucide-react";

export default function BusinessModel() {
  const [activeTab, setActiveTab] = useState("canvas");
  const [selectedTemplate, setSelectedTemplate] = useState<string | null>(null);

  // Modelo de Negócios Canvas
  const [canvasData, setCanvasData] = useState({
    keyPartners: "",
    keyActivities: "",
    keyResources: "",
    valueProposition: "",
    customerRelationships: "",
    channels: "",
    customerSegments: "",
    costStructure: "",
    revenueStreams: ""
  });

  // Modelos de Negócios Web3
  const businessModels = [
    {
      id: "token-utility",
      name: "Utilidade de Token",
      description: "Modelo baseado em token com utilidade específica dentro do ecossistema",
      examples: ["Filecoin (armazenamento)", "Basic Attention Token (atenção/publicidade)"],
      strengths: [
        "Incentivo direto para uso da plataforma",
        "Alinhamento entre detentores de token e usuários",
        "Potencial para efeitos de rede"
      ],
      challenges: [
        "Necessidade de utilidade genuína",
        "Dependência do crescimento do ecossistema",
        "Regulamentação incerta em algumas jurisdições"
      ],
      tokenomicsConsiderations: [
        "Mecanismos de queima para capturar valor",
        "Oferta limitada para escassez",
        "Utilidade que escala com adoção"
      ]
    },
    {
      id: "staking-rewards",
      name: "Staking e Recompensas",
      description: "Modelo onde tokens são bloqueados para receber recompensas/juros",
      examples: ["Ethereum (ETH staking)", "Cosmos (ATOM)", "Solana (SOL)"],
      strengths: [
        "Redução de circulação ativa",
        "Alinhamento de incentivos de longo prazo",
        "Suporte à segurança da rede através de staking"
      ],
      challenges: [
        "Necessidade de alto rendimento para competir",
        "Risco de instabilidade se grandes holders desistirem",
        "Centralização potencial entre stakers grandes"
      ],
      tokenomicsConsiderations: [
        "Equilíbrio entre inflação para recompensas e valor capturado",
        "Períodos de lock adequados para estabilidade",
        "Modelo de distribuição das recompensas"
      ]
    },
    {
      id: "governance",
      name: "Governança & DAOs",
      description: "Modelo baseado em tokens que conferem direitos de governança/voto",
      examples: ["Uniswap (UNI)", "MakerDAO (MKR)", "Compound (COMP)"],
      strengths: [
        "Descentralização real de tomada de decisão",
        "Comunidade engajada de stakeholders",
        "Potencial para inovação contínua"
      ],
      challenges: [
        "Participação limitada em votações (apatia)",
        "Plutocracias (governança dominada por grandes holders)",
        "Processos decisórios lentos"
      ],
      tokenomicsConsiderations: [
        "Mecanismos de votação ponderada ou quadrática",
        "Incentivos para participação em votações",
        "Captura de valor através de taxas para tesouro"
      ]
    },
    {
      id: "nft-royalties",
      name: "NFTs e Royalties",
      description: "Modelo baseado em ativos digitais únicos com royalties contínuos",
      examples: ["NBA Top Shot", "Bored Ape Yacht Club", "Art Blocks"],
      strengths: [
        "Fluxo de receita contínuo para criadores",
        "Propriedade verificável de bens digitais",
        "Comunidades fortes em torno de coleções"
      ],
      challenges: [
        "Cumprimento técnico de royalties não garantido",
        "Volatilidade de mercado",
        "Saturação potencial de oferta"
      ],
      tokenomicsConsiderations: [
        "Estrutura de royalties sustentável",
        "Utilidade adicional para NFTs (acesso, staking)",
        "Integração com tokens fungíveis para liquidez"
      ]
    },
    {
      id: "tokenized-equity",
      name: "Equity Tokenizada",
      description: "Modelo onde tokens representam participação acionária ou compartilhamento de lucros",
      examples: ["INX Limited", "tZERO", "Blockchain Capital"],
      strengths: [
        "Clareza sobre a proposta de valor",
        "Alinhamento direto com a performance do negócio",
        "Familiar para investidores tradicionais"
      ],
      challenges: [
        "Requisitos regulatórios complexos",
        "Necessidade de registro em várias jurisdições",
        "Potenciais limitações de transferência"
      ],
      tokenomicsConsiderations: [
        "Estrutura de dividendos/distribuição de lucros",
        "Captura de valor direta via performance empresarial",
        "Tokenomics compatível com requisitos regulatórios"
      ]
    }
  ];

  // Revenue Models para comparação
  const revenueModels = [
    { category: "Tradicional", model: "Assinatura", example: "Adobe Creative Cloud", web3Equivalente: "Taxas de acesso recorrentes pagas em tokens" },
    { category: "Tradicional", model: "Freemium", example: "Dropbox", web3Equivalente: "Acesso básico gratuito, recursos premium via staking ou pagamento em tokens" },
    { category: "Tradicional", model: "Transacional", example: "eBay", web3Equivalente: "Taxas de protocolo em transações (0.1-3%)" },
    { category: "Tradicional", model: "Publicidade", example: "Google", web3Equivalente: "Atenção tokenizada (BAT) ou espaços publicitários leiloados via smart contracts" },
    { category: "Web3", model: "Taxas de Protocolo", example: "Uniswap", web3Equivalente: "Pequena taxa sobre transações direcionada ao tesouro ou detentores" },
    { category: "Web3", model: "Captura de Valor via Token", example: "ETH (EIP-1559)", web3Equivalente: "Queima de tokens para criar escassez com base no uso" },
    { category: "Web3", model: "Staking/Farming", example: "Curve Finance", web3Equivalente: "Recompensas de protocolo por prover liquidez ou segurança" },
    { category: "Web3", model: "NFT Royalties", example: "OpenSea Collections", web3Equivalente: "2.5-10% de royalties em vendas secundárias" },
    { category: "Web3", model: "Governança Paga", example: "Snapshot/Squads/Llama", web3Equivalente: "Taxas para propostas ou execução de decisões de governança" },
  ];

  // Tokenomics Configuration Models
  const tokenomicsModels = [
    {
      id: "token-utility",
      name: "Modelo de Utilidade",
      configurations: [
        { category: "Supply", value: "Limitado (100M-10B)" },
        { category: "Emissão", value: "Maioria no TGE, pequena inflação para recompensas" },
        { category: "Mecânica de Valor", value: "Queima baseada em uso, lock para acesso a serviços" },
        { category: "Incentivos", value: "Descontos por usar token, benefícios por segmentar" },
        { category: "Governança", value: "Limitada - principalmente decisões sobre utilidade" }
      ]
    },
    {
      id: "staking-rewards",
      name: "Modelo de Staking",
      configurations: [
        { category: "Supply", value: "Inflacionário com limite máximo ou ilimitado" },
        { category: "Emissão", value: "Inicial + emissão contínua para recompensas" },
        { category: "Mecânica de Valor", value: "Recompensas por bloquear tokens, períodos de lock" },
        { category: "Incentivos", value: "APY competitiva, recompensas compostas" },
        { category: "Governança", value: "Votação baseada em quantidade staked e tempo" }
      ]
    },
    {
      id: "governance",
      name: "Modelo de Governança",
      configurations: [
        { category: "Supply", value: "Fixo ou levemente inflacionário" },
        { category: "Emissão", value: "Airdrop para usuários + reserva para tesouro" },
        { category: "Mecânica de Valor", value: "Taxas para tesouro, compartilhamento de receitas" },
        { category: "Incentivos", value: "Poder de voto, capacidade de proposição" },
        { category: "Governança", value: "Abrangente - controle total de parâmetros" }
      ]
    },
    {
      id: "nft-royalties",
      name: "Modelo de NFTs + Royalties",
      configurations: [
        { category: "Supply", value: "Edições limitadas, coleções de diferentes raridades" },
        { category: "Emissão", value: "Lançamentos em fases, mints limitados" },
        { category: "Mecânica de Valor", value: "Royalties em vendas secundárias (5-10%)" },
        { category: "Incentivos", value: "Utilidade em ecosistema, acesso exclusivo" },
        { category: "Governança", value: "Voto ponderado por raridade ou quantidade" }
      ]
    },
    {
      id: "tokenized-equity",
      name: "Modelo de Equity Tokenizada",
      configurations: [
        { category: "Supply", value: "Fixo, representando ações da empresa" },
        { category: "Emissão", value: "Venda inicial + possível diluição futura" },
        { category: "Mecânica de Valor", value: "Dividendos, compartilhamento de lucros" },
        { category: "Incentivos", value: "Retorno financeiro direto" },
        { category: "Governança", value: "Similar a ações - votação proporcional à posse" }
      ]
    }
  ];

  const handleCanvasChange = (field: keyof typeof canvasData, value: string) => {
    setCanvasData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const renderBusinessModelCanvas = () => (
    <div className="space-y-6">
      <div className="bg-muted/30 p-4 rounded-lg">
        <h3 className="font-medium text-lg mb-2">Business Model Canvas</h3>
        <p className="text-muted-foreground">
          O Business Model Canvas é uma ferramenta estratégica que permite descrever, desenhar e analisar
          o modelo de negócios da sua startup. Preencha cada componente para criar uma visão completa.
        </p>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-4">
        <div className="xl:col-span-1 space-y-4">
          <Card>
            <CardHeader className="bg-blue-50 dark:bg-blue-950/30">
              <CardTitle className="text-base">Parcerias Principais</CardTitle>
              <CardDescription>Quem são seus principais parceiros e fornecedores?</CardDescription>
            </CardHeader>
            <CardContent className="pt-4">
              <Textarea 
                placeholder="Liste suas parcerias chave" 
                rows={6}
                value={canvasData.keyPartners}
                onChange={(e) => handleCanvasChange('keyPartners', e.target.value)}
              />
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="bg-indigo-50 dark:bg-indigo-950/30">
              <CardTitle className="text-base">Atividades Principais</CardTitle>
              <CardDescription>Quais atividades seu modelo de negócios requer?</CardDescription>
            </CardHeader>
            <CardContent className="pt-4">
              <Textarea 
                placeholder="Descreva as atividades essenciais" 
                rows={6}
                value={canvasData.keyActivities}
                onChange={(e) => handleCanvasChange('keyActivities', e.target.value)}
              />
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="bg-purple-50 dark:bg-purple-950/30">
              <CardTitle className="text-base">Recursos Principais</CardTitle>
              <CardDescription>Quais recursos são necessários?</CardDescription>
            </CardHeader>
            <CardContent className="pt-4">
              <Textarea 
                placeholder="Liste seus recursos essenciais" 
                rows={6}
                value={canvasData.keyResources}
                onChange={(e) => handleCanvasChange('keyResources', e.target.value)}
              />
            </CardContent>
          </Card>
        </div>

        <div className="xl:col-span-1 space-y-4">
          <Card className="xl:mt-16">
            <CardHeader className="bg-green-50 dark:bg-green-950/30">
              <CardTitle className="text-base">Proposta de Valor</CardTitle>
              <CardDescription>Que valor você entrega ao cliente?</CardDescription>
            </CardHeader>
            <CardContent className="pt-4">
              <Textarea 
                placeholder="Descreva sua proposta de valor única" 
                rows={12}
                value={canvasData.valueProposition}
                onChange={(e) => handleCanvasChange('valueProposition', e.target.value)}
              />
            </CardContent>
          </Card>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card>
              <CardHeader className="bg-amber-50 dark:bg-amber-950/30">
                <CardTitle className="text-base">Relacionamento com Clientes</CardTitle>
                <CardDescription>Como você se relaciona com seus clientes?</CardDescription>
              </CardHeader>
              <CardContent className="pt-4">
                <Textarea 
                  placeholder="Descreva os relacionamentos" 
                  rows={6}
                  value={canvasData.customerRelationships}
                  onChange={(e) => handleCanvasChange('customerRelationships', e.target.value)}
                />
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="bg-orange-50 dark:bg-orange-950/30">
                <CardTitle className="text-base">Canais</CardTitle>
                <CardDescription>Como você alcança seus clientes?</CardDescription>
              </CardHeader>
              <CardContent className="pt-4">
                <Textarea 
                  placeholder="Liste seus canais" 
                  rows={6}
                  value={canvasData.channels}
                  onChange={(e) => handleCanvasChange('channels', e.target.value)}
                />
              </CardContent>
            </Card>
          </div>
        </div>

        <div className="xl:col-span-1 space-y-4">
          <Card>
            <CardHeader className="bg-red-50 dark:bg-red-950/30">
              <CardTitle className="text-base">Segmentos de Clientes</CardTitle>
              <CardDescription>Para quem você cria valor?</CardDescription>
            </CardHeader>
            <CardContent className="pt-4">
              <Textarea 
                placeholder="Liste seus segmentos de clientes" 
                rows={6}
                value={canvasData.customerSegments}
                onChange={(e) => handleCanvasChange('customerSegments', e.target.value)}
              />
            </CardContent>
          </Card>

          <Card className="mt-auto">
            <CardHeader className="bg-slate-50 dark:bg-slate-950/30">
              <CardTitle className="text-base">Estrutura de Custos</CardTitle>
              <CardDescription>Quais são os custos mais importantes?</CardDescription>
            </CardHeader>
            <CardContent className="pt-4">
              <Textarea 
                placeholder="Descreva sua estrutura de custos" 
                rows={6}
                value={canvasData.costStructure}
                onChange={(e) => handleCanvasChange('costStructure', e.target.value)}
              />
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="bg-emerald-50 dark:bg-emerald-950/30">
              <CardTitle className="text-base">Fontes de Receita</CardTitle>
              <CardDescription>Como você gera receita?</CardDescription>
            </CardHeader>
            <CardContent className="pt-4">
              <Textarea 
                placeholder="Liste suas fontes de receita" 
                rows={6}
                value={canvasData.revenueStreams}
                onChange={(e) => handleCanvasChange('revenueStreams', e.target.value)}
              />
            </CardContent>
          </Card>
        </div>
      </div>

      <div className="flex justify-end gap-2 pt-4">
        <Button variant="outline">
          <FileText className="mr-2 h-4 w-4" />
          Salvar Rascunho
        </Button>
        <Button variant="outline">
          <Download className="mr-2 h-4 w-4" />
          Exportar PDF
        </Button>
        <Button variant="outline">
          <Share2 className="mr-2 h-4 w-4" />
          Compartilhar
        </Button>
      </div>
    </div>
  );

  const renderWeb3BusinessModels = () => (
    <div className="space-y-6">
      <div className="bg-muted/30 p-4 rounded-lg">
        <h3 className="font-medium text-lg mb-2">Modelos de Negócios Web3</h3>
        <p className="text-muted-foreground">
          Explore diferentes modelos de negócios nativos de Web3 e suas características.
          Selecione um modelo para ver detalhes ou use como inspiração para seu projeto.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-4">
          {businessModels.map((model) => (
            <div
              key={model.id}
              className={`border rounded-lg p-4 cursor-pointer transition-colors ${
                selectedTemplate === model.id 
                  ? 'border-primary bg-primary/5' 
                  : 'hover:bg-muted/50'
              }`}
              onClick={() => setSelectedTemplate(model.id)}
            >
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="font-medium">{model.name}</h3>
                  <p className="text-sm text-muted-foreground">{model.description}</p>
                </div>
                {selectedTemplate === model.id && <CheckCircle2 className="h-5 w-5 text-primary" />}
              </div>
            </div>
          ))}
        </div>

        <div className="lg:col-span-2">
          {selectedTemplate ? (
            <Card>
              <CardHeader>
                <CardTitle>
                  {businessModels.find(m => m.id === selectedTemplate)?.name}
                </CardTitle>
                <CardDescription>
                  {businessModels.find(m => m.id === selectedTemplate)?.description}
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div>
                  <h3 className="text-sm font-medium mb-2">Exemplos</h3>
                  <div className="flex flex-wrap gap-2">
                    {businessModels
                      .find(m => m.id === selectedTemplate)
                      ?.examples.map((example, i) => (
                        <div 
                          key={i} 
                          className="bg-secondary/20 text-secondary-foreground px-2 py-1 rounded text-sm"
                        >
                          {example}
                        </div>
                      ))}
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h3 className="text-sm font-medium mb-2">Pontos Fortes</h3>
                    <ul className="space-y-1">
                      {businessModels
                        .find(m => m.id === selectedTemplate)
                        ?.strengths.map((strength, i) => (
                          <li key={i} className="flex items-start gap-2 text-sm">
                            <CheckCircle2 className="h-4 w-4 text-green-500 mt-0.5" />
                            <span>{strength}</span>
                          </li>
                        ))}
                    </ul>
                  </div>

                  <div>
                    <h3 className="text-sm font-medium mb-2">Desafios</h3>
                    <ul className="space-y-1">
                      {businessModels
                        .find(m => m.id === selectedTemplate)
                        ?.challenges.map((challenge, i) => (
                          <li key={i} className="flex items-start gap-2 text-sm">
                            <XCircle className="h-4 w-4 text-red-500 mt-0.5" />
                            <span>{challenge}</span>
                          </li>
                        ))}
                    </ul>
                  </div>
                </div>

                <Separator />

                <div>
                  <h3 className="text-sm font-medium mb-2">Considerações de Tokenomics</h3>
                  <ul className="space-y-1">
                    {businessModels
                      .find(m => m.id === selectedTemplate)
                      ?.tokenomicsConsiderations.map((consideration, i) => (
                        <li key={i} className="flex items-start gap-2 text-sm">
                          <ArrowRight className="h-4 w-4 text-blue-500 mt-0.5" />
                          <span>{consideration}</span>
                        </li>
                      ))}
                  </ul>
                </div>

                <div className="bg-muted/50 p-4 rounded-lg mt-4">
                  <h3 className="font-medium mb-2">Configuração de Tokenomics Recomendada</h3>
                  
                  <div className="rounded-md border">
                    <table className="min-w-full divide-y divide-border">
                      <thead>
                        <tr>
                          <th className="px-4 py-2 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                            Categoria
                          </th>
                          <th className="px-4 py-2 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                            Configuração
                          </th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-border">
                        {tokenomicsModels.find(m => m.id === selectedTemplate)
                          ?.configurations.map((config, i) => (
                            <tr key={i}>
                              <td className="px-4 py-2 text-sm font-medium">
                                {config.category}
                              </td>
                              <td className="px-4 py-2 text-sm">
                                {config.value}
                              </td>
                            </tr>
                          ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </CardContent>
              <CardFooter className="flex justify-between">
                <Button variant="outline">
                  <FileText className="mr-2 h-4 w-4" />
                  Tutorial Completo
                </Button>
                <Button>
                  Usar este Modelo
                </Button>
              </CardFooter>
            </Card>
          ) : (
            <div className="flex items-center justify-center h-full border rounded-lg p-8">
              <div className="text-center">
                <Layers className="h-12 w-12 text-muted-foreground mx-auto mb-4 opacity-50" />
                <h3 className="text-lg font-medium">Selecione um Modelo</h3>
                <p className="text-muted-foreground mt-2 max-w-md">
                  Escolha um modelo de negócio Web3 à esquerda para visualizar seus detalhes, 
                  pontos fortes, desafios e considerações de tokenomics.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );

  const renderRevenueModels = () => (
    <div className="space-y-6">
      <div className="bg-muted/30 p-4 rounded-lg">
        <h3 className="font-medium text-lg mb-2">Modelos de Receita</h3>
        <p className="text-muted-foreground">
          Compare modelos de receita tradicionais com suas contrapartes Web3.
          Esta tabela mostra como modelos de negócios tradicionais foram adaptados para o contexto blockchain.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Comparação de Modelos de Receita</CardTitle>
          <CardDescription>
            Tradicionais vs. Web3
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="rounded-md border">
            <table className="min-w-full divide-y divide-border">
              <thead className="bg-muted/50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                    Categoria
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                    Modelo de Receita
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                    Exemplo Tradicional
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                    Equivalente Web3
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                {revenueModels.map((model, i) => (
                  <tr key={i} className={model.category === "Web3" ? "bg-primary/5" : ""}>
                    <td className="px-4 py-3 text-sm">
                      {model.category}
                    </td>
                    <td className="px-4 py-3 text-sm font-medium">
                      {model.model}
                    </td>
                    <td className="px-4 py-3 text-sm">
                      {model.example}
                    </td>
                    <td className="px-4 py-3 text-sm">
                      {model.web3Equivalente}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <DollarSign className="h-5 w-5 text-green-500" />
              <span>Principais Fontes de Receita Web3</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-4">
              <li className="space-y-1">
                <div className="font-medium">Taxas de Protocolo (0.1-3%)</div>
                <p className="text-sm text-muted-foreground">
                  Pequena taxa cobrada sobre transações ou atividades realizadas no protocolo.
                  Exemplo: 0.3% nas trocas do Uniswap, direcionadas para os provedores de liquidez.
                </p>
              </li>
              <li className="space-y-1">
                <div className="font-medium">Staking e Yield Farming</div>
                <p className="text-sm text-muted-foreground">
                  Emissão de tokens como recompensa para usuários que bloqueiam ativos ou fornecem
                  liquidez. Pode gerar receita através da diferença entre APY oferecido e ganho.
                </p>
              </li>
              <li className="space-y-1">
                <div className="font-medium">Royalties em NFTs (2.5-10%)</div>
                <p className="text-sm text-muted-foreground">
                  Percentual sobre vendas secundárias de NFTs, permitindo receita contínua para
                  criadores e potencialmente para o protocolo/plataforma.
                </p>
              </li>
              <li className="space-y-1">
                <div className="font-medium">Premium Features</div>
                <p className="text-sm text-muted-foreground">
                  Funcionalidades avançadas desbloqueadas através de assinatura ou staking de tokens
                  no protocolo, criando utilidade adicional.
                </p>
              </li>
            </ul>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Rocket className="h-5 w-5 text-blue-500" />
              <span>Tendências Emergentes em Receita</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-4">
              <li className="space-y-1">
                <div className="font-medium">Real World Asset (RWA) Tokenization</div>
                <p className="text-sm text-muted-foreground">
                  Receita através da tokenização de ativos do mundo real (imóveis, commodities, etc.),
                  cobrando taxas de emissão, gestão e transação desses tokens.
                </p>
              </li>
              <li className="space-y-1">
                <div className="font-medium">Subscription DAOs</div>
                <p className="text-sm text-muted-foreground">
                  Modelos de assinatura descentralizados onde membros pagam taxas periódicas
                  em troca de benefícios contínuos, como acesso a conteúdo exclusivo.
                </p>
              </li>
              <li className="space-y-1">
                <div className="font-medium">Pay-per-use Infrastructure</div>
                <p className="text-sm text-muted-foreground">
                  Micropagamentos por uso de infraestrutura descentralizada (armazenamento,
                  computação, bandwidth) com base na demanda real.
                </p>
              </li>
              <li className="space-y-1">
                <div className="font-medium">Tokenized Intellectual Property</div>
                <p className="text-sm text-muted-foreground">
                  Fracionamento e licenciamento de propriedade intelectual via tokens,
                  permitindo receitas de licenciamento e royalties distribuídas.
                </p>
              </li>
            </ul>
          </CardContent>
        </Card>
      </div>

      <div className="flex justify-end gap-2 pt-4">
        <Button variant="outline">
          <Download className="mr-2 h-4 w-4" />
          Exportar Comparação
        </Button>
        <Button>
          Criar Modelo de Receita
        </Button>
      </div>
    </div>
  );

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight">Modelos de Negócio</h1>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="canvas" className="flex items-center gap-1">
            <Building2 className="h-4 w-4" />
            <span>Business Canvas</span>
          </TabsTrigger>
          <TabsTrigger value="web3-models" className="flex items-center gap-1">
            <PieChart className="h-4 w-4" />
            <span>Modelos Web3</span>
          </TabsTrigger>
          <TabsTrigger value="revenue-models" className="flex items-center gap-1">
            <DollarSign className="h-4 w-4" />
            <span>Fontes de Receita</span>
          </TabsTrigger>
        </TabsList>
        
        <div className="mt-6">
          <TabsContent value="canvas">
            {renderBusinessModelCanvas()}
          </TabsContent>
          
          <TabsContent value="web3-models">
            {renderWeb3BusinessModels()}
          </TabsContent>
          
          <TabsContent value="revenue-models">
            {renderRevenueModels()}
          </TabsContent>
        </div>
      </Tabs>
    </div>
  );
}