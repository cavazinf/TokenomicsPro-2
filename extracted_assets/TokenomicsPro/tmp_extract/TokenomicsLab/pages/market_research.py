import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import os

# Import local modules
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.tokenomics import TokenomicsModel

st.set_page_config(
    page_title="Pesquisa de Mercado | Tokenomics Lab",
    page_icon="🔍",
    layout="wide"
)

# Sidebar
st.sidebar.title("Tokenomics Lab")
st.sidebar.image("https://cdn.jsdelivr.net/npm/cryptocurrency-icons@0.18.1/svg/icon/btc.svg", width=50)

# Main content
st.title("Pesquisa de Mercado")
st.markdown("""
    Conduza uma análise detalhada do mercado de criptomoedas, identificando tendências, 
    segmentos de mercado e oportunidades para o seu projeto de tokenomics.
""")

# Check if model exists in session state
if 'model' not in st.session_state:
    st.warning("Você ainda não criou um modelo de tokenomics. Vá para a página de Simulação para criar um modelo primeiro.")
    
    # Button to go to simulation page
    if st.button("Ir para Simulação"):
        st.switch_page("pages/simulation.py")
        
    st.stop()

# Initialize market research data in session state if not exists
if 'market_research' not in st.session_state:
    st.session_state.market_research = {
        "market_segments": [],
        "trends": [],
        "competition": [],
        "user_research": [],
        "survey_results": {},
        "market_size": {
            "global_crypto": 1500000000000,  # $1.5 trillion
            "segment": 0,
            "growth_rate": 15.0,
            "addressable": 0
        }
    }

# Market Research Configuration
st.header("Configuração da Pesquisa de Mercado")

# Market Segments
st.subheader("Segmentos de Mercado")
st.markdown("Identifique e analise os segmentos de mercado relevantes para o seu projeto.")

# Dynamic form for market segments
if st.button("Adicionar Segmento de Mercado"):
    st.session_state.market_research["market_segments"].append({
        "name": "",
        "description": "",
        "size": 0,
        "growth_rate": 0.0,
        "maturity": "Emergente",
        "key_players": []
    })

# Display existing market segments
segments_to_remove = []

for i, segment in enumerate(st.session_state.market_research["market_segments"]):
    with st.expander(f"Segmento {i+1}: {segment['name'] or 'Novo Segmento'}"):
        col1, col2 = st.columns(2)
        
        with col1:
            segment["name"] = st.text_input(
                "Nome do Segmento", 
                value=segment["name"],
                key=f"seg_name_{i}"
            )
            
            segment["description"] = st.text_area(
                "Descrição", 
                value=segment["description"],
                height=100,
                key=f"seg_desc_{i}"
            )
            
            segment["maturity"] = st.selectbox(
                "Maturidade do Mercado", 
                ["Emergente", "Em crescimento", "Maduro", "Saturado"],
                index=["Emergente", "Em crescimento", "Maduro", "Saturado"].index(segment["maturity"]),
                key=f"seg_maturity_{i}"
            )
        
        with col2:
            segment["size"] = st.number_input(
                "Tamanho do Mercado (USD)", 
                min_value=0, 
                value=segment["size"],
                step=1000000,
                key=f"seg_size_{i}"
            )
            
            segment["growth_rate"] = st.slider(
                "Taxa de Crescimento Anual (%)", 
                min_value=-50.0, 
                max_value=200.0, 
                value=segment["growth_rate"],
                step=0.5,
                key=f"seg_growth_{i}"
            )
            
            key_players = st.text_area(
                "Principais Competidores", 
                value="\n".join(segment["key_players"]),
                height=100,
                key=f"seg_players_{i}"
            )
            segment["key_players"] = [player.strip() for player in key_players.split("\n") if player.strip()]
        
        if st.button("Remover Segmento", key=f"remove_seg_{i}"):
            segments_to_remove.append(i)

# Remove segments marked for removal
if segments_to_remove:
    st.session_state.market_research["market_segments"] = [seg for i, seg in enumerate(st.session_state.market_research["market_segments"]) 
                                    if i not in segments_to_remove]

# Market Trends
st.subheader("Tendências de Mercado")
st.markdown("Identifique as principais tendências que afetam o mercado de criptomoedas e o seu projeto específico.")

# Dynamic form for market trends
if st.button("Adicionar Tendência de Mercado"):
    st.session_state.market_research["trends"].append({
        "name": "",
        "description": "",
        "impact": "Médio",
        "timeframe": "Médio prazo",
        "relevance": 5
    })

# Display existing market trends
trends_to_remove = []

