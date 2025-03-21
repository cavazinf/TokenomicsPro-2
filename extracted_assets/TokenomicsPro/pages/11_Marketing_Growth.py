import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Set page configuration
st.set_page_config(
    page_title="Marketing & Growth - TokenomicsLab",
    page_icon="📊",
    layout="wide",
)

# Initialize language if not set
if 'language' not in st.session_state:
    st.session_state.language = 'English'

# Page title and description based on language
if st.session_state.language == 'English':
    title = "Marketing & Growth"
    description = """
    Plan and model your token's marketing and growth strategies to optimize adoption and community engagement.
    """
elif st.session_state.language == 'Português':
    title = "Marketing e Crescimento"
    description = """
    Planeje e modele as estratégias de marketing e crescimento do seu token para otimizar a adoção e o engajamento da comunidade.
    """
elif st.session_state.language == 'Español':
    title = "Marketing y Crecimiento"
    description = """
    Planifica y modela las estrategias de marketing y crecimiento de tu token para optimizar la adopción y el compromiso de la comunidad.
    """
else:
    title = "Marketing & Growth"
    description = """
    Plan and model your token's marketing and growth strategies to optimize adoption and community engagement.
    """

st.title(title)
st.markdown(description)

# Define multi-language labels and texts
if st.session_state.language == 'English':
    # Sections
    strategy_section = "Marketing Strategy"
    acquisition_section = "User Acquisition"
    budget_section = "Marketing Budget"
    timeline_section = "Growth Timeline"
    metrics_section = "Key Growth Metrics"
    community_section = "Community Building"
    
    # Marketing Strategy
    strategy_text = "Define your core marketing strategy and key value propositions."
    strategy_type = "Strategy Type"
    value_prop = "Value Proposition"
    target_audience = "Target Audience"
    key_messages = "Key Messages"
    
    # User Acquisition
    acquisition_text = "Plan your user acquisition channels and expected conversion metrics."
    add_channel_btn = "Add Acquisition Channel"
    channel_name = "Channel Name"
    reach = "Estimated Reach"
    conversion = "Conversion Rate (%)"
    cost_per_user = "Cost Per User (USD)"
    cac = "Customer Acquisition Cost (CAC)"
    
    # Marketing Budget
    budget_text = "Allocate your marketing budget across different channels and activities."
    total_budget_label = "Total Marketing Budget (USD)"
    budget_allocation = "Budget Allocation"
    calculate_roi_btn = "Calculate Marketing ROI"
    roi_label = "Return on Investment (ROI)"
    
    # Growth Timeline
    timeline_text = "Set milestone targets for user growth and token adoption."
    months = "Months"
    target_users = "Target Users"
    token_stakers = "Token Stakers"
    token_holders = "Token Holders"
    active_users = "Active Users"
    
    # Key Growth Metrics
    metrics_text = "Track and project key growth metrics for your token."
    metric_name = "Metric Name"
    current_value = "Current Value"
    target_value = "Target Value"
    timeframe = "Timeframe"
    
    # Community Building
    community_text = "Develop strategies for building and engaging your community."
    platform = "Platform"
    members = "Members"
    engagement = "Engagement Rate (%)"
    growth_rate = "Monthly Growth Rate (%)"
    strategies = "Engagement Strategies"
    
