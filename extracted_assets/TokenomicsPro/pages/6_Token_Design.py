import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils import get_color_scale

# Set page configuration
st.set_page_config(
    page_title="Token Design - TokenomicsLab",
    page_icon="📊",
    layout="wide"
)

# Load language variables
if 'language' not in st.session_state:
    st.session_state.language = 'English'

# Page title and description based on language
if st.session_state.language == 'English':
    title = "Token Design"
    description = """
    This section helps you design the fundamental aspects of your token, including token type, functionality, 
    and utility within your ecosystem.
    """
    token_type_label = "Token Type"
    token_standard_label = "Token Standard"
    token_utility_label = "Token Utilities"
    governance_label = "Governance Features"
    utility_score_label = "Utility Score Analysis"
    save_button = "Save Token Design"
    utility_analysis_title = "Token Utility Analysis"
    utility_description = "Rate the importance of each utility feature (1-10)"
    governance_description = "Configure governance features for your token"
    saved_message = "Token design settings saved!"
elif st.session_state.language == 'Português':
    title = "Design do Token"
    description = """
    Esta seção ajuda você a projetar os aspectos fundamentais do seu token, incluindo tipo de token, funcionalidade 
    e utilidade dentro do seu ecossistema.
    """
    token_type_label = "Tipo de Token"
    token_standard_label = "Padrão do Token"
    token_utility_label = "Utilidades do Token"
    governance_label = "Recursos de Governança"
    utility_score_label = "Análise de Pontuação de Utilidade"
    save_button = "Salvar Design do Token"
    utility_analysis_title = "Análise de Utilidade do Token"
    utility_description = "Avalie a importância de cada recurso de utilidade (1-10)"
    governance_description = "Configure recursos de governança para seu token"
    saved_message = "Configurações de design do token salvas!"
elif st.session_state.language == 'Español':
    title = "Diseño del Token"
    description = """
    Esta sección te ayuda a diseñar los aspectos fundamentales de tu token, incluyendo el tipo de token, funcionalidad 
    y utilidad dentro de tu ecosistema.
    """
    token_type_label = "Tipo de Token"
    token_standard_label = "Estándar del Token"
    token_utility_label = "Utilidades del Token"
    governance_label = "Características de Gobernanza"
    utility_score_label = "Análisis de Puntuación de Utilidad"
    save_button = "Guardar Diseño del Token"
    utility_analysis_title = "Análisis de Utilidad del Token"
    utility_description = "Califica la importancia de cada característica de utilidad (1-10)"
    governance_description = "Configura características de gobernanza para tu token"
    saved_message = "¡Configuración de diseño del token guardada!"
else:
    title = "Token Design"
    description = """
    This section helps you design the fundamental aspects of your token, including token type, functionality, 
    and utility within your ecosystem.
    """
    token_type_label = "Token Type"
    token_standard_label = "Token Standard"
    token_utility_label = "Token Utilities"
    governance_label = "Governance Features"
    utility_score_label = "Utility Score Analysis"
    save_button = "Save Token Design"
    utility_analysis_title = "Token Utility Analysis"
    utility_description = "Rate the importance of each utility feature (1-10)"
    governance_description = "Configure governance features for your token"
    saved_message = "Token design settings saved!"

# Page title and description
st.title(title)
st.markdown(description)

# Check if tokenomics data is initialized
if 'tokenomics_data' not in st.session_state:
    st.error("Please start from the main page to initialize your token data.")
    st.stop()

# Initialize token design data if not present
if 'token_design' not in st.session_state.tokenomics_data:
    st.session_state.tokenomics_data['token_design'] = {
        'token_type': 'Utility',
        'token_standard': 'ERC-20',
        'token_utilities': {
            'Payment': 5,
            'Access': 3,
            'Staking': 7,
            'Governance': 8,
            'Fee Sharing': 4,
            'Network Security': 6,
        },
        'governance_features': {
            'Proposal Threshold': 1.0,
            'Voting Period (days)': 7,
            'Quorum Percentage': 30,
            'Execution Delay (days)': 2
        }
    }

token_design = st.session_state.tokenomics_data['token_design']

# Token Type Selection
col1, col2 = st.columns(2)

with col1:
    st.subheader(token_type_label)
    
    token_type = st.selectbox(
        token_type_label,
        options=['Utility', 'Security', 'Governance', 'Payment', 'NFT', 'Stablecoin', 'Asset-Backed', 'Hybrid'],
        index=['Utility', 'Security', 'Governance', 'Payment', 'NFT', 'Stablecoin', 'Asset-Backed', 'Hybrid'].index(token_design['token_type'])
    )
    
    # Token standard selection based on type
    standards = {
        'Utility': ['ERC-20', 'BEP-20', 'TRC-20', 'SPL'],
        'Security': ['ERC-20', 'ERC-1400', 'BEP-20', 'DS-Token'],
        'Governance': ['ERC-20', 'Compound', 'BEP-20', 'SPL'],
        'Payment': ['ERC-20', 'BEP-20', 'TRC-20', 'XRP Ledger'],
        'NFT': ['ERC-721', 'ERC-1155', 'BEP-721', 'SPL'],
        'Stablecoin': ['ERC-20', 'BEP-20', 'TRC-20', 'SPL'],
        'Asset-Backed': ['ERC-20', 'ERC-1400', 'BEP-20', 'SPL'],
        'Hybrid': ['ERC-20', 'ERC-1155', 'BEP-20', 'SPL']
    }
    
    token_standard = st.selectbox(
        token_standard_label,
        options=standards[token_type],
        index=standards[token_type].index(token_design['token_standard']) if token_design['token_standard'] in standards[token_type] else 0
    )

