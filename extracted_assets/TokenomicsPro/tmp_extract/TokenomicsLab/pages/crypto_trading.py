import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os

# Import local modules
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.tokenomics import TokenomicsModel

st.set_page_config(
    page_title="Crypto Trading | Tokenomics Lab",
    page_icon="📈",
    layout="wide"
)

# Sidebar
st.sidebar.title("Tokenomics Lab")
st.sidebar.image("https://cdn.jsdelivr.net/npm/cryptocurrency-icons@0.18.1/svg/icon/btc.svg", width=50)

# Main content
st.title("Crypto Trading")
st.markdown("""
    Analise diferentes aspectos de trading para o seu token, incluindo liquidez, pares de trading,
    spreads, profundidade de mercado e estratégias para market makers.
""")

# Check if model exists in session state
if 'model' not in st.session_state:
    st.warning("Você ainda não criou um modelo de tokenomics. Vá para a página de Simulação para criar um modelo primeiro.")
    
    # Button to go to simulation page
    if st.button("Ir para Simulação"):
        st.switch_page("pages/simulation.py")
        
    st.stop()

# Initialize crypto trading data in session state if not exists
if 'crypto_trading' not in st.session_state:
    st.session_state.crypto_trading = {
        "exchanges": [],
        "trading_pairs": ["USDT", "ETH", "BTC"],
        "liquidity_allocation": {
            "centralized": 40,
            "decentralized": 60
        },
        "market_making": {
            "initial_capital": 250000,
            "bid_ask_spread": 0.5,
            "depth_distribution": [40, 30, 20, 10],
            "rebalancing_frequency": "4h",
            "volatility_response": "medium"
        },
        "market_impact": {
            "buy_1pct": 0.5,
            "buy_5pct": 3.0,
            "buy_10pct": 7.0,
            "sell_1pct": 0.7,
            "sell_5pct": 4.0,
            "sell_10pct": 9.0
        },
        "token_metrics": {
            "daily_volume": 0,
            "liquidity_ratio": 0.0,
            "holding_distribution": []
        }
    }

# Crypto Trading Configuration
st.header("Configuração de Crypto Trading")

# Trading Pair Configuration
st.subheader("Pares de Trading")
st.markdown("Configure os principais pares de trading para o seu token.")

# Trading pairs input
trading_pairs_str = st.text_input(
    "Pares de Trading (separados por vírgula)",
    value=", ".join(st.session_state.crypto_trading["trading_pairs"]),
    help="Lista dos pares de trading que seu token terá (ex: USDT, ETH, BTC)."
)

trading_pairs = [pair.strip() for pair in trading_pairs_str.split(",") if pair.strip()]

# Exchange Configuration
st.subheader("Exchanges")
st.markdown("Adicione exchanges onde seu token será listado.")

# Dynamic form for exchanges
if st.button("Adicionar Exchange"):
    st.session_state.crypto_trading["exchanges"].append({
        "name": "",
        "type": "CEX",
        "trading_pairs": [],
        "listing_cost": 0,
        "estimated_volume": 0
    })

# Display existing exchanges
exchanges_to_remove = []