elif st.session_state.language == 'Português':
    # Sections
    strategy_section = "Estratégia de Marketing"
    acquisition_section = "Aquisição de Usuários"
    budget_section = "Orçamento de Marketing"
    timeline_section = "Cronograma de Crescimento"
    metrics_section = "Métricas Principais de Crescimento"
    community_section = "Construção de Comunidade"
    
    # Marketing Strategy
    strategy_text = "Defina sua estratégia central de marketing e propostas de valor principais."
    strategy_type = "Tipo de Estratégia"
    value_prop = "Proposta de Valor"
    target_audience = "Público-Alvo"
    key_messages = "Mensagens Principais"
    
    # User Acquisition
    acquisition_text = "Planeje seus canais de aquisição de usuários e métricas esperadas de conversão."
    add_channel_btn = "Adicionar Canal de Aquisição"
    channel_name = "Nome do Canal"
    reach = "Alcance Estimado"
    conversion = "Taxa de Conversão (%)"
    cost_per_user = "Custo Por Usuário (USD)"
    cac = "Custo de Aquisição de Cliente (CAC)"
    
    # Marketing Budget
    budget_text = "Aloque seu orçamento de marketing entre diferentes canais e atividades."
    total_budget_label = "Orçamento Total de Marketing (USD)"
    budget_allocation = "Alocação de Orçamento"
    calculate_roi_btn = "Calcular ROI de Marketing"
    roi_label = "Retorno sobre Investimento (ROI)"
    
    # Growth Timeline
    timeline_text = "Defina metas de marcos para crescimento de usuários e adoção de tokens."
    months = "Meses"
    target_users = "Usuários Alvo"
    token_stakers = "Stakers de Token"
    token_holders = "Detentores de Token"
    active_users = "Usuários Ativos"
    
    # Key Growth Metrics
    metrics_text = "Acompanhe e projete métricas principais de crescimento para seu token."
    metric_name = "Nome da Métrica"
    current_value = "Valor Atual"
    target_value = "Valor Alvo"
    timeframe = "Período"
    
    # Community Building
    community_text = "Desenvolva estratégias para construir e engajar sua comunidade."
    platform = "Plataforma"
    members = "Membros"
    engagement = "Taxa de Engajamento (%)"
    growth_rate = "Taxa de Crescimento Mensal (%)"
    strategies = "Estratégias de Engajamento"
    
elif st.session_state.language == 'Español':
    # Sections
    strategy_section = "Estrategia de Marketing"
    acquisition_section = "Adquisición de Usuarios"
    budget_section = "Presupuesto de Marketing"
    timeline_section = "Cronograma de Crecimiento"
    metrics_section = "Métricas Clave de Crecimiento"
    community_section = "Construcción de Comunidad"
    
    # Marketing Strategy
    strategy_text = "Define tu estrategia central de marketing y propuestas de valor clave."
    strategy_type = "Tipo de Estrategia"
    value_prop = "Propuesta de Valor"
    target_audience = "Público Objetivo"
    key_messages = "Mensajes Clave"
    
    # User Acquisition
    acquisition_text = "Planifica tus canales de adquisición de usuarios y métricas esperadas de conversión."
    add_channel_btn = "Añadir Canal de Adquisición"
    channel_name = "Nombre del Canal"
    reach = "Alcance Estimado"
    conversion = "Tasa de Conversión (%)"
    cost_per_user = "Costo Por Usuario (USD)"
    cac = "Costo de Adquisición de Cliente (CAC)"
    
    # Marketing Budget
    budget_text = "Asigna tu presupuesto de marketing entre diferentes canales y actividades."
    total_budget_label = "Presupuesto Total de Marketing (USD)"
    budget_allocation = "Asignación de Presupuesto"
    calculate_roi_btn = "Calcular ROI de Marketing"
    roi_label = "Retorno de Inversión (ROI)"
    
    # Growth Timeline
    timeline_text = "Establece objetivos para el crecimiento de usuarios y la adopción de tokens."
    months = "Meses"
    target_users = "Usuarios Objetivo"
    token_stakers = "Stakers de Token"
    token_holders = "Poseedores de Token"
    active_users = "Usuarios Activos"
    
    # Key Growth Metrics
    metrics_text = "Rastrea y proyecta métricas clave de crecimiento para tu token."
    metric_name = "Nombre de la Métrica"
    current_value = "Valor Actual"
    target_value = "Valor Objetivo"
    timeframe = "Plazo"
    
    # Community Building
    community_text = "Desarrolla estrategias para construir y comprometer a tu comunidad."
    platform = "Plataforma"
    members = "Miembros"
    engagement = "Tasa de Compromiso (%)"
    growth_rate = "Tasa de Crecimiento Mensual (%)"
    strategies = "Estrategias de Compromiso"
    