for i, trend in enumerate(st.session_state.market_research["trends"]):
    with st.expander(f"Tendência {i+1}: {trend['name'] or 'Nova Tendência'}"):
        col1, col2 = st.columns(2)
        
        with col1:
            trend["name"] = st.text_input(
                "Nome da Tendência", 
                value=trend["name"],
                key=f"trend_name_{i}"
            )
            
            trend["description"] = st.text_area(
                "Descrição", 
                value=trend["description"],
                height=100,
                key=f"trend_desc_{i}"
            )
        
        with col2:
            trend["impact"] = st.selectbox(
                "Impacto", 
                ["Baixo", "Médio", "Alto", "Transformador"],
                index=["Baixo", "Médio", "Alto", "Transformador"].index(trend["impact"]),
                key=f"trend_impact_{i}"
            )
            
            trend["timeframe"] = st.selectbox(
                "Horizonte Temporal", 
                ["Curto prazo", "Médio prazo", "Longo prazo"],
                index=["Curto prazo", "Médio prazo", "Longo prazo"].index(trend["timeframe"]),
                key=f"trend_time_{i}"
            )
            
            trend["relevance"] = st.slider(
                "Relevância para o Projeto (1-10)", 
                min_value=1, 
                max_value=10, 
                value=trend["relevance"],
                key=f"trend_rel_{i}"
            )
        
        if st.button("Remover Tendência", key=f"remove_trend_{i}"):
            trends_to_remove.append(i)

# Remove trends marked for removal
if trends_to_remove:
    st.session_state.market_research["trends"] = [trend for i, trend in enumerate(st.session_state.market_research["trends"]) 
                              if i not in trends_to_remove]

# Competitive Analysis
st.subheader("Análise Competitiva")
st.markdown("Analise os principais competidores no seu espaço de mercado.")

# Dynamic form for competitors
if st.button("Adicionar Competidor"):
    st.session_state.market_research["competition"].append({
        "name": "",
        "token_symbol": "",
        "description": "",
        "market_cap": 0,
        "users": 0,
        "unique_selling_points": [],
        "strengths": [],
        "weaknesses": []
    })

# Display existing competitors
competition_to_remove = []

for i, competitor in enumerate(st.session_state.market_research["competition"]):
    with st.expander(f"Competidor {i+1}: {competitor['name'] or 'Novo Competidor'}"):
        col1, col2 = st.columns(2)
        
        with col1:
            competitor["name"] = st.text_input(
                "Nome do Projeto/Empresa", 
                value=competitor["name"],
                key=f"comp_name_{i}"
            )
            
            competitor["token_symbol"] = st.text_input(
                "Símbolo do Token", 
                value=competitor["token_symbol"],
                key=f"comp_symbol_{i}"
            )
            
            competitor["description"] = st.text_area(
                "Descrição", 
                value=competitor["description"],
                height=100,
                key=f"comp_desc_{i}"
            )
            
            usp = st.text_area(
                "Diferenciais Competitivos", 
                value="\n".join(competitor["unique_selling_points"]),
                height=100,
                key=f"comp_usp_{i}"
            )
            competitor["unique_selling_points"] = [item.strip() for item in usp.split("\n") if item.strip()]
        
        with col2:
            competitor["market_cap"] = st.number_input(
                "Market Cap (USD)", 
                min_value=0, 
                value=competitor["market_cap"],
                step=1000000,
                key=f"comp_mcap_{i}"
            )
            
            competitor["users"] = st.number_input(
                "Base de Usuários", 
                min_value=0, 
                value=competitor["users"],
                step=1000,
                key=f"comp_users_{i}"
            )
            
            strengths = st.text_area(
                "Pontos Fortes", 
                value="\n".join(competitor["strengths"]),
                height=100,
                key=f"comp_strengths_{i}"
            )
            competitor["strengths"] = [item.strip() for item in strengths.split("\n") if item.strip()]
            
            weaknesses = st.text_area(
                "Pontos Fracos", 
                value="\n".join(competitor["weaknesses"]),
                height=100,
                key=f"comp_weak_{i}"
            )
            competitor["weaknesses"] = [item.strip() for item in weaknesses.split("\n") if item.strip()]
        
        if st.button("Remover Competidor", key=f"remove_comp_{i}"):
            competition_to_remove.append(i)

# Remove competitors marked for removal
if competition_to_remove:
    st.session_state.market_research["competition"] = [comp for i, comp in enumerate(st.session_state.market_research["competition"]) 
                                  if i not in competition_to_remove]

# User Research
st.subheader("Pesquisa de Usuários")
st.markdown("Adicione insights de pesquisas com usuários para informar o design do seu token.")

# Dynamic form for user research
if st.button("Adicionar Insight de Usuário"):
    st.session_state.market_research["user_research"].append({
        "source": "",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "description": "",
        "key_findings": [],
        "implications": ""
    })

