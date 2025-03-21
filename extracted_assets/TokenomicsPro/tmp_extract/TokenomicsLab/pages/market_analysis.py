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
    page_title="Análise de Mercado | Tokenomics Lab",
    page_icon="📊",
    layout="wide"
)

# Sidebar
st.sidebar.title("Tokenomics Lab")
st.sidebar.image("https://cdn.jsdelivr.net/npm/cryptocurrency-icons@0.18.1/svg/icon/btc.svg", width=50)

# Main content
st.title("Análise de Mercado")
st.markdown("""
    Analise o mercado-alvo para o seu projeto de token, incluindo tamanho de mercado,
    tendências, concorrência e oportunidades.
""")

# Check if model exists in session state
if 'model' not in st.session_state:
    st.warning("Você ainda não criou um modelo de tokenomics. Vá para a página de Simulação para criar um modelo primeiro.")
    
    # Button to go to simulation page
    if st.button("Ir para Simulação"):
        st.switch_page("pages/simulation.py")
        
    st.stop()

# Initialize market analysis data in session state if not exists
if 'market_analysis' not in st.session_state:
    st.session_state.market_analysis = {
        "market_size": {
            "total_addressable_market": 0,
            "serviceable_available_market": 0,
            "serviceable_obtainable_market": 0,
            "cagr": 5.0
        },
        "competitors": [],
        "swot": {
            "strengths": [],
            "weaknesses": [],
            "opportunities": [],
            "threats": []
        },
        "trends": [],
        "target_demographics": [],
        "market_adoption": {
            "year1": 0.1,
            "year2": 0.3,
            "year3": 0.6,
            "year4": 1.0,
            "year5": 1.5
        }
    }

# Market Analysis Configuration
st.header("Configuração da Análise de Mercado")

# Market Size
st.subheader("Tamanho do Mercado")

col1, col2 = st.columns(2)

with col1:
    tam = st.number_input(
        "Mercado Endereçável Total (TAM) em $",
        min_value=0,
        value=st.session_state.market_analysis["market_size"]["total_addressable_market"],
        step=1000000,
        help="Valor total do mercado que seu projeto poderia teoricamente atingir."
    )
    
    sam = st.number_input(
        "Mercado Disponível para Atendimento (SAM) em $",
        min_value=0,
        value=st.session_state.market_analysis["market_size"]["serviceable_available_market"],
        step=1000000,
        help="Parte do TAM que seu produto/serviço pode atender atualmente."
    )

with col2:
    som = st.number_input(
        "Mercado Obtenível para Atendimento (SOM) em $",
        min_value=0,
        value=st.session_state.market_analysis["market_size"]["serviceable_obtainable_market"],
        step=1000000,
        help="Parte do SAM que você pode realisticamente capturar."
    )
    
    cagr = st.slider(
        "Taxa de Crescimento Anual Composta (CAGR) %",
        min_value=0.0,
        max_value=100.0,
        value=st.session_state.market_analysis["market_size"]["cagr"],
        step=0.5,
        help="Taxa estimada de crescimento anual do mercado."
    )

# Target Demographics
st.subheader("Demografia-Alvo")
st.markdown("Defina as principais características demográficas do seu público-alvo.")

target_demographics = st.text_area(
    "Demografias-Alvo",
    value="\n".join(st.session_state.market_analysis.get("target_demographics", [])),
    height=100,
    help="Liste as principais características demográficas do seu público-alvo, uma por linha."
)

# Competitive Analysis
st.subheader("Análise Competitiva")
st.markdown("Adicione competidores para análise comparativa.")

# Dynamic form for competitors
if st.button("Adicionar Competidor"):
    st.session_state.market_analysis["competitors"].append({
        "name": "",
        "token_type": "Utility",
        "market_cap": 0,
        "user_base": 0,
        "strengths": "",
        "weaknesses": ""
    })

# Display existing competitors
competitors_to_remove = []

