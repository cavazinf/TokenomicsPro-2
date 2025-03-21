import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils import get_color_scale

# Set page configuration
st.set_page_config(
    page_title="Tokenization Models - TokenomicsLab",
    page_icon="📊",
    layout="wide"
)

# Load language variables
if 'language' not in st.session_state:
    st.session_state.language = 'English'

# Page title and description based on language
if st.session_state.language == 'English':
    title = "Tokenization Models"
    description = """
    This section helps you explore different approaches to tokenizing assets, services, or access rights.
    Compare various tokenization models and their implications for your project.
    """
    model_type_label = "Tokenization Model Type"
    asset_class_label = "Asset Class"
    compliance_label = "Regulatory Considerations"
    model_comparison_title = "Model Comparison"
    benefits_title = "Benefits & Considerations"
    roi_title = "ROI Simulation"
    save_button = "Save Tokenization Model"
    saved_message = "Tokenization model saved!"
elif st.session_state.language == 'Português':
    title = "Modelos de Tokenização"
    description = """
    Esta seção ajuda você a explorar diferentes abordagens para tokenizar ativos, serviços ou direitos de acesso.
    Compare vários modelos de tokenização e suas implicações para seu projeto.
    """
    model_type_label = "Tipo de Modelo de Tokenização"
    asset_class_label = "Classe de Ativo"
    compliance_label = "Considerações Regulatórias"
    model_comparison_title = "Comparação de Modelos"
    benefits_title = "Benefícios e Considerações"
    roi_title = "Simulação de ROI"
    save_button = "Salvar Modelo de Tokenização"
    saved_message = "Modelo de tokenização salvo!"
elif st.session_state.language == 'Español':
    title = "Modelos de Tokenización"
    description = """
    Esta sección te ayuda a explorar diferentes enfoques para tokenizar activos, servicios o derechos de acceso.
    Compara varios modelos de tokenización y sus implicaciones para tu proyecto.
    """
    model_type_label = "Tipo de Modelo de Tokenización"
    asset_class_label = "Clase de Activo"
    compliance_label = "Consideraciones Regulatorias"
    model_comparison_title = "Comparación de Modelos"
    benefits_title = "Beneficios y Consideraciones"
    roi_title = "Simulación de ROI"
    save_button = "Guardar Modelo de Tokenización"
    saved_message = "¡Modelo de tokenización guardado!"
else:
    title = "Tokenization Models"
    description = """
    This section helps you explore different approaches to tokenizing assets, services, or access rights.
    Compare various tokenization models and their implications for your project.
    """
    model_type_label = "Tokenization Model Type"
    asset_class_label = "Asset Class"
    compliance_label = "Regulatory Considerations"
    model_comparison_title = "Model Comparison"
    benefits_title = "Benefits & Considerations"
    roi_title = "ROI Simulation"
    save_button = "Save Tokenization Model"
    saved_message = "Tokenization model saved!"

# Page title and description
st.title(title)
st.markdown(description)

# Check if tokenomics data is initialized
if 'tokenomics_data' not in st.session_state:
    st.error("Please start from the main page to initialize your token data.")
    st.stop()

# Initialize tokenization model data if not present
if 'tokenization_model' not in st.session_state.tokenomics_data:
    st.session_state.tokenomics_data['tokenization_model'] = {
        'model_type': 'Utility Access',
        'asset_class': 'Digital Services',
        'target_market': 'Global',
        'user_rights': ['Access', 'Usage'],
        'compliance_features': {
            'KYC Required': True,
            'AML Compliance': True,
            'Transfer Restrictions': False,
            'Accredited Investors Only': False
        },
        'revenue_model': 'Usage Fees',
        'fee_structure': {
            'Transaction Fee': 0.5,
            'Platform Fee': 2.0,
            'Subscription Fee': 0.0
        }
    }

tokenization_model = st.session_state.tokenomics_data['tokenization_model']

# Tokenization model selection
col1, col2 = st.columns(2)