# Display existing user research
research_to_remove = []

for i, research in enumerate(st.session_state.market_research["user_research"]):
    with st.expander(f"Pesquisa {i+1}: {research['source'] or 'Nova Pesquisa'}"):
        col1, col2 = st.columns(2)
        
        with col1:
            research["source"] = st.text_input(
                "Fonte da Pesquisa", 
                value=research["source"],
                key=f"res_source_{i}"
            )
            
            research["date"] = st.date_input(
                "Data", 
                value=datetime.strptime(research["date"], "%Y-%m-%d") if isinstance(research["date"], str) else research["date"],
                key=f"res_date_{i}"
            ).strftime("%Y-%m-%d")
            
            research["description"] = st.text_area(
                "Descrição da Pesquisa", 
                value=research["description"],
                height=100,
                key=f"res_desc_{i}"
            )
        
        with col2:
            findings = st.text_area(
                "Principais Descobertas", 
                value="\n".join(research["key_findings"]),
                height=100,
                key=f"res_findings_{i}"
            )
            research["key_findings"] = [item.strip() for item in findings.split("\n") if item.strip()]
            
            research["implications"] = st.text_area(
                "Implicações para o Projeto", 
                value=research["implications"],
                height=100,
                key=f"res_impl_{i}"
            )
        
        if st.button("Remover Pesquisa", key=f"remove_res_{i}"):
            research_to_remove.append(i)

# Remove research marked for removal
if research_to_remove:
    st.session_state.market_research["user_research"] = [res for i, res in enumerate(st.session_state.market_research["user_research"]) 
                                   if i not in research_to_remove]

# Market Size Estimation
st.subheader("Estimativa de Tamanho de Mercado")

col1, col2 = st.columns(2)

with col1:
    global_crypto_market = st.number_input(
        "Mercado Global de Criptomoedas (USD)",
        min_value=0,
        value=st.session_state.market_research["market_size"]["global_crypto"],
        step=100000000,
        help="Tamanho atual do mercado global de criptomoedas."
    )
    
    segment_size = st.number_input(
        "Tamanho do Segmento-Alvo (USD)",
        min_value=0,
        value=st.session_state.market_research["market_size"]["segment"],
        step=10000000,
        help="Tamanho estimado do segmento específico do seu token (ex: DeFi, NFTs, etc.)."
    )

with col2:
    growth_rate = st.slider(
        "Taxa de Crescimento Anual do Segmento (%)",
        min_value=-50.0,
        max_value=200.0,
        value=st.session_state.market_research["market_size"]["growth_rate"],
        step=0.5,
        help="Taxa de crescimento anual estimada para o segmento-alvo."
    )
    
    addressable_market = st.number_input(
        "Mercado Endereçável (USD)",
        min_value=0,
        value=st.session_state.market_research["market_size"]["addressable"],
        step=1000000,
        help="Porção do segmento que seu projeto pode realisticamente endereçar."
    )

# Survey Results
st.subheader("Resultados de Pesquisas")
st.markdown("Adicione resultados de pesquisas de mercado para informar o design do seu token.")

