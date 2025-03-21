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
    page_title="Teste de Estresse | Tokenomics Lab",
    page_icon="🔥",
    layout="wide"
)

# Sidebar
st.sidebar.title("Tokenomics Lab")
st.sidebar.image("https://cdn.jsdelivr.net/npm/cryptocurrency-icons@0.18.1/svg/icon/btc.svg", width=50)

# Main content
st.title("Teste de Estresse de Mercado")
st.markdown("""
    Teste seu modelo de tokenomics sob diferentes condições adversas de mercado para avaliar
    sua robustez e resiliência em diferentes cenários econômicos.
""")

# Check if model exists in session state
if 'model' not in st.session_state:
    st.warning("Você ainda não criou um modelo de tokenomics. Vá para a página de Simulação para criar um modelo primeiro.")
    
    # Button to go to simulation page
    if st.button("Ir para Simulação"):
        st.switch_page("pages/simulation.py")
        
    st.stop()

# Initialize stress test data in session state if not exists
if 'stress_test' not in st.session_state:
    st.session_state.stress_test = {
        "scenarios": {
            "bear_market": {
                "name": "Mercado em Baixa",
                "description": "Cenário de mercado em baixa prolongada",
                "price_impact": -50,
                "volatility": 40,
                "liquidity_impact": -30,
                "duration_months": 12
            },
            "high_inflation": {
                "name": "Alta Inflação",
                "description": "Cenário de inflação elevada na economia global",
                "price_impact": -20,
                "volatility": 30,
                "liquidity_impact": -10,
                "duration_months": 24
            },
            "regulatory_crackdown": {
                "name": "Repressão Regulatória",
                "description": "Cenário de aumento significativo na regulação de criptomoedas",
                "price_impact": -35,
                "volatility": 50,
                "liquidity_impact": -40,
                "duration_months": 18
            },
            "competitor_emergence": {
                "name": "Surgimento de Competidor",
                "description": "Surgimento de um forte competidor no mercado",
                "price_impact": -25,
                "volatility": 25,
                "liquidity_impact": -15,
                "duration_months": 12
            },
            "technical_failure": {
                "name": "Falha Técnica",
                "description": "Descoberta de uma falha técnica significativa no protocolo",
                "price_impact": -60,
                "volatility": 70,
                "liquidity_impact": -50,
                "duration_months": 6
            }
        },
        "custom_scenarios": [],
        "selected_scenario": "bear_market",
        "simulation_results": {}
    }

# Market Stress Test Configuration
st.header("Configuração do Teste de Estresse")

# Scenario Selection
st.subheader("Selecione o Cenário")

# Get all scenarios (predefined + custom)
all_scenarios = {}
for key, scenario in st.session_state.stress_test["scenarios"].items():
    all_scenarios[key] = scenario["name"]

for i, scenario in enumerate(st.session_state.stress_test["custom_scenarios"]):
    all_scenarios[f"custom_{i}"] = scenario["name"]

selected_scenario_key = st.selectbox(
    "Cenário de Estresse",
    options=list(all_scenarios.keys()),
    format_func=lambda x: all_scenarios[x],
    index=list(all_scenarios.keys()).index(st.session_state.stress_test["selected_scenario"]) if st.session_state.stress_test["selected_scenario"] in all_scenarios else 0,
    help="Selecione um cenário de estresse para simular."
)

st.session_state.stress_test["selected_scenario"] = selected_scenario_key

# Get the selected scenario
if selected_scenario_key.startswith("custom_"):
    custom_index = int(selected_scenario_key.split("_")[1])
    selected_scenario = st.session_state.stress_test["custom_scenarios"][custom_index]
else:
    selected_scenario = st.session_state.stress_test["scenarios"][selected_scenario_key]

# Display and edit scenario details
st.markdown(f"**{selected_scenario['name']}**: {selected_scenario['description']}")

col1, col2 = st.columns(2)

with col1:
    price_impact = st.slider(
        "Impacto no Preço (%)",
        min_value=-90,
        max_value=50,
        value=selected_scenario["price_impact"],
        help="Impacto percentual no preço do token durante este cenário. Valores negativos representam queda."
    )
    
    volatility = st.slider(
        "Volatilidade (%)",
        min_value=5,
        max_value=100,
        value=selected_scenario["volatility"],
        help="Nível de volatilidade esperado durante este cenário."
    )

