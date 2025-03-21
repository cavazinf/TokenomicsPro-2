import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils import simulate_token_economics, get_color_scale

# Set page configuration
st.set_page_config(
    page_title="Economic Simulation - TokenomicsLab",
    page_icon="📊",
    layout="wide"
)

# Page title and description
st.title("Token Economic Simulation")
st.markdown("""
This section allows you to simulate the economic behavior of your token over time. 
Adjust parameters like inflation rate, burn rate, and staking rewards to visualize different scenarios.
""")

# Check if tokenomics data is initialized
if 'tokenomics_data' not in st.session_state:
    st.error("Please start from the main page to initialize your token data.")
    st.stop()

# Get current economic parameters
economic_params = st.session_state.tokenomics_data['economic_params']
token_name = st.session_state.tokenomics_data['token_name']
token_symbol = st.session_state.tokenomics_data['token_symbol']
total_supply = st.session_state.tokenomics_data['total_supply']
initial_price = st.session_state.tokenomics_data['initial_price']

# Parameter input section
st.subheader("Economic Parameters")

col1, col2, col3 = st.columns(3)

with col1:
    inflation_rate = st.slider(
        "Annual Inflation Rate (%)",
        min_value=0.0,
        max_value=50.0,
        value=float(economic_params['inflation_rate']),
        step=0.1,
        help="The annual rate at which new tokens are created"
    )

with col2:
    staking_reward = st.slider(
        "Staking Reward (%)",
        min_value=0.0,
        max_value=30.0,
        value=float(economic_params['staking_reward']),
        step=0.1,
        help="Annual reward rate for token stakers"
    )

with col3:
    burn_rate = st.slider(
        "Annual Burn Rate (%)",
        min_value=0.0,
        max_value=25.0,
        value=float(economic_params['burn_rate']),
        step=0.1,
        help="The annual rate at which tokens are burned or removed from circulation"
    )

# Additional simulation parameters
st.subheader("Simulation Parameters")

col1, col2 = st.columns(2)

with col1:
    simulation_years = st.slider(
        "Simulation Duration (Years)",
        min_value=1,
        max_value=20,
        value=5,
        step=1,
        help="Number of years to simulate"
    )

with col2:
    initial_circulating = st.slider(
        "Initial Circulating Supply (%)",
        min_value=1.0,
        max_value=100.0,
        value=20.0,
        step=1.0,
        help="Percentage of total supply in circulation at the start"
    )

# Update economic parameters in session state
updated_params = {
    'inflation_rate': inflation_rate,
    'staking_reward': staking_reward,
    'burn_rate': burn_rate
}

if updated_params != economic_params:
    st.session_state.tokenomics_data['economic_params'] = updated_params

# Create temp data for simulation
simulation_data = st.session_state.tokenomics_data.copy()
simulation_data['initial_circulating_pct'] = initial_circulating

# Run simulation
if st.button("Run Simulation"):
    with st.spinner("Running economic simulation..."):
        # Run the simulation
        simulation_results = simulate_token_economics(simulation_data, years=simulation_years)
        
        st.session_state.simulation_results = simulation_results
        
        st.success("Simulation completed! Results are shown below.")