else:
    # Sections
    strategy_section = "Marketing Strategy"
    acquisition_section = "User Acquisition"
    budget_section = "Marketing Budget"
    timeline_section = "Growth Timeline"
    metrics_section = "Key Growth Metrics"
    community_section = "Community Building"
    
    # Marketing Strategy
    strategy_text = "Define your core marketing strategy and key value propositions."
    strategy_type = "Strategy Type"
    value_prop = "Value Proposition"
    target_audience = "Target Audience"
    key_messages = "Key Messages"
    
    # User Acquisition
    acquisition_text = "Plan your user acquisition channels and expected conversion metrics."
    add_channel_btn = "Add Acquisition Channel"
    channel_name = "Channel Name"
    reach = "Estimated Reach"
    conversion = "Conversion Rate (%)"
    cost_per_user = "Cost Per User (USD)"
    cac = "Customer Acquisition Cost (CAC)"
    
    # Marketing Budget
    budget_text = "Allocate your marketing budget across different channels and activities."
    total_budget_label = "Total Marketing Budget (USD)"
    budget_allocation = "Budget Allocation"
    calculate_roi_btn = "Calculate Marketing ROI"
    roi_label = "Return on Investment (ROI)"
    
    # Growth Timeline
    timeline_text = "Set milestone targets for user growth and token adoption."
    months = "Months"
    target_users = "Target Users"
    token_stakers = "Token Stakers"
    token_holders = "Token Holders"
    active_users = "Active Users"
    
    # Key Growth Metrics
    metrics_text = "Track and project key growth metrics for your token."
    metric_name = "Metric Name"
    current_value = "Current Value"
    target_value = "Target Value"
    timeframe = "Timeframe"
    
    # Community Building
    community_text = "Develop strategies for building and engaging your community."
    platform = "Platform"
    members = "Members"
    engagement = "Engagement Rate (%)"
    growth_rate = "Monthly Growth Rate (%)"
    strategies = "Engagement Strategies"

# Initialize session state for marketing and growth data
if 'marketing_growth' not in st.session_state:
    st.session_state.marketing_growth = {
        'strategy': {
            'type': 'Community-Driven Growth',
            'value_proposition': '',
            'target_audience': '',
            'key_messages': []
        },
        'acquisition_channels': [],
        'marketing_budget': 500000,  # $500k initial budget
        'budget_allocation': {
            'Social Media': 30,
            'Influencer Marketing': 20,
            'Content Creation': 15,
            'Community Events': 15,
            'PR & Media': 10,
            'Paid Ads': 5,
            'Other': 5
        },
        'growth_timeline': {
            'months': [3, 6, 12, 18, 24],
            'users': [1000, 5000, 20000, 50000, 100000],
            'stakers': [200, 1000, 5000, 15000, 35000],
            'holders': [500, 2500, 10000, 30000, 70000],
            'active_users': [800, 4000, 16000, 40000, 80000]
        },
        'growth_metrics': [],
        'community': [
            {
                'platform': 'Discord',
                'members': 500,
                'engagement': 20,
                'growth_rate': 15,
                'strategies': 'Regular AMAs, exclusive content'
            },
            {
                'platform': 'Twitter',
                'members': 2000,
                'engagement': 5,
                'growth_rate': 10,
                'strategies': 'Daily updates, content sharing'
            }
        ]
    }

# Marketing Strategy Section
st.header(strategy_section)
st.markdown(strategy_text)

strategy_col1, strategy_col2 = st.columns(2)