with st.expander("Configurar Resultados de Pesquisa"):
    # Interest Level
    st.markdown("#### Nível de Interesse no Conceito")
    
    interest_very_high = st.slider(
        "Muito Interessado (%)",
        min_value=0,
        max_value=100,
        value=st.session_state.market_research.get("survey_results", {}).get("interest", {}).get("very_high", 25),
        step=1,
        key="interest_very_high"
    )
    
    interest_high = st.slider(
        "Interessado (%)",
        min_value=0,
        max_value=100,
        value=st.session_state.market_research.get("survey_results", {}).get("interest", {}).get("high", 35),
        step=1,
        key="interest_high"
    )
    
    interest_neutral = st.slider(
        "Neutro (%)",
        min_value=0,
        max_value=100,
        value=st.session_state.market_research.get("survey_results", {}).get("interest", {}).get("neutral", 20),
        step=1,
        key="interest_neutral"
    )
    
    interest_low = st.slider(
        "Pouco Interessado (%)",
        min_value=0,
        max_value=100,
        value=st.session_state.market_research.get("survey_results", {}).get("interest", {}).get("low", 15),
        step=1,
        key="interest_low"
    )
    
    interest_very_low = st.slider(
        "Sem Interesse (%)",
        min_value=0,
        max_value=100,
        value=st.session_state.market_research.get("survey_results", {}).get("interest", {}).get("very_low", 5),
        step=1,
        key="interest_very_low"
    )
    
    # Check if interest levels sum to 100%
    total_interest = interest_very_high + interest_high + interest_neutral + interest_low + interest_very_low
    if total_interest != 100:
        st.warning(f"Os níveis de interesse somam {total_interest}%. O total deve ser 100%.")
    
    # Price Sensitivity
    st.markdown("#### Sensibilidade a Preço")
    
    price_high = st.slider(
        "Dispostos a Pagar Prêmio (%)",
        min_value=0,
        max_value=100,
        value=st.session_state.market_research.get("survey_results", {}).get("price_sensitivity", {}).get("high", 10),
        step=1,
        key="price_high"
    )
    
    price_medium = st.slider(
        "Preço de Mercado (%)",
        min_value=0,
        max_value=100,
        value=st.session_state.market_research.get("survey_results", {}).get("price_sensitivity", {}).get("medium", 50),
        step=1,
        key="price_medium"
    )
    
    price_low = st.slider(
        "Sensíveis a Preço (%)",
        min_value=0,
        max_value=100,
        value=st.session_state.market_research.get("survey_results", {}).get("price_sensitivity", {}).get("low", 40),
        step=1,
        key="price_low"
    )
    
    # Check if price sensitivity levels sum to 100%
    total_price = price_high + price_medium + price_low
    if total_price != 100:
        st.warning(f"Os níveis de sensibilidade a preço somam {total_price}%. O total deve ser 100%.")
    
    # Key Features
    st.markdown("#### Importância das Características")
    
    feature_1 = st.text_input(
        "Característica 1",
        value=st.session_state.market_research.get("survey_results", {}).get("features", {}).get("feature_1", {}).get("name", "Segurança"),
        key="feature_1_name"
    )
    
    feature_1_score = st.slider(
        f"Importância: {feature_1}",
        min_value=1,
        max_value=10,
        value=st.session_state.market_research.get("survey_results", {}).get("features", {}).get("feature_1", {}).get("score", 8),
        step=1,
        key="feature_1_score"
    )
    
    feature_2 = st.text_input(
        "Característica 2",
        value=st.session_state.market_research.get("survey_results", {}).get("features", {}).get("feature_2", {}).get("name", "Facilidade de uso"),
        key="feature_2_name"
    )
    
    feature_2_score = st.slider(
        f"Importância: {feature_2}",
        min_value=1,
        max_value=10,
        value=st.session_state.market_research.get("survey_results", {}).get("features", {}).get("feature_2", {}).get("score", 7),
        step=1,
        key="feature_2_score"
    )
    
    feature_3 = st.text_input(
        "Característica 3",
        value=st.session_state.market_research.get("survey_results", {}).get("features", {}).get("feature_3", {}).get("name", "Valorização potencial"),
        key="feature_3_name"
    )
    
    feature_3_score = st.slider(
        f"Importância: {feature_3}",
        min_value=1,
        max_value=10,
        value=st.session_state.market_research.get("survey_results", {}).get("features", {}).get("feature_3", {}).get("score", 9),
        step=1,
        key="feature_3_score"
    )
    
    feature_4 = st.text_input(
        "Característica 4",
        value=st.session_state.market_research.get("survey_results", {}).get("features", {}).get("feature_4", {}).get("name", "Utilidade no ecossistema"),
        key="feature_4_name"
    )
    
    feature_4_score = st.slider(
        f"Importância: {feature_4}",
        min_value=1,
        max_value=10,
        value=st.session_state.market_research.get("survey_results", {}).get("features", {}).get("feature_4", {}).get("score", 6),
        step=1,
        key="feature_4_score"
    )
    
    feature_5 = st.text_input(
        "Característica 5",
        value=st.session_state.market_research.get("survey_results", {}).get("features", {}).get("feature_5", {}).get("name", "Liquidez"),
        key="feature_5_name"
    )
    
    feature_5_score = st.slider(
        f"Importância: {feature_5}",
        min_value=1,
        max_value=10,
        value=st.session_state.market_research.get("survey_results", {}).get("features", {}).get("feature_5", {}).get("score", 7),
        step=1,
        key="feature_5_score"
    )

# Save button
if st.button("Salvar Pesquisa de Mercado", type="primary"):
    # Update market research data in session state
    st.session_state.market_research["market_size"]["global_crypto"] = global_crypto_market
    st.session_state.market_research["market_size"]["segment"] = segment_size
    st.session_state.market_research["market_size"]["growth_rate"] = growth_rate
    st.session_state.market_research["market_size"]["addressable"] = addressable_market
    
    # Update survey results
    st.session_state.market_research["survey_results"] = {
        "interest": {
            "very_high": interest_very_high,
            "high": interest_high,
            "neutral": interest_neutral,
            "low": interest_low,
            "very_low": interest_very_low
        },
        "price_sensitivity": {
            "high": price_high,
            "medium": price_medium,
            "low": price_low
        },
        "features": {
            "feature_1": {"name": feature_1, "score": feature_1_score},
            "feature_2": {"name": feature_2, "score": feature_2_score},
            "feature_3": {"name": feature_3, "score": feature_3_score},
            "feature_4": {"name": feature_4, "score": feature_4_score},
            "feature_5": {"name": feature_5, "score": feature_5_score}
        }
    }
    
    st.success("Pesquisa de mercado salva com sucesso!")

