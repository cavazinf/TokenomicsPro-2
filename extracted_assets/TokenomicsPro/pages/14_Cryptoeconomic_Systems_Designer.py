import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time

# Set page configuration
st.set_page_config(
    page_title="Cryptoeconomic Systems Designer - TokenomicsLab",
    page_icon="🔄",
    layout="wide",
)

# Initialize language if not set
if 'language' not in st.session_state:
    st.session_state.language = 'English'

# Page title and description based on language
if st.session_state.language == 'English':
    title = "Cryptoeconomic Systems Designer"
    description = """
    Design comprehensive cryptoeconomic systems with incentive mechanisms, governance, and token utilities.
    """
    subtitle = "Create the foundation for a decentralized economy"
elif st.session_state.language == 'Português':
    title = "Designer de Sistemas Criptoeconômicos"
    description = """
    Projete sistemas criptoeconômicos completos com mecanismos de incentivo, governança e utilidades para tokens.
    """
    subtitle = "Crie a base para uma economia descentralizada"
elif st.session_state.language == 'Español':
    title = "Diseñador de Sistemas Criptoeconómicos"
    description = """
    Diseñe sistemas criptoeconómicos completos con mecanismos de incentivo, gobernanza y utilidades para tokens.
    """
    subtitle = "Crea la base para una economía descentralizada"
else:
    title = "Cryptoeconomic Systems Designer"
    description = """
    Design comprehensive cryptoeconomic systems with incentive mechanisms, governance, and token utilities.
    """
    subtitle = "Create the foundation for a decentralized economy"

st.title(title)
st.markdown(description)
st.markdown(f"**{subtitle}**")

# Initialize session state for cryptoeconomic system designer
if 'crypto_system' not in st.session_state:
    st.session_state.crypto_system = {
        'name': '',
        'description': '',
        'components': {
            'token': {
                'enabled': False,
                'functions': [],
                'details': ''
            },
            'blockchain': {
                'enabled': False,
                'features': [],
                'details': ''
            },
            'incentives': {
                'enabled': False,
                'mechanisms': [],
                'details': ''
            },
            'governance': {
                'enabled': False,
                'mechanisms': [],
                'details': ''
            }
        },
        'applications': [],
        'advantages': [],
        'challenges': []
    }

# Define multilingual labels
if st.session_state.language == 'English':
    # System info labels
    system_info_title = "System Information"
    system_name_label = "System Name"
    system_desc_label = "System Description"
    
    # Component labels
    components_title = "Essential Components"
    token_title = "Token"
    blockchain_title = "Blockchain"
    incentives_title = "Incentive Mechanisms"
    governance_title = "Governance"
    
    # Token function options
    token_functions = [
        "Medium of Exchange",
        "Store of Value",
        "Unit of Account",
        "Access Rights",
        "Staking Mechanism",
        "Governance Rights",
        "Work Token",
        "Utility Token"
    ]
    
    # Blockchain feature options
    blockchain_features = [
        "Security",
        "Transparency",
        "Immutability",
        "Transaction recording",
        "Smart Contracts",
        "Consensus Mechanism",
        "Decentralized Storage",
        "Interoperability"
    ]
    
    # Incentive mechanism options
    incentive_mechanisms = [
        "Staking Rewards",
        "Yield Farming",
        "Transaction Fees",
        "Liquidity Mining",
        "Airdrops",
        "Referral Rewards",
        "Work Verification",
        "Reputation Systems"
    ]
    
    # Governance mechanism options
    governance_mechanisms = [
        "Token Voting",
        "Quadratic Voting",
        "Delegated Voting",
        "Committee Governance",
        "Futarchy",
        "On-chain Governance",
        "Off-chain Governance",
        "Hybrid Governance"
    ]
    
    # Applications, advantages and challenges labels
    applications_title = "Applications and Examples"
    advantages_title = "Advantages of Cryptoeconomic Systems"
    challenges_title = "Challenges and Considerations"
    
    # Application options
    application_options = [
        "Decentralized Finance (DeFi)",
        "NFT Marketplaces",
        "Gaming and Metaverse",
        "Decentralized Autonomous Organizations (DAOs)",
        "Supply Chain Tracking",
        "Content Creation and Distribution",
        "Identity Management",
        "Decentralized Social Networks"
    ]
    
    # Advantage options
    advantage_options = [
        "Decentralization - Removes intermediaries and promotes autonomy",
        "Transparency - All data and transactions are public and auditable",
        "Efficiency - Reduces costs by removing middlemen",
        "Incentives - Creates effective mechanisms for participation",
        "Innovation - Opens opportunities for new business models"
    ]
    
    # Challenge options
    challenge_options = [
        "Volatility - Crypto markets are volatile and can affect token stability",
        "Security - Tokens and platforms must be secured against attacks",
        "Regulation - Lack of clear regulations makes adoption difficult",
        "Complexity - Systems can be difficult to design and implement",
        "Scalability - Technical limitations for mass adoption"
    ]
    
    # Action buttons
    generate_button = "Generate Cryptoeconomic System"
    save_button = "Save System Design"
    
    # Visualization labels
    visualization_title = "System Visualization"
    
