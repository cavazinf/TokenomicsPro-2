import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import calculate_allocation_amounts, get_color_scale

# Set page configuration
st.set_page_config(
    page_title="Token Supply & Distribution - TokenomicsLab",
    page_icon="📊",
    layout="wide"
)

# Page title and description
st.title("Token Supply & Distribution")
st.markdown("""
This section allows you to visualize and adjust your token's supply distribution across different categories.
Define your allocation percentages and see how tokens are distributed.
""")

# Check if tokenomics data is initialized
if 'tokenomics_data' not in st.session_state:
    st.error("Please start from the main page to initialize your token data.")
    st.stop()

# Get the current allocation data
allocation_categories = st.session_state.tokenomics_data['allocation_categories']
total_supply = st.session_state.tokenomics_data['total_supply']
token_name = st.session_state.tokenomics_data['token_name']
token_symbol = st.session_state.tokenomics_data['token_symbol']

# Create input widgets for allocation percentages
st.subheader("Token Allocation Percentages")
st.info("Adjust the percentages for each category. The total should equal 100%.")

col1, col2 = st.columns(2)

new_allocations = {}
with col1:
    for i, (category, percentage) in enumerate(list(allocation_categories.items())[:3]):
        new_allocations[category] = st.slider(
            f"{category} (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(percentage),
            step=0.1,
            key=f"allocation_{category}"
        )

with col2:
    for i, (category, percentage) in enumerate(list(allocation_categories.items())[3:]):
        new_allocations[category] = st.slider(
            f"{category} (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(percentage),
            step=0.1,
            key=f"allocation_{category}"
        )

# Calculate and display the total percentage
total_percentage = sum(new_allocations.values())
st.metric("Total Allocation", f"{total_percentage:.1f}%", delta=f"{total_percentage-100:.1f}%" if total_percentage != 100 else "")

# Warning if total is not 100%
if abs(total_percentage - 100.0) > 0.1:
    st.warning(f"The total allocation should be 100%. Current total: {total_percentage:.1f}%")
else:
    # Update the session state with the new allocations
    st.session_state.tokenomics_data['allocation_categories'] = new_allocations

# Calculate token amounts based on percentages
token_amounts = calculate_allocation_amounts(total_supply, new_allocations)

# Create a dataframe for the allocation
allocation_df = pd.DataFrame({
    'Category': list(new_allocations.keys()),
    'Percentage': list(new_allocations.values()),
    'Token Amount': [token_amounts[cat] for cat in new_allocations.keys()]
})

# Display the allocation table
st.subheader("Token Allocation Details")
st.dataframe(
    allocation_df.style.format({
        'Percentage': '{:.2f}%',
        'Token Amount': '{:,.0f}'
    }),
    use_container_width=True
)

# Visualizations
st.subheader("Allocation Visualizations")

col1, col2 = st.columns(2)

# Pie chart for percentages
with col1:
    st.write("Percentage Allocation")
    fig_pie = px.pie(
        allocation_df,
        values='Percentage',
        names='Category',
        title=f"{token_name} ({token_symbol}) Token Allocation" if token_name and token_symbol else "Token Allocation"
    )
    fig_pie.update_traces(
        textposition='inside',
        textinfo='percent+label',
        marker=dict(colors=get_color_scale())
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# Bar chart for token amounts
with col2:
    st.write("Token Amount Allocation")
    fig_bar = px.bar(
        allocation_df,
        x='Category',
        y='Token Amount',
        color='Category',
        title=f"Token Amount per Category",
        color_discrete_sequence=get_color_scale()
    )
    fig_bar.update_layout(xaxis_title="Category", yaxis_title="Token Amount")
    st.plotly_chart(fig_bar, use_container_width=True)

# Add custom category functionality
st.subheader("Customize Allocation Categories")

col1, col2 = st.columns(2)

with col1:
    new_category = st.text_input("New Category Name")
    new_percentage = st.slider("New Category Percentage (%)", 0.0, 100.0, 5.0, 0.1)

with col2:
    st.write("Remove Categories")
    categories_to_remove = st.multiselect(
        "Select categories to remove",
        options=list(new_allocations.keys())
    )

# Add new category button
if st.button("Add New Category") and new_category:
    if new_category in new_allocations:
        st.error(f"Category '{new_category}' already exists.")
    else:
        # Add the new category
        updated_allocations = st.session_state.tokenomics_data['allocation_categories'].copy()
        updated_allocations[new_category] = new_percentage
        
        # Scale other categories proportionally to make total 100%
        total = sum(updated_allocations.values())
        if total > 0:
            scaling_factor = 100 / total
            for cat in updated_allocations:
                updated_allocations[cat] *= scaling_factor
        
        st.session_state.tokenomics_data['allocation_categories'] = updated_allocations
        st.success(f"Added category '{new_category}' with {new_percentage}% allocation.")
        st.rerun()

# Remove categories button
if st.button("Remove Selected Categories") and categories_to_remove:
    updated_allocations = st.session_state.tokenomics_data['allocation_categories'].copy()
    for cat in categories_to_remove:
        if cat in updated_allocations:
            del updated_allocations[cat]
    
    # Normalize remaining categories to 100%
    total = sum(updated_allocations.values())
    if total > 0:
        scaling_factor = 100 / total
        for cat in updated_allocations:
            updated_allocations[cat] *= scaling_factor
    
    st.session_state.tokenomics_data['allocation_categories'] = updated_allocations
    st.success(f"Removed {len(categories_to_remove)} categories and rescaled remaining allocations to 100%.")
    st.rerun()

# Information box about tokenomics best practices
st.markdown("---")
st.subheader("Token Allocation Best Practices")

with st.expander("Learn about token allocation best practices"):
    st.markdown("""
    ### Common Token Allocation Practices
    
    - **Team & Advisors (15-20%)**: Incentivizes founders, developers, and advisors
    - **Investors (15-30%)**: Allocated to seed, private, and public sale investors
    - **Community & Ecosystem (20-40%)**: Rewards for community participation, grants, airdrops
    - **Treasury (10-20%)**: Long-term project funding and operations
    - **Liquidity (5-10%)**: Market making and exchange liquidity
    - **Foundation (5-15%)**: Non-profit development and governance
    
    ### Allocation Considerations
    
    1. **Balance stakeholder interests** - Ensure fair distribution across different parties
    2. **Prevent centralization** - Avoid high concentration of tokens in few hands
    3. **Support long-term growth** - Allocate sufficient tokens for ongoing development
    4. **Align incentives** - Use vesting schedules to align long-term interests
    5. **Enable liquidity** - Allocate adequate tokens for market liquidity
    
    Each project is unique, so adjust these guidelines to fit your specific tokenomics model.
    """)
