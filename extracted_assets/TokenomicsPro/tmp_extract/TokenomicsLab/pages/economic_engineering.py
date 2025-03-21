import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import json
import os

# Import local modules
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.tokenomics import TokenomicsModel

st.set_page_config(
    page_title="Engenharia Econômica | Tokenomics Lab",
    page_icon="⚙️",
    layout="wide"
)

# Sidebar
st.sidebar.title("Tokenomics Lab")
st.sidebar.image("https://cdn.jsdelivr.net/npm/cryptocurrency-icons@0.18.1/svg/icon/btc.svg", width=50)

# Main content
st.title("Engenharia Econômica")
st.markdown("""
    Projete mecanismos econômicos avançados para o seu token, incluindo dinâmicas de oferta e demanda, 
    incentivos, sistemas de governança e controle de inflação/deflação.
""")

# Check if model exists in session state
if 'model' not in st.session_state:
    st.warning("Você ainda não criou um modelo de tokenomics. Vá para a página de Simulação para criar um modelo primeiro.")
    
    # Button to go to simulation page
    if st.button("Ir para Simulação"):
        st.switch_page("pages/simulation.py")
        
    st.stop()

# Initialize economic engineering data in session state if not exists
if 'economic_engineering' not in st.session_state:
    st.session_state.economic_engineering = {
        "supply_mechanisms": {
            "max_supply": 0,
            "has_cap": True,
            "burn_mechanism": False,
            "burn_rate": 0.0,
            "burn_conditions": "",
            "inflation_rate": 0.0,
            "emission_schedule": [
                {"year": 1, "emission": 100.0},
                {"year": 2, "emission": 80.0},
                {"year": 3, "emission": 50.0},
                {"year": 4, "emission": 20.0},
                {"year": 5, "emission": 5.0}
            ]
        },
        "incentive_mechanisms": [],
        "governance_mechanisms": {
            "voting_power": "token-based",
            "proposal_threshold": 1.0,
            "voting_period": 7,
            "quorum": 30.0,
            "supermajority": 66.7,
            "delegation": True,
            "timelock": 2
        },
        "monetary_policy": {
            "policy_type": "fixed",
            "target_inflation": 3.0,
            "adjustment_frequency": "quarterly",
            "min_inflation": 0.0,
            "max_inflation": 10.0,
            "policy_parameters": []
        },
        "economic_metrics": {
            "velocity": 4.0,
            "liquidity_ratio": 0.2,
            "holder_distribution": [70, 20, 10]
        }
    }

# Economic Engineering Configuration
st.header("Configuração de Engenharia Econômica")

# Get model parameters
model = st.session_state.model
total_supply = model.total_supply if hasattr(model, 'total_supply') else 100000000

# Supply Mechanisms
st.subheader("Mecanismos de Oferta")
st.markdown("Configure os mecanismos que controlam a oferta do seu token ao longo do tempo.")

col1, col2 = st.columns(2)

with col1:
    has_cap = st.checkbox(
        "Token tem oferta máxima limitada?",
        value=st.session_state.economic_engineering["supply_mechanisms"]["has_cap"],
        help="Se marcado, o token terá uma oferta máxima definida. Se desmarcado, poderá ser inflacionário sem limite."
    )
    
    max_supply = st.number_input(
        "Oferta Máxima de Tokens",
        min_value=0,
        value=st.session_state.economic_engineering["supply_mechanisms"]["max_supply"] or total_supply,
        step=1000000,
        help="Número máximo de tokens que podem existir (se aplicável)."
    )
    
    if not has_cap:
        inflation_rate = st.slider(
            "Taxa de Inflação Anual (%)",
            min_value=0.0,
            max_value=50.0,
            value=st.session_state.economic_engineering["supply_mechanisms"]["inflation_rate"],
            step=0.1,
            help="Taxa de inflação anual para tokens sem limite de oferta."
        )
    else:
        inflation_rate = 0.0

with col2:
    burn_mechanism = st.checkbox(
        "Implementar mecanismo de queima de tokens?",
        value=st.session_state.economic_engineering["supply_mechanisms"]["burn_mechanism"],
        help="Se marcado, o token terá um mecanismo para remover tokens de circulação permanentemente."
    )
    
    if burn_mechanism:
        burn_rate = st.slider(
            "Taxa de Queima (%)",
            min_value=0.0,
            max_value=100.0,
            value=st.session_state.economic_engineering["supply_mechanisms"]["burn_rate"],
            step=0.1,
            help="Porcentagem de tokens que serão queimados conforme as condições estabelecidas."
        )
        
        burn_conditions = st.text_area(
            "Condições para Queima",
            value=st.session_state.economic_engineering["supply_mechanisms"]["burn_conditions"],
            height=100,
            help="Descreva as condições que acionam a queima de tokens (ex: porcentagem de taxas de transação, compra e queima programática, etc)."
        )
    else:
        burn_rate = 0.0
        burn_conditions = ""

# Emission Schedule
st.subheader("Cronograma de Emissão")
st.markdown("Configure o cronograma de emissão de tokens ao longo do tempo.")

# Display existing emission schedule
emission_schedule = st.session_state.economic_engineering["supply_mechanisms"]["emission_schedule"]

# Create a dataframe for editing
emission_df = pd.DataFrame(emission_schedule)