elif st.session_state.language == 'Português':
    # System info labels
    system_info_title = "Informações do Sistema"
    system_name_label = "Nome do Sistema"
    system_desc_label = "Descrição do Sistema"
    
    # Component labels
    components_title = "Componentes Essenciais"
    token_title = "Token"
    blockchain_title = "Blockchain"
    incentives_title = "Mecanismos de Incentivo"
    governance_title = "Governança"
    
    # Token function options
    token_functions = [
        "Meio de Troca",
        "Reserva de Valor",
        "Unidade de Conta",
        "Direitos de Acesso",
        "Mecanismo de Staking",
        "Direitos de Governança",
        "Token de Trabalho",
        "Token de Utilidade"
    ]
    
    # Blockchain feature options
    blockchain_features = [
        "Segurança",
        "Transparência",
        "Imutabilidade",
        "Registro de transações",
        "Contratos Inteligentes",
        "Mecanismo de Consenso",
        "Armazenamento Descentralizado",
        "Interoperabilidade"
    ]
    
    # Incentive mechanism options
    incentive_mechanisms = [
        "Recompensas de Staking",
        "Yield Farming",
        "Taxas de Transação",
        "Mineração de Liquidez",
        "Airdrops",
        "Recompensas por Indicação",
        "Verificação de Trabalho",
        "Sistemas de Reputação"
    ]
    
    # Governance mechanism options
    governance_mechanisms = [
        "Votação por Token",
        "Votação Quadrática",
        "Votação Delegada",
        "Governança por Comitê",
        "Futarquia",
        "Governança On-chain",
        "Governança Off-chain",
        "Governança Híbrida"
    ]
    
    # Applications, advantages and challenges labels
    applications_title = "Aplicações e Exemplos"
    advantages_title = "Vantagens dos Sistemas Criptoeconômicos"
    challenges_title = "Desafios e Considerações"
    
    # Application options
    application_options = [
        "Finanças Descentralizadas (DeFi)",
        "Marketplaces de NFTs",
        "Jogos e Metaverso",
        "Organizações Autônomas Descentralizadas (DAOs)",
        "Rastreamento de Cadeia de Suprimentos",
        "Criação e Distribuição de Conteúdo",
        "Gerenciamento de Identidade",
        "Redes Sociais Descentralizadas"
    ]
    
    # Advantage options
    advantage_options = [
        "Descentralização - Elimina intermediários e promove autonomia",
        "Transparência - Todos os dados e transações são públicos e auditáveis",
        "Eficiência - Reduz custos ao remover intermediários",
        "Incentivos - Cria mecanismos eficazes para participação",
        "Inovação - Abre portas para novos modelos de negócios"
    ]
    
    # Challenge options
    challenge_options = [
        "Volatilidade - Mercados de criptomoedas são voláteis e podem afetar a estabilidade dos tokens",
        "Segurança - Tokens e plataformas precisam ser protegidos contra ataques",
        "Regulamentação - Falta de regulamentação clara dificulta a adoção",
        "Complexidade - Sistemas podem ser difíceis de projetar e implementar",
        "Escalabilidade - Limitações técnicas para adoção em massa"
    ]
    
    # Action buttons
    generate_button = "Gerar Sistema Criptoeconômico"
    save_button = "Salvar Design do Sistema"
    
    # Visualization labels
    visualization_title = "Visualização do Sistema"
    