for i, competitor in enumerate(st.session_state.market_analysis["competitors"]):
    with st.expander(f"Competidor {i+1}: {competitor['name'] or 'Novo'}"):
        col1, col2 = st.columns(2)
        
        with col1:
            competitor["name"] = st.text_input(
                "Nome do Competidor", 
                value=competitor["name"],
                key=f"comp_name_{i}"
            )
            
            competitor["token_type"] = st.selectbox(
                "Tipo de Token", 
                ["Utility", "Governance", "Security", "NFT", "Stablecoin", "Exchange", "Sem token"],
                index=["Utility", "Governance", "Security", "NFT", "Stablecoin", "Exchange", "Sem token"].index(competitor["token_type"]),
                key=f"comp_type_{i}"
            )
            
        with col2:
            competitor["market_cap"] = st.number_input(
                "Market Cap ($)", 
                min_value=0, 
                value=competitor["market_cap"],
                step=1000000,
                key=f"comp_mcap_{i}"
            )
            
            competitor["user_base"] = st.number_input(
                "Base de Usuários", 
                min_value=0, 
                value=competitor["user_base"],
                step=1000,
                key=f"comp_users_{i}"
            )
        
        col1, col2 = st.columns(2)
        
        with col1:
            competitor["strengths"] = st.text_area(
                "Pontos Fortes", 
                value=competitor["strengths"],
                height=100,
                key=f"comp_strengths_{i}"
            )
            
        with col2:
            competitor["weaknesses"] = st.text_area(
                "Pontos Fracos", 
                value=competitor["weaknesses"],
                height=100,
                key=f"comp_weaknesses_{i}"
            )
        
        if st.button("Remover Competidor", key=f"remove_comp_{i}"):
            competitors_to_remove.append(i)

# Remove competitors marked for removal
if competitors_to_remove:
    st.session_state.market_analysis["competitors"] = [comp for i, comp in enumerate(st.session_state.market_analysis["competitors"]) 
                                 if i not in competitors_to_remove]

# SWOT Analysis
st.subheader("Análise SWOT")

tab1, tab2, tab3, tab4 = st.tabs(["Forças", "Fraquezas", "Oportunidades", "Ameaças"])

with tab1:
    strengths = st.text_area(
        "Forças",
        value="\n".join(st.session_state.market_analysis["swot"]["strengths"]),
        height=150,
        help="Liste os pontos fortes e vantagens competitivas do seu projeto, um por linha."
    )
    
with tab2:
    weaknesses = st.text_area(
        "Fraquezas",
        value="\n".join(st.session_state.market_analysis["swot"]["weaknesses"]),
        height=150,
        help="Liste as áreas que precisam ser melhoradas ou desvantagens do seu projeto, uma por linha."
    )
    
with tab3:
    opportunities = st.text_area(
        "Oportunidades",
        value="\n".join(st.session_state.market_analysis["swot"]["opportunities"]),
        height=150,
        help="Liste as oportunidades externas que seu projeto pode explorar, uma por linha."
    )
    
with tab4:
    threats = st.text_area(
        "Ameaças",
        value="\n".join(st.session_state.market_analysis["swot"]["threats"]),
        height=150,
        help="Liste as ameaças externas que podem impactar seu projeto, uma por linha."
    )

# Market Trends
st.subheader("Tendências de Mercado")
st.markdown("Identifique as principais tendências que podem impactar seu projeto.")

trends = st.text_area(
    "Tendências",
    value="\n".join(st.session_state.market_analysis["trends"]),
    height=150,
    help="Liste as principais tendências de mercado, uma por linha."
)

# Market Adoption Forecast
st.subheader("Previsão de Adoção de Mercado")
st.markdown("Estime a porcentagem do mercado-alvo que você espera capturar ao longo do tempo.")

col1, col2 = st.columns(2)

