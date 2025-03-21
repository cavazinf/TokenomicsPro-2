import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import uuid
from datetime import datetime, timedelta
import hashlib

st.set_page_config(
    page_title="Tokenomics Lab",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Função para verificar o login
def check_password():
    # Sistema de usuários (simples para demonstração)
    # Em um sistema real, isso seria armazenado em banco de dados com senhas hash
    users = {
        "ADMIN": hashlib.sha256("123".encode()).hexdigest(),
        "user1": hashlib.sha256("password1".encode()).hexdigest(),
        "user2": hashlib.sha256("password2".encode()).hexdigest()
    }
    
    # Inicializa o estado da sessão de autenticação
    if 'authentication_status' not in st.session_state:
        st.session_state.authentication_status = False
    if 'username' not in st.session_state:
        st.session_state.username = ""
    
    # Se já está autenticado, retorna True
    if st.session_state.authentication_status:
        return True
    
    # Caso contrário, mostra o formulário de login
    st.title("Login - Tokenomics Lab")
    
    with st.form("login_form"):
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        submit_button = st.form_submit_button("Login")
        
        st.info("Para demonstração, você pode usar o usuário ADMIN com senha 123")
        
        if submit_button:
            if username in users:
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                if hashed_password == users[username]:
                    st.session_state.authentication_status = True
                    st.session_state.username = username
                    return True
                else:
                    st.error("Senha incorreta!")
            else:
                st.error("Usuário não encontrado!")
    
    return False

# Inicializar estados da sessão para controle de usuário e créditos
if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())
if 'credits' not in st.session_state:
    st.session_state.credits = 0
if 'subscription' not in st.session_state:
    st.session_state.subscription = None
if 'subscription_expiry' not in st.session_state:
    st.session_state.subscription_expiry = None
if 'project_type' not in st.session_state:
    st.session_state.project_type = None
if 'onboarding_complete' not in st.session_state:
    st.session_state.onboarding_complete = False
if 'features_used' not in st.session_state:
    st.session_state.features_used = {}

# Definição de planos de assinatura
subscription_plans = {
    "Gratuito": {
        "price": 0,
        "credits": 5,
        "features": ["Dashboard básico", "Simulação básica", "1 modelo salvo"],
        "description": "Perfeito para explorar a plataforma"
    },
    "Startup": {
        "price": 29.90,
        "credits": 50,
        "features": ["Dashboard completo", "Simulação avançada", "5 modelos salvos", "Relatórios básicos", "Exportação PDF"],
        "description": "Ideal para startups em estágio inicial"
    },
    "Business": {
        "price": 99.90,
        "credits": 200,
        "features": ["Tudo no plano Startup", "Relatórios avançados", "Modelos ilimitados", "Simulações econômicas", "Análise de mercado", "Suporte prioritário"],
        "description": "Para empresas estabelecidas com necessidades avançadas"
    },
    "Enterprise": {
        "price": 299.90,
        "credits": 500,
        "features": ["Tudo no plano Business", "APIs customizadas", "Whitelabel", "Suporte dedicado", "Consultoria mensal"],
        "description": "Solução completa para grandes empresas e instituições"
    }
}

# Função para comprar créditos adicionais
def buy_credits(amount):
    price = {
        10: 9.90,
        50: 39.90,
        100: 69.90,
        500: 299.90
    }
    if amount in price:
        # Simulando uma compra bem-sucedida
        st.session_state.credits += amount
        st.success(f"Compra bem-sucedida! Adicionados {amount} créditos à sua conta.")
        
        # Registro de atividade (na implementação real, isso seria salvo em um banco de dados)
        st.session_state.last_purchase = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "amount": amount,
            "price": price[amount]
        }
    return

# Função para assinar um plano
def subscribe_plan(plan_name):
    if plan_name in subscription_plans:
        plan = subscription_plans[plan_name]
        # Simulando uma assinatura bem-sucedida
        st.session_state.subscription = plan_name
        st.session_state.credits += plan["credits"]
        st.session_state.subscription_expiry = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        st.success(f"Assinatura do plano {plan_name} realizada com sucesso! Adicionados {plan['credits']} créditos à sua conta.")
    return