# Visualizations
st.header("Visualizações da Pesquisa de Mercado")

# Market Size Visualization
if addressable_market > 0 and segment_size > 0 and global_crypto_market > 0:
    st.subheader("Tamanho de Mercado")
    
    market_labels = ["Mercado Global de Criptomoedas", "Segmento-Alvo", "Mercado Endereçável"]
    market_values = [global_crypto_market, segment_size, addressable_market]
    
    fig = go.Figure()
    
    fig.add_trace(go.Funnel(
        name = 'Tamanho de Mercado',
        y = market_labels,
        x = market_values,
        textinfo = "value+percent initial",
        textposition = "inside",
        textfont = {"size": 16},
        marker = {"color": ["#0068c9", "#83c9ff", "#c5e5ff"]}
    ))
    
    fig.update_layout(
        title="Funil de Tamanho de Mercado",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Growth Projection
    if growth_rate != 0:
        st.subheader("Projeção de Crescimento do Segmento")
        
        years = list(range(1, 6))
        segment_projection = [segment_size * ((1 + (growth_rate / 100)) ** year) for year in range(5)]
        addressable_projection = [addressable_market * ((1 + (growth_rate / 100)) ** year) for year in range(5)]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=years, 
            y=segment_projection,
            mode='lines+markers',
            name='Segmento-Alvo',
            line=dict(color='#0068c9', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=years, 
            y=addressable_projection,
            mode='lines+markers',
            name='Mercado Endereçável',
            line=dict(color='#83c9ff', width=3)
        ))
        
        fig.update_layout(
            title="Projeção de Crescimento de Mercado (5 Anos)",
            xaxis_title="Ano",
            yaxis_title="Tamanho do Mercado ($)",
            legend=dict(x=0.01, y=0.99),
            hovermode="x unified"
        )
        
        fig.update_yaxes(tickprefix="$")
        
        st.plotly_chart(fig, use_container_width=True)

# Competitive Analysis
if st.session_state.market_research["competition"]:
    st.subheader("Análise Competitiva")
    
    # Filter out competitors without name or market cap
    valid_competitors = [comp for comp in st.session_state.market_research["competition"] 
                       if comp["name"] and comp["market_cap"] > 0]
    
    if valid_competitors:
        # Bubble chart of competitors
        comp_names = [comp["name"] for comp in valid_competitors]
        comp_mcaps = [comp["market_cap"] for comp in valid_competitors]
        comp_users = [comp["users"] for comp in valid_competitors]
        
        # Create bubble chart
        fig = px.scatter(
            x=comp_mcaps,
            y=comp_users,
            size=[mcap/10000 + 10 for mcap in comp_mcaps],
            text=comp_names,
            labels={"x": "Market Cap ($)", "y": "Base de Usuários"},
            title="Mapa Competitivo"
        )
        
        fig.update_traces(
            textposition='top center',
            marker=dict(sizemode='area', sizeref=2.*max(comp_mcaps)/(100.**2)),
        )
        
        fig.update_layout(
            height=600,
            hovermode="closest"
        )
        
        fig.update_xaxes(tickprefix="$")
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Competitive comparison table
        st.markdown("### Comparação Competitiva")
        
        comp_data = []
        for comp in valid_competitors:
            comp_data.append({
                "Projeto": comp["name"],
                "Token": comp["token_symbol"],
                "Market Cap": f"${comp['market_cap']:,}",
                "Usuários": f"{comp['users']:,}",
                "Pontos Fortes": ", ".join(comp["strengths"][:3]),
                "Pontos Fracos": ", ".join(comp["weaknesses"][:3])
            })
        
        comp_df = pd.DataFrame(comp_data)
        st.dataframe(comp_df, hide_index=True)

