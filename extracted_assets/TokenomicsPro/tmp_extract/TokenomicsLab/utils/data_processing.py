import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Union

def calculate_token_metrics(
    df: pd.DataFrame,
    initial_price: float,
    total_supply: int
) -> pd.DataFrame:
    """
    Calculate additional token metrics from simulation data
    
    Args:
        df (pd.DataFrame): Simulation dataframe
        initial_price (float): Initial token price
        total_supply (int): Total token supply
        
    Returns:
        pd.DataFrame: Enhanced dataframe with additional metrics
    """
    # Make a copy to avoid modifying the original
    result = df.copy()
    
    # Calculate percentage changes
    result['Price_Change_Pct'] = ((result['Price'] / initial_price) - 1) * 100
    
    # Calculate market cap
    if 'Market_Cap' not in result.columns:
        result['Market_Cap'] = result['Price'] * result['Circulating_Supply']
    
    # Calculate fully diluted valuation
    result['Fully_Diluted_Valuation'] = result['Price'] * total_supply
    
    # Calculate percentage of total supply in circulation
    result['Circulating_Supply_Pct'] = (result['Circulating_Supply'] / total_supply) * 100
    
    return result

def annualize_returns(
    df: pd.DataFrame,
    price_column: str = 'Price',
    periods_per_year: int = 12
) -> float:
    """
    Calculate annualized return from price data
    
    Args:
        df (pd.DataFrame): Dataframe with price data
        price_column (str): Column name containing price data
        periods_per_year (int): Number of periods in a year (e.g., 12 for monthly data)
        
    Returns:
        float: Annualized return percentage
    """
    initial_price = df[price_column].iloc[0]
    final_price = df[price_column].iloc[-1]
    num_periods = len(df) - 1
    
    # Calculate total return
    total_return = (final_price / initial_price) - 1
    
    # Annualize the return
    years = num_periods / periods_per_year
    annualized_return = ((1 + total_return) ** (1 / years)) - 1
    
    return annualized_return * 100  # Convert to percentage

def calculate_volatility(
    df: pd.DataFrame,
    price_column: str = 'Price'
) -> float:
    """
    Calculate price volatility (standard deviation of returns)
    
    Args:
        df (pd.DataFrame): Dataframe with price data
        price_column (str): Column name containing price data
        
    Returns:
        float: Volatility as percentage
    """
    # Calculate percentage returns
    returns = df[price_column].pct_change().dropna()
    
    # Calculate volatility as standard deviation of returns
    volatility = returns.std() * 100  # Convert to percentage
    
    return volatility

def project_token_release(
    distribution: Dict[str, float],
    vesting_schedules: Dict[str, List[Tuple[int, float]]],
    total_supply: int,
    months: int
) -> pd.DataFrame:
    """
    Project token release schedule based on distribution and vesting
    
    Args:
        distribution (Dict[str, float]): Token distribution percentages by category
        vesting_schedules (Dict[str, List[Tuple[int, float]]]): Vesting schedules by category
        total_supply (int): Total token supply
        months (int): Number of months to project
        
    Returns:
        pd.DataFrame: Projected token release schedule
    """
    # Initialize dataframe with months
    data = {'Month': list(range(months + 1))}
    
    # Calculate tokens per category
    for category, percentage in distribution.items():
        category_tokens = total_supply * (percentage / 100)
        monthly_release = [0] * (months + 1)
        
        if category in vesting_schedules:
            schedule = vesting_schedules[category]
            
            for month, pct in schedule:
                if month <= months:
                    tokens_released = category_tokens * (pct / 100)
                    monthly_release[month] += tokens_released
        else:
            # If no vesting schedule, release all at month 0
            monthly_release[0] = category_tokens
        
        # Add cumulative release column
        data[f'{category}_Monthly'] = monthly_release
        data[f'{category}_Cumulative'] = np.cumsum(monthly_release)
    
    # Create dataframe
    df = pd.DataFrame(data)
    
    # Add total columns
    monthly_cols = [col for col in df.columns if col.endswith('_Monthly') and col != 'Total_Monthly']
    cumulative_cols = [col for col in df.columns if col.endswith('_Cumulative') and col != 'Total_Cumulative']
    
    df['Total_Monthly'] = df[monthly_cols].sum(axis=1)
    df['Total_Cumulative'] = df[cumulative_cols].sum(axis=1)
    
    return df

def calculate_token_velocity(
    df: pd.DataFrame,
    supply_column: str = 'Circulating_Supply',
    demand_column: str = 'Token_Demand'
) -> pd.DataFrame:
    """
    Calculate token velocity (how quickly tokens change hands)
    
    Args:
        df (pd.DataFrame): Simulation dataframe
        supply_column (str): Column name for circulating supply
        demand_column (str): Column name for token demand
        
    Returns:
        pd.DataFrame: Dataframe with velocity metric added
    """
    # Make a copy to avoid modifying the original
    result = df.copy()
    
    # Check if token demand column exists
    if demand_column in result.columns:
        # Calculate velocity as demand / supply
        result['Token_Velocity'] = result[demand_column] / result[supply_column]
        result['Token_Velocity'] = result['Token_Velocity'].fillna(0)
    else:
        # If no demand column, set velocity to NaN
        result['Token_Velocity'] = np.nan
    
    return result