for i, exchange in enumerate(st.session_state.crypto_trading["exchanges"]):
    with st.expander(f"Exchange {i+1}: {exchange['name'] or 'Nova Exchange'}"):
        col1, col2 = st.columns(2)
        
        with col1:
            exchange["name"] = st.text_input(
                "Nome da Exchange", 
                value=exchange["name"],
                key=f"ex_name_{i}"
            )
            
            exchange["type"] = st.selectbox(
                "Tipo", 
                ["CEX (Centralizada)", "DEX (Descentralizada)"],
                index=0 if exchange["type"] == "CEX" else 1,
                key=f"ex_type_{i}"
            )
            
            # Convert type to short form
            exchange["type"] = "CEX" if exchange["type"] == "CEX (Centralizada)" else "DEX"
        
        with col2:
            # Multi-select for trading pairs from the main trading pairs list
            selected_pairs = st.multiselect(
                "Pares de Trading",
                options=trading_pairs,
                default=exchange["trading_pairs"],
                key=f"ex_pairs_{i}"
            )
            exchange["trading_pairs"] = selected_pairs
            
            exchange["listing_cost"] = st.number_input(
                "Custo de Listagem (USD)", 
                min_value=0, 
                value=exchange["listing_cost"],
                step=1000,
                key=f"ex_cost_{i}"
            )
            
            exchange["estimated_volume"] = st.number_input(
                "Volume Diário Estimado (USD)", 
                min_value=0, 
                value=exchange["estimated_volume"],
                step=10000,
                key=f"ex_volume_{i}"
            )
        
        if st.button("Remover Exchange", key=f"remove_ex_{i}"):
            exchanges_to_remove.append(i)

# Remove exchanges marked for removal
if exchanges_to_remove:
    st.session_state.crypto_trading["exchanges"] = [ex for i, ex in enumerate(st.session_state.crypto_trading["exchanges"]) 
                                if i not in exchanges_to_remove]

# Liquidity Allocation
st.subheader("Alocação de Liquidez")
st.markdown("Configure como a liquidez será distribuída entre exchanges centralizadas e descentralizadas.")

col1, col2 = st.columns(2)

with col1:
    centralized_allocation = st.slider(
        "Alocação em Exchanges Centralizadas (%)",
        min_value=0,
        max_value=100,
        value=st.session_state.crypto_trading["liquidity_allocation"]["centralized"],
        step=5,
        help="Porcentagem da liquidez alocada em exchanges centralizadas."
    )
    
    # Ensure decentralized allocation sums to 100%
    decentralized_allocation = 100 - centralized_allocation

with col2:
    st.write(f"Alocação em Exchanges Descentralizadas: {decentralized_allocation}%")
    
    # Calculate total estimated volume
    total_volume = sum(ex["estimated_volume"] for ex in st.session_state.crypto_trading["exchanges"])
    
    st.metric(
        "Volume Diário Total Estimado", 
        f"${total_volume:,.0f}"
    )

# Market Making Configuration
st.subheader("Configuração de Market Making")
st.markdown("Configure parâmetros para atividades de market making.")

col1, col2 = st.columns(2)

with col1:
    initial_capital = st.number_input(
        "Capital Inicial para Market Making (USD)",
        min_value=0,
        value=st.session_state.crypto_trading["market_making"]["initial_capital"],
        step=10000,
        help="Capital inicial alocado para atividades de market making."
    )
    
    bid_ask_spread = st.slider(
        "Spread Bid-Ask Alvo (%)",
        min_value=0.01,
        max_value=5.0,
        value=st.session_state.crypto_trading["market_making"]["bid_ask_spread"],
        step=0.01,
        help="Diferença percentual alvo entre as ordens de compra e venda."
    )
    
    rebalancing_frequency = st.selectbox(
        "Frequência de Rebalanceamento",
        ["1h", "2h", "4h", "6h", "12h", "24h"],
        index=["1h", "2h", "4h", "6h", "12h", "24h"].index(
            st.session_state.crypto_trading["market_making"]["rebalancing_frequency"]
        ),
        help="Com que frequência as posições de market making são rebalanceadas."
    )

with col2:
    depth_distribution = st.slider(
        "Distribuição de Profundidade do Livro de Ordens (%)",
        min_value=0,
        max_value=100,
        value=(40, 70, 90),
        help="Distribuição da profundidade do livro de ordens entre diferentes níveis de preço (1º, 2º, 3º e 4º níveis)."
    )
    
    # Calculate depth distribution
    depth_levels = [
        depth_distribution[0],
        depth_distribution[1] - depth_distribution[0],
        depth_distribution[2] - depth_distribution[1],
        100 - depth_distribution[2]
    ]
    
    volatility_response = st.selectbox(
        "Resposta à Volatilidade",
        ["baixa", "média", "alta"],
        index=["baixa", "média", "alta"].index(
            st.session_state.crypto_trading["market_making"]["volatility_response"]
        ),
        help="Como a estratégia de market making responde a períodos de alta volatilidade."
    )

