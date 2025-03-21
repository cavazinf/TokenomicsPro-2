import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime

# Import local modules
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.tokenomics import TokenomicsModel, UtilityTokenModel, GovernanceTokenModel

# Função para gastar créditos (importada do app.py)
def spend_credits(feature_name, cost=1):
    if 'credits' not in st.session_state:
        st.session_state.credits = 0
    if 'features_used' not in st.session_state:
        st.session_state.features_used = {}
        
    if st.session_state.credits >= cost:
        st.session_state.credits -= cost
        
        # Registro de uso de recursos
        if feature_name in st.session_state.features_used:
            st.session_state.features_used[feature_name] += 1
        else:
            st.session_state.features_used[feature_name] = 1
            
        return True
    else:
        st.warning(f"Créditos insuficientes para usar {feature_name}. Por favor, adquira mais créditos ou assine um plano.")
        return False

st.set_page_config(
    page_title="Simulação | Tokenomics Lab",
    page_icon="🧪",
    layout="wide"
)

# Initialize session states if not exists
if 'model' not in st.session_state:
    st.session_state.model = None
if 'simulation_result' not in st.session_state:
    st.session_state.simulation_result = None
if 'category_inputs' not in st.session_state:
    st.session_state.category_inputs = []
if 'vesting_inputs' not in st.session_state:
    st.session_state.vesting_inputs = {}

# Sidebar
st.sidebar.title("Tokenomics Lab")
st.sidebar.image("https://cdn.jsdelivr.net/npm/cryptocurrency-icons@0.18.1/svg/icon/btc.svg", width=50)

# Main content
st.title("Simulação de Tokenomics")
st.markdown("""
    Configure e simule diferentes modelos de tokenomics para analisar o comportamento
    dos tokens ao longo do tempo sob diferentes condições.
""")

# Step 1: Model Selection
st.header("1. Selecione o Tipo de Modelo")

model_type = st.selectbox(
    "Tipo de Modelo de Tokenomics",
    ["Modelo Básico", "Utility Token", "Governance Token"],
    help="Escolha o tipo de modelo de tokenomics que melhor se adapta ao seu projeto."
)

col1, col2 = st.columns(2)

with col1:
    model_name = st.text_input(
        "Nome do Modelo", 
        value="Meu Modelo de Tokenomics",
        help="Dê um nome ao seu modelo para identificação."
    )
    
    total_supply = st.number_input(
        "Oferta Total de Tokens", 
        min_value=1_000_000, 
        max_value=1_000_000_000_000, 
        value=100_000_000,
        step=1_000_000,
        help="Defina a oferta total de tokens para o seu projeto."
    )

with col2:
    if model_type == "Utility Token":
        initial_users = st.number_input(
            "Número Inicial de Usuários", 
            min_value=100, 
            max_value=10_000_000, 
            value=10_000,
            help="Número de usuários no lançamento do token."
        )
        
        user_growth_rate = st.slider(
            "Taxa de Crescimento Mensal de Usuários (%)", 
            min_value=0.0, 
            max_value=50.0, 
            value=5.0,
            step=0.5,
            help="Taxa estimada de crescimento mensal da base de usuários."
        ) / 100
    
    elif model_type == "Governance Token":
        initial_staking_rate = st.slider(
            "Taxa Inicial de Staking (%)", 
            min_value=0.0, 
            max_value=90.0, 
            value=30.0,
            step=1.0,
            help="Porcentagem estimada de tokens que serão colocados em staking inicialmente."
        ) / 100
        
        staking_apy = st.slider(
            "APY de Staking (%)", 
            min_value=0.0, 
            max_value=100.0, 
            value=12.0,
            step=0.5,
            help="Rendimento anual percentual para tokens em staking."
        ) / 100

# Step 2: Token Distribution
st.header("2. Distribuição de Tokens")

# Dynamic form for token distribution categories
if st.button("Adicionar Categoria"):
    if 'category_inputs' not in st.session_state:
        st.session_state.category_inputs = []
    
    st.session_state.category_inputs.append({
        "name": "",
        "percentage": 0.0
    })

# Display existing categories
categories_changed = False
categories_to_remove = []