# Add default years if needed
for year in range(1, 6):
    if year not in emission_df["year"].values:
        emission_df = emission_df.append({"year": year, "emission": 0.0}, ignore_index=True)

# Sort by year
emission_df = emission_df.sort_values("year").reset_index(drop=True)

# Display as editable dataframe using columns
cols = st.columns(6)
new_emission_schedule = []

for i in range(5):  # Years 1-5
    with cols[i]:
        st.markdown(f"**Ano {i+1}**")
        emission_value = st.number_input(
            f"Emissão (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(emission_df[emission_df["year"] == i+1]["emission"].values[0]) if i < len(emission_df) and i+1 in emission_df["year"].values else 0.0,
            step=1.0,
            key=f"emission_{i+1}"
        )
        new_emission_schedule.append({"year": i+1, "emission": emission_value})

# Incentive Mechanisms
st.subheader("Mecanismos de Incentivo")
st.markdown("Configure mecanismos para incentivar comportamentos desejados no ecossistema.")

# Dynamic form for incentive mechanisms
if st.button("Adicionar Mecanismo de Incentivo"):
    st.session_state.economic_engineering["incentive_mechanisms"].append({
        "name": "",
        "description": "",
        "type": "Staking",
        "reward_rate": 5.0,
        "duration": 30,
        "constraints": ""
    })

# Display existing incentive mechanisms
incentives_to_remove = []

for i, incentive in enumerate(st.session_state.economic_engineering["incentive_mechanisms"]):
    with st.expander(f"Incentivo {i+1}: {incentive['name'] or 'Novo Incentivo'}"):
        col1, col2 = st.columns(2)
        
        with col1:
            incentive["name"] = st.text_input(
                "Nome do Mecanismo", 
                value=incentive["name"],
                key=f"inc_name_{i}"
            )
            
            incentive["description"] = st.text_area(
                "Descrição", 
                value=incentive["description"],
                height=100,
                key=f"inc_desc_{i}"
            )
            
            incentive["type"] = st.selectbox(
                "Tipo de Incentivo", 
                ["Staking", "Liquidity Mining", "Governance Rewards", "Usage Rewards", "Referral", "Outro"],
                index=["Staking", "Liquidity Mining", "Governance Rewards", "Usage Rewards", "Referral", "Outro"].index(incentive["type"]) if incentive["type"] in ["Staking", "Liquidity Mining", "Governance Rewards", "Usage Rewards", "Referral", "Outro"] else 0,
                key=f"inc_type_{i}"
            )
        
        with col2:
            incentive["reward_rate"] = st.slider(
                "Taxa de Recompensa Anual (%)", 
                min_value=0.0, 
                max_value=100.0, 
                value=incentive["reward_rate"],
                step=0.5,
                key=f"inc_rate_{i}"
            )
            
            incentive["duration"] = st.number_input(
                "Duração (dias)", 
                min_value=1, 
                value=incentive["duration"],
                step=1,
                key=f"inc_duration_{i}"
            )
            
            incentive["constraints"] = st.text_area(
                "Restrições e Condições", 
                value=incentive["constraints"],
                height=100,
                key=f"inc_constraints_{i}"
            )
        
        if st.button("Remover Incentivo", key=f"remove_inc_{i}"):
            incentives_to_remove.append(i)

# Remove incentives marked for removal
if incentives_to_remove:
    st.session_state.economic_engineering["incentive_mechanisms"] = [inc for i, inc in enumerate(st.session_state.economic_engineering["incentive_mechanisms"]) 
                                             if i not in incentives_to_remove]

# Governance Mechanisms
st.subheader("Mecanismos de Governança")
st.markdown("Configure como os detentores de tokens podem participar da governança do projeto.")

col1, col2 = st.columns(2)

with col1:
    voting_power = st.selectbox(
        "Modelo de Poder de Voto",
        ["Baseado em tokens", "Quadrático", "Holográfico", "Delegação Líquida", "Multisig"],
        index=["Baseado em tokens", "Quadrático", "Holográfico", "Delegação Líquida", "Multisig"].index(
            "Baseado em tokens" if st.session_state.economic_engineering["governance_mechanisms"]["voting_power"] == "token-based" else
            "Quadrático" if st.session_state.economic_engineering["governance_mechanisms"]["voting_power"] == "quadratic" else
            "Holográfico" if st.session_state.economic_engineering["governance_mechanisms"]["voting_power"] == "holographic" else
            "Delegação Líquida" if st.session_state.economic_engineering["governance_mechanisms"]["voting_power"] == "delegated" else
            "Multisig"
        ),
        help="Método para calcular o poder de voto dos participantes."
    )
    
    # Convert selection to internal representation
    voting_power_map = {
        "Baseado em tokens": "token-based",
        "Quadrático": "quadratic",
        "Holográfico": "holographic",
        "Delegação Líquida": "delegated",
        "Multisig": "multisig"
    }
    voting_power_internal = voting_power_map[voting_power]
    
    proposal_threshold = st.slider(
        "Limite para Propostas (%)",
        min_value=0.01,
        max_value=10.0,
        value=st.session_state.economic_engineering["governance_mechanisms"]["proposal_threshold"],
        step=0.01,
        help="Porcentagem da oferta total que um usuário precisa possuir para fazer uma proposta."
    )
    
    voting_period = st.slider(
        "Período de Votação (dias)",
        min_value=1,
        max_value=30,
        value=st.session_state.economic_engineering["governance_mechanisms"]["voting_period"],
        step=1,
        help="Duração das votações em dias."
    )

