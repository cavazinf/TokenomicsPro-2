import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Union

class TokenomicsModel:
    """Base class for tokenomics models"""
    
    def __init__(self, name: str, total_supply: int):
        """
        Initialize a tokenomics model
        
        Args:
            name (str): Name of the tokenomics model
            total_supply (int): Total supply of tokens
        """
        self.name = name
        self.total_supply = total_supply
        self.distribution = {}
        self.vesting_schedules = {}
        self.token_price_history = []
        self.token_supply_history = []
        
    def set_distribution(self, distribution: Dict[str, float]) -> None:
        """
        Set token distribution percentages
        
        Args:
            distribution (Dict[str, float]): Dictionary mapping categories to percentage allocations
        """
        # Validate total is 100%
        total = sum(distribution.values())
        if not np.isclose(total, 100.0):
            raise ValueError(f"Distribution percentages must sum to 100%, got {total}%")
            
        self.distribution = distribution
        
    def set_vesting_schedule(self, category: str, 
                             schedule: List[Tuple[int, float]]) -> None:
        """
        Set vesting schedule for a category
        
        Args:
            category (str): Distribution category
            schedule (List[Tuple[int, float]]): List of (month, percentage) tuples
        """
        if category not in self.distribution:
            raise ValueError(f"Category {category} not in distribution")
            
        # Validate schedule percentages sum to 100%
        total = sum(pct for _, pct in schedule)
        if not np.isclose(total, 100.0):
            raise ValueError(f"Vesting schedule must sum to 100%, got {total}%")
            
        self.vesting_schedules[category] = schedule
        
    def calculate_released_tokens(self, month: int) -> Dict[str, int]:
        """
        Calculate tokens released per category at a given month
        
        Args:
            month (int): Month to calculate for (0-indexed)
            
        Returns:
            Dict[str, int]: Tokens released per category
        """
        result = {}
        
        for category, percentage in self.distribution.items():
            category_tokens = self.total_supply * (percentage / 100)
            
            # If no vesting schedule, assume all tokens are released immediately
            if category not in self.vesting_schedules:
                result[category] = category_tokens
                continue
                
            # Calculate based on vesting schedule
            schedule = self.vesting_schedules[category]
            released_pct = sum(pct for m, pct in schedule if m <= month)
            result[category] = category_tokens * (released_pct / 100)
            
        return result
        
    def simulate_token_price(self, months: int, 
                             initial_price: float, 
                             market_factors: List[Tuple[str, float]] = None,
                             volatility: float = 0.1) -> pd.DataFrame:
        """
        Simulate token price over time based on vesting and market factors
        
        Args:
            months (int): Number of months to simulate
            initial_price (float): Initial token price
            market_factors (List[Tuple[str, float]], optional): List of (factor_name, impact) tuples
            volatility (float, optional): Random volatility factor
            
        Returns:
            pd.DataFrame: Token price simulation results
        """
        if market_factors is None:
            market_factors = []
            
        price = initial_price
        prices = [price]
        circulating_supply = [0]
        market_cap = [0]
        
        for month in range(months + 1):
            # Calculate circulating supply based on vesting
            released = self.calculate_released_tokens(month)
            total_released = sum(released.values())
            
            # Apply market factors
            factor_impact = 1.0
            for _, impact in market_factors:
                factor_impact *= (1 + impact)
                
            # Apply supply impact (simplified model: more supply = lower price)
            supply_impact = 1.0
            if month > 0:
                supply_ratio = total_released / circulating_supply[-1] if circulating_supply[-1] > 0 else 1.0
                if supply_ratio > 1.0:
                    # Supply increased
                    supply_impact = 0.98  # Price decreases slightly with more supply
                
            # Apply random volatility
            random_impact = 1.0 + np.random.uniform(-volatility, volatility)
            
            # Calculate new price
            if month > 0:  # Keep initial price for month 0
                price = prices[-1] * factor_impact * supply_impact * random_impact
                
            prices.append(price)
            circulating_supply.append(total_released)
            market_cap.append(price * total_released)
            
        # Create dataframe
        data = {
            'Month': list(range(len(prices))),
            'Price': prices,
            'Circulating_Supply': circulating_supply,
            'Market_Cap': market_cap
        }
        
        # Add released tokens by category
        for category in self.distribution.keys():
            # Garantir que todos os arrays tenham o mesmo comprimento
            released_tokens = []
            for m in range(len(prices)):
                released_tokens.append(self.calculate_released_tokens(m).get(category, 0))
            
            data[f'{category}_Released'] = released_tokens
            
        return pd.DataFrame(data)
        
    def to_dict(self) -> Dict:
        """
        Convert model to dictionary for storage/serialization
        
        Returns:
            Dict: Dictionary representation of the model
        """
        return {
            'name': self.name,
            'total_supply': self.total_supply,
            'distribution': self.distribution,
            'vesting_schedules': self.vesting_schedules
        }
        
    @classmethod
    def from_dict(cls, data: Dict) -> 'TokenomicsModel':
        """
        Create model from dictionary
        
        Args:
            data (Dict): Dictionary representation of the model
            
        Returns:
            TokenomicsModel: Instantiated model
        """
        model = cls(data['name'], data['total_supply'])
        model.distribution = data['distribution']
        model.vesting_schedules = data['vesting_schedules']
        return model