if st.session_state.category_inputs:
    for i, category in enumerate(st.session_state.category_inputs):
        col1, col2, col3 = st.columns([3, 2, 1])
        
        with col1:
            new_name = st.text_input(
                f"Nome da Categoria {i+1}", 
                value=category["name"],
                key=f"cat_name_{i}"
            )
            if new_name != category["name"]:
                category["name"] = new_name
                categories_changed = True
                
        with col2:
            new_percentage = st.number_input(
                f"Porcentagem {i+1} (%)", 
                min_value=0.0, 
                max_value=100.0, 
                value=category["percentage"],
                step=0.5,
                key=f"cat_pct_{i}"
            )
            if new_percentage != category["percentage"]:
                category["percentage"] = new_percentage
                categories_changed = True
                
        with col3:
            if st.button("Remover", key=f"remove_cat_{i}"):
                categories_to_remove.append(i)

# Remove categories marked for removal
if categories_to_remove:
    st.session_state.category_inputs = [cat for i, cat in enumerate(st.session_state.category_inputs) 
                                        if i not in categories_to_remove]
    categories_changed = True

# Calculate total percentage
total_percentage = sum(cat["percentage"] for cat in st.session_state.category_inputs)
if total_percentage != 100.0:
    st.warning(f"A soma das porcentagens é {total_percentage}%. O total deve ser 100%.")

# Show distribution pie chart
if st.session_state.category_inputs and all(cat["name"] for cat in st.session_state.category_inputs):
    fig = px.pie(
        values=[cat["percentage"] for cat in st.session_state.category_inputs],
        names=[cat["name"] for cat in st.session_state.category_inputs],
        title="Distribuição de Tokens",
        color_discrete_sequence=px.colors.sequential.Blues_r,
    )
    st.plotly_chart(fig, use_container_width=True)

# Step 3: Vesting Schedule
st.header("3. Cronograma de Vesting")
st.markdown("""
    Configure como os tokens serão liberados ao longo do tempo para cada categoria.
    O cronograma de vesting define quando os tokens de cada categoria estarão disponíveis.
""")

if st.session_state.category_inputs:
    # Create tabs for each category
    category_tabs = st.tabs([cat["name"] for cat in st.session_state.category_inputs 
                            if cat["name"]])
    
    for i, tab in enumerate(category_tabs):
        category_name = st.session_state.category_inputs[i]["name"]
        
        with tab:
            st.subheader(f"Vesting para {category_name}")
            
            # Initialize vesting inputs for this category if not exists
            if category_name not in st.session_state.vesting_inputs:
                st.session_state.vesting_inputs[category_name] = []
            
            # Add new vesting period button
            if st.button(f"Adicionar Período de Vesting", key=f"add_vesting_{category_name}"):
                st.session_state.vesting_inputs[category_name].append({
                    "month": 0,
                    "percentage": 0.0
                })
            
            # Display existing vesting periods
            vesting_to_remove = []
            
            for j, vesting in enumerate(st.session_state.vesting_inputs[category_name]):
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    vesting["month"] = st.number_input(
                        f"Mês {j+1}", 
                        min_value=0, 
                        max_value=60, 
                        value=vesting["month"],
                        key=f"vesting_month_{category_name}_{j}"
                    )
                    
                with col2:
                    vesting["percentage"] = st.number_input(
                        f"Porcentagem Liberada {j+1} (%)", 
                        min_value=0.0, 
                        max_value=100.0, 
                        value=vesting["percentage"],
                        step=0.5,
                        key=f"vesting_pct_{category_name}_{j}"
                    )
                    
                with col3:
                    if st.button("Remover", key=f"remove_vesting_{category_name}_{j}"):
                        vesting_to_remove.append(j)
            
            # Remove vesting periods marked for removal
            if vesting_to_remove:
                st.session_state.vesting_inputs[category_name] = [
                    v for j, v in enumerate(st.session_state.vesting_inputs[category_name]) 
                    if j not in vesting_to_remove
                ]
            
            # Calculate total percentage
            vesting_total = sum(v["percentage"] for v in st.session_state.vesting_inputs[category_name])
            if vesting_total != 100.0:
                st.warning(f"A soma das porcentagens de vesting é {vesting_total}%. O total deve ser 100%.")
            
            # Show vesting chart if we have data
            if st.session_state.vesting_inputs[category_name]:
                # Sort by month
                sorted_vesting = sorted(st.session_state.vesting_inputs[category_name], 
                                        key=lambda x: x["month"])
                
                # Calculate cumulative percentage
                cumulative = []
                running_total = 0
                
                for v in sorted_vesting:
                    running_total += v["percentage"]
                    cumulative.append({
                        "month": v["month"],
                        "percentage": v["percentage"],
                        "cumulative": running_total
                    })
                
                # Create dataframe
                vesting_df = pd.DataFrame(cumulative)
                
                # Create chart
                fig = px.line(
                    vesting_df, 
                    x="month", 
                    y="cumulative",
                    markers=True,
                    title=f"Cronograma de Vesting para {category_name}",
                    labels={"month": "Mês", "cumulative": "% Acumulada"}
                )
                
                fig.update_layout(
                    yaxis=dict(range=[0, 105], ticksuffix="%"),
                    xaxis=dict(tickmode='linear')
                )
                
                st.plotly_chart(fig, use_container_width=True)

