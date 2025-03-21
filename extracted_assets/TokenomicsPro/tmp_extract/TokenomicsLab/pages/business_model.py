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
    page_title="Modelo de Negócio | Tokenomics Lab",
    page_icon="💼",
    layout="wide"
)

# Sidebar
st.sidebar.title("Tokenomics Lab")
st.sidebar.image("https://cdn.jsdelivr.net/npm/cryptocurrency-icons@0.18.1/svg/icon/btc.svg", width=50)

# Main content
st.title("Modelo de Negócio")
st.markdown("""
    Defina e analise o modelo de negócio do seu projeto de tokenomics.
    Um modelo de negócio bem estruturado é essencial para o sucesso de qualquer projeto de token.
""")

# Check if model exists in session state
if 'model' not in st.session_state:
    st.warning("Você ainda não criou um modelo de tokenomics. Vá para a página de Simulação para criar um modelo primeiro.")
    
    # Button to go to simulation page
    if st.button("Ir para Simulação"):
        st.switch_page("pages/simulation.py")
        
    st.stop()

# Initialize business model data in session state if not exists
if 'business_model' not in st.session_state:
    st.session_state.business_model = {
        "revenue_streams": [],
        "cost_structure": [],
        "key_metrics": {},
        "token_utility": [],
        "value_proposition": "",
        "market_segments": [],
        "business_type": "B2C"
    }

# Business Model Configuration
st.header("Configuração do Modelo de Negócio")

# Business Type
business_type = st.selectbox(
    "Tipo de Negócio",
    ["B2C", "B2B", "B2B2C", "P2P", "DAO", "DeFi", "NFT", "GameFi", "SocialFi"],
    index=["B2C", "B2B", "B2B2C", "P2P", "DAO", "DeFi", "NFT", "GameFi", "SocialFi"].index(st.session_state.business_model["business_type"]),
    help="Selecione o tipo principal de negócio do seu projeto."
)

# Value Proposition
value_proposition = st.text_area(
    "Proposta de Valor",
    value=st.session_state.business_model.get("value_proposition", ""),
    height=100,
    help="Descreva o valor único que seu projeto oferece aos usuários."
)

# Market Segments
market_segments = st.text_area(
    "Segmentos de Mercado",
    value="\n".join(st.session_state.business_model.get("market_segments", [])),
    height=100,
    help="Liste os principais segmentos de mercado que seu projeto atende, um por linha."
)

# Revenue Streams
st.subheader("Fontes de Receita")
st.markdown("Adicione as diferentes fontes de receita do seu projeto.")

# Dynamic form for revenue streams
if st.button("Adicionar Fonte de Receita"):
    st.session_state.business_model["revenue_streams"].append({
        "name": "",
        "description": "",
        "percentage": 0.0
    })

# Display existing revenue streams
revenue_streams_to_remove = []

for i, stream in enumerate(st.session_state.business_model["revenue_streams"]):
    col1, col2, col3, col4 = st.columns([2, 3, 1, 1])
    
    with col1:
        new_name = st.text_input(
            f"Nome da Fonte {i+1}", 
            value=stream["name"],
            key=f"rev_name_{i}"
        )
        stream["name"] = new_name
        
    with col2:
        new_desc = st.text_input(
            f"Descrição {i+1}", 
            value=stream["description"],
            key=f"rev_desc_{i}"
        )
        stream["description"] = new_desc
        
    with col3:
        new_percentage = st.number_input(
            f"% da Receita {i+1}", 
            min_value=0.0, 
            max_value=100.0, 
            value=stream["percentage"],
            step=0.5,
            key=f"rev_pct_{i}"
        )
        stream["percentage"] = new_percentage
        
    with col4:
        if st.button("Remover", key=f"remove_rev_{i}"):
            revenue_streams_to_remove.append(i)

# Remove streams marked for removal
if revenue_streams_to_remove:
    st.session_state.business_model["revenue_streams"] = [stream for i, stream in enumerate(st.session_state.business_model["revenue_streams"]) 
                                     if i not in revenue_streams_to_remove]

# Cost Structure
st.subheader("Estrutura de Custos")
st.markdown("Adicione os principais custos do seu projeto.")