elif st.session_state.language == 'Español':
    # System info labels
    system_info_title = "Información del Sistema"
    system_name_label = "Nombre del Sistema"
    system_desc_label = "Descripción del Sistema"
    
    # Component labels
    components_title = "Componentes Esenciales"
    token_title = "Token"
    blockchain_title = "Blockchain"
    incentives_title = "Mecanismos de Incentivo"
    governance_title = "Gobernanza"
    
    # Token function options
    token_functions = [
        "Medio de Intercambio",
        "Reserva de Valor",
        "Unidad de Cuenta",
        "Derechos de Acceso",
        "Mecanismo de Staking",
        "Derechos de Gobernanza",
        "Token de Trabajo",
        "Token de Utilidad"
    ]
    
    # Blockchain feature options
    blockchain_features = [
        "Seguridad",
        "Transparencia",
        "Inmutabilidad",
        "Registro de transacciones",
        "Contratos Inteligentes",
        "Mecanismo de Consenso",
        "Almacenamiento Descentralizado",
        "Interoperabilidad"
    ]
    
    # Incentive mechanism options
    incentive_mechanisms = [
        "Recompensas de Staking",
        "Yield Farming",
        "Comisiones de Transacción",
        "Minería de Liquidez",
        "Airdrops",
        "Recompensas por Referidos",
        "Verificación de Trabajo",
        "Sistemas de Reputación"
    ]
    
    # Governance mechanism options
    governance_mechanisms = [
        "Votación por Token",
        "Votación Cuadrática",
        "Votación Delegada",
        "Gobernanza por Comité",
        "Futarquía",
        "Gobernanza On-chain",
        "Gobernanza Off-chain",
        "Gobernanza Híbrida"
    ]
    
    # Applications, advantages and challenges labels
    applications_title = "Aplicaciones y Ejemplos"
    advantages_title = "Ventajas de los Sistemas Criptoeconómicos"
    challenges_title = "Desafíos y Consideraciones"
    
    # Application options
    application_options = [
        "Finanzas Descentralizadas (DeFi)",
        "Mercados de NFTs",
        "Juegos y Metaverso",
        "Organizaciones Autónomas Descentralizadas (DAOs)",
        "Seguimiento de Cadena de Suministro",
        "Creación y Distribución de Contenido",
        "Gestión de Identidad",
        "Redes Sociales Descentralizadas"
    ]
    
    # Advantage options
    advantage_options = [
        "Descentralización - Elimina intermediarios y promueve autonomía",
        "Transparencia - Todos los datos y transacciones son públicos y auditables",
        "Eficiencia - Reduce costos al eliminar intermediarios",
        "Incentivos - Crea mecanismos eficaces para la participación",
        "Innovación - Abre puertas para nuevos modelos de negocio"
    ]
    
    # Challenge options
    challenge_options = [
        "Volatilidad - Los mercados de criptomonedas son volátiles y pueden afectar la estabilidad de los tokens",
        "Seguridad - Los tokens y plataformas deben protegerse contra ataques",
        "Regulación - La falta de regulación clara dificulta la adopción",
        "Complejidad - Los sistemas pueden ser difíciles de diseñar e implementar",
        "Escalabilidad - Limitaciones técnicas para la adopción masiva"
    ]
    
    # Action buttons
    generate_button = "Generar Sistema Criptoeconómico"
    save_button = "Guardar Diseño del Sistema"
    
    # Visualization labels
    visualization_title = "Visualización del Sistema"
    