with strategy_col1:
    strategy_types = [
        'Community-Driven Growth',
        'Influencer Marketing',
        'Content Marketing',
        'Partnerships & Integrations',
        'Airdrops & Incentives',
        'Growth Hacking',
        'Traditional Marketing'
    ]
    
    selected_strategy = st.selectbox(
        strategy_type,
        options=strategy_types,
        index=strategy_types.index(st.session_state.marketing_growth['strategy']['type']) if st.session_state.marketing_growth['strategy']['type'] in strategy_types else 0
    )
    
    if selected_strategy != st.session_state.marketing_growth['strategy']['type']:
        st.session_state.marketing_growth['strategy']['type'] = selected_strategy
    
    value_proposition = st.text_area(
        value_prop,
        value=st.session_state.marketing_growth['strategy']['value_proposition'],
        height=100
    )
    
    if value_proposition != st.session_state.marketing_growth['strategy']['value_proposition']:
        st.session_state.marketing_growth['strategy']['value_proposition'] = value_proposition

with strategy_col2:
    target_audience_text = st.text_area(
        target_audience,
        value=st.session_state.marketing_growth['strategy']['target_audience'],
        height=100
    )
    
    if target_audience_text != st.session_state.marketing_growth['strategy']['target_audience']:
        st.session_state.marketing_growth['strategy']['target_audience'] = target_audience_text
    
    # Convert list to string for textarea
    key_messages_text = '\n'.join(st.session_state.marketing_growth['strategy']['key_messages']) if st.session_state.marketing_growth['strategy']['key_messages'] else ''
    
    key_messages_input = st.text_area(
        key_messages,
        value=key_messages_text,
        height=100,
        help="Enter one message per line"
    )
    
    # Convert back to list and update session state
    if key_messages_input:
        new_messages = [msg.strip() for msg in key_messages_input.split('\n') if msg.strip()]
        if new_messages != st.session_state.marketing_growth['strategy']['key_messages']:
            st.session_state.marketing_growth['strategy']['key_messages'] = new_messages

# User Acquisition Section
st.header(acquisition_section)
st.markdown(acquisition_text)

# Add a new acquisition channel
with st.expander(add_channel_btn):
    acq_col1, acq_col2 = st.columns(2)
    
    with acq_col1:
        new_channel = st.text_input(channel_name)
        new_reach = st.number_input(
            reach,
            min_value=0,
            value=10000,
            step=1000
        )
    
    with acq_col2:
        new_conversion = st.number_input(
            conversion,
            min_value=0.0,
            max_value=100.0,
            value=2.0,
            step=0.1
        )
        new_cost = st.number_input(
            cost_per_user,
            min_value=0.0,
            value=5.0,
            step=0.5
        )
    
    if st.button(add_channel_btn):
        if new_channel:  # Only add if channel has a name
            st.session_state.marketing_growth['acquisition_channels'].append({
                'name': new_channel,
                'reach': new_reach,
                'conversion': new_conversion,
                'cost_per_user': new_cost
            })
            st.success(f"Added {new_channel} to acquisition channels")

# Display acquisition channels if available
if st.session_state.marketing_growth['acquisition_channels']:
    # Prepare data for visualization
    channel_data = pd.DataFrame(st.session_state.marketing_growth['acquisition_channels'])
    
    # Calculate expected users and total cost
    channel_data['expected_users'] = (channel_data['reach'] * channel_data['conversion'] / 100).astype(int)
    channel_data['total_cost'] = channel_data['expected_users'] * channel_data['cost_per_user']
    
    # Display acquisition funnel
    st.subheader("Acquisition Funnel")
    
    fig = px.funnel(
        channel_data,
        x='expected_users',
        y='name',
        title="Expected User Acquisition by Channel",
    )
    fig.update_layout(xaxis_title="Expected Users", yaxis_title=channel_name)
    st.plotly_chart(fig, use_container_width=True)
    
    # Display channel metrics
    st.subheader(cac)
    
    # Format for display
    display_data = channel_data.copy()
    display_data['reach'] = display_data['reach'].apply(lambda x: f"{x:,}")
    display_data['conversion'] = display_data['conversion'].apply(lambda x: f"{x:.1f}%")
    display_data['cost_per_user'] = display_data['cost_per_user'].apply(lambda x: f"${x:.2f}")
    display_data['expected_users'] = display_data['expected_users'].apply(lambda x: f"{x:,}")
    display_data['total_cost'] = display_data['total_cost'].apply(lambda x: f"${x:,.2f}")
    
    st.table(display_data)
    
    # Calculate overall CAC
    total_users = channel_data['expected_users'].sum()
    total_cost = channel_data['total_cost'].sum()
    overall_cac = total_cost / total_users if total_users > 0 else 0
    
    st.metric(f"Overall {cac}", f"${overall_cac:.2f}")