with col2:
    quorum = st.slider(
        "Quórum (%)",
        min_value=1.0,
        max_value=100.0,
        value=st.session_state.economic_engineering["governance_mechanisms"]["quorum"],
        step=0.5,
        help="Porcentagem mínima de participação para uma votação ser válida."
    )
    
    supermajority = st.slider(
        "Supermaioria (%)",
        min_value=50.0,
        max_value=100.0,
        value=st.session_state.economic_engineering["governance_mechanisms"]["supermajority"],
        step=0.1,
        help="Porcentagem de votos 'sim' necessária para aprovar uma proposta."
    )
    
    delegation = st.checkbox(
        "Permitir Delegação de Votos",
        value=st.session_state.economic_engineering["governance_mechanisms"]["delegation"],
        help="Se marcado, os usuários podem delegar seu poder de voto para outros usuários."
    )
    
    timelock = st.number_input(
        "Período de Timelock (dias)",
        min_value=0,
        max_value=30,
        value=st.session_state.economic_engineering["governance_mechanisms"]["timelock"],
        step=1,
        help="Período de espera entre a aprovação e a execução de uma proposta."
    )

# Monetary Policy
st.subheader("Política Monetária")
st.markdown("Configure mecanismos para ajustar a oferta e incentivar estabilidade de preço.")

col1, col2 = st.columns(2)

with col1:
    policy_type = st.selectbox(
        "Tipo de Política Monetária",
        ["Fixa", "Algorítmica", "Híbrida", "Gerenciada por DAO"],
        index=["Fixa", "Algorítmica", "Híbrida", "Gerenciada por DAO"].index(
            "Fixa" if st.session_state.economic_engineering["monetary_policy"]["policy_type"] == "fixed" else
            "Algorítmica" if st.session_state.economic_engineering["monetary_policy"]["policy_type"] == "algorithmic" else
            "Híbrida" if st.session_state.economic_engineering["monetary_policy"]["policy_type"] == "hybrid" else
            "Gerenciada por DAO"
        ),
        help="Método para ajustar parâmetros monetários do token."
    )
    
    # Convert selection to internal representation
    policy_type_map = {
        "Fixa": "fixed",
        "Algorítmica": "algorithmic",
        "Híbrida": "hybrid",
        "Gerenciada por DAO": "dao"
    }
    policy_type_internal = policy_type_map[policy_type]
    
    if policy_type != "Fixa":
        target_inflation = st.slider(
            "Inflação Alvo (%)",
            min_value=-10.0,
            max_value=20.0,
            value=st.session_state.economic_engineering["monetary_policy"]["target_inflation"],
            step=0.1,
            help="Taxa de inflação alvo para a política monetária."
        )
    else:
        target_inflation = 0.0

with col2:
    if policy_type != "Fixa":
        adjustment_frequency = st.selectbox(
            "Frequência de Ajuste",
            ["Diária", "Semanal", "Mensal", "Trimestral", "Anual"],
            index=["Diária", "Semanal", "Mensal", "Trimestral", "Anual"].index(
                "Diária" if st.session_state.economic_engineering["monetary_policy"]["adjustment_frequency"] == "daily" else
                "Semanal" if st.session_state.economic_engineering["monetary_policy"]["adjustment_frequency"] == "weekly" else
                "Mensal" if st.session_state.economic_engineering["monetary_policy"]["adjustment_frequency"] == "monthly" else
                "Trimestral" if st.session_state.economic_engineering["monetary_policy"]["adjustment_frequency"] == "quarterly" else
                "Anual"
            ),
            help="Com que frequência a política monetária é ajustada."
        )
        
        # Convert selection to internal representation
        freq_map = {
            "Diária": "daily",
            "Semanal": "weekly",
            "Mensal": "monthly",
            "Trimestral": "quarterly",
            "Anual": "yearly"
        }
        adjustment_frequency_internal = freq_map[adjustment_frequency]
        
        min_inflation = st.number_input(
            "Inflação Mínima (%)",
            min_value=-50.0,
            max_value=0.0,
            value=st.session_state.economic_engineering["monetary_policy"]["min_inflation"],
            step=0.1,
            help="Limite inferior para a taxa de inflação (pode ser negativo para deflação)."
        )
        
        max_inflation = st.number_input(
            "Inflação Máxima (%)",
            min_value=0.0,
            max_value=100.0,
            value=st.session_state.economic_engineering["monetary_policy"]["max_inflation"],
            step=0.1,
            help="Limite superior para a taxa de inflação."
        )
    else:
        adjustment_frequency_internal = "none"
        min_inflation = 0.0
        max_inflation = 0.0