with col1:
    year1 = st.slider(
        "Ano 1 (%)",
        min_value=0.0,
        max_value=100.0,
        value=st.session_state.market_analysis["market_adoption"]["year1"] * 100,
        step=0.1,
        help="Porcentagem do mercado-alvo que você espera capturar no primeiro ano."
    ) / 100
    
    year2 = st.slider(
        "Ano 2 (%)",
        min_value=0.0,
        max_value=100.0,
        value=st.session_state.market_analysis["market_adoption"]["year2"] * 100,
        step=0.1,
        help="Porcentagem do mercado-alvo que você espera capturar no segundo ano."
    ) / 100

with col2:
    year3 = st.slider(
        "Ano 3 (%)",
        min_value=0.0,
        max_value=100.0,
        value=st.session_state.market_analysis["market_adoption"]["year3"] * 100,
        step=0.1,
        help="Porcentagem do mercado-alvo que você espera capturar no terceiro ano."
    ) / 100
    
    year5 = st.slider(
        "Ano 5 (%)",
        min_value=0.0,
        max_value=100.0,
        value=st.session_state.market_analysis["market_adoption"]["year5"] * 100,
        step=0.1,
        help="Porcentagem do mercado-alvo que você espera capturar no quinto ano."
    ) / 100

# Save button
if st.button("Salvar Análise de Mercado", type="primary"):
    # Update market analysis in session state
    st.session_state.market_analysis["market_size"]["total_addressable_market"] = tam
    st.session_state.market_analysis["market_size"]["serviceable_available_market"] = sam
    st.session_state.market_analysis["market_size"]["serviceable_obtainable_market"] = som
    st.session_state.market_analysis["market_size"]["cagr"] = cagr
    
    st.session_state.market_analysis["target_demographics"] = [demo.strip() for demo in target_demographics.split("\n") if demo.strip()]
    
    st.session_state.market_analysis["swot"]["strengths"] = [strength.strip() for strength in strengths.split("\n") if strength.strip()]
    st.session_state.market_analysis["swot"]["weaknesses"] = [weakness.strip() for weakness in weaknesses.split("\n") if weakness.strip()]
    st.session_state.market_analysis["swot"]["opportunities"] = [opportunity.strip() for opportunity in opportunities.split("\n") if opportunity.strip()]
    st.session_state.market_analysis["swot"]["threats"] = [threat.strip() for threat in threats.split("\n") if threat.strip()]
    
    st.session_state.market_analysis["trends"] = [trend.strip() for trend in trends.split("\n") if trend.strip()]
    
    st.session_state.market_analysis["market_adoption"]["year1"] = year1
    st.session_state.market_analysis["market_adoption"]["year2"] = year2
    st.session_state.market_analysis["market_adoption"]["year3"] = year3
    st.session_state.market_analysis["market_adoption"]["year5"] = year5
    
    st.success("Análise de mercado salva com sucesso!")

# Visualizations
st.header("Visualizações da Análise de Mercado")

# Market Size Funnel
if tam > 0:
    st.subheader("Funil de Tamanho de Mercado")
    
    market_labels = ["TAM", "SAM", "SOM"]
    market_values = [tam, sam, som]
    
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

# Market Growth Projection
if tam > 0 and cagr > 0:
    st.subheader("Projeção de Crescimento do Mercado")
    
    years = list(range(1, 6))
    tam_growth = [tam * ((1 + (cagr / 100)) ** year) for year in range(5)]
    sam_growth = [sam * ((1 + (cagr / 100)) ** year) for year in range(5)]
    som_projected = [som * ((1 + (cagr / 100)) ** year) for year in range(5)]
    
    # Add market adoption to SOM
    adoption_rates = [year1, year2, year3, (year3 + year5) / 2, year5]  # Estimated year4
    project_market = [som * rate for som, rate in zip(som_projected, adoption_rates)]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=years, 
        y=tam_growth,
        mode='lines+markers',
        name='TAM',
        line=dict(color='#0068c9', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=years, 
        y=sam_growth,
        mode='lines+markers',
        name='SAM',
        line=dict(color='#83c9ff', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=years, 
        y=project_market,
        mode='lines+markers',
        name='Projeto',
        line=dict(color='#ff9e0a', width=3)
    ))
    
    fig.update_layout(
        title="Projeção de Crescimento do Mercado (5 Anos)",
        xaxis_title="Ano",
        yaxis_title="Tamanho do Mercado ($)",
        legend=dict(x=0.01, y=0.99),
        hovermode="x unified"
    )
    
    fig.update_yaxes(tickprefix="$")
    
    st.plotly_chart(fig, use_container_width=True)

