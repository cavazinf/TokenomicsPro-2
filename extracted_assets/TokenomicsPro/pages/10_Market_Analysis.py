import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Set page configuration
st.set_page_config(
    page_title="Market Analysis - TokenomicsLab",
    page_icon="📊",
    layout="wide",
)

# Initialize language if not set
if 'language' not in st.session_state:
    st.session_state.language = 'English'

# Page title and description based on language
if st.session_state.language == 'English':
    title = "Market Analysis"
    description = """
    Analyze market trends, competitive landscape, and potential market scenarios for your token.
    """
elif st.session_state.language == 'Português':
    title = "Análise de Mercado"
    description = """
    Analise tendências de mercado, cenário competitivo e potenciais cenários de mercado para o seu token.
    """
elif st.session_state.language == 'Español':
    title = "Análisis de Mercado"
    description = """
    Analiza tendencias del mercado, panorama competitivo y posibles escenarios de mercado para tu token.
    """
else:
    title = "Market Analysis"
    description = """
    Analyze market trends, competitive landscape, and potential market scenarios for your token.
    """

st.title(title)
st.markdown(description)

# Define multi-language labels and texts
if st.session_state.language == 'English':
    market_section = "Market Overview"
    market_trends_section = "Market Trends"
    competitor_section = "Competitive Analysis"
    market_sizing_section = "Market Sizing"
    scenario_section = "Market Scenarios"
    
    # Market Overview labels
    overview_text = "Analyze the overall cryptocurrency market conditions and how they might affect your token."
    total_mcap_label = "Total Crypto Market Cap (USD)"
    btc_dom_label = "Bitcoin Dominance (%)"
    market_sentiment_label = "Market Sentiment"
    
    # Market Trends labels
    trends_text = "Identify key market trends that could impact your token's performance."
    trend_1 = "DeFi TVL Growth"
    trend_2 = "NFT Market Volume"
    trend_3 = "Layer 2 Solutions Adoption"
    trend_4 = "Web3 Developer Activity"
    
    # Competitor Analysis labels
    competitor_text = "Compare your token to similar projects in the market."
    add_competitor_btn = "Add Competitor"
    competitor_name = "Competitor Name"
    competitor_mcap = "Market Cap (USD)"
    competitor_price = "Token Price (USD)"
    competitor_supply = "Circulating Supply"
    competitor_holders = "Number of Holders"
    comparison_chart = "Comparison Chart"
    competitor_table = "Competitor Data"
    
    # Market Sizing labels
    market_size_text = "Estimate the potential market size for your token."
    tam_label = "Total Addressable Market (TAM)"
    sam_label = "Serviceable Available Market (SAM)"
    som_label = "Serviceable Obtainable Market (SOM)"
    tam_tooltip = "The total market demand for your token's category"
    sam_tooltip = "The segment of TAM that your token can realistically target"
    som_tooltip = "The portion of SAM that your token can capture"
    calculate_btn = "Calculate Market Size Estimates"
    
    # Market Scenarios labels
    scenario_text = "Model different market scenarios based on varying conditions."
    bull_label = "Bull Market Scenario"
    base_label = "Base Case Scenario"
    bear_label = "Bear Market Scenario"
    scenario_chart = "Market Scenario Comparison"
    scenario_params = "Scenario Parameters"
    
