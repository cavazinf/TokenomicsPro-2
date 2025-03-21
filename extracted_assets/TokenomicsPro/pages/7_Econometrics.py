import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils import get_color_scale
import statsmodels.api as sm
from datetime import datetime, timedelta

# Set page configuration
st.set_page_config(
    page_title="Econometrics - TokenomicsLab",
    page_icon="📊",
    layout="wide"
)

# Load language variables
if 'language' not in st.session_state:
    st.session_state.language = 'English'

# Page title and description based on language
if st.session_state.language == 'English':
    title = "Econometrics"
    description = """
    This section provides advanced economic modeling and analysis tools for your token.
    Simulate market behaviors, analyze correlations, and forecast token metrics.
    """
    model_title = "Economic Models"
    simulation_title = "Monte Carlo Simulation"
    correlation_title = "Correlation Analysis"
    forecast_title = "Token Metric Forecasting"
    param_title = "Simulation Parameters"
    run_sim_button = "Run Simulation"
    run_corr_button = "Run Correlation Analysis"
    run_forecast_button = "Generate Forecast"
    periods_label = "Forecast Periods"
    confidence_label = "Confidence Interval (%)"
    simulation_desc = "Simulates multiple possible price paths based on volatility and growth assumptions"
    correlation_desc = "Analyzes relationships between market variables and token performance"
    forecast_desc = "Forecasts token metrics using time series analysis"
elif st.session_state.language == 'Português':
    title = "Econometria"
    description = """
    Esta seção fornece ferramentas avançadas de modelagem e análise econômica para seu token.
    Simule comportamentos de mercado, analise correlações e faça previsões de métricas de token.
    """
    model_title = "Modelos Econômicos"
    simulation_title = "Simulação de Monte Carlo"
    correlation_title = "Análise de Correlação"
    forecast_title = "Previsão de Métricas do Token"
    param_title = "Parâmetros de Simulação"
    run_sim_button = "Executar Simulação"
    run_corr_button = "Executar Análise de Correlação"
    run_forecast_button = "Gerar Previsão"
    periods_label = "Períodos de Previsão"
    confidence_label = "Intervalo de Confiança (%)"
    simulation_desc = "Simula múltiplos caminhos de preço possíveis baseados em suposições de volatilidade e crescimento"
    correlation_desc = "Analisa relações entre variáveis de mercado e desempenho do token"
    forecast_desc = "Prevê métricas do token usando análise de séries temporais"
elif st.session_state.language == 'Español':
    title = "Econometría"
    description = """
    Esta sección proporciona herramientas avanzadas de modelado y análisis económico para tu token.
    Simula comportamientos de mercado, analiza correlaciones y pronostica métricas de token.
    """
    model_title = "Modelos Económicos"
    simulation_title = "Simulación de Monte Carlo"
    correlation_title = "Análisis de Correlación"
    forecast_title = "Pronóstico de Métricas del Token"
    param_title = "Parámetros de Simulación"
    run_sim_button = "Ejecutar Simulación"
    run_corr_button = "Ejecutar Análisis de Correlación"
    run_forecast_button = "Generar Pronóstico"
    periods_label = "Períodos de Pronóstico"
    confidence_label = "Intervalo de Confianza (%)"
    simulation_desc = "Simula múltiples caminos de precio posibles basados en supuestos de volatilidad y crecimiento"
    correlation_desc = "Analiza relaciones entre variables de mercado y rendimiento del token"
    forecast_desc = "Pronostica métricas del token usando análisis de series temporales"
else:
    title = "Econometrics"
    description = """
    This section provides advanced economic modeling and analysis tools for your token.
    Simulate market behaviors, analyze correlations, and forecast token metrics.
    """
    model_title = "Economic Models"
    simulation_title = "Monte Carlo Simulation"
    correlation_title = "Correlation Analysis"
    forecast_title = "Token Metric Forecasting"
    param_title = "Simulation Parameters"
    run_sim_button = "Run Simulation"
    run_corr_button = "Run Correlation Analysis"
    run_forecast_button = "Generate Forecast"
    periods_label = "Forecast Periods"
    confidence_label = "Confidence Interval (%)"
    simulation_desc = "Simulates multiple possible price paths based on volatility and growth assumptions"
    correlation_desc = "Analyzes relationships between market variables and token performance"
    forecast_desc = "Forecasts token metrics using time series analysis"