# Monetary Policy Parameters
if policy_type != "Fixa":
    st.subheader("Parâmetros da Política Monetária")
    st.markdown("Adicione parâmetros específicos para a política monetária algorítmica.")
    
    # Dynamic form for policy parameters
    if st.button("Adicionar Parâmetro de Política"):
        st.session_state.economic_engineering["monetary_policy"]["policy_parameters"].append({
            "name": "",
            "description": "",
            "target": 0.0,
            "weight": 1.0
        })
    
    # Display existing policy parameters
    params_to_remove = []
    
    for i, param in enumerate(st.session_state.economic_engineering["monetary_policy"]["policy_parameters"]):
        col1, col2, col3, col4 = st.columns([3, 3, 2, 1])
        
        with col1:
            param["name"] = st.text_input(
                f"Nome do Parâmetro {i+1}", 
                value=param["name"],
                key=f"param_name_{i}"
            )
        
        with col2:
            param["description"] = st.text_input(
                f"Descrição {i+1}", 
                value=param["description"],
                key=f"param_desc_{i}"
            )
        
        with col3:
            param["target"] = st.number_input(
                f"Valor Alvo {i+1}", 
                value=param["target"],
                step=0.1,
                key=f"param_target_{i}"
            )
            
            param["weight"] = st.slider(
                f"Peso {i+1}", 
                min_value=0.1, 
                max_value=10.0, 
                value=param["weight"],
                step=0.1,
                key=f"param_weight_{i}"
            )
        
        with col4:
            if st.button("Remover", key=f"remove_param_{i}"):
                params_to_remove.append(i)
    
    # Remove parameters marked for removal
    if params_to_remove:
        st.session_state.economic_engineering["monetary_policy"]["policy_parameters"] = [
            param for i, param in enumerate(st.session_state.economic_engineering["monetary_policy"]["policy_parameters"]) 
            if i not in params_to_remove
        ]

# Economic Metrics
st.subheader("Métricas Econômicas")
st.markdown("Configure métricas econômicas alvo para seu token.")

col1, col2 = st.columns(2)

with col1:
    velocity = st.slider(
        "Velocidade do Token (rotações/ano)",
        min_value=0.1,
        max_value=50.0,
        value=st.session_state.economic_engineering["economic_metrics"]["velocity"],
        step=0.1,
        help="Número médio de vezes que um token muda de mãos em um ano."
    )

with col2:
    liquidity_ratio = st.slider(
        "Ratio de Liquidez (Volume/Market Cap)",
        min_value=0.01,
        max_value=1.0,
        value=st.session_state.economic_engineering["economic_metrics"]["liquidity_ratio"],
        step=0.01,
        help="Relação entre volume diário de negociação e capitalização de mercado."
    )

# Holder Distribution
st.subheader("Distribuição de Holders Alvo")
st.markdown("Configure a distribuição ideal de tokens entre diferentes tipos de holders.")

# Usando três sliders separados em vez de um único slider de tupla
col1, col2, col3 = st.columns(3)

with col1:
    holder_long_term = st.slider(
        "Holders de Longo Prazo (%)",
        min_value=0,
        max_value=100,
        value=st.session_state.economic_engineering["economic_metrics"]["holder_distribution"][0] if len(st.session_state.economic_engineering["economic_metrics"]["holder_distribution"]) >= 1 else 70,
        help="Porcentagem de tokens mantidos por holders de longo prazo."
    )

with col2:
    holder_medium_term = st.slider(
        "Holders de Médio Prazo (%)",
        min_value=0,
        max_value=100,
        value=st.session_state.economic_engineering["economic_metrics"]["holder_distribution"][1] if len(st.session_state.economic_engineering["economic_metrics"]["holder_distribution"]) >= 2 else 20,
        help="Porcentagem de tokens mantidos por holders de médio prazo."
    )

with col3:
    holder_short_term = st.slider(
        "Holders de Curto Prazo (%)",
        min_value=0,
        max_value=100,
        value=st.session_state.economic_engineering["economic_metrics"]["holder_distribution"][2] if len(st.session_state.economic_engineering["economic_metrics"]["holder_distribution"]) >= 3 else 10,
        help="Porcentagem de tokens mantidos por holders de curto prazo."
    )

distribution = [holder_long_term, holder_medium_term, holder_short_term]

# Check if distribution sums to 100%
total_distribution = sum(distribution)
if total_distribution != 100:
    st.warning(f"A distribuição de holders soma {total_distribution}%. O total deve ser 100%.")

# Save button
if st.button("Salvar Configurações de Engenharia Econômica", type="primary"):
    # Update economic engineering data in session state
    st.session_state.economic_engineering["supply_mechanisms"]["has_cap"] = has_cap
    st.session_state.economic_engineering["supply_mechanisms"]["max_supply"] = max_supply
    st.session_state.economic_engineering["supply_mechanisms"]["inflation_rate"] = inflation_rate
    st.session_state.economic_engineering["supply_mechanisms"]["burn_mechanism"] = burn_mechanism
    st.session_state.economic_engineering["supply_mechanisms"]["burn_rate"] = burn_rate
    st.session_state.economic_engineering["supply_mechanisms"]["burn_conditions"] = burn_conditions
    st.session_state.economic_engineering["supply_mechanisms"]["emission_schedule"] = new_emission_schedule
    
    st.session_state.economic_engineering["governance_mechanisms"]["voting_power"] = voting_power_internal
    st.session_state.economic_engineering["governance_mechanisms"]["proposal_threshold"] = proposal_threshold
    st.session_state.economic_engineering["governance_mechanisms"]["voting_period"] = voting_period
    st.session_state.economic_engineering["governance_mechanisms"]["quorum"] = quorum
    st.session_state.economic_engineering["governance_mechanisms"]["supermajority"] = supermajority
    st.session_state.economic_engineering["governance_mechanisms"]["delegation"] = delegation
    st.session_state.economic_engineering["governance_mechanisms"]["timelock"] = timelock
    
    st.session_state.economic_engineering["monetary_policy"]["policy_type"] = policy_type_internal
    st.session_state.economic_engineering["monetary_policy"]["target_inflation"] = target_inflation
    st.session_state.economic_engineering["monetary_policy"]["adjustment_frequency"] = adjustment_frequency_internal
    st.session_state.economic_engineering["monetary_policy"]["min_inflation"] = min_inflation
    st.session_state.economic_engineering["monetary_policy"]["max_inflation"] = max_inflation
    
    st.session_state.economic_engineering["economic_metrics"]["velocity"] = velocity
    st.session_state.economic_engineering["economic_metrics"]["liquidity_ratio"] = liquidity_ratio
    st.session_state.economic_engineering["economic_metrics"]["holder_distribution"] = list(distribution)
    
    st.success("Configurações de engenharia econômica salvas com sucesso!")