elif st.session_state.language == 'Português':
    market_section = "Visão Geral do Mercado"
    market_trends_section = "Tendências de Mercado"
    competitor_section = "Análise Competitiva"
    market_sizing_section = "Dimensionamento de Mercado"
    scenario_section = "Cenários de Mercado"
    
    # Market Overview labels
    overview_text = "Analise as condições gerais do mercado de criptomoedas e como elas podem afetar seu token."
    total_mcap_label = "Capitalização Total do Mercado Cripto (USD)"
    btc_dom_label = "Dominância do Bitcoin (%)"
    market_sentiment_label = "Sentimento do Mercado"
    
    # Market Trends labels
    trends_text = "Identifique tendências-chave do mercado que podem impactar o desempenho do seu token."
    trend_1 = "Crescimento do TVL em DeFi"
    trend_2 = "Volume do Mercado de NFTs"
    trend_3 = "Adoção de Soluções Layer 2"
    trend_4 = "Atividade de Desenvolvedores Web3"
    
    # Competitor Analysis labels
    competitor_text = "Compare seu token com projetos similares no mercado."
    add_competitor_btn = "Adicionar Concorrente"
    competitor_name = "Nome do Concorrente"
    competitor_mcap = "Cap. de Mercado (USD)"
    competitor_price = "Preço do Token (USD)"
    competitor_supply = "Oferta Circulante"
    competitor_holders = "Número de Detentores"
    comparison_chart = "Gráfico Comparativo"
    competitor_table = "Dados dos Concorrentes"
    
    # Market Sizing labels
    market_size_text = "Estime o tamanho potencial do mercado para seu token."
    tam_label = "Mercado Total Endereçável (TAM)"
    sam_label = "Mercado Disponível Atendível (SAM)"
    som_label = "Mercado Obtenível Atendível (SOM)"
    tam_tooltip = "A demanda total do mercado para a categoria do seu token"
    sam_tooltip = "O segmento do TAM que seu token pode realisticamente atingir"
    som_tooltip = "A porção do SAM que seu token pode capturar"
    calculate_btn = "Calcular Estimativas de Tamanho de Mercado"
    
    # Market Scenarios labels
    scenario_text = "Modele diferentes cenários de mercado com base em condições variadas."
    bull_label = "Cenário de Mercado em Alta"
    base_label = "Cenário Base"
    bear_label = "Cenário de Mercado em Baixa"
    scenario_chart = "Comparação de Cenários de Mercado"
    scenario_params = "Parâmetros de Cenário"
    
elif st.session_state.language == 'Español':
    market_section = "Visión General del Mercado"
    market_trends_section = "Tendencias del Mercado"
    competitor_section = "Análisis Competitivo"
    market_sizing_section = "Dimensionamiento del Mercado"
    scenario_section = "Escenarios de Mercado"
    
    # Market Overview labels
    overview_text = "Analiza las condiciones generales del mercado de criptomonedas y cómo podrían afectar a tu token."
    total_mcap_label = "Capitalización Total del Mercado Cripto (USD)"
    btc_dom_label = "Dominancia de Bitcoin (%)"
    market_sentiment_label = "Sentimiento del Mercado"
    
    # Market Trends labels
    trends_text = "Identifica tendencias clave del mercado que podrían impactar el rendimiento de tu token."
    trend_1 = "Crecimiento de TVL en DeFi"
    trend_2 = "Volumen del Mercado de NFTs"
    trend_3 = "Adopción de Soluciones Layer 2"
    trend_4 = "Actividad de Desarrolladores Web3"
    
    # Competitor Analysis labels
    competitor_text = "Compara tu token con proyectos similares en el mercado."
    add_competitor_btn = "Añadir Competidor"
    competitor_name = "Nombre del Competidor"
    competitor_mcap = "Cap. de Mercado (USD)"
    competitor_price = "Precio del Token (USD)"
    competitor_supply = "Suministro Circulante"
    competitor_holders = "Número de Poseedores"
    comparison_chart = "Gráfico Comparativo"
    competitor_table = "Datos de Competidores"
    
    # Market Sizing labels
    market_size_text = "Estima el tamaño potencial del mercado para tu token."
    tam_label = "Mercado Total Direccionable (TAM)"
    sam_label = "Mercado Disponible Abordable (SAM)"
    som_label = "Mercado Obtenible Abordable (SOM)"
    tam_tooltip = "La demanda total del mercado para la categoría de tu token"
    sam_tooltip = "El segmento del TAM que tu token puede alcanzar de manera realista"
    som_tooltip = "La porción del SAM que tu token puede capturar"
    calculate_btn = "Calcular Estimaciones del Tamaño del Mercado"
    
    # Market Scenarios labels
    scenario_text = "Modela diferentes escenarios de mercado basados en condiciones variables."
    bull_label = "Escenario de Mercado Alcista"
    base_label = "Escenario Base"
    bear_label = "Escenario de Mercado Bajista"
    scenario_chart = "Comparación de Escenarios de Mercado"
    scenario_params = "Parámetros de Escenario"
    