class UtilityTokenModel(TokenomicsModel):
    """Model for utility tokens with demand based on network usage"""
    
    def __init__(self, name: str, total_supply: int, 
                 initial_users: int, user_growth_rate: float):
        """
        Initialize a utility token model
        
        Args:
            name (str): Name of the tokenomics model
            total_supply (int): Total supply of tokens
            initial_users (int): Initial number of users
            user_growth_rate (float): Monthly user growth rate (e.g., 0.05 for 5%)
        """
        super().__init__(name, total_supply)
        self.initial_users = initial_users
        self.user_growth_rate = user_growth_rate
        
    def simulate_token_price(self, months: int, 
                             initial_price: float,
                             tokens_per_user: float = 10.0,
                             volatility: float = 0.1) -> pd.DataFrame:
        """
        Simulate token price with network effects and user growth
        
        Args:
            months (int): Number of months to simulate
            initial_price (float): Initial token price
            tokens_per_user (float): Average tokens used per user
            volatility (float): Random volatility factor
            
        Returns:
            pd.DataFrame: Token price simulation results
        """
        price = initial_price
        prices = [price]
        users = [self.initial_users]
        demand = [self.initial_users * tokens_per_user]
        circulating_supply = [0]
        market_cap = [0]
        
        for month in range(1, months + 1):
            # Update user count with growth rate
            new_users = users[-1] * (1 + self.user_growth_rate)
            users.append(new_users)
            
            # Calculate token demand
            new_demand = new_users * tokens_per_user
            demand.append(new_demand)
            
            # Calculate circulating supply
            released = self.calculate_released_tokens(month)
            total_released = sum(released.values())
            circulating_supply.append(total_released)
            
            # Apply supply/demand dynamics to price
            supply_demand_ratio = min(new_demand / max(1, total_released), 2.0)  # Cap the effect
            
            # Apply random volatility
            random_impact = 1.0 + np.random.uniform(-volatility, volatility)
            
            # Calculate new price 
            price = prices[-1] * supply_demand_ratio * random_impact
            prices.append(price)
            
            market_cap.append(price * total_released)
            
        # Create dataframe
        data = {
            'Month': list(range(len(prices))),
            'Price': prices,
            'Users': users,
            'Token_Demand': demand,
            'Circulating_Supply': circulating_supply,
            'Market_Cap': market_cap
        }
        
        # Add released tokens by category
        for category in self.distribution.keys():
            # Garantir que todos os arrays tenham o mesmo comprimento
            released_tokens = []
            for m in range(len(prices)):
                released_tokens.append(self.calculate_released_tokens(m).get(category, 0))
            
            data[f'{category}_Released'] = released_tokens
            
        return pd.DataFrame(data)
        
    def to_dict(self) -> Dict:
        """Convert model to dictionary with additional utility token parameters"""
        data = super().to_dict()
        data.update({
            'model_type': 'utility',
            'initial_users': self.initial_users,
            'user_growth_rate': self.user_growth_rate
        })
        return data
        
    @classmethod
    def from_dict(cls, data: Dict) -> 'UtilityTokenModel':
        """Create utility token model from dictionary"""
        model = cls(
            data['name'], 
            data['total_supply'],
            data['initial_users'],
            data['user_growth_rate']
        )
        model.distribution = data['distribution']
        model.vesting_schedules = data['vesting_schedules']
        return model


