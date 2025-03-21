import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Import local modules
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.tokenomics import TokenomicsModel, create_model_from_dict

st.set_page_config(
    page_title="Token Design | Tokenomics Lab",
    page_icon="🪙",
    layout="wide"
)

# Sidebar
st.sidebar.title("Tokenomics Lab")
st.sidebar.image("https://cdn.jsdelivr.net/npm/cryptocurrency-icons@0.18.1/svg/icon/btc.svg", width=50)

# Main content
st.title("Token Design")
st.markdown("""
    Nesta seção, você pode projetar as características fundamentais do seu token, definindo seu propósito, 
    funcionalidades e mecanismos econômicos básicos.
""")

# Token Purpose Selection
st.header("1. Propósito do Token")

token_purpose = st.selectbox(
    "Selecione o propósito principal do seu token",
    [
        "Utility Token (Acesso a Serviços/Plataforma)",
        "Security Token (Representação de Ativos/Participação)",
        "Governance Token (Direitos de Governança)",
        "Payment Token (Meio de Pagamento)",
        "Reward Token (Incentivos e Recompensas)",
        "Asset-Backed Token (Lastreado em Ativos)",
        "Hybrid Token (Múltiplos Propósitos)"
    ],
    help="O propósito do token determina sua função principal e impacta diretamente no design de tokenomics."
)

# Token Utility Features
st.header("2. Funcionalidades do Token")

st.markdown("Selecione as funcionalidades que seu token oferecerá:")

col1, col2 = st.columns(2)

with col1:
    access_feature = st.checkbox(
        "Acesso a Plataforma/Serviços", 
        value=True,
        help="O token permite acesso a serviços ou recursos específicos na plataforma."
    )
    
    governance_feature = st.checkbox(
        "Governança", 
        value=False,
        help="Os detentores podem votar em decisões e propostas na rede/plataforma."
    )
    
    payment_feature = st.checkbox(
        "Pagamentos", 
        value=True,
        help="O token pode ser usado como meio de troca dentro do ecossistema."
    )

with col2:
    staking_feature = st.checkbox(
        "Staking/Yield", 
        value=False,
        help="Os tokens podem ser bloqueados para receber recompensas ou rendimentos."
    )
    
    discount_feature = st.checkbox(
        "Descontos/Benefícios", 
        value=False,
        help="Os detentores recebem descontos ou benefícios no uso da plataforma."
    )
    
    reward_feature = st.checkbox(
        "Recompensas por Participação", 
        value=True,
        help="Usuários recebem tokens como incentivo pela participação no ecossistema."
    )

# Token Supply Mechanics
st.header("3. Mecânica de Oferta do Token")

supply_model = st.radio(
    "Modelo de Emissão",
    ["Oferta Fixa (Fixed Supply)", "Oferta Inflacionária (Inflationary)", "Oferta Deflacionária (Deflationary)"],
    help="Define como a oferta total de tokens se comportará ao longo do tempo."
)

col1, col2 = st.columns(2)

with col1:
    initial_supply = st.number_input(
        "Oferta Inicial de Tokens", 
        min_value=1_000, 
        max_value=1_000_000_000_000, 
        value=100_000_000,
        step=1_000_000,
        help="Quantidade de tokens disponíveis no lançamento."
    )
    
    if supply_model == "Oferta Fixa (Fixed Supply)":
        max_supply = initial_supply
        st.info(f"Oferta Máxima: {max_supply:,} tokens (igual à oferta inicial)")
    else:
        max_supply = st.number_input(
            "Oferta Máxima de Tokens", 
            min_value=initial_supply, 
            max_value=10_000_000_000_000, 
            value=initial_supply * 2,
            step=10_000_000,
            help="Limite máximo de tokens que podem existir (se aplicável)."
        )