# Visualizations
st.header("Visualizações de Engenharia Econômica")

# Token Supply Visualization
st.subheader("Dinâmica de Oferta de Tokens")

# Create data for token supply projection
years = list(range(1, 11))  # 10 years projection
initial_supply = model.total_supply if hasattr(model, 'total_supply') else 100000000
circulating_supply = []

current_supply = initial_supply
for year in years:
    # Find emission for this year
    year_emission = 0.0
    for emission in new_emission_schedule:
        if emission["year"] == year:
            year_emission = emission["emission"]
            break
    
    # For years beyond the schedule, use the last year's emission or inflation rate
    if year > len(new_emission_schedule):
        if has_cap:
            if burn_mechanism:
                # With cap and burn, apply burn rate
                current_supply = current_supply * (1 - burn_rate / 100)
            else:
                # With cap but no burn, no change
                pass
        else:
            # No cap, apply inflation
            current_supply = current_supply * (1 + inflation_rate / 100)
    else:
        # Apply scheduled emission
        current_supply = initial_supply * year_emission / 100
    
    # Apply burn mechanism if enabled
    if burn_mechanism and year > 1:
        current_supply = current_supply * (1 - burn_rate / 100)
    
    # Ensure supply doesn't exceed max supply
    if has_cap and current_supply > max_supply:
        current_supply = max_supply
    
    circulating_supply.append(current_supply)

# Create line chart for token supply
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=years, 
    y=circulating_supply,
    mode='lines+markers',
    name='Oferta Circulante',
    line=dict(color='#0068c9', width=3)
))

if has_cap:
    # Add max supply line
    fig.add_trace(go.Scatter(
        x=years,
        y=[max_supply] * len(years),
        mode='lines',
        name='Oferta Máxima',
        line=dict(color='#ff4b4b', width=2, dash='dash')
    ))

