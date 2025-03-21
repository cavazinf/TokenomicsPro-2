import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

# Set page configuration
st.set_page_config(
    page_title="Crypto Trading - TokenomicsLab",
    page_icon="📊",
    layout="wide",
)

# Initialize language if not set
if 'language' not in st.session_state:
    st.session_state.language = 'English'

# Page title and description based on language
if st.session_state.language == 'English':
    title = "Crypto Trading Analysis"
    description = """
    Analyze trading patterns, simulate trading strategies, and understand market dynamics for your token.
    """
elif st.session_state.language == 'Português':
    title = "Análise de Negociação de Criptomoedas"
    description = """
    Analise padrões de negociação, simule estratégias de trading e entenda a dinâmica do mercado para o seu token.
    """
elif st.session_state.language == 'Español':
    title = "Análisis de Trading de Criptomonedas"
    description = """
    Analiza patrones de trading, simula estrategias de trading y comprende la dinámica del mercado para tu token.
    """
else:
    title = "Crypto Trading Analysis"
    description = """
    Analyze trading patterns, simulate trading strategies, and understand market dynamics for your token.
    """

st.title(title)
st.markdown(description)

# Define multi-language labels and texts
if st.session_state.language == 'English':
    # Sections
    market_section = "Market Data"
    volume_section = "Volume Analysis"
    liquidity_section = "Liquidity Analysis"
    strategies_section = "Trading Strategies"
    indicators_section = "Technical Indicators"
    sentiment_section = "Market Sentiment"
    
    # Market Data
    market_text = "View and analyze historical market data for benchmarking."
    select_token = "Select Benchmark Token"
    time_period = "Time Period"
    price_chart = "Price Chart"
    download_data = "Download Historical Data"
    
    # Volume Analysis
    volume_text = "Analyze trading volume patterns and trends."
    daily_volume = "Daily Trading Volume"
    volume_metrics = "Volume Metrics"
    avg_daily_volume = "Average Daily Volume"
    volume_trends = "Volume Trends"
    
    # Liquidity Analysis
    liquidity_text = "Understand liquidity depth and market impact."
    liquidity_pools = "Liquidity Pools"
    add_pool = "Add Liquidity Pool"
    pool_name = "Pool Name"
    token_amount = "Token Amount"
    paired_token = "Paired Token"
    paired_amount = "Paired Amount"
    slippage_impact = "Slippage Impact"
    trade_size = "Trade Size"
    slippage = "Slippage (%)"
    
    # Trading Strategies
    strategies_text = "Test different trading strategies for your token."
    strategy_name = "Strategy Name"
    backtest_btn = "Backtest Strategy"
    performance_metrics = "Performance Metrics"
    profit_loss = "Profit/Loss"
    win_rate = "Win Rate"
    roi = "Return on Investment (ROI)"
    drawdown = "Maximum Drawdown"
    
    # Technical Indicators
    indicators_text = "Analyze technical indicators to predict price movements."
    indicator_name = "Indicator"
    apply_indicator = "Apply Indicator"
    indicator_value = "Current Value"
    indicator_signal = "Signal"
    
    # Market Sentiment
    sentiment_text = "Gauge market sentiment from social media and news sources."
    sentiment_score = "Sentiment Score"
    sentiment_source = "Source"
    sentiment_trend = "Sentiment Trend"
    
elif st.session_state.language == 'Português':
    # Sections
    market_section = "Dados de Mercado"
    volume_section = "Análise de Volume"
    liquidity_section = "Análise de Liquidez"
    strategies_section = "Estratégias de Trading"
    indicators_section = "Indicadores Técnicos"
    sentiment_section = "Sentimento de Mercado"
    
    # Market Data
    market_text = "Visualize e analise dados históricos de mercado para benchmarking."
    select_token = "Selecionar Token de Referência"
    time_period = "Período de Tempo"
    price_chart = "Gráfico de Preço"
    download_data = "Baixar Dados Históricos"
    
    # Volume Analysis
    volume_text = "Analise padrões e tendências de volume de negociação."
    daily_volume = "Volume Diário de Negociação"
    volume_metrics = "Métricas de Volume"
    avg_daily_volume = "Volume Diário Médio"
    volume_trends = "Tendências de Volume"
    
    # Liquidity Analysis
    liquidity_text = "Entenda a profundidade de liquidez e o impacto no mercado."
    liquidity_pools = "Pools de Liquidez"
    add_pool = "Adicionar Pool de Liquidez"
    pool_name = "Nome do Pool"
    token_amount = "Quantidade de Tokens"
    paired_token = "Token Pareado"
    paired_amount = "Quantidade Pareada"
    slippage_impact = "Impacto de Slippage"
    trade_size = "Tamanho da Transação"
    slippage = "Slippage (%)"
    
    # Trading Strategies
    strategies_text = "Teste diferentes estratégias de trading para seu token."
    strategy_name = "Nome da Estratégia"
    backtest_btn = "Backtesting da Estratégia"
    performance_metrics = "Métricas de Desempenho"
    profit_loss = "Lucro/Prejuízo"
    win_rate = "Taxa de Sucesso"
    roi = "Retorno sobre Investimento (ROI)"
    drawdown = "Drawdown Máximo"
    
    # Technical Indicators
    indicators_text = "Analise indicadores técnicos para prever movimentos de preço."
    indicator_name = "Indicador"
    apply_indicator = "Aplicar Indicador"
    indicator_value = "Valor Atual"
    indicator_signal = "Sinal"
    
    # Market Sentiment
    sentiment_text = "Meça o sentimento do mercado a partir de mídias sociais e fontes de notícias."
    sentiment_score = "Pontuação de Sentimento"
    sentiment_source = "Fonte"
    sentiment_trend = "Tendência de Sentimento"
    