else:
    st.info(f"No acquisition channels added yet. Use the '{add_channel_btn}' section to add channels.")

# Marketing Budget Section
st.header(budget_section)
st.markdown(budget_text)

budget_col1, budget_col2 = st.columns([1, 2])

with budget_col1:
    total_budget = st.number_input(
        total_budget_label,
        min_value=0,
        value=st.session_state.marketing_growth['marketing_budget'],
        step=10000,
        format="%d"
    )
    
    if total_budget != st.session_state.marketing_growth['marketing_budget']:
        st.session_state.marketing_growth['marketing_budget'] = total_budget

with budget_col2:
    # Create a bar chart for budget allocation
    allocation_data = pd.DataFrame({
        'Category': list(st.session_state.marketing_growth['budget_allocation'].keys()),
        'Percentage': list(st.session_state.marketing_growth['budget_allocation'].values()),
        'Amount': [total_budget * (p/100) for p in st.session_state.marketing_growth['budget_allocation'].values()]
    })
    
    fig = px.bar(
        allocation_data,
        x='Category',
        y='Percentage',
        title=budget_allocation,
        text=allocation_data['Percentage'].apply(lambda x: f"{x:.1f}%"),
        color='Category'
    )
    fig.update_layout(yaxis_title="Percentage (%)", xaxis_title="Category")
    st.plotly_chart(fig, use_container_width=True)

# Allow users to adjust the budget allocation
st.subheader(budget_allocation)

# Create sliders for each budget category
allocation_sum = 0
updated_allocation = {}

# Create columns for better layout
allocation_cols = st.columns(2)
col_idx = 0

for category, percentage in st.session_state.marketing_growth['budget_allocation'].items():
    with allocation_cols[col_idx]:
        new_percentage = st.slider(
            f"{category} (%)",
            min_value=0,
            max_value=100,
            value=int(percentage),
            key=f"budget_{category}"
        )
        updated_allocation[category] = new_percentage
        allocation_sum += new_percentage
    
    # Switch columns for next item
    col_idx = (col_idx + 1) % 2

# Check if allocation adds up to 100%
if allocation_sum != 100:
    st.warning(f"Your budget allocation adds up to {allocation_sum}%. Please adjust to total 100%.")
else:
    # Update session state if allocation has changed
    if updated_allocation != st.session_state.marketing_growth['budget_allocation']:
        st.session_state.marketing_growth['budget_allocation'] = updated_allocation
        st.success("Budget allocation updated successfully")

# Calculate ROI if we have acquisition channel data
if st.button(calculate_roi_btn) and st.session_state.marketing_growth['acquisition_channels']:
    total_users = sum([ch['reach'] * ch['conversion'] / 100 for ch in st.session_state.marketing_growth['acquisition_channels']])
    
    # Assuming a value per user based on token price and expected holdings
    token_price = st.session_state.tokenomics_data.get('initial_price', 0.01)
    avg_tokens_per_user = 1000  # Assumption
    user_value = token_price * avg_tokens_per_user
    
    total_value = total_users * user_value
    roi = ((total_value - total_budget) / total_budget) * 100 if total_budget > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Expected Users", f"{int(total_users):,}")
    
    with col2:
        st.metric("Total Investment", f"${total_budget:,.2f}")
    
    with col3:
        st.metric(roi_label, f"{roi:.2f}%", delta=f"{roi:.1f}%" if roi > 0 else f"{roi:.1f}%")
    
    st.info(f"ROI calculation assumes an average value of ${user_value:.2f} per user based on expected token holdings.")