# Step 4: Simulation Parameters
st.header("4. Parâmetros de Simulação")

col1, col2 = st.columns(2)

with col1:
    simulation_months = st.slider(
        "Período de Simulação (Meses)", 
        min_value=12, 
        max_value=60, 
        value=36,
        step=3,
        help="Número de meses para simular o modelo de tokenomics."
    )
    
    initial_price = st.number_input(
        "Preço Inicial do Token ($)", 
        min_value=0.00001, 
        max_value=1000.0, 
        value=0.1,
        step=0.01,
        format="%.5f",
        help="Preço do token no lançamento/início da simulação."
    )

with col2:
    volatility = st.slider(
        "Volatilidade do Mercado", 
        min_value=0.01, 
        max_value=0.5, 
        value=0.1,
        step=0.01,
        help="Fator de volatilidade aleatória aplicada ao preço do token."
    )
    
    if model_type == "Utility Token":
        tokens_per_user = st.number_input(
            "Tokens por Usuário", 
            min_value=0.1, 
            max_value=1000.0, 
            value=10.0,
            step=0.5,
            help="Número médio de tokens utilizados por usuário."
        )
    
    elif model_type == "Governance Token":
        staking_growth = st.slider(
            "Crescimento Mensal da Taxa de Staking (%)", 
            min_value=0.0, 
            max_value=5.0, 
            value=0.5,
            step=0.1,
            help="Crescimento mensal estimado na taxa de staking."
        ) / 100

# Run Simulation Button
if st.button("Executar Simulação", type="primary"):
    # Validate inputs
    if not model_name:
        st.error("Por favor, insira um nome para o modelo.")
    elif not st.session_state.category_inputs:
        st.error("Por favor, adicione pelo menos uma categoria de distribuição.")
    elif total_percentage != 100.0:
        st.error(f"A soma das porcentagens de distribuição deve ser 100%, atualmente é {total_percentage}%.")
    elif any(not cat["name"] for cat in st.session_state.category_inputs):
        st.error("Todas as categorias devem ter um nome.")
    else:
        # Verificar plano e créditos disponíveis
        simulation_cost = 2 if model_type == "Modelo Básico" else 5  # Simulações avançadas custam mais
        
        # Mostrar custo ao usuário
        st.info(f"Esta simulação custará {simulation_cost} créditos.")
        
        # Verificar se tem créditos suficientes
        if not spend_credits("Simulação", simulation_cost):
            st.error("Créditos insuficientes para executar esta simulação. Por favor, adquira mais créditos ou assine um plano.")
            # Exibir botão para comprar mais créditos
            if st.button("Adquirir créditos"):
                st.session_state.page = "comprar_creditos"
                st.experimental_rerun()
        else:
            # Check if all categories have valid vesting schedules
            invalid_vesting = False
            for cat in st.session_state.category_inputs:
                if cat["name"] in st.session_state.vesting_inputs:
                    vesting_total = sum(v["percentage"] for v in st.session_state.vesting_inputs[cat["name"]])
                    if vesting_total != 100.0:
                        st.error(f"A soma das porcentagens de vesting para {cat['name']} deve ser 100%, atualmente é {vesting_total}%.")
                        invalid_vesting = True
            
            if not invalid_vesting:
                # Create model based on type
                if model_type == "Modelo Básico":
                    model = TokenomicsModel(model_name, total_supply)
                elif model_type == "Utility Token":
                    model = UtilityTokenModel(model_name, total_supply, initial_users, user_growth_rate)
                elif model_type == "Governance Token":
                    model = GovernanceTokenModel(model_name, total_supply, initial_staking_rate, staking_apy)
            
                # Set distribution
                distribution = {cat["name"]: cat["percentage"] for cat in st.session_state.category_inputs}
                model.set_distribution(distribution)
                
                # Set vesting schedules
                for cat_name, vesting_periods in st.session_state.vesting_inputs.items():
                    if vesting_periods:  # Only if we have vesting data
                        # Format as (month, percentage) tuples
                        schedule = [(v["month"], v["percentage"]) for v in vesting_periods]
                        model.set_vesting_schedule(cat_name, schedule)
                
                # Run simulation based on model type
                if model_type == "Utility Token":
                    simulation_result = model.simulate_token_price(
                        simulation_months, 
                        initial_price,
                        tokens_per_user=tokens_per_user,
                        volatility=volatility
                    )
                elif model_type == "Governance Token":
                    simulation_result = model.simulate_token_price(
                        simulation_months, 
                        initial_price,
                        staking_growth=staking_growth,
                        volatility=volatility
                    )
                else:
                    simulation_result = model.simulate_token_price(
                        simulation_months, 
                        initial_price,
                        volatility=volatility
                    )
                
                # Store in session state
                st.session_state.model = model
                st.session_state.simulation_result = simulation_result
                
                st.success("Simulação executada com sucesso! Veja os resultados abaixo.")
                
                # Save the model
                if not os.path.exists("saved_models"):
                    os.makedirs("saved_models")
                    
                model_data = model.to_dict()
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"saved_models/{model_name.replace(' ', '_')}_{timestamp}.json"
                
                with open(filename, "w") as f:
                    json.dump(model_data, f, indent=4)
                    
                st.info(f"Modelo salvo como {filename}")

