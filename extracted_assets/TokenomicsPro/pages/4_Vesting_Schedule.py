import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils import calculate_vesting_release, get_color_scale
from datetime import datetime, timedelta

# Set page configuration
st.set_page_config(
    page_title="Vesting Schedule - TokenomicsLab",
    page_icon="📊",
    layout="wide"
)

# Page title and description
st.title("Token Vesting Schedule Calculator")
st.markdown("""
This section helps you design and visualize token vesting schedules for different stakeholder groups.
Create custom vesting plans with cliff periods, linear vesting, and TGE (Token Generation Event) unlocks.
""")

# Check if tokenomics data is initialized
if 'tokenomics_data' not in st.session_state:
    st.error("Please start from the main page to initialize your token data.")
    st.stop()

# Get data from session state
total_supply = st.session_state.tokenomics_data['total_supply']
allocation_categories = st.session_state.tokenomics_data['allocation_categories']
token_name = st.session_state.tokenomics_data['token_name']
token_symbol = st.session_state.tokenomics_data['token_symbol']

# Initialize vesting schedules if not present
if 'vesting_schedules' not in st.session_state.tokenomics_data:
    st.session_state.tokenomics_data['vesting_schedules'] = {}

# Vesting schedule creation form
st.subheader("Create Vesting Schedule")

col1, col2 = st.columns(2)

with col1:
    # Select category to create vesting for
    selected_category = st.selectbox(
        "Select Allocation Category",
        options=list(allocation_categories.keys())
    )
    
    # Calculate tokens for this category
    category_tokens = total_supply * allocation_categories[selected_category] / 100
    
    st.info(f"Category allocation: {category_tokens:,.0f} tokens ({allocation_categories[selected_category]}% of total supply)")
    
    # Allow user to adjust token amount if needed
    vest_amount = st.number_input(
        "Tokens to Vest",
        min_value=0.0,
        max_value=float(category_tokens),
        value=float(category_tokens),
        step=1000.0
    )

with col2:
    # Vesting parameters
    cliff_period = st.slider(
        "Cliff Period (months)",
        min_value=0,
        max_value=36,
        value=6,
        step=1,
        help="Time before any tokens are released (excluding TGE)"
    )
    
    vesting_period = st.slider(
        "Vesting Period (months)",
        min_value=1,
        max_value=60,
        value=24,
        step=1,
        help="Total duration for the complete vesting schedule"
    )
    
    tge_percentage = st.slider(
        "TGE Release (%)",
        min_value=0.0,
        max_value=100.0,
        value=5.0,
        step=1.0,
        help="Percentage of tokens released at Token Generation Event"
    )

# Calculate and display vesting schedule
if st.button("Calculate Vesting Schedule"):
    with st.spinner("Calculating vesting schedule..."):
        # Calculate vesting schedule
        vesting_schedule = calculate_vesting_release(
            vest_amount,
            cliff_period,
            vesting_period,
            tge_percentage
        )
        
        # Save to session state
        st.session_state.tokenomics_data['vesting_schedules'][selected_category] = {
            'amount': vest_amount,
            'cliff_months': cliff_period,
            'vesting_months': vesting_period,
            'tge_percent': tge_percentage,
            'schedule': vesting_schedule.to_dict('records')
        }
        
        st.success(f"Created vesting schedule for {selected_category}")

# Display created vesting schedules
st.subheader("Vesting Schedules")

# Get all created schedules
vesting_schedules = st.session_state.tokenomics_data['vesting_schedules']

if not vesting_schedules:
    st.info("No vesting schedules created yet. Use the form above to create one.")