# Market Segments Analysis
if st.session_state.market_research["market_segments"]:
    st.subheader("Análise de Segmentos de Mercado")
    
    # Filter out segments without name or size
    valid_segments = [seg for seg in st.session_state.market_research["market_segments"] 
                    if seg["name"] and seg["size"] > 0]
    
    if valid_segments:
        # Create treemap
        segment_names = [seg["name"] for seg in valid_segments]
        segment_sizes = [seg["size"] for seg in valid_segments]
        segment_growth = [seg["growth_rate"] for seg in valid_segments]
        segment_maturity = [seg["maturity"] for seg in valid_segments]
        
        # Create df for treemap
        segment_df = pd.DataFrame({
            "Segmento": segment_names,
            "Tamanho": segment_sizes,
            "Crescimento": segment_growth,
            "Maturidade": segment_maturity
        })
        
        fig = px.treemap(
            segment_df,
            path=["Segmento"],
            values="Tamanho",
            color="Crescimento",
            hover_data=["Maturidade"],
            color_continuous_scale="RdBu",
            color_continuous_midpoint=0,
            title="Segmentos de Mercado por Tamanho e Crescimento"
        )
        
        fig.update_layout(height=500)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display segment details
        col1, col2 = st.columns(2)
        
        for i, segment in enumerate(valid_segments):
            with col1 if i % 2 == 0 else col2:
                st.markdown(f"### {segment['name']}")
                st.markdown(f"**Descrição:** {segment['description']}")
                st.markdown(f"**Tamanho:** ${segment['size']:,}")
                st.markdown(f"**Crescimento Anual:** {segment['growth_rate']}%")
                st.markdown(f"**Maturidade:** {segment['maturity']}")
                
                if segment['key_players']:
                    st.markdown(f"**Principais Players:** {', '.join(segment['key_players'])}")
                
                st.markdown("---")

# Market Trends Analysis
if st.session_state.market_research["trends"]:
    st.subheader("Análise de Tendências de Mercado")
    
    # Filter out trends without name
    valid_trends = [trend for trend in st.session_state.market_research["trends"] 
                  if trend["name"]]
    
    if valid_trends:
        # Sort trends by relevance
        sorted_trends = sorted(valid_trends, key=lambda x: x["relevance"], reverse=True)
        
        # Create radar chart
        trend_names = [trend["name"] for trend in sorted_trends]
        trend_relevance = [trend["relevance"] for trend in sorted_trends]
        
        # Create impact score based on impact level
        impact_map = {"Baixo": 3, "Médio": 6, "Alto": 9, "Transformador": 10}
        trend_impact = [impact_map[trend["impact"]] for trend in sorted_trends]
        
        # Create timeframe score
        timeframe_map = {"Curto prazo": 9, "Médio prazo": 6, "Longo prazo": 3}
        trend_timeframe = [timeframe_map[trend["timeframe"]] for trend in sorted_trends]
        
        # Create radar chart for top 5 trends
        if len(trend_names) > 5:
            trend_names = trend_names[:5]
            trend_relevance = trend_relevance[:5]
            trend_impact = trend_impact[:5]
            trend_timeframe = trend_timeframe[:5]
        
        # Add first point again to close the loop
        if trend_names:
            trend_names.append(trend_names[0])
            trend_relevance.append(trend_relevance[0])
            trend_impact.append(trend_impact[0])
            trend_timeframe.append(trend_timeframe[0])
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=trend_relevance,
                theta=trend_names,
                fill='toself',
                name='Relevância',
                line=dict(color='#0068c9')
            ))
            
            fig.add_trace(go.Scatterpolar(
                r=trend_impact,
                theta=trend_names,
                fill='toself',
                name='Impacto',
                line=dict(color='#83c9ff')
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 10]
                    )
                ),
                title="Análise de Tendências de Mercado",
                height=600,
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Display trend details
        st.markdown("### Detalhes das Tendências")
        
        for trend in sorted_trends:
            with st.expander(f"{trend['name']} (Relevância: {trend['relevance']}/10)"):
                st.markdown(f"**Descrição:** {trend['description']}")
                st.markdown(f"**Impacto:** {trend['impact']}")
                st.markdown(f"**Horizonte Temporal:** {trend['timeframe']}")