else:
    # System info labels
    system_info_title = "System Information"
    system_name_label = "System Name"
    system_desc_label = "System Description"
    
    # Component labels
    components_title = "Essential Components"
    token_title = "Token"
    blockchain_title = "Blockchain"
    incentives_title = "Incentive Mechanisms"
    governance_title = "Governance"
    
    # Token function options
    token_functions = [
        "Medium of Exchange",
        "Store of Value",
        "Unit of Account",
        "Access Rights",
        "Staking Mechanism",
        "Governance Rights",
        "Work Token",
        "Utility Token"
    ]
    
    # Blockchain feature options
    blockchain_features = [
        "Security",
        "Transparency",
        "Immutability",
        "Transaction recording",
        "Smart Contracts",
        "Consensus Mechanism",
        "Decentralized Storage",
        "Interoperability"
    ]
    
    # Incentive mechanism options
    incentive_mechanisms = [
        "Staking Rewards",
        "Yield Farming",
        "Transaction Fees",
        "Liquidity Mining",
        "Airdrops",
        "Referral Rewards",
        "Work Verification",
        "Reputation Systems"
    ]
    
    # Governance mechanism options
    governance_mechanisms = [
        "Token Voting",
        "Quadratic Voting",
        "Delegated Voting",
        "Committee Governance",
        "Futarchy",
        "On-chain Governance",
        "Off-chain Governance",
        "Hybrid Governance"
    ]
    
    # Applications, advantages and challenges labels
    applications_title = "Applications and Examples"
    advantages_title = "Advantages of Cryptoeconomic Systems"
    challenges_title = "Challenges and Considerations"
    
    # Application options
    application_options = [
        "Decentralized Finance (DeFi)",
        "NFT Marketplaces",
        "Gaming and Metaverse",
        "Decentralized Autonomous Organizations (DAOs)",
        "Supply Chain Tracking",
        "Content Creation and Distribution",
        "Identity Management",
        "Decentralized Social Networks"
    ]
    
    # Advantage options
    advantage_options = [
        "Decentralization - Removes intermediaries and promotes autonomy",
        "Transparency - All data and transactions are public and auditable",
        "Efficiency - Reduces costs by removing middlemen",
        "Incentives - Creates effective mechanisms for participation",
        "Innovation - Opens opportunities for new business models"
    ]
    
    # Challenge options
    challenge_options = [
        "Volatility - Crypto markets are volatile and can affect token stability",
        "Security - Tokens and platforms must be secured against attacks",
        "Regulation - Lack of clear regulations makes adoption difficult",
        "Complexity - Systems can be difficult to design and implement",
        "Scalability - Technical limitations for mass adoption"
    ]
    
    # Action buttons
    generate_button = "Generate Cryptoeconomic System"
    save_button = "Save System Design"
    
    # Visualization labels
    visualization_title = "System Visualization"
    

# Create a two-column layout
col1, col2 = st.columns([3, 2])