# Growth Timeline Section
st.header(timeline_section)
st.markdown(timeline_text)

# Create growth timeline chart
timeline_data = {
    'Months': st.session_state.marketing_growth['growth_timeline']['months'],
    target_users: st.session_state.marketing_growth['growth_timeline']['users'],
    token_holders: st.session_state.marketing_growth['growth_timeline']['holders'],
    token_stakers: st.session_state.marketing_growth['growth_timeline']['stakers'],
    active_users: st.session_state.marketing_growth['growth_timeline']['active_users']
}

timeline_df = pd.DataFrame(timeline_data)

# Plot growth timeline
fig = px.line(
    timeline_df,
    x='Months',
    y=[target_users, token_holders, token_stakers, active_users],
    title="Projected Growth Timeline",
    labels={'value': 'Number of Users/Holders', 'variable': 'Metric'}
)
fig.update_layout(hovermode="x unified", xaxis_title=months)
st.plotly_chart(fig, use_container_width=True)

# Allow adjusting growth timeline targets
st.subheader("Growth Target Adjustments")

with st.expander("Adjust Growth Targets"):
    # Create fields for each month's target
    for i, month in enumerate(st.session_state.marketing_growth['growth_timeline']['months']):
        st.write(f"Month {month}")
        cols = st.columns(4)
        
        new_users = cols[0].number_input(
            target_users,
            min_value=0,
            value=st.session_state.marketing_growth['growth_timeline']['users'][i],
            key=f"users_month_{month}"
        )
        
        new_holders = cols[1].number_input(
            token_holders,
            min_value=0,
            value=st.session_state.marketing_growth['growth_timeline']['holders'][i],
            key=f"holders_month_{month}"
        )
        
        new_stakers = cols[2].number_input(
            token_stakers,
            min_value=0,
            value=st.session_state.marketing_growth['growth_timeline']['stakers'][i],
            key=f"stakers_month_{month}"
        )
        
        new_active = cols[3].number_input(
            active_users,
            min_value=0,
            value=st.session_state.marketing_growth['growth_timeline']['active_users'][i],
            key=f"active_month_{month}"
        )
        
        # Update session state
        st.session_state.marketing_growth['growth_timeline']['users'][i] = new_users
        st.session_state.marketing_growth['growth_timeline']['holders'][i] = new_holders
        st.session_state.marketing_growth['growth_timeline']['stakers'][i] = new_stakers
        st.session_state.marketing_growth['growth_timeline']['active_users'][i] = new_active

# Key Growth Metrics Section
st.header(metrics_section)
st.markdown(metrics_text)

# Add new growth metric
with st.expander("Add Growth Metric"):
    metric_col1, metric_col2 = st.columns(2)
    
    with metric_col1:
        metric_name_input = st.text_input("Metric Name", key="new_metric_name")
        current_value_input = st.number_input("Current Value", value=0, key="new_metric_current")
    
    with metric_col2:
        target_value_input = st.number_input("Target Value", value=0, key="new_metric_target")
        timeframe_options = ["3 months", "6 months", "1 year", "2 years"]
        timeframe_input = st.selectbox("Timeframe", options=timeframe_options, key="new_metric_timeframe")
    
    if st.button("Add Metric"):
        if metric_name_input:
            st.session_state.marketing_growth['growth_metrics'].append({
                'name': metric_name_input,
                'current': current_value_input,
                'target': target_value_input,
                'timeframe': timeframe_input
            })
            st.success(f"Added {metric_name_input} to growth metrics")