# Market Impact
st.subheader("Impacto de Mercado")
st.markdown("Configure o impacto estimado de diferentes tamanhos de ordens no preço do token.")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Impacto de Compras:**")
    
    buy_1pct = st.slider(
        "Compra de 1% da Liquidez (%)",
        min_value=0.0,
        max_value=10.0,
        value=st.session_state.crypto_trading["market_impact"]["buy_1pct"],
        step=0.1,
        help="Impacto percentual no preço de uma compra que consome 1% da liquidez."
    )
    
    buy_5pct = st.slider(
        "Compra de 5% da Liquidez (%)",
        min_value=0.0,
        max_value=20.0,
        value=st.session_state.crypto_trading["market_impact"]["buy_5pct"],
        step=0.1,
        help="Impacto percentual no preço de uma compra que consome 5% da liquidez."
    )
    
    buy_10pct = st.slider(
        "Compra de 10% da Liquidez (%)",
        min_value=0.0,
        max_value=30.0,
        value=st.session_state.crypto_trading["market_impact"]["buy_10pct"],
        step=0.1,
        help="Impacto percentual no preço de uma compra que consome 10% da liquidez."
    )

with col2:
    st.markdown("**Impacto de Vendas:**")
    
    sell_1pct = st.slider(
        "Venda de 1% da Liquidez (%)",
        min_value=0.0,
        max_value=10.0,
        value=st.session_state.crypto_trading["market_impact"]["sell_1pct"],
        step=0.1,
        help="Impacto percentual no preço de uma venda que consome 1% da liquidez."
    )
    
    sell_5pct = st.slider(
        "Venda de 5% da Liquidez (%)",
        min_value=0.0,
        max_value=20.0,
        value=st.session_state.crypto_trading["market_impact"]["sell_5pct"],
        step=0.1,
        help="Impacto percentual no preço de uma venda que consome 5% da liquidez."
    )
    
    sell_10pct = st.slider(
        "Venda de 10% da Liquidez (%)",
        min_value=0.0,
        max_value=30.0,
        value=st.session_state.crypto_trading["market_impact"]["sell_10pct"],
        step=0.1,
        help="Impacto percentual no preço de uma venda que consome 10% da liquidez."
    )

# Token Metrics
st.subheader("Métricas de Liquidez do Token")

daily_volume = st.number_input(
    "Volume Diário de Trading (USD)",
    min_value=0,
    value=st.session_state.crypto_trading["token_metrics"]["daily_volume"],
    step=10000,
    help="Volume diário total de trading do token."
)

# Liquidity Ratio (calculated or manual)
if 'model' in st.session_state and hasattr(st.session_state.model, 'total_supply') and 'simulation_result' in st.session_state:
    # Get model parameters
    model = st.session_state.model
    
    # Get the price from simulation
    df = st.session_state.simulation_result
    latest_price = df['Price'].iloc[-1]
    market_cap = latest_price * model.total_supply
    
    # Calculate liquidity ratio
    if market_cap > 0 and daily_volume > 0:
        liquidity_ratio = (daily_volume / market_cap) * 100
    else:
        liquidity_ratio = 0.0
else:
    liquidity_ratio = st.number_input(
        "Ratio de Liquidez (Volume/Market Cap em %)",
        min_value=0.0,
        max_value=100.0,
        value=st.session_state.crypto_trading["token_metrics"]["liquidity_ratio"],
        step=0.1,
        help="Ratio entre o volume diário de trading e o market cap do token (expresso como porcentagem)."
    )

# Holding Distribution
st.subheader("Distribuição de Holders")
st.markdown("Configure a distribuição estimada dos holders do seu token.")

