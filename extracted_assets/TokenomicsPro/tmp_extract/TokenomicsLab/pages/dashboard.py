import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Import local modules
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.tokenomics import TokenomicsModel, create_model_from_dict

st.set_page_config(
    page_title="Dashboard | Tokenomics Lab",
    page_icon="📊",
    layout="wide"
)

# Initialize session state for model if not exists
if 'model' not in st.session_state:
    # Create a default model to show as example
    default_model = TokenomicsModel("Exemplo", 100_000_000)
    default_model.set_distribution({
        "Equipe": 15.0,
        "Investidores": 25.0,
        "Comunidade": 30.0,
        "Reserva": 20.0,
        "Marketing": 10.0
    })
    
    # Set vesting schedules
    default_model.set_vesting_schedule("Equipe", [
        (0, 0),      # 0% at launch
        (6, 25),     # 25% after 6 months
        (12, 25),    # 25% after 12 months
        (18, 25),    # 25% after 18 months
        (24, 25)     # 25% after 24 months
    ])
    
    default_model.set_vesting_schedule("Investidores", [
        (0, 10),     # 10% at launch
        (3, 15),     # 15% after 3 months
        (6, 15),     # 15% after 6 months
        (9, 15),     # 15% after 9 months
        (12, 15),    # 15% after 12 months
        (15, 15),    # 15% after 15 months
        (18, 15)     # 15% after 18 months
    ])
    
    default_model.set_vesting_schedule("Comunidade", [
        (0, 20),     # 20% at launch
        (6, 20),     # 20% after 6 months
        (12, 20),    # 20% after 12 months
        (18, 20),    # 20% after 18 months
        (24, 20)     # 20% after 24 months
    ])
    
    # Simulate token price
    simulation_months = 36
    initial_price = 0.1
    st.session_state.simulation_result = default_model.simulate_token_price(
        simulation_months, 
        initial_price,
        volatility=0.08
    )
    
    st.session_state.model = default_model

st.sidebar.title("Tokenomics Lab")
st.sidebar.image("https://cdn.jsdelivr.net/npm/cryptocurrency-icons@0.18.1/svg/icon/btc.svg", width=50)

# Dashboard content
st.title("Dashboard de Tokenomics")
st.markdown("Visualize os principais indicadores do seu modelo de tokenomics e acompanhe a evolução ao longo do tempo.")

# Get simulation results
if 'simulation_result' not in st.session_state:
    st.warning("Você ainda não simulou nenhum modelo. Vá para a página de Simulação para criar um modelo.")
    st.stop()

df = st.session_state.simulation_result

# Top metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    latest_price = df['Price'].iloc[-1]
    initial_price = df['Price'].iloc[0]
    price_change = ((latest_price - initial_price) / initial_price) * 100
    
    st.metric(
        "Preço Atual do Token", 
        f"${latest_price:.4f}", 
        f"{price_change:.2f}% desde início"
    )

with col2:
    latest_supply = df['Circulating_Supply'].iloc[-1]
    total_supply = st.session_state.model.total_supply
    supply_percent = (latest_supply / total_supply) * 100
    
    st.metric(
        "Oferta Circulante", 
        f"{latest_supply:,.0f} tokens", 
        f"{supply_percent:.1f}% do total"
    )

with col3:
    latest_mcap = df['Market_Cap'].iloc[-1]
    st.metric(
        "Market Cap", 
        f"${latest_mcap:,.2f}"
    )

with col4:
    if 'Users' in df.columns:
        latest_users = df['Users'].iloc[-1]
        initial_users = df['Users'].iloc[0]
        users_change = ((latest_users - initial_users) / initial_users) * 100
        
        st.metric(
            "Usuários", 
            f"{latest_users:,.0f}", 
            f"{users_change:.1f}%"
        )
    elif 'Staking_Rate' in df.columns:
        latest_staking = df['Staking_Rate'].iloc[-1] * 100
        initial_staking = df['Staking_Rate'].iloc[0] * 100
        staking_change = latest_staking - initial_staking
        
        st.metric(
            "Taxa de Staking", 
            f"{latest_staking:.1f}%", 
            f"{staking_change:.1f}%"
        )
    else:
        # For basic model without specific metrics
        max_month = df['Month'].max()
        st.metric(
            "Período de Simulação",
            f"{max_month} meses"
        )

# Main charts
st.subheader("Evolução do Preço e Oferta de Tokens")

# Create subplot with shared x-axis
fig = make_subplots(
    rows=2, 
    cols=1, 
    shared_xaxes=True, 
    vertical_spacing=0.1,
    subplot_titles=("Preço do Token ($)", "Oferta Circulante de Tokens")
)

# Add price line
fig.add_trace(
    go.Scatter(
        x=df['Month'], 
        y=df['Price'],
        mode='lines',
        name='Preço',
        line=dict(color='#0068c9', width=2)
    ),
    row=1, col=1
)

# Add circulating supply line
fig.add_trace(
    go.Scatter(
        x=df['Month'], 
        y=df['Circulating_Supply'],
        mode='lines',
        name='Oferta Circulante',
        line=dict(color='#83c9ff', width=2),
        fill='tozeroy'
    ),
    row=2, col=1
)

# Update layout
fig.update_layout(
    height=600,
    hovermode="x unified",
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)

# Update y-axes
fig.update_yaxes(title_text="Preço ($)", row=1, col=1)
fig.update_yaxes(title_text="Tokens", row=2, col=1)
fig.update_xaxes(title_text="Mês", row=2, col=1)

st.plotly_chart(fig, use_container_width=True)

# Token Distribution
st.subheader("Distribuição de Tokens")
col1, col2 = st.columns(2)