# Função para gastar créditos
def spend_credits(feature_name, cost=1):
    if st.session_state.credits >= cost:
        st.session_state.credits -= cost
        
        # Registro de uso de recursos
        if feature_name in st.session_state.features_used:
            st.session_state.features_used[feature_name] += 1
        else:
            st.session_state.features_used[feature_name] = 1
            
        return True
    else:
        st.warning(f"Créditos insuficientes para usar {feature_name}. Por favor, adquira mais créditos ou assine um plano.")
        return False

# Primeiro, verificar o login
if not check_password():
    st.stop()  # Parar a execução se não estiver autenticado

# Se o usuário for ADMIN, garantir créditos extras para demonstração
if st.session_state.username == "ADMIN" and st.session_state.credits < 100:
    st.session_state.credits = 500
    st.session_state.subscription = "Enterprise"
    st.session_state.subscription_expiry = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    
# Formulário de Onboarding - Se o usuário ainda não completou o onboarding
if not st.session_state.onboarding_complete:
    st.title("Bem-vindo ao Tokenomics Lab")
    st.markdown("""
        ### Plataforma de Simulação e Desenvolvimento de Tokenomics para Projetos Blockchain
        
        Antes de começarmos, gostaríamos de entender um pouco mais sobre o seu projeto
        para personalizar a experiência de acordo com suas necessidades.
    """)
    
    with st.form("onboarding_form"):
        st.subheader("Sobre o seu Projeto")
        
        project_name = st.text_input("Nome do Projeto", placeholder="Ex: MeuToken Finance")
        
        project_type = st.radio(
            "Tipo de Projeto:",
            ["Startup", "DAO (Organização Autônoma Descentralizada)", "Outro"],
            help="O tipo de projeto determinará modelos e recomendações específicas"
        )
        
        if project_type == "Startup":
            startup_stage = st.selectbox(
                "Estágio da Startup:",
                ["Ideação", "MVP", "Seed", "Series A ou posterior"]
            )
            
            business_model = st.multiselect(
                "Modelo de Negócio (selecione todos que se aplicam):",
                ["DeFi (Finanças Descentralizadas)", "GameFi", "SocialFi", "NFT Marketplace", 
                 "Protocolo de Infraestrutura", "DAO Tools", "Metaverso", "Outro"]
            )
            
            funding_status = st.radio(
                "Status de Financiamento:",
                ["Bootstrapped", "Anjo/Pré-seed", "Seed", "Série A ou posterior"]
            )
            
        elif project_type == "DAO (Organização Autônoma Descentralizada)":
            dao_purpose = st.selectbox(
                "Propósito Principal da DAO:",
                ["Protocolo", "Investimento", "Social", "Filantropia", "Serviço", "Colecionável", "Outro"]
            )
            
            governance_model = st.radio(
                "Modelo de Governança Preferido:",
                ["Baseado em Tokens", "Quadrático", "Reputação", "Multisig", "Híbrido", "Ainda não decidido"]
            )
            
            members_expectation = st.slider("Número Esperado de Membros:", min_value=10, max_value=100000, value=1000, step=100)
        
        token_exists = st.radio(
            "Você já possui um token?",
            ["Sim", "Não, mas pretendo criar", "Não tenho certeza se preciso de um token"]
        )
        
        if token_exists == "Sim":
            token_type = st.multiselect(
                "Tipo(s) de Token:",
                ["Utility", "Governance", "Security", "Social", "NFT", "Stablecoin", "Outro"]
            )
            
            blockchain = st.selectbox(
                "Blockchain Principal:",
                ["Ethereum", "Polygon", "Solana", "Binance Smart Chain", "Avalanche", "Near", "Outro"]
            )
        
        goals = st.multiselect(
            "Principais Objetivos com o Tokenomics (selecione todos que se aplicam):",
            ["Captação de recursos", "Governança descentralizada", "Alinhar incentivos da comunidade", 
             "Distribuição de valor", "Crescimento de usuários", "Modelo econômico sustentável", "Outro"]
        )
        
        custom_goal = st.text_input("Se selecionou 'Outro' em alguma questão acima, favor especificar:", "")
        
        # Campo para seleção de plano
        st.subheader("Escolha seu Plano")
        
        selected_plan = st.selectbox(
            "Selecione um plano para começar:",
            list(subscription_plans.keys()),
            format_func=lambda x: f"{x} - R${subscription_plans[x]['price']:.2f}/mês"
        )
        
        st.markdown(f"**Plano {selected_plan}**: {subscription_plans[selected_plan]['description']}")
        
        st.markdown("**Recursos incluídos:**")
        for feature in subscription_plans[selected_plan]["features"]:
            st.markdown(f"- {feature}")
        
        st.markdown(f"**Créditos incluídos:** {subscription_plans[selected_plan]['credits']} créditos")
        
        agree_terms = st.checkbox("Concordo com os Termos de Serviço e Política de Privacidade")
        
        submitted = st.form_submit_button("Começar a usar o Tokenomics Lab")
        
        if submitted:
            if not agree_terms:
                st.error("Você precisa concordar com os Termos de Serviço e Política de Privacidade para continuar.")
            else:
                # Salvar as informações na sessão
                st.session_state.project_type = project_type
                
                if project_type == "Startup":
                    st.session_state.project_details = {
                        "name": project_name,
                        "type": project_type,
                        "stage": startup_stage,
                        "business_model": business_model,
                        "funding_status": funding_status,
                        "has_token": token_exists,
                        "goals": goals
                    }
                    
                    if token_exists == "Sim":
                        st.session_state.project_details["token_type"] = token_type
                        st.session_state.project_details["blockchain"] = blockchain
                        
                elif project_type == "DAO (Organização Autônoma Descentralizada)":
                    st.session_state.project_details = {
                        "name": project_name,
                        "type": project_type,
                        "purpose": dao_purpose,
                        "governance": governance_model,
                        "members": members_expectation,
                        "has_token": token_exists,
                        "goals": goals
                    }
                    
                    if token_exists == "Sim":
                        st.session_state.project_details["token_type"] = token_type
                        st.session_state.project_details["blockchain"] = blockchain
                
                # Ativar o plano selecionado
                subscribe_plan(selected_plan)
                
                # Marcar onboarding como concluído
                st.session_state.onboarding_complete = True
                
                st.success("Configuração concluída com sucesso! Redirecionando para o dashboard...")
                st.experimental_rerun()