elif st.session_state.language == 'Español':
    # Sections
    market_section = "Datos de Mercado"
    volume_section = "Análisis de Volumen"
    liquidity_section = "Análisis de Liquidez"
    strategies_section = "Estrategias de Trading"
    indicators_section = "Indicadores Técnicos"
    sentiment_section = "Sentimiento de Mercado"
    
    # Market Data
    market_text = "Visualiza y analiza datos históricos de mercado para benchmarking."
    select_token = "Seleccionar Token de Referencia"
    time_period = "Período de Tiempo"
    price_chart = "Gráfico de Precio"
    download_data = "Descargar Datos Históricos"
    
    # Volume Analysis
    volume_text = "Analiza patrones y tendencias de volumen de trading."
    daily_volume = "Volumen Diario de Trading"
    volume_metrics = "Métricas de Volumen"
    avg_daily_volume = "Volumen Diario Promedio"
    volume_trends = "Tendencias de Volumen"
    
    # Liquidity Analysis
    liquidity_text = "Comprende la profundidad de liquidez y el impacto en el mercado."
    liquidity_pools = "Pools de Liquidez"
    add_pool = "Añadir Pool de Liquidez"
    pool_name = "Nombre del Pool"
    token_amount = "Cantidad de Tokens"
    paired_token = "Token Pareado"
    paired_amount = "Cantidad Pareada"
    slippage_impact = "Impacto de Slippage"
    trade_size = "Tamaño de Operación"
    slippage = "Slippage (%)"
    
    # Trading Strategies
    strategies_text = "Prueba diferentes estrategias de trading para tu token."
    strategy_name = "Nombre de Estrategia"
    backtest_btn = "Backtesting de Estrategia"
    performance_metrics = "Métricas de Rendimiento"
    profit_loss = "Beneficio/Pérdida"
    win_rate = "Tasa de Éxito"
    roi = "Retorno de Inversión (ROI)"
    drawdown = "Drawdown Máximo"
    
    # Technical Indicators
    indicators_text = "Analiza indicadores técnicos para predecir movimientos de precio."
    indicator_name = "Indicador"
    apply_indicator = "Aplicar Indicador"
    indicator_value = "Valor Actual"
    indicator_signal = "Señal"
    
    # Market Sentiment
    sentiment_text = "Mide el sentimiento del mercado a partir de redes sociales y fuentes de noticias."
    sentiment_score = "Puntuación de Sentimiento"
    sentiment_source = "Fuente"
    sentiment_trend = "Tendencia de Sentimiento"
    
else:
    # Sections
    market_section = "Market Data"
    volume_section = "Volume Analysis"
    liquidity_section = "Liquidity Analysis"
    strategies_section = "Trading Strategies"
    indicators_section = "Technical Indicators"
    sentiment_section = "Market Sentiment"
    
    # Market Data
    market_text = "View and analyze historical market data for benchmarking."
    select_token = "Select Benchmark Token"
    time_period = "Time Period"
    price_chart = "Price Chart"
    download_data = "Download Historical Data"
    
    # Volume Analysis
    volume_text = "Analyze trading volume patterns and trends."
    daily_volume = "Daily Trading Volume"
    volume_metrics = "Volume Metrics"
    avg_daily_volume = "Average Daily Volume"
    volume_trends = "Volume Trends"
    
    # Liquidity Analysis
    liquidity_text = "Understand liquidity depth and market impact."
    liquidity_pools = "Liquidity Pools"
    add_pool = "Add Liquidity Pool"
    pool_name = "Pool Name"
    token_amount = "Token Amount"
    paired_token = "Paired Token"
    paired_amount = "Paired Amount"
    slippage_impact = "Slippage Impact"
    trade_size = "Trade Size"
    slippage = "Slippage (%)"
    
    # Trading Strategies
    strategies_text = "Test different trading strategies for your token."
    strategy_name = "Strategy Name"
    backtest_btn = "Backtest Strategy"
    performance_metrics = "Performance Metrics"
    profit_loss = "Profit/Loss"
    win_rate = "Win Rate"
    roi = "Return on Investment (ROI)"
    drawdown = "Maximum Drawdown"
    
    # Technical Indicators
    indicators_text = "Analyze technical indicators to predict price movements."
    indicator_name = "Indicator"
    apply_indicator = "Apply Indicator"
    indicator_value = "Current Value"
    indicator_signal = "Signal"
    
    # Market Sentiment
    sentiment_text = "Gauge market sentiment from social media and news sources."
    sentiment_score = "Sentiment Score"
    sentiment_source = "Source"
    sentiment_trend = "Sentiment Trend"