# Survey Results Visualization
if 'survey_results' in st.session_state.market_research and st.session_state.market_research["survey_results"]:
    st.subheader("Resultados da Pesquisa de Mercado")
    
    survey_results = st.session_state.market_research["survey_results"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Interest Level Pie Chart
        if 'interest' in survey_results:
            interest = survey_results['interest']
            
            interest_labels = [
                "Muito Interessado", 
                "Interessado",
                "Neutro",
                "Pouco Interessado",
                "Sem Interesse"
            ]
            
            interest_values = [
                interest.get('very_high', 0),
                interest.get('high', 0),
                interest.get('neutral', 0),
                interest.get('low', 0),
                interest.get('very_low', 0)
            ]
            
            fig = px.pie(
                values=interest_values,
                names=interest_labels,
                title="Nível de Interesse no Conceito",
                color_discrete_sequence=px.colors.sequential.Greens,
                hole=0.4
            )
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Price Sensitivity Pie Chart
        if 'price_sensitivity' in survey_results:
            price = survey_results['price_sensitivity']
            
            price_labels = [
                "Dispostos a Pagar Prêmio", 
                "Preço de Mercado",
                "Sensíveis a Preço"
            ]
            
            price_values = [
                price.get('high', 0),
                price.get('medium', 0),
                price.get('low', 0)
            ]
            
            fig = px.pie(
                values=price_values,
                names=price_labels,
                title="Sensibilidade a Preço",
                color_discrete_sequence=px.colors.sequential.Blues,
                hole=0.4
            )
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Feature Importance Bar Chart
    if 'features' in survey_results:
        features = survey_results['features']
        
        feature_names = []
        feature_scores = []
        
        for i in range(1, 6):
            feature_key = f"feature_{i}"
            if feature_key in features and features[feature_key]['name']:
                feature_names.append(features[feature_key]['name'])
                feature_scores.append(features[feature_key]['score'])
        
        if feature_names and feature_scores:
            # Sort by score descending
            sorted_features = sorted(zip(feature_names, feature_scores), key=lambda x: x[1], reverse=True)
            feature_names = [x[0] for x in sorted_features]
            feature_scores = [x[1] for x in sorted_features]
            
            fig = px.bar(
                x=feature_scores,
                y=feature_names,
                orientation='h',
                title="Importância das Características do Token",
                labels={"x": "Importância (1-10)", "y": ""},
                color=feature_scores,
                color_continuous_scale=px.colors.sequential.Blues
            )
            
            fig.update_layout(
                yaxis={'categoryorder':'total ascending'},
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)

# User Research Insights
if st.session_state.market_research["user_research"]:
    st.subheader("Insights da Pesquisa de Usuários")
    
    # Filter out research without source
    valid_research = [res for res in st.session_state.market_research["user_research"] 
                    if res["source"]]
    
    if valid_research:
        # Sort by date descending
        sorted_research = sorted(valid_research, key=lambda x: x["date"], reverse=True)
        
        for res in sorted_research:
            with st.expander(f"{res['source']} ({res['date']})"):
                st.markdown(f"**Descrição:** {res['description']}")
                
                if res['key_findings']:
                    st.markdown("**Principais Descobertas:**")
                    for i, finding in enumerate(res['key_findings']):
                        st.markdown(f"{i+1}. {finding}")
                
                if res['implications']:
                    st.markdown(f"**Implicações para o Projeto:** {res['implications']}")

# Market Research Findings
st.header("Conclusões da Pesquisa de Mercado")

# Generate market research findings based on the data
findings = []

# Check if we have enough data
if (st.session_state.market_research["market_segments"] or 
    st.session_state.market_research["trends"] or
    st.session_state.market_research["competition"]):
    
    # Market Size Finding
    if addressable_market > 0:
        findings.append(f"O mercado endereçável estimado é de ${addressable_market:,}, com uma taxa de crescimento anual projetada de {growth_rate:.1f}%.")
    
    # Competitive Landscape Finding
    valid_competitors = [comp for comp in st.session_state.market_research["competition"] 
                       if comp["name"] and comp["market_cap"] > 0]
    if valid_competitors:
        num_competitors = len(valid_competitors)
        avg_mcap = sum(comp["market_cap"] for comp in valid_competitors) / num_competitors
        findings.append(f"Existem {num_competitors} principais competidores no mercado, com um market cap médio de ${avg_mcap:,.0f}.")
    
    # Market Trends Finding
    valid_trends = [trend for trend in st.session_state.market_research["trends"] 
                  if trend["name"]]
    if valid_trends:
        high_impact_trends = [trend for trend in valid_trends if trend["impact"] in ["Alto", "Transformador"]]
        if high_impact_trends:
            trend_names = [trend["name"] for trend in high_impact_trends[:3]]
            findings.append(f"As principais tendências de alto impacto identificadas são: {', '.join(trend_names)}.")
    
    # User Research Finding
    valid_research = [res for res in st.session_state.market_research["user_research"] 
                    if res["source"] and res["key_findings"]]
    if valid_research:
        findings.append(f"A pesquisa de usuários identificou {sum(len(res['key_findings']) for res in valid_research)} insights chave de {len(valid_research)} fontes diferentes.")
    
    # Survey Results Finding
    if 'survey_results' in st.session_state.market_research and 'interest' in st.session_state.market_research["survey_results"]:
        interest = st.session_state.market_research["survey_results"]["interest"]
        high_interest = interest.get('very_high', 0) + interest.get('high', 0)
        findings.append(f"{high_interest}% dos respondentes da pesquisa demonstraram alto interesse no conceito do token.")

# Ensure we have at least one finding
if not findings:
    findings = [
        "Complete as seções de pesquisa de mercado para gerar conclusões automáticas.",
        "Adicione competidores, tendências e segmentos de mercado para uma análise mais completa.",
        "Conduza pesquisas com usuários para entender melhor as necessidades e expectativas do mercado."
    ]

# Display findings
for i, finding in enumerate(findings):
    st.markdown(f"**{i+1}.** {finding}")

# Recommendations
st.subheader("Recomendações Estratégicas")

# Generate recommendations based on the data
recommendations = []

# Competitive Recommendations
valid_competitors = [comp for comp in st.session_state.market_research["competition"] 
                   if comp["name"] and comp["strengths"]]
if valid_competitors:
    # Find common strengths among competitors
    all_strengths = []
    for comp in valid_competitors:
        all_strengths.extend(comp["strengths"])
    
    if all_strengths:
        recommendations.append("Diferencie seu token dos competidores existentes, focando em funcionalidades exclusivas e casos de uso específicos.")

# Market Trends Recommendations
valid_trends = [trend for trend in st.session_state.market_research["trends"] 
              if trend["name"] and trend["relevance"] > 5]
if valid_trends:
    recommendations.append(f"Alinhe o design do token com as tendências emergentes de alta relevância identificadas na pesquisa, especialmente {valid_trends[0]['name']} para maximizar o potencial de mercado.")

# User Research Recommendations
valid_research = [res for res in st.session_state.market_research["user_research"] 
                if res["source"] and res["key_findings"]]
if valid_research:
    recommendations.append("Incorpore os insights da pesquisa de usuários no design do token, priorizando as funcionalidades mais valorizadas pelos potenciais usuários.")

# Survey Results Recommendations
if 'survey_results' in st.session_state.market_research:
    survey_results = st.session_state.market_research["survey_results"]
    
    if 'price_sensitivity' in survey_results:
        price = survey_results['price_sensitivity']
        price_low = price.get('low', 0)
        
        if price_low > 40:
            recommendations.append("Considere estratégias de precificação escalonadas ou modelos freemium, dado o alto número de usuários sensíveis a preço identificados na pesquisa.")
    
    if 'features' in survey_results:
        features = survey_results['features']
        top_features = []
        
        for i in range(1, 6):
            feature_key = f"feature_{i}"
            if feature_key in features and features[feature_key]['score'] >= 8:
                top_features.append(features[feature_key]['name'])
        
        if top_features:
            recommendations.append(f"Priorize o desenvolvimento das características mais valorizadas pelos usuários: {', '.join(top_features[:2])}.")

# Ensure we have at least a few recommendations
if len(recommendations) < 3:
    default_recommendations = [
        "Conduza pesquisas de mercado adicionais para validar o conceito do token com potenciais usuários.",
        "Monitore continuamente as tendências de mercado e ajuste a estratégia conforme necessário.",
        "Desenvolva um roadmap claro de desenvolvimento do token, alinhado com as necessidades do mercado e expectativas dos usuários."
    ]
    
    for rec in default_recommendations:
        if rec not in recommendations:
            recommendations.append(rec)
            if len(recommendations) >= 5:
                break

# Display recommendations
for i, rec in enumerate(recommendations):
    st.markdown(f"**{i+1}.** {rec}")

# Action Items
st.subheader("Próximos Passos")

# Generate action items based on the data
action_items = []

# Check what's missing from the market research
if not st.session_state.market_research["competition"]:
    action_items.append("Realizar uma análise competitiva detalhada, identificando os principais competidores e suas vantagens competitivas.")

if not st.session_state.market_research["market_segments"]:
    action_items.append("Definir e analisar os segmentos de mercado relevantes para o projeto, estimando tamanho e taxa de crescimento de cada um.")

if not st.session_state.market_research["user_research"]:
    action_items.append("Conduzir entrevistas com potenciais usuários para entender melhor suas necessidades, expectativas e casos de uso prioritários.")

if not st.session_state.market_research["trends"]:
    action_items.append("Pesquisar e documentar as principais tendências do mercado que podem impactar o projeto nos próximos 12-24 meses.")

# Add generic action items if needed
if len(action_items) < 3:
    default_actions = [
        "Desenvolver um plano de entrada no mercado com base nos insights da pesquisa.",
        "Criar personas de usuários para guiar o desenvolvimento do produto baseadas na pesquisa de mercado.",
        "Configurar métricas de acompanhamento para validar hipóteses de mercado durante o lançamento do token.",
        "Preparar materiais de marketing alinhados com os segmentos-alvo e necessidades identificadas na pesquisa."
    ]
    
    for action in default_actions:
        if action not in action_items:
            action_items.append(action)
            if len(action_items) >= 5:
                break

# Display action items
for i, action in enumerate(action_items):
    st.markdown(f"**{i+1}.** {action}")