else:
    market_section = "Market Overview"
    market_trends_section = "Market Trends"
    competitor_section = "Competitive Analysis"
    market_sizing_section = "Market Sizing"
    scenario_section = "Market Scenarios"
    
    # Market Overview labels
    overview_text = "Analyze the overall cryptocurrency market conditions and how they might affect your token."
    total_mcap_label = "Total Crypto Market Cap (USD)"
    btc_dom_label = "Bitcoin Dominance (%)"
    market_sentiment_label = "Market Sentiment"
    
    # Market Trends labels
    trends_text = "Identify key market trends that could impact your token's performance."
    trend_1 = "DeFi TVL Growth"
    trend_2 = "NFT Market Volume"
    trend_3 = "Layer 2 Solutions Adoption"
    trend_4 = "Web3 Developer Activity"
    
    # Competitor Analysis labels
    competitor_text = "Compare your token to similar projects in the market."
    add_competitor_btn = "Add Competitor"
    competitor_name = "Competitor Name"
    competitor_mcap = "Market Cap (USD)"
    competitor_price = "Token Price (USD)"
    competitor_supply = "Circulating Supply"
    competitor_holders = "Number of Holders"
    comparison_chart = "Comparison Chart"
    competitor_table = "Competitor Data"
    
    # Market Sizing labels
    market_size_text = "Estimate the potential market size for your token."
    tam_label = "Total Addressable Market (TAM)"
    sam_label = "Serviceable Available Market (SAM)"
    som_label = "Serviceable Obtainable Market (SOM)"
    tam_tooltip = "The total market demand for your token's category"
    sam_tooltip = "The segment of TAM that your token can realistically target"
    som_tooltip = "The portion of SAM that your token can capture"
    calculate_btn = "Calculate Market Size Estimates"
    
    # Market Scenarios labels
    scenario_text = "Model different market scenarios based on varying conditions."
    bull_label = "Bull Market Scenario"
    base_label = "Base Case Scenario"
    bear_label = "Bear Market Scenario"
    scenario_chart = "Market Scenario Comparison"
    scenario_params = "Scenario Parameters"

# Initialize session state for market analysis data
if 'market_analysis' not in st.session_state:
    st.session_state.market_analysis = {
        'total_market_cap': 1200000000000,  # $1.2T
        'btc_dominance': 45.5,
        'market_sentiment': 'Neutral',
        'competitors': [],
        'tam': 100000000000,  # $100B
        'sam': 20000000000,   # $20B
        'som': 1000000000,    # $1B
        'scenarios': {
            'bull': {
                'growth_rate': 150,  # 150%
                'market_share': 5.0,
                'adoption_rate': 75.0
            },
            'base': {
                'growth_rate': 50,   # 50%
                'market_share': 2.0,
                'adoption_rate': 40.0
            },
            'bear': {
                'growth_rate': -20,  # -20%
                'market_share': 0.5,
                'adoption_rate': 15.0
            }
        }
    }

# Market Overview Section
st.header(market_section)
st.markdown(overview_text)

col1, col2, col3 = st.columns(3)

with col1:
    market_cap = st.number_input(
        total_mcap_label,
        min_value=0,
        value=st.session_state.market_analysis['total_market_cap'],
        step=10000000000,
        format="%d"
    )
    if market_cap != st.session_state.market_analysis['total_market_cap']:
        st.session_state.market_analysis['total_market_cap'] = market_cap