# Dynamic form for cost structure
if st.button("Adicionar Custo"):
    st.session_state.business_model["cost_structure"].append({
        "name": "",
        "description": "",
        "percentage": 0.0
    })

# Display existing cost structure
costs_to_remove = []

for i, cost in enumerate(st.session_state.business_model["cost_structure"]):
    col1, col2, col3, col4 = st.columns([2, 3, 1, 1])
    
    with col1:
        new_name = st.text_input(
            f"Nome do Custo {i+1}", 
            value=cost["name"],
            key=f"cost_name_{i}"
        )
        cost["name"] = new_name
        
    with col2:
        new_desc = st.text_input(
            f"Descrição {i+1}", 
            value=cost["description"],
            key=f"cost_desc_{i}"
        )
        cost["description"] = new_desc
        
    with col3:
        new_percentage = st.number_input(
            f"% do Custo {i+1}", 
            min_value=0.0, 
            max_value=100.0, 
            value=cost["percentage"],
            step=0.5,
            key=f"cost_pct_{i}"
        )
        cost["percentage"] = new_percentage
        
    with col4:
        if st.button("Remover", key=f"remove_cost_{i}"):
            costs_to_remove.append(i)

# Remove costs marked for removal
if costs_to_remove:
    st.session_state.business_model["cost_structure"] = [cost for i, cost in enumerate(st.session_state.business_model["cost_structure"]) 
                                  if i not in costs_to_remove]

# Token Utility
st.subheader("Utilidade do Token")
st.markdown("Defina as utilidades do token dentro do ecossistema do projeto.")

# Dynamic form for token utilities
token_utility = st.text_area(
    "Utilidades do Token",
    value="\n".join(st.session_state.business_model.get("token_utility", [])),
    height=150,
    help="Liste as principais utilidades do token no seu projeto, uma por linha."
)

# Key Business Metrics
st.subheader("Métricas-Chave de Negócio")

col1, col2 = st.columns(2)

with col1:
    cac = st.number_input(
        "Custo de Aquisição de Cliente (CAC em $)",
        min_value=0.0,
        value=st.session_state.business_model.get("key_metrics", {}).get("cac", 10.0),
        step=0.5,
        help="Custo médio para adquirir um novo usuário ou cliente."
    )
    
    ltv = st.number_input(
        "Valor do Tempo de Vida do Cliente (LTV em $)",
        min_value=0.0,
        value=st.session_state.business_model.get("key_metrics", {}).get("ltv", 50.0),
        step=1.0,
        help="Valor médio gerado por um cliente durante todo o relacionamento."
    )

with col2:
    churn_rate = st.slider(
        "Taxa de Churn Mensal (%)",
        min_value=0.0,
        max_value=50.0,
        value=st.session_state.business_model.get("key_metrics", {}).get("churn_rate", 5.0),
        step=0.1,
        help="Porcentagem de usuários que deixam de usar o serviço por mês."
    )
    
    conversion_rate = st.slider(
        "Taxa de Conversão (%)",
        min_value=0.0,
        max_value=100.0,
        value=st.session_state.business_model.get("key_metrics", {}).get("conversion_rate", 2.5),
        step=0.1,
        help="Porcentagem de visitantes que se convertem em usuários."
    )

# Save button
if st.button("Salvar Modelo de Negócio", type="primary"):
    # Update business model in session state
    st.session_state.business_model["business_type"] = business_type
    st.session_state.business_model["value_proposition"] = value_proposition
    st.session_state.business_model["market_segments"] = [segment.strip() for segment in market_segments.split("\n") if segment.strip()]
    st.session_state.business_model["token_utility"] = [utility.strip() for utility in token_utility.split("\n") if utility.strip()]
    st.session_state.business_model["key_metrics"] = {
        "cac": cac,
        "ltv": ltv,
        "churn_rate": churn_rate,
        "conversion_rate": conversion_rate
    }
    
    # Calculate LTV/CAC ratio
    if cac > 0:
        ltv_cac_ratio = ltv / cac
        st.session_state.business_model["key_metrics"]["ltv_cac_ratio"] = ltv_cac_ratio
    
    st.success("Modelo de negócio salvo com sucesso!")

    # Show key business metrics
    if cac > 0:
        st.metric("Ratio LTV/CAC", f"{ltv_cac_ratio:.2f}x", 
                 delta="Bom" if ltv_cac_ratio >= 3 else "Precisa melhorar")
        
        if ltv_cac_ratio < 3:
            st.warning("Seu ratio LTV/CAC está abaixo do ideal (3x). Considere estratégias para aumentar o LTV ou reduzir o CAC.")
        else:
            st.success(f"Seu ratio LTV/CAC de {ltv_cac_ratio:.2f}x é saudável (acima de 3x).")