with col1:
    # Get distribution from model
    distribution = st.session_state.model.distribution
    
    # Create data for pie chart
    categories = list(distribution.keys())
    values = list(distribution.values())
    
    # Create pie chart
    fig = px.pie(
        values=values,
        names=categories,
        title="Alocação Total de Tokens",
        color_discrete_sequence=px.colors.sequential.Blues_r,
        hole=0.4,
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Get latest month data
    latest_month = df['Month'].max()
    latest_data = df[df['Month'] == latest_month].iloc[0]
    
    # Create data for current distribution
    current_data = {}
    for category in categories:
        col_name = f'{category}_Released'
        if col_name in df.columns:
            current_data[category] = latest_data[col_name]
    
    # Create bar chart
    fig = px.bar(
        x=list(current_data.keys()),
        y=list(current_data.values()),
        title=f"Tokens Liberados (Mês {latest_month})",
        labels={'x': 'Categoria', 'y': 'Tokens Liberados'},
        color_discrete_sequence=['#0068c9']
    )
    st.plotly_chart(fig, use_container_width=True)

# Vesting schedule visualization
st.subheader("Cronograma de Vesting por Categoria")

# Prepare vesting data
vesting_data = []
for category, schedule in st.session_state.model.vesting_schedules.items():
    category_total = st.session_state.model.distribution[category] * st.session_state.model.total_supply / 100
    
    cumulative_pct = 0
    for month, pct in schedule:
        cumulative_pct += pct
        vesting_data.append({
            'Categoria': category,
            'Mês': month,
            'Porcentagem Acumulada': cumulative_pct,
            'Tokens Liberados': category_total * cumulative_pct / 100
        })

if vesting_data:
    vesting_df = pd.DataFrame(vesting_data)
    
    # Create line chart
    fig = px.line(
        vesting_df, 
        x='Mês', 
        y='Porcentagem Acumulada', 
        color='Categoria',
        title="Cronograma de Vesting (% Acumulada)",
        labels={'Porcentagem Acumulada': '% Acumulada'},
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    
    fig.update_layout(
        yaxis=dict(ticksuffix="%"),
        hovermode="x unified"
    )
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Não há dados de vesting configurados no modelo atual.")

# Market cap chart
st.subheader("Evolução do Market Cap")

fig = px.area(
    df, 
    x='Month', 
    y='Market_Cap',
    title="Evolução do Market Cap ao Longo do Tempo",
    labels={'Month': 'Mês', 'Market_Cap': 'Market Cap ($)'},
    color_discrete_sequence=['#83c9ff']
)

fig.update_layout(
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# Model-specific metrics
st.subheader("Métricas Específicas do Modelo")

if 'Users' in df.columns and 'Token_Demand' in df.columns:
    # Utility token model
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.line(
            df, 
            x='Month', 
            y='Users',
            title="Crescimento de Usuários",
            labels={'Month': 'Mês', 'Users': 'Usuários'},
            color_discrete_sequence=['#0068c9']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.line(
            df, 
            x='Month', 
            y='Token_Demand',
            title="Demanda de Tokens",
            labels={'Month': 'Mês', 'Token_Demand': 'Demanda de Tokens'},
            color_discrete_sequence=['#ff9e0a']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Supply vs Demand
    fig = px.line(
        df, 
        x='Month', 
        y=['Circulating_Supply', 'Token_Demand'],
        title="Oferta vs Demanda de Tokens",
        labels={'Month': 'Mês', 'value': 'Tokens', 'variable': 'Métrica'},
        color_discrete_map={
            'Circulating_Supply': '#0068c9',
            'Token_Demand': '#ff9e0a'
        }
    )
    
    fig.update_layout(
        hovermode="x unified"
    )
    
    st.plotly_chart(fig, use_container_width=True)

elif 'Staking_Rate' in df.columns and 'Staked_Tokens' in df.columns:
    # Governance token model
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.line(
            df, 
            x='Month', 
            y='Staking_Rate',
            title="Taxa de Staking",
            labels={'Month': 'Mês', 'Staking_Rate': 'Taxa de Staking'},
            color_discrete_sequence=['#0068c9']
        )
        
        fig.update_layout(
            yaxis=dict(tickformat=".0%")
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.line(
            df, 
            x='Month', 
            y=['Staked_Tokens', 'Liquid_Tokens'],
            title="Tokens em Staking vs Tokens Líquidos",
            labels={'Month': 'Mês', 'value': 'Tokens', 'variable': 'Tipo'},
            color_discrete_map={
                'Staked_Tokens': '#0068c9',
                'Liquid_Tokens': '#ff9e0a'
            }
        )
        
        fig.update_layout(
            hovermode="x unified"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Price vs Staking Rate
    df['Normalized_Price'] = df['Price'] / df['Price'].iloc[0]
    df['Staking_Rate_Pct'] = df['Staking_Rate'] * 100
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(
            x=df['Month'], 
            y=df['Normalized_Price'],
            mode='lines',
            name='Preço Normalizado',
            line=dict(color='#0068c9', width=2)
        ),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(
            x=df['Month'], 
            y=df['Staking_Rate_Pct'],
            mode='lines',
            name='Taxa de Staking (%)',
            line=dict(color='#ff9e0a', width=2)
        ),
        secondary_y=True
    )
    
    fig.update_layout(
        title_text="Correlação entre Preço e Taxa de Staking",
        hovermode="x unified"
    )
    
    fig.update_yaxes(title_text="Preço Normalizado", secondary_y=False)
    fig.update_yaxes(title_text="Taxa de Staking (%)", secondary_y=True)
    fig.update_xaxes(title_text="Mês")
    
    st.plotly_chart(fig, use_container_width=True)
else:
    # Basic model
    st.info("Este é um modelo básico de tokenomics. Experimente os modelos de Utility Token ou Governance Token na página de Simulação para visualizar métricas específicas.")