# Initialize session state for crypto trading data
if 'crypto_trading' not in st.session_state:
    st.session_state.crypto_trading = {
        'selected_token': 'BTC',
        'time_period': '1y',
        'liquidity_pools': [
            {
                'name': 'Uniswap v3',
                'token_amount': 100000,
                'paired_token': 'ETH',
                'paired_amount': 50
            },
            {
                'name': 'PancakeSwap',
                'token_amount': 200000,
                'paired_token': 'BNB',
                'paired_amount': 500
            }
        ],
        'trading_strategies': [
            {
                'name': 'Simple Moving Average Crossover',
                'description': 'Buy when short-term SMA crosses above long-term SMA, sell when it crosses below',
                'performance': {
                    'profit_loss': 15.2,
                    'win_rate': 58.5,
                    'roi': 0.32,
                    'drawdown': 12.4
                }
            },
            {
                'name': 'RSI Oversold/Overbought',
                'description': 'Buy when RSI < 30 (oversold), sell when RSI > 70 (overbought)',
                'performance': {
                    'profit_loss': 9.7,
                    'win_rate': 62.3,
                    'roi': 0.21,
                    'drawdown': 8.1
                }
            }
        ],
        'technical_indicators': [
            {
                'name': 'RSI',
                'value': 45.3,
                'signal': 'Neutral'
            },
            {
                'name': 'MACD',
                'value': 0.0024,
                'signal': 'Bullish'
            },
            {
                'name': 'Bollinger Bands',
                'value': 'Middle',
                'signal': 'Neutral'
            }
        ],
        'sentiment_data': [
            {
                'source': 'Twitter',
                'score': 72,
                'signal': 'Bullish'
            },
            {
                'source': 'Reddit',
                'score': 65,
                'signal': 'Bullish'
            },
            {
                'source': 'News Articles',
                'score': 58,
                'signal': 'Neutral'
            }
        ]
    }

# Market Data Section
st.header(market_section)
st.markdown(market_text)

# Token selection and time period
col1, col2 = st.columns(2)

with col1:
    tokens = ['BTC', 'ETH', 'BNB', 'ADA', 'SOL', 'DOT', 'DOGE']
    selected_token = st.selectbox(
        select_token,
        options=tokens,
        index=tokens.index(st.session_state.crypto_trading['selected_token']) if st.session_state.crypto_trading['selected_token'] in tokens else 0
    )
    
    if selected_token != st.session_state.crypto_trading['selected_token']:
        st.session_state.crypto_trading['selected_token'] = selected_token

with col2:
    periods = ['1w', '1m', '3m', '6m', '1y', 'All']
    period_labels = {
        '1w': '1 Week', 
        '1m': '1 Month', 
        '3m': '3 Months', 
        '6m': '6 Months', 
        '1y': '1 Year', 
        'All': 'All Time'
    }
    
    selected_period = st.selectbox(
        time_period,
        options=periods,
        index=periods.index(st.session_state.crypto_trading['time_period']) if st.session_state.crypto_trading['time_period'] in periods else 4,
        format_func=lambda x: period_labels.get(x, x)
    )
    
    if selected_period != st.session_state.crypto_trading['time_period']:
        st.session_state.crypto_trading['time_period'] = selected_period

# Generate historical price data based on selection
def generate_price_data(token, period):
    today = datetime.now()
    
    if period == '1w':
        days = 7
    elif period == '1m':
        days = 30
    elif period == '3m':
        days = 90
    elif period == '6m':
        days = 180
    elif period == '1y':
        days = 365
    else:  # 'All'
        days = 730  # 2 years
    
    dates = [today - timedelta(days=i) for i in range(days)]
    dates.reverse()  # oldest to newest
    
    # Base values for different tokens
    base_values = {
        'BTC': 27000,
        'ETH': 1800,
        'BNB': 220,
        'ADA': 0.30,
        'SOL': 20,
        'DOT': 4.5,
        'DOGE': 0.07
    }
    
    base_value = base_values.get(token, 100)
    
    # Generate realistic price data with trends, noise, and some volatility
    price = base_value
    prices = []
    volumes = []
    
    for i in range(len(dates)):
        # Add trend
        trend = np.sin(i / 50) * 0.01
        
        # Add some random daily movement
        daily_change = np.random.normal(0, 0.02)
        
        # Add some momentum (previous changes affect future changes)
        momentum = 0
        if i > 0:
            momentum = (prices[-1] / prices[0] - 1) * 0.001
        
        # Calculate new price
        price = price * (1 + trend + daily_change + momentum)
        prices.append(price)
        
        # Generate volume data (correlated with price changes but with some randomness)
        volume_base = abs(daily_change) * base_value * 1000000  # Higher volume on bigger price moves
        volume = volume_base * (1 + np.random.normal(0, 0.5))  # Add noise
        volumes.append(max(0, volume))  # Ensure non-negative
    
    return pd.DataFrame({
        'Date': dates,
        'Price': prices,
        'Volume': volumes
    })