# Interface principal (após o onboarding)
else:
    # Main app layout
    st.title("Tokenomics Lab")
    st.markdown(f"""
        ### Plataforma de Simulação e Desenvolvimento de Tokenomics para {st.session_state.project_type}s
        
        Utilize esta plataforma para modelar, simular e analisar diferentes modelos de tokenomics
        para seu projeto.
    """)
    
    # Informações do plano atual na barra lateral
    st.sidebar.title("Sua Conta")
    st.sidebar.markdown(f"**Plano:** {st.session_state.subscription or 'Gratuito'}")
    st.sidebar.markdown(f"**Créditos disponíveis:** {st.session_state.credits}")
    
    if st.session_state.subscription_expiry:
        st.sidebar.markdown(f"**Validade:** {st.session_state.subscription_expiry}")
    
    # Opção para comprar créditos
    with st.sidebar.expander("Adquirir mais créditos"):
        credit_options = {
            10: "R$9,90",
            50: "R$39,90",
            100: "R$69,90",
            500: "R$299,90"
        }
        
        credit_amount = st.selectbox(
            "Quantidade de créditos:",
            list(credit_options.keys()),
            format_func=lambda x: f"{x} créditos - {credit_options[x]}"
        )
        
        if st.button("Comprar créditos"):
            buy_credits(credit_amount)
    
    # Opção para mudar de plano
    with st.sidebar.expander("Mudar de Plano"):
        new_plan = st.selectbox(
            "Selecione um novo plano:",
            list(subscription_plans.keys()),
            format_func=lambda x: f"{x} - R${subscription_plans[x]['price']:.2f}/mês"
        )
        
        st.markdown(f"**Plano {new_plan}**: {subscription_plans[new_plan]['description']}")
        
        if st.button("Assinar Plano"):
            subscribe_plan(new_plan)
    
    # Navegação principal
    st.sidebar.title("Navegação")
    page = st.sidebar.radio(
        "Escolha uma seção:",
        ["Início", "Dashboard", "Simulação", "Simulação de Mercado", "Benchmark de Tokenomics", "Biblioteca de Modelos", "Relatórios"]
    )