# Display simulation results if available
if 'simulation_results' in st.session_state:
    results_df = st.session_state.simulation_results
    
    # Format results for display
    display_df = results_df.copy()
    display_df['Circulating Supply'] = display_df['Circulating Supply'].map('{:,.0f}'.format)
    display_df['Price (USD)'] = display_df['Price (USD)'].map('${:,.6f}'.format)
    display_df['Market Cap (USD)'] = display_df['Market Cap (USD)'].map('${:,.0f}'.format)
    
    # Display results table
    st.subheader("Simulation Results")
    st.dataframe(display_df, use_container_width=True)
    
    # Visualizations
    st.subheader("Simulation Visualizations")
    
    # Create tabs for different visualizations
    tab1, tab2, tab3 = st.tabs(["Supply", "Price", "Market Cap"])
    
    with tab1:
        # Supply over time
        fig = px.line(
            results_df,
            x='Year',
            y='Circulating Supply',
            title=f"{token_name} Circulating Supply Over Time",
            markers=True
        )
        fig.update_layout(xaxis_title="Year", yaxis_title="Circulating Supply")
        st.plotly_chart(fig, use_container_width=True)
        
        # Annual supply change
        if len(results_df) > 1:
            supply_change = pd.DataFrame({
                'Year': results_df['Year'][1:].values,
                'Annual Change (%)': [
                    ((results_df['Circulating Supply'][i] / results_df['Circulating Supply'][i-1]) - 1) * 100
                    for i in range(1, len(results_df))
                ]
            })
            
            fig = px.bar(
                supply_change,
                x='Year',
                y='Annual Change (%)',
                title="Annual Supply Change (%)",
                color='Annual Change (%)',
                color_continuous_scale=['red', 'gray', 'green']
            )
            st.plotly_chart(fig, use_container_width=True)
        
    with tab2:
        # Price over time
        fig = px.line(
            results_df,
            x='Year',
            y='Price (USD)',
            title=f"{token_name} Price Over Time",
            markers=True
        )
        fig.update_layout(xaxis_title="Year", yaxis_title="Price (USD)")
        st.plotly_chart(fig, use_container_width=True)
        
        # Annual price change
        if len(results_df) > 1:
            price_change = pd.DataFrame({
                'Year': results_df['Year'][1:].values,
                'Annual Change (%)': [
                    ((results_df['Price (USD)'][i] / results_df['Price (USD)'][i-1]) - 1) * 100
                    for i in range(1, len(results_df))
                ]
            })
            
            fig = px.bar(
                price_change,
                x='Year',
                y='Annual Change (%)',
                title="Annual Price Change (%)",
                color='Annual Change (%)',
                color_continuous_scale=['red', 'gray', 'green']
            )
            st.plotly_chart(fig, use_container_width=True)
        
    with tab3:
        # Market cap over time
        fig = px.line(
            results_df,
            x='Year',
            y='Market Cap (USD)',
            title=f"{token_name} Market Cap Over Time",
            markers=True
        )
        fig.update_layout(xaxis_title="Year", yaxis_title="Market Cap (USD)")
        st.plotly_chart(fig, use_container_width=True)
        
        # Annual market cap change
        if len(results_df) > 1:
            mcap_change = pd.DataFrame({
                'Year': results_df['Year'][1:].values,
                'Annual Change (%)': [
                    ((results_df['Market Cap (USD)'][i] / results_df['Market Cap (USD)'][i-1]) - 1) * 100
                    for i in range(1, len(results_df))
                ]
            })
            
            fig = px.bar(
                mcap_change,
                x='Year',
                y='Annual Change (%)',
                title="Annual Market Cap Change (%)",
                color='Annual Change (%)',
                color_continuous_scale=['red', 'gray', 'green']
            )
            st.plotly_chart(fig, use_container_width=True)

    # Scenario comparison
    st.subheader("Scenario Comparison")
    st.markdown("""
    Use the simulation tool multiple times with different parameters to compare various economic scenarios.
    Adjust inflation, burn rates, and other parameters to find the optimal tokenomics model for your project.
    """)
    
    if st.button("Save Current Scenario"):
        # Get the latest simulation results
        current_results = st.session_state.simulation_results.copy()
        
        # Initialize the scenarios dict if it doesn't exist
        if 'simulation_scenarios' not in st.session_state:
            st.session_state.simulation_scenarios = {}
        
        # Create a name for the scenario based on parameters
        scenario_name = f"Scenario {len(st.session_state.simulation_scenarios) + 1}: I={inflation_rate}%, B={burn_rate}%"
        
        # Save the scenario
        st.session_state.simulation_scenarios[scenario_name] = {
            'results': current_results,
            'params': {
                'inflation_rate': inflation_rate,
                'burn_rate': burn_rate,
                'staking_reward': staking_reward,
                'years': simulation_years,
                'initial_circulating': initial_circulating
            }
        }
        
        st.success(f"Saved scenario: {scenario_name}")

