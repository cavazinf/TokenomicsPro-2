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
    page_title="Mercado & Valoração | Tokenomics Lab",
    page_icon="💵",
    layout="wide"
)

# Sidebar
st.sidebar.title("Tokenomics Lab")
st.sidebar.image("https://cdn.jsdelivr.net/npm/cryptocurrency-icons@0.18.1/svg/icon/btc.svg", width=50)

# Main content
st.title("Mercado & Valoração")
st.markdown("""
    Analise o mercado e estime a valoração do seu token ao longo do tempo.
    Uma valoração sólida é essencial para atrair investidores e justificar o valor do seu token.
""")

# Check if model exists in session state
if 'model' not in st.session_state:
    st.warning("Você ainda não criou um modelo de tokenomics. Vá para a página de Simulação para criar um modelo primeiro.")
    
    # Button to go to simulation page
    if st.button("Ir para Simulação"):
        st.switch_page("pages/simulation.py")
        
    st.stop()

# Initialize valuation data in session state if not exists
if 'valuation' not in st.session_state:
    st.session_state.valuation = {
        "initial_token_price": 0.1,
        "initial_market_cap": 0,
        "comparable_tokens": [],
        "valuation_method": "DCF",
        "discount_rate": 20.0,
        "growth_rates": {
            "year1": 100.0,
            "year2": 50.0,
            "year3": 30.0,
            "year4": 20.0,
            "year5": 10.0
        },
        "terminal_value_multiple": 10.0,
        "cash_flows": {
            "year1": 0,
            "year2": 0,
            "year3": 0,
            "year4": 0,
            "year5": 0
        },
        "token_metrics": {
            "velocity": 5.0,
            "retention_rate": 70.0,
            "utility_value": "medium",
            "scarcity_value": "medium",
            "governance_value": "medium"
        }
    }

# Market & Valuation Configuration
st.header("Configuração de Mercado & Valoração")

# Token Pricing
st.subheader("Precificação do Token")

col1, col2 = st.columns(2)

with col1:
    initial_token_price = st.number_input(
        "Preço Inicial do Token ($)",
        min_value=0.0000001,
        max_value=1000.0,
        value=st.session_state.valuation["initial_token_price"],
        format="%.8f",
        help="Preço inicial estimado para o token no lançamento."
    )
    
    if 'model' in st.session_state and hasattr(st.session_state.model, 'total_supply'):
        total_supply = st.session_state.model.total_supply
        initial_market_cap = initial_token_price * total_supply
        st.session_state.valuation["initial_market_cap"] = initial_market_cap
        
        st.metric(
            "Market Cap Inicial", 
            f"${initial_market_cap:,.2f}"
        )

with col2:
    st.markdown("### Método de Valoração")
    
    valuation_method = st.selectbox(
        "Método de Valoração",
        ["DCF (Fluxo de Caixa Descontado)", "Comparáveis de Mercado", "Equação de Troca (MV=PQ)", "Híbrido"],
        index=["DCF (Fluxo de Caixa Descontado)", "Comparáveis de Mercado", "Equação de Troca (MV=PQ)", "Híbrido"].index(
            "DCF (Fluxo de Caixa Descontado)" if st.session_state.valuation["valuation_method"] == "DCF" else
            "Comparáveis de Mercado" if st.session_state.valuation["valuation_method"] == "Comparable" else
            "Equação de Troca (MV=PQ)" if st.session_state.valuation["valuation_method"] == "MV=PQ" else
            "Híbrido"
        ),
        help="Método utilizado para calcular a valoração do token."
    )
    
    # Update valuation method in session state
    method_map = {
        "DCF (Fluxo de Caixa Descontado)": "DCF",
        "Comparáveis de Mercado": "Comparable",
        "Equação de Troca (MV=PQ)": "MV=PQ",
        "Híbrido": "Hybrid"
    }
    st.session_state.valuation["valuation_method"] = method_map[valuation_method]