# Dynamic form for holder groups
if "holding_distribution" not in st.session_state:
    st.session_state.holding_distribution = st.session_state.crypto_trading["token_metrics"]["holding_distribution"]
    
    # Add default groups if empty
    if not st.session_state.holding_distribution:
        st.session_state.holding_distribution = [
            {"group": "Grandes Holders (>1%)", "percentage": 30.0},
            {"group": "Médios Holders (0.1-1%)", "percentage": 45.0},
            {"group": "Pequenos Holders (<0.1%)", "percentage": 25.0}
        ]

if st.button("Adicionar Grupo de Holders"):
    st.session_state.holding_distribution.append({
        "group": "",
        "percentage": 0.0
    })

# Display existing holding groups
holders_to_remove = []

for i, holder in enumerate(st.session_state.holding_distribution):
    col1, col2, col3 = st.columns([3, 2, 1])
    
    with col1:
        holder["group"] = st.text_input(
            f"Grupo de Holders {i+1}", 
            value=holder["group"],
            key=f"holder_group_{i}"
        )
    
    with col2:
        holder["percentage"] = st.number_input(
            f"Porcentagem {i+1} (%)", 
            min_value=0.0, 
            max_value=100.0, 
            value=holder["percentage"],
            step=0.5,
            key=f"holder_pct_{i}"
        )
    
    with col3:
        if st.button("Remover", key=f"remove_holder_{i}"):
            holders_to_remove.append(i)

# Remove holders marked for removal
if holders_to_remove:
    st.session_state.holding_distribution = [holder for i, holder in enumerate(st.session_state.holding_distribution) 
                               if i not in holders_to_remove]

# Calculate total holding percentage
total_holdings = sum(holder["percentage"] for holder in st.session_state.holding_distribution)
if total_holdings != 100.0:
    st.warning(f"A soma das porcentagens de holders é {total_holdings:.1f}%. O total deve ser 100%.")

# Save button
if st.button("Salvar Configurações de Trading", type="primary"):
    # Update crypto trading data in session state
    st.session_state.crypto_trading["trading_pairs"] = trading_pairs
    
    st.session_state.crypto_trading["liquidity_allocation"] = {
        "centralized": centralized_allocation,
        "decentralized": decentralized_allocation
    }
    
    st.session_state.crypto_trading["market_making"] = {
        "initial_capital": initial_capital,
        "bid_ask_spread": bid_ask_spread,
        "depth_distribution": depth_levels,
        "rebalancing_frequency": rebalancing_frequency,
        "volatility_response": volatility_response
    }
    
    st.session_state.crypto_trading["market_impact"] = {
        "buy_1pct": buy_1pct,
        "buy_5pct": buy_5pct,
        "buy_10pct": buy_10pct,
        "sell_1pct": sell_1pct,
        "sell_5pct": sell_5pct,
        "sell_10pct": sell_10pct
    }
    
    st.session_state.crypto_trading["token_metrics"] = {
        "daily_volume": daily_volume,
        "liquidity_ratio": liquidity_ratio,
        "holding_distribution": st.session_state.holding_distribution
    }
    
    st.success("Configurações de trading salvas com sucesso!")

# Visualizations
st.header("Visualizações de Trading")

# Volume by Exchange
if st.session_state.crypto_trading["exchanges"]:
    st.subheader("Volume por Exchange")
    
    exchange_names = [ex["name"] for ex in st.session_state.crypto_trading["exchanges"] if ex["name"]]
    exchange_volumes = [ex["estimated_volume"] for ex in st.session_state.crypto_trading["exchanges"] if ex["name"]]
    exchange_types = [ex["type"] for ex in st.session_state.crypto_trading["exchanges"] if ex["name"]]
    
    if exchange_names and all(exchange_names):
        fig = px.bar(
            x=exchange_names,
            y=exchange_volumes,
            color=exchange_types,
            labels={"x": "Exchange", "y": "Volume Diário Estimado ($)", "color": "Tipo"},
            title="Volume Diário Estimado por Exchange",
            color_discrete_map={"CEX": "#0068c9", "DEX": "#83c9ff"}
        )
        
        st.plotly_chart(fig, use_container_width=True)