with col2:
    if supply_model == "Oferta Inflacionária (Inflationary)":
        inflation_rate = st.slider(
            "Taxa de Inflação Anual (%)", 
            min_value=0.0, 
            max_value=20.0, 
            value=5.0,
            step=0.5,
            help="Percentual de novos tokens emitidos anualmente."
        )
        
        if st.checkbox("Definir Limite de Tempo para Inflação"):
            inflation_years = st.number_input(
                "Anos de Inflação", 
                min_value=1, 
                max_value=20, 
                value=5,
                help="Número de anos em que novos tokens serão emitidos."
            )
    
    if supply_model == "Oferta Deflacionária (Deflationary)":
        burn_mechanism = st.multiselect(
            "Mecanismos de Queima (Burn)",
            [
                "Percentual das Transações", 
                "Recompra e Queima", 
                "Queima de Taxas",
                "Queima Programada",
                "Queima baseada em Uso"
            ],
            default=["Percentual das Transações"],
            help="Métodos pelos quais tokens serão permanentemente removidos da circulação."
        )
        
        if "Percentual das Transações" in burn_mechanism:
            burn_percentage = st.slider(
                "Percentual de Queima por Transação (%)", 
                min_value=0.1, 
                max_value=10.0, 
                value=1.0,
                step=0.1,
                help="Percentual de cada transação que será queimado."
            )

# Token Economic Model
st.header("4. Modelo Econômico do Token")

economic_model = st.radio(
    "Selecione o Modelo Econômico",
    [
        "Work Token (valor baseado em trabalho/serviços)",
        "Usage Token (valor baseado no uso da plataforma)",
        "Ownership Token (valor baseado em propriedade/ativos)",
        "Burn and Mint (equilíbrio por queima e emissão)",
        "Collateral Backing (lastreado em outros ativos)",
        "Híbrido (combinação de modelos)"
    ],
    help="O modelo econômico define como o valor do token é derivado e sustentado."
)

# Visualização do Design do Token
st.header("5. Visualização do Design do Token")

# Criar dados de distribuição baseados nas escolhas
token_features = []
feature_values = []

if access_feature:
    token_features.append("Acesso")
    feature_values.append(20)
if governance_feature:
    token_features.append("Governança")
    feature_values.append(15)
if payment_feature:
    token_features.append("Pagamentos")
    feature_values.append(25)
if staking_feature:
    token_features.append("Staking")
    feature_values.append(15)
if discount_feature:
    token_features.append("Descontos")
    feature_values.append(10)
if reward_feature:
    token_features.append("Recompensas")
    feature_values.append(15)

# Ajustar valores para soma de 100%
if sum(feature_values) > 0:
    normalized_values = [val * (100 / sum(feature_values)) for val in feature_values]
else:
    normalized_values = []

# Criar gráfico de radar para funcionalidades
if token_features:
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=normalized_values,
        theta=token_features,
        fill='toself',
        name='Token Features',
        line_color='rgb(0, 104, 201)',
        fillcolor='rgba(0, 104, 201, 0.5)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        title="Perfil de Funcionalidades do Token",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Resumo do design do token
st.subheader("Resumo do Design do Token")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    **Propósito Principal:** {token_purpose}
    
    **Modelo de Oferta:** {supply_model}
    - Oferta Inicial: {initial_supply:,} tokens
    - Oferta Máxima: {max_supply:,} tokens
    
    **Modelo Econômico:** {economic_model}
    """)

with col2:
    st.markdown("**Funcionalidades Incluídas:**")
    
    for feature, value in zip(token_features, normalized_values):
        st.markdown(f"- {feature}: {value:.1f}%")

# Ações para avançar
st.header("Próximos Passos")

col1, col2 = st.columns(2)

with col1:
    if st.button("Salvar Design do Token", key="save_design", type="primary"):
        st.session_state.token_design = {
            "purpose": token_purpose,
            "features": dict(zip(token_features, normalized_values)),
            "supply_model": supply_model,
            "initial_supply": initial_supply,
            "max_supply": max_supply,
            "economic_model": economic_model
        }
        
        st.success("Design do token salvo com sucesso!")

with col2:
    if st.button("Avançar para Distribuição", key="next_distribution"):
        st.session_state.token_design = {
            "purpose": token_purpose,
            "features": dict(zip(token_features, normalized_values)),
            "supply_model": supply_model,
            "initial_supply": initial_supply,
            "max_supply": max_supply,
            "economic_model": economic_model
        }
        
        st.switch_page("pages/simulation.py")