with col2:
    liquidity_impact = st.slider(
        "Impacto na Liquidez (%)",
        min_value=-90,
        max_value=50,
        value=selected_scenario["liquidity_impact"],
        help="Impacto percentual na liquidez do token durante este cenário. Valores negativos representam redução."
    )
    
    duration_months = st.slider(
        "Duração (Meses)",
        min_value=1,
        max_value=36,
        value=selected_scenario["duration_months"],
        help="Duração estimada deste cenário em meses."
    )

# Update scenario values
if selected_scenario_key.startswith("custom_"):
    custom_index = int(selected_scenario_key.split("_")[1])
    st.session_state.stress_test["custom_scenarios"][custom_index].update({
        "price_impact": price_impact,
        "volatility": volatility,
        "liquidity_impact": liquidity_impact,
        "duration_months": duration_months
    })
else:
    st.session_state.stress_test["scenarios"][selected_scenario_key].update({
        "price_impact": price_impact,
        "volatility": volatility,
        "liquidity_impact": liquidity_impact,
        "duration_months": duration_months
    })

# Add custom scenario
st.subheader("Adicionar Cenário Personalizado")

with st.expander("Criar novo cenário"):
    custom_name = st.text_input("Nome do Cenário", value="", help="Dê um nome ao seu cenário personalizado.")
    custom_description = st.text_area("Descrição", value="", help="Descreva as condições deste cenário.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        custom_price_impact = st.slider(
            "Impacto no Preço (%) - Personalizado",
            min_value=-90,
            max_value=50,
            value=-30,
            help="Impacto percentual no preço do token durante este cenário. Valores negativos representam queda."
        )
        
        custom_volatility = st.slider(
            "Volatilidade (%) - Personalizado",
            min_value=5,
            max_value=100,
            value=35,
            help="Nível de volatilidade esperado durante este cenário."
        )
    
    with col2:
        custom_liquidity_impact = st.slider(
            "Impacto na Liquidez (%) - Personalizado",
            min_value=-90,
            max_value=50,
            value=-20,
            help="Impacto percentual na liquidez do token durante este cenário. Valores negativos representam redução."
        )
        
        custom_duration_months = st.slider(
            "Duração (Meses) - Personalizado",
            min_value=1,
            max_value=36,
            value=12,
            help="Duração estimada deste cenário em meses."
        )
    
    if st.button("Adicionar Cenário Personalizado"):
        if custom_name:
            new_scenario = {
                "name": custom_name,
                "description": custom_description,
                "price_impact": custom_price_impact,
                "volatility": custom_volatility,
                "liquidity_impact": custom_liquidity_impact,
                "duration_months": custom_duration_months
            }
            
            st.session_state.stress_test["custom_scenarios"].append(new_scenario)
            st.session_state.stress_test["selected_scenario"] = f"custom_{len(st.session_state.stress_test['custom_scenarios']) - 1}"
            
            st.success(f"Cenário '{custom_name}' adicionado com sucesso!")
            st.rerun()
        else:
            st.error("Por favor, forneça um nome para o cenário.")

# Run Stress Test
st.header("Executar Teste de Estresse")

if st.button("Executar Simulação de Estresse", type="primary"):
    # Get the selected scenario
    if selected_scenario_key.startswith("custom_"):
        custom_index = int(selected_scenario_key.split("_")[1])
        scenario = st.session_state.stress_test["custom_scenarios"][custom_index]
    else:
        scenario = st.session_state.stress_test["scenarios"][selected_scenario_key]
    
    # Run stress test simulation
    with st.spinner(f"Executando simulação para o cenário '{scenario['name']}'..."):
        # Get model parameters
        model = st.session_state.model
        
        # Prepare stress test parameters
        months = scenario["duration_months"]
        initial_price = 0.1  # default
        if 'simulation_result' in st.session_state and st.session_state.simulation_result is not None:
            initial_price = st.session_state.simulation_result['Price'].iloc[0]
        
        stress_volatility = scenario["volatility"] / 100
        
        # Run stress test simulation
        if hasattr(model, 'initial_users'):
            # Utility token model
            result = model.simulate_token_price(
                months, 
                initial_price,
                tokens_per_user=10.0 * (1 + scenario["liquidity_impact"] / 100),  # Adjust tokens per user based on liquidity impact
                volatility=stress_volatility
            )
        elif hasattr(model, 'initial_staking_rate'):
            # Governance token model
            result = model.simulate_token_price(
                months, 
                initial_price,
                staking_growth=0.01 * (1 + scenario["liquidity_impact"] / 100),  # Adjust staking growth based on liquidity impact
                volatility=stress_volatility
            )
        else:
            # Basic model
            result = model.simulate_token_price(
                months, 
                initial_price,
                volatility=stress_volatility
            )
        
        # Apply price impact to the simulation result
        price_factor = 1 + (scenario["price_impact"] / 100)
        result['Price'] = result['Price'] * price_factor
        result['Market_Cap'] = result['Price'] * result['Circulating_Supply']
        
        # Store the stress test result
        st.session_state.stress_test["simulation_results"][selected_scenario_key] = result
        
        st.success(f"Simulação para o cenário '{scenario['name']}' concluída!")