with col2:
    btc_dom = st.number_input(
        btc_dom_label,
        min_value=0.0,
        max_value=100.0,
        value=st.session_state.market_analysis['btc_dominance'],
        step=0.1,
        format="%.1f"
    )
    if btc_dom != st.session_state.market_analysis['btc_dominance']:
        st.session_state.market_analysis['btc_dominance'] = btc_dom

with col3:
    sentiment_options = ['Very Bearish', 'Bearish', 'Neutral', 'Bullish', 'Very Bullish']
    sent_index = sentiment_options.index(st.session_state.market_analysis['market_sentiment']) if st.session_state.market_analysis['market_sentiment'] in sentiment_options else 2
    
    sentiment = st.selectbox(
        market_sentiment_label,
        options=sentiment_options,
        index=sent_index
    )
    if sentiment != st.session_state.market_analysis['market_sentiment']:
        st.session_state.market_analysis['market_sentiment'] = sentiment

# Create a visual representation of market conditions
fig = go.Figure()

# Add market cap data
fig.add_trace(go.Indicator(
    mode="number",
    value=market_cap,
    number={'prefix': "$", 'suffix': "", 'valueformat': '.3s'},
    title={"text": total_mcap_label},
    domain={'row': 0, 'column': 0}
))

# Add Bitcoin dominance gauge
fig.add_trace(go.Indicator(
    mode="gauge+number",
    value=btc_dom,
    title={"text": btc_dom_label},
    gauge={
        'axis': {'range': [None, 100]},
        'bar': {'color': 'orange'},
        'steps': [
            {'range': [0, 25], 'color': 'lightgreen'},
            {'range': [25, 50], 'color': 'lightyellow'},
            {'range': [50, 75], 'color': 'orange'},
            {'range': [75, 100], 'color': 'red'}
        ],
    },
    domain={'row': 0, 'column': 1}
))

# Add market sentiment indicator
sentiment_map = {
    'Very Bearish': 10,
    'Bearish': 30,
    'Neutral': 50,
    'Bullish': 70,
    'Very Bullish': 90
}

fig.add_trace(go.Indicator(
    mode="gauge+number",
    value=sentiment_map.get(sentiment, 50),
    title={"text": market_sentiment_label},
    gauge={
        'axis': {'range': [None, 100], 'tickvals': [], 'ticktext': []},
        'bar': {'color': 'darkblue'},
        'steps': [
            {'range': [0, 20], 'color': 'red'},
            {'range': [20, 40], 'color': 'orange'},
            {'range': [40, 60], 'color': 'yellow'},
            {'range': [60, 80], 'color': 'lightgreen'},
            {'range': [80, 100], 'color': 'green'}
        ],
        'threshold': {
            'line': {'color': 'black', 'width': 3},
            'thickness': 0.75,
            'value': sentiment_map.get(sentiment, 50)
        }
    },
    domain={'row': 0, 'column': 2}
))

fig.update_layout(
    grid={'rows': 1, 'columns': 3, 'pattern': "independent"},
    height=250,
)

st.plotly_chart(fig, use_container_width=True)

# Market Trends Section
st.header(market_trends_section)
st.markdown(trends_text)

# Generate sample trend data for the last 12 months
dates = [datetime.now() - timedelta(days=30*i) for i in range(12)]
dates.reverse()  # Oldest to newest

# Sample data for market trends
trend_data = pd.DataFrame({
    'Date': dates,
    trend_1: np.random.normal(100, 10, 12).cumsum() + 500,
    trend_2: np.random.normal(50, 15, 12).cumsum() + 200,
    trend_3: np.random.normal(30, 5, 12).cumsum() + 100,
    trend_4: np.random.normal(20, 3, 12).cumsum() + 50,
})

# Plot the trends
fig = px.line(
    trend_data, 
    x='Date', 
    y=[trend_1, trend_2, trend_3, trend_4],
    title="Market Trends Over Time",
    labels={
        'value': 'Value', 
        'variable': 'Trend',
        'Date': 'Date'
    }
)
fig.update_layout(hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)

# Competitive Analysis Section
st.header(competitor_section)
st.markdown(competitor_text)