# Liquidity Allocation Pie Chart
st.subheader("Alocação de Liquidez")

fig = px.pie(
    values=[centralized_allocation, decentralized_allocation],
    names=["Exchanges Centralizadas", "Exchanges Descentralizadas"],
    title="Alocação de Liquidez por Tipo de Exchange",
    color_discrete_sequence=["#0068c9", "#83c9ff"],
    hole=0.4
)

fig.update_traces(textposition='inside', textinfo='percent+label')

st.plotly_chart(fig, use_container_width=True)

# Market Impact Visualization
st.subheader("Impacto de Mercado")

# Create data for impact chart
impact_sizes = ["1%", "5%", "10%"]
buy_impacts = [buy_1pct, buy_5pct, buy_10pct]
sell_impacts = [-sell_1pct, -sell_5pct, -sell_10pct]  # Negative for sells

# Create dataframe for the chart
impact_df = pd.DataFrame({
    "Tamanho da Ordem (% da Liquidez)": impact_sizes * 2,
    "Impacto no Preço (%)": buy_impacts + sell_impacts,
    "Tipo de Ordem": ["Compra"] * 3 + ["Venda"] * 3
})

# Create horizontal bar chart
fig = px.bar(
    impact_df,
    x="Impacto no Preço (%)",
    y="Tamanho da Ordem (% da Liquidez)",
    color="Tipo de Ordem",
    barmode="group",
    orientation="h",
    title="Impacto de Mercado por Tamanho de Ordem",
    color_discrete_map={"Compra": "#0068c9", "Venda": "#ff4b4b"}
)

fig.update_layout(yaxis=dict(autorange="reversed"))

st.plotly_chart(fig, use_container_width=True)

# Liquidity Depth Visualization
st.subheader("Profundidade de Mercado")