# Competitive Landscape
if st.session_state.market_analysis["competitors"] and all(comp["name"] for comp in st.session_state.market_analysis["competitors"]):
    st.subheader("Panorama Competitivo")
    
    comp_names = [comp["name"] for comp in st.session_state.market_analysis["competitors"]]
    comp_mcaps = [comp["market_cap"] for comp in st.session_state.market_analysis["competitors"]]
    comp_users = [comp["user_base"] for comp in st.session_state.market_analysis["competitors"]]
    comp_types = [comp["token_type"] for comp in st.session_state.market_analysis["competitors"]]
    
    # Add our project to the comparison
    if som > 0:
        comp_names.append("Nosso Projeto")
        comp_mcaps.append(som)
        comp_users.append(st.session_state.model.total_supply if hasattr(st.session_state.model, 'total_supply') else 0)
        
        if hasattr(st.session_state.model, 'initial_users'):
            comp_users[-1] = st.session_state.model.initial_users
            
        # Determine token type
        if hasattr(st.session_state.model, 'initial_users'):
            comp_types.append("Utility")
        elif hasattr(st.session_state.model, 'initial_staking_rate'):
            comp_types.append("Governance")
        else:
            comp_types.append("Básico")
    
    # Create bubble chart
    fig = px.scatter(
        x=comp_mcaps,
        y=comp_users,
        size=[mcap/10000 + 10 for mcap in comp_mcaps],  # Adjust size for visibility
        color=comp_types,
        text=comp_names,
        labels={"x": "Market Cap ($)", "y": "Base de Usuários", "color": "Tipo de Token"},
        title="Análise Competitiva"
    )
    
    fig.update_traces(
        textposition='top center',
        marker=dict(sizemode='area', sizeref=2.*max(comp_mcaps)/(60.**2)),
    )
    
    fig.update_layout(
        height=600,
        hovermode="closest"
    )
    
    fig.update_xaxes(tickprefix="$")
    
    st.plotly_chart(fig, use_container_width=True)

