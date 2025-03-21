import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from datetime import datetime

# Import local modules
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.tokenomics import TokenomicsModel, UtilityTokenModel, GovernanceTokenModel, create_model_from_dict

st.set_page_config(
    page_title="Biblioteca de Modelos | Tokenomics Lab",
    page_icon="📚",
    layout="wide"
)

# Sidebar
st.sidebar.title("Tokenomics Lab")
st.sidebar.image("https://cdn.jsdelivr.net/npm/cryptocurrency-icons@0.18.1/svg/icon/btc.svg", width=50)

# Main content
st.title("Biblioteca de Modelos de Tokenomics")
st.markdown("""
    Explore modelos pré-configurados de tokenomics ou carregue modelos salvos anteriormente.
    Utilize estes modelos como ponto de partida para o desenvolvimento do seu próprio tokenomics.
""")

# Tabs for template models and saved models
tab1, tab2 = st.tabs(["Modelos Pré-configurados", "Modelos Salvos"])

with tab1:
    st.header("Modelos Pré-configurados")
    
    # Define template models
    template_models = {
        "DeFi Token": {
            "description": "Um token com foco em finanças descentralizadas (DeFi), incluindo distribuição equilibrada entre comunidade, staking e reservas de liquidez.",
            "type": "governance",
            "icon": "https://cdn.jsdelivr.net/npm/cryptocurrency-icons@0.18.1/svg/icon/eth.svg",
            "model": {
                "name": "Modelo DeFi Token",
                "total_supply": 100_000_000,
                "model_type": "governance",
                "initial_staking_rate": 0.3,
                "staking_apy": 0.15,
                "distribution": {
                    "Equipe": 15.0,
                    "Investidores": 20.0,
                    "Comunidade": 30.0,
                    "Staking e Recompensas": 20.0,
                    "Reserva de Liquidez": 10.0,
                    "Ecossistema": 5.0
                },
                "vesting_schedules": {
                    "Equipe": [
                        [0, 0],
                        [6, 10],
                        [12, 15],
                        [18, 25],
                        [24, 25],
                        [30, 25]
                    ],
                    "Investidores": [
                        [0, 10],
                        [3, 15],
                        [6, 15],
                        [9, 15],
                        [12, 15],
                        [15, 15],
                        [18, 15]
                    ],
                    "Comunidade": [
                        [0, 20],
                        [3, 20],
                        [6, 20],
                        [9, 20],
                        [12, 20]
                    ]
                }
            }
        },
        "GameFi Token": {
            "description": "Um token para jogos blockchain (GameFi) com foco em recompensas para jogadores, incentivos para desenvolvedores e marketing.",
            "type": "utility",
            "icon": "https://cdn.jsdelivr.net/npm/cryptocurrency-icons@0.18.1/svg/icon/mana.svg",
            "model": {
                "name": "Modelo GameFi Token",
                "total_supply": 500_000_000,
                "model_type": "utility",
                "initial_users": 50000,
                "user_growth_rate": 0.08,
                "distribution": {
                    "Equipe": 12.0,
                    "Investidores": 18.0,
                    "Jogadores": 35.0,
                    "Recompensas no Jogo": 20.0,
                    "Marketing": 8.0,
                    "Desenvolvedores": 7.0
                },
                "vesting_schedules": {
                    "Equipe": [
                        [0, 0],
                        [6, 10],
                        [12, 15],
                        [18, 25],
                        [24, 25],
                        [30, 25]
                    ],
                    "Investidores": [
                        [0, 5],
                        [3, 10],
                        [6, 15],
                        [9, 15],
                        [12, 15],
                        [15, 20],
                        [18, 20]
                    ],
                    "Jogadores": [
                        [0, 15],
                        [3, 15],
                        [6, 15],
                        [9, 15],
                        [12, 15],
                        [15, 15],
                        [18, 10]
                    ]
                }
            }
        },
        "DAO Token": {
            "description": "Um token de governança para uma Organização Autônoma Descentralizada (DAO), com ênfase em participação comunitária e decisões coletivas.",
            "type": "governance",
            "icon": "https://cdn.jsdelivr.net/npm/cryptocurrency-icons@0.18.1/svg/icon/comp.svg",
            "model": {
                "name": "Modelo DAO Token",
                "total_supply": 200_000_000,
                "model_type": "governance",
                "initial_staking_rate": 0.4,
                "staking_apy": 0.10,
                "distribution": {
                    "Core Contributors": 10.0,
                    "Investidores": 15.0,
                    "Comunidade": 40.0,
                    "Governança": 25.0,
                    "Ecossistema": 10.0
                },
                "vesting_schedules": {
                    "Core Contributors": [
                        [0, 0],
                        [6, 10],
                        [12, 15],
                        [18, 25],
                        [24, 25],
                        [30, 25]
                    ],
                    "Investidores": [
                        [0, 0],
                        [3, 10],
                        [6, 15],
                        [9, 15],
                        [12, 15],
                        [15, 20],
                        [18, 25]
                    ],
                    "Comunidade": [
                        [0, 10],
                        [3, 15],
                        [6, 15],
                        [9, 15],
                        [12, 15],
                        [15, 15],
                        [18, 15]
                    ]
                }
            }
        },
        "SocialFi Token": {
            "description": "Um token para plataformas sociais descentralizadas (SocialFi), com incentivos para criadores de conteúdo e engajamento do usuário.",
            "type": "utility",
            "icon": "https://cdn.jsdelivr.net/npm/cryptocurrency-icons@0.18.1/svg/icon/steem.svg",
            "model": {
                "name": "Modelo SocialFi Token",
                "total_supply": 1_000_000_000,
                "model_type": "utility",
                "initial_users": 100000,
                "user_growth_rate": 0.10,
                "distribution": {
                    "Equipe": 10.0,
                    "Investidores": 15.0,
                    "Criadores de Conteúdo": 25.0,
                    "Recompensas de Engajamento": 20.0,
                    "Marketing e Crescimento": 15.0,
                    "Reserva": 15.0
                },
                "vesting_schedules": {
                    "Equipe": [
                        [0, 0],
                        [6, 10],
                        [12, 15],
                        [18, 25],
                        [24, 25],
                        [30, 25]
                    ],
                    "Investidores": [
                        [0, 0],
                        [3, 10],
                        [6, 15],
                        [9, 15],
                        [12, 15],
                        [15, 20],
                        [18, 25]
                    ],
                    "Criadores de Conteúdo": [
                        [0, 10],
                        [3, 15],
                        [6, 15],
                        [9, 15],
                        [12, 15],
                        [15, 15],
                        [18, 15]
                    ]
                }
            }
        }
    }
    
    # Display template models in grid
    col1, col2 = st.columns(2)
    
    for i, (name, data) in enumerate(template_models.items()):
        # Alternate between columns
        with col1 if i % 2 == 0 else col2:
            st.markdown(f"""
            <div style="border: 1px solid #ddd; border-radius: 5px; padding: 15px; margin-bottom: 20px;">
                <h3><img src="{data['icon']}" style="height: 30px; margin-right: 10px;"> {name}</h3>
                <p>{data['description']}</p>
                <p><strong>Tipo:</strong> {data['type'].title()}</p>
                <p><strong>Oferta Total:</strong> {data['model']['total_supply']:,} tokens</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Usar este modelo", key=f"use_{name}"):
                model_dict = data["model"]
                
                if model_dict["model_type"] == "utility":
                    model = UtilityTokenModel.from_dict(model_dict)
                elif model_dict["model_type"] == "governance":
                    model = GovernanceTokenModel.from_dict(model_dict)
                else:
                    model = TokenomicsModel.from_dict(model_dict)
                
                # Store model in session state
                st.session_state.model = model
                
                # Prepare data for simulation page
                st.session_state.category_inputs = [
                    {"name": cat, "percentage": pct}
                    for cat, pct in model.distribution.items()
                ]
                
                st.session_state.vesting_inputs = {
                    cat: [{"month": month, "percentage": pct} for month, pct in schedule]
                    for cat, schedule in model.vesting_schedules.items()
                }
                
                # Message and redirect
                st.success(f"Modelo {name} carregado com sucesso! Redirecionando para a página de simulação...")
                st.switch_page("pages/simulation.py")

with tab2:
    st.header("Modelos Salvos")
    
    # Check for saved models directory
    if not os.path.exists("saved_models"):
        os.makedirs("saved_models")
    
    # Find saved model files
    saved_files = [f for f in os.listdir("saved_models") if f.endswith(".json")]
    
    if not saved_files:
        st.info("Nenhum modelo salvo encontrado. Crie e salve modelos na página de Simulação.")
    else:
        # Display saved models
        for file in saved_files:
            file_path = os.path.join("saved_models", file)
            
            try:
                with open(file_path, "r") as f:
                    model_data = json.load(f)
                
                # Get basic info
                model_name = model_data.get("name", "Modelo sem nome")
                model_type = model_data.get("model_type", "base").title()
                total_supply = model_data.get("total_supply", 0)
                distribution = model_data.get("distribution", {})
                
                # Create expandable card for each model
                with st.expander(f"{model_name} ({model_type})"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**Tipo de Modelo:** {model_type}")
                        st.markdown(f"**Oferta Total:** {total_supply:,} tokens")
                        
                        # Show distribution
                        st.markdown("**Distribuição:**")
                        for cat, pct in distribution.items():
                            st.markdown(f"- {cat}: {pct}%")
                    
                    with col2:
                        # Distribution pie chart
                        fig = px.pie(
                            values=list(distribution.values()),
                            names=list(distribution.keys()),
                            title="Distribuição",
                            height=200
                        )
                        fig.update_layout(margin=dict(l=0, r=0, t=30, b=0))
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Actions
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button("Carregar este Modelo", key=f"load_{file}"):
                            # Create model from data
                            model = create_model_from_dict(model_data)
                            
                            # Store in session state
                            st.session_state.model = model
                            
                            # Prepare data for simulation page
                            st.session_state.category_inputs = [
                                {"name": cat, "percentage": pct}
                                for cat, pct in model.distribution.items()
                            ]
                            
                            st.session_state.vesting_inputs = {
                                cat: [{"month": month, "percentage": pct} for month, pct in schedule]
                                for cat, schedule in model.vesting_schedules.items()
                            }
                            
                            # Message and redirect
                            st.success(f"Modelo {model_name} carregado com sucesso! Redirecionando para a página de simulação...")
                            st.switch_page("pages/simulation.py")
                    
                    with col2:
                        if st.button("Simular", key=f"simulate_{file}"):
                            # Create model from data
                            model = create_model_from_dict(model_data)
                            
                            # Store in session state
                            st.session_state.model = model
                            
                            # Run simulation
                            simulation_months = 36
                            initial_price = 0.1
                            
                            if model_data.get("model_type") == "utility":
                                simulation_result = model.simulate_token_price(
                                    simulation_months, 
                                    initial_price,
                                    tokens_per_user=10.0,
                                    volatility=0.1
                                )
                            elif model_data.get("model_type") == "governance":
                                simulation_result = model.simulate_token_price(
                                    simulation_months, 
                                    initial_price,
                                    staking_growth=0.01,
                                    volatility=0.1
                                )
                            else:
                                simulation_result = model.simulate_token_price(
                                    simulation_months, 
                                    initial_price,
                                    volatility=0.1
                                )
                            
                            st.session_state.simulation_result = simulation_result
                            
                            # Message and redirect
                            st.success(f"Modelo {model_name} simulado com sucesso! Redirecionando para o dashboard...")
                            st.switch_page("pages/dashboard.py")
                    
                    with col3:
                        if st.button("Excluir", key=f"delete_{file}"):
                            os.remove(file_path)
                            st.warning(f"Modelo {model_name} excluído.")
                            st.rerun()
            
            except Exception as e:
                st.error(f"Erro ao carregar o modelo {file}: {str(e)}")

# Templates section
st.header("Crie um Novo Modelo")

# Button to go to simulation page
if st.button("Criar Novo Modelo", type="primary"):
    # Go to simulation page
    st.switch_page("pages/simulation.py")

# Educational content about tokenomics models
with st.expander("Saiba mais sobre Modelos de Tokenomics"):
    st.markdown("""
    ## Tipos de Modelos de Tokenomics
    
    ### Utility Tokens
    Os tokens de utilidade (utility tokens) têm valor derivado de sua utilidade dentro de um ecossistema específico.
    Características:
    - Usados para acessar produtos/serviços da plataforma
    - Valor geralmente relacionado ao crescimento da rede
    - Exemplos: Filecoin (FIL), Basic Attention Token (BAT)
    
    ### Governance Tokens
    Os tokens de governança dão a seus detentores direito de voto nas decisões do protocolo.
    Características:
    - Permitem participação em decisões de governança
    - Frequentemente possuem mecanismos de staking
    - Exemplos: Uniswap (UNI), Compound (COMP)
    
    ### Security Tokens
    Os tokens de segurança representam propriedade de um ativo subjacente e são regulamentados como valores mobiliários.
    Características:
    - Representam propriedade de um ativo
    - Frequentemente pagam dividendos
    - Sujeitos a regulamentações de valores mobiliários
    
    ### Stablecoins
    Tokens projetados para manter um valor estável, geralmente atrelado a uma moeda fiduciária.
    Características:
    - Valor atrelado a um ativo de referência (USD, ouro, etc.)
    - Usados para reduzir volatilidade no ecossistema cripto
    - Exemplos: USDC, DAI, USDT
    
    ## Parâmetros Importantes em Tokenomics
    
    - **Oferta Total**: Número máximo de tokens que existirão
    - **Distribuição Inicial**: Como os tokens são alocados entre diferentes grupos
    - **Cronograma de Vesting**: Quando os tokens são liberados ao longo do tempo
    - **Inflação/Deflação**: Mudanças na oferta de tokens ao longo do tempo
    - **Utilidade**: O que os tokens permitem que os usuários façam
    - **Incentivos**: Como o design incentiva comportamentos desejados
    
    ## Boas Práticas
    
    - Alinhe incentivos entre todos os stakeholders
    - Evite concentração excessiva de tokens
    - Projete vesting de longo prazo para equipe e investidores
    - Balanceie mecanismos inflacionários e deflacionários
    - Garanta utilidade real para o token dentro do ecossistema
    - Considere modelos sustentáveis de longo prazo
    """)
