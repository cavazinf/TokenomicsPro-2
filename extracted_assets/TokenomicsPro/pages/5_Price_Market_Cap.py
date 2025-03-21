import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils import get_color_scale

# Set page configuration
st.set_page_config(
    page_title="Token Price & Market Cap - TokenomicsLab",
    page_icon="📊",
    layout="wide"
)

# Page title and description
st.title("Token Price & Market Cap Calculator")
st.markdown("""
This section helps you model and visualize different token price scenarios and analyze their impact on market capitalization.
Calculate FDV (Fully Diluted Valuation), market cap, and price targets.
""")

# Check if tokenomics data is initialized
if 'tokenomics_data' not in st.session_state:
    st.error("Please start from the main page to initialize your token data.")
    st.stop()

# Get data from session state
total_supply = st.session_state.tokenomics_data['total_supply']
initial_price = st.session_state.tokenomics_data['initial_price']
token_name = st.session_state.tokenomics_data['token_name']
token_symbol = st.session_state.tokenomics_data['token_symbol']

# Function to calculate circulating supply based on vesting schedules
def calculate_circulating_supply(month):
    if 'vesting_schedules' not in st.session_state.tokenomics_data:
        # Default to 20% if no vesting schedules
        return total_supply * 0.2
    
    vesting_schedules = st.session_state.tokenomics_data['vesting_schedules']
    
    # If no schedules created, default to 20% circulating
    if not vesting_schedules:
        return total_supply * 0.2
    
    # Calculate total released tokens up to the given month
    total_released = 0
    for category, schedule_data in vesting_schedules.items():
        schedule = pd.DataFrame(schedule_data['schedule'])
        
        # Find the row for the given month, or the last row if month exceeds schedule
        if month > schedule['Month'].max():
            # Use the max month data
            month_row = schedule[schedule['Month'] == schedule['Month'].max()]
        else:
            # Use the specified month
            month_row = schedule[schedule['Month'] == month]
        
        if not month_row.empty:
            total_released += month_row['Cumulative Released'].values[0]
    
    return total_released

# Price Calculator
st.subheader("Token Price Calculator")