with col1:
    # System information form
    st.subheader(system_info_title)
    system_name = st.text_input(
        system_name_label,
        value=st.session_state.crypto_system['name'],
        help="Name your cryptoeconomic system"
    )
    if system_name != st.session_state.crypto_system['name']:
        st.session_state.crypto_system['name'] = system_name
    
    system_desc = st.text_area(
        system_desc_label,
        value=st.session_state.crypto_system['description'],
        help="Provide a detailed description of your system"
    )
    if system_desc != st.session_state.crypto_system['description']:
        st.session_state.crypto_system['description'] = system_desc
    
    # Essential components
    st.subheader(components_title)
    
    # Token component
    with st.expander(f"{token_title}", expanded=True):
        token_enabled = st.checkbox(
            f"Enable {token_title}",
            value=st.session_state.crypto_system['components']['token']['enabled'],
            key="token_enabled"
        )
        if token_enabled != st.session_state.crypto_system['components']['token']['enabled']:
            st.session_state.crypto_system['components']['token']['enabled'] = token_enabled
        
        if token_enabled:
            selected_functions = st.multiselect(
                "Token Functions",
                options=token_functions,
                default=st.session_state.crypto_system['components']['token']['functions'],
                help="Select the functions your token will serve in the system"
            )
            if selected_functions != st.session_state.crypto_system['components']['token']['functions']:
                st.session_state.crypto_system['components']['token']['functions'] = selected_functions
            
            token_details = st.text_area(
                "Token Details",
                value=st.session_state.crypto_system['components']['token']['details'],
                help="Provide more details about your token design"
            )
            if token_details != st.session_state.crypto_system['components']['token']['details']:
                st.session_state.crypto_system['components']['token']['details'] = token_details
    
    # Blockchain component
    with st.expander(f"{blockchain_title}", expanded=True):
        blockchain_enabled = st.checkbox(
            f"Enable {blockchain_title}",
            value=st.session_state.crypto_system['components']['blockchain']['enabled'],
            key="blockchain_enabled"
        )
        if blockchain_enabled != st.session_state.crypto_system['components']['blockchain']['enabled']:
            st.session_state.crypto_system['components']['blockchain']['enabled'] = blockchain_enabled
        
        if blockchain_enabled:
            selected_features = st.multiselect(
                "Blockchain Features",
                options=blockchain_features,
                default=st.session_state.crypto_system['components']['blockchain']['features'],
                help="Select the features your blockchain will provide in the system"
            )
            if selected_features != st.session_state.crypto_system['components']['blockchain']['features']:
                st.session_state.crypto_system['components']['blockchain']['features'] = selected_features
            
            blockchain_details = st.text_area(
                "Blockchain Details",
                value=st.session_state.crypto_system['components']['blockchain']['details'],
                help="Provide more details about your blockchain design"
            )
            if blockchain_details != st.session_state.crypto_system['components']['blockchain']['details']:
                st.session_state.crypto_system['components']['blockchain']['details'] = blockchain_details
    
    # Incentive mechanisms component
    with st.expander(f"{incentives_title}", expanded=True):
        incentives_enabled = st.checkbox(
            f"Enable {incentives_title}",
            value=st.session_state.crypto_system['components']['incentives']['enabled'],
            key="incentives_enabled"
        )
        if incentives_enabled != st.session_state.crypto_system['components']['incentives']['enabled']:
            st.session_state.crypto_system['components']['incentives']['enabled'] = incentives_enabled
        
        if incentives_enabled:
            selected_mechanisms = st.multiselect(
                "Incentive Mechanisms",
                options=incentive_mechanisms,
                default=st.session_state.crypto_system['components']['incentives']['mechanisms'],
                help="Select the incentive mechanisms your system will implement"
            )
            if selected_mechanisms != st.session_state.crypto_system['components']['incentives']['mechanisms']:
                st.session_state.crypto_system['components']['incentives']['mechanisms'] = selected_mechanisms
            
            incentives_details = st.text_area(
                "Incentive Details",
                value=st.session_state.crypto_system['components']['incentives']['details'],
                help="Provide more details about your incentive mechanisms"
            )
            if incentives_details != st.session_state.crypto_system['components']['incentives']['details']:
                st.session_state.crypto_system['components']['incentives']['details'] = incentives_details
    
    # Governance component
    with st.expander(f"{governance_title}", expanded=True):
        governance_enabled = st.checkbox(
            f"Enable {governance_title}",
            value=st.session_state.crypto_system['components']['governance']['enabled'],
            key="governance_enabled"
        )
        if governance_enabled != st.session_state.crypto_system['components']['governance']['enabled']:
            st.session_state.crypto_system['components']['governance']['enabled'] = governance_enabled
        
        if governance_enabled:
            selected_gov_mechanisms = st.multiselect(
                "Governance Mechanisms",
                options=governance_mechanisms,
                default=st.session_state.crypto_system['components']['governance']['mechanisms'],
                help="Select the governance mechanisms your system will implement"
            )
            if selected_gov_mechanisms != st.session_state.crypto_system['components']['governance']['mechanisms']:
                st.session_state.crypto_system['components']['governance']['mechanisms'] = selected_gov_mechanisms
            
            governance_details = st.text_area(
                "Governance Details",
                value=st.session_state.crypto_system['components']['governance']['details'],
                help="Provide more details about your governance mechanisms"
            )
            if governance_details != st.session_state.crypto_system['components']['governance']['details']:
                st.session_state.crypto_system['components']['governance']['details'] = governance_details
    
    # Applications
    st.subheader(applications_title)
    selected_applications = st.multiselect(
        "Choose Applications",
        options=application_options,
        default=st.session_state.crypto_system['applications'],
        help="Select the applications where your cryptoeconomic system could be implemented"
    )
    if selected_applications != st.session_state.crypto_system['applications']:
        st.session_state.crypto_system['applications'] = selected_applications
    
    # Advantages
    st.subheader(advantages_title)
    selected_advantages = st.multiselect(
        "Select Advantages",
        options=advantage_options,
        default=st.session_state.crypto_system['advantages'],
        help="Select the advantages your cryptoeconomic system offers"
    )
    if selected_advantages != st.session_state.crypto_system['advantages']:
        st.session_state.crypto_system['advantages'] = selected_advantages
    
    # Challenges
    st.subheader(challenges_title)
    selected_challenges = st.multiselect(
        "Identify Challenges",
        options=challenge_options,
        default=st.session_state.crypto_system['challenges'],
        help="Identify the challenges your cryptoeconomic system might face"
    )
    if selected_challenges != st.session_state.crypto_system['challenges']:
        st.session_state.crypto_system['challenges'] = selected_challenges