with col1:
    st.subheader(model_type_label)
    
    model_type = st.selectbox(
        model_type_label,
        options=[
            'Utility Access', 
            'Digital Asset Ownership', 
            'Security Token', 
            'Governance Rights',
            'Reward Points',
            'Fractional Ownership',
            'Subscription Access',
            'Revenue Sharing'
        ],
        index=[
            'Utility Access', 
            'Digital Asset Ownership', 
            'Security Token', 
            'Governance Rights',
            'Reward Points',
            'Fractional Ownership',
            'Subscription Access',
            'Revenue Sharing'
        ].index(tokenization_model['model_type'])
    )
    
    asset_class = st.selectbox(
        asset_class_label,
        options=[
            'Digital Services',
            'Digital Content',
            'Virtual Real Estate',
            'Real World Assets (RWA)',
            'Financial Instruments',
            'Collectibles',
            'Intellectual Property',
            'Infrastructure'
        ],
        index=[
            'Digital Services',
            'Digital Content',
            'Virtual Real Estate',
            'Real World Assets (RWA)',
            'Financial Instruments',
            'Collectibles',
            'Intellectual Property',
            'Infrastructure'
        ].index(tokenization_model['asset_class'])
    )
    
    target_market = st.selectbox(
        "Target Market",
        options=['Global', 'Regional', 'National', 'Enterprise', 'Retail'],
        index=['Global', 'Regional', 'National', 'Enterprise', 'Retail'].index(tokenization_model['target_market'])
    )
    
    user_rights = st.multiselect(
        "User Rights",
        options=['Access', 'Usage', 'Ownership', 'Governance', 'Profit Sharing', 'Transfer', 'Redemption'],
        default=tokenization_model['user_rights']
    )

with col2:
    st.subheader(compliance_label)
    
    compliance_features = {}
    
    compliance_features['KYC Required'] = st.checkbox(
        "KYC Required",
        value=tokenization_model['compliance_features'].get('KYC Required', False),
        help="Users must complete Know Your Customer verification"
    )
    
    compliance_features['AML Compliance'] = st.checkbox(
        "AML Compliance",
        value=tokenization_model['compliance_features'].get('AML Compliance', False),
        help="Anti-Money Laundering compliance measures in place"
    )
    
    compliance_features['Transfer Restrictions'] = st.checkbox(
        "Transfer Restrictions",
        value=tokenization_model['compliance_features'].get('Transfer Restrictions', False),
        help="Restrictions on who can buy/sell/transfer tokens"
    )
    
    compliance_features['Accredited Investors Only'] = st.checkbox(
        "Accredited Investors Only",
        value=tokenization_model['compliance_features'].get('Accredited Investors Only', False),
        help="Limited to accredited/qualified investors"
    )
    
    st.subheader("Revenue Model")
    
    revenue_model = st.selectbox(
        "Primary Revenue Model",
        options=[
            'Usage Fees', 
            'Transaction Fees', 
            'Subscription', 
            'Asset Appreciation', 
            'Dividend/Yield', 
            'Platform Fees',
            'Premium Features',
            'NFT Sales'
        ],
        index=[
            'Usage Fees', 
            'Transaction Fees', 
            'Subscription', 
            'Asset Appreciation', 
            'Dividend/Yield', 
            'Platform Fees',
            'Premium Features',
            'NFT Sales'
        ].index(tokenization_model['revenue_model'])
    )
    
    # Fee structure
    st.subheader("Fee Structure (%)")
    
    fee_structure = {}
    
    col1, col2 = st.columns(2)
    
    with col1:
        fee_structure['Transaction Fee'] = st.number_input(
            "Transaction Fee (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(tokenization_model['fee_structure'].get('Transaction Fee', 0.5)),
            step=0.1
        )
        
        fee_structure['Platform Fee'] = st.number_input(
            "Platform Fee (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(tokenization_model['fee_structure'].get('Platform Fee', 2.0)),
            step=0.1
        )
    
    with col2:
        fee_structure['Subscription Fee'] = st.number_input(
            "Subscription Fee (USD)",
            min_value=0.0,
            max_value=1000.0,
            value=float(tokenization_model['fee_structure'].get('Subscription Fee', 0.0)),
            step=1.0
        )
        
        fee_structure['Royalty Fee'] = st.number_input(
            "Royalty Fee (%)",
            min_value=0.0,
            max_value=50.0,
            value=float(tokenization_model['fee_structure'].get('Royalty Fee', 0.0)),
            step=0.5
        )