# Add a competitor
with st.expander(add_competitor_btn):
    comp_col1, comp_col2 = st.columns(2)
    
    with comp_col1:
        new_competitor = st.text_input(competitor_name)
        new_mcap = st.number_input(
            competitor_mcap,
            min_value=0,
            value=1000000000,  # $1B default
            format="%d"
        )
        new_price = st.number_input(
            competitor_price,
            min_value=0.0,
            value=1.0,
            format="%.6f"
        )
    
    with comp_col2:
        new_supply = st.number_input(
            competitor_supply,
            min_value=0,
            value=1000000000,  # 1B tokens default
            format="%d"
        )
        new_holders = st.number_input(
            competitor_holders,
            min_value=0,
            value=10000,  # 10k holders default
            format="%d"
        )
    
    if st.button(add_competitor_btn):
        if new_competitor:  # Only add if competitor has a name
            st.session_state.market_analysis['competitors'].append({
                'name': new_competitor,
                'market_cap': new_mcap,
                'price': new_price,
                'supply': new_supply,
                'holders': new_holders
            })
            st.success(f"Added {new_competitor} to competitive analysis")

# Display competitor data if available
if st.session_state.market_analysis['competitors']:
    # Prepare data for visualization
    comp_data = pd.DataFrame(st.session_state.market_analysis['competitors'])
    
    # Add your token for comparison
    if st.session_state.tokenomics_data['token_name'] and st.session_state.tokenomics_data['token_symbol']:
        your_token_mcap = st.session_state.tokenomics_data['total_supply'] * st.session_state.tokenomics_data['initial_price']
        your_token = {
            'name': f"{st.session_state.tokenomics_data['token_name']} ({st.session_state.tokenomics_data['token_symbol']})",
            'market_cap': your_token_mcap,
            'price': st.session_state.tokenomics_data['initial_price'],
            'supply': st.session_state.tokenomics_data['total_supply'],
            'holders': 0  # Default, as we don't have this info
        }
        # Add to the beginning of the DataFrame
        comp_data = pd.concat([pd.DataFrame([your_token]), comp_data], ignore_index=True)
    
    # Display comparison chart for market cap
    st.subheader(comparison_chart)
    fig = px.bar(
        comp_data,
        x='name',
        y='market_cap',
        title=f"{competitor_mcap} {comparison_chart}",
        labels={'market_cap': competitor_mcap, 'name': competitor_name},
        color='name'
    )
    fig.update_layout(xaxis_title=competitor_name, yaxis_title=competitor_mcap)
    st.plotly_chart(fig, use_container_width=True)
    
    # Display tabular data
    st.subheader(competitor_table)
    
    # Format the data for display
    display_data = comp_data.copy()
    display_data['market_cap'] = display_data['market_cap'].apply(lambda x: f"${x:,.2f}")
    display_data['price'] = display_data['price'].apply(lambda x: f"${x:,.6f}")
    display_data['supply'] = display_data['supply'].apply(lambda x: f"{x:,}")
    display_data['holders'] = display_data['holders'].apply(lambda x: f"{x:,}")
    
    st.table(display_data)
else:
    st.info(f"No competitors added yet. Use the '{add_competitor_btn}' section to add competitors.")

# Market Sizing Section
st.header(market_sizing_section)
st.markdown(market_size_text)

sizing_col1, sizing_col2, sizing_col3 = st.columns(3)

with sizing_col1:
    tam = st.number_input(
        tam_label,
        min_value=0,
        value=st.session_state.market_analysis['tam'],
        step=1000000000,
        format="%d",
        help=tam_tooltip
    )
    if tam != st.session_state.market_analysis['tam']:
        st.session_state.market_analysis['tam'] = tam

with sizing_col2:
    sam = st.number_input(
        sam_label,
        min_value=0,
        max_value=tam,
        value=min(st.session_state.market_analysis['sam'], tam),
        step=500000000,
        format="%d",
        help=sam_tooltip
    )
    if sam != st.session_state.market_analysis['sam']:
        st.session_state.market_analysis['sam'] = sam