class GovernanceTokenModel(TokenomicsModel):
    """Model for governance tokens with staking mechanics"""
    
    def __init__(self, name: str, total_supply: int, 
                 initial_staking_rate: float, staking_apy: float):
        """
        Initialize a governance token model
        
        Args:
            name (str): Name of the tokenomics model
            total_supply (int): Total supply of tokens
            initial_staking_rate (float): Initial percentage of tokens staked (0-1)
            staking_apy (float): Annual percentage yield for staking
        """
        super().__init__(name, total_supply)
        self.initial_staking_rate = initial_staking_rate
        self.staking_apy = staking_apy
        
    def simulate_token_price(self, months: int, 
                             initial_price: float,
                             staking_growth: float = 0.01,
                             volatility: float = 0.1) -> pd.DataFrame:
        """
        Simulate token price with staking mechanics
        
        Args:
            months (int): Number of months to simulate
            initial_price (float): Initial token price
            staking_growth (float): Monthly growth in staking rate
            volatility (float): Random volatility factor
            
        Returns:
            pd.DataFrame: Token price simulation results
        """
        price = initial_price
        prices = [price]
        staking_rate = [self.initial_staking_rate]
        circulating_supply = [0]
        staked_tokens = [0]
        liquid_tokens = [0]
        market_cap = [0]
        
        for month in range(1, months + 1):
            # Calculate circulating supply
            released = self.calculate_released_tokens(month)
            total_released = sum(released.values())
            circulating_supply.append(total_released)
            
            # Update staking rate with growth (capped at 80%)
            new_staking_rate = min(staking_rate[-1] + staking_growth, 0.8)
            staking_rate.append(new_staking_rate)
            
            # Calculate staked and liquid tokens
            staked = total_released * new_staking_rate
            staked_tokens.append(staked)
            
            liquid = total_released - staked
            liquid_tokens.append(liquid)
            
            # Calculate price impact of staking (more staking = higher price due to decreased supply)
            staking_impact = 1.0 + (new_staking_rate / 10)  # 10% staking = 1% price increase
            
            # Apply random volatility
            random_impact = 1.0 + np.random.uniform(-volatility, volatility)
            
            # Calculate new price
            price = prices[-1] * staking_impact * random_impact
            prices.append(price)
            
            market_cap.append(price * total_released)
            
        # Create dataframe
        data = {
            'Month': list(range(len(prices))),
            'Price': prices,
            'Staking_Rate': staking_rate,
            'Circulating_Supply': circulating_supply,
            'Staked_Tokens': staked_tokens,
            'Liquid_Tokens': liquid_tokens,
            'Market_Cap': market_cap
        }
        
        # Add released tokens by category
        for category in self.distribution.keys():
            # Garantir que todos os arrays tenham o mesmo comprimento
            released_tokens = []
            for m in range(len(prices)):
                released_tokens.append(self.calculate_released_tokens(m).get(category, 0))
            
            data[f'{category}_Released'] = released_tokens
            
        return pd.DataFrame(data)
        
    def to_dict(self) -> Dict:
        """Convert model to dictionary with additional governance token parameters"""
        data = super().to_dict()
        data.update({
            'model_type': 'governance',
            'initial_staking_rate': self.initial_staking_rate,
            'staking_apy': self.staking_apy
        })
        return data
        
    @classmethod
    def from_dict(cls, data: Dict) -> 'GovernanceTokenModel':
        """Create governance token model from dictionary"""
        model = cls(
            data['name'], 
            data['total_supply'],
            data['initial_staking_rate'],
            data['staking_apy']
        )
        model.distribution = data['distribution']
        model.vesting_schedules = data['vesting_schedules']
        return model


def create_model_from_dict(data: Dict) -> TokenomicsModel:
    """
    Factory function to create the appropriate model type from a dictionary
    
    Args:
        data (Dict): Dictionary representation of the model
        
    Returns:
        TokenomicsModel: The appropriate model instance
    """
    model_type = data.get('model_type', 'base')
    
    if model_type == 'utility':
        return UtilityTokenModel.from_dict(data)
    elif model_type == 'governance':
        return GovernanceTokenModel.from_dict(data)
    else:
        return TokenomicsModel.from_dict(data)