# Model Comparison
st.subheader(model_comparison_title)

# Create comparison data
comparison_data = {
    'Model Type': [
        'Utility Access',
        'Digital Asset Ownership',
        'Security Token',
        'Governance Rights',
        'Reward Points',
        'Fractional Ownership',
        'Subscription Access',
        'Revenue Sharing'
    ],
    'Regulatory Complexity': [2, 3, 5, 3, 1, 4, 2, 4],
    'Technical Complexity': [2, 4, 4, 4, 1, 3, 2, 3],
    'Market Potential': [4, 5, 4, 3, 4, 5, 4, 5],
    'Implementation Time': [2, 3, 5, 3, 1, 4, 2, 3],
    'Ecosystem Fit': [0, 0, 0, 0, 0, 0, 0, 0]  # Will be calculated based on selection
}

# Set ecosystem fit score based on selected model
for i, model in enumerate(comparison_data['Model Type']):
    if model == model_type:
        comparison_data['Ecosystem Fit'][i] = 5
    elif model in [
        'Utility Access', 
        'Digital Asset Ownership'
    ] and model_type in [
        'Utility Access', 
        'Digital Asset Ownership'
    ]:
        comparison_data['Ecosystem Fit'][i] = 4
    elif model in [
        'Security Token', 
        'Revenue Sharing'
    ] and model_type in [
        'Security Token', 
        'Revenue Sharing'
    ]:
        comparison_data['Ecosystem Fit'][i] = 4
    else:
        comparison_data['Ecosystem Fit'][i] = 3

# Create DataFrame
comparison_df = pd.DataFrame(comparison_data)

# Highlight current selection
comparison_df['Selected'] = [model == model_type for model in comparison_df['Model Type']]

# Set up color for the plot
colors = comparison_df['Selected'].map({True: 'red', False: 'blue'})

# Create radar chart
categories = ['Regulatory Complexity', 'Technical Complexity', 'Market Potential', 'Implementation Time', 'Ecosystem Fit']

fig = go.Figure()

# Add traces for selected model
selected_model = comparison_df[comparison_df['Selected'] == True]
fig.add_trace(go.Scatterpolar(
    r=selected_model[categories].values[0],
    theta=categories,
    fill='toself',
    name=selected_model['Model Type'].values[0],
    fillcolor='rgba(255, 0, 0, 0.2)',
    line=dict(color='red')
))

# Add an average trace for comparison
average_values = comparison_df[comparison_df['Selected'] == False][categories].mean().values
fig.add_trace(go.Scatterpolar(
    r=average_values,
    theta=categories,
    fill='toself',
    name='Average (Other Models)',
    fillcolor='rgba(0, 0, 255, 0.2)',
    line=dict(color='blue')
))

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 5]
        )
    ),
    title="Model Characteristics Comparison",
    showlegend=True
)

st.plotly_chart(fig, use_container_width=True)

# Model Comparison Table
st.write("Detailed Model Comparison")
st.dataframe(comparison_df[['Model Type', 'Regulatory Complexity', 'Technical Complexity', 'Market Potential', 'Implementation Time', 'Ecosystem Fit']])

# Benefits and Considerations
st.subheader(benefits_title)

