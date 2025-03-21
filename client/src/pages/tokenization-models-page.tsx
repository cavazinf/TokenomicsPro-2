import React, { useState } from 'react';
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Label } from "@/components/ui/label";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Separator } from "@/components/ui/separator";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Checkbox } from "@/components/ui/checkbox";
import { Download, Info, CheckCircle2, ShieldCheck, Users, Coins, FileText, ArrowRight } from "lucide-react";

export default function TokenizationModels() {
  const [activeTab, setActiveTab] = useState("industry-models");
  const [selectedModel, setSelectedModel] = useState<string | null>(null);
  const [selectedFeatures, setSelectedFeatures] = useState<string[]>([]);

  const handleFeatureToggle = (featureId: string) => {
    if (selectedFeatures.includes(featureId)) {
      setSelectedFeatures(selectedFeatures.filter(id => id !== featureId));
    } else {
      setSelectedFeatures([...selectedFeatures, featureId]);
    }
  };

  // Modelos de tokenização por indústria
  const industryModels = [
    {
      id: "gaming",
      name: "Gaming & Metaverse",
      description: "Modelos de token para ecossistemas de jogos e ambientes virtuais compartilhados.",
      icon: <Users className="h-5 w-5 text-indigo-500" />,
      bgColor: "bg-indigo-50",
      examples: ["Axie Infinity (AXS)", "The Sandbox (SAND)", "Decentraland (MANA)"],
      features: [
        "Ativos virtuais negociáveis (NFTs)",
        "Governança da plataforma de jogo",
        "Play-to-earn e recompensas",
        "Acesso a áreas exclusivas/eventos",
        "Staking para multiplicadores no jogo"
      ]
    },
    {
      id: "defi",
      name: "DeFi (Finanças Descentralizadas)",
      description: "Modelos para protocolos financeiros descentralizados, como empréstimos e negociações.",
      icon: <Coins className="h-5 w-5 text-blue-500" />,
      bgColor: "bg-blue-50",
      examples: ["Uniswap (UNI)", "Aave (AAVE)", "Compound (COMP)"],
      features: [
        "Governança do protocolo",
        "Compartilhamento de taxas/receitas",
        "Incentivos de liquidez",
        "Staking e recompensas",
        "Empréstimos e colaterais"
      ]
    },
    {
      id: "realestate",
      name: "Imobiliário Tokenizado",
      description: "Modelos para tokenização de ativos imobiliários e REITs descentralizados.",
      icon: <ShieldCheck className="h-5 w-5 text-green-500" />,
      bgColor: "bg-green-50",
      examples: ["RealT", "Propy", "LoftY"],
      features: [
        "Fracionamento de propriedades",
        "Distribuição de renda (aluguéis)",
        "Governança de DAOs imobiliárias",
        "Liquidez para ativos ilíquidos",
        "Registro de propriedade em blockchain"
      ]
    },
    {
      id: "content",
      name: "Criação e Curadoria de Conteúdo",
      description: "Modelos para plataformas de conteúdo descentralizadas e economia de criadores.",
      icon: <FileText className="h-5 w-5 text-purple-500" />,
      bgColor: "bg-purple-50",
      examples: ["Audius (AUDIO)", "Livepeer (LPT)", "Mirror"],
      features: [
        "Recompensas para criação de conteúdo",
        "Incentivos para curadoria",
        "NFTs de mídia e obras de arte",
        "Governança de plataforma",
        "Modelos de assinatura descentralizados"
      ]
    }
  ];

  // Frameworks de tokenização
  const tokenizationFrameworks = [
    {
      id: "utility-tokens",
      name: "Tokens Utilitários",
      description: "Frameworks para tokens com utilidade funcional dentro de um ecossistema específico.",
      applications: ["Acesso a serviços", "Pagamentos dentro da plataforma", "Descontos e benefícios para usuários"],
      considerations: ["Clara proposta de valor para usuários", "Equilíbrio de oferta/demanda", "Mecanismos de queima"],
    },
    {
      id: "security-tokens",
      name: "Tokens de Segurança/Ativos",
      description: "Frameworks para tokenização de ativos financeiros e securitização blockchain.",
      applications: ["Ações tokenizadas", "Títulos de dívida", "Fundos de investimento e REITs"],
      considerations: ["Conformidade regulatória (KYC/AML)", "Dividendos e direitos", "Custódia e transferência legal"],
    },
    {
      id: "governance-tokens",
      name: "Tokens de Governança",
      description: "Frameworks para tokens focados em direitos de governança e votação em DAOs.",
      applications: ["Votação de propostas", "Controle de parâmetros de protocolos", "Alocação de fundos do tesouro"],
      considerations: ["Distribuição inicial justa", "Proteção contra ataques Sybil", "Mecanismos de delegação"],
    },
    {
      id: "reward-tokens",
      name: "Tokens de Recompensa",
      description: "Frameworks para tokens que incentivam comportamentos desejados na rede.",
      applications: ["Programas de fidelidade", "Staking e farming", "Contribuições para desenvolvimento"],
      considerations: ["Sustentabilidade de longo prazo", "Inflação controlada", "Prevenção de mercenários"],
    },
    {
      id: "nfts",
      name: "NFTs & Tokens Semi-Fungíveis",
      description: "Frameworks para tokens não-fungíveis e tokens com características únicas.",
      applications: ["Colecionáveis digitais", "Acesso a eventos/comunidades", "Representação de ativos únicos"],
      considerations: ["Royalties para criadores", "Metadados e armazenamento", "Interoperabilidade entre plataformas"],
    }
  ];
  
  // Características personalizáveis para modelos de token
  const customizableFeatures = [
    {
      id: "supply-model",
      name: "Modelo de Oferta",
      options: [
        { id: "fixed", name: "Oferta Fixa" },
        { id: "inflationary", name: "Inflacionário" },
        { id: "deflationary", name: "Deflacionário" },
        { id: "elastic", name: "Oferta Elástica" }
      ]
    },
    {
      id: "governance",
      name: "Governança",
      options: [
        { id: "voting", name: "Votação direta" },
        { id: "delegation", name: "Delegação" },
        { id: "quadratic", name: "Votação quadrática" },
        { id: "holographic", name: "Consenso holográfico" }
      ]
    },
    {
      id: "economics",
      name: "Mecanismos Econômicos",
      options: [
        { id: "staking", name: "Staking e Recompensas" },
        { id: "burn", name: "Mecanismos de Queima" },
        { id: "bonding", name: "Bonding Curves" },
        { id: "fee-sharing", name: "Compartilhamento de Taxas" }
      ]
    },
    {
      id: "utility",
      name: "Utilidade e Acesso",
      options: [
        { id: "payment", name: "Meio de Pagamento" },
        { id: "discount", name: "Descontos em Serviços" },
        { id: "access", name: "Acesso a Recursos/Plataforma" },
        { id: "status", name: "Status/Benefícios por Nível" }
      ]
    },
    {
      id: "compliance",
      name: "Compliance e Controle",
      options: [
        { id: "kyc", name: "KYC/AML Integrado" },
        { id: "transfer-restrictions", name: "Restrições de Transferência" },
        { id: "whitelisting", name: "Whitelisting de Endereços" },
        { id: "regulatory-reporting", name: "Relatórios Regulatórios" }
      ]
    }
  ];

  const renderIndustryModels = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {industryModels.map(model => (
          <Card 
            key={model.id}
            className={`hover:shadow-md transition-shadow cursor-pointer ${
              selectedModel === model.id ? 'ring-2 ring-primary' : ''
            }`}
            onClick={() => setSelectedModel(model.id === selectedModel ? null : model.id)}
          >
            <CardHeader className={`${model.bgColor} rounded-t-lg pb-2`}>
              <div className="flex justify-between items-center">
                <div className="flex items-center gap-2">
                  {model.icon}
                  <CardTitle className="text-lg">{model.name}</CardTitle>
                </div>
                {selectedModel === model.id && (
                  <CheckCircle2 className="h-5 w-5 text-primary" />
                )}
              </div>
              <CardDescription>{model.description}</CardDescription>
            </CardHeader>
            <CardContent className="pt-4">
              <div className="space-y-2">
                <div className="text-sm font-medium">Exemplos:</div>
                <div className="flex flex-wrap gap-2">
                  {model.examples.map(example => (
                    <Badge key={example} variant="outline">{example}</Badge>
                  ))}
                </div>
              </div>
              <div className="mt-4">
                <div className="text-sm font-medium">Características principais:</div>
                <ul className="mt-2 space-y-1 text-sm">
                  {model.features.map(feature => (
                    <li key={feature} className="flex items-start">
                      <span className="text-primary mr-2">•</span>
                      <span>{feature}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="flex justify-end">
        <Button variant="outline" className="mr-2">
          Exportar Modelo
        </Button>
        <Button>
          Personalizar Modelo <ArrowRight className="ml-2 h-4 w-4" />
        </Button>
      </div>
    </div>
  );

  const renderTokenizationFrameworks = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-1 space-y-4">
          <div className="bg-muted/50 p-4 rounded-lg">
            <h3 className="font-medium flex items-center gap-2">
              <Info className="h-4 w-4 text-muted-foreground" />
              Frameworks de Tokenização
            </h3>
            <p className="text-sm text-muted-foreground mt-2">
              Selecione um framework para ver seus detalhes e características. Cada framework oferece 
              diferentes abordagens para criar valor e utilidade através de tokens.
            </p>
          </div>

          <div className="border rounded-lg overflow-hidden">
            <RadioGroup
              value={selectedModel || ''}
              onValueChange={setSelectedModel}
              className="divide-y"
            >
              {tokenizationFrameworks.map(framework => (
                <div key={framework.id} className="p-3 hover:bg-muted/50">
                  <div className="flex items-start space-x-3">
                    <RadioGroupItem value={framework.id} id={framework.id} className="mt-1" />
                    <div className="grid gap-1.5">
                      <Label htmlFor={framework.id} className="font-medium cursor-pointer">
                        {framework.name}
                      </Label>
                      <p className="text-sm text-muted-foreground">
                        {framework.description}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </RadioGroup>
          </div>
        </div>

        <div className="lg:col-span-2">
          {selectedModel ? (
            <Card>
              <CardHeader>
                <CardTitle>
                  {tokenizationFrameworks.find(f => f.id === selectedModel)?.name}
                </CardTitle>
                <CardDescription>
                  {tokenizationFrameworks.find(f => f.id === selectedModel)?.description}
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div>
                  <h3 className="text-sm font-medium mb-2">Aplicações Comuns</h3>
                  <ul className="space-y-2">
                    {tokenizationFrameworks
                      .find(f => f.id === selectedModel)
                      ?.applications.map((app, i) => (
                        <li key={i} className="flex items-start gap-2">
                          <CheckCircle2 className="h-4 w-4 text-green-500 mt-0.5" />
                          <span>{app}</span>
                        </li>
                      ))}
                  </ul>
                </div>

                <Separator />

                <div>
                  <h3 className="text-sm font-medium mb-2">Considerações Principais</h3>
                  <ul className="space-y-2">
                    {tokenizationFrameworks
                      .find(f => f.id === selectedModel)
                      ?.considerations.map((consideration, i) => (
                        <li key={i} className="flex items-start gap-2">
                          <Info className="h-4 w-4 text-blue-500 mt-0.5" />
                          <span>{consideration}</span>
                        </li>
                      ))}
                  </ul>
                </div>

                <div className="bg-muted/50 p-4 rounded-lg mt-4">
                  <h3 className="font-medium mb-2">Compatibilidade Regulatória</h3>
                  <p className="text-sm text-muted-foreground">
                    {selectedModel === 'security-tokens' ? (
                      "Alta necessidade de compliance regulatório. Exige KYC/AML, possivelmente registro em entidades reguladoras, e transferências controladas."
                    ) : selectedModel === 'utility-tokens' ? (
                      "Média necessidade de compliance, dependendo da jurisdição. Foco em utilidade genuína e evitando características de valores mobiliários."
                    ) : selectedModel === 'nfts' ? (
                      "Geralmente baixa necessidade de compliance, mas atenção para questões de propriedade intelectual e direitos autorais é essencial."
                    ) : (
                      "Necessidade variável de compliance, dependendo da implementação específica e jurisdição de operação."
                    )}
                  </p>
                </div>
              </CardContent>
              <CardFooter className="flex justify-between">
                <Button variant="outline">
                  <Download className="mr-2 h-4 w-4" /> Guia Completo
                </Button>
                <Button>
                  Usar este Framework <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </CardFooter>
            </Card>
          ) : (
            <div className="flex items-center justify-center h-full border rounded-lg p-8">
              <div className="text-center">
                <Info className="h-10 w-10 text-muted-foreground mx-auto mb-4" />
                <h3 className="text-lg font-medium">Selecione um Framework</h3>
                <p className="text-muted-foreground mt-2">
                  Escolha um modelo de tokenização para visualizar seus detalhes e considerações.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );

  const renderCustomizableFeatures = () => (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Personalize seu Modelo de Tokenização</CardTitle>
          <CardDescription>
            Selecione as características desejadas para o seu modelo de token
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {customizableFeatures.map(category => (
              <div key={category.id} className="space-y-3">
                <h3 className="font-medium">{category.name}</h3>
                <div className="space-y-2">
                  {category.options.map(option => (
                    <div
                      key={option.id}
                      className={`p-3 border rounded-md flex items-center space-x-3 cursor-pointer hover:bg-muted/50 transition-colors ${
                        selectedFeatures.includes(`${category.id}-${option.id}`) ? 'border-primary bg-primary/5' : ''
                      }`}
                      onClick={() => handleFeatureToggle(`${category.id}-${option.id}`)}
                    >
                      <Checkbox
                        id={`${category.id}-${option.id}`}
                        checked={selectedFeatures.includes(`${category.id}-${option.id}`)}
                        onCheckedChange={() => handleFeatureToggle(`${category.id}-${option.id}`)}
                      />
                      <Label
                        htmlFor={`${category.id}-${option.id}`}
                        className="flex-1 cursor-pointer"
                      >
                        {option.name}
                      </Label>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </CardContent>
        <CardFooter className="flex justify-end space-x-2">
          <Button variant="outline">Limpar Seleção</Button>
          <Button disabled={selectedFeatures.length === 0}>
            Gerar Modelo Personalizado
          </Button>
        </CardFooter>
      </Card>

      {selectedFeatures.length > 0 && (
        <Card className="mt-6">
          <CardHeader>
            <CardTitle>Características Selecionadas</CardTitle>
            <CardDescription>
              Seu modelo personalizado com {selectedFeatures.length} características
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {customizableFeatures.map(category => {
                const selectedInCategory = category.options.filter(option => 
                  selectedFeatures.includes(`${category.id}-${option.id}`)
                );
                
                if (selectedInCategory.length === 0) return null;
                
                return (
                  <div key={category.id} className="space-y-2">
                    <h3 className="text-sm font-medium">{category.name}</h3>
                    <ul className="space-y-1">
                      {selectedInCategory.map(option => (
                        <li key={option.id} className="flex items-center gap-2 text-sm">
                          <CheckCircle2 className="h-4 w-4 text-green-500" />
                          <span>{option.name}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight">Modelos de Tokenização</h1>
        <Button variant="outline">
          <Download className="mr-2 h-4 w-4" /> Exportar Modelos
        </Button>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="industry-models">Modelos por Indústria</TabsTrigger>
          <TabsTrigger value="tokenization-frameworks">Frameworks de Tokenização</TabsTrigger>
          <TabsTrigger value="customizable-features">Recursos Personalizáveis</TabsTrigger>
        </TabsList>
        
        <div className="mt-6">
          <TabsContent value="industry-models">
            {renderIndustryModels()}
          </TabsContent>
          
          <TabsContent value="tokenization-frameworks">
            {renderTokenizationFrameworks()}
          </TabsContent>
          
          <TabsContent value="customizable-features">
            {renderCustomizableFeatures()}
          </TabsContent>
        </div>
      </Tabs>
    </div>
  );
}