# Display Stress Test Results
if selected_scenario_key in st.session_state.stress_test["simulation_results"]:
    st.header("Resultados do Teste de Estresse")
    
    # Get the simulation result
    df = st.session_state.stress_test["simulation_results"][selected_scenario_key]
    
    # Get the scenario
    if selected_scenario_key.startswith("custom_"):
        custom_index = int(selected_scenario_key.split("_")[1])
        scenario = st.session_state.stress_test["custom_scenarios"][custom_index]
    else:
        scenario = st.session_state.stress_test["scenarios"][selected_scenario_key]
    
    # Display scenario details
    st.subheader(f"Análise de Estresse: {scenario['name']}")
    st.markdown(f"**Descrição:** {scenario['description']}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Impacto no Preço", 
            f"{scenario['price_impact']}%",
            delta=None
        )
    
    with col2:
        st.metric(
            "Volatilidade", 
            f"{scenario['volatility']}%",
            delta=None
        )
    
    with col3:
        st.metric(
            "Impacto na Liquidez", 
            f"{scenario['liquidity_impact']}%",
            delta=None
        )
    
    # Key metrics
    st.subheader("Métricas-Chave sob Estresse")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        initial_price = df['Price'].iloc[0]
        final_price = df['Price'].iloc[-1]
        price_change = ((final_price - initial_price) / initial_price) * 100
        
        st.metric(
            "Preço Final do Token", 
            f"${final_price:.4f}", 
            f"{price_change:.1f}%"
        )
    
    with col2:
        final_supply = df['Circulating_Supply'].iloc[-1]
        total_supply = st.session_state.model.total_supply
        supply_percent = (final_supply / total_supply) * 100
        
        st.metric(
            "Oferta Circulante", 
            f"{final_supply:,.0f}", 
            f"{supply_percent:.1f}% do total"
        )
    
    with col3:
        final_mcap = df['Market_Cap'].iloc[-1]
        initial_mcap = df['Market_Cap'].iloc[0]
        mcap_change = ((final_mcap - initial_mcap) / initial_mcap) * 100
        
        st.metric(
            "Market Cap Final", 
            f"${final_mcap:,.2f}", 
            f"{mcap_change:.1f}%"
        )
    
    with col4:
        if 'Token_Demand' in df.columns:
            final_demand = df['Token_Demand'].iloc[-1]
            initial_demand = df['Token_Demand'].iloc[0]
            demand_change = ((final_demand - initial_demand) / initial_demand) * 100
            
            st.metric(
                "Demanda Final", 
                f"{final_demand:,.0f}", 
                f"{demand_change:.1f}%"
            )
        elif 'Staking_Rate' in df.columns:
            final_staking = df['Staking_Rate'].iloc[-1] * 100
            initial_staking = df['Staking_Rate'].iloc[0] * 100
            staking_change = final_staking - initial_staking
            
            st.metric(
                "Taxa de Staking Final", 
                f"{final_staking:.1f}%", 
                f"{staking_change:+.1f}%"
            )
        else:
            final_month = df['Month'].max()
            
            st.metric(
                "Período de Estresse", 
                f"{final_month} meses"
            )
    
    # Price chart
    st.subheader("Evolução do Preço sob Estresse")
    
    fig = px.line(
        df, 
        x="Month", 
        y="Price",
        title=f"Preço do Token sob Cenário de Estresse: {scenario['name']}",
        labels={"Month": "Mês", "Price": "Preço ($)"}
    )
    
    fig.update_layout(
        hovermode="x unified"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Market cap chart
    st.subheader("Evolução do Market Cap sob Estresse")
    
    fig = px.area(
        df, 
        x="Month", 
        y="Market_Cap",
        title=f"Market Cap sob Cenário de Estresse: {scenario['name']}",
        labels={"Month": "Mês", "Market_Cap": "Market Cap ($)"},
        color_discrete_sequence=['#ff9e0a']
    )
    
    fig.update_layout(
        hovermode="x unified"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Token distribution chart
    st.subheader("Distribuição de Tokens sob Estresse")
    
    # Identify token release columns
    release_columns = [col for col in df.columns if col.endswith("_Released")]
    
    if release_columns:
        # Create dataframe for released tokens
        release_df = pd.DataFrame()
        release_df['Month'] = df['Month']
        
        for col in release_columns:
            category = col.replace("_Released", "")
            release_df[category] = df[col]
        
        # Create stacked area chart
        fig = px.area(
            release_df, 
            x="Month", 
            y=release_df.columns[1:],
            title=f"Liberação de Tokens sob Cenário de Estresse: {scenario['name']}",
            labels={"Month": "Mês", "value": "Tokens Liberados", "variable": "Categoria"}
        )
        
        fig.update_layout(
            hovermode="x unified"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Model-specific charts
    if 'Token_Demand' in df.columns:
        # Utility token model
        st.subheader("Métricas de Utility Token sob Estresse")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.line(
                df, 
                x="Month", 
                y="Users",
                title="Crescimento de Usuários sob Estresse",
                labels={"Month": "Mês", "Users": "Usuários"},
                color_discrete_sequence=['#0068c9']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.line(
                df, 
                x="Month", 
                y="Token_Demand",
                title="Demanda de Tokens sob Estresse",
                labels={"Month": "Mês", "Token_Demand": "Demanda de Tokens"},
                color_discrete_sequence=['#ff9e0a']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Supply vs Demand
        fig = px.line(
            df, 
            x="Month", 
            y=["Circulating_Supply", "Token_Demand"],
            title="Oferta vs Demanda de Tokens sob Estresse",
            labels={"Month": "Mês", "value": "Tokens", "variable": "Métrica"},
            color_discrete_map={
                'Circulating_Supply': '#0068c9',
                'Token_Demand': '#ff9e0a'
            }
        )
        
        fig.update_layout(
            hovermode="x unified"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    elif 'Staking_Rate' in df.columns:
        # Governance token model
        st.subheader("Métricas de Governance Token sob Estresse")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.line(
                df, 
                x="Month", 
                y="Staking_Rate",
                title="Taxa de Staking sob Estresse",
                labels={"Month": "Mês", "Staking_Rate": "Taxa de Staking"},
                color_discrete_sequence=['#0068c9']
            )
            
            fig.update_layout(
                yaxis=dict(tickformat=".0%")
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.line(
                df, 
                x="Month", 
                y=["Staked_Tokens", "Liquid_Tokens"],
                title="Tokens em Staking vs Tokens Líquidos sob Estresse",
                labels={"Month": "Mês", "value": "Tokens", "variable": "Tipo"},
                color_discrete_map={
                    'Staked_Tokens': '#0068c9',
                    'Liquid_Tokens': '#ff9e0a'
                }
            )
            
            fig.update_layout(
                hovermode="x unified"
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Resilience Analysis
    st.subheader("Análise de Resiliência")
    
    # Calculate minimum and recovery metrics
    min_price = df['Price'].min()
    min_price_month = df['Month'].iloc[df['Price'].argmin()]
    
    if min_price == df['Price'].iloc[-1]:
        recovery_percent = 0
        recovery_time = "Sem recuperação no período"
    else:
        # Find first month after min where price is higher than initial * 0.8
        initial_price = df['Price'].iloc[0]
        recovery_threshold = initial_price * 0.8
        
        # Find all points after minimum
        post_min = df[df['Month'] > min_price_month]
        recovery_points = post_min[post_min['Price'] >= recovery_threshold]
        
        if len(recovery_points) > 0:
            recovery_month = recovery_points.iloc[0]['Month']
            recovery_time = f"{recovery_month - min_price_month} meses após o mínimo"
            recovery_percent = (recovery_points.iloc[0]['Price'] / min_price - 1) * 100
        else:
            recovery_time = "Sem recuperação no período"
            recovery_percent = 0
    
    # Display resilience metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        initial_price = df['Price'].iloc[0]
        drawdown = ((min_price - initial_price) / initial_price) * 100
        
        st.metric(
            "Drawdown Máximo", 
            f"{drawdown:.1f}%", 
            delta=None
        )
    
    with col2:
        st.metric(
            "Mês do Preço Mínimo", 
            f"{min_price_month}", 
            delta=None
        )
    
    with col3:
        if recovery_percent > 0:
            st.metric(
                "Tempo de Recuperação", 
                recovery_time, 
                f"+{recovery_percent:.1f}% do mínimo"
            )
        else:
            st.metric(
                "Tempo de Recuperação", 
                recovery_time, 
                delta=None
            )
    
    # Recovery comparison vs benchmark
    if 'simulation_result' in st.session_state and st.session_state.simulation_result is not None:
        st.subheader("Comparação com Cenário Base")
        
        # Create a dataframe for comparison
        base_df = st.session_state.simulation_result
        
        # Check if length of base_df is sufficient
        if len(base_df) >= len(df):
            base_comparison = base_df.iloc[:len(df)].copy()
            
            # Create a comparison dataframe
            comparison_df = pd.DataFrame()
            comparison_df['Month'] = df['Month']
            comparison_df['Cenário de Estresse'] = df['Price']
            comparison_df['Cenário Base'] = base_comparison['Price']
            
            # Create line chart
            fig = px.line(
                comparison_df, 
                x="Month", 
                y=["Cenário de Estresse", "Cenário Base"],
                title="Comparação de Preço: Cenário Base vs Estresse",
                labels={"Month": "Mês", "value": "Preço ($)", "variable": "Cenário"},
                color_discrete_map={
                    'Cenário de Estresse': '#ff4b4b',
                    'Cenário Base': '#0068c9'
                }
            )
            
            fig.update_layout(
                hovermode="x unified"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Calculate impact metrics
            final_price_stress = df['Price'].iloc[-1]
            final_price_base = base_comparison['Price'].iloc[-1]
            
            price_impact = ((final_price_stress - final_price_base) / final_price_base) * 100
            
            final_mcap_stress = df['Market_Cap'].iloc[-1]
            final_mcap_base = base_comparison['Market_Cap'].iloc[-1]
            
            mcap_impact = ((final_mcap_stress - final_mcap_base) / final_mcap_base) * 100
            
            st.markdown(f"""
            ### Impacto do Cenário de Estresse
            
            Comparando com o cenário base, o cenário de estresse '{scenario['name']}' causou:
            
            - **Impacto no Preço Final:** {price_impact:.1f}%
            - **Impacto no Market Cap Final:** {mcap_impact:.1f}%
            """)
    
    # Recommendations
    st.subheader("Recomendações para Mitigação de Riscos")
    
    # Generate recommendations based on scenario
    recommendations = []
    
    if scenario['price_impact'] < -40:
        recommendations.append("Implementar mecanismos de estabilidade de preço como recompras programáticas ou queima de tokens.")
        
    if scenario['liquidity_impact'] < -30:
        recommendations.append("Aumentar reservas de liquidez e estabelecer parcerias estratégicas com provedores de liquidez.")
        
    if scenario['volatility'] > 50:
        recommendations.append("Desenvolver mecanismos de redução de volatilidade, como staking com períodos de lock-up mais longos.")
        
    if scenario['duration_months'] > 18:
        recommendations.append("Manter um fundo de reserva significativo para sustentar operações durante períodos prolongados de estresse de mercado.")
    
    # Add model-specific recommendations
    if 'Token_Demand' in df.columns:
        recommendations.append("Focar em aumentar utilidade do token para manter demanda mesmo em cenários adversos.")
        if (df['Token_Demand'] < df['Circulating_Supply']).any():
            recommendations.append("Implementar mecanismos para reduzir temporariamente a oferta circulante em resposta a quedas na demanda.")
            
    elif 'Staking_Rate' in df.columns:
        if (df['Staking_Rate'] < 0.5).any():
            recommendations.append("Oferecer incentivos adicionais para staking durante períodos de estresse para reduzir oferta circulante.")
            
    if not recommendations:
        recommendations = [
            "Manter uma comunicação transparente com a comunidade durante períodos de estresse.",
            "Continuar desenvolvimento do produto independentemente das condições de mercado.",
            "Diversificar reservas do tesouro para reduzir exposição a um único ativo."
        ]
    
    for i, rec in enumerate(recommendations):
        st.markdown(f"**{i+1}.** {rec}")
        
    # Data table
    st.subheader("Dados Detalhados da Simulação")
    st.dataframe(df, height=300)