# Parameters based on valuation method
if st.session_state.valuation["valuation_method"] in ["DCF", "Hybrid"]:
    st.subheader("Parâmetros de Fluxo de Caixa Descontado (DCF)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        discount_rate = st.slider(
            "Taxa de Desconto (%)",
            min_value=5.0,
            max_value=50.0,
            value=st.session_state.valuation["discount_rate"],
            step=0.5,
            help="Taxa de desconto aplicada aos fluxos de caixa futuros. Projetos de criptomoedas geralmente têm taxas mais altas devido ao risco."
        )
        
        terminal_value_multiple = st.slider(
            "Múltiplo do Valor Terminal",
            min_value=1.0,
            max_value=30.0,
            value=st.session_state.valuation["terminal_value_multiple"],
            step=0.5,
            help="Múltiplo aplicado ao último fluxo de caixa para calcular o valor terminal."
        )
    
    with col2:
        # Growth rates
        st.markdown("**Taxas de Crescimento Anual:**")
        
        growth_year1 = st.slider(
            "Ano 1 (%)",
            min_value=-100.0,
            max_value=1000.0,
            value=st.session_state.valuation["growth_rates"]["year1"],
            step=5.0,
            help="Taxa de crescimento esperada para o primeiro ano."
        )
        
        growth_year2 = st.slider(
            "Ano 2 (%)",
            min_value=-100.0,
            max_value=500.0,
            value=st.session_state.valuation["growth_rates"]["year2"],
            step=5.0,
            help="Taxa de crescimento esperada para o segundo ano."
        )
        
        growth_year3 = st.slider(
            "Ano 3 (%)",
            min_value=-100.0,
            max_value=300.0,
            value=st.session_state.valuation["growth_rates"]["year3"],
            step=5.0,
            help="Taxa de crescimento esperada para o terceiro ano."
        )
        
        growth_year4 = st.slider(
            "Ano 4 (%)",
            min_value=-100.0,
            max_value=200.0,
            value=st.session_state.valuation["growth_rates"]["year4"],
            step=5.0,
            help="Taxa de crescimento esperada para o quarto ano."
        )
        
        growth_year5 = st.slider(
            "Ano 5 (%)",
            min_value=-100.0,
            max_value=100.0,
            value=st.session_state.valuation["growth_rates"]["year5"],
            step=5.0,
            help="Taxa de crescimento esperada para o quinto ano."
        )
    
    # Cash Flow Projections
    st.subheader("Projeções de Fluxo de Caixa")
    st.markdown("Estime os fluxos de caixa anuais gerados pelo projeto.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        cash_flow_year1 = st.number_input(
            "Fluxo de Caixa Ano 1 ($)",
            min_value=0,
            value=st.session_state.valuation["cash_flows"]["year1"],
            step=10000,
            help="Fluxo de caixa estimado para o primeiro ano."
        )
        
        cash_flow_year2 = st.number_input(
            "Fluxo de Caixa Ano 2 ($)",
            min_value=0,
            value=st.session_state.valuation["cash_flows"]["year2"],
            step=10000,
            help="Fluxo de caixa estimado para o segundo ano."
        )
    
    with col2:
        cash_flow_year3 = st.number_input(
            "Fluxo de Caixa Ano 3 ($)",
            min_value=0,
            value=st.session_state.valuation["cash_flows"]["year3"],
            step=10000,
            help="Fluxo de caixa estimado para o terceiro ano."
        )
        
        cash_flow_year4 = st.number_input(
            "Fluxo de Caixa Ano 4 ($)",
            min_value=0,
            value=st.session_state.valuation["cash_flows"]["year4"],
            step=10000,
            help="Fluxo de caixa estimado para o quarto ano."
        )
    
    with col3:
        cash_flow_year5 = st.number_input(
            "Fluxo de Caixa Ano 5 ($)",
            min_value=0,
            value=st.session_state.valuation["cash_flows"]["year5"],
            step=10000,
            help="Fluxo de caixa estimado para o quinto ano."
        )

if st.session_state.valuation["valuation_method"] in ["Comparable", "Hybrid"]:
    st.subheader("Comparáveis de Mercado")
    st.markdown("Adicione tokens comparáveis para análise de valoração relativa.")
    
    # Dynamic form for comparable tokens
    if st.button("Adicionar Token Comparável"):
        st.session_state.valuation["comparable_tokens"].append({
            "name": "",
            "symbol": "",
            "market_cap": 0,
            "price": 0.0,
            "circulating_supply": 0,
            "fully_diluted_valuation": 0,
            "pe_ratio": 0.0,
            "ps_ratio": 0.0
        })
    
    # Display existing comparable tokens
    tokens_to_remove = []
    
    for i, token in enumerate(st.session_state.valuation["comparable_tokens"]):
        with st.expander(f"Token {i+1}: {token['name'] or token['symbol'] or 'Novo Token'}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                token["name"] = st.text_input(
                    "Nome do Token", 
                    value=token["name"],
                    key=f"token_name_{i}"
                )
                
                token["symbol"] = st.text_input(
                    "Símbolo", 
                    value=token["symbol"],
                    key=f"token_symbol_{i}"
                )
                
                token["price"] = st.number_input(
                    "Preço ($)", 
                    min_value=0.0, 
                    value=token["price"],
                    format="%.8f",
                    key=f"token_price_{i}"
                )
            
            with col2:
                token["market_cap"] = st.number_input(
                    "Market Cap ($)", 
                    min_value=0, 
                    value=token["market_cap"],
                    step=1000000,
                    key=f"token_mcap_{i}"
                )
                
                token["circulating_supply"] = st.number_input(
                    "Oferta Circulante", 
                    min_value=0, 
                    value=token["circulating_supply"],
                    step=1000000,
                    key=f"token_supply_{i}"
                )
                
                token["fully_diluted_valuation"] = st.number_input(
                    "Valoração Totalmente Diluída ($)", 
                    min_value=0, 
                    value=token["fully_diluted_valuation"],
                    step=1000000,
                    key=f"token_fdv_{i}"
                )
            
            with col3:
                token["pe_ratio"] = st.number_input(
                    "Índice P/L (opcional)", 
                    min_value=0.0, 
                    value=token["pe_ratio"],
                    key=f"token_pe_{i}"
                )
                
                token["ps_ratio"] = st.number_input(
                    "Índice P/V (opcional)", 
                    min_value=0.0, 
                    value=token["ps_ratio"],
                    key=f"token_ps_{i}"
                )
            
            if st.button("Remover Token", key=f"remove_token_{i}"):
                tokens_to_remove.append(i)
    
    # Remove tokens marked for removal
    if tokens_to_remove:
        st.session_state.valuation["comparable_tokens"] = [token for i, token in enumerate(st.session_state.valuation["comparable_tokens"]) 
                                    if i not in tokens_to_remove]