# Generate and display price chart
price_data = generate_price_data(selected_token, selected_period)

st.subheader(f"{selected_token} {price_chart} ({period_labels[selected_period]})")

# Create candlestick chart (for simplicity, we'll use a line chart with slider instead)
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=price_data['Date'], 
    y=price_data['Price'],
    mode='lines',
    name=selected_token
))

fig.update_layout(
    xaxis_title="Date",
    yaxis_title=f"Price (USD)",
    height=500,
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=7, label="1w", step="day", stepmode="backward"),
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=3, label="3m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(visible=True),
        type="date"
    )
)

st.plotly_chart(fig, use_container_width=True)

# Option to download data
if st.download_button(
    label=download_data,
    data=price_data.to_csv(index=False).encode('utf-8'),
    file_name=f"{selected_token}_price_data_{selected_period}.csv",
    mime="text/csv"
):
    st.success(f"Downloaded {selected_token} price data for {period_labels[selected_period]}")

# Volume Analysis Section
st.header(volume_section)
st.markdown(volume_text)

# Display volume chart
st.subheader(f"{selected_token} {daily_volume} ({period_labels[selected_period]})")

fig = go.Figure()
fig.add_trace(go.Bar(
    x=price_data['Date'],
    y=price_data['Volume'],
    name=daily_volume,
    marker_color='rgba(58, 71, 80, 0.6)'
))

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Volume (USD)",
    height=400
)

st.plotly_chart(fig, use_container_width=True)

# Volume metrics
avg_volume = price_data['Volume'].mean()
max_volume = price_data['Volume'].max()
min_volume = price_data['Volume'].min()
std_volume = price_data['Volume'].std()

vol_col1, vol_col2, vol_col3, vol_col4 = st.columns(4)

with vol_col1:
    st.metric(avg_daily_volume, f"${avg_volume:,.2f}")

with vol_col2:
    st.metric("Max Volume", f"${max_volume:,.2f}")

with vol_col3:
    st.metric("Min Volume", f"${min_volume:,.2f}")

with vol_col4:
    st.metric("Volume Volatility", f"${std_volume:,.2f}")

# Volume trends over the period
st.subheader(volume_trends)

# Calculate 7-day moving average
if len(price_data) > 7:
    price_data['MA7_Volume'] = price_data['Volume'].rolling(window=7).mean()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=price_data['Date'],
        y=price_data['Volume'],
        name=daily_volume,
        marker_color='rgba(58, 71, 80, 0.6)'
    ))
    fig.add_trace(go.Scatter(
        x=price_data['Date'],
        y=price_data['MA7_Volume'],
        name="7-Day Moving Average",
        line=dict(color='firebrick', width=2)
    ))

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Volume (USD)",
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Need at least 7 days of data to calculate volume moving average")

# Liquidity Analysis Section
st.header(liquidity_section)
st.markdown(liquidity_text)