# Dynamic benefits and considerations based on selected model
benefits_considerations = {
    'Utility Access': {
        'Benefits': [
            "Lower regulatory complexity",
            "Straightforward implementation",
            "Broad market applicability",
            "Flexible utility design"
        ],
        'Considerations': [
            "May have limited investment appeal",
            "Requires clear utility value proposition",
            "Market perception may vary by region",
            "Utility must be sustainable"
        ]
    },
    'Digital Asset Ownership': {
        'Benefits': [
            "Strong ownership rights",
            "Potential for asset appreciation",
            "Clear value proposition",
            "Appeals to collectors and investors"
        ],
        'Considerations': [
            "Requires clear ownership definitions",
            "Moderate regulatory complexity",
            "More complex technical implementation",
            "May require custody solutions"
        ]
    },
    'Security Token': {
        'Benefits': [
            "Regulatory clarity in some jurisdictions",
            "Appeals to traditional investors",
            "Established frameworks",
            "Potential for dividend distribution"
        ],
        'Considerations': [
            "Highest regulatory complexity",
            "Jurisdictional limitations",
            "Compliance costs",
            "Restricted transferability"
        ]
    },
    'Governance Rights': {
        'Benefits': [
            "Encourages community participation",
            "Aligns user and protocol interests",
            "Creates engaged ecosystem",
            "May increase token utility"
        ],
        'Considerations': [
            "Governance design complexity",
            "Potential for governance attacks",
            "May not appeal to passive users",
            "Requires ongoing governance refinement"
        ]
    },
    'Reward Points': {
        'Benefits': [
            "Familiar model for users",
            "Low regulatory complexity",
            "Encourages platform engagement",
            "Simple implementation"
        ],
        'Considerations': [
            "Limited investment appeal",
            "May face competition from traditional rewards",
            "Potential inflation concerns",
            "Requires ongoing value proposition"
        ]
    },
    'Fractional Ownership': {
        'Benefits': [
            "Democratizes access to expensive assets",
            "Strong value proposition",
            "Appeals to new investor demographics",
            "Leverages blockchain's strengths"
        ],
        'Considerations': [
            "Complex legal framework",
            "Regulatory uncertainty in some regions",
            "Requires clear fractional rights definition",
            "May have custody challenges"
        ]
    },
    'Subscription Access': {
        'Benefits': [
            "Predictable revenue stream",
            "Familiar business model",
            "Clear value proposition",
            "Low technical complexity"
        ],
        'Considerations': [
            "Competes with traditional subscriptions",
            "Requires ongoing value delivery",
            "May have limited token appreciation",
            "User churn concerns"
        ]
    },
    'Revenue Sharing': {
        'Benefits': [
            "Aligns user and platform incentives",
            "Clear value proposition",
            "Passive income potential",
            "May qualify as productive asset"
        ],
        'Considerations': [
            "Potential security classification",
            "Revenue calculation transparency",
            "Legal and tax implications",
            "Platform must be profitable"
        ]
    }
}

# Display benefits and considerations for selected model
selected_bc = benefits_considerations.get(model_type, {
    'Benefits': ["Custom model benefits would appear here."],
    'Considerations': ["Custom model considerations would appear here."]
})

col1, col2 = st.columns(2)

with col1:
    st.write("##### Benefits")
    for benefit in selected_bc['Benefits']:
        st.markdown(f"✅ {benefit}")

with col2:
    st.write("##### Considerations")
    for consideration in selected_bc['Considerations']:
        st.markdown(f"⚠️ {consideration}")

# ROI Simulation
st.subheader(roi_title)

# Set up simulation parameters
col1, col2, col3 = st.columns(3)

with col1:
    initial_investment = st.number_input(
        "Initial Investment (USD)",
        min_value=1000,
        max_value=10000000,
        value=100000,
        step=10000
    )

with col2:
    growth_rate = st.slider(
        "Annual Growth Rate (%)",
        min_value=0,
        max_value=100,
        value=20,
        step=5
    )

with col3:
    years = st.slider(
        "Simulation Years",
        min_value=1,
        max_value=10,
        value=5,
        step=1
    )

