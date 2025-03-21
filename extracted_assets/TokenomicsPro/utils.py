import pandas as pd
import numpy as np
import streamlit as st
from io import StringIO
import base64
from datetime import datetime, timedelta

def convert_df_to_csv(df):
    """
    Convert a pandas dataframe to CSV format for download
    """
    return df.to_csv(index=False).encode('utf-8')

def generate_sample_tokenomics_data(tokenomics_data):
    """
    Generate a dataframe with the tokenomics data for export
    """
    # Basic token info
    basic_info = pd.DataFrame({
        'Parameter': ['Token Name', 'Token Symbol', 'Total Supply', 'Initial Price', 'Initial Market Cap'],
        'Value': [
            tokenomics_data['token_name'],
            tokenomics_data['token_symbol'],
            tokenomics_data['total_supply'],
            tokenomics_data['initial_price'],
            tokenomics_data['total_supply'] * tokenomics_data['initial_price']
        ]
    })
    
    # Token allocation
    allocation_data = []
    for category, percentage in tokenomics_data['allocation_categories'].items():
        allocation_tokens = tokenomics_data['total_supply'] * percentage / 100
        allocation_data.append({
            'Category': category,
            'Percentage': percentage,
            'Token Amount': allocation_tokens,
            'USD Value': allocation_tokens * tokenomics_data['initial_price']
        })
    
    allocation_df = pd.DataFrame(allocation_data)
    
    # Combine all data
    combined_data = pd.concat([basic_info, allocation_df], axis=0, ignore_index=True)
    
    return combined_data

def calculate_vesting_release(total_tokens, cliff_months, vesting_months, tge_percent=0):
    """
    Calculate token release schedule based on vesting parameters
    
    Parameters:
    - total_tokens: Total tokens to be vested
    - cliff_months: Number of months before any tokens are released
    - vesting_months: Number of months for the full vesting period
    - tge_percent: Percentage of tokens released at TGE (Token Generation Event)
    
    Returns:
    - DataFrame with release schedule
    """
    # Initial release at TGE
    tge_release = total_tokens * tge_percent / 100
    remaining_tokens = total_tokens - tge_release
    
    # Calculate monthly release after cliff
    if vesting_months <= 0:
        monthly_release = remaining_tokens
    else:
        monthly_release = remaining_tokens / vesting_months
    
    # Create schedule dataframe
    schedule = []
    
    # Add TGE release if any
    if tge_percent > 0:
        schedule.append({
            'Month': 0,
            'Date': datetime.now().strftime('%Y-%m-%d'),
            'Released Tokens': tge_release,
            'Cumulative Released': tge_release,
            'Percentage Released': tge_percent,
            'Still Locked': total_tokens - tge_release
        })
    
    cum_released = tge_release
    
    # Add all months including cliff period
    for month in range(1, cliff_months + vesting_months + 1):
        date = (datetime.now() + timedelta(days=30*month)).strftime('%Y-%m-%d')
        
        # Determine release for this month
        if month <= cliff_months:
            # During cliff period, no tokens are released
            month_release = 0
        else:
            # After cliff, release monthly amount
            month_release = monthly_release
        
        cum_released += month_release
        percentage = (cum_released / total_tokens) * 100
        
        schedule.append({
            'Month': month,
            'Date': date,
            'Released Tokens': month_release,
            'Cumulative Released': cum_released,
            'Percentage Released': percentage,
            'Still Locked': total_tokens - cum_released
        })
    
    return pd.DataFrame(schedule)

def simulate_token_economics(tokenomics_data, years=5):
    """
    Simulate token economics over time based on parameters
    
    Parameters:
    - tokenomics_data: Dictionary with token economics parameters
    - years: Number of years to simulate
    
    Returns:
    - DataFrame with simulation results
    """
    total_supply = tokenomics_data['total_supply']
    inflation_rate = tokenomics_data['economic_params']['inflation_rate'] / 100
    burn_rate = tokenomics_data['economic_params']['burn_rate'] / 100
    
    simulation = []
    
    for year in range(years + 1):
        if year == 0:
            # Initial state
            circulating_supply = total_supply * 0.2  # Assumption: 20% circulating at launch
            price = tokenomics_data['initial_price']
        else:
            # New tokens minted
            new_tokens = circulating_supply * inflation_rate
            
            # Tokens burned
            burned_tokens = circulating_supply * burn_rate
            
            # Update circulating supply
            circulating_supply = circulating_supply + new_tokens - burned_tokens
            
            # Simple price model (inverse to supply change)
            supply_change_factor = (1 + inflation_rate - burn_rate)
            price = price / supply_change_factor if supply_change_factor > 0 else price
        
        market_cap = circulating_supply * price
        
        simulation.append({
            'Year': year,
            'Circulating Supply': circulating_supply,
            'Price (USD)': price,
            'Market Cap (USD)': market_cap,
            'Inflation': inflation_rate * 100,
            'Burn Rate': burn_rate * 100
        })
    
    return pd.DataFrame(simulation)

def calculate_allocation_amounts(total_supply, allocations):
    """
    Calculate the token amounts for each allocation category
    
    Parameters:
    - total_supply: Total token supply
    - allocations: Dictionary with category names and percentages
    
    Returns:
    - Dictionary with category names and token amounts
    """
    allocation_amounts = {}
    for category, percentage in allocations.items():
        allocation_amounts[category] = total_supply * percentage / 100
    
    return allocation_amounts

def get_color_scale():
    """Return a consistent color scale for plots"""
    return [
        '#1f77b4',  # Blue
        '#ff7f0e',  # Orange
        '#2ca02c',  # Green
        '#d62728',  # Red
        '#9467bd',  # Purple
        '#8c564b',  # Brown
        '#e377c2',  # Pink
        '#7f7f7f',  # Gray
        '#bcbd22',  # Yellow-green
        '#17becf'   # Cyan
    ]
