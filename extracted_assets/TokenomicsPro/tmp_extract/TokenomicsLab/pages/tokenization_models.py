import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Import local modules
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.tokenomics import TokenomicsModel, UtilityTokenModel, GovernanceTokenModel

st.set_page_config(
    page_title="Tokenization Models | Tokenomics Lab",
    page_icon="🏗️",
    layout="wide"
)

# Sidebar
st.sidebar.title("Tokenomics Lab")
st.sidebar.image("https://cdn.jsdelivr.net/npm/cryptocurrency-icons@0.18.1/svg/icon/btc.svg", width=50)

# Main content
st.title("Modelos de Tokenização")
st.markdown("""
    Explore diferentes modelos de tokenização para seu projeto ou startup. 
    Cada modelo oferece características únicas e adequa-se a diferentes tipos de negócios e objetivos.
""")

# Models explanation section
st.header("Entendendo os Modelos de Tokenização")

# Create tabs for different tokenization models
models_tabs = st.tabs([
    "Utility Token", 
    "Security Token", 
    "Governance Token", 
    "Stablecoin", 
    "NFT", 
    "Composto/Híbrido"
])

with models_tabs[0]:
    st.subheader("Utility Token")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **Descrição:**
        Tokens de utilidade fornecem acesso a um produto, serviço ou recurso dentro de um ecossistema específico.

        **Principais Características:**
        - Representam o direito de usar um produto ou serviço
        - Valor derivado da utilidade e demanda pelo serviço
        - Não são considerados investimentos (idealmente)
        - Podem incluir mecanismos de staking ou queima

        **Exemplos de Uso:**
        - Acesso a funcionalidades em plataformas
        - Pagamento de taxas de transação
        - Descontos em serviços
        - Sistema de recompensas
        """)
        
        st.markdown("**Exemplos de Projetos:**")
        st.markdown("- **Filecoin (FIL)**: Acesso e pagamento por armazenamento descentralizado")
        st.markdown("- **Basic Attention Token (BAT)**: Recompensas para atenção do usuário no ecossistema Brave")
        st.markdown("- **Chainlink (LINK)**: Pagamento para oráculos fornecerem dados à rede")
    
    with col2:
        # Simple diagram
        flow_data = pd.DataFrame([
            {"Etapa": "Usuário Adquire Tokens", "Posição": 1, "Valor": 10},
            {"Etapa": "Usuário Utiliza o Serviço", "Posição": 2, "Valor": 10},
            {"Etapa": "Tokens são Utilizados", "Posição": 3, "Valor": 10},
            {"Etapa": "Serviço Entregue", "Posição": 4, "Valor": 10},
        ])
        
        fig = px.bar(
            flow_data, 
            x="Posição", 
            y="Valor", 
            color="Etapa", 
            title="Fluxo de Utility Token",
            labels={"Valor": "", "Posição": ""},
            height=300
        )
        
        fig.update_layout(
            showlegend=True,
            xaxis={'visible': False},
            yaxis={'visible': False}
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Market fit assessment
        st.markdown("### Adequação ao Mercado")
        
        st.markdown("""
        **Ideal para:**
        - Plataformas de tecnologia
        - Marketplaces
        - Sistemas de compartilhamento
        - Redes de serviços
        """)

with models_tabs[1]:
    st.subheader("Security Token")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **Descrição:**
        Security tokens representam ativos de investimento tradicionais como ações, títulos, ou participação em fundos 
        e propriedades, mas tokenizados em uma blockchain.

        **Principais Características:**
        - Representam participação em ativos subjacentes com valor
        - Geralmente sujeitos a regulações de valores mobiliários
        - Podem pagar dividendos ou dar direitos de propriedade
        - Oferecem maior liquidez a ativos tradicionalmente ilíquidos

        **Exemplos de Uso:**
        - Tokenização de ações e participações em empresas
        - Representação de dívida (bonds)
        - Tokenização de imóveis (frações de propriedades)
        - Fundos de investimento tokenizados
        """)
        
        st.markdown("**Exemplos de Projetos:**")
        st.markdown("- **Polymath (POLY)**: Plataforma para criação e gerenciamento de security tokens")
        st.markdown("- **tZERO**: Plataforma de negociação de security tokens")
        st.markdown("- **RealT**: Tokenização de imóveis fracionados")
    
    with col2:
        # Simple diagram
        pie_data = pd.DataFrame([
            {"Categoria": "Retorno aos Investidores", "Valor": 40},
            {"Categoria": "Reserva Legal", "Valor": 25},
            {"Categoria": "Desenvolvimento", "Valor": 20},
            {"Categoria": "Marketing", "Valor": 15}
        ])
        
        fig = px.pie(
            pie_data, 
            values='Valor', 
            names='Categoria', 
            title="Distribuição Típica de Retornos",
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Market fit assessment
        st.markdown("### Adequação ao Mercado")
        
        st.markdown("""
        **Ideal para:**
        - Empresas buscando captar investimento
        - Fundos de investimento
        - Mercado imobiliário
        - Empresas de private equity
        - Mercados financeiros tradicionais
        """)

with models_tabs[2]:
    st.subheader("Governance Token")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **Descrição:**
        Tokens de governança permitem que seus detentores votem em decisões importantes que afetam o futuro de um protocolo ou plataforma, 
        criando um sistema de governança descentralizada.

        **Principais Características:**
        - Representam direitos de voto e poder de decisão
        - Geralmente usados em DAOs (Organizações Autônomas Descentralizadas)
        - Podem incluir direitos adicionais (staking, participação em receitas)
        - Incentivam participação comunitária de longo prazo

        **Exemplos de Uso:**
        - Votação em propostas de melhoria
        - Decisões sobre alocação de recursos
        - Mudanças de parâmetros do protocolo
        - Seleção de provedores de serviços
        """)
        
        st.markdown("**Exemplos de Projetos:**")
        st.markdown("- **Compound (COMP)**: Governança do protocolo de empréstimo Compound")
        st.markdown("- **Uniswap (UNI)**: Governança da exchange descentralizada Uniswap")
        st.markdown("- **MakerDAO (MKR)**: Governança do protocolo que gerencia a stablecoin DAI")
    
    with col2:
        # Simple diagram
        gov_data = pd.DataFrame([
            {"Fase": "Proposta", "Valor": 25},
            {"Fase": "Discussão", "Valor": 25},
            {"Fase": "Votação", "Valor": 25},
            {"Fase": "Implementação", "Valor": 25}
        ])
        
        fig = px.pie(
            gov_data, 
            values='Valor', 
            names='Fase', 
            title="Ciclo de Governança",
            hole=0.4,
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Market fit assessment
        st.markdown("### Adequação ao Mercado")
        
        st.markdown("""
        **Ideal para:**
        - Protocolos DeFi
        - DAOs
        - Projetos orientados à comunidade
        - Plataformas descentralizadas de conteúdo
        - Redes sociais descentralizadas
        """)

with models_tabs[3]:
    st.subheader("Stablecoin")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **Descrição:**
        Stablecoins são tokens criados para manter um valor estável, geralmente atrelado a um ativo ou cesta de ativos 
        como o dólar americano, ouro ou outras moedas fiat.

        **Principais Características:**
        - Valor estável, geralmente ancorado 1:1 com um ativo de referência
        - Diferentes mecanismos de estabilização (colateralização, algoritmos)
        - Reduzem a volatilidade típica das criptomoedas
        - Servem como ponte entre finanças tradicionais e cripto

        **Tipos Principais:**
        - **Colateralizadas por Fiat**: Lastreadas por moedas fiduciárias em custódia (USDC, USDT)
        - **Colateralizadas por Cripto**: Garantidas por criptoativos (DAI)
        - **Algorítmicas**: Usam algoritmos para controlar oferta e manter o peg (FRAX)
        - **Colateralizadas por Commodities**: Lastreadas por ativos como ouro (PAXG)
        """)
        
        st.markdown("**Exemplos de Projetos:**")
        st.markdown("- **USDC (USD Coin)**: Stablecoin colateralizada por dólares americanos")
        st.markdown("- **DAI**: Stablecoin colateralizada por cripto com valor atrelado ao dólar")
        st.markdown("- **FRAX**: Stablecoin parcialmente algorítmica")
    
    with col2:
        # Simple diagram
        stable_data = pd.DataFrame({
            'Data': range(1, 31),
            'Stablecoin': [1.0] * 30,
            'Crypto': [1.0 + 0.1 * np.sin(i / 2) + 0.05 * np.random.randn() for i in range(30)]
        })
        
        fig = px.line(
            stable_data, 
            x='Data', 
            y=['Stablecoin', 'Crypto'],
            title="Estabilidade de Preço",
            labels={"value": "Valor Relativo", "variable": "Tipo de Token"},
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Market fit assessment
        st.markdown("### Adequação ao Mercado")
        
        st.markdown("""
        **Ideal para:**
        - Serviços de pagamento
        - Remessas internacionais
        - Preservação de valor em mercados voláteis
        - Aplicações DeFi
        - Comércio eletrônico
        """)

with models_tabs[4]:
    st.subheader("Non-Fungible Token (NFT)")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **Descrição:**
        NFTs são tokens únicos que representam a propriedade de um item digital ou físico específico, 
        criando escassez digital e provando autenticidade e propriedade.

        **Principais Características:**
        - Representam itens únicos ou de edição limitada
        - Não são intercambiáveis como tokens fungíveis
        - Provam autenticidade, propriedade e procedência
        - Podem incluir royalties para criadores em vendas secundárias

        **Exemplos de Uso:**
        - Arte digital
        - Colecionáveis
        - Propriedade virtual (terrenos, itens em jogos)
        - Ingressos para eventos
        - Certificados e credenciais
        - Direitos de propriedade intelectual
        """)
        
        st.markdown("**Exemplos de Projetos:**")
        st.markdown("- **CryptoPunks**: Coleção pioneira de avatares pixelados")
        st.markdown("- **NBA Top Shot**: Momentos memoráveis de jogos da NBA como colecionáveis")
        st.markdown("- **Decentraland**: Propriedades virtuais tokenizadas")
    
    with col2:
        # Simple diagram
        nft_data = pd.DataFrame([
            {"Categoria": "Arte Digital", "Valor": 40},
            {"Categoria": "Colecionáveis", "Valor": 25},
            {"Categoria": "Gaming", "Valor": 20},
            {"Categoria": "Metaverso", "Valor": 15}
        ])
        
        fig = px.bar(
            nft_data, 
            x="Categoria", 
            y="Valor", 
            title="Distribuição de Mercado NFT",
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Market fit assessment
        st.markdown("### Adequação ao Mercado")
        
        st.markdown("""
        **Ideal para:**
        - Artistas e criadores de conteúdo
        - Indústria de entretenimento
        - Jogos e metaverso
        - Gestão de propriedade intelectual
        - Autenticação de produtos físicos
        """)

with models_tabs[5]:
    st.subheader("Tokens Compostos/Híbridos")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **Descrição:**
        Tokens híbridos combinam características de múltiplos tipos de tokens, criando modelos mais flexíveis 
        e adaptados às necessidades específicas de um projeto.

        **Principais Características:**
        - Combinam elementos de diferentes modelos de token
        - Oferecem múltiplas funcionalidades e casos de uso
        - Geralmente mais complexos em design e implementação
        - Podem se adaptar a diferentes fases do projeto

        **Exemplos de Combinações:**
        - **Utility + Governance**: Acesso a serviços + direitos de voto
        - **Security + Utility**: Participação nos lucros + uso na plataforma
        - **Governance + Staking**: Direitos de voto + recompensas por staking
        """)
        
        st.markdown("**Exemplos de Projetos:**")
        st.markdown("- **BNB (Binance Coin)**: Utilidade no ecossistema Binance + governança na BNB Chain")
        st.markdown("- **LINK (Chainlink)**: Utilidade para pagamentos + participação no sistema como validador")
        st.markdown("- **CAKE (PancakeSwap)**: Utilidade no ecossistema + yield farming + governança")
    
    with col2:
        # Simple diagram
        hybrid_data = pd.DataFrame([
            {"Característica": "Utilidade", "Valor": 35},
            {"Característica": "Governança", "Valor": 25},
            {"Característica": "Staking", "Valor": 20},
            {"Característica": "Investimento", "Valor": 20}
        ])
        
        fig = px.pie(
            hybrid_data, 
            values='Valor', 
            names='Característica', 
            title="Composição Típica de Token Híbrido",
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Market fit assessment
        st.markdown("### Adequação ao Mercado")
        
        st.markdown("""
        **Ideal para:**
        - Ecossistemas complexos
        - Plataformas multi-facetadas
        - Projetos em crescimento
        - Aplicações inovadoras de blockchain
        """)

# Model Selection Tool
st.header("Seletor de Modelo de Tokenização")
st.markdown("""
    Use esta ferramenta para identificar o modelo de token mais adequado para seu projeto
    com base nas características do seu negócio e objetivos.
""")

# Questions for model selection
st.subheader("Responda às perguntas abaixo:")

col1, col2 = st.columns(2)

with col1:
    primary_purpose = st.selectbox(
        "1. Qual é o propósito principal do seu token?",
        [
            "Acesso a produtos/serviços na plataforma",
            "Representar participação/propriedade no projeto",
            "Permitir que usuários participem da governança",
            "Criar um meio de pagamento estável",
            "Representar ativos únicos/colecionáveis",
            "Múltiplos propósitos"
        ]
    )
    
    business_type = st.selectbox(
        "2. Qual é o tipo de negócio/plataforma?",
        [
            "Aplicação/Plataforma de software",
            "Marketplace ou exchange",
            "Organização descentralizada (DAO)",
            "Projeto de conteúdo/mídia",
            "Produto financeiro",
            "Jogo ou metaverso",
            "Infraestrutura blockchain"
        ]
    )
    
    revenue_model = st.selectbox(
        "3. Como o projeto pretende gerar valor?",
        [
            "Taxas de serviço/assinatura",
            "Valorização do token pelo uso crescente",
            "Comissões em transações",
            "Venda de ativos digitais/NFTs",
            "Modelo de advertising",
            "Participação nos lucros",
            "Combinação de fontes de receita"
        ]
    )

with col2:
    user_incentives = st.selectbox(
        "4. Como você planeja incentivar os usuários?",
        [
            "Descontos e benefícios no uso da plataforma",
            "Recompensas pelo uso/participação",
            "Direitos de voto em decisões",
            "Participação nas receitas/lucros",
            "Propriedade de ativos exclusivos",
            "Combinação de incentivos"
        ]
    )
    
    regulatory_concerns = st.selectbox(
        "5. Qual é sua posição em relação a regulações?",
        [
            "Evitar qualquer característica de security/investimento",
            "Compliance total com regulações de securities",
            "Foco em utilidade e governança",
            "Preocupação moderada com aspectos regulatórios",
            "Operação em área com regulação ainda indefinida"
        ]
    )
    
    timescale = st.selectbox(
        "6. Qual é o horizonte temporal para o seu projeto?",
        [
            "Curto prazo (1-2 anos)",
            "Médio prazo (3-5 anos)",
            "Longo prazo (5+ anos)",
            "Perpétuo (sem prazo definido)"
        ]
    )

# Calculate model recommendation
if st.button("Analisar e Recomendar Modelo", key="recommend", type="primary"):
    # Simple scoring system for demonstration
    scores = {
        "Utility Token": 0,
        "Security Token": 0,
        "Governance Token": 0,
        "Stablecoin": 0,
        "NFT": 0,
        "Híbrido": 0
    }
    
    # Score based on primary purpose
    if primary_purpose == "Acesso a produtos/serviços na plataforma":
        scores["Utility Token"] += 5
        scores["Híbrido"] += 2
    elif primary_purpose == "Representar participação/propriedade no projeto":
        scores["Security Token"] += 5
        scores["Híbrido"] += 2
    elif primary_purpose == "Permitir que usuários participem da governança":
        scores["Governance Token"] += 5
        scores["Híbrido"] += 2
    elif primary_purpose == "Criar um meio de pagamento estável":
        scores["Stablecoin"] += 5
    elif primary_purpose == "Representar ativos únicos/colecionáveis":
        scores["NFT"] += 5
    elif primary_purpose == "Múltiplos propósitos":
        scores["Híbrido"] += 5
        scores["Utility Token"] += 2
        scores["Governance Token"] += 2
    
    # Score based on business type
    if business_type == "Aplicação/Plataforma de software":
        scores["Utility Token"] += 3
        scores["Híbrido"] += 2
    elif business_type == "Marketplace ou exchange":
        scores["Utility Token"] += 3
        scores["Híbrido"] += 2
    elif business_type == "Organização descentralizada (DAO)":
        scores["Governance Token"] += 4
        scores["Híbrido"] += 3
    elif business_type == "Projeto de conteúdo/mídia":
        scores["Utility Token"] += 2
        scores["NFT"] += 3
    elif business_type == "Produto financeiro":
        scores["Security Token"] += 3
        scores["Stablecoin"] += 3
    elif business_type == "Jogo ou metaverso":
        scores["Utility Token"] += 2
        scores["NFT"] += 4
    elif business_type == "Infraestrutura blockchain":
        scores["Utility Token"] += 3
        scores["Governance Token"] += 3
        scores["Híbrido"] += 3
    
    # Score based on revenue model
    if revenue_model == "Taxas de serviço/assinatura":
        scores["Utility Token"] += 3
    elif revenue_model == "Valorização do token pelo uso crescente":
        scores["Utility Token"] += 3
        scores["Híbrido"] += 2
    elif revenue_model == "Comissões em transações":
        scores["Utility Token"] += 2
        scores["Stablecoin"] += 2
    elif revenue_model == "Venda de ativos digitais/NFTs":
        scores["NFT"] += 4
    elif revenue_model == "Modelo de advertising":
        scores["Utility Token"] += 2
    elif revenue_model == "Participação nos lucros":
        scores["Security Token"] += 4
    elif revenue_model == "Combinação de fontes de receita":
        scores["Híbrido"] += 3
    
    # Score based on user incentives
    if user_incentives == "Descontos e benefícios no uso da plataforma":
        scores["Utility Token"] += 3
    elif user_incentives == "Recompensas pelo uso/participação":
        scores["Utility Token"] += 3
        scores["Híbrido"] += 2
    elif user_incentives == "Direitos de voto em decisões":
        scores["Governance Token"] += 4
    elif user_incentives == "Participação nas receitas/lucros":
        scores["Security Token"] += 4
    elif user_incentives == "Propriedade de ativos exclusivos":
        scores["NFT"] += 4
    elif user_incentives == "Combinação de incentivos":
        scores["Híbrido"] += 4
    
    # Score based on regulatory concerns
    if regulatory_concerns == "Evitar qualquer característica de security/investimento":
        scores["Security Token"] -= 3
        scores["Utility Token"] += 2
        scores["Governance Token"] += 1
    elif regulatory_concerns == "Compliance total com regulações de securities":
        scores["Security Token"] += 3
    elif regulatory_concerns == "Foco em utilidade e governança":
        scores["Utility Token"] += 2
        scores["Governance Token"] += 2
    elif regulatory_concerns == "Preocupação moderada com aspectos regulatórios":
        scores["Híbrido"] += 1
    elif regulatory_concerns == "Operação em área com regulação ainda indefinida":
        scores["Híbrido"] += 1
    
    # Score based on timescale
    if timescale == "Curto prazo (1-2 anos)":
        scores["Utility Token"] += 1
        scores["NFT"] += 2
    elif timescale == "Médio prazo (3-5 anos)":
        scores["Híbrido"] += 2
    elif timescale == "Longo prazo (5+ anos)":
        scores["Governance Token"] += 2
        scores["Híbrido"] += 2
    elif timescale == "Perpétuo (sem prazo definido)":
        scores["Governance Token"] += 3
        scores["Híbrido"] += 2
    
    # Find top recommendations
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_recommendations = sorted_scores[:3]
    
    # Display recommendations
    st.subheader("Recomendações de Modelos de Token")
    
    # Create chart of scores
    chart_data = pd.DataFrame({
        'Modelo': list(scores.keys()),
        'Pontuação': list(scores.values())
    })
    
    fig = px.bar(
        chart_data,
        x='Modelo',
        y='Pontuação',
        title="Avaliação de Adequação dos Modelos",
        color='Pontuação',
        color_continuous_scale=px.colors.sequential.Blues
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display detailed recommendations
    for i, (model, score) in enumerate(top_recommendations):
        st.markdown(f"### {i+1}. {model} ({score} pontos)")
        
        if model == "Utility Token":
            st.markdown("""
            **Por que este modelo é adequado para você:**
            - Seu foco em fornecer acesso a produtos/serviços se alinha com o modelo de utility token
            - A estrutura de receita baseada em uso da plataforma é bem servida por um token de utilidade
            - Este modelo minimiza preocupações regulatórias em comparação com security tokens
            
            **Considerações para implementação:**
            - Defina claramente a utilidade do token dentro do seu ecossistema
            - Desenvolva mecanismos para capturar valor no token à medida que a plataforma cresce
            - Considere mecanismos de queima ou staking para gerenciar a oferta do token
            """)
            
        elif model == "Security Token":
            st.markdown("""
            **Por que este modelo é adequado para você:**
            - Seu objetivo de representar participação econômica se alinha com o modelo de security token
            - Sua disposição para compliance regulatório é compatível com este modelo
            - O foco em participação nos lucros é uma característica central dos security tokens
            
            **Considerações para implementação:**
            - Busque consultoria jurídica especializada para compliance regulatório
            - Defina claramente os direitos econômicos associados ao token
            - Considere trabalhar com plataformas especializadas em emissão de security tokens
            - Desenvolva um plano para listagem em exchanges regulamentadas
            """)
            
        elif model == "Governance Token":
            st.markdown("""
            **Por que este modelo é adequado para você:**
            - Seu interesse em envolver a comunidade na tomada de decisões se alinha com este modelo
            - A estrutura organizacional descentralizada é compatível com tokens de governança
            - A visão de longo prazo do projeto é bem servida por um modelo de governança descentralizada
            
            **Considerações para implementação:**
            - Defina claramente o escopo e mecanismos de governança (votação, propostas, quóruns)
            - Crie um sistema que equilibre a participação ampla com a tomada de decisões eficiente
            - Considere implementar delegação de votos para aumentar a participação efetiva
            - Introduza governança gradualmente, começando com decisões menos críticas
            """)
            
        elif model == "Stablecoin":
            st.markdown("""
            **Por que este modelo é adequado para você:**
            - Seu foco em criar um meio de pagamento estável se alinha perfeitamente com este modelo
            - A necessidade de reduzir volatilidade para transações no seu ecossistema
            - Os casos de uso financeiros do seu projeto se beneficiam de valores estáveis
            
            **Considerações para implementação:**
            - Determine o mecanismo de estabilização mais apropriado (colateralizado, algorítmico ou híbrido)
            - Desenvolva sistemas robustos de auditoria e transparência
            - Considere os requisitos regulatórios específicos para stablecoins
            - Estabeleça parcerias com instituições financeiras se necessário
            """)
            
        elif model == "NFT":
            st.markdown("""
            **Por que este modelo é adequado para você:**
            - Seu foco em ativos únicos e colecionáveis se alinha com o modelo NFT
            - O tipo de negócio baseado em conteúdo, jogos ou metaverso é ideal para NFTs
            - A capacidade de monetizar ativos digitais únicos
            
            **Considerações para implementação:**
            - Defina o valor único que seus NFTs oferecerão (estética, utilidade, raridade)
            - Desenvolva uma estratégia clara para lançamentos iniciais e mercado secundário
            - Considere implementar royalties para receita contínua em vendas secundárias
            - Crie experiências envolventes em torno dos seus NFTs para aumentar o valor
            """)
            
        elif model == "Híbrido":
            st.markdown("""
            **Por que este modelo é adequado para você:**
            - Seus múltiplos objetivos e casos de uso se beneficiam de um modelo flexível
            - A combinação de diferentes modelos de incentivo no seu projeto
            - A necessidade de adaptar o token para diferentes fases do projeto
            
            **Considerações para implementação:**
            - Identifique claramente quais características de cada modelo você quer incorporar
            - Defina a ponderação e importância relativa de cada componente
            - Desenvolva uma documentação detalhada para explicar o design do token híbrido
            - Considere como as diferentes funcionalidades do token interagem entre si
            - Avalie as implicações regulatórias das diversas características incorporadas
            """)
    
    # Store recommendation in session state
    if 'token_model_recommendation' not in st.session_state:
        st.session_state.token_model_recommendation = {}
    
    st.session_state.token_model_recommendation = {
        'top_model': top_recommendations[0][0],
        'all_recommendations': top_recommendations,
        'scores': scores
    }
    
    # Offer to proceed to simulation
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("Salvar Recomendação", key="save_recommendation"):
            st.success(f"Recomendação do modelo {top_recommendations[0][0]} salva com sucesso!")
    
    with col2:
        if st.button("Prosseguir para Simulação", key="goto_simulation"):
            st.switch_page("pages/simulation.py")