# Page title and description
st.title(title)
st.markdown(description)

# Check if tokenomics data is initialized
if 'tokenomics_data' not in st.session_state:
    st.error("Please start from the main page to initialize your token data.")
    st.stop()

token_name = st.session_state.tokenomics_data['token_name']
token_symbol = st.session_state.tokenomics_data['token_symbol']
initial_price = st.session_state.tokenomics_data['initial_price']

# Initialize econometrics data if not present
if 'econometrics' not in st.session_state.tokenomics_data:
    st.session_state.tokenomics_data['econometrics'] = {
        'monte_carlo': {
            'simulations': 50,
            'periods': 365,
            'volatility': 0.05,
            'drift': 0.002,
            'results': None
        },
        'correlation': {
            'btc_correlation': 0.7,
            'eth_correlation': 0.8,
            'market_correlation': 0.6,
            'results': None
        },
        'forecast': {
            'periods': 90,
            'confidence': 80,
            'results': None
        }
    }

econometrics = st.session_state.tokenomics_data['econometrics']

# Tab layout for different econometric models
tab1, tab2, tab3 = st.tabs([simulation_title, correlation_title, forecast_title])

with tab1:
    st.subheader(simulation_title)
    st.markdown(simulation_desc)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(param_title)
        
        monte_carlo = econometrics['monte_carlo']
        
        num_simulations = st.slider(
            "Number of Simulations",
            min_value=10,
            max_value=100,
            value=monte_carlo['simulations'],
            step=5
        )
        
        num_periods = st.slider(
            "Simulation Period (Days)",
            min_value=30,
            max_value=730,
            value=monte_carlo['periods'],
            step=30
        )
        
        volatility = st.slider(
            "Daily Volatility (%)",
            min_value=0.1,
            max_value=15.0,
            value=float(monte_carlo['volatility'] * 100),
            step=0.1
        ) / 100
        
        drift = st.slider(
            "Daily Drift (%)",
            min_value=-1.0,
            max_value=1.0,
            value=float(monte_carlo['drift'] * 100),
            step=0.01
        ) / 100
    
    with col2:
        st.write("Initial Parameters")
        st.metric("Initial Price", f"${initial_price:.6f}")
        st.metric("Expected Annual Return", f"{drift * 365 * 100:.2f}%")
        st.metric("Annual Volatility", f"{volatility * np.sqrt(365) * 100:.2f}%")
    
    if st.button(run_sim_button):
        with st.spinner("Running Monte Carlo simulation..."):
            # Generate price paths using Monte Carlo simulation
            price_paths = []
            
            for i in range(num_simulations):
                # Generate random returns
                random_returns = np.random.normal(drift, volatility, num_periods)
                
                # Calculate price path
                price_path = [initial_price]
                for r in random_returns:
                    price_path.append(price_path[-1] * (1 + r))
                
                price_paths.append(price_path)
            
            # Convert to DataFrame
            dates = [datetime.now() + timedelta(days=i) for i in range(num_periods + 1)]
            
            sim_results = pd.DataFrame({
                'Date': dates
            })
            
            for i, path in enumerate(price_paths):
                sim_results[f'Sim {i+1}'] = path
            
            # Calculate statistics
            sim_results['Mean'] = sim_results.iloc[:, 1:num_simulations+1].mean(axis=1)
            sim_results['Max'] = sim_results.iloc[:, 1:num_simulations+1].max(axis=1)
            sim_results['Min'] = sim_results.iloc[:, 1:num_simulations+1].min(axis=1)
            sim_results['Median'] = sim_results.iloc[:, 1:num_simulations+1].median(axis=1)
            
            # Store results
            econometrics['monte_carlo'] = {
                'simulations': num_simulations,
                'periods': num_periods,
                'volatility': volatility,
                'drift': drift,
                'results': sim_results.to_dict()
            }
            
            st.session_state.tokenomics_data['econometrics'] = econometrics
            
            st.success("Monte Carlo simulation completed!")
    
    # Display simulation results if available
    if econometrics['monte_carlo'].get('results'):
        # Reconstruct DataFrame from stored dict
        mc_results = pd.DataFrame(econometrics['monte_carlo']['results'])
        
        # Plot the simulation results
        fig = go.Figure()
        
        # Add individual paths (limit to 20 for performance)
        for i in range(1, min(econometrics['monte_carlo']['simulations'], 20) + 1):
            fig.add_trace(go.Scatter(
                x=mc_results['Date'],
                y=mc_results[f'Sim {i}'],
                mode='lines',
                opacity=0.2,
                line=dict(width=1),
                showlegend=False
            ))
        
        # Add mean, min, max
        fig.add_trace(go.Scatter(
            x=mc_results['Date'],
            y=mc_results['Mean'],
            mode='lines',
            name='Mean Price',
            line=dict(color='blue', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=mc_results['Date'],
            y=mc_results['Max'],
            mode='lines',
            name='Maximum',
            line=dict(color='green', width=2, dash='dash')
        ))
        
        fig.add_trace(go.Scatter(
            x=mc_results['Date'],
            y=mc_results['Min'],
            mode='lines',
            name='Minimum',
            line=dict(color='red', width=2, dash='dash')
        ))
        
        fig.update_layout(
            title=f"{token_symbol} Price Simulation ({econometrics['monte_carlo']['simulations']} paths)",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            hovermode="x unified"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Price distribution at the end of simulation
        final_prices = mc_results.iloc[-1, 1:econometrics['monte_carlo']['simulations']+1]
        
        fig = px.histogram(
            final_prices,
            nbins=20,
            title=f"Distribution of Simulated Prices at End of Period",
            labels={'value': 'Price (USD)', 'count': 'Frequency'}
        )
        
        fig.add_vline(x=final_prices.mean(), line_dash="dash", line_color="red",
                     annotation_text=f"Mean: ${final_prices.mean():.6f}")
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Key statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Final Mean Price", f"${final_prices.mean():.6f}", f"{(final_prices.mean()/initial_price - 1) * 100:.2f}%")
        
        with col2:
            st.metric("Final Median Price", f"${final_prices.median():.6f}", f"{(final_prices.median()/initial_price - 1) * 100:.2f}%")
        
        with col3:
            st.metric("95th Percentile", f"${np.percentile(final_prices, 95):.6f}")

with tab2:
    st.subheader(correlation_title)
    st.markdown(correlation_desc)
    
    col1, col2 = st.columns(2)
    
    with col1:
        btc_correlation = st.slider(
            "Bitcoin Price Correlation",
            min_value=-1.0,
            max_value=1.0,
            value=econometrics['correlation']['btc_correlation'],
            step=0.01,
            help="Correlation between your token price and Bitcoin price"
        )
        
        eth_correlation = st.slider(
            "Ethereum Price Correlation",
            min_value=-1.0,
            max_value=1.0,
            value=econometrics['correlation']['eth_correlation'],
            step=0.01,
            help="Correlation between your token price and Ethereum price"
        )
        
        market_correlation = st.slider(
            "Overall Market Correlation",
            min_value=-1.0,
            max_value=1.0,
            value=econometrics['correlation']['market_correlation'],
            step=0.01,
            help="Correlation between your token price and the overall crypto market"
        )
    
    if st.button(run_corr_button):
        with st.spinner("Generating correlation analysis..."):
            # Generate simulated correlated data
            np.random.seed(42)  # For reproducibility
            n = 365  # One year of daily data
            
            # Generate correlated returns
            cov_matrix = np.array([
                [1.0, 0.7, 0.6, btc_correlation, eth_correlation],
                [0.7, 1.0, 0.8, btc_correlation * 0.8, eth_correlation * 0.7],
                [0.6, 0.8, 1.0, market_correlation, market_correlation * 0.9],
                [btc_correlation, btc_correlation * 0.8, market_correlation, 1.0, 0.5],
                [eth_correlation, eth_correlation * 0.7, market_correlation * 0.9, 0.5, 1.0]
            ])
            
            mean_returns = np.array([0.001, 0.0012, 0.0008, 0.002, 0.0015])  # Daily mean returns
            
            # Ensure the covariance matrix is positive semi-definite
            eigvals = np.linalg.eigvals(cov_matrix)
            if np.any(eigvals < 0):
                # Make it positive definite by adding a small value to the diagonal
                cov_matrix += np.eye(5) * 0.01
            
            # Generate correlated random returns
            returns = np.random.multivariate_normal(mean_returns, cov_matrix * 0.0001, n)
            
            # Convert to price series
            btc_price = 100 * np.cumprod(1 + returns[:, 0])
            eth_price = 100 * np.cumprod(1 + returns[:, 1])
            market_index = 100 * np.cumprod(1 + returns[:, 2])
            token_price = initial_price * np.cumprod(1 + returns[:, 3])
            defi_index = 100 * np.cumprod(1 + returns[:, 4])
            
            # Create a DataFrame with dates
            dates = [datetime.now() + timedelta(days=i) for i in range(n)]
            corr_results = pd.DataFrame({
                'Date': dates,
                'BTC': btc_price,
                'ETH': eth_price,
                'Market': market_index,
                'DeFi': defi_index,
                'Token': token_price
            })
            
            # Calculate actual correlations
            price_corr = corr_results[['BTC', 'ETH', 'Market', 'DeFi', 'Token']].corr()
            
            # Store results
            econometrics['correlation'] = {
                'btc_correlation': btc_correlation,
                'eth_correlation': eth_correlation,
                'market_correlation': market_correlation,
                'results': corr_results.to_dict(),
                'correlation_matrix': price_corr.to_dict()
            }
            
            st.session_state.tokenomics_data['econometrics'] = econometrics
            
            st.success("Correlation analysis completed!")
    
    # Display correlation results if available
    if econometrics['correlation'].get('results'):
        # Reconstruct DataFrame from stored dict
        corr_results = pd.DataFrame(econometrics['correlation']['results'])
        price_corr = pd.DataFrame(econometrics['correlation']['correlation_matrix'])
        
        # Plot price series
        fig = go.Figure()
        
        # Normalize all series to 100 at the beginning for better comparison
        normalized_data = corr_results.copy()
        for col in ['BTC', 'ETH', 'Market', 'DeFi', 'Token']:
            normalized_data[col] = 100 * normalized_data[col] / normalized_data[col].iloc[0]
        
        fig.add_trace(go.Scatter(
            x=normalized_data['Date'], y=normalized_data['Token'],
            mode='lines', name=f'{token_symbol} (Token)',
            line=dict(width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=normalized_data['Date'], y=normalized_data['BTC'],
            mode='lines', name='Bitcoin',
        ))
        
        fig.add_trace(go.Scatter(
            x=normalized_data['Date'], y=normalized_data['ETH'],
            mode='lines', name='Ethereum',
        ))
        
        fig.add_trace(go.Scatter(
            x=normalized_data['Date'], y=normalized_data['Market'],
            mode='lines', name='Crypto Market',
        ))
        
        fig.update_layout(
            title="Normalized Price Comparison (Base 100)",
            xaxis_title="Date",
            yaxis_title="Price (Normalized)",
            hovermode="x unified"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show correlation matrix heatmap
        fig = px.imshow(
            price_corr,
            text_auto=True,
            color_continuous_scale='RdBu_r',
            title="Price Correlation Matrix",
            range_color=[-1, 1],
        )
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Show key insights
        st.subheader("Key Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("BTC-Token Correlation", f"{price_corr.loc['BTC', 'Token']:.2f}")
            st.metric("ETH-Token Correlation", f"{price_corr.loc['ETH', 'Token']:.2f}")
        
        with col2:
            st.metric("Market-Token Correlation", f"{price_corr.loc['Market', 'Token']:.2f}")
            st.metric("DeFi-Token Correlation", f"{price_corr.loc['DeFi', 'Token']:.2f}")
        
        st.markdown("""
        ### Interpretation Guide
        
        - **Strong positive correlation (0.7 to 1.0)**: The token closely follows the correlated asset's price movements
        - **Moderate correlation (0.3 to 0.7)**: Some influence, but maintains some independence
        - **Low correlation (-0.3 to 0.3)**: Mostly independent price action
        - **Negative correlation (-1.0 to -0.3)**: Tends to move in the opposite direction
        
        High correlations with major assets like Bitcoin may reduce diversification benefits but can provide more predictable behavior.
        Low correlations may indicate a more unique value proposition but potentially higher volatility.
        """)

with tab3:
    st.subheader(forecast_title)
    st.markdown(forecast_desc)
    
    col1, col2 = st.columns(2)
    
    with col1:
        forecast_periods = st.slider(
            periods_label,
            min_value=30,
            max_value=365,
            value=econometrics['forecast']['periods'],
            step=30,
            help="Number of days to forecast into the future"
        )
    
    with col2:
        confidence_interval = st.slider(
            confidence_label,
            min_value=50,
            max_value=99,
            value=econometrics['forecast']['confidence'],
            step=5,
            help="Confidence interval for the forecast"
        )
    
    if st.button(run_forecast_button):
        with st.spinner("Generating forecast..."):
            # Create a simulated historical price series
            n_history = 180  # 6 months of history
            
            # Generate some realistic price history with trend and seasonality
            t = np.arange(n_history)
            trend = 0.001 * t  # Small upward trend
            seasonality = 0.05 * np.sin(2 * np.pi * t / 30)  # Monthly cycle
            noise = 0.02 * np.random.randn(n_history)  # Random noise
            
            # Combine components
            returns = trend + seasonality + noise
            price_history = initial_price * np.cumprod(1 + returns)
            
            # Create dates for the historical data
            hist_dates = [datetime.now() - timedelta(days=n_history-i) for i in range(n_history)]
            
            # Create a simple forecast model (AR model)
            # Convert to returns for stationarity
            pct_returns = np.diff(np.log(price_history))
            
            # Fit AR model
            model = sm.tsa.AutoReg(pct_returns, lags=5)
            model_fit = model.fit()
            
            # Generate forecasts
            returns_forecast = model_fit.forecast(forecast_periods)
            
            # Convert forecasted returns to prices
            last_price = price_history[-1]
            price_forecast = [last_price]
            
            for r in returns_forecast:
                price_forecast.append(price_forecast[-1] * np.exp(r))
            
            # Create confidence intervals
            std_error = np.std(model_fit.resid) * np.sqrt(np.arange(1, forecast_periods + 1))
            z_value = abs(np.percentile(np.random.standard_normal(10000), (100 - confidence_interval) / 2))
            
            lower_bound = price_forecast[1:]
            upper_bound = price_forecast[1:]
            
            for i in range(forecast_periods):
                # Confidence intervals in log space, then convert back
                lower_bound[i] = price_forecast[i+1] * np.exp(-z_value * std_error[i])
                upper_bound[i] = price_forecast[i+1] * np.exp(z_value * std_error[i])
            
            # Create dates for the forecast
            forecast_dates = [datetime.now() + timedelta(days=i) for i in range(forecast_periods + 1)]
            
            # Store the results
            forecast_results = pd.DataFrame({
                'Date': hist_dates + forecast_dates,
                'Type': ['Historical'] * n_history + ['Forecast'] * (forecast_periods + 1),
                'Price': np.concatenate([price_history, price_forecast]),
                'Lower': np.concatenate([price_history, [price_history[-1]], lower_bound]),
                'Upper': np.concatenate([price_history, [price_history[-1]], upper_bound])
            })
            
            # Store in session state
            econometrics['forecast'] = {
                'periods': forecast_periods,
                'confidence': confidence_interval,
                'results': forecast_results.to_dict()
            }
            
            st.session_state.tokenomics_data['econometrics'] = econometrics
            
            st.success("Forecast generated successfully!")
    
    # Display forecast results if available
    if econometrics['forecast'].get('results'):
        # Reconstruct DataFrame from stored dict
        forecast_results = pd.DataFrame(econometrics['forecast']['results'])
        
        # Split into historical and forecast
        historical = forecast_results[forecast_results['Type'] == 'Historical']
        forecast = forecast_results[forecast_results['Type'] == 'Forecast']
        
        # Create forecast plot
        fig = go.Figure()
        
        # Historical prices
        fig.add_trace(go.Scatter(
            x=historical['Date'],
            y=historical['Price'],
            mode='lines',
            name='Historical',
            line=dict(color='blue')
        ))
        
        # Forecast
        fig.add_trace(go.Scatter(
            x=forecast['Date'],
            y=forecast['Price'],
            mode='lines',
            name='Forecast',
            line=dict(color='red')
        ))
        
        # Confidence intervals
        fig.add_trace(go.Scatter(
            x=forecast['Date'],
            y=forecast['Upper'],
            mode='lines',
            name=f'{econometrics["forecast"]["confidence"]}% Upper Bound',
            line=dict(width=0),
            showlegend=True
        ))
        
        fig.add_trace(go.Scatter(
            x=forecast['Date'],
            y=forecast['Lower'],
            mode='lines',
            name=f'{econometrics["forecast"]["confidence"]}% Lower Bound',
            line=dict(width=0),
            fillcolor='rgba(0, 176, 246, 0.2)',
            fill='tonexty',
            showlegend=True
        ))
        
        fig.update_layout(
            title=f"{token_symbol} Price Forecast ({econometrics['forecast']['periods']} days)",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            hovermode="x unified"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Price forecast metrics
        last_historical = historical['Price'].iloc[-1]
        final_forecast = forecast['Price'].iloc[-1]
        lower_bound = forecast['Lower'].iloc[-1]
        upper_bound = forecast['Upper'].iloc[-1]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Current Price",
                f"${last_historical:.6f}"
            )
        
        with col2:
            st.metric(
                f"Forecast in {econometrics['forecast']['periods']} days",
                f"${final_forecast:.6f}",
                f"{(final_forecast/last_historical - 1) * 100:.2f}%"
            )
        
        with col3:
            st.metric(
                f"{econometrics['forecast']['confidence']}% Confidence Range",
                f"${lower_bound:.6f} to ${upper_bound:.6f}"
            )
        
        # Monthly forecasts table
        if forecast_periods >= 30:
            st.subheader("Monthly Price Forecasts")
            
            monthly_forecasts = []
            for i in range(0, forecast_periods, 30):
                if i < len(forecast):
                    idx = min(i, len(forecast) - 1)
                    monthly_forecasts.append({
                        'Month': f"Month {i//30 + 1}",
                        'Date': forecast['Date'].iloc[idx],
                        'Forecasted Price': f"${forecast['Price'].iloc[idx]:.6f}",
                        'Lower Bound': f"${forecast['Lower'].iloc[idx]:.6f}",
                        'Upper Bound': f"${forecast['Upper'].iloc[idx]:.6f}",
                        'Change from Current': f"{(forecast['Price'].iloc[idx]/last_historical - 1) * 100:.2f}%"
                    })
            
            monthly_df = pd.DataFrame(monthly_forecasts)
            st.dataframe(monthly_df, use_container_width=True)

# Information about econometric models
with st.expander("About Econometric Models"):
    st.markdown("""
    ### Econometric Models in Token Economics
    
    #### Monte Carlo Simulation
    
    Monte Carlo simulation generates multiple random price paths based on assumptions about returns and volatility.
    It helps assess the range of possible outcomes and their probabilities, rather than providing a single forecast.
    
    Key parameters:
    - **Volatility**: Measures price fluctuation (higher values = more extreme price movements)
    - **Drift**: Expected daily return (positive = upward trend, negative = downward trend)
    
    #### Correlation Analysis
    
    Correlation analysis examines how your token price moves in relation to other assets:
    - **Strong positive correlation** means assets tend to move together
    - **Negative correlation** means assets tend to move in opposite directions
    - **Low correlation** means limited relationship between price movements
    
    Understanding correlations helps with:
    - Portfolio risk management
    - Marketing positioning
    - Understanding market behavior during different conditions
    
    #### Time Series Forecasting
    
    Time series forecasting uses historical patterns to project future token price movements:
    - Accounts for trends, seasonality, and cycles
    - Provides confidence intervals around forecasts
    - Updates as new data becomes available
    
    These models are tools for exploration, not guarantees of future performance. They should be complemented with
    fundamental analysis of tokenomics, project milestones, and market conditions.
    """)