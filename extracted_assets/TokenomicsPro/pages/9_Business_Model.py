import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils import get_color_scale

# Set page configuration
st.set_page_config(
    page_title="Business Model - TokenomicsLab",
    page_icon="📊",
    layout="wide"
)

# Load language variables
if 'language' not in st.session_state:
    st.session_state.language = 'English'

# Page title and description based on language
if st.session_state.language == 'English':
    title = "Business Model"
    description = """
    This section helps you design and analyze your project's business model, revenue streams, 
    and financial projections.
    """
    revenue_title = "Revenue Streams"
    cost_title = "Cost Structure"
    projection_title = "Financial Projections"
    metrics_title = "Key Business Metrics"
    save_button = "Save Business Model"
    saved_message = "Business model saved!"
elif st.session_state.language == 'Português':
    title = "Modelo de Negócio"
    description = """
    Esta seção ajuda você a projetar e analisar o modelo de negócios do seu projeto, fontes de receita
    e projeções financeiras.
    """
    revenue_title = "Fontes de Receita"
    cost_title = "Estrutura de Custos"
    projection_title = "Projeções Financeiras"
    metrics_title = "Métricas de Negócios Chave"
    save_button = "Salvar Modelo de Negócio"
    saved_message = "Modelo de negócio salvo!"
elif st.session_state.language == 'Español':
    title = "Modelo de Negocio"
    description = """
    Esta sección te ayuda a diseñar y analizar el modelo de negocio de tu proyecto, fuentes de ingresos
    y proyecciones financieras.
    """
    revenue_title = "Fuentes de Ingresos"
    cost_title = "Estructura de Costos"
    projection_title = "Proyecciones Financieras"
    metrics_title = "Métricas Clave de Negocio"
    save_button = "Guardar Modelo de Negocio"
    saved_message = "¡Modelo de negocio guardado!"
else:
    title = "Business Model"
    description = """
    This section helps you design and analyze your project's business model, revenue streams, 
    and financial projections.
    """
    revenue_title = "Revenue Streams"
    cost_title = "Cost Structure"
    projection_title = "Financial Projections"
    metrics_title = "Key Business Metrics"
    save_button = "Save Business Model"
    saved_message = "Business model saved!"

# Page title and description
st.title(title)
st.markdown(description)

# Check if tokenomics data is initialized
if 'tokenomics_data' not in st.session_state:
    st.error("Please start from the main page to initialize your token data.")
    st.stop()

# Initialize business model data if not present
if 'business_model' not in st.session_state.tokenomics_data:
    st.session_state.tokenomics_data['business_model'] = {
        'revenue_streams': {
            'Transaction Fees': {'enabled': True, 'percentage': 0.5, 'growth_rate': 10},
            'Premium Features': {'enabled': True, 'percentage': 10, 'growth_rate': 15},
            'Token Sales': {'enabled': True, 'percentage': 40, 'growth_rate': 5},
            'Staking Rewards': {'enabled': True, 'percentage': 15, 'growth_rate': 20},
            'NFT Sales': {'enabled': False, 'percentage': 0, 'growth_rate': 0},
            'API Services': {'enabled': False, 'percentage': 0, 'growth_rate': 0},
            'Partnerships': {'enabled': False, 'percentage': 0, 'growth_rate': 0},
            'Advertising': {'enabled': False, 'percentage': 0, 'growth_rate': 0}
        },
        'cost_structure': {
            'Development': {'percentage': 35, 'fixed': True},
            'Marketing': {'percentage': 25, 'fixed': False},
            'Operations': {'percentage': 15, 'fixed': True},
            'Legal & Compliance': {'percentage': 10, 'fixed': True},
            'Community': {'percentage': 10, 'fixed': False},
            'Security Audits': {'percentage': 5, 'fixed': False}
        },
        'growth_model': {
            'initial_users': 1000,
            'user_growth_rate': 15,
            'revenue_per_user': 5,
            'retention_rate': 70,
            'burn_rate': 50000
        }
    }

business_model = st.session_state.tokenomics_data['business_model']

# Revenue streams
st.subheader(revenue_title)

revenue_streams = business_model['revenue_streams']
revenue_tabs = st.tabs(["Revenue Sources", "Revenue Breakdown", "Growth Projections"])