# Visualizations
if st.session_state.business_model["revenue_streams"] and all(stream["name"] for stream in st.session_state.business_model["revenue_streams"]):
    st.header("Visualização do Modelo de Negócio")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue Streams Pie Chart
        rev_names = [stream["name"] for stream in st.session_state.business_model["revenue_streams"]]
        rev_values = [stream["percentage"] for stream in st.session_state.business_model["revenue_streams"]]
        
        fig = px.pie(
            values=rev_values,
            names=rev_names,
            title="Distribuição de Fontes de Receita",
            color_discrete_sequence=px.colors.sequential.Greens_r,
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Cost Structure Pie Chart
        if st.session_state.business_model["cost_structure"] and all(cost["name"] for cost in st.session_state.business_model["cost_structure"]):
            cost_names = [cost["name"] for cost in st.session_state.business_model["cost_structure"]]
            cost_values = [cost["percentage"] for cost in st.session_state.business_model["cost_structure"]]
            
            fig = px.pie(
                values=cost_values,
                names=cost_names,
                title="Distribuição de Custos",
                color_discrete_sequence=px.colors.sequential.Reds_r,
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

    # Token Utility and Business Metrics
    if st.session_state.business_model["token_utility"]:
        st.subheader("Utilidade do Token no Modelo de Negócio")
        
        for i, utility in enumerate(st.session_state.business_model["token_utility"]):
            st.markdown(f"**{i+1}.** {utility}")
    
    # Business Model Canvas Visualization
    st.subheader("Business Model Canvas")
    
    # Create a simple visualization of the Business Model Canvas
    canvas_data = [
        ["Proposta de Valor", "Segmentos de Mercado"],
        [st.session_state.business_model["value_proposition"], 
         "\n".join(st.session_state.business_model["market_segments"])],
        ["Fontes de Receita", "Estrutura de Custos"],
        ["\n".join([f"{s['name']}: {s['percentage']}%" for s in st.session_state.business_model["revenue_streams"]]),
         "\n".join([f"{c['name']}: {c['percentage']}%" for c in st.session_state.business_model["cost_structure"]])]
    ]
    
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["<b>Elemento</b>", "<b>Descrição</b>"],
            fill_color='#0068c9',
            align='center',
            font=dict(color='white', size=14)
        ),
        cells=dict(
            values=[
                ["<b>Proposta de Valor</b>", "<b>Segmentos de Mercado</b>", "<b>Fontes de Receita</b>", "<b>Estrutura de Custos</b>", "<b>Utilidade do Token</b>", "<b>Métricas-Chave</b>"],
                [
                    st.session_state.business_model["value_proposition"],
                    "<br>".join(st.session_state.business_model["market_segments"]),
                    "<br>".join([f"{s['name']}: {s['percentage']}%" for s in st.session_state.business_model["revenue_streams"]]),
                    "<br>".join([f"{c['name']}: {c['percentage']}%" for c in st.session_state.business_model["cost_structure"]]),
                    "<br>".join(st.session_state.business_model["token_utility"]),
                    f"CAC: ${cac}<br>LTV: ${ltv}<br>LTV/CAC: {ltv/cac if cac > 0 else 'N/A'}<br>Churn: {churn_rate}%<br>Conversão: {conversion_rate}%"
                ]
            ],
            fill_color=[['#f5f7fa', '#edf3f9'] * 6],
            align=['center', 'left'],
            font=dict(size=12),
            height=50
        )
    )])
    
    fig.update_layout(
        height=600,
        margin=dict(l=10, r=10, t=10, b=10)
    )
    
    st.plotly_chart(fig, use_container_width=True)