# Calculate ROI based on tokenization model
base_multiplier = {
    'Utility Access': 1.0,
    'Digital Asset Ownership': 1.2,
    'Security Token': 0.9,
    'Governance Rights': 0.8,
    'Reward Points': 0.7,
    'Fractional Ownership': 1.1,
    'Subscription Access': 0.9,
    'Revenue Sharing': 1.3
}

model_multiplier = base_multiplier.get(model_type, 1.0)

# Generate ROI projection
projection_data = []
investment_value = initial_investment

for year in range(years + 1):
    if year == 0:
        roi_percentage = 0
    else:
        # Compound growth with model-specific adjustments
        compound_rate = (1 + (growth_rate / 100) * model_multiplier) ** year
        roi_percentage = (compound_rate - 1) * 100
    
    investment_value = initial_investment * (1 + (growth_rate / 100) * model_multiplier) ** year
    
    projection_data.append({
        'Year': year,
        'Investment Value': investment_value,
        'ROI (%)': roi_percentage
    })

# Create DataFrame
projection_df = pd.DataFrame(projection_data)

# Create projection chart
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=projection_df['Year'],
    y=projection_df['Investment Value'],
    mode='lines+markers',
    name='Investment Value',
    line=dict(color='green', width=3),
    hovertemplate='Year %{x}<br>Value: $%{y:,.2f}<extra></extra>'
))

fig.update_layout(
    title=f"Investment Projection ({model_type} Model)",
    xaxis_title="Year",
    yaxis_title="Value (USD)",
    yaxis_tickformat='$,.0f',
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# Projected ROI table
st.write("Projected Return on Investment")
st.dataframe(
    projection_df.style.format({
        'Investment Value': '${:,.2f}',
        'ROI (%)': '{:.2f}%'
    }),
    use_container_width=True
)

# Save tokenization model
if st.button(save_button):
    # Update the session state with new values
    st.session_state.tokenomics_data['tokenization_model'] = {
        'model_type': model_type,
        'asset_class': asset_class,
        'target_market': target_market,
        'user_rights': user_rights,
        'compliance_features': compliance_features,
        'revenue_model': revenue_model,
        'fee_structure': fee_structure
    }
    
    st.success(saved_message)

# Model Selection Guide
with st.expander("Tokenization Model Selection Guide"):
    st.markdown("""
    ### Tokenization Model Selection Guide
    
    #### Model Types Overview
    
    - **Utility Access**: Tokens grant access to services, features, or resources. Example: Basic Attention Token (BAT).
    
    - **Digital Asset Ownership**: Tokens represent ownership of a digital asset. Example: NFTs like CryptoPunks.
    
    - **Security Token**: Tokens that represent investment contracts with expectation of profit. Example: tZERO.
    
    - **Governance Rights**: Tokens that grant voting power in a protocol or organization. Example: Compound (COMP).
    
    - **Reward Points**: Tokens earned and redeemed for participation. Example: Brave browser rewards.
    
    - **Fractional Ownership**: Tokens representing partial ownership of high-value assets. Example: RealT (real estate).
    
    - **Subscription Access**: Token staking or holding grants subscription benefits. Example: Binance's BNB.
    
    - **Revenue Sharing**: Token holders receive a portion of protocol revenue. Example: Curve Finance (CRV).
    
    #### Selecting the Right Model
    
    1. **Value Proposition**: What is the core value your token provides to users?
    
    2. **Regulatory Environment**: Consider the regulatory implications in your target markets.
    
    3. **Technical Feasibility**: Assess your team's ability to implement the chosen model.
    
    4. **Target Audience**: Different models appeal to different user segments.
    
    5. **Business Model Alignment**: The token model should strengthen your core business model.
    
    #### Legal and Regulatory Considerations
    
    - Utility tokens generally face less regulatory scrutiny than security tokens
    - Security tokens may require registration or exemptions in many jurisdictions
    - Revenue sharing models may trigger security classification
    - Always consult with legal experts specialized in blockchain
    
    Remember that a well-designed tokenization model should create value for both users and the protocol ecosystem.
    """)