# SWOT Analysis Visualization
if any([st.session_state.market_analysis["swot"]["strengths"], 
        st.session_state.market_analysis["swot"]["weaknesses"],
        st.session_state.market_analysis["swot"]["opportunities"],
        st.session_state.market_analysis["swot"]["threats"]]):
    
    st.subheader("Análise SWOT")
    
    # Create SWOT grid
    swot_data = [
        ["<b>FORÇAS</b>", "<b>FRAQUEZAS</b>"],
        [
            "<br>".join([f"• {strength}" for strength in st.session_state.market_analysis["swot"]["strengths"]]) or "Nenhuma força definida",
            "<br>".join([f"• {weakness}" for weakness in st.session_state.market_analysis["swot"]["weaknesses"]]) or "Nenhuma fraqueza definida"
        ],
        ["<b>OPORTUNIDADES</b>", "<b>AMEAÇAS</b>"],
        [
            "<br>".join([f"• {opportunity}" for opportunity in st.session_state.market_analysis["swot"]["opportunities"]]) or "Nenhuma oportunidade definida",
            "<br>".join([f"• {threat}" for threat in st.session_state.market_analysis["swot"]["threats"]]) or "Nenhuma ameaça definida"
        ]
    ]
    
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["Fatores Internos", "Fatores Externos"],
            fill_color='#0068c9',
            align='center',
            font=dict(color='white', size=14),
            height=30
        ),
        cells=dict(
            values=[
                ["<b>FORÇAS</b>", "<b>FRAQUEZAS</b>"],
                ["<b>OPORTUNIDADES</b>", "<b>AMEAÇAS</b>"]
            ],
            fill_color=[
                ['#c5e5ff', '#ffcccc'],
                ['#c5e5ff', '#ffcccc']
            ],
            align='center',
            font=dict(size=12),
            height=30
        )
    )])
    
    # Add the internal factors (strengths and weaknesses)
    fig.add_trace(go.Table(
        header=dict(
            values=["<b>FORÇAS</b>", "<b>FRAQUEZAS</b>"],
            fill_color=['#c5e5ff', '#ffcccc'],
            align='center',
            font=dict(size=12),
            height=30
        ),
        cells=dict(
            values=[
                ["<br>".join([f"• {strength}" for strength in st.session_state.market_analysis["swot"]["strengths"]]) or "Nenhuma força definida"],
                ["<br>".join([f"• {weakness}" for weakness in st.session_state.market_analysis["swot"]["weaknesses"]]) or "Nenhuma fraqueza definida"]
            ],
            fill_color=['white', 'white'],
            align='left',
            font=dict(size=11),
            height=200
        ),
        domain=dict(y=[0.5, 1])
    ))
    
    # Add the external factors (opportunities and threats)
    fig.add_trace(go.Table(
        header=dict(
            values=["<b>OPORTUNIDADES</b>", "<b>AMEAÇAS</b>"],
            fill_color=['#c5ffe5', '#ffe5c5'],
            align='center',
            font=dict(size=12),
            height=30
        ),
        cells=dict(
            values=[
                ["<br>".join([f"• {opportunity}" for opportunity in st.session_state.market_analysis["swot"]["opportunities"]]) or "Nenhuma oportunidade definida"],
                ["<br>".join([f"• {threat}" for threat in st.session_state.market_analysis["swot"]["threats"]]) or "Nenhuma ameaça definida"]
            ],
            fill_color=['white', 'white'],
            align='left',
            font=dict(size=11),
            height=200
        ),
        domain=dict(y=[0, 0.45])
    ))
    
    fig.update_layout(
        height=600,
        margin=dict(l=10, r=10, t=30, b=10),
        title="Análise SWOT"
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Market Adoption Curve
st.subheader("Curva de Adoção de Mercado")

# Calculate adoption curve
years = list(range(1, 6))
adoption_rates = [year1, year2, year3, (year3 + year5) / 2, year5]  # Estimated year4
adoption_percentages = [rate * 100 for rate in adoption_rates]

fig = px.line(
    x=years,
    y=adoption_percentages,
    markers=True,
    labels={"x": "Ano", "y": "Adoção de Mercado (%)"},
    title="Curva de Adoção de Mercado"
)

fig.update_traces(line=dict(color='#0068c9', width=3), marker=dict(size=10))
fig.update_layout(hovermode="x unified")
fig.update_yaxes(ticksuffix="%")

st.plotly_chart(fig, use_container_width=True)

# Target Demographics Visualization
if st.session_state.market_analysis["target_demographics"]:
    st.subheader("Demográficas-Alvo")
    
    # Create a simple visualization of target demographics
    demographics = st.session_state.market_analysis["target_demographics"]
    
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["<b>Principais Demografias-Alvo</b>"],
            fill_color='#0068c9',
            align='center',
            font=dict(color='white', size=14)
        ),
        cells=dict(
            values=[demographics],
            fill_color='#f5f7fa',
            align='left',
            font=dict(size=12)
        )
    )])
    
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10)
    )
    
    st.plotly_chart(fig, use_container_width=True)