with revenue_tabs[0]:
    st.markdown("Configure your primary revenue streams and their relative importance.")
    
    # Create columns for the revenue streams
    col1, col2, col3 = st.columns(3)
    
    # Track updates to revenue streams
    updated_revenue_streams = {}
    
    # Process existing and predefined revenue streams
    all_streams = [
        'Transaction Fees', 'Premium Features', 'Token Sales', 'Staking Rewards',
        'NFT Sales', 'API Services', 'Partnerships', 'Advertising'
    ]
    
    # Split streams into columns
    streams_per_column = (len(all_streams) + 2) // 3
    column_streams = [
        all_streams[:streams_per_column],
        all_streams[streams_per_column:2*streams_per_column],
        all_streams[2*streams_per_column:]
    ]
    
    # Display streams in columns
    for col_idx, column in enumerate([col1, col2, col3]):
        with column:
            for stream in column_streams[col_idx]:
                st.markdown(f"##### {stream}")
                
                # Get existing stream data or defaults
                stream_data = revenue_streams.get(stream, {'enabled': False, 'percentage': 0, 'growth_rate': 0})
                
                # Enable/disable the stream
                enabled = st.checkbox(
                    f"Enable {stream}",
                    value=stream_data.get('enabled', False),
                    key=f"enable_{stream}"
                )
                
                # Configure percentage and growth if enabled
                if enabled:
                    percentage = st.slider(
                        f"{stream} % of Revenue",
                        min_value=0,
                        max_value=100,
                        value=int(stream_data.get('percentage', 0)),
                        key=f"percentage_{stream}"
                    )
                    
                    growth_rate = st.slider(
                        f"{stream} Annual Growth Rate (%)",
                        min_value=-10,
                        max_value=100,
                        value=int(stream_data.get('growth_rate', 10)),
                        key=f"growth_{stream}"
                    )
                else:
                    percentage = 0
                    growth_rate = 0
                
                # Store updated values
                updated_revenue_streams[stream] = {
                    'enabled': enabled,
                    'percentage': percentage,
                    'growth_rate': growth_rate
                }
                
                st.markdown("---")
    
    # Custom revenue stream
    with st.expander("Add Custom Revenue Stream"):
        custom_stream_name = st.text_input("Revenue Stream Name", key="custom_revenue_name")
        
        if custom_stream_name and custom_stream_name not in updated_revenue_streams:
            custom_enabled = st.checkbox("Enable this revenue stream", value=True, key="custom_revenue_enabled")
            
            if custom_enabled:
                custom_percentage = st.slider(
                    f"{custom_stream_name} % of Revenue",
                    min_value=0,
                    max_value=100,
                    value=10,
                    key="custom_revenue_percentage"
                )
                
                custom_growth = st.slider(
                    f"{custom_stream_name} Annual Growth Rate (%)",
                    min_value=-10,
                    max_value=100,
                    value=10,
                    key="custom_revenue_growth"
                )
                
                if st.button("Add Revenue Stream"):
                    updated_revenue_streams[custom_stream_name] = {
                        'enabled': custom_enabled,
                        'percentage': custom_percentage,
                        'growth_rate': custom_growth
                    }
                    st.success(f"Added {custom_stream_name} to revenue streams!")