with sizing_col3:
    som = st.number_input(
        som_label,
        min_value=0,
        max_value=sam,
        value=min(st.session_state.market_analysis['som'], sam),
        step=100000000,
        format="%d",
        help=som_tooltip
    )
    if som != st.session_state.market_analysis['som']:
        st.session_state.market_analysis['som'] = som

if st.button(calculate_btn):
    # Create a funnel chart for market sizing
    fig = go.Figure(go.Funnel(
        y=[tam_label, sam_label, som_label],
        x=[tam, sam, som],
        textinfo="value+percent initial",
        textposition="inside",
        textfont={"size": 15},
        marker={"color": ["#1f77b4", "#2ca02c", "#d62728"]},
        connector={"line": {"color": "black", "width": 2}}
    ))
    
    fig.update_layout(
        title_text="Market Size Funnel Analysis",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Calculate potential token value based on market size
    if st.session_state.tokenomics_data['total_supply'] > 0:
        potential_token_value = som / st.session_state.tokenomics_data['total_supply']
        current_token_value = st.session_state.tokenomics_data['initial_price']
        
        growth_potential = (potential_token_value / current_token_value) - 1 if current_token_value > 0 else 0
        
        if growth_potential > 0:
            st.success(f"Based on your SOM estimate and token supply, your token has a potential value of ${potential_token_value:.6f}, representing a {growth_potential:.2%} growth potential from your initial price.")
        else:
            st.warning(f"Based on your SOM estimate and token supply, your token has a potential value of ${potential_token_value:.6f}. You may want to reconsider your market size estimates or token supply.")

# Market Scenarios Section
st.header(scenario_section)
st.markdown(scenario_text)

# Initialize scenario options
scenario_cols = st.columns(3)

with scenario_cols[0]:
    st.subheader(bull_label)
    bull_growth = st.number_input(
        "Growth Rate (%)",
        min_value=-100.0,
        max_value=1000.0,
        value=float(st.session_state.market_analysis['scenarios']['bull']['growth_rate']),
        step=5.0,
        key="bull_growth"
    )
    bull_share = st.number_input(
        "Market Share (%)",
        min_value=0.0,
        max_value=100.0,
        value=float(st.session_state.market_analysis['scenarios']['bull']['market_share']),
        step=0.1,
        key="bull_share"
    )
    bull_adoption = st.number_input(
        "Adoption Rate (%)",
        min_value=0.0,
        max_value=100.0,
        value=float(st.session_state.market_analysis['scenarios']['bull']['adoption_rate']),
        step=1.0,
        key="bull_adoption"
    )
    
    # Update session state
    st.session_state.market_analysis['scenarios']['bull']['growth_rate'] = bull_growth
    st.session_state.market_analysis['scenarios']['bull']['market_share'] = bull_share
    st.session_state.market_analysis['scenarios']['bull']['adoption_rate'] = bull_adoption

with scenario_cols[1]:
    st.subheader(base_label)
    base_growth = st.number_input(
        "Growth Rate (%)",
        min_value=-100.0,
        max_value=1000.0,
        value=float(st.session_state.market_analysis['scenarios']['base']['growth_rate']),
        step=5.0,
        key="base_growth"
    )
    base_share = st.number_input(
        "Market Share (%)",
        min_value=0.0,
        max_value=100.0,
        value=float(st.session_state.market_analysis['scenarios']['base']['market_share']),
        step=0.1,
        key="base_share"
    )
    base_adoption = st.number_input(
        "Adoption Rate (%)",
        min_value=0.0,
        max_value=100.0,
        value=float(st.session_state.market_analysis['scenarios']['base']['adoption_rate']),
        step=1.0,
        key="base_adoption"
    )
    
    # Update session state
    st.session_state.market_analysis['scenarios']['base']['growth_rate'] = base_growth
    st.session_state.market_analysis['scenarios']['base']['market_share'] = base_share
    st.session_state.market_analysis['scenarios']['base']['adoption_rate'] = base_adoption

with scenario_cols[2]:
    st.subheader(bear_label)
    bear_growth = st.number_input(
        "Growth Rate (%)",
        min_value=-100.0,
        max_value=1000.0,
        value=float(st.session_state.market_analysis['scenarios']['bear']['growth_rate']),
        step=5.0,
        key="bear_growth"
    )
    bear_share = st.number_input(
        "Market Share (%)",
        min_value=0.0,
        max_value=100.0,
        value=float(st.session_state.market_analysis['scenarios']['bear']['market_share']),
        step=0.1,
        key="bear_share"
    )
    bear_adoption = st.number_input(
        "Adoption Rate (%)",
        min_value=0.0,
        max_value=100.0,
        value=float(st.session_state.market_analysis['scenarios']['bear']['adoption_rate']),
        step=1.0,
        key="bear_adoption"
    )
    
    # Update session state
    st.session_state.market_analysis['scenarios']['bear']['growth_rate'] = bear_growth
    st.session_state.market_analysis['scenarios']['bear']['market_share'] = bear_share
    st.session_state.market_analysis['scenarios']['bear']['adoption_rate'] = bear_adoption

# Generate scenario projections for the next 5 years
years = list(range(2025, 2030))
initial_mcap = st.session_state.tokenomics_data['total_supply'] * st.session_state.tokenomics_data['initial_price']

# Calculate scenario projections
bull_projections = [initial_mcap]
base_projections = [initial_mcap]
bear_projections = [initial_mcap]

for i in range(1, 5):
    # Compound growth formula
    bull_projections.append(bull_projections[-1] * (1 + bull_growth/100))
    base_projections.append(base_projections[-1] * (1 + base_growth/100))
    bear_projections.append(bear_projections[-1] * (1 + bear_growth/100))

# Convert to DataFrame for easier plotting
scenario_df = pd.DataFrame({
    'Year': [2025, 2026, 2027, 2028, 2029],
    bull_label: bull_projections,
    base_label: base_projections,
    bear_label: bear_projections
})

# Plot scenario comparison
st.subheader(scenario_chart)
fig = px.line(
    scenario_df,
    x='Year',
    y=[bull_label, base_label, bear_label],
    title="Projected Market Cap by Scenario",
    labels={'value': 'Market Cap (USD)', 'variable': 'Scenario'}
)
fig.update_layout(hovermode="x unified", yaxis_tickformat='$,.2s')
st.plotly_chart(fig, use_container_width=True)

# Add a market scenario comparison table
st.subheader(scenario_params)

# Create a comparison table for the scenario parameters
params_df = pd.DataFrame({
    'Parameter': ['Growth Rate (%)', 'Market Share (%)', 'Adoption Rate (%)'],
    bull_label: [bull_growth, bull_share, bull_adoption],
    base_label: [base_growth, base_share, base_adoption],
    bear_label: [bear_growth, bear_share, bear_adoption]
})

st.table(params_df)

# Calculate the projected token price for each scenario in the final year
if st.session_state.tokenomics_data['total_supply'] > 0:
    bull_price = bull_projections[-1] / st.session_state.tokenomics_data['total_supply']
    base_price = base_projections[-1] / st.session_state.tokenomics_data['total_supply']
    bear_price = bear_projections[-1] / st.session_state.tokenomics_data['total_supply']
    
    price_df = pd.DataFrame({
        'Scenario': [bull_label, base_label, bear_label],
        'Final Market Cap (USD)': [f"${bull_projections[-1]:,.2f}", f"${base_projections[-1]:,.2f}", f"${bear_projections[-1]:,.2f}"],
        'Projected Token Price (USD)': [f"${bull_price:.6f}", f"${base_price:.6f}", f"${bear_price:.6f}"]
    })
    
    st.subheader("Projected Token Price by Scenario (2029)")
    st.table(price_df)

# Footer
st.markdown("---")
st.markdown("TokenomicsLab - Market Analysis Module")