# Display saved scenarios if available
if 'simulation_scenarios' in st.session_state and st.session_state.simulation_scenarios:
    st.subheader("Saved Scenarios")
    
    scenarios = list(st.session_state.simulation_scenarios.keys())
    selected_scenarios = st.multiselect(
        "Select scenarios to compare",
        options=scenarios,
        default=scenarios[:min(3, len(scenarios))]
    )
    
    if selected_scenarios:
        # Create comparison visualizations
        tab1, tab2, tab3 = st.tabs(["Supply Comparison", "Price Comparison", "Market Cap Comparison"])
        
        with tab1:
            # Supply comparison
            fig = go.Figure()
            
            for scenario in selected_scenarios:
                scenario_data = st.session_state.simulation_scenarios[scenario]['results']
                fig.add_trace(go.Scatter(
                    x=scenario_data['Year'],
                    y=scenario_data['Circulating Supply'],
                    mode='lines+markers',
                    name=scenario
                ))
            
            fig.update_layout(
                title="Circulating Supply Comparison",
                xaxis_title="Year",
                yaxis_title="Circulating Supply"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # Price comparison
            fig = go.Figure()
            
            for scenario in selected_scenarios:
                scenario_data = st.session_state.simulation_scenarios[scenario]['results']
                fig.add_trace(go.Scatter(
                    x=scenario_data['Year'],
                    y=scenario_data['Price (USD)'],
                    mode='lines+markers',
                    name=scenario
                ))
            
            fig.update_layout(
                title="Price Comparison",
                xaxis_title="Year",
                yaxis_title="Price (USD)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Market cap comparison
            fig = go.Figure()
            
            for scenario in selected_scenarios:
                scenario_data = st.session_state.simulation_scenarios[scenario]['results']
                fig.add_trace(go.Scatter(
                    x=scenario_data['Year'],
                    y=scenario_data['Market Cap (USD)'],
                    mode='lines+markers',
                    name=scenario
                ))
            
            fig.update_layout(
                title="Market Cap Comparison",
                xaxis_title="Year",
                yaxis_title="Market Cap (USD)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Scenario parameters comparison
        st.subheader("Scenario Parameters")
        
        params_df = []
        for scenario in selected_scenarios:
            scenario_params = st.session_state.simulation_scenarios[scenario]['params']
            params_df.append({
                'Scenario': scenario,
                'Inflation Rate (%)': scenario_params['inflation_rate'],
                'Burn Rate (%)': scenario_params['burn_rate'],
                'Staking Reward (%)': scenario_params['staking_reward'],
                'Initial Circulating (%)': scenario_params['initial_circulating'],
                'Simulation Years': scenario_params['years']
            })
        
        params_df = pd.DataFrame(params_df)
        st.dataframe(params_df, use_container_width=True)

# Information about economic models
with st.expander("Learn about token economic models"):
    st.markdown("""
    ### Token Economic Models
    
    #### Inflation and Monetary Policy
    
    - **Inflationary Models**: New tokens are created over time (inflation rate > 0%)
      - Pros: Funds ongoing development, incentivizes participation
      - Cons: Can dilute value if not balanced with utility and demand
    
    - **Deflationary Models**: Tokens are removed from circulation over time (burn rate > 0%)
      - Pros: Creates scarcity, may increase value if demand remains constant
      - Cons: May limit ecosystem growth if too aggressive
    
    - **Stable Supply Models**: Supply remains roughly constant (inflation ≈ burn rate)
      - Pros: Predictable tokenomics, balanced approach
      - Cons: Less flexible for responding to market conditions
    
    #### Economic Factors to Consider
    
    1. **Velocity of Money**: How quickly tokens change hands affects price stability
    2. **Utility Value**: The usefulness of the token within its ecosystem
    3. **Demand Drivers**: What creates and sustains token demand
    4. **Staking Economics**: How staking affects circulating supply and price
    5. **Network Effects**: How user growth affects token value
    
    #### Testing Parameters
    
    For optimal tokenomics, consider testing multiple scenarios with different:
    - Inflation rates (0-15%)
    - Burn rates (0-10%)
    - Staking rewards (0-20%)
    - Initial circulating supply (10-50%)
    
    The ideal model will depend on your specific project goals and use cases.
    """)