# Display simulation results
if st.session_state.simulation_result is not None:
    st.header("Resultados da Simulação")
    
    df = st.session_state.simulation_result
    
    # Show price chart
    st.subheader("Evolução do Preço do Token")
    
    fig = px.line(
        df, 
        x="Month", 
        y="Price",
        title="Preço do Token ao Longo do Tempo",
        labels={"Month": "Mês", "Price": "Preço ($)"}
    )
    
    fig.update_layout(
        hovermode="x unified"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show circulating supply and token release
    st.subheader("Oferta Circulante e Liberação de Tokens")
    
    # Identify token release columns
    release_columns = [col for col in df.columns if col.endswith("_Released")]
    if release_columns:
        # Prepare data for stacked area chart
        fig = go.Figure()
        
        for col in release_columns:
            category = col.replace("_Released", "")
            fig.add_trace(
                go.Scatter(
                    x=df["Month"], 
                    y=df[col],
                    name=category,
                    stackgroup='one',
                    mode='lines'
                )
            )
        
        fig.update_layout(
            title="Liberação de Tokens por Categoria",
            xaxis_title="Mês",
            yaxis_title="Tokens Liberados",
            hovermode="x unified"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Show market cap
    st.subheader("Market Cap")
    
    fig = px.area(
        df, 
        x="Month", 
        y="Market_Cap",
        title="Evolução do Market Cap",
        labels={"Month": "Mês", "Market_Cap": "Market Cap ($)"}
    )
    
    fig.update_layout(
        hovermode="x unified"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show model-specific charts
    if model_type == "Utility Token":
        st.subheader("Métricas de Utility Token")
        
        # Users and Token Demand
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.line(
                df, 
                x="Month", 
                y="Users",
                title="Crescimento de Usuários",
                labels={"Month": "Mês", "Users": "Usuários"}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.line(
                df, 
                x="Month", 
                y="Token_Demand",
                title="Demanda de Tokens",
                labels={"Month": "Mês", "Token_Demand": "Demanda"}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Supply vs Demand
        fig = px.line(
            df, 
            x="Month", 
            y=["Circulating_Supply", "Token_Demand"],
            title="Oferta vs Demanda",
            labels={"Month": "Mês", "value": "Tokens", "variable": "Métrica"}
        )
        
        fig.update_layout(
            hovermode="x unified"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    elif model_type == "Governance Token":
        st.subheader("Métricas de Governance Token")
        
        # Staking Rate and Tokens
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.line(
                df, 
                x="Month", 
                y="Staking_Rate",
                title="Taxa de Staking",
                labels={"Month": "Mês", "Staking_Rate": "Taxa de Staking"}
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
                title="Tokens em Staking vs Líquidos",
                labels={"Month": "Mês", "value": "Tokens", "variable": "Tipo"}
            )
            
            fig.update_layout(
                hovermode="x unified"
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Data table with simulation results
    with st.expander("Ver Dados da Simulação"):
        st.dataframe(df)
        
        # Download button for CSV
        csv = df.to_csv(index=False)
        st.download_button(
            label="Baixar dados como CSV",
            data=csv,
            file_name=f"{model_name}_simulation.csv",
            mime="text/csv",
        )