# Display existing liquidity pools
if st.session_state.crypto_trading['liquidity_pools']:
    st.subheader(liquidity_pools)
    
    pool_data = pd.DataFrame(st.session_state.crypto_trading['liquidity_pools'])
    
    # Calculate total value
    token_price = price_data['Price'].iloc[-1]  # Use latest price from generated data
    
    # Simplified paired token prices
    paired_prices = {
        'ETH': 1800,
        'BNB': 220,
        'USDT': 1,
        'USDC': 1,
        'DAI': 1
    }
    
    # Calculate total USD value for each pool
    pool_data['Token Value (USD)'] = pool_data['token_amount'] * token_price
    pool_data['Paired Value (USD)'] = pool_data.apply(
        lambda row: row['paired_amount'] * paired_prices.get(row['paired_token'], 1), 
        axis=1
    )
    pool_data['Total Value (USD)'] = pool_data['Token Value (USD)'] + pool_data['Paired Value (USD)']
    
    # Display as a pie chart of TVL by pool
    fig = px.pie(
        pool_data,
        values='Total Value (USD)',
        names='name',
        title="Total Value Locked (TVL) by Liquidity Pool",
        hover_data=['token_amount', 'paired_token', 'paired_amount']
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display pool data in a table
    display_pools = pool_data.copy()
    display_pools.columns = ['Pool', 'Token Amount', 'Paired Token', 'Paired Amount', 
                            'Token Value (USD)', 'Paired Value (USD)', 'Total Value (USD)']
    
    # Format for display
    display_pools['Token Amount'] = display_pools['Token Amount'].apply(lambda x: f"{x:,}")
    display_pools['Paired Amount'] = display_pools['Paired Amount'].apply(lambda x: f"{x:,}")
    display_pools['Token Value (USD)'] = display_pools['Token Value (USD)'].apply(lambda x: f"${x:,.2f}")
    display_pools['Paired Value (USD)'] = display_pools['Paired Value (USD)'].apply(lambda x: f"${x:,.2f}")
    display_pools['Total Value (USD)'] = display_pools['Total Value (USD)'].apply(lambda x: f"${x:,.2f}")
    
    st.table(display_pools[['Pool', 'Token Amount', 'Paired Token', 'Paired Amount', 'Total Value (USD)']])

# Add new liquidity pool
with st.expander(add_pool):
    liq_col1, liq_col2 = st.columns(2)
    
    with liq_col1:
        new_pool_name = st.text_input(pool_name)
        new_token_amount = st.number_input(
            token_amount,
            min_value=0,
            value=10000,
            step=1000
        )
    
    with liq_col2:
        paired_options = ['ETH', 'BNB', 'USDT', 'USDC', 'DAI']
        new_paired_token = st.selectbox(paired_token, options=paired_options)
        new_paired_amount = st.number_input(
            paired_amount,
            min_value=0.0,
            value=10.0,
            step=1.0
        )
    
    if st.button(add_pool):
        if new_pool_name:  # Only add if pool has a name
            st.session_state.crypto_trading['liquidity_pools'].append({
                'name': new_pool_name,
                'token_amount': new_token_amount,
                'paired_token': new_paired_token,
                'paired_amount': new_paired_amount
            })
            st.success(f"Added {new_pool_name} to liquidity pools")

# Slippage impact analysis
st.subheader(slippage_impact)

if st.session_state.crypto_trading['liquidity_pools']:
    # Create sliders for analyzing slippage
    slip_col1, slip_col2 = st.columns(2)
    
    with slip_col1:
        selected_pool = st.selectbox(
            "Select Liquidity Pool",
            options=[pool['name'] for pool in st.session_state.crypto_trading['liquidity_pools']]
        )
    
    with slip_col2:
        trade_size_value = st.slider(
            trade_size,
            min_value=100,
            max_value=100000,
            value=10000,
            step=100
        )
    
    # Find the selected pool
    selected_pool_data = next((p for p in st.session_state.crypto_trading['liquidity_pools'] if p['name'] == selected_pool), None)
    
    if selected_pool_data:
        # Calculate slippage (simplified version using constant product formula)
        token_amount = selected_pool_data['token_amount']
        paired_amount = selected_pool_data['paired_amount']
        
        # Constant product k = x * y
        k = token_amount * paired_amount
        
        # New amount after trade (assuming selling tokens)
        new_token_amount = token_amount + trade_size_value
        new_paired_amount = k / new_token_amount
        
        # Calculate tokens received and slippage
        tokens_out = paired_amount - new_paired_amount
        no_slip_price = paired_amount / token_amount
        actual_price = tokens_out / trade_size_value
        
        # Slippage percentage
        slip_percentage = (1 - actual_price / no_slip_price) * 100
        
        # Display results
        st.subheader(f"{slippage} Analysis for {selected_pool}")
        
        slip_metrics_col1, slip_metrics_col2, slip_metrics_col3 = st.columns(3)
        
        with slip_metrics_col1:
            st.metric("No Slippage Price", f"{no_slip_price:.6f} {selected_pool_data['paired_token']}")
        
        with slip_metrics_col2:
            st.metric("Actual Execution Price", f"{actual_price:.6f} {selected_pool_data['paired_token']}")
        
        with slip_metrics_col3:
            st.metric(slippage, f"{slip_percentage:.2f}%", delta=-slip_percentage, delta_color="inverse")
        
        # Generate slippage curve for different trade sizes
        trade_sizes = np.linspace(100, 100000, 100)
        slippages = []
        
        for size in trade_sizes:
            new_amount = token_amount + size
            new_paired = k / new_amount
            tokens_received = paired_amount - new_paired
            actual_price_point = tokens_received / size
            slippages.append((1 - actual_price_point / no_slip_price) * 100)
        
        slip_data = pd.DataFrame({
            trade_size: trade_sizes,
            slippage: slippages
        })
        
        fig = px.line(
            slip_data,
            x=trade_size,
            y=slippage,
            title=f"{slippage} Curve for {selected_pool}",
            labels={trade_size: f"{trade_size} ({st.session_state.tokenomics_data.get('token_symbol', 'Token')})", slippage: f"{slippage} (%)"}
        )
        
        # Add marker for the current trade size
        fig.add_trace(go.Scatter(
            x=[trade_size_value],
            y=[slip_percentage],
            mode='markers',
            marker=dict(color='red', size=10),
            name=f"Current {trade_size}"
        ))
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info(f"No liquidity pools added yet. Use the '{add_pool}' section to add pools.")

# Trading Strategies Section
st.header(strategies_section)
st.markdown(strategies_text)

# Display existing trading strategies
if st.session_state.crypto_trading['trading_strategies']:
    strategy_tabs = st.tabs([strategy['name'] for strategy in st.session_state.crypto_trading['trading_strategies']])
    
    for i, tab in enumerate(strategy_tabs):
        strategy = st.session_state.crypto_trading['trading_strategies'][i]
        
        with tab:
            st.write(f"**Description:** {strategy['description']}")
            
            st.subheader(performance_metrics)
            
            metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
            
            with metrics_col1:
                st.metric(
                    profit_loss, 
                    f"{strategy['performance']['profit_loss']}%",
                    delta=f"{strategy['performance']['profit_loss']:.1f}%" if strategy['performance']['profit_loss'] > 0 else f"{strategy['performance']['profit_loss']:.1f}%"
                )
            
            with metrics_col2:
                st.metric(win_rate, f"{strategy['performance']['win_rate']}%")
            
            with metrics_col3:
                st.metric(
                    roi, 
                    f"{strategy['performance']['roi'] * 100:.1f}%",
                    delta=f"{strategy['performance']['roi'] * 100:.1f}%" if strategy['performance']['roi'] > 0 else f"{strategy['performance']['roi'] * 100:.1f}%"
                )
            
            with metrics_col4:
                st.metric(drawdown, f"{strategy['performance']['drawdown']}%", delta=f"-{strategy['performance']['drawdown']:.1f}%", delta_color="inverse")
            
            # Simulate strategy performance on selected token
            if st.button(f"{backtest_btn} on {selected_token}", key=f"backtest_{i}"):
                # Generate random trading signals based on strategy
                signals = np.random.choice(['Buy', 'Sell', 'Hold'], size=len(price_data), p=[0.2, 0.2, 0.6])
                price_data['Signal'] = signals
                
                # Mark buy and sell points on chart
                buy_points = price_data[price_data['Signal'] == 'Buy']
                sell_points = price_data[price_data['Signal'] == 'Sell']
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=price_data['Date'], 
                    y=price_data['Price'],
                    mode='lines',
                    name=selected_token
                ))
                
                fig.add_trace(go.Scatter(
                    x=buy_points['Date'],
                    y=buy_points['Price'],
                    mode='markers',
                    marker=dict(color='green', size=10, symbol='triangle-up'),
                    name='Buy Signal'
                ))
                
                fig.add_trace(go.Scatter(
                    x=sell_points['Date'],
                    y=sell_points['Price'],
                    mode='markers',
                    marker=dict(color='red', size=10, symbol='triangle-down'),
                    name='Sell Signal'
                ))
                
                fig.update_layout(
                    title=f"{strategy['name']} Backtest on {selected_token}",
                    xaxis_title="Date",
                    yaxis_title=f"Price (USD)",
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Calculate simulated performance
                if len(buy_points) > 0 and len(sell_points) > 0:
                    buy_prices = buy_points['Price'].tolist()
                    sell_prices = sell_points['Price'].tolist()
                    
                    # Pair buys with sells
                    trades = []
                    buy_index = 0
                    
                    for i, row in sell_points.iterrows():
                        sell_date = row['Date']
                        sell_price = row['Price']
                        
                        # Find the most recent buy before this sell
                        valid_buys = buy_points[buy_points['Date'] < sell_date]
                        
                        if not valid_buys.empty:
                            last_buy = valid_buys.iloc[-1]
                            buy_date = last_buy['Date']
                            buy_price = last_buy['Price']
                            
                            profit_pct = (sell_price - buy_price) / buy_price * 100
                            trades.append({
                                'Buy Date': buy_date,
                                'Buy Price': buy_price,
                                'Sell Date': sell_date,
                                'Sell Price': sell_price,
                                'Profit (%)': profit_pct
                            })
                    
                    if trades:
                        trades_df = pd.DataFrame(trades)
                        
                        # Calculate performance metrics
                        total_profit = trades_df['Profit (%)'].sum()
                        winning_trades = len(trades_df[trades_df['Profit (%)'] > 0])
                        total_trades = len(trades_df)
                        win_rate_calc = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
                        
                        st.subheader("Backtest Results")
                        
                        result_col1, result_col2, result_col3 = st.columns(3)
                        
                        with result_col1:
                            st.metric("Total Profit/Loss", f"{total_profit:.2f}%")
                        
                        with result_col2:
                            st.metric("Win Rate", f"{win_rate_calc:.1f}%")
                        
                        with result_col3:
                            st.metric("Number of Trades", f"{total_trades}")
                        
                        # Show trade details
                        st.subheader("Trade Details")
                        
                        display_trades = trades_df.copy()
                        display_trades['Buy Price'] = display_trades['Buy Price'].apply(lambda x: f"${x:.2f}")
                        display_trades['Sell Price'] = display_trades['Sell Price'].apply(lambda x: f"${x:.2f}")
                        display_trades['Profit (%)'] = display_trades['Profit (%)'].apply(lambda x: f"{x:.2f}%")
                        
                        st.table(display_trades)
                    else:
                        st.info("Not enough valid trades to analyze. Try a different time period.")
                else:
                    st.info("Not enough buy/sell signals in the selected time period.")

# Add new trading strategy
with st.expander("Add Trading Strategy"):
    new_strategy_name = st.text_input("Strategy Name")
    new_strategy_desc = st.text_area("Strategy Description")
    
    if st.button("Add Strategy"):
        if new_strategy_name and new_strategy_desc:
            # Generate random initial performance metrics
            new_strategy = {
                'name': new_strategy_name,
                'description': new_strategy_desc,
                'performance': {
                    'profit_loss': round(np.random.normal(10, 5), 1),
                    'win_rate': round(np.random.normal(55, 10), 1),
                    'roi': round(np.random.normal(0.2, 0.1), 2),
                    'drawdown': round(np.random.normal(10, 3), 1)
                }
            }
            
            st.session_state.crypto_trading['trading_strategies'].append(new_strategy)
            st.success(f"Added {new_strategy_name} to trading strategies")

# Technical Indicators Section
st.header(indicators_section)
st.markdown(indicators_text)

# Select and apply technical indicators
indicators = [
    'Simple Moving Average (SMA)',
    'Exponential Moving Average (EMA)',
    'Relative Strength Index (RSI)',
    'Moving Average Convergence Divergence (MACD)',
    'Bollinger Bands',
    'Stochastic Oscillator',
    'Average Directional Index (ADX)'
]

selected_indicators = st.multiselect(
    "Select Technical Indicators",
    options=indicators,
    default=['Simple Moving Average (SMA)', 'Relative Strength Index (RSI)']
)

if selected_indicators and st.button(apply_indicator):
    # Calculate and display selected indicators
    if 'Simple Moving Average (SMA)' in selected_indicators:
        # Calculate 20-day and 50-day SMAs
        if len(price_data) >= 50:
            price_data['SMA20'] = price_data['Price'].rolling(window=20).mean()
            price_data['SMA50'] = price_data['Price'].rolling(window=50).mean()
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=price_data['Date'], 
                y=price_data['Price'],
                mode='lines',
                name=selected_token
            ))
            fig.add_trace(go.Scatter(
                x=price_data['Date'],
                y=price_data['SMA20'],
                mode='lines',
                line=dict(width=2, color='blue'),
                name='20-Day SMA'
            ))
            fig.add_trace(go.Scatter(
                x=price_data['Date'],
                y=price_data['SMA50'],
                mode='lines',
                line=dict(width=2, color='red'),
                name='50-Day SMA'
            ))
            
            fig.update_layout(
                title=f"Simple Moving Average (SMA) for {selected_token}",
                xaxis_title="Date",
                yaxis_title=f"Price (USD)",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Determine signal
            last_sma20 = price_data['SMA20'].iloc[-1]
            last_sma50 = price_data['SMA50'].iloc[-1]
            
            if last_sma20 > last_sma50:
                signal = "Bullish"
            elif last_sma20 < last_sma50:
                signal = "Bearish"
            else:
                signal = "Neutral"
            
            st.metric(
                "SMA Signal",
                signal,
                delta="SMA20 > SMA50" if signal == "Bullish" else "SMA20 < SMA50" if signal == "Bearish" else "SMA20 = SMA50"
            )
        else:
            st.info("Need at least 50 days of data for SMA calculation")
    
    if 'Relative Strength Index (RSI)' in selected_indicators:
        # Calculate RSI
        if len(price_data) >= 14:
            # Calculate price changes
            price_data['Price Change'] = price_data['Price'].diff()
            
            # Get gains and losses
            price_data['Gain'] = price_data['Price Change'].apply(lambda x: x if x > 0 else 0)
            price_data['Loss'] = price_data['Price Change'].apply(lambda x: abs(x) if x < 0 else 0)
            
            # Calculate average gain and loss over 14 periods
            price_data['Avg Gain'] = price_data['Gain'].rolling(window=14).mean()
            price_data['Avg Loss'] = price_data['Loss'].rolling(window=14).mean()
            
            # Calculate Relative Strength (RS) and RSI
            price_data['RS'] = price_data['Avg Gain'] / price_data['Avg Loss']
            price_data['RSI'] = 100 - (100 / (1 + price_data['RS']))
            
            # Create RSI chart
            fig = make_subplots(
                rows=2, 
                cols=1, 
                shared_xaxes=True,
                vertical_spacing=0.1,
                subplot_titles=(f"{selected_token} Price", "RSI (14)")
            )
            
            fig.add_trace(
                go.Scatter(
                    x=price_data['Date'], 
                    y=price_data['Price'],
                    mode='lines',
                    name=selected_token
                ),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=price_data['Date'],
                    y=price_data['RSI'],
                    mode='lines',
                    line=dict(color='purple', width=1),
                    name='RSI (14)'
                ),
                row=2, col=1
            )
            
            # Add overbought/oversold lines
            fig.add_trace(
                go.Scatter(
                    x=[price_data['Date'].iloc[0], price_data['Date'].iloc[-1]],
                    y=[70, 70],
                    mode='lines',
                    line=dict(color='red', width=1, dash='dash'),
                    name='Overbought (70)'
                ),
                row=2, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=[price_data['Date'].iloc[0], price_data['Date'].iloc[-1]],
                    y=[30, 30],
                    mode='lines',
                    line=dict(color='green', width=1, dash='dash'),
                    name='Oversold (30)'
                ),
                row=2, col=1
            )
            
            fig.update_layout(
                title=f"Relative Strength Index (RSI) for {selected_token}",
                height=600
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Determine signal
            last_rsi = price_data['RSI'].iloc[-1]
            
            if last_rsi > 70:
                signal = "Bearish (Overbought)"
                delta_text = f"RSI: {last_rsi:.1f} > 70 (Overbought)"
            elif last_rsi < 30:
                signal = "Bullish (Oversold)"
                delta_text = f"RSI: {last_rsi:.1f} < 30 (Oversold)"
            else:
                signal = "Neutral"
                delta_text = f"RSI: {last_rsi:.1f}"
            
            st.metric("RSI Signal", signal, delta=delta_text)
        else:
            st.info("Need at least 14 days of data for RSI calculation")

# Display current technical indicator values
if st.session_state.crypto_trading['technical_indicators']:
    st.subheader("Current Technical Indicator Values")
    
    indicators_df = pd.DataFrame(st.session_state.crypto_trading['technical_indicators'])
    
    # Format the dataframe for display
    indicators_df.columns = [indicator_name, indicator_value, indicator_signal]
    
    # Apply color to signal column
    def color_signal(val):
        if 'Bullish' in val:
            return 'background-color: rgba(0, 128, 0, 0.2)'
        elif 'Bearish' in val:
            return 'background-color: rgba(255, 0, 0, 0.2)'
        else:
            return ''
    
    styled_indicators = indicators_df.style.applymap(color_signal, subset=[indicator_signal])
    
    st.table(styled_indicators)

# Market Sentiment Section
st.header(sentiment_section)
st.markdown(sentiment_text)

# Display sentiment data if available
if st.session_state.crypto_trading['sentiment_data']:
    sentiment_df = pd.DataFrame(st.session_state.crypto_trading['sentiment_data'])
    
    # Create a gauge chart for sentiment score
    fig = go.Figure()
    
    for i, row in sentiment_df.iterrows():
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=row['score'],
            title={"text": row['source']},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': 'darkblue'},
                'steps': [
                    {'range': [0, 25], 'color': 'red'},
                    {'range': [25, 45], 'color': 'orange'},
                    {'range': [45, 55], 'color': 'yellow'},
                    {'range': [55, 75], 'color': 'lightgreen'},
                    {'range': [75, 100], 'color': 'green'}
                ],
                'threshold': {
                    'line': {'color': 'black', 'width': 4},
                    'thickness': 0.75,
                    'value': row['score']
                }
            },
            domain={'row': 0, 'column': i}
        ))
    
    fig.update_layout(
        grid={'rows': 1, 'columns': len(sentiment_df), 'pattern': "independent"},
        title=sentiment_score,
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Format sentiment data for display
    display_sentiment = sentiment_df.copy()
    display_sentiment.columns = [sentiment_source, sentiment_score, indicator_signal]
    
    # Apply color to signal column
    def color_signal(val):
        if 'Bullish' in val:
            return 'background-color: rgba(0, 128, 0, 0.2)'
        elif 'Bearish' in val:
            return 'background-color: rgba(255, 0, 0, 0.2)'
        else:
            return ''
    
    styled_sentiment = display_sentiment.style.applymap(color_signal, subset=[indicator_signal])
    
    st.table(styled_sentiment)
    
    # Generate simulated sentiment trend data
    days = 30
    trend_dates = [datetime.now() - timedelta(days=i) for i in range(days)]
    trend_dates.reverse()
    
    sentiment_trends = []
    
    for source in sentiment_df['source']:
        # Generate a realistic trend with some noise
        baseline = 50  # Neutral sentiment
        trend = []
        
        for i in range(days):
            # Add trend component
            trend_component = np.sin(i / 10) * 10
            
            # Add noise
            noise = np.random.normal(0, 5)
            
            # Calculate sentiment value
            value = baseline + trend_component + noise
            value = max(0, min(100, value))  # Clamp between 0 and 100
            
            trend.append(value)
        
        sentiment_trends.append({
            'source': source,
            'trend': trend
        })
    
    # Plot sentiment trends
    st.subheader(sentiment_trend)
    
    fig = go.Figure()
    
    for trend_data in sentiment_trends:
        fig.add_trace(go.Scatter(
            x=trend_dates,
            y=trend_data['trend'],
            mode='lines',
            name=trend_data['source']
        ))
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title=sentiment_score,
        height=400,
        yaxis=dict(range=[0, 100])
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Calculate overall sentiment
    avg_sentiment = sentiment_df['score'].mean()
    
    if avg_sentiment > 70:
        overall_signal = "Very Bullish"
    elif avg_sentiment > 55:
        overall_signal = "Bullish"
    elif avg_sentiment > 45:
        overall_signal = "Neutral"
    elif avg_sentiment > 30:
        overall_signal = "Bearish"
    else:
        overall_signal = "Very Bearish"
    
    st.metric(
        "Overall Market Sentiment",
        overall_signal,
        delta=f"Score: {avg_sentiment:.1f}/100"
    )

# Footer
st.markdown("---")
st.markdown("TokenomicsLab - Crypto Trading Analysis Module")