# Display growth metrics if available
if st.session_state.marketing_growth['growth_metrics']:
    metrics_df = pd.DataFrame(st.session_state.marketing_growth['growth_metrics'])
    
    # Calculate progress percentage
    metrics_df['progress'] = metrics_df.apply(
        lambda row: min(100, max(0, (row['current'] / row['target']) * 100)) if row['target'] > 0 else 0, 
        axis=1
    )
    
    # Display metrics as progress bars
    st.subheader("Growth Metrics Progress")
    
    for i, row in metrics_df.iterrows():
        st.write(f"**{row['name']}** ({row['timeframe']})")
        cols = st.columns([3, 1])
        
        # Progress bar
        cols[0].progress(int(row['progress']))
        
        # Current and target values
        cols[1].write(f"{row['current']} / {row['target']} ({row['progress']:.1f}%)")
    
    # Show metrics in a table as well
    st.subheader("Growth Metrics Summary")
    display_metrics = metrics_df.drop(columns=['progress'])
    display_metrics.columns = [metric_name, current_value, target_value, timeframe]
    st.table(display_metrics)
else:
    st.info("No growth metrics added yet. Use the 'Add Growth Metric' section to add metrics.")

# Community Building Section
st.header(community_section)
st.markdown(community_text)

# Add new community platform
with st.expander("Add Community Platform"):
    comm_col1, comm_col2 = st.columns(2)
    
    with comm_col1:
        platform_input = st.text_input("Platform Name", key="new_platform")
        members_input = st.number_input("Number of Members", value=0, min_value=0, key="new_members")
    
    with comm_col2:
        engagement_input = st.number_input("Engagement Rate (%)", value=0.0, min_value=0.0, max_value=100.0, key="new_engagement")
        growth_input = st.number_input("Monthly Growth Rate (%)", value=0.0, min_value=0.0, max_value=100.0, key="new_growth")
    
    strategies_input = st.text_area("Engagement Strategies", key="new_strategies")
    
    if st.button("Add Platform"):
        if platform_input:
            st.session_state.marketing_growth['community'].append({
                'platform': platform_input,
                'members': members_input,
                'engagement': engagement_input,
                'growth_rate': growth_input,
                'strategies': strategies_input
            })
            st.success(f"Added {platform_input} to community platforms")

# Display community platforms if available
if st.session_state.marketing_growth['community']:
    community_df = pd.DataFrame(st.session_state.marketing_growth['community'])
    
    # Create visualization for community platforms
    st.subheader("Community Size by Platform")
    
    fig = px.bar(
        community_df,
        x='platform',
        y='members',
        color='engagement',
        text=community_df['members'].apply(lambda x: f"{x:,}"),
        title="Community Size and Engagement by Platform",
        color_continuous_scale='Viridis',
        labels={'members': 'Number of Members', 'platform': 'Platform', 'engagement': 'Engagement Rate (%)'}
    )
    fig.update_layout(xaxis_title="Platform", yaxis_title="Number of Members")
    st.plotly_chart(fig, use_container_width=True)
    
    # Display community data in a table
    st.subheader("Community Platforms Summary")
    
    display_community = community_df.copy()
    display_community.columns = [platform, members, engagement, growth_rate, strategies]
    # Format numbers for display
    display_community[members] = display_community[members].apply(lambda x: f"{x:,}")
    display_community[engagement] = display_community[engagement].apply(lambda x: f"{x:.1f}%")
    display_community[growth_rate] = display_community[growth_rate].apply(lambda x: f"{x:.1f}%")
    
    st.table(display_community)
    
    # Calculate projected community growth
    months_ahead = [1, 3, 6, 12]
    platforms = community_df['platform'].tolist()
    
    growth_projections = []
    
    for platform_name, members, growth in zip(community_df['platform'], community_df['members'], community_df['growth_rate']):
        platform_projections = {'Platform': platform_name}
        
        for month in months_ahead:
            # Compound growth formula: P(t) = P0 * (1 + r)^t
            projected = int(members * ((1 + growth/100) ** month))
            platform_projections[f"{month} {months}"] = projected
        
        growth_projections.append(platform_projections)
    
    growth_df = pd.DataFrame(growth_projections)
    
    st.subheader("Projected Community Growth")
    st.table(growth_df)
else:
    st.info("No community platforms added yet. Use the 'Add Community Platform' section to add platforms.")

# Footer
st.markdown("---")
st.markdown("TokenomicsLab - Marketing & Growth Module")