tab1, tab2 = st.tabs(["Calculate Price from Market Cap", "Calculate Market Cap from Price"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        target_market_cap = st.number_input(
            "Target Market Cap (USD)",
            min_value=0.0,
            value=10000000.0,
            step=1000000.0,
            format="%.2f"
        )
        
        month_selection = st.slider(
            "Month After Launch",
            min_value=0,
            max_value=36,
            value=0,
            step=1,
            help="Select the month after launch to use circulating supply from vesting schedules"
        )
    
    with col2:
        # Calculate circulating supply based on vesting schedules
        circulating_supply = calculate_circulating_supply(month_selection)
        
        st.metric(
            "Circulating Supply",
            f"{circulating_supply:,.0f}",
            f"{(circulating_supply/total_supply)*100:.2f}% of total supply"
        )
        
        # Calculated price
        price = target_market_cap / circulating_supply if circulating_supply > 0 else 0
        
        st.metric(
            "Calculated Token Price (USD)",
            f"${price:.6f}",
            f"{(price/initial_price - 1)*100:.2f}% from initial" if initial_price > 0 else ""
        )

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        target_price = st.number_input(
            "Target Token Price (USD)",
            min_value=0.0,
            value=initial_price * 10,  # Default to 10x initial price
            step=initial_price,
            format="%.6f"
        )
        
        month_for_mcap = st.slider(
            "Month After Launch",
            min_value=0,
            max_value=36,
            value=0,
            step=1,
            help="Select the month after launch to use circulating supply from vesting schedules",
            key="month_for_mcap"
        )
    
    with col2:
        # Calculate circulating supply based on vesting schedules
        circulating_supply = calculate_circulating_supply(month_for_mcap)
        
        st.metric(
            "Circulating Supply",
            f"{circulating_supply:,.0f}",
            f"{(circulating_supply/total_supply)*100:.2f}% of total supply"
        )
        
        # Calculated market cap
        market_cap = target_price * circulating_supply
        fdv = target_price * total_supply
        
        st.metric(
            "Calculated Market Cap (USD)",
            f"${market_cap:,.2f}"
        )
        
        st.metric(
            "Fully Diluted Valuation (USD)",
            f"${fdv:,.2f}"
        )

# Price model visualization
st.subheader("Price Model Visualization")

# Allow user to set price multiples to visualize
price_multiples = [1, 2, 5, 10, 25, 50, 100]  # Default values for price multiples

# Create a multiselect for price multiples
selected_multiples = st.multiselect(
    "Price Multiples to Visualize",
    options=list(range(1, 101)),  # Options from 1x to 100x
    default=price_multiples,
    help="Select price multiples to visualize (e.g., 10 = 10x initial price)"
)

# Use selected_multiples if user made selections, otherwise use default price_multiples
price_multiples = selected_multiples if selected_multiples else price_multiples

# Create a range of months to plot
months = list(range(0, 37))  # 0 to 36 months

# Calculate circulating supply for each month
circulating_supplies = [calculate_circulating_supply(m) for m in months]

# Create a dataframe for visualization
model_df = pd.DataFrame({
    'Month': months,
    'Circulating Supply': circulating_supplies,
    'Circulating %': [cs/total_supply*100 for cs in circulating_supplies]
})

# Calculate market caps for each multiple and month
for multiple in price_multiples:
    price = initial_price * multiple
    model_df[f'{multiple}x (${price:.6f})'] = model_df['Circulating Supply'] * price

# Visualization
col1, col2 = st.columns(2)

with col1:
    # Circulating supply over time
    fig = px.line(
        model_df,
        x='Month',
        y='Circulating Supply',
        title="Circulating Supply Over Time",
        markers=True
    )
    fig.update_layout(xaxis_title="Month", yaxis_title="Circulating Supply")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Circulating percentage over time
    fig = px.line(
        model_df,
        x='Month',
        y='Circulating %',
        title="Circulating Supply Percentage Over Time",
        markers=True
    )
    fig.update_layout(xaxis_title="Month", yaxis_title="Circulating %", yaxis_range=[0, 100])
    st.plotly_chart(fig, use_container_width=True)

# Market cap projections for different price multiples
fig = go.Figure()

for multiple in price_multiples:
    price = initial_price * multiple
    fig.add_trace(go.Scatter(
        x=model_df['Month'],
        y=model_df[f'{multiple}x (${price:.6f})'],
        mode='lines+markers',
        name=f'{multiple}x (${price:.6f})'
    ))

fig.update_layout(
    title="Market Cap Projections by Price Multiple",
    xaxis_title="Month",
    yaxis_title="Market Cap (USD)",
    legend_title="Price Multiple"
)
st.plotly_chart(fig, use_container_width=True)

# Price target calculator
st.subheader("Price Target Calculator")

st.markdown("""
Compare your token to existing projects by market capitalization to set realistic price targets.
""")

col1, col2 = st.columns(2)

with col1:
    comparison_mcap = st.number_input(
        "Comparison Project Market Cap (USD)",
        min_value=1000000.0,
        value=1000000000.0,  # Default to 1B
        step=10000000.0,
        format="%.2f"
    )
    
    month_for_target = st.slider(
        "Month After Launch for Target",
        min_value=0,
        max_value=36,
        value=12,
        step=1,
        key="month_for_target"
    )

with col2:
    # Calculate price target
    target_circulating = calculate_circulating_supply(month_for_target)
    
    if target_circulating > 0:
        price_target = comparison_mcap / target_circulating
        multiple = price_target / initial_price if initial_price > 0 else 0
        
        st.metric(
            "Price Target (USD)",
            f"${price_target:.6f}",
            f"{multiple:.2f}x from initial price"
        )
        
        st.metric(
            "Fully Diluted Valuation at Target",
            f"${price_target * total_supply:,.2f}"
        )
    else:
        st.error("Cannot calculate target: circulating supply is zero")

# Common comparable projects
st.subheader("Common Cryptocurrency Market Caps")

# Create a table of common projects for comparison
common_projects = pd.DataFrame({
    'Project': ['Bitcoin', 'Ethereum', 'Binance Coin', 'XRP', 'Cardano', 
                'Solana', 'Polkadot', 'Dogecoin', 'Uniswap', 'Top 100 Coin'],
    'Approx. Market Cap (USD)': ['$1 Trillion', '$500 Billion', '$100 Billion', '$50 Billion', '$25 Billion',
                               '$10 Billion', '$5 Billion', '$1 Billion', '$500 Million', '$100 Million']
})

st.table(common_projects)

st.markdown("""
*Note: These are approximate market caps that can vary significantly. Always check current market data for accurate values.*
""")

# Price impact simulation
st.subheader("Token Sale Impact Simulation")

st.markdown("""
Estimate the impact of token sales or purchases on price using a simplified AMM (Automated Market Maker) model.
This is useful for estimating price impact for exchange listings or large sales.
""")

col1, col2 = st.columns(2)

with col1:
    liquidity_pool_size = st.number_input(
        "Liquidity Pool Size (USD)",
        min_value=10000.0,
        value=1000000.0,
        step=10000.0,
        help="Total liquidity in the trading pool"
    )
    
    token_action = st.radio(
        "Action",
        options=["Buy", "Sell"]
    )

with col2:
    token_amount = st.number_input(
        f"Amount of Tokens to {token_action}",
        min_value=0.0,
        value=total_supply * 0.01,  # Default to 1% of supply
        step=1000.0
    )
    
    # Calculate percentage of circulating supply
    month_0_circulating = calculate_circulating_supply(0)
    token_percent = (token_amount / month_0_circulating * 100) if month_0_circulating > 0 else 0
    
    st.write(f"This is approximately {token_percent:.2f}% of the initial circulating supply.")

# Calculate price impact
token_value = token_amount * initial_price
price_impact_percent = (token_value / liquidity_pool_size) * 100 if liquidity_pool_size > 0 else 0

if token_action == "Buy":
    new_price = initial_price * (1 + price_impact_percent/100)
    impact_direction = "increase"
else:  # Sell
    new_price = initial_price * (1 - price_impact_percent/100)
    impact_direction = "decrease"

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Estimated Price Impact",
        f"{price_impact_percent:.2f}%",
        delta=f"{impact_direction} in price"
    )

with col2:
    st.metric(
        "New Estimated Price",
        f"${new_price:.6f}",
        delta=f"{((new_price/initial_price)-1)*100:.2f}% from ${initial_price:.6f}"
    )

# Information about price models
with st.expander("Learn about token price and market cap models"):
    st.markdown("""
    ### Token Price and Market Cap Models
    
    #### Key Metrics
    
    - **Market Capitalization**: The total value of circulating supply (Price × Circulating Supply)
    - **Fully Diluted Valuation (FDV)**: The total value if all tokens were in circulation (Price × Total Supply)
    - **Circulating Supply**: The tokens currently available in the market (not locked or unissued)
    - **Price Impact**: How a large buy or sell affects the token price (depends on liquidity depth)
    
    #### Price Determination Factors
    
    1. **Supply and Demand**: The fundamental driver of price
    2. **Token Utility**: The value created by the token's use cases
    3. **Market Sentiment**: Overall cryptocurrency market trends
    4. **Project Milestones**: Development progress and adoption
    5. **Liquidity**: Ease of buying and selling without large price impact
    
    #### Setting Realistic Price Targets
    
    When setting price targets, consider:
    
    - **Comparable Projects**: Look at similar projects' market caps
    - **Total Addressable Market**: The size of the market your project serves
    - **Circulating Supply Timeline**: How token unlocks affect supply
    - **Network Effects**: How user growth correlates with value
    - **Sustainable Growth**: Targets should reflect realistic adoption curves
    
    #### Common Misconceptions
    
    - **Low Supply = High Price**: Price depends on market cap, not just supply
    - **Burning Always Increases Price**: Only if demand remains constant or increases
    - **FDV = Future Market Cap**: Not all tokens may circulate, and price will fluctuate
    
    Always build multiple scenarios with different assumptions to prepare for various market conditions.
    """)