else:
    # Select schedule to view
    schedule_to_view = st.selectbox(
        "Select Schedule to View",
        options=list(vesting_schedules.keys())
    )
    
    selected_schedule = vesting_schedules[schedule_to_view]
    
    # Convert schedule back to dataframe
    schedule_df = pd.DataFrame(selected_schedule['schedule'])
    
    # Display schedule parameters
    st.markdown(f"""
    ### {schedule_to_view} Vesting Schedule
    
    - **Total Tokens**: {selected_schedule['amount']:,.0f}
    - **Cliff Period**: {selected_schedule['cliff_months']} months
    - **Vesting Period**: {selected_schedule['vesting_months']} months
    - **TGE Release**: {selected_schedule['tge_percent']}%
    """)
    
    # Format schedule for display
    display_df = schedule_df.copy()
    display_df['Released Tokens'] = display_df['Released Tokens'].map('{:,.0f}'.format)
    display_df['Cumulative Released'] = display_df['Cumulative Released'].map('{:,.0f}'.format)
    display_df['Percentage Released'] = display_df['Percentage Released'].map('{:.2f}%'.format)
    display_df['Still Locked'] = display_df['Still Locked'].map('{:,.0f}'.format)
    
    # Display schedule table
    st.dataframe(display_df, use_container_width=True)
    
    # Visualizations
    st.subheader("Vesting Visualizations")
    
    # Monthly and cumulative release charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Monthly release chart
        fig = px.bar(
            schedule_df,
            x='Month',
            y='Released Tokens',
            title=f"{schedule_to_view} Monthly Token Release",
            labels={'Released Tokens': 'Tokens Released', 'Month': 'Month'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Cumulative release chart
        fig = px.line(
            schedule_df,
            x='Month',
            y='Cumulative Released',
            title=f"{schedule_to_view} Cumulative Token Release",
            labels={'Cumulative Released': 'Tokens Released', 'Month': 'Month'},
            markers=True
        )
        fig.add_trace(
            go.Scatter(
                x=schedule_df['Month'],
                y=[selected_schedule['amount']] * len(schedule_df),
                mode='lines',
                name='Total Allocation',
                line=dict(dash='dash', color='red')
            )
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Percentage released chart
    fig = px.line(
        schedule_df,
        x='Month',
        y='Percentage Released',
        title=f"{schedule_to_view} Percentage Released Over Time",
        labels={'Percentage Released': 'Percentage', 'Month': 'Month'},
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)

# Combined vesting visualization (if multiple schedules exist)
if len(vesting_schedules) > 1:
    st.subheader("Combined Vesting Overview")
    
    # Create a combined dataset
    combined_data = []
    
    # Find the maximum month across all schedules
    max_month = 0
    for category, schedule_data in vesting_schedules.items():
        schedule = pd.DataFrame(schedule_data['schedule'])
        max_month = max(max_month, schedule['Month'].max())
    
    # Create a month range from 0 to max_month
    months = list(range(max_month + 1))
    
    # Initialize data structure
    combined_df = pd.DataFrame({
        'Month': months,
        'Date': [(datetime.now() + timedelta(days=30*m)).strftime('%Y-%m-%d') for m in months]
    })
    
    # For each category, add the cumulative release data
    for category, schedule_data in vesting_schedules.items():
        schedule = pd.DataFrame(schedule_data['schedule'])
        # Merge with the combined dataframe
        category_data = schedule[['Month', 'Cumulative Released']].copy()
        category_data.rename(columns={'Cumulative Released': category}, inplace=True)
        combined_df = pd.merge(combined_df, category_data, on='Month', how='left')
    
    # Fill NaN values with previous value or 0
    combined_df = combined_df.fillna(method='ffill').fillna(0)
    
    # Calculate total released per month
    category_columns = [col for col in combined_df.columns if col not in ['Month', 'Date']]
    combined_df['Total Released'] = combined_df[category_columns].sum(axis=1)
    
    # Calculate percentage of total supply
    combined_df['Percent of Total Supply'] = (combined_df['Total Released'] / total_supply) * 100
    
    # Create stacked area chart
    fig = px.area(
        combined_df,
        x='Month',
        y=category_columns,
        title="Combined Token Release Schedule",
        labels={'value': 'Tokens Released', 'Month': 'Month', 'variable': 'Category'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Create line chart for percent of total supply
    fig = px.line(
        combined_df,
        x='Month',
        y='Percent of Total Supply',
        title="Percentage of Total Supply Released Over Time",
        labels={'Percent of Total Supply': 'Percentage', 'Month': 'Month'},
        markers=True
    )
    fig.update_layout(yaxis_range=[0, 100])
    st.plotly_chart(fig, use_container_width=True)

# Vesting schedule template selector
st.subheader("Vesting Schedule Templates")
st.markdown("""
You can use one of the common vesting schedule templates below as a starting point for your token vesting plan.
""")

template_options = {
    "Team/Founders": {
        "cliff_months": 12,
        "vesting_months": 36,
        "tge_percent": 0
    },
    "Seed Investors": {
        "cliff_months": 6,
        "vesting_months": 24,
        "tge_percent": 5
    },
    "Private Sale": {
        "cliff_months": 3,
        "vesting_months": 18,
        "tge_percent": 10
    },
    "Public Sale": {
        "cliff_months": 0,
        "vesting_months": 12,
        "tge_percent": 20
    },
    "Advisors": {
        "cliff_months": 6,
        "vesting_months": 24,
        "tge_percent": 0
    },
    "Community/Ecosystem": {
        "cliff_months": 1,
        "vesting_months": 36,
        "tge_percent": 5
    },
    "Liquidity": {
        "cliff_months": 0,
        "vesting_months": 6,
        "tge_percent": 50
    },
}

col1, col2 = st.columns(2)

with col1:
    template_category = st.selectbox(
        "Select Allocation Category for Template",
        options=list(allocation_categories.keys())
    )

with col2:
    template_type = st.selectbox(
        "Select Vesting Template",
        options=list(template_options.keys())
    )

if st.button("Apply Template"):
    template = template_options[template_type]
    category_tokens = total_supply * allocation_categories[template_category] / 100
    
    with st.spinner("Applying template..."):
        # Calculate vesting schedule using template
        vesting_schedule = calculate_vesting_release(
            category_tokens,
            template["cliff_months"],
            template["vesting_months"],
            template["tge_percent"]
        )
        
        # Save to session state
        st.session_state.tokenomics_data['vesting_schedules'][template_category] = {
            'amount': category_tokens,
            'cliff_months': template["cliff_months"],
            'vesting_months': template["vesting_months"],
            'tge_percent': template["tge_percent"],
            'schedule': vesting_schedule.to_dict('records')
        }
        
        st.success(f"Applied {template_type} template to {template_category}")
        st.rerun()

# Delete vesting schedule
if vesting_schedules:
    st.subheader("Delete Vesting Schedule")
    delete_schedule = st.selectbox(
        "Select Schedule to Delete",
        options=list(vesting_schedules.keys()),
        key="delete_schedule"
    )
    
    if st.button("Delete Selected Schedule"):
        del st.session_state.tokenomics_data['vesting_schedules'][delete_schedule]
        st.success(f"Deleted vesting schedule for {delete_schedule}")
        st.rerun()

# Information about vesting schedules
with st.expander("Learn about token vesting best practices"):
    st.markdown("""
    ### Token Vesting Best Practices
    
    #### Why Use Vesting Schedules?
    
    1. **Align Incentives**: Ensures long-term commitment from team members and investors
    2. **Prevent Market Flooding**: Avoids selling pressure from large token holders
    3. **Market Confidence**: Signals to the market that key stakeholders have long-term commitment
    4. **Regulatory Compliance**: May help with securities regulations in some jurisdictions
    
    #### Common Vesting Periods by Stakeholder
    
    | Stakeholder | Typical Cliff | Typical Vesting | TGE Release |
    |-------------|---------------|-----------------|-------------|
    | Team/Founders | 6-12 months | 2-4 years | 0% |
    | Seed Investors | 3-6 months | 1.5-2 years | 5-10% |
    | Private Sale | 1-3 months | 12-18 months | 10-15% |
    | Public Sale | 0-1 month | 6-12 months | 15-30% |
    | Advisors | 3-6 months | 1-2 years | 0-5% |
    | Community | 0-1 month | 1-3 years | 5-10% |
    | Liquidity | 0 months | 3-12 months | 30-100% |
    
    #### Vesting Schedule Types
    
    - **Linear Vesting**: Tokens release at a constant rate after the cliff period
    - **Milestone-based Vesting**: Tokens release when specific project milestones are achieved
    - **Exponential Vesting**: Release rate increases over time
    - **Logarithmic Vesting**: Release rate decreases over time
    
    This calculator currently implements linear vesting with cliff periods and TGE releases, which is the most common approach in the industry.
    """)