if st.session_state.valuation["valuation_method"] in ["MV=PQ", "Hybrid"]:
    st.subheader("Parâmetros da Equação de Troca (MV=PQ)")
    st.markdown("""
        A equação de troca é dada por MV=PQ, onde:
        - M = Oferta monetária (tokens em circulação)
        - V = Velocidade do token (quantas vezes um token é trocado em um período)
        - P = Nível de preço dos bens/serviços
        - Q = Quantidade de bens/serviços transacionados
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        velocity = st.slider(
            "Velocidade do Token (V)",
            min_value=0.1,
            max_value=50.0,
            value=st.session_state.valuation["token_metrics"]["velocity"],
            step=0.1,
            help="Número médio de vezes que um token muda de mãos em um ano."
        )
        
        retention_rate = st.slider(
            "Taxa de Retenção do Token (%)",
            min_value=0.0,
            max_value=100.0,
            value=st.session_state.valuation["token_metrics"]["retention_rate"],
            step=0.5,
            help="Porcentagem de tokens que permanecem guardados/stakados em vez de circular."
        )
    
    with col2:
        utility_value = st.select_slider(
            "Valor de Utilidade",
            options=["muito baixo", "baixo", "médio", "alto", "muito alto"],
            value=st.session_state.valuation["token_metrics"]["utility_value"],
            help="Quão útil é o token no ecossistema do projeto."
        )
        
        scarcity_value = st.select_slider(
            "Valor de Escassez",
            options=["muito baixo", "baixo", "médio", "alto", "muito alto"],
            value=st.session_state.valuation["token_metrics"]["scarcity_value"],
            help="Quão escasso é o token em relação à sua demanda."
        )
        
        governance_value = st.select_slider(
            "Valor de Governança",
            options=["muito baixo", "baixo", "médio", "alto", "muito alto"],
            value=st.session_state.valuation["token_metrics"]["governance_value"],
            help="Quanto valor os direitos de governança do token adicionam."
        )

# Save button
if st.button("Salvar Parâmetros de Valoração", type="primary"):
    # Update valuation data in session state
    st.session_state.valuation["initial_token_price"] = initial_token_price
    
    if st.session_state.valuation["valuation_method"] in ["DCF", "Hybrid"]:
        st.session_state.valuation["discount_rate"] = discount_rate
        st.session_state.valuation["terminal_value_multiple"] = terminal_value_multiple
        st.session_state.valuation["growth_rates"] = {
            "year1": growth_year1,
            "year2": growth_year2,
            "year3": growth_year3,
            "year4": growth_year4,
            "year5": growth_year5
        }
        st.session_state.valuation["cash_flows"] = {
            "year1": cash_flow_year1,
            "year2": cash_flow_year2,
            "year3": cash_flow_year3,
            "year4": cash_flow_year4,
            "year5": cash_flow_year5
        }
    
    if st.session_state.valuation["valuation_method"] in ["MV=PQ", "Hybrid"]:
        st.session_state.valuation["token_metrics"] = {
            "velocity": velocity,
            "retention_rate": retention_rate,
            "utility_value": utility_value,
            "scarcity_value": scarcity_value,
            "governance_value": governance_value
        }
    
    st.success("Parâmetros de valoração salvos com sucesso!")

# Calculate valuation based on chosen method
st.header("Resultados da Valoração")

if st.session_state.valuation["valuation_method"] in ["DCF", "Hybrid"]:
    st.subheader("Valoração por DCF (Fluxo de Caixa Descontado)")
    
    # Calculate DCF valuation
    discount_factor = 1 + (discount_rate / 100)
    
    # Initialize list to store yearly results
    dcf_years = ["Ano 1", "Ano 2", "Ano 3", "Ano 4", "Ano 5"]
    cash_flows = [
        cash_flow_year1,
        cash_flow_year2,
        cash_flow_year3,
        cash_flow_year4,
        cash_flow_year5
    ]
    
    # Calc<response clipped><NOTE>To save on context only part of this file has been shown to you. You should retry this tool after you have searched inside the file with `grep -n` in order to find the line numbers of what you are looking for.</NOTE></function_results>
    # Calcular valor presente líquido (NPV)
    npv = 0
    for i, cf in enumerate(cash_flows):
        npv += cf / ((1 + discount_rate) ** (i + 1))
    
    # Calcular valor terminal
    terminal_value = cash_flows[-1] * terminal_value_multiple
    npv_terminal = terminal_value / ((1 + discount_rate) ** len(cash_flows))
    
    total_npv = npv + npv_terminal