with col2:
    st.subheader(token_utility_label)
    
    st.markdown(utility_description)
    
    utility_scores = {}
    
    utility_options = {
        'Payment': 'Use as a medium of exchange',
        'Access': 'Access to products/services',
        'Staking': 'Locking tokens for rewards',
        'Governance': 'Voting rights',
        'Fee Sharing': 'Share in protocol revenue',
        'Network Security': 'Secure the network'
    }
    
    for utility, description in utility_options.items():
        score = st.slider(
            f"{utility}: {description}",
            min_value=0,
            max_value=10,
            value=token_design['token_utilities'].get(utility, 5),
            help=f"Rate how important {utility} is for your token's utility"
        )
        utility_scores[utility] = score

# Governance Features
st.subheader(governance_label)
st.markdown(governance_description)

col1, col2 = st.columns(2)

governance_features = {}

with col1:
    governance_features['Proposal Threshold'] = st.number_input(
        "Proposal Threshold (%)",
        min_value=0.1,
        max_value=10.0,
        value=float(token_design['governance_features'].get('Proposal Threshold', 1.0)),
        step=0.1,
        help="Percentage of total supply needed to submit a proposal"
    )
    
    governance_features['Voting Period (days)'] = st.number_input(
        "Voting Period (days)",
        min_value=1,
        max_value=30,
        value=int(token_design['governance_features'].get('Voting Period (days)', 7)),
        step=1,
        help="Duration of the voting period"
    )

with col2:
    governance_features['Quorum Percentage'] = st.number_input(
        "Quorum Percentage",
        min_value=1,
        max_value=100,
        value=int(token_design['governance_features'].get('Quorum Percentage', 30)),
        step=1,
        help="Minimum participation required for a valid vote"
    )
    
    governance_features['Execution Delay (days)'] = st.number_input(
        "Execution Delay (days)",
        min_value=0,
        max_value=14,
        value=int(token_design['governance_features'].get('Execution Delay (days)', 2)),
        step=1,
        help="Time delay before implementing approved proposals"
    )

# Utility Score Analysis
st.subheader(utility_score_label)

# Create visualization of utility scores
utility_df = pd.DataFrame({
    'Utility': list(utility_scores.keys()),
    'Score': list(utility_scores.values())
})

fig = px.bar(
    utility_df,
    x='Utility',
    y='Score',
    color='Score',
    color_continuous_scale='viridis',
    title=utility_analysis_title
)

fig.update_layout(xaxis_title="Utility Type", yaxis_title="Importance Score (1-10)", yaxis_range=[0, 10])
st.plotly_chart(fig, use_container_width=True)

# Radar chart for balanced utility assessment
fig = px.line_polar(
    utility_df,
    r='Score',
    theta='Utility',
    line_close=True,
    title="Balanced Utility Assessment"
)
fig.update_traces(fill='toself')
st.plotly_chart(fig, use_container_width=True)

# Save Token Design
if st.button(save_button):
    # Update the session state with new values
    st.session_state.tokenomics_data['token_design'] = {
        'token_type': token_type,
        'token_standard': token_standard,
        'token_utilities': utility_scores,
        'governance_features': governance_features
    }
    
    st.success(saved_message)

# Token Design Best Practices
with st.expander("Token Design Best Practices"):
    st.markdown("""
    ### Token Design Best Practices
    
    #### Token Types
    
    - **Utility Tokens**: Provide access to a product or service
    - **Security Tokens**: Represent ownership in an asset
    - **Governance Tokens**: Grant voting rights in a protocol
    - **NFTs**: Non-fungible tokens representing unique assets
    - **Stablecoins**: Tokens pegged to a stable asset like USD
    
    #### Design Considerations
    
    1. **Clear Utility**: The token should have a well-defined purpose in the ecosystem
    2. **Value Accrual**: Mechanisms that drive demand for the token
    3. **Sustainability**: Token economics that are sustainable over the long term
    4. **Incentive Alignment**: Aligning stakeholder incentives through token design
    5. **Regulatory Compliance**: Considering legal and regulatory implications
    
    #### Governance Design
    
    - **Proposal Threshold**: Too high limits participation, too low may lead to spam
    - **Quorum**: Ensures sufficient participation for legitimacy
    - **Voting Period**: Provides time for informed decision-making
    - **Execution Delay**: Allows users to exit if they disagree with decisions
    
    #### Utility Score Optimization
    
    A good token design balances multiple utilities but often excels in 2-3 core areas.
    Focus on the utilities that directly support your project's core value proposition.
    """)