with revenue_tabs[1]:
    # Create a pie chart of revenue streams
    enabled_streams = {k: v for k, v in updated_revenue_streams.items() if v['enabled']}
    
    if enabled_streams:
        # Normalize percentages if they don't add up to 100%
        total_percentage = sum(stream['percentage'] for stream in enabled_streams.values())
        
        if total_percentage != 100 and total_percentage > 0:
            # Ask if user wants to normalize
            st.warning(f"Your revenue percentages add up to {total_percentage}%, not 100%.")
            if st.button("Normalize to 100%"):
                for stream in enabled_streams:
                    enabled_streams[stream]['percentage'] = (enabled_streams[stream]['percentage'] / total_percentage) * 100
                st.success("Revenue percentages normalized to 100%.")
        
        # Create DataFrame for visualization
        revenue_df = pd.DataFrame({
            'Revenue Stream': list(enabled_streams.keys()),
            'Percentage': [stream['percentage'] for stream in enabled_streams.values()],
            'Growth Rate': [stream['growth_rate'] for stream in enabled_streams.values()]
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie chart
            fig = px.pie(
                revenue_df,
                values='Percentage',
                names='Revenue Stream',
                title="Revenue Breakdown",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Bar chart of growth rates
            fig = px.bar(
                revenue_df,
                x='Revenue Stream',
                y='Growth Rate',
                title="Projected Annual Growth by Revenue Stream",
                color='Growth Rate',
                color_continuous_scale='Viridis'
            )
            fig.update_layout(xaxis_title="Revenue Stream", yaxis_title="Annual Growth Rate (%)")
            st.plotly_chart(fig, use_container_width=True)
        
        # Table with revenue data
        st.subheader("Revenue Streams Summary")
        st.dataframe(revenue_df)
    else:
        st.info("Enable at least one revenue stream to see the breakdown.")

with revenue_tabs[2]:
    st.subheader("Revenue Growth Projections")
    
    # Growth model parameters
    growth_model = business_model['growth_model']
    
    col1, col2 = st.columns(2)
    
    with col1:
        initial_users = st.number_input(
            "Initial Users",
            min_value=100,
            max_value=1000000,
            value=int(growth_model['initial_users']),
            step=100
        )
        
        user_growth_rate = st.slider(
            "Monthly User Growth Rate (%)",
            min_value=1,
            max_value=50,
            value=int(growth_model['user_growth_rate']),
            help="Monthly percentage increase in user base"
        )
    
    with col2:
        revenue_per_user = st.number_input(
            "Average Revenue per User (USD/month)",
            min_value=0.1,
            max_value=1000.0,
            value=float(growth_model['revenue_per_user']),
            step=0.1,
            format="%.2f"
        )
        
        retention_rate = st.slider(
            "Monthly User Retention Rate (%)",
            min_value=50,
            max_value=99,
            value=int(growth_model['retention_rate']),
            help="Percentage of users who remain active month-to-month"
        )
    
    # Generate revenue projections for 3 years (36 months)
    projection_months = 36
    months = list(range(1, projection_months + 1))
    users = [initial_users]
    revenue = [initial_users * revenue_per_user]
    
    for i in range(1, projection_months):
        # Calculate user growth with retention factored in
        new_users = users[-1] * (user_growth_rate / 100)
        retained_users = users[-1] * (retention_rate / 100)
        current_users = retained_users + new_users
        users.append(current_users)
        
        # Calculate revenue
        current_revenue = current_users * revenue_per_user
        revenue.append(current_revenue)
    
    # Create projections dataframe
    projections_df = pd.DataFrame({
        'Month': months,
        'Users': users,
        'Monthly Revenue': revenue,
        'Cumulative Revenue': np.cumsum(revenue)
    })
    
    # Plot the projections
    col1, col2 = st.columns(2)
    
    with col1:
        # User growth chart
        fig = px.line(
            projections_df,
            x='Month',
            y='Users',
            title="Projected User Growth",
            markers=True
        )
        fig.update_layout(xaxis_title="Month", yaxis_title="Active Users")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Revenue growth chart
        fig = px.line(
            projections_df,
            x='Month',
            y=['Monthly Revenue', 'Cumulative Revenue'],
            title="Projected Revenue Growth",
            markers=True
        )
        fig.update_layout(xaxis_title="Month", yaxis_title="Revenue (USD)")
        st.plotly_chart(fig, use_container_width=True)
    
    # Annual summary
    annual_summary = []
    for year in range(1, 4):
        year_data = projections_df[(projections_df['Month'] > (year-1)*12) & (projections_df['Month'] <= year*12)]
        annual_summary.append({
            'Year': year,
            'End Users': int(year_data['Users'].iloc[-1]),
            'Annual Revenue': int(year_data['Monthly Revenue'].sum()),
            'Growth vs Prev': f"{((year_data['Users'].iloc[-1] / users[0]) - 1) * 100:.2f}%" if year == 1 else f"{((year_data['Users'].iloc[-1] / projections_df[projections_df['Month'] == (year-1)*12]['Users'].values[0]) - 1) * 100:.2f}%"
        })
    
    annual_df = pd.DataFrame(annual_summary)
    st.subheader("Annual Summary")
    st.table(annual_df)

# Cost structure
st.subheader(cost_title)

cost_structure = business_model['cost_structure']
updated_cost_structure = {}

cost_tabs = st.tabs(["Cost Categories", "Cost Breakdown", "Burn Rate Analysis"])

with cost_tabs[0]:
    st.markdown("Define your project's cost structure and the approximate percentage of each cost category.")
    
    col1, col2 = st.columns(2)
    
    # Predefined cost categories
    cost_categories = [
        'Development', 'Marketing', 'Operations', 'Legal & Compliance',
        'Community', 'Security Audits', 'Infrastructure', 'Research'
    ]
    
    # Split into two columns
    first_half = cost_categories[:len(cost_categories)//2]
    second_half = cost_categories[len(cost_categories)//2:]
    
    # First column of costs
    with col1:
        for category in first_half:
            st.markdown(f"##### {category}")
            
            # Get existing data or defaults
            category_data = cost_structure.get(category, {'percentage': 0, 'fixed': True})
            
            # Cost percentage
            percentage = st.slider(
                f"{category} % of Costs",
                min_value=0,
                max_value=100,
                value=int(category_data.get('percentage', 0)),
                key=f"cost_{category}"
            )
            
            # Fixed or variable
            fixed = st.checkbox(
                "Fixed Cost",
                value=category_data.get('fixed', True),
                key=f"fixed_{category}",
                help="Fixed costs don't scale with user numbers, variable costs do"
            )
            
            # Store updated values
            updated_cost_structure[category] = {
                'percentage': percentage,
                'fixed': fixed
            }
            
            st.markdown("---")
    
    # Second column of costs
    with col2:
        for category in second_half:
            st.markdown(f"##### {category}")
            
            # Get existing data or defaults
            category_data = cost_structure.get(category, {'percentage': 0, 'fixed': True})
            
            # Cost percentage
            percentage = st.slider(
                f"{category} % of Costs",
                min_value=0,
                max_value=100,
                value=int(category_data.get('percentage', 0)),
                key=f"cost_{category}"
            )
            
            # Fixed or variable
            fixed = st.checkbox(
                "Fixed Cost",
                value=category_data.get('fixed', True),
                key=f"fixed_{category}",
                help="Fixed costs don't scale with user numbers, variable costs do"
            )
            
            # Store updated values
            updated_cost_structure[category] = {
                'percentage': percentage,
                'fixed': fixed
            }
            
            st.markdown("---")
    
    # Custom cost category
    with st.expander("Add Custom Cost Category"):
        custom_cost_name = st.text_input("Cost Category Name", key="custom_cost_name")
        
        if custom_cost_name and custom_cost_name not in updated_cost_structure:
            custom_percentage = st.slider(
                f"{custom_cost_name} % of Costs",
                min_value=0,
                max_value=100,
                value=10,
                key="custom_cost_percentage"
            )
            
            custom_fixed = st.checkbox(
                "Fixed Cost",
                value=True,
                key="custom_cost_fixed",
                help="Fixed costs don't scale with user numbers, variable costs do"
            )
            
            if st.button("Add Cost Category"):
                updated_cost_structure[custom_cost_name] = {
                    'percentage': custom_percentage,
                    'fixed': custom_fixed
                }
                st.success(f"Added {custom_cost_name} to cost structure!")

with cost_tabs[1]:
    # Filter out zero percentage cost categories
    active_costs = {k: v for k, v in updated_cost_structure.items() if v['percentage'] > 0}
    
    if active_costs:
        # Normalize percentages if they don't add up to 100%
        total_percentage = sum(cost['percentage'] for cost in active_costs.values())
        
        if total_percentage != 100 and total_percentage > 0:
            # Ask if user wants to normalize
            st.warning(f"Your cost percentages add up to {total_percentage}%, not 100%.")
            if st.button("Normalize Cost Percentages"):
                for cost in active_costs:
                    active_costs[cost]['percentage'] = (active_costs[cost]['percentage'] / total_percentage) * 100
                st.success("Cost percentages normalized to 100%.")
        
        # Create DataFrame for visualization
        cost_df = pd.DataFrame({
            'Cost Category': list(active_costs.keys()),
            'Percentage': [cost['percentage'] for cost in active_costs.values()],
            'Type': ['Fixed' if cost['fixed'] else 'Variable' for cost in active_costs.values()]
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie chart
            fig = px.pie(
                cost_df,
                values='Percentage',
                names='Cost Category',
                title="Cost Breakdown",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Bar chart split by fixed/variable
            fig = px.bar(
                cost_df,
                x='Cost Category',
                y='Percentage',
                color='Type',
                title="Fixed vs Variable Costs",
                color_discrete_sequence=['#636EFA', '#EF553B']
            )
            fig.update_layout(xaxis_title="Cost Category", yaxis_title="Percentage of Total Costs (%)")
            st.plotly_chart(fig, use_container_width=True)
        
        # Table with cost data
        st.subheader("Cost Structure Summary")
        st.dataframe(cost_df)
        
        # Fixed vs Variable summary
        fixed_costs = cost_df[cost_df['Type'] == 'Fixed']['Percentage'].sum()
        variable_costs = cost_df[cost_df['Type'] == 'Variable']['Percentage'].sum()
        
        # Initialize default values if missing
        if 'fixed_costs' not in locals() or pd.isna(fixed_costs):
            fixed_costs = 70.0
            
        if 'variable_costs' not in locals() or pd.isna(variable_costs):
            variable_costs = 30.0
        
        st.subheader("Fixed vs Variable Split")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Fixed Costs", f"{fixed_costs:.1f}%")
        
        with col2:
            st.metric("Variable Costs", f"{variable_costs:.1f}%")
    else:
        st.info("Add cost categories with percentages greater than 0 to see the breakdown.")

with cost_tabs[2]:
    st.subheader("Burn Rate Analysis")
    
    # Burn rate and runway calculation
    initial_funding = st.number_input(
        "Available Funding (USD)",
        min_value=10000,
        max_value=100000000,
        value=1000000,
        step=10000
    )
    
    monthly_burn = st.number_input(
        "Initial Monthly Burn Rate (USD)",
        min_value=1000,
        max_value=10000000,
        value=int(business_model['growth_model'].get('burn_rate', 50000)),
        step=1000
    )
    
    revenue_offset = st.checkbox(
        "Account for Revenue in Runway Calculation",
        value=True,
        help="Factors projected revenue into the runway calculation"
    )
    
    # Calculate runway
    months = list(range(0, 37))  # 0 to 36 months
    funding_remaining = [initial_funding]
    monthly_burns = [monthly_burn]
    
    for i in range(1, len(months)):
        # Simple burn without revenue
        if not revenue_offset:
            current_burn = monthly_burn
            
            # Adjust for variable costs as company grows
            if 'cost_df' in locals() and not cost_df.empty and 'Type' in cost_df.columns:
                # If we have cost data from previous sections
                variable_costs_pct = cost_df[cost_df['Type'] == 'Variable']['Percentage'].sum()
                if pd.isna(variable_costs_pct) or variable_costs_pct == 0:
                    variable_costs_pct = 30.0  # Default to 30% variable costs
                variable_portion = variable_costs_pct / 100
            else:
                variable_portion = 0.3  # Default: 30% of costs are variable
                
            growth_factor = 1 + (0.05 * (i // 3))  # Increase by 5% every quarter
            current_burn = monthly_burn * (1 + (growth_factor - 1) * variable_portion)
            
            monthly_burns.append(current_burn)
            funding_remaining.append(max(0, funding_remaining[-1] - current_burn))
        else:
            # Get projected revenue if available, otherwise estimate
            if i < len(projections_df):
                month_revenue = projections_df.iloc[i-1]['Monthly Revenue']
            else:
                month_revenue = 0
            
            # Adjust burn rate for variable costs as company grows
            if 'cost_df' in locals() and not cost_df.empty and 'Type' in cost_df.columns:
                # If we have cost data from previous sections
                variable_costs_pct = cost_df[cost_df['Type'] == 'Variable']['Percentage'].sum()
                if pd.isna(variable_costs_pct) or variable_costs_pct == 0:
                    variable_costs_pct = 30.0  # Default to 30% variable costs
                variable_portion = variable_costs_pct / 100
            else:
                variable_portion = 0.3  # Default: 30% of costs are variable
                
            growth_factor = 1 + (0.05 * (i // 3))  # Increase by 5% every quarter
            current_burn = monthly_burn * (1 + (growth_factor - 1) * variable_portion)
            
            # Net burn is burn minus revenue
            net_burn = max(0, current_burn - month_revenue)
            monthly_burns.append(current_burn)
            funding_remaining.append(max(0, funding_remaining[-1] - net_burn))
    
    # Create runway dataframe
    runway_df = pd.DataFrame({
        'Month': months,
        'Funding Remaining': funding_remaining,
        'Monthly Burn': monthly_burns
    })
    
    # If we have revenue projections, add them
    if revenue_offset and 'projections_df' in locals():
        # Extend revenue data if needed
        extended_revenue = projections_df['Monthly Revenue'].tolist()
        if len(extended_revenue) < len(months):
            # Extend with last value or zeros
            extended_revenue.extend([extended_revenue[-1] if extended_revenue else 0] * (len(months) - len(extended_revenue)))
        
        runway_df['Monthly Revenue'] = extended_revenue
        runway_df['Net Burn'] = runway_df['Monthly Burn'] - runway_df['Monthly Revenue']
        runway_df['Net Burn'] = runway_df['Net Burn'].apply(lambda x: max(0, x))
    
    # Calculate runway
    if funding_remaining[-1] > 0:
        runway_months = "36+ months"
    else:
        # Find where funding runs out
        zero_funding = next((i for i, val in enumerate(funding_remaining) if val <= 0), len(funding_remaining))
        runway_months = f"{zero_funding} months"
    
    # Display runway metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Initial Funding", f"${initial_funding:,}")
    
    with col2:
        st.metric("Initial Monthly Burn", f"${monthly_burn:,}")
    
    with col3:
        st.metric("Projected Runway", runway_months)
    
    # Plot the runway
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=runway_df['Month'],
        y=runway_df['Funding Remaining'],
        mode='lines',
        name='Funding Remaining',
        line=dict(color='blue', width=3)
    ))
    
    if 'Net Burn' in runway_df.columns:
        # Add net burn as a bar chart on secondary y-axis
        fig.add_trace(go.Bar(
            x=runway_df['Month'],
            y=runway_df['Net Burn'],
            name='Net Monthly Burn',
            marker=dict(color='red'),
            opacity=0.7,
            yaxis='y2'
        ))
        
        # Add revenue as a bar
        fig.add_trace(go.Bar(
            x=runway_df['Month'],
            y=runway_df['Monthly Revenue'],
            name='Monthly Revenue',
            marker=dict(color='green'),
            opacity=0.7,
            yaxis='y2'
        ))
        
        fig.update_layout(
            title="Funding Runway Projection",
            xaxis_title="Month",
            yaxis_title="Funding Remaining (USD)",
            yaxis2=dict(
                title=dict(
                    text="Monthly Amount (USD)",
                    font=dict(color="red")
                ),
                tickfont=dict(color="red"),
                overlaying="y",
                side="right"
            ),
            barmode='group',
            hovermode="x unified"
        )
    else:
        # Simpler chart without revenue data
        fig.add_trace(go.Bar(
            x=runway_df['Month'],
            y=runway_df['Monthly Burn'],
            name='Monthly Burn',
            marker=dict(color='red'),
            opacity=0.7,
            yaxis='y2'
        ))
        
        fig.update_layout(
            title="Funding Runway Projection",
            xaxis_title="Month",
            yaxis_title="Funding Remaining (USD)",
            yaxis2=dict(
                title=dict(
                    text="Monthly Burn (USD)",
                    font=dict(color="red")
                ),
                tickfont=dict(color="red"),
                overlaying="y",
                side="right"
            ),
            hovermode="x unified"
        )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Sustainability analysis
    if 'Net Burn' in runway_df.columns:
        break_even_month = next((i for i, row in runway_df.iterrows() if row['Monthly Revenue'] >= row['Monthly Burn']), None)
        
        if break_even_month is not None:
            st.success(f"Projected break-even point: Month {break_even_month}")
        else:
            st.warning("No break-even point within the 36-month projection period.")

# Key business metrics
st.subheader(metrics_title)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Profitability Metrics")
    
    # Projected profitability based on revenue and cost models
    if 'projections_df' in locals() and 'runway_df' in locals() and 'Net Burn' in runway_df.columns:
        # Create profit projection
        profit_data = []
        for i in range(min(len(projections_df), len(runway_df))):
            if i < len(projections_df) and i < len(runway_df):
                month = i + 1
                revenue = projections_df.iloc[i]['Monthly Revenue']
                burn = runway_df.iloc[i+1]['Monthly Burn']  # +1 because runway_df starts at month 0
                profit = revenue - burn
                profit_margin = (profit / revenue) * 100 if revenue > 0 else -100
                
                profit_data.append({
                    'Month': month,
                    'Revenue': revenue,
                    'Costs': burn,
                    'Profit': profit,
                    'Margin': profit_margin
                })
        
        profit_df = pd.DataFrame(profit_data)
        
        # Plot profit/loss
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=profit_df['Month'],
            y=profit_df['Profit'],
            name='Monthly Profit/Loss',
            marker=dict(
                color=profit_df['Profit'].apply(lambda x: 'green' if x >= 0 else 'red')
            )
        ))
        
        fig.add_trace(go.Scatter(
            x=profit_df['Month'],
            y=profit_df['Margin'],
            mode='lines+markers',
            name='Profit Margin (%)',
            yaxis='y2',
            line=dict(color='blue', width=2)
        ))
        
        fig.update_layout(
            title="Projected Profitability",
            xaxis_title="Month",
            yaxis_title="Profit/Loss (USD)",
            yaxis2=dict(
                title=dict(
                    text="Profit Margin (%)",
                    font=dict(color="blue")
                ),
                tickfont=dict(color="blue"),
                overlaying="y",
                side="right",
                range=[-100, 100]
            ),
            hovermode="x unified"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Key financial metrics
        last_month = profit_df.iloc[-1]
        
        st.metric(
            "Projected Monthly Profit at Month 36",
            f"${last_month['Profit']:,.2f}",
            f"{last_month['Margin']:.1f}% margin"
        )
        
        # Calculate ROI over the 3-year period
        total_investment = initial_funding
        total_profit = profit_df[profit_df['Profit'] > 0]['Profit'].sum()
        roi = (total_profit / total_investment) * 100 if total_investment > 0 else 0
        
        st.metric(
            "3-Year ROI",
            f"{roi:.1f}%"
        )
    else:
        st.info("Complete the revenue and cost projections to view profitability metrics.")

with col2:
    st.markdown("### User Economics")
    
    if 'projections_df' in locals():
        # Calculate LTV (Lifetime Value) based on revenue per user and retention
        monthly_churn = (100 - retention_rate) / 100
        avg_user_lifetime = 1 / monthly_churn if monthly_churn > 0 else 36  # In months
        lifetime_value = revenue_per_user * avg_user_lifetime
        
        # Estimated customer acquisition cost
        if 'cost_df' in locals() and 'Marketing' in cost_df['Cost Category'].values:
            # Get marketing percentage
            marketing_pct = cost_df[cost_df['Cost Category'] == 'Marketing']['Percentage'].values[0]
            total_monthly_cost = monthly_burn
            marketing_cost = total_monthly_cost * (marketing_pct / 100)
            
            # Assume first month's new users came from marketing
            first_month_new_users = projections_df.iloc[0]['Users']
            cac = marketing_cost / first_month_new_users if first_month_new_users > 0 else 0
        else:
            # Estimate CAC
            cac = revenue_per_user * 3  # Rough estimate
        
        # LTV:CAC ratio
        ltv_cac_ratio = lifetime_value / cac if cac > 0 else 0
        
        # Display user metrics
        st.metric(
            "Customer Lifetime Value (LTV)",
            f"${lifetime_value:.2f}",
            f"Avg. lifetime: {avg_user_lifetime:.1f} months"
        )
        
        st.metric(
            "Customer Acquisition Cost (CAC)",
            f"${cac:.2f}"
        )
        
        st.metric(
            "LTV:CAC Ratio",
            f"{ltv_cac_ratio:.2f}",
            "Good" if ltv_cac_ratio >= 3 else "Needs improvement"
        )
        
        # Time to recover CAC
        months_to_recover = cac / revenue_per_user if revenue_per_user > 0 else float('inf')
        
        st.metric(
            "Months to Recover CAC",
            f"{months_to_recover:.1f}" if months_to_recover != float('inf') else "∞"
        )
        
        # Create user economics chart
        months_to_show = min(36, int(avg_user_lifetime * 2))
        
        user_economics = []
        cumulative_revenue = 0
        
        for month in range(1, months_to_show + 1):
            survival_prob = (retention_rate / 100) ** (month - 1)
            month_revenue = revenue_per_user * survival_prob
            cumulative_revenue += month_revenue
            
            user_economics.append({
                'Month': month,
                'Survival Probability': survival_prob * 100,
                'Monthly Revenue': month_revenue,
                'Cumulative Revenue': cumulative_revenue,
                'Net Value': cumulative_revenue - cac
            })
        
        user_econ_df = pd.DataFrame(user_economics)
        
        # Plot user economics
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=user_econ_df['Month'],
            y=user_econ_df['Monthly Revenue'],
            name='Monthly Revenue',
            marker=dict(color='green'),
            opacity=0.7
        ))
        
        fig.add_trace(go.Scatter(
            x=user_econ_df['Month'],
            y=user_econ_df['Cumulative Revenue'],
            mode='lines+markers',
            name='Cumulative Revenue',
            line=dict(color='blue', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=user_econ_df['Month'],
            y=user_econ_df['Net Value'],
            mode='lines',
            name='Net User Value',
            line=dict(color='purple', width=2, dash='dash')
        ))
        
        # Add horizontal line for CAC
        fig.add_hline(
            y=cac, 
            line_dash="dash", 
            line_color="red",
            annotation_text=f"CAC: ${cac:.2f}",
            annotation_position="top right"
        )
        
        fig.update_layout(
            title="User Economics Over Time",
            xaxis_title="Month",
            yaxis_title="Value (USD)",
            hovermode="x unified"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Complete the revenue and user growth projections to view user economics.")

# Save business model
if st.button(save_button):
    # Update growth model with new values
    updated_growth_model = {
        'initial_users': initial_users,
        'user_growth_rate': user_growth_rate,
        'revenue_per_user': revenue_per_user,
        'retention_rate': retention_rate,
        'burn_rate': monthly_burn
    }
    
    # Update the session state with new values
    st.session_state.tokenomics_data['business_model'] = {
        'revenue_streams': updated_revenue_streams,
        'cost_structure': updated_cost_structure,
        'growth_model': updated_growth_model
    }
    
    st.success(saved_message)

# Business Model Canvas
with st.expander("Business Model Canvas Guide"):
    st.markdown("""
    ### Business Model Canvas
    
    The Business Model Canvas is a strategic management template for developing new business models or documenting existing ones. Here's a brief overview of the key components:
    
    #### 1. Value Propositions
    - What value do you deliver to customers?
    - Which customer problems are you solving?
    
    #### 2. Customer Segments
    - Who are your most important customers?
    - What are their needs and behaviors?
    
    #### 3. Channels
    - How do you reach your customer segments?
    - How are your channels integrated?
    
    #### 4. Customer Relationships
    - What type of relationship does each customer segment expect?
    - How costly are they to maintain?
    
    #### 5. Revenue Streams
    - What are customers willing to pay for?
    - How do they currently pay?
    - How would they prefer to pay?
    
    #### 6. Key Resources
    - What key assets are required for your value propositions?
    
    #### 7. Key Activities
    - What key activities do your value propositions require?
    
    #### 8. Key Partnerships
    - Who are your key partners and suppliers?
    - What resources do you acquire from them?
    
    #### 9. Cost Structure
    - What are the most important costs in your business model?
    - Which key resources and activities are most expensive?
    
    ### Web3 Business Model Considerations
    
    In Web3 projects, traditional business models are often adapted to include:
    
    - **Token Utility**: How the token provides value in the ecosystem
    - **Network Effects**: How value increases with more users/contributors
    - **Governance Rights**: How token holders participate in decision-making
    - **Value Capture**: How the protocol or project retains value
    - **Value Distribution**: How value is shared with participants
    
    Consider how your token economics and business model work together to create a sustainable system.
    """)