# Page content
if st.session_state.get('page'):
    page = st.session_state.page
else:
    page = "Início"
    
if page == "Início":
    st.header("Bem-vindo ao Tokenomics Lab")
    
    st.subheader("Funcionalidades Principais")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Dashboard")
        st.markdown("Visualize métricas importantes sobre seu modelo de tokenomics.")
        if st.button("Ir para Dashboard", key="dash_btn"):
            st.switch_page("pages/dashboard.py")
            
        st.markdown("### 📈 Simulação de Mercado")
        st.markdown("Simule o comportamento do token no mercado com eventos aleatórios.")
        if st.button("Ir para Simulação de Mercado", key="market_sim_btn"):
            st.switch_page("pages/market_simulation.py")
            
        st.markdown("### 🔍 Benchmark de Tokenomics")
        st.markdown("Compare diferentes estratégias de tokenomics lado a lado.")
        if st.button("Ir para Benchmark", key="benchmark_btn"):
            st.switch_page("pages/tokenomics_benchmark.py")
    
    with col2:
        st.markdown("### 🧪 Simulação")
        st.markdown("Simule diferentes cenários de distribuição e comportamento de tokens.")
        if st.button("Ir para Simulação", key="sim_btn"):
            st.switch_page("pages/simulation.py")
    
        st.markdown("### 📚 Biblioteca de Modelos")
        st.markdown("Explore modelos pré-configurados de tokenomics para diferentes casos de uso.")
        if st.button("Ir para Biblioteca", key="lib_btn"):
            st.switch_page("pages/models_library.py")
    
    st.markdown("---")
    
    st.subheader("O que é Tokenomics?")
    st.markdown("""
    Tokenomics refere-se à economia de tokens em projetos blockchain e criptomoedas. 
    Engloba vários aspectos, incluindo:
    
    - **Distribuição de tokens**: Como os tokens são alocados entre diferentes stakeholders
    - **Mecanismos de oferta**: Taxa de emissão, limites máximos, queima de tokens
    - **Utilidade do token**: Funções e casos de uso dentro do ecossistema
    - **Incentivos**: Como o design econômico incentiva comportamentos desejados
    - **Governança**: Como os detentores de tokens participam na tomada de decisões
    
    Um design de tokenomics bem pensado é crucial para a sustentabilidade e sucesso de 
    projetos baseados em blockchain.
    """)
    
    # Sample visualization for the home page
    st.subheader("Exemplo de Visualização de Tokenomics")
    
    # Create sample data for token distribution
    categories = ["Equipe", "Investidores", "Comunidade", "Fundação", "Incentivos", "Reserva"]
    percentages = [20, 25, 30, 10, 10, 5]
    
    # Create pie chart
    fig = px.pie(
        values=percentages,
        names=categories,
        title="Exemplo de Distribuição de Tokens",
        color_discrete_sequence=px.colors.sequential.Blues_r,
        hole=0.4,
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)
    
    st.caption("Este é apenas um exemplo ilustrativo. Use a plataforma para criar modelos personalizados.")

elif page == "Dashboard":
    st.switch_page("pages/dashboard.py")
elif page == "Simulação":
    st.switch_page("pages/simulation.py")
elif page == "Biblioteca de Modelos":
    st.switch_page("pages/models_library.py")
elif page == "Relatórios":
    st.switch_page("pages/reports.py")
elif page == "Simulação de Mercado":
    st.switch_page("pages/market_simulation.py")
elif page == "Benchmark de Tokenomics":
    st.switch_page("pages/tokenomics_benchmark.py")
