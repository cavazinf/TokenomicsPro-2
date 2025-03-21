import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from typing import Dict, List, Tuple, Optional, Union

def create_distribution_pie_chart(
    distribution: Dict[str, float], 
    title: str = "Distribuição de Tokens"
) -> go.Figure:
    """
    Create a pie chart for token distribution
    
    Args:
        distribution (Dict[str, float]): Token distribution percentages by category
        title (str): Chart title
        
    Returns:
        go.Figure: Plotly figure object
    """
    fig = px.pie(
        values=list(distribution.values()),
        names=list(distribution.keys()),
        title=title,
        color_discrete_sequence=px.colors.sequential.Blues_r,
        hole=0.4,
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    return fig

def create_price_chart(
    df: pd.DataFrame,
    title: str = "Evolução do Preço do Token"
) -> go.Figure:
    """
    Create a line chart for token price evolution
    
    Args:
        df (pd.DataFrame): Simulation dataframe
        title (str): Chart title
        
    Returns:
        go.Figure: Plotly figure object
    """
    fig = px.line(
        df, 
        x="Month", 
        y="Price",
        title=title,
        labels={"Month": "Mês", "Price": "Preço ($)"}
    )
    
    fig.update_layout(
        hovermode="x unified"
    )
    
    return fig

def create_market_cap_chart(
    df: pd.DataFrame,
    title: str = "Evolução do Market Cap"
) -> go.Figure:
    """
    Create an area chart for market cap evolution
    
    Args:
        df (pd.DataFrame): Simulation dataframe
        title (str): Chart title
        
    Returns:
        go.Figure: Plotly figure object
    """
    fig = px.area(
        df, 
        x="Month", 
        y="Market_Cap",
        title=title,
        labels={"Month": "Mês", "Market_Cap": "Market Cap ($)"},
        color_discrete_sequence=['#83c9ff']
    )
    
    fig.update_layout(
        hovermode="x unified"
    )
    
    return fig

def create_vesting_chart(
    vesting_schedules: Dict[str, List[Tuple[int, float]]],
    distribution: Dict[str, float],
    title: str = "Cronograma de Vesting"
) -> Optional[go.Figure]:
    """
    Create a line chart for vesting schedules
    
    Args:
        vesting_schedules (Dict[str, List[Tuple[int, float]]]): Vesting schedules by category
        distribution (Dict[str, float]): Token distribution percentages by category
        title (str): Chart title
        
    Returns:
        Optional[go.Figure]: Plotly figure object or None if no vesting data
    """
    if not vesting_schedules:
        return None
        
    # Prepare vesting data
    vesting_data = []
    for category, schedule in vesting_schedules.items():
        if category not in distribution:
            continue
            
        cumulative_pct = 0
        for month, pct in sorted(schedule, key=lambda x: x[0]):
            cumulative_pct += pct
            vesting_data.append({
                'Categoria': category,
                'Mês': month,
                'Porcentagem Acumulada': cumulative_pct
            })
    
    if not vesting_data:
        return None
        
    # Create dataframe
    vesting_df = pd.DataFrame(vesting_data)
    
    # Create line chart
    fig = px.line(
        vesting_df, 
        x='Mês', 
        y='Porcentagem Acumulada', 
        color='Categoria',
        title=title,
        labels={'Porcentagem Acumulada': '% Acumulada'},
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    
    fig.update_layout(
        yaxis=dict(ticksuffix="%"),
        hovermode="x unified"
    )
    
    return fig

def create_token_release_chart(
    df: pd.DataFrame,
    title: str = "Liberação de Tokens por Categoria"
) -> go.Figure:
    """
    Create a stacked area chart for token release
    
    Args:
        df (pd.DataFrame): Simulation dataframe
        title (str): Chart title
        
    Returns:
        go.Figure: Plotly figure object
    """
    # Identify token release columns
    release_columns = [col for col in df.columns if col.endswith("_Released")]
    
    # Create figure
    fig = go.Figure()
    
    for col in release_columns:
        category = col.replace("_Released", "")
        fig.add_trace(
            go.Scatter(
                x=df["Month"], 
                y=df[col],
                name=category,
                stackgroup='one',
                mode='lines'
            )
        )
    
    fig.update_layout(
        title=title,
        xaxis_title="Mês",
        yaxis_title="Tokens Liberados",
        hovermode="x unified"
    )
    
    return fig

def create_dual_axis_chart(
    df: pd.DataFrame, 
    x_column: str,
    y1_column: str, 
    y2_column: str,
    y1_title: str,
    y2_title: str,
    title: str
) -> go.Figure:
    """
    Create a chart with dual y-axes
    
    Args:
        df (pd.DataFrame): Dataframe with chart data
        x_column (str): Column name for x-axis
        y1_column (str): Column name for first y-axis
        y2_column (str): Column name for second y-axis
        y1_title (str): Title for first y-axis
        y2_title (str): Title for second y-axis
        title (str): Chart title
        
    Returns:
        go.Figure: Plotly figure object
    """
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(
            x=df[x_column], 
            y=df[y1_column],
            mode='lines',
            name=y1_title,
            line=dict(color='#0068c9', width=2)
        ),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(
            x=df[x_column], 
            y=df[y2_column],
            mode='lines',
            name=y2_title,
            line=dict(color='#ff9e0a', width=2)
        ),
        secondary_y=True
    )
    
    fig.update_layout(
        title_text=title,
        hovermode="x unified"
    )
    
    fig.update_yaxes(title_text=y1_title, secondary_y=False)
    fig.update_yaxes(title_text=y2_title, secondary_y=True)
    fig.update_xaxes(title_text="Mês")
    
    return fig

def create_price_supply_chart(
    df: pd.DataFrame,
    title_price: str = "Preço do Token ($)",
    title_supply: str = "Oferta Circulante de Tokens"
) -> go.Figure:
    """
    Create a chart with price and circulating supply
    
    Args:
        df (pd.DataFrame): Simulation dataframe
        title_price (str): Title for price subplot
        title_supply (str): Title for supply subplot
        
    Returns:
        go.Figure: Plotly figure object
    """
    fig = make_subplots(
        rows=2, 
        cols=1, 
        shared_xaxes=True, 
        vertical_spacing=0.1,
        subplot_titles=(title_price, title_supply)
    )

    # Add price line
    fig.add_trace(
        go.Scatter(
            x=df['Month'], 
            y=df['Price'],
            mode='lines',
            name='Preço',
            line=dict(color='#0068c9', width=2)
        ),
        row=1, col=1
    )

    # Add circulating supply line
    fig.add_trace(
        go.Scatter(
            x=df['Month'], 
            y=df['Circulating_Supply'],
            mode='lines',
            name='Oferta Circulante',
            line=dict(color='#83c9ff', width=2),
            fill='tozeroy'
        ),
        row=2, col=1
    )

    # Update layout
    fig.update_layout(
        height=600,
        hovermode="x unified",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    # Update y-axes
    fig.update_yaxes(title_text="Preço ($)", row=1, col=1)
    fig.update_yaxes(title_text="Tokens", row=2, col=1)
    fig.update_xaxes(title_text="Mês", row=2, col=1)

    return fig

def create_utility_token_charts(df: pd.DataFrame) -> Dict[str, go.Figure]:
    """
    Create charts specific to utility token models
    
    Args:
        df (pd.DataFrame): Simulation dataframe
        
    Returns:
        Dict[str, go.Figure]: Dictionary of chart name to figure object
    """
    charts = {}
    
    # Users chart
    charts['users'] = px.line(
        df, 
        x="Month", 
        y="Users",
        title="Crescimento de Usuários",
        labels={"Month": "Mês", "Users": "Usuários"},
        color_discrete_sequence=['#0068c9']
    )
    
    # Token demand chart
    charts['demand'] = px.line(
        df, 
        x="Month", 
        y="Token_Demand",
        title="Demanda de Tokens",
        labels={"Month": "Mês", "Token_Demand": "Demanda de Tokens"},
        color_discrete_sequence=['#ff9e0a']
    )
    
    # Supply vs demand chart
    charts['supply_vs_demand'] = px.line(
        df, 
        x="Month", 
        y=["Circulating_Supply", "Token_Demand"],
        title="Oferta vs Demanda de Tokens",
        labels={"Month": "Mês", "value": "Tokens", "variable": "Métrica"},
        color_discrete_map={
            'Circulating_Supply': '#0068c9',
            'Token_Demand': '#ff9e0a'
        }
    )
    
    charts['supply_vs_demand'].update_layout(
        hovermode="x unified"
    )
    
    return charts

def create_governance_token_charts(df: pd.DataFrame) -> Dict[str, go.Figure]:
    """
    Create charts specific to governance token models
    
    Args:
        df (pd.DataFrame): Simulation dataframe
        
    Returns:
        Dict[str, go.Figure]: Dictionary of chart name to figure object
    """
    charts = {}
    
    # Staking rate chart
    charts['staking_rate'] = px.line(
        df, 
        x="Month", 
        y="Staking_Rate",
        title="Taxa de Staking",
        labels={"Month": "Mês", "Staking_Rate": "Taxa de Staking"},
        color_discrete_sequence=['#0068c9']
    )
    
    charts['staking_rate'].update_layout(
        yaxis=dict(tickformat=".0%")
    )
    
    # Staked vs liquid tokens chart
    charts['staked_vs_liquid'] = px.line(
        df, 
        x="Month", 
        y=["Staked_Tokens", "Liquid_Tokens"],
        title="Tokens em Staking vs Tokens Líquidos",
        labels={"Month": "Mês", "value": "Tokens", "variable": "Tipo"},
        color_discrete_map={
            'Staked_Tokens': '#0068c9',
            'Liquid_Tokens': '#ff9e0a'
        }
    )
    
    charts['staked_vs_liquid'].update_layout(
        hovermode="x unified"
    )
    
    # Price vs staking rate chart
    if 'Price' in df.columns and 'Staking_Rate' in df.columns:
        # Normalize price for comparison
        df_copy = df.copy()
        df_copy['Normalized_Price'] = df_copy['Price'] / df_copy['Price'].iloc[0]
        df_copy['Staking_Rate_Pct'] = df_copy['Staking_Rate'] * 100
        
        charts['price_vs_staking'] = create_dual_axis_chart(
            df_copy,
            'Month',
            'Normalized_Price',
            'Staking_Rate_Pct',
            'Preço Normalizado',
            'Taxa de Staking (%)',
            'Correlação entre Preço e Taxa de Staking'
        )
    
    return charts

def create_matplotlib_distribution_chart(
    distribution: Dict[str, float],
    title: str = "Distribuição de Tokens"
) -> plt.Figure:
    """
    Create a Matplotlib pie chart for token distribution
    
    Args:
        distribution (Dict[str, float]): Token distribution percentages by category
        title (str): Chart title
        
    Returns:
        plt.Figure: Matplotlib figure object
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.pie(
        list(distribution.values()),
        labels=list(distribution.keys()),
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops={'edgecolor': 'white'}
    )
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    plt.title(title)
    
    return fig

def create_matplotlib_price_chart(
    df: pd.DataFrame,
    title: str = "Evolução do Preço do Token"
) -> plt.Figure:
    """
    Create a Matplotlib line chart for token price evolution
    
    Args:
        df (pd.DataFrame): Simulation dataframe
        title (str): Chart title
        
    Returns:
        plt.Figure: Matplotlib figure object
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df['Month'], df['Price'], 'b-', linewidth=2)
    ax.set_title(title)
    ax.set_xlabel('Mês')
    ax.set_ylabel('Preço ($)')
    ax.grid(True, linestyle='--', alpha=0.7)
    
    return fig

def create_matplotlib_market_cap_chart(
    df: pd.DataFrame,
    title: str = "Evolução do Market Cap"
) -> plt.Figure:
    """
    Create a Matplotlib area chart for market cap evolution
    
    Args:
        df (pd.DataFrame): Simulation dataframe
        title (str): Chart title
        
    Returns:
        plt.Figure: Matplotlib figure object
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.fill_between(df['Month'], df['Market_Cap'], alpha=0.5, color='blue')
    ax.plot(df['Month'], df['Market_Cap'], 'b-', linewidth=2)
    ax.set_title(title)
    ax.set_xlabel('Mês')
    ax.set_ylabel('Market Cap ($)')
    ax.grid(True, linestyle='--', alpha=0.7)
    
    return fig