with col2:
    st.subheader(visualization_title)
    
    # Check if we have enough data to generate a visualization
    if (st.session_state.crypto_system['name'] and
        (st.session_state.crypto_system['components']['token']['enabled'] or
         st.session_state.crypto_system['components']['blockchain']['enabled'] or
         st.session_state.crypto_system['components']['incentives']['enabled'] or
         st.session_state.crypto_system['components']['governance']['enabled'])):
        
        # Generate data for visualizations
        
        # Component radar chart
        components_list = ["Token", "Blockchain", "Incentives", "Governance"]
        component_values = [
            len(st.session_state.crypto_system['components']['token']['functions']) if st.session_state.crypto_system['components']['token']['enabled'] else 0,
            len(st.session_state.crypto_system['components']['blockchain']['features']) if st.session_state.crypto_system['components']['blockchain']['enabled'] else 0,
            len(st.session_state.crypto_system['components']['incentives']['mechanisms']) if st.session_state.crypto_system['components']['incentives']['enabled'] else 0,
            len(st.session_state.crypto_system['components']['governance']['mechanisms']) if st.session_state.crypto_system['components']['governance']['enabled'] else 0
        ]
        
        # Normalize the values for better visualization
        max_val = max(max(component_values), 1)  # Avoid division by zero
        normalized_values = [val / max_val * 10 for val in component_values]
        
        # Create radar chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=normalized_values,
            theta=components_list,
            fill='toself',
            name=st.session_state.crypto_system['name']
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )
            ),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # System summary
        st.subheader("System Summary")
        
        st.info(f"**{st.session_state.crypto_system['name']}**\n\n{st.session_state.crypto_system['description']}")
        
        # Components summary
        if st.session_state.crypto_system['components']['token']['enabled']:
            st.success(f"**Token**: {', '.join(st.session_state.crypto_system['components']['token']['functions'])}")
        
        if st.session_state.crypto_system['components']['blockchain']['enabled']:
            st.success(f"**Blockchain**: {', '.join(st.session_state.crypto_system['components']['blockchain']['features'])}")
        
        if st.session_state.crypto_system['components']['incentives']['enabled']:
            st.success(f"**Incentives**: {', '.join(st.session_state.crypto_system['components']['incentives']['mechanisms'])}")
        
        if st.session_state.crypto_system['components']['governance']['enabled']:
            st.success(f"**Governance**: {', '.join(st.session_state.crypto_system['components']['governance']['mechanisms'])}")
        
        # Applications summary
        if st.session_state.crypto_system['applications']:
            st.subheader("Applications")
            for app in st.session_state.crypto_system['applications']:
                st.markdown(f"• {app}")
        
        # Challenges and advantages summary
        if st.session_state.crypto_system['advantages'] or st.session_state.crypto_system['challenges']:
            col1_inner, col2_inner = st.columns(2)
            
            with col1_inner:
                if st.session_state.crypto_system['advantages']:
                    st.subheader("Advantages")
                    for adv in st.session_state.crypto_system['advantages']:
                        st.markdown(f"✓ {adv.split(' - ')[0]}")
            
            with col2_inner:
                if st.session_state.crypto_system['challenges']:
                    st.subheader("Challenges")
                    for challenge in st.session_state.crypto_system['challenges']:
                        st.markdown(f"⚠ {challenge.split(' - ')[0]}")
        
        # Export options
        st.download_button(
            label="Export System Design (JSON)",
            data=str(st.session_state.crypto_system),
            file_name=f"{st.session_state.crypto_system['name'].replace(' ', '_')}_crypto_system.json",
            mime="application/json"
        )
    else:
        st.info("Fill in the system information and enable at least one component to see the visualization.")

# Educational content
with st.expander("What are Cryptoeconomic Systems?"):
    st.markdown("""
    ### Cryptoeconomic Systems

    Cryptoeconomic systems combine elements of traditional economics with the principles of cryptography and blockchain technology, creating transparent, autonomous, and decentralized systems.

    Key characteristics:
    
    1. **Token-Based Incentives**: Systems that use token-based mechanisms to incentivize certain behaviors, creating economic alignment between participants.
    
    2. **Decentralized Infrastructure**: Utilize blockchain or distributed ledger technology to enable trustless interactions.
    
    3. **Programmable Economics**: Smart contracts automatically enforce rules and distribute incentives, removing the need for trusted intermediaries.
    
    4. **Governance Mechanisms**: Decision-making protocols that allow token holders to vote on system changes and improvements.
    
    5. **Network Effects**: Value increases as more users participate in the system.
    
    Examples include:
    
    - **Bitcoin**: A peer-to-peer electronic cash system with a fixed supply and mining incentives
    - **Ethereum**: A platform for decentralized applications with a native currency and gas fee structure
    - **Compound**: A lending protocol where governance token holders can vote on protocol parameters
    - **Uniswap**: An automated market maker where liquidity providers earn fees
    
    Cryptoeconomic systems are increasingly being applied beyond cryptocurrencies to areas like supply chain, digital identity, and content creation.
    """)

# Footer
st.markdown("---")
st.markdown("TokenomicsLab - Cryptoeconomic Systems Designer")