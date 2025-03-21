import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
import datetime

# Import local modules
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.tokenomics import TokenomicsModel, create_model_from_dict

st.set_page_config(
    page_title="Econometrics | Tokenomics Lab",
    page_icon="📈",
    layout="wide"
)

# Sidebar
st.sidebar.title("Tokenomics Lab")
st.sidebar.image("https://cdn.jsdelivr.net/npm/cryptocurrency-icons@0.18.1/svg/icon/btc.svg", width=50)

# Main content
st.title("Econometrics")
st.markdown("""
    Análise econométrica do modelo de token, incluindo projeções avançadas, correlações com variáveis externas
    e modelagem de cenários macroeconômicos.
""")

# Check if simulation data exists
if 'simulation_result' not in st.session_state:
    st.warning("Você precisa executar uma simulação primeiro. Vá para a página de Simulação.")
    if st.button("Ir para Simulação"):
        st.switch_page("pages/simulation.py")
    st.stop()

# Get simulation data
df = st.session_state.simulation_result
model = st.session_state.model if 'model' in st.session_state else None

# Econometric Analysis Tabs
tabs = st.tabs(["Previsão de Preço", "Correlações", "Análise de Elasticidade", "Cenários"])

with tabs[0]:
    st.header("Previsão de Preço")
    st.markdown("""
        Utilize modelos econométricos para projetar o preço do token além do período de simulação inicial.
        Esta análise utiliza métodos estatísticos como ARIMA e regressão.
    """)
    
    # Set up forecasting parameters
    forecast_period = st.slider(
        "Período de Previsão Adicional (Meses)",
        min_value=1,
        max_value=24,
        value=12,
        help="Número de meses adicionais para previsão além do período de simulação original."
    )
    
    confidence_level = st.slider(
        "Nível de Confiança (%)",
        min_value=50,
        max_value=99,
        value=95,
        help="Nível de confiança para os intervalos de previsão."
    )
    
    forecast_model = st.selectbox(
        "Modelo de Previsão",
        ["ARIMA", "SARIMAX", "Regressão Linear"],
        help="Modelo estatístico para realizar a previsão."
    )
    
    if st.button("Executar Previsão"):
        with st.spinner("Calculando previsão..."):
            # Prepare data
            y = df['Price']
            X = df[['Month']]
            
            # Fit model based on selection
            if forecast_model == "ARIMA":
                try:
                    # Use statsmodels ARIMA
                    model_fit = ARIMA(y, order=(2,1,2)).fit()
                    
                    # Make forecast
                    forecast_result = model_fit.get_forecast(forecast_period)
                    forecast_mean = forecast_result.predicted_mean
                    forecast_ci = forecast_result.conf_int(alpha=(100-confidence_level)/100)
                    
                    # Create forecast dataframe
                    last_month = df['Month'].max()
                    forecast_index = range(last_month+1, last_month+forecast_period+1)
                    forecast_df = pd.DataFrame({
                        'Month': forecast_index,
                        'Price': forecast_mean.values,
                        'Lower_CI': forecast_ci.iloc[:, 0].values,
                        'Upper_CI': forecast_ci.iloc[:, 1].values
                    })
                    
                    # Create combined dataframe for plotting
                    combined_df = pd.concat([
                        df[['Month', 'Price']],
                        forecast_df[['Month', 'Price', 'Lower_CI', 'Upper_CI']]
                    ], axis=0)
                    
                    # Plot results
                    fig = go.Figure()
                    
                    # Historical data
                    fig.add_trace(
                        go.Scatter(
                            x=df['Month'],
                            y=df['Price'],
                            mode='lines',
                            name='Dados Históricos',
                            line=dict(color='blue')
                        )
                    )
                    
                    # Forecasted data
                    fig.add_trace(
                        go.Scatter(
                            x=forecast_df['Month'],
                            y=forecast_df['Price'],
                            mode='lines',
                            name='Previsão',
                            line=dict(color='red', dash='dash')
                        )
                    )
                    
                    # Confidence intervals
                    fig.add_trace(
                        go.Scatter(
                            x=forecast_df['Month'],
                            y=forecast_df['Upper_CI'],
                            mode='lines',
                            name=f'Intervalo de Confiança {confidence_level}%',
                            line=dict(width=0),
                            showlegend=False
                        )
                    )
                    
                    fig.add_trace(
                        go.Scatter(
                            x=forecast_df['Month'],
                            y=forecast_df['Lower_CI'],
                            mode='lines',
                            name=f'Intervalo de Confiança {confidence_level}%',
                            line=dict(width=0),
                            fillcolor='rgba(68, 68, 68, 0.3)',
                            fill='tonexty',
                            showlegend=True
                        )
                    )
                    
                    fig.update_layout(
                        title=f'Previsão de Preço com {forecast_model} - {forecast_period} Meses',
                        xaxis_title='Mês',
                        yaxis_title='Preço ($)',
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                        height=600
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Summary statistics
                    st.subheader("Estatísticas da Previsão")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric(
                            "Preço Final Previsto",
                            f"${forecast_df['Price'].iloc[-1]:.4f}",
                            f"{(forecast_df['Price'].iloc[-1] / df['Price'].iloc[-1] - 1) * 100:.2f}%"
                        )
                    
                    with col2:
                        st.metric(
                            "Limite Inferior de Confiança",
                            f"${forecast_df['Lower_CI'].iloc[-1]:.4f}"
                        )
                    
                    with col3:
                        st.metric(
                            "Limite Superior de Confiança",
                            f"${forecast_df['Upper_CI'].iloc[-1]:.4f}"
                        )
                    
                    # Display forecast data
                    st.subheader("Dados da Previsão")
                    st.dataframe(forecast_df)
                    
                except Exception as e:
                    st.error(f"Erro ao executar o modelo ARIMA: {str(e)}")
                    st.info("Tente utilizar um modelo diferente ou ajustar os parâmetros.")
            
            elif forecast_model == "SARIMAX":
                try:
                    # Simplified model for demonstration
                    model_fit = SARIMAX(y, order=(1, 1, 1), seasonal_order=(0, 0, 0, 0)).fit(disp=False)
                    
                    # Make forecast
                    forecast_result = model_fit.get_forecast(forecast_period)
                    forecast_mean = forecast_result.predicted_mean
                    forecast_ci = forecast_result.conf_int(alpha=(100-confidence_level)/100)
                    
                    # Create forecast dataframe
                    last_month = df['Month'].max()
                    forecast_index = range(last_month+1, last_month+forecast_period+1)
                    forecast_df = pd.DataFrame({
                        'Month': forecast_index,
                        'Price': forecast_mean.values,
                        'Lower_CI': forecast_ci.iloc[:, 0].values,
                        'Upper_CI': forecast_ci.iloc[:, 1].values
                    })
                    
                    # Create plot
                    fig = go.Figure()
                    
                    # Historical data
                    fig.add_trace(
                        go.Scatter(
                            x=df['Month'],
                            y=df['Price'],
                            mode='lines',
                            name='Dados Históricos',
                            line=dict(color='blue')
                        )
                    )
                    
                    # Forecasted data
                    fig.add_trace(
                        go.Scatter(
                            x=forecast_df['Month'],
                            y=forecast_df['Price'],
                            mode='lines',
                            name='Previsão',
                            line=dict(color='red', dash='dash')
                        )
                    )
                    
                    # Confidence intervals
                    fig.add_trace(
                        go.Scatter(
                            x=forecast_df['Month'],
                            y=forecast_df['Upper_CI'],
                            mode='lines',
                            name=f'Intervalo de Confiança {confidence_level}%',
                            line=dict(width=0),
                            showlegend=False
                        )
                    )
                    
                    fig.add_trace(
                        go.Scatter(
                            x=forecast_df['Month'],
                            y=forecast_df['Lower_CI'],
                            mode='lines',
                            name=f'Intervalo de Confiança {confidence_level}%',
                            line=dict(width=0),
                            fillcolor='rgba(68, 68, 68, 0.3)',
                            fill='tonexty',
                            showlegend=True
                        )
                    )
                    
                    fig.update_layout(
                        title=f'Previsão de Preço com {forecast_model} - {forecast_period} Meses',
                        xaxis_title='Mês',
                        yaxis_title='Preço ($)',
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                        height=600
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Summary statistics
                    st.subheader("Estatísticas da Previsão")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric(
                            "Preço Final Previsto",
                            f"${forecast_df['Price'].iloc[-1]:.4f}",
                            f"{(forecast_df['Price'].iloc[-1] / df['Price'].iloc[-1] - 1) * 100:.2f}%"
                        )
                    
                    with col2:
                        st.metric(
                            "Limite Inferior de Confiança",
                            f"${forecast_df['Lower_CI'].iloc[-1]:.4f}"
                        )
                    
                    with col3:
                        st.metric(
                            "Limite Superior de Confiança",
                            f"${forecast_df['Upper_CI'].iloc[-1]:.4f}"
                        )
                    
                    # Display forecast data
                    st.subheader("Dados da Previsão")
                    st.dataframe(forecast_df)
                    
                except Exception as e:
                    st.error(f"Erro ao executar o modelo SARIMAX: {str(e)}")
                    st.info("Tente utilizar um modelo diferente ou ajustar os parâmetros.")
            
            elif forecast_model == "Regressão Linear":
                try:
                    # Add constant to predictor
                    X = sm.add_constant(X)
                    
                    # Fit regression model
                    model_fit = sm.OLS(y, X).fit()
                    
                    # Make predictions for future months
                    last_month = df['Month'].max()
                    future_months = pd.DataFrame({
                        'Month': range(last_month+1, last_month+forecast_period+1)
                    })
                    future_months_with_const = sm.add_constant(future_months)
                    
                    # Predict mean
                    forecast_mean = model_fit.predict(future_months_with_const)
                    
                    # Predict confidence intervals
                    forecast_ci = model_fit.get_prediction(future_months_with_const).conf_int(alpha=(100-confidence_level)/100)
                    
                    # Create forecast dataframe
                    forecast_df = pd.DataFrame({
                        'Month': future_months['Month'],
                        'Price': forecast_mean,
                        'Lower_CI': forecast_ci.iloc[:, 0],
                        'Upper_CI': forecast_ci.iloc[:, 1]
                    })
                    
                    # Create plot
                    fig = go.Figure()
                    
                    # Historical data
                    fig.add_trace(
                        go.Scatter(
                            x=df['Month'],
                            y=df['Price'],
                            mode='lines',
                            name='Dados Históricos',
                            line=dict(color='blue')
                        )
                    )
                    
                    # Forecasted data
                    fig.add_trace(
                        go.Scatter(
                            x=forecast_df['Month'],
                            y=forecast_df['Price'],
                            mode='lines',
                            name='Previsão',
                            line=dict(color='red', dash='dash')
                        )
                    )
                    
                    # Confidence intervals
                    fig.add_trace(
                        go.Scatter(
                            x=forecast_df['Month'],
                            y=forecast_df['Upper_CI'],
                            mode='lines',
                            name=f'Intervalo de Confiança {confidence_level}%',
                            line=dict(width=0),
                            showlegend=False
                        )
                    )
                    
                    fig.add_trace(
                        go.Scatter(
                            x=forecast_df['Month'],
                            y=forecast_df['Lower_CI'],
                            mode='lines',
                            name=f'Intervalo de Confiança {confidence_level}%',
                            line=dict(width=0),
                            fillcolor='rgba(68, 68, 68, 0.3)',
                            fill='tonexty',
                            showlegend=True
                        )
                    )
                    
                    fig.update_layout(
                        title=f'Previsão de Preço com {forecast_model} - {forecast_period} Meses',
                        xaxis_title='Mês',
                        yaxis_title='Preço ($)',
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                        height=600
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Model summary
                    st.subheader("Resumo do Modelo")
                    st.text(model_fit.summary().as_text())
                    
                    # Summary statistics
                    st.subheader("Estatísticas da Previsão")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric(
                            "Preço Final Previsto",
                            f"${forecast_df['Price'].iloc[-1]:.4f}",
                            f"{(forecast_df['Price'].iloc[-1] / df['Price'].iloc[-1] - 1) * 100:.2f}%"
                        )
                    
                    with col2:
                        st.metric(
                            "Limite Inferior de Confiança",
                            f"${forecast_df['Lower_CI'].iloc[-1]:.4f}"
                        )
                    
                    with col3:
                        st.metric(
                            "Limite Superior de Confiança",
                            f"${forecast_df['Upper_CI'].iloc[-1]:.4f}"
                        )
                    
                    # Display forecast data
                    st.subheader("Dados da Previsão")
                    st.dataframe(forecast_df)
                    
                except Exception as e:
                    st.error(f"Erro ao executar o modelo de Regressão Linear: {str(e)}")
                    st.info("Tente utilizar um modelo diferente ou ajustar os parâmetros.")

with tabs[1]:
    st.header("Análise de Correlações")
    st.markdown("""
        Analise as correlações entre diferentes variáveis do modelo para entender como os fatores se influenciam.
        Identificar correlações fortes pode ajudar a otimizar o design de tokenomics.
    """)
    
    # Select variables for correlation analysis
    available_columns = df.columns.tolist()
    
    # Exclude non-numeric columns for correlation
    exclude_cols = ['Month']
    numeric_columns = [col for col in available_columns if col not in exclude_cols]
    
    if len(numeric_columns) < 2:
        st.warning("São necessárias pelo menos duas variáveis numéricas para análise de correlação.")
    else:
        # Let user select variables
        selected_vars = st.multiselect(
            "Selecione as variáveis para análise de correlação",
            options=numeric_columns,
            default=["Price", "Circulating_Supply", "Market_Cap"],
            help="Escolha pelo menos duas variáveis para analisar suas correlações."
        )
        
        if len(selected_vars) < 2:
            st.warning("Selecione pelo menos duas variáveis para análise.")
        else:
            # Calculate correlation matrix
            corr_matrix = df[selected_vars].corr()
            
            # Plot heatmap
            fig = px.imshow(
                corr_matrix, 
                text_auto=True, 
                color_continuous_scale='RdBu_r',
                title="Matriz de Correlação",
                labels=dict(x="Variável", y="Variável", color="Correlação")
            )
            
            fig.update_layout(
                height=600,
                width=700
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Strongest correlations
            st.subheader("Correlações Mais Fortes")
            
            # Convert correlation matrix to long format
            corr_data = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i):
                    corr_data.append({
                        'Variable 1': corr_matrix.columns[i],
                        'Variable 2': corr_matrix.columns[j],
                        'Correlation': corr_matrix.iloc[i, j]
                    })
            
            if corr_data:
                corr_df = pd.DataFrame(corr_data)
                corr_df['Abs_Correlation'] = corr_df['Correlation'].abs()
                corr_df = corr_df.sort_values('Abs_Correlation', ascending=False)
                
                st.dataframe(corr_df[['Variable 1', 'Variable 2', 'Correlation']])
                
                # Scatter plot for top correlation
                if not corr_df.empty:
                    top_corr = corr_df.iloc[0]
                    var1 = top_corr['Variable 1']
                    var2 = top_corr['Variable 2']
                    corr_val = top_corr['Correlation']
                    
                    st.subheader(f"Visualização da Correlação mais Forte: {var1} vs {var2} ({corr_val:.3f})")
                    
                    fig = px.scatter(
                        df, 
                        x=var1, 
                        y=var2, 
                        trendline="ols",
                        title=f"Correlação entre {var1} e {var2}",
                        labels={var1: var1, var2: var2}
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Interpretation
                    st.subheader("Interpretação")
                    
                    corr_value = corr_val
                    if corr_value > 0.7:
                        st.info(f"Existe uma forte correlação positiva ({corr_value:.3f}) entre {var1} e {var2}, " 
                                f"indicando que quando {var1} aumenta, {var2} também tende a aumentar significativamente.")
                    elif corr_value > 0.3:
                        st.info(f"Existe uma correlação positiva moderada ({corr_value:.3f}) entre {var1} e {var2}, " 
                                f"indicando alguma tendência de aumento conjunto.")
                    elif corr_value > -0.3:
                        st.info(f"A correlação ({corr_value:.3f}) entre {var1} e {var2} é fraca, " 
                                f"indicando pouca relação linear entre as variáveis.")
                    elif corr_value > -0.7:
                        st.info(f"Existe uma correlação negativa moderada ({corr_value:.3f}) entre {var1} e {var2}, " 
                                f"indicando que quando uma variável aumenta, a outra tende a diminuir moderadamente.")
                    else:
                        st.info(f"Existe uma forte correlação negativa ({corr_value:.3f}) entre {var1} e {var2}, " 
                                f"indicando que quando uma variável aumenta, a outra tende a diminuir significativamente.")

with tabs[2]:
    st.header("Análise de Elasticidade")
    st.markdown("""
        A elasticidade mede como uma variável responde a mudanças em outra variável.
        Esta análise é crucial para entender a sensibilidade do preço do token em relação 
        a fatores como oferta circulante, demanda e outras variáveis do modelo.
    """)
    
    # Choose variables for elasticity analysis
    dependent_var = st.selectbox(
        "Variável Dependente (Y)",
        options=numeric_columns,
        index=numeric_columns.index("Price") if "Price" in numeric_columns else 0,
        help="Variável cujas mudanças você quer analisar (geralmente o preço)."
    )
    
    independent_vars = [col for col in numeric_columns if col != dependent_var]
    
    if not independent_vars:
        st.warning("Não há variáveis independentes disponíveis para análise de elasticidade.")
    else:
        independent_var = st.selectbox(
            "Variável Independente (X)",
            options=independent_vars,
            index=independent_vars.index("Circulating_Supply") if "Circulating_Supply" in independent_vars else 0,
            help="Variável que influencia a variável dependente."
        )
        
        # Calculate elasticity
        if st.button("Calcular Elasticidade"):
            try:
                # Create log-transformed data for elasticity calculation
                log_data = pd.DataFrame({
                    'log_y': np.log(df[dependent_var]),
                    'log_x': np.log(df[independent_var])
                }).dropna()
                
                if len(log_data) < 3:
                    st.error("Dados insuficientes para calcular elasticidade. Verifique se há valores zero ou negativos nas variáveis selecionadas.")
                else:
                    # Add constant
                    log_data = sm.add_constant(log_data)
                    
                    # Fit regression model
                    model = sm.OLS(log_data['log_y'], log_data[['const', 'log_x']]).fit()
                    
                    # The coefficient of log_x is the elasticity
                    elasticity = model.params['log_x']
                    
                    # Display results
                    st.subheader("Resultados da Análise de Elasticidade")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric(
                            "Elasticidade",
                            f"{elasticity:.4f}"
                        )
                        
                        # Interpretation
                        if abs(elasticity) < 0.5:
                            elasticity_type = "Inelástica"
                            interpretation = f"Uma variação de 1% em {independent_var} resulta em apenas {abs(elasticity):.2f}% de variação em {dependent_var}."
                        elif abs(elasticity) < 1.0:
                            elasticity_type = "Menos Elástica"
                            interpretation = f"Uma variação de 1% em {independent_var} resulta em {abs(elasticity):.2f}% de variação em {dependent_var}."
                        elif abs(elasticity) < 1.5:
                            elasticity_type = "Elasticidade Unitária"
                            interpretation = f"Uma variação de 1% em {independent_var} resulta em aproximadamente a mesma variação ({abs(elasticity):.2f}%) em {dependent_var}."
                        else:
                            elasticity_type = "Altamente Elástica"
                            interpretation = f"Uma variação de 1% em {independent_var} resulta em uma grande variação de {abs(elasticity):.2f}% em {dependent_var}."
                        
                        sign = "positiva" if elasticity > 0 else "negativa"
                        
                        st.markdown(f"**Classificação:** {elasticity_type}")
                        st.markdown(f"**Direção:** Correlação {sign}")
                        st.markdown(f"**Interpretação:** {interpretation}")
                    
                    with col2:
                        # Create scatter plot with fitted line
                        fig = px.scatter(
                            df, 
                            x=independent_var, 
                            y=dependent_var, 
                            trendline="ols",
                            title=f"Relação entre {dependent_var} e {independent_var}",
                            labels={independent_var: independent_var, dependent_var: dependent_var}
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Display regression summary
                    st.subheader("Resumo do Modelo de Regressão")
                    st.text(model.summary().as_text())
                    
                    # Implications
                    st.subheader("Implicações para o Tokenomics")
                    
                    if independent_var == "Circulating_Supply" and dependent_var == "Price":
                        if elasticity < -0.8:
                            st.info(f"A alta elasticidade negativa ({elasticity:.2f}) indica que o preço é muito sensível a mudanças na oferta circulante. Isto sugere que controlar cuidadosamente o cronograma de vesting e liberação de tokens é crucial para a estabilidade de preço.")
                        elif elasticity < -0.3:
                            st.info(f"A elasticidade moderada ({elasticity:.2f}) indica que aumentos na oferta circulante têm um impacto negativo no preço, mas não tão severo. Um cronograma de vesting gradual é recomendado.")
                        else:
                            st.info(f"A baixa elasticidade ({elasticity:.2f}) sugere que o preço não é muito sensível a mudanças na oferta circulante, indicando que outros fatores podem ter maior influência no preço do token.")
                    elif independent_var == "Market_Cap" and dependent_var == "Price":
                        if elasticity > 0.8:
                            st.info(f"A alta elasticidade positiva ({elasticity:.2f}) entre market cap e preço sugere uma forte correlação. Estratégias que aumentam o valor de mercado terão um impacto significativo no preço do token.")
                        else:
                            st.info(f"A elasticidade moderada ({elasticity:.2f}) entre market cap e preço sugere que, embora relacionados, outros fatores também influenciam significativamente o preço do token.")
                    elif "Staking" in independent_var and dependent_var == "Price":
                        if elasticity > 0.5:
                            st.info(f"A elasticidade positiva ({elasticity:.2f}) entre staking e preço sugere que incentivos de staking podem ser uma estratégia efetiva para suportar o preço do token.")
                        else:
                            st.info(f"A elasticidade modesta ({elasticity:.2f}) entre staking e preço sugere que, embora o staking contribua para o suporte de preço, seu impacto é limitado.")
                    else:
                        st.info(f"A elasticidade de {elasticity:.2f} entre {dependent_var} e {independent_var} fornece insights sobre como esses fatores se inter-relacionam em seu modelo de tokenomics. Considere este valor ao ajustar parâmetros do modelo.")
            
            except Exception as e:
                st.error(f"Erro ao calcular elasticidade: {str(e)}")
                st.info("Verifique se as variáveis selecionadas contêm valores válidos para análise logarítmica (não podem ter zeros ou valores negativos).")

with tabs[3]:
    st.header("Simulação de Cenários Macroeconômicos")
    st.markdown("""
        Analise como diferentes cenários macroeconômicos podem impactar seu token.
        Esta ferramenta permite simular o comportamento do token sob diferentes condições de mercado.
    """)
    
    # Scenario options
    scenario = st.selectbox(
        "Selecione um Cenário Macroeconômico",
        [
            "Mercado de Alta (Bull Market)",
            "Mercado de Baixa (Bear Market)",
            "Alta Inflação",
            "Recessão Econômica",
            "Adoção Acelerada de Criptomoedas",
            "Regulação Restritiva",
            "Cenário Personalizado"
        ]
    )
    
    # Set default parameters based on selected scenario
    if scenario == "Mercado de Alta (Bull Market)":
        market_growth = 0.2
        volatility_factor = 1.5
        adoption_factor = 1.3
        regulatory_impact = 0.0
    elif scenario == "Mercado de Baixa (Bear Market)":
        market_growth = -0.15
        volatility_factor = 2.0
        adoption_factor = 0.7
        regulatory_impact = 0.0
    elif scenario == "Alta Inflação":
        market_growth = 0.05
        volatility_factor = 1.8
        adoption_factor = 0.9
        regulatory_impact = 0.0
    elif scenario == "Recessão Econômica":
        market_growth = -0.1
        volatility_factor = 1.7
        adoption_factor = 0.6
        regulatory_impact = 0.1
    elif scenario == "Adoção Acelerada de Criptomoedas":
        market_growth = 0.25
        volatility_factor = 1.2
        adoption_factor = 2.0
        regulatory_impact = -0.05
    elif scenario == "Regulação Restritiva":
        market_growth = -0.05
        volatility_factor = 1.6
        adoption_factor = 0.8
        regulatory_impact = 0.3
    else:  # Cenário Personalizado
        market_growth = 0.0
        volatility_factor = 1.0
        adoption_factor = 1.0
        regulatory_impact = 0.0
    
    # Allow customization of parameters
    st.subheader("Parâmetros do Cenário")
    
    col1, col2 = st.columns(2)
    
    with col1:
        market_growth = st.slider(
            "Crescimento de Mercado",
            min_value=-0.5,
            max_value=0.5,
            value=market_growth,
            step=0.05,
            format="%+.0f%%",
            help="Crescimento ou declínio geral do mercado de criptomoedas."
        )
        
        volatility_factor = st.slider(
            "Fator de Volatilidade",
            min_value=0.5,
            max_value=3.0,
            value=volatility_factor,
            step=0.1,
            help="Multiplicador da volatilidade normal do token."
        )
    
    with col2:
        adoption_factor = st.slider(
            "Fator de Adoção",
            min_value=0.1,
            max_value=3.0,
            value=adoption_factor,
            step=0.1,
            help="Taxa de crescimento de usuários/uso em relação ao normal."
        )
        
        regulatory_impact = st.slider(
            "Impacto Regulatório",
            min_value=-0.3,
            max_value=0.5,
            value=regulatory_impact,
            step=0.05,
            help="Impacto de regulações no valor do token (negativo=favorável, positivo=desfavorável)."
        )
    
    # Simulation length
    sim_months = st.slider(
        "Período de Simulação (Meses)",
        min_value=6,
        max_value=36,
        value=12,
        step=6
    )
    
    # Run simulation
    if st.button("Simular Cenário", type="primary"):
        with st.spinner(f"Simulando cenário '{scenario}'..."):
            try:
                # Start with base data
                last_price = df['Price'].iloc[-1]
                last_supply = df['Circulating_Supply'].iloc[-1]
                max_supply = st.session_state.model.total_supply
                
                # Generate dates for simulation
                last_month = df['Month'].max()
                sim_months_range = range(last_month + 1, last_month + sim_months + 1)
                
                # Create simulation data
                prices = [last_price]
                supplies = [last_supply]
                
                # Simple simulation model
                for i in range(sim_months):
                    # Calculate new supply (simplified)
                    new_supply = min(supplies[-1] * (1 + 0.02 * adoption_factor), max_supply)
                    supplies.append(new_supply)
                    
                    # Calculate price impact factors
                    supply_factor = supplies[-2] / supplies[-1] if supplies[-1] > 0 else 1
                    market_factor = 1 + market_growth / 12  # Monthly growth
                    reg_factor = 1 - regulatory_impact / 12  # Monthly impact
                    random_factor = 1 + np.random.normal(0, 0.08 * volatility_factor)
                    
                    # Calculate new price
                    new_price = prices[-1] * supply_factor * market_factor * reg_factor * random_factor
                    new_price = max(new_price, 0.00001)  # Prevent negative prices
                    prices.append(new_price)
                
                # Create dataframe
                scenario_df = pd.DataFrame({
                    'Month': sim_months_range,
                    'Price': prices[1:],
                    'Circulating_Supply': supplies[1:],
                    'Market_Cap': [p * s for p, s in zip(prices[1:], supplies[1:])]
                })
                
                # Combine with original data for plotting
                combined_df = pd.concat([
                    df[['Month', 'Price', 'Circulating_Supply', 'Market_Cap']],
                    scenario_df
                ], axis=0)
                
                # Plot results
                st.subheader(f"Resultados da Simulação: {scenario}")
                
                # Price chart
                fig = go.Figure()
                
                # Add historical data
                fig.add_trace(
                    go.Scatter(
                        x=df['Month'],
                        y=df['Price'],
                        mode='lines',
                        name='Dados Históricos',
                        line=dict(color='blue')
                    )
                )
                
                # Add scenario data
                fig.add_trace(
                    go.Scatter(
                        x=scenario_df['Month'],
                        y=scenario_df['Price'],
                        mode='lines',
                        name=f'Cenário: {scenario}',
                        line=dict(color='red')
                    )
                )
                
                fig.update_layout(
                    title='Projeção de Preço do Token',
                    xaxis_title='Mês',
                    yaxis_title='Preço ($)',
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Key metrics
                st.subheader("Métricas-Chave do Cenário")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    price_change = (scenario_df['Price'].iloc[-1] / df['Price'].iloc[-1] - 1) * 100
                    st.metric(
                        "Preço Final Projetado",
                        f"${scenario_df['Price'].iloc[-1]:.4f}",
                        f"{price_change:.2f}%"
                    )
                
                with col2:
                    supply_change = (scenario_df['Circulating_Supply'].iloc[-1] / df['Circulating_Supply'].iloc[-1] - 1) * 100
                    st.metric(
                        "Oferta Circulante Final",
                        f"{scenario_df['Circulating_Supply'].iloc[-1]:,.0f}",
                        f"{supply_change:.2f}%"
                    )
                
                with col3:
                    mcap_change = (scenario_df['Market_Cap'].iloc[-1] / df['Market_Cap'].iloc[-1] - 1) * 100
                    st.metric(
                        "Market Cap Final",
                        f"${scenario_df['Market_Cap'].iloc[-1]:,.2f}",
                        f"{mcap_change:.2f}%"
                    )
                
                # Scenario analysis
                st.subheader("Análise do Cenário")
                
                if price_change > 50:
                    price_assessment = "extremamente positivo"
                elif price_change > 20:
                    price_assessment = "muito positivo"
                elif price_change > 0:
                    price_assessment = "positivo"
                elif price_change > -20:
                    price_assessment = "ligeiramente negativo"
                else:
                    price_assessment = "fortemente negativo"
                
                st.markdown(f"""
                    **Impacto no Preço:** O cenário '{scenario}' tem um impacto {price_assessment} no preço do token, 
                    resultando em uma mudança de {price_change:.2f}% ao longo de {sim_months} meses.
                    
                    **Recomendações:**
                """)
                
                if price_change < 0:
                    st.markdown("""
                        - Considere ajustar o cronograma de vesting para reduzir a pressão de venda durante este período
                        - Implemente programas de staking ou recompensas para incentivar a retenção de tokens
                        - Enfatize os casos de uso de longo prazo do token para mitigar vendas baseadas em medo
                    """)
                else:
                    st.markdown("""
                        - Este cenário favorece o crescimento do valor do token
                        - Considere acelerar o desenvolvimento e adoção do projeto durante este período favorável
                        - Mantenha reservas para o caso de reversão do cenário positivo
                    """)
                
                # Display full simulation data
                st.subheader("Dados Completos da Simulação")
                st.dataframe(scenario_df)
                
            except Exception as e:
                st.error(f"Erro na simulação: {str(e)}")
                st.info("Verifique os parâmetros do modelo e tente novamente.")

# Add this simulation to the model's data for reporting
if st.sidebar.button("Salvar Análise Econométrica para Relatório"):
    if 'econometric_analysis' not in st.session_state:
        st.session_state.econometric_analysis = {}
    
    # Store current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Save a basic record of the analysis performed
    st.session_state.econometric_analysis[timestamp] = {
        "type": "Econometric Analysis",
        "description": "Análise econométrica incluindo projeções de preço, correlações e simulações de cenários.",
        "model_name": st.session_state.model.name if 'model' in st.session_state else "N/A"
    }
    
    st.sidebar.success("Análise econométrica salva para inclusão no relatório final!")