fig.update_layout(
    title="Projeção de Oferta de Tokens (10 Anos)",
    xaxis_title="Ano",
    yaxis_title="Oferta de Tokens",
    legend=dict(x=0.01, y=0.99),
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# Emission Schedule Visualization
st.subheader("Cronograma de Emissão")

# Create bar chart for emission schedule
emission_years = [item["year"] for item in new_emission_schedule]
emission_values = [item["emission"] for item in new_emission_schedule]

fig = px.bar(
    x=emission_years,
    y=emission_values,
    labels={"x": "Ano", "y": "Emissão (% do Total)"},
    title="Cronograma de Emissão de Tokens",
    color=emission_values,
    color_continuous_scale="Blues"
)

st.plotly_chart(fig, use_container_width=True)

# Token Metrics Visualization
st.subheader("Métricas Econômicas")

# Create visualizations for token metrics
col1, col2 = st.columns(2)

with col1:
    # Holder distribution
    holder_labels = ["Longo Prazo", "Médio Prazo", "Curto Prazo"]
    holder_values = list(distribution)
    
    fig = px.pie(
        values=holder_values,
        names=holder_labels,
        title="Distribuição de Holders Alvo",
        color_discrete_sequence=px.colors.sequential.Blues_r,
        hole=0.4
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Velocity and liquidity metrics
    metrics_labels = ["Velocidade do Token", "Ratio de Liquidez"]
    metrics_values = [velocity, liquidity_ratio * 100]  # Convert liquidity ratio to percentage
    
    fig = px.bar(
        x=metrics_labels,
        y=metrics_values,
        labels={"x": "Métrica", "y": "Valor"},
        title="Métricas Econômicas do Token",
        color=metrics_values,
        color_continuous_scale="Blues"
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Governance Visualization
st.subheader("Mecanismos de Governança")

# Create data for governance visualization
gov_metrics = [
    {"Métrica": "Limite de Proposta", "Valor": f"{proposal_threshold:.2f}%"},
    {"Métrica": "Período de Votação", "Valor": f"{voting_period} dias"},
    {"Métrica": "Quórum", "Valor": f"{quorum:.1f}%"},
    {"Métrica": "Supermaioria", "Valor": f"{supermajority:.1f}%"},
    {"Métrica": "Timelock", "Valor": f"{timelock} dias"},
    {"Métrica": "Delegação", "Valor": "Sim" if delegation else "Não"}
]

# Create a table for governance metrics
fig = go.Figure(data=[go.Table(
    header=dict(
        values=["<b>Parâmetro de Governança</b>", "<b>Valor</b>"],
        fill_color='#0068c9',
        align='center',
        font=dict(color='white', size=14)
    ),
    cells=dict(
        values=[
            [m["Métrica"] for m in gov_metrics],
            [m["Valor"] for m in gov_metrics]
        ],
        fill_color=['#f5f7fa', '#edf3f9'],
        align='left',
        font=dict(size=12)
    )
)])

fig.update_layout(
    margin=dict(l=10, r=10, t=10, b=10),
    height=300
)

st.plotly_chart(fig, use_container_width=True)

# Monetary Policy Visualization
if policy_type != "Fixa":
    st.subheader("Política Monetária")
    
    # Create radar chart for monetary policy parameters
    if st.session_state.economic_engineering["monetary_policy"]["policy_parameters"]:
        params = st.session_state.economic_engineering["monetary_policy"]["policy_parameters"]
        
        param_names = [param["name"] for param in params]
        param_targets = [param["target"] for param in params]
        param_weights = [param["weight"] for param in params]
        
        # Add first point again to close the loop
        if param_names:
            param_names.append(param_names[0])
            param_targets.append(param_targets[0])
            param_weights.append(param_weights[0])
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=param_targets,
                theta=param_names,
                fill='toself',
                name='Valores Alvo',
                line=dict(color='#0068c9')
            ))
            
            fig.add_trace(go.Scatterpolar(
                r=param_weights,
                theta=param_names,
                fill='toself',
                name='Pesos',
                line=dict(color='#83c9ff')
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, max(max(param_targets), max(param_weights)) * 1.2]
                    )
                ),
                title="Parâmetros da Política Monetária",
                height=500,
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Create inflation bounds visualization
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=[0, 1, 2, 3, 4, 5],
        y=[target_inflation] * 6,
        mode='lines',
        name='Inflação Alvo',
        line=dict(color='#0068c9', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=[0, 1, 2, 3, 4, 5],
        y=[max_inflation] * 6,
        mode='lines',
        name='Inflação Máxima',
        line=dict(color='#ff4b4b', width=2, dash='dash')
    ))
    
    fig.add_trace(go.Scatter(
        x=[0, 1, 2, 3, 4, 5],
        y=[min_inflation] * 6,
        mode='lines',
        name='Inflação Mínima',
        line=dict(color='#00b050', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title="Limites de Inflação",
        xaxis_title="Tempo",
        yaxis_title="Taxa de Inflação (%)",
        legend=dict(x=0.01, y=0.99),
        hovermode="x unified"
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Incentive Mechanisms Visualization
if st.session_state.economic_engineering["incentive_mechanisms"]:
    st.subheader("Mecanismos de Incentivo")
    
    # Create bar chart for incentive reward rates
    incentives = st.session_state.economic_engineering["incentive_mechanisms"]
    
    incentive_names = [inc["name"] for inc in incentives]
    incentive_rates = [inc["reward_rate"] for inc in incentives]
    incentive_types = [inc["type"] for inc in incentives]
    
    if incentive_names and all(incentive_names):
        fig = px.bar(
            x=incentive_names,
            y=incentive_rates,
            color=incentive_types,
            labels={"x": "Mecanismo de Incentivo", "y": "Taxa de Recompensa (% anual)", "color": "Tipo"},
            title="Taxas de Recompensa por Mecanismo de Incentivo"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Create detailed table of incentives
        incentive_data = []
        for inc in incentives:
            incentive_data.append({
                "Mecanismo": inc["name"],
                "Tipo": inc["type"],
                "Recompensa": f"{inc['reward_rate']:.1f}% ao ano",
                "Duração": f"{inc['duration']} dias",
                "Descrição": inc["description"]
            })
        
        incentive_df = pd.DataFrame(incentive_data)
        st.dataframe(incentive_df, height=200, hide_index=True)

# Simulation Results
st.header("Simulação de Economia do Token")

# Create token economy simulation
st.subheader("Simulação de Economia do Token (10 Anos)")

# Initialize more detailed simulation data
def simulate_token_economy(years, initial_supply):
    # Create arrays for simulation data
    simulation_data = []
    
    # Initialize variables
    circulating_supply = 0
    staked_supply = 0
    price = 1.0  # Normalized initial price
    market_cap = 0
    total_staking_rewards = 0
    burn_amount = 0
    inflation_amount = 0
    
    for year in range(1, years + 1):
        # Find emission for this year
        year_emission = 0.0
        for emission in new_emission_schedule:
            if emission["year"] == year:
                year_emission = emission["emission"]
                break
        
        # For years beyond the schedule, use the last year's emission or inflation rate
        if year > len(new_emission_schedule):
            if has_cap:
                if year == 1:
                    # Initial year
                    circulating_supply = initial_supply * (year_emission / 100)
                elif burn_mechanism:
                    # With cap and burn, apply burn rate
                    burn_amount = circulating_supply * (burn_rate / 100)
                    circulating_supply -= burn_amount
                else:
                    # With cap but no burn, no change
                    pass
            else:
                # No cap, apply inflation
                inflation_amount = circulating_supply * (inflation_rate / 100)
                circulating_supply += inflation_amount
        else:
            # Apply scheduled emission
            circulating_supply = initial_supply * (year_emission / 100)
        
        # Calculate staked amount (based on incentives)
        staking_rate = 0.0
        for inc in st.session_state.economic_engineering["incentive_mechanisms"]:
            if inc["type"] == "Staking" and inc["reward_rate"] > 0:
                # Simple model: staking rate increases with reward rate
                staking_rate += (inc["reward_rate"] / 100) * 0.5  # 50% of tokens staked at 100% APY
        
        # Limit staking rate to 90%
        staking_rate = min(staking_rate, 0.9)
        
        staked_supply = circulating_supply * staking_rate
        
        # Calculate staking rewards
        staking_rewards = 0
        for inc in st.session_state.economic_engineering["incentive_mechanisms"]:
            if inc["type"] == "Staking":
                staking_rewards += staked_supply * (inc["reward_rate"] / 100)
        
        total_staking_rewards += staking_rewards
        
        # Ensure supply doesn't exceed max supply
        if has_cap and circulating_supply > max_supply:
            circulating_supply = max_supply
        
        # Simple price model based on supply/demand and holder distribution
        price_change = 0.0
        
        # Factor 1: Impact of emission schedule (more emission = price decrease)
        if year <= len(new_emission_schedule):
            # Only apply during emission schedule
            emission_factor = -0.1 * (year_emission / 100)  # -10% at full emission
            price_change += emission_factor
        
        # Factor 2: Staking impact (more staking = price increase)
        staking_factor = 0.15 * staking_rate  # +15% at 100% staking
        price_change += staking_factor
        
        # Factor 3: Burn impact (more burn = price increase)
        if burn_mechanism:
            burn_factor = 0.2 * (burn_rate / 100)  # +20% at 100% burn rate
            price_change += burn_factor
        
        # Factor 4: Inflation impact (more inflation = price decrease)
        if not has_cap:
            inflation_factor = -0.2 * (inflation_rate / 100)  # -20% at 100% inflation
            price_change += inflation_factor
        
        # Apply price change with random noise
        random_factor = np.random.normal(0, 0.05)  # Random noise with 5% std dev
        price = price * (1 + price_change + random_factor)
        
        # Ensure price doesn't go negative
        price = max(price, 0.01)
        
        # Calculate market cap
        market_cap = circulating_supply * price
        
        # Calculate token velocity based on settings
        token_velocity = velocity * (1 - staking_rate)  # Staking reduces velocity
        
        # Calculate liquidity
        daily_volume = market_cap * liquidity_ratio
        
        # Store simulation data
        simulation_data.append({
            "Year": year,
            "Circulating_Supply": circulating_supply,
            "Staked_Supply": staked_supply,
            "Staking_Rate": staking_rate,
            "Price": price,
            "Market_Cap": market_cap,
            "Staking_Rewards": staking_rewards,
            "Token_Velocity": token_velocity,
            "Daily_Volume": daily_volume,
            "Burn_Amount": burn_amount,
            "Inflation_Amount": inflation_amount
        })
    
    return pd.DataFrame(simulation_data)

# Run simulation
simulation_df = simulate_token_economy(10, initial_supply)

# Display economic simulation
col1, col2 = st.columns([7, 3])

with col1:
    # Price and Supply Chart
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(x=simulation_df["Year"], y=simulation_df["Price"], 
                  name="Preço", line=dict(color='#0068c9', width=3)),
        secondary_y=False,
    )
    
    fig.add_trace(
        go.Scatter(x=simulation_df["Year"], y=simulation_df["Circulating_Supply"], 
                  name="Oferta Circulante", line=dict(color='#83c9ff', width=3)),
        secondary_y=True,
    )
    
    fig.update_layout(
        title_text="Preço e Oferta Circulante",
        hovermode="x unified"
    )
    
    fig.update_xaxes(title_text="Ano")
    fig.update_yaxes(title_text="Preço (normalizado)", secondary_y=False)
    fig.update_yaxes(title_text="Oferta de Tokens", secondary_y=True)
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Key metrics
    st.metric(
        "Preço Ano 5", 
        f"{simulation_df['Price'].iloc[4]:.4f}", 
        f"{((simulation_df['Price'].iloc[4] / simulation_df['Price'].iloc[0]) - 1) * 100:.1f}%"
    )
    
    st.metric(
        "Preço Ano 10", 
        f"{simulation_df['Price'].iloc[9]:.4f}", 
        f"{((simulation_df['Price'].iloc[9] / simulation_df['Price'].iloc[0]) - 1) * 100:.1f}%"
    )
    
    st.metric(
        "Oferta Circulante Final", 
        f"{simulation_df['Circulating_Supply'].iloc[9]:,.0f}", 
        f"{((simulation_df['Circulating_Supply'].iloc[9] / simulation_df['Circulating_Supply'].iloc[0]) - 1) * 100:.1f}%" if simulation_df['Circulating_Supply'].iloc[0] > 0 else "N/A"
    )
    
    st.metric(
        "Market Cap Final", 
        f"{simulation_df['Market_Cap'].iloc[9]:,.0f}", 
        f"{((simulation_df['Market_Cap'].iloc[9] / simulation_df['Market_Cap'].iloc[0]) - 1) * 100:.1f}%" if simulation_df['Market_Cap'].iloc[0] > 0 else "N/A"
    )

# Staking and Velocity Chart
col1, col2 = st.columns(2)

with col1:
    fig = px.line(
        simulation_df,
        x="Year",
        y="Staking_Rate",
        labels={"Year": "Ano", "Staking_Rate": "Taxa de Staking"},
        title="Taxa de Staking ao Longo do Tempo"
    )
    
    fig.update_layout(yaxis=dict(tickformat=".0%"))
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.line(
        simulation_df,
        x="Year",
        y="Token_Velocity",
        labels={"Year": "Ano", "Token_Velocity": "Velocidade do Token"},
        title="Velocidade do Token ao Longo do Tempo"
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Display simulation data table
st.subheader("Dados Detalhados da Simulação")

# Format the dataframe for display
display_df = simulation_df.copy()
display_df["Price"] = display_df["Price"].map("{:.4f}".format)
display_df["Staking_Rate"] = display_df["Staking_Rate"].map("{:.1%}".format)
display_df["Token_Velocity"] = display_df["Token_Velocity"].map("{:.1f}".format)

display_df.columns = [
    "Ano", 
    "Oferta Circulante", 
    "Tokens em Staking", 
    "Taxa de Staking", 
    "Preço", 
    "Market Cap", 
    "Recompensas de Staking",
    "Velocidade do Token",
    "Volume Diário",
    "Quantidade Queimada",
    "Inflação"
]

st.dataframe(display_df, height=300, hide_index=True)

# Economic Engineering Recommendations
st.header("Recomendações de Engenharia Econômica")

# Generate recommendations based on simulation results
recommendations = []

# Check if price is stable or growing
price_year1 = simulation_df['Price'].iloc[0]
price_year5 = simulation_df['Price'].iloc[4]
price_year10 = simulation_df['Price'].iloc[9]

price_growth_5yr = (price_year5 / price_year1) - 1
price_growth_10yr = (price_year10 / price_year1) - 1

if price_growth_10yr < 0:
    recommendations.append("O modelo atual resulta em queda de preço a longo prazo. Considere aumentar mecanismos de queima ou reduzir a emissão de tokens nos anos iniciais.")
elif price_growth_10yr > 5:
    recommendations.append("O modelo atual resulta em crescimento de preço muito acentuado, o que pode limitar a adoção. Considere ajustar a emissão para suavizar a curva de valorização.")
else:
    recommendations.append("O modelo atual demonstra um crescimento de preço sustentável a longo prazo, o que é positivo para o valor do token.")

# Check staking rate
avg_staking_rate = simulation_df['Staking_Rate'].mean()
if avg_staking_rate < 0.1:  # < 10%
    recommendations.append("A taxa de staking é muito baixa. Considere aumentar os incentivos de staking para reduzir a oferta circulante e promover retenção de longo prazo.")
elif avg_staking_rate > 0.7:  # > 70%
    recommendations.append("A taxa de staking é muito alta, o que pode afetar a liquidez. Considere reduzir os incentivos de staking ou aumentar os incentivos para outras atividades no ecossistema.")
else:
    recommendations.append("A taxa de staking está em um nível saudável, balanceando liquidez e retenção de longo prazo.")

# Check token velocity
avg_velocity = simulation_df['Token_Velocity'].mean()
if avg_velocity > 10:
    recommendations.append("A velocidade do token é alta, o que pode pressionar o preço para baixo. Considere implementar mecanismos para reduzir a velocidade, como staking, vesting ou utilidade de longo prazo.")
elif avg_velocity < 1:
    recommendations.append("A velocidade do token é muito baixa, o que pode indicar pouca utilidade ou atividade. Considere adicionar mais casos de uso para aumentar a utilidade do token.")

# Check burn mechanism
if burn_mechanism and burn_rate < 1:
    recommendations.append("O mecanismo de queima tem taxa baixa. Para maior impacto no preço, considere aumentar a taxa de queima ou implementar eventos de queima específicos.")
elif not burn_mechanism and not has_cap:
    recommendations.append("O token não tem limite de oferta nem mecanismo de queima, o que pode levar à inflação descontrolada. Considere implementar um desses mecanismos para controlar a oferta.")

# Check governance parameters
if quorum > 50:
    recommendations.append("O quórum de governança é alto, o que pode dificultar a aprovação de propostas. Considere reduzir o quórum para facilitar a tomada de decisões, especialmente nos estágios iniciais.")

# Check incentive mechanisms
if not st.session_state.economic_engineering["incentive_mechanisms"]:
    recommendations.append("Não há mecanismos de incentivo definidos. Considere implementar incentivos para atividades como staking, liquidez e participação em governança.")
elif len(st.session_state.economic_engineering["incentive_mechanisms"]) == 1:
    recommendations.append("Há apenas um mecanismo de incentivo definido. Considere diversificar os incentivos para diferentes atividades no ecossistema.")

# Ensure we have at least a few recommendations
if len(recommendations) < 3:
    default_recommendations = [
        "Monitore continuamente a dinâmica de oferta e demanda do token após o lançamento e ajuste os parâmetros conforme necessário.",
        "Considere implementar um fundo de reserva para intervir no mercado em situações extremas.",
        "Estabeleça mecanismos de feedback com a comunidade para avaliar e ajustar os parâmetros econômicos ao longo do tempo."
    ]
    
    for rec in default_recommendations:
        if rec not in recommendations:
            recommendations.append(rec)
            if len(recommendations) >= 5:
                break

# Display recommendations
for i, rec in enumerate(recommendations):
    st.markdown(f"**{i+1}.** {rec}")