# Calculate bid and ask levels based on depth distribution
if initial_capital > 0:
    # Calculate capital at each level
    level_capital = [initial_capital * (pct / 100) for pct in depth_levels]
    
    # Create bid and ask prices
    base_price = 1.0  # Normalized to 1.0
    spread_half = bid_ask_spread / 100 / 2
    
    bid_prices = [
        base_price * (1 - spread_half),                    # Level 1
        base_price * (1 - spread_half - 0.005),            # Level 2
        base_price * (1 - spread_half - 0.015),            # Level 3
        base_price * (1 - spread_half - 0.03)              # Level 4
    ]
    
    ask_prices = [
        base_price * (1 + spread_half),                    # Level 1
        base_price * (1 + spread_half + 0.005),            # Level 2
        base_price * (1 + spread_half + 0.015),            # Level 3
        base_price * (1 + spread_half + 0.03)              # Level 4
    ]
    
    # Calculate order sizes (tokens) at each level
    # Assume tokens are priced at $1 for simplicity
    bid_sizes = [capital / price for capital, price in zip(level_capital, bid_prices)]
    ask_sizes = [capital / price for capital, price in zip(level_capital, ask_prices)]
    
    # Create data for depth chart
    depth_data = []
    
    # Add bid orders (buy side) - display negative size for visual purposes
    for level, (price, size) in enumerate(zip(bid_prices, bid_sizes)):
        depth_data.append({
            "price": price,
            "size": -size,  # Negative for buy side
            "level": f"Bid Nível {level+1}",
            "side": "Compra"
        })
    
    # Add ask orders (sell side)
    for level, (price, size) in enumerate(zip(ask_prices, ask_sizes)):
        depth_data.append({
            "price": price,
            "size": size,
            "level": f"Ask Nível {level+1}",
            "side": "Venda"
        })
    
    # Create dataframe
    depth_df = pd.DataFrame(depth_data)
    
    # Create depth chart
    fig = px.bar(
        depth_df,
        x="price",
        y="size",
        color="side",
        hover_data=["level"],
        labels={"price": "Preço Normalizado", "size": "Tamanho da Ordem", "side": "Lado"},
        title="Profundidade de Mercado",
        color_discrete_map={"Compra": "#0068c9", "Venda": "#ff4b4b"}
    )
    
    # Add middle line for current price
    fig.add_shape(
        type="line",
        x0=1.0,
        y0=min(depth_df["size"].min() * 1.1, -100),
        x1=1.0,
        y1=max(depth_df["size"].max() * 1.1, 100),
        line=dict(color="green", width=2, dash="dash")
    )
    
    fig.add_annotation(
        x=1.0,
        y=0,
        text="Preço Atual",
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-40
    )
    
    # Update layout
    fig.update_layout(
        bargap=0.1,
        xaxis=dict(title="Preço Normalizado", tickformat=".4f"),
        yaxis=dict(title="Tamanho da Ordem (Tokens)"),
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Explanation
    st.markdown("""
    **Interpretação do Gráfico de Profundidade:**
    - Barras azuis (lado esquerdo): Ordens de compra (bids) - quanto os compradores estão dispostos a pagar
    - Barras vermelhas (lado direito): Ordens de venda (asks) - quanto os vendedores estão pedindo
    - Linha verde: Preço atual do token (normalizado para 1.0)
    - Spread: Diferença entre o menor preço de venda e o maior preço de compra
    
    A distribuição da liquidez pelos diferentes níveis de preço indica quão fácil é comprar/vender 
    diferentes quantidades do token sem causar impacto significativo no preço.
    """)

# Holding Distribution Pie Chart
if st.session_state.holding_distribution and all(holder["group"] for holder in st.session_state.holding_distribution):
    st.subheader("Distribuição de Holders")
    
    holder_groups = [holder["group"] for holder in st.session_state.holding_distribution]
    holder_percentages = [holder["percentage"] for holder in st.session_state.holding_distribution]
    
    fig = px.pie(
        values=holder_percentages,
        names=holder_groups,
        title="Distribuição de Tokens por Grupo de Holders",
        color_discrete_sequence=px.colors.sequential.Blues_r,
        hole=0.4
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    st.plotly_chart(fig, use_container_width=True)

# Trading Pair Distribution
if st.session_state.crypto_trading["exchanges"] and trading_pairs:
    st.subheader("Distribuição por Par de Trading")
    
    # Count occurrences of each trading pair across exchanges
    pair_counts = {}
    for pair in trading_pairs:
        count = sum(1 for ex in st.session_state.crypto_trading["exchanges"] if pair in ex["trading_pairs"])
        pair_counts[pair] = count
    
    if pair_counts:
        pairs = list(pair_counts.keys())
        counts = list(pair_counts.values())
        
        fig = px.bar(
            x=pairs,
            y=counts,
            labels={"x": "Par de Trading", "y": "Número de Exchanges"},
            title="Disponibilidade de Pares de Trading",
            color=counts,
            color_continuous_scale="Blues"
        )
        
        st.plotly_chart(fig, use_container_width=True)

# Liquidity Metrics Table
st.subheader("Métricas de Liquidez")

# Create metrics data
if 'model' in st.session_state and hasattr(st.session_state.model, 'total_supply') and 'simulation_result' in st.session_state:
    # Get model parameters and price
    model = st.session_state.model
    df = st.session_state.simulation_result
    latest_price = df['Price'].iloc[-1]
    market_cap = latest_price * model.total_supply
    circulating_supply = df['Circulating_Supply'].iloc[-1]
    circulating_mcap = latest_price * circulating_supply
    
    # Calculate metrics
    metrics_data = {
        "Métrica": [
            "Volume Diário",
            "Market Cap (Diluído)",
            "Market Cap (Circulante)",
            "Ratio de Liquidez (Volume/MC Diluído)",
            "Ratio de Liquidez (Volume/MC Circulante)",
            "Preço por Token",
            "Bid-Ask Spread"
        ],
        "Valor": [
            f"${daily_volume:,.0f}",
            f"${market_cap:,.0f}",
            f"${circulating_mcap:,.0f}",
            f"{(daily_volume / market_cap * 100) if market_cap > 0 else 0:.2f}%",
            f"{(daily_volume / circulating_mcap * 100) if circulating_mcap > 0 else 0:.2f}%",
            f"${latest_price:.6f}",
            f"{bid_ask_spread:.2f}%"
        ]
    }
else:
    # Use placeholder data
    metrics_data = {
        "Métrica": [
            "Volume Diário",
            "Ratio de Liquidez",
            "Bid-Ask Spread"
        ],
        "Valor": [
            f"${daily_volume:,.0f}",
            f"{liquidity_ratio:.2f}%",
            f"{bid_ask_spread:.2f}%"
        ]
    }

# Create dataframe
metrics_df = pd.DataFrame(metrics_data)

# Display as table
st.table(metrics_df)

# Recommendations
st.subheader("Recomendações de Trading")

# Generate recommendations based on the data
recommendations = []

# Check if volume is sufficient
if daily_volume < 100000:
    recommendations.append("Considere aumentar as atividades de market making para melhorar a liquidez do token.")
elif daily_volume > 1000000:
    recommendations.append("A liquidez parece saudável. Considere expandir para mais exchanges para diversificar.")

# Check liquidity ratio
if liquidity_ratio < 1.0:
    recommendations.append("O ratio de liquidez está abaixo do ideal (1-5%). Implemente programas de incentivo para aumentar o volume de trading.")
elif liquidity_ratio > 10.0:
    recommendations.append("O ratio de liquidez está acima da média. Considere estratégias para aumentar retenção de longo prazo.")

# Check bid-ask spread
if bid_ask_spread > 1.0:
    recommendations.append("O spread bid-ask é amplo. Considere aumentar o capital de market making para reduzir o spread.")
elif bid_ask_spread < 0.1:
    recommendations.append("O spread bid-ask é muito estreito. Considere ajustar a estratégia de market making para melhorar a rentabilidade.")

# Check holding distribution
large_holders_pct = sum(holder["percentage"] for holder in st.session_state.holding_distribution 
                     if "grande" in holder["group"].lower() or ">1%" in holder["group"])
if large_holders_pct > 60:
    recommendations.append("A concentração de tokens em grandes holders é alta. Trabalhe em iniciativas para melhorar a distribuição de tokens.")

# Check exchange distribution
if len(st.session_state.crypto_trading["exchanges"]) < 3 and total_volume > 500000:
    recommendations.append("Considere adicionar mais exchanges para diversificar a liquidez e reduzir riscos de concentração.")

# Add market making recommendations
if centralized_allocation > 80:
    recommendations.append("Considere diversificar a liquidez para DEXs para evitar excesso de concentração em exchanges centralizadas.")
elif decentralized_allocation > 80:
    recommendations.append("Considere adicionar mais liquidez em CEXs para alcançar traders tradicionais e aumentar a exposição.")

# Ensure we have at least one recommendation
if not recommendations:
    recommendations = [
        "Monitore constantemente a liquidez e o volume de trading para identificar tendências e possíveis problemas.",
        "Considere implementar incentivos de trading para aumentar o volume e a liquidez.",
        "Mantenha uma relação próxima com as exchanges para garantir suporte adequado e visibilidade."
    ]

# Display recommendations
for i, rec in enumerate(recommendations):
    st.markdown(f"**{i+1}.** {rec}")

# Trading Strategy Section
st.header("Estratégia de Trading")

# Simple trading strategy recommendation based on inputs
st.markdown("""
### Estratégia de Market Making Recomendada

Com base nas configurações de trading definidas, sugerimos a seguinte estratégia de market making:
""")

# Calculate recommended strategy parameters
if initial_capital > 0:
    # Distribution by exchange type
    cex_capital = initial_capital * (centralized_allocation / 100)
    dex_capital = initial_capital * (decentralized_allocation / 100)
    
    # Distribution by trading pair (simplified)
    pair_capital = {}
    pair_count = len(trading_pairs)
    if pair_count > 0:
        # Assign capital based on importance of pairs (USDT usually gets more)
        if "USDT" in trading_pairs:
            pair_capital["USDT"] = initial_capital * 0.5
            remaining = initial_capital * 0.5
            remaining_pairs = [p for p in trading_pairs if p != "USDT"]
            for pair in remaining_pairs:
                pair_capital[pair] = remaining / len(remaining_pairs)
        else:
            for pair in trading_pairs:
                pair_capital[pair] = initial_capital / pair_count
    
    # Market making parameters
    orders_per_side = 4  # Number of orders on each side
    
    # Display strategy
    st.markdown(f"""
    #### Alocação de Capital
    - **Exchanges Centralizadas:** ${cex_capital:,.0f} ({centralized_allocation}%)
    - **Exchanges Descentralizadas:** ${dex_capital:,.0f} ({decentralized_allocation}%)
    
    #### Alocação por Par de Trading
    """)
    
    for pair, capital in pair_capital.items():
        st.markdown(f"- **{pair}:** ${capital:,.0f}")
    
    st.markdown(f"""
    #### Parâmetros da Estratégia
    - **Spread Bid-Ask:** {bid_ask_spread:.2f}%
    - **Número de Ordens por Lado:** {orders_per_side}
    - **Frequência de Rebalanceamento:** {rebalancing_frequency}
    - **Distribuição de Profundidade:**
      - Nível 1: {depth_levels[0]}% do capital
      - Nível 2: {depth_levels[1]}% do capital
      - Nível 3: {depth_levels[2]}% do capital
      - Nível 4: {depth_levels[3]}% do capital
    
    #### Resposta à Volatilidade
    """)
    
    if volatility_response == "baixa":
        st.markdown("""
        - Manter a mesma estratégia independente da volatilidade
        - Foco em consistência e previsibilidade
        """)
    elif volatility_response == "média":
        st.markdown("""
        - Aumentar spreads em 50% durante períodos de alta volatilidade
        - Reduzir tamanho de ordens em 30% durante períodos de alta volatilidade
        - Rebalancear com maior frequência em mercados voláteis
        """)
    else:  # alta
        st.markdown("""
        - Duplicar spreads durante períodos de alta volatilidade
        - Reduzir tamanho de ordens em 50% durante períodos de alta volatilidade
        - Mover capital para pares mais estáveis durante turbulência de mercado
        - Considerar pausar temporariamente o market making em condições extremas
        """)
    
    # Risk management
    st.markdown("""
    #### Gestão de Risco
    - **Limite de Drawdown:** 10% do capital inicial antes de recalibrar estratégia
    - **Exposição Máxima por Par:** 40% do capital alocado para esse par
    - **Stop Loss:** Implementar parada em movimentos de preço >20% em curto período
    - **Hedge:** Considerar hedging parcial em futuros para reduzir exposição direcional
    """)
    
    # Performance metrics
    st.markdown("""
    #### Métricas de Performance a Monitorar
    - **P&L Diário:** Lucro e perda realizado e não realizado
    - **Volume Facilitado:** Quanto do volume total do token é facilitado pelo market maker
    - **Spread Médio:** Média do spread bid-ask ao longo do tempo
    - **Tempo de Atividade:** Percentual do tempo em que as ordens estão ativas
    - **Skew Ratio:** Balanço entre exposição de compra e venda
    """)