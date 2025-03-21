import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
from datetime import datetime, timedelta
import time
import math
from models.tokenomics import TokenomicsModel, UtilityTokenModel, GovernanceTokenModel

st.set_page_config(
    page_title="Benchmark de Tokenomics | Tokenomics Lab",
    page_icon="🔍",
    layout="wide"
)

# Função para gastar créditos (importada do app.py)
def spend_credits(feature_name, cost=1):
    if 'credits' not in st.session_state:
        st.session_state.credits = 0
    if 'features_used' not in st.session_state:
        st.session_state.features_used = {}
        
    if st.session_state.credits >= cost:
        st.session_state.credits -= cost
        
        # Registro de uso de recursos
        if feature_name in st.session_state.features_used:
            st.session_state.features_used[feature_name] += 1
        else:
            st.session_state.features_used[feature_name] = 1
            
        return True
    else:
        st.warning(f"Créditos insuficientes para usar {feature_name}. Por favor, adquira mais créditos ou assine um plano.")
        return False

# Inicializar estados da sessão para benchmark
if 'benchmark_models' not in st.session_state:
    st.session_state.benchmark_models = {}
if 'benchmark_results' not in st.session_state:
    st.session_state.benchmark_results = {}
if 'benchmark_running' not in st.session_state:
    st.session_state.benchmark_running = False
if 'simulation_months' not in st.session_state:
    st.session_state.simulation_months = 36
if 'current_month' not in st.session_state:
    st.session_state.current_month = 0
if 'speed_multiplier' not in st.session_state:
    st.session_state.speed_multiplier = 1
if 'last_update_time' not in st.session_state:
    st.session_state.last_update_time = datetime.now()

# Título e introdução
st.title("🔍 Benchmark de Estratégias de Tokenomics")
st.markdown("""
    Compare diferentes estratégias de tokenomics lado a lado para identificar qual modelo 
    pode ser mais adequado para seu projeto. Simule cenários e veja como cada modelo se comporta 
    em termos de preço, liquidez, adoção e outros indicadores importantes.
""")

# Layout principal
tab1, tab2 = st.tabs(["Configuração de Modelos", "Análise Comparativa"])

with tab1:
    st.subheader("Configure os Modelos para Comparação")
    
    # Configurações gerais da simulação
    col_general, col_controls = st.columns([3, 1])
    
    with col_general:
        st.markdown("### Parâmetros da Simulação")
        
        months = st.slider(
            "Duração da Simulação (meses)",
            min_value=12,
            max_value=60,
            value=st.session_state.simulation_months,
            step=12,
            help="Período de tempo para simular os modelos"
        )
        st.session_state.simulation_months = months
        
        market_conditions = st.select_slider(
            "Condições de Mercado",
            options=["Muito Negativas", "Negativas", "Neutras", "Positivas", "Muito Positivas"],
            value="Neutras",
            help="Impacta todas as simulações com um viés geral de mercado"
        )
        
        market_bias = {
            "Muito Negativas": -0.02,
            "Negativas": -0.01, 
            "Neutras": 0.0,
            "Positivas": 0.01,
            "Muito Positivas": 0.02
        }[market_conditions]
        
        volatility = st.slider(
            "Volatilidade do Mercado",
            min_value=0.05,
            max_value=0.3,
            value=0.15,
            step=0.05,
            format="%.2f",
            help="Quanto maior, mais voláteis serão os preços simulados"
        )
        
        speed_options = {
            "0.5x (Lento)": 0.5,
            "1x (Normal)": 1,
            "2x (Rápido)": 2,
            "5x (Ultra-rápido)": 5
        }
        
        selected_speed = st.selectbox(
            "Velocidade da Simulação",
            options=list(speed_options.keys()),
            index=1
        )
        st.session_state.speed_multiplier = speed_options[selected_speed]
    
    with col_controls:
        st.markdown("### Controles")
        
        # Botão para iniciar/pausar simulação
        start_button = st.button(
            "Iniciar Benchmark" if not st.session_state.benchmark_running else "Pausar Benchmark",
            use_container_width=True
        )
        
        if start_button:
            if not st.session_state.benchmark_running:
                # Verificar se há modelos suficientes para comparar
                if len(st.session_state.benchmark_models) >= 2:
                    # Verificar créditos
                    if spend_credits("Benchmark de Tokenomics", 5):  # Custo mais alto por ser análise avançada
                        st.session_state.benchmark_running = True
                        st.session_state.current_month = 0
                        st.session_state.last_update_time = datetime.now()
                        
                        # Inicializar resultados
                        st.session_state.benchmark_results = {}
                        for model_id, model in st.session_state.benchmark_models.items():
                            initial_price = 1.0  # Todos começam do mesmo ponto para comparação justa
                            st.session_state.benchmark_results[model_id] = {
                                'data': pd.DataFrame({
                                    'Month': [0],
                                    'Price': [initial_price],
                                    'Circulating_Supply': [0],
                                    'Market_Cap': [0],
                                    'Adoption': [0],
                                    'ROI': [0]
                                }),
                                'events': []
                            }
                        st.rerun()
                else:
                    st.error("Adicione pelo menos dois modelos para executar o benchmark.")
            else:
                st.session_state.benchmark_running = False
        
        # Botão para reiniciar simulação
        if st.button("Reiniciar Benchmark", use_container_width=True):
            st.session_state.benchmark_running = False
            st.session_state.current_month = 0
            st.session_state.benchmark_results = {}
            st.rerun()
            
        # Botão para limpar todos os modelos
        if st.button("Limpar Todos Modelos", use_container_width=True):
            st.session_state.benchmark_models = {}
            st.session_state.benchmark_results = {}
            st.session_state.benchmark_running = False
            st.session_state.current_month = 0
            st.rerun()
    
    # Formulário para adicionar novo modelo
    st.markdown("---")
    with st.expander("Adicionar Novo Modelo para Benchmark", expanded=True if len(st.session_state.benchmark_models) < 2 else False):
        with st.form("add_model_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                model_name = st.text_input("Nome do Modelo", value="Modelo " + str(len(st.session_state.benchmark_models) + 1))
                model_type = st.selectbox(
                    "Tipo de Modelo",
                    options=["Token de Utilidade", "Token de Governança"]
                )
                
                total_supply = st.number_input(
                    "Supply Total",
                    min_value=1000,
                    max_value=10000000000,
                    value=100000000,
                    format="%d"
                )
                
                vesting_periods = st.multiselect(
                    "Períodos de Vesting",
                    options=["Equipe", "Investidores", "Comunidade", "Fundação", "Ecosistema", "Reserva"],
                    default=["Equipe", "Investidores"]
                )
            
            with col2:
                # Parâmetros específicos do tipo de modelo
                if model_type == "Token de Utilidade":
                    initial_users = st.number_input(
                        "Usuários Iniciais",
                        min_value=10,
                        max_value=1000000,
                        value=1000
                    )
                    
                    user_growth_rate = st.slider(
                        "Taxa de Crescimento Mensal de Usuários",
                        min_value=0.01,
                        max_value=0.2,
                        value=0.05,
                        format="%.2f"
                    )
                    
                    token_utility = st.slider(
                        "Utilidade do Token",
                        min_value=1,
                        max_value=10,
                        value=5,
                        help="Quão útil o token é no ecossistema (1=baixa, 10=alta)"
                    )
                    
                    usage_frequency = st.slider(
                        "Frequência de Uso",
                        min_value=1,
                        max_value=10,
                        value=5,
                        help="Com que frequência os usuários usam o token (1=raramente, 10=constantemente)"
                    )
                    
                elif model_type == "Token de Governança":
                    initial_staking_rate = st.slider(
                        "Taxa Inicial de Staking",
                        min_value=0.05,
                        max_value=0.5,
                        value=0.2,
                        format="%.2f",
                        help="Percentual de tokens que estarão em staking inicialmente"
                    )
                    
                    staking_apy = st.slider(
                        "APY do Staking",
                        min_value=0.05,
                        max_value=0.5,
                        value=0.12,
                        format="%.2f",
                        help="Rendimento anual para quem faz staking"
                    )
                    
                    governance_power = st.slider(
                        "Poder de Governança",
                        min_value=1,
                        max_value=10,
                        value=5,
                        help="Impacto das decisões de governança (1=baixo, 10=alto)"
                    )
                    
                    staking_lock = st.slider(
                        "Período de Lock no Staking (meses)",
                        min_value=1,
                        max_value=12,
                        value=3
                    )
                
                # Distribuição simples do token (para ambos os tipos)
                distribution_options = {
                    "Equipe": (0.0, 0.3),
                    "Investidores": (0.0, 0.3),
                    "Comunidade": (0.0, 0.5),
                    "Fundação": (0.0, 0.2),
                    "Ecosistema": (0.0, 0.3),
                    "Reserva": (0.0, 0.2)
                }
                
                distribution = {}
                for category in distribution_options:
                    min_val, max_val = distribution_options[category]
                    distribution[category] = st.slider(
                        f"Distribuição - {category}",
                        min_value=min_val,
                        max_value=max_val,
                        value=(min_val + max_val) / 2,
                        format="%.2f"
                    )
            
            # Botão para adicionar o modelo
            submit_button = st.form_submit_button("Adicionar Modelo ao Benchmark")
            
            if submit_button:
                # Verificar se a distribuição soma 1
                total_distribution = sum(distribution.values())
                if abs(total_distribution - 1.0) > 0.01:
                    st.error(f"A distribuição deve somar 1.0 (atual: {total_distribution:.2f})")
                else:
                    # Criar ID único para o modelo
                    model_id = f"model_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    
                    # Criar o modelo conforme o tipo
                    if model_type == "Token de Utilidade":
                        model = UtilityTokenModel(
                            name=model_name,
                            total_supply=total_supply,
                            initial_users=initial_users,
                            user_growth_rate=user_growth_rate
                        )
                        # Adicionar atributos específicos para benchmark
                        model.token_utility = token_utility
                        model.usage_frequency = usage_frequency
                        
                    else:  # Token de Governança
                        model = GovernanceTokenModel(
                            name=model_name,
                            total_supply=total_supply,
                            initial_staking_rate=initial_staking_rate,
                            staking_apy=staking_apy
                        )
                        # Adicionar atributos específicos para benchmark
                        model.governance_power = governance_power
                        model.staking_lock = staking_lock
                    
                    # Configurar a distribuição e vesting
                    model.set_distribution(distribution)
                    
                    # Configurar vesting simples para as categorias selecionadas
                    for category in vesting_periods:
                        if category == "Equipe":
                            # Equipe geralmente tem vesting mais longo
                            model.set_vesting_schedule(category, [(0, 0.1), (6, 0.2), (12, 0.3), (18, 0.2), (24, 0.2)])
                        elif category == "Investidores":
                            # Investidores têm um período de lock seguido por liberação
                            model.set_vesting_schedule(category, [(0, 0.0), (3, 0.2), (6, 0.2), (9, 0.3), (12, 0.3)])
                        elif category == "Comunidade":
                            # Comunidade geralmente tem liberação mais rápida
                            model.set_vesting_schedule(category, [(0, 0.3), (3, 0.3), (6, 0.4)])
                        elif category == "Fundação":
                            # Fundação com liberação gradual
                            model.set_vesting_schedule(category, [(0, 0.1), (6, 0.2), (12, 0.2), (18, 0.2), (24, 0.3)])
                        elif category == "Ecosistema":
                            # Incentivos do ecossistema liberados gradualmente
                            model.set_vesting_schedule(category, [(0, 0.2), (4, 0.2), (8, 0.2), (12, 0.2), (16, 0.2)])
                        elif category == "Reserva":
                            # Reserva técnica com liberação muito lenta
                            model.set_vesting_schedule(category, [(0, 0.0), (12, 0.2), (24, 0.3), (36, 0.5)])
                    
                    # Armazenar o modelo na sessão
                    st.session_state.benchmark_models[model_id] = {
                        "id": model_id,
                        "name": model_name,
                        "type": model_type,
                        "model": model,
                        "color": f"#{random.randint(0, 0xFFFFFF):06x}"  # Cor aleatória para gráficos
                    }
                    st.success(f"Modelo '{model_name}' adicionado com sucesso!")
                    st.rerun()
    
    # Exibir modelos adicionados
    if st.session_state.benchmark_models:
        st.markdown("### Modelos para Benchmark")
        
        models_cols = st.columns(min(len(st.session_state.benchmark_models), 3))
        
        for i, (model_id, model_info) in enumerate(st.session_state.benchmark_models.items()):
            col_idx = i % len(models_cols)
            
            with models_cols[col_idx]:
                st.markdown(f"#### {model_info['name']}")
                st.markdown(f"**Tipo:** {model_info['type']}")
                
                if model_info['type'] == "Token de Utilidade":
                    model = model_info['model']
                    st.markdown(f"**Supply Total:** {model.total_supply:,}")
                    st.markdown(f"**Usuários Iniciais:** {model.initial_users:,}")
                    st.markdown(f"**Crescimento Mensal:** {model.user_growth_rate:.1%}")
                    
                    # Criar gráfico simples de distribuição
                    fig = px.pie(
                        values=list(model.distribution.values()),
                        names=list(model.distribution.keys()),
                        title=f"Distribuição - {model_info['name']}",
                        color_discrete_sequence=px.colors.qualitative.Pastel,
                        hole=0.4
                    )
                    fig.update_layout(height=250, margin=dict(l=20, r=20, t=30, b=20))
                    st.plotly_chart(fig, use_container_width=True)
                    
                else:  # Token de Governança
                    model = model_info['model']
                    st.markdown(f"**Supply Total:** {model.total_supply:,}")
                    st.markdown(f"**Taxa Inicial de Staking:** {model.initial_staking_rate:.1%}")
                    st.markdown(f"**APY do Staking:** {model.staking_apy:.1%}")
                    
                    # Criar gráfico simples de distribuição
                    fig = px.pie(
                        values=list(model.distribution.values()),
                        names=list(model.distribution.keys()),
                        title=f"Distribuição - {model_info['name']}",
                        color_discrete_sequence=px.colors.qualitative.Pastel,
                        hole=0.4
                    )
                    fig.update_layout(height=250, margin=dict(l=20, r=20, t=30, b=20))
                    st.plotly_chart(fig, use_container_width=True)
                
                # Botão para remover o modelo
                if st.button(f"Remover Modelo", key=f"remove_{model_id}"):
                    del st.session_state.benchmark_models[model_id]
                    if model_id in st.session_state.benchmark_results:
                        del st.session_state.benchmark_results[model_id]
                    st.rerun()

# Tab de Análise Comparativa
with tab2:
    if not st.session_state.benchmark_models:
        st.info("Adicione pelo menos dois modelos de tokenomics na aba 'Configuração de Modelos' para iniciar o benchmark.")
    elif not st.session_state.benchmark_results:
        st.info("Clique em 'Iniciar Benchmark' na aba 'Configuração de Modelos' para começar a simulação.")
    else:
        # Mostrar progresso da simulação
        if st.session_state.benchmark_running:
            progress = st.session_state.current_month / st.session_state.simulation_months
            st.progress(progress)
            st.markdown(f"**Simulando:** Mês {st.session_state.current_month} de {st.session_state.simulation_months}")
        
        # Métricas comparativas
        st.subheader("Métricas Comparativas")
        metric_cols = st.columns(len(st.session_state.benchmark_models))
        
        for i, (model_id, model_info) in enumerate(st.session_state.benchmark_models.items()):
            if model_id in st.session_state.benchmark_results:
                with metric_cols[i]:
                    result_data = st.session_state.benchmark_results[model_id]['data']
                    
                    if not result_data.empty:
                        last_row = result_data.iloc[-1]
                        
                        # Calcular ROI desde o início
                        roi = (last_row['Price'] / 1.0 - 1) * 100  # 1.0 é o preço inicial
                        
                        st.markdown(f"### {model_info['name']}")
                        
                        # Preço atual
                        st.metric(
                            "Preço Atual",
                            f"${last_row['Price']:.2f}",
                            delta=f"{roi:.1f}% ROI" if roi != 0 else None,
                            delta_color="normal"
                        )
                        
                        # Circulating Supply
                        supply_pct = last_row['Circulating_Supply'] / model_info['model'].total_supply * 100
                        st.metric(
                            "Supply Circulante",
                            f"{int(last_row['Circulating_Supply']):,}",
                            delta=f"{supply_pct:.1f}% do total"
                        )
                        
                        # Market Cap
                        st.metric(
                            "Market Cap",
                            f"${int(last_row['Market_Cap']):,}"
                        )
                        
                        # Adoção/Utilização
                        st.metric(
                            "Adoção",
                            f"{last_row['Adoption']:.1f}/10"
                        )
        
        # Gráficos comparativos
        st.subheader("Comparação de Desempenho ao Longo do Tempo")
        
        comparison_options = [
            "Preço",
            "Circulating Supply",
            "Market Cap",
            "Adoção",
            "ROI"
        ]
        
        metrics_to_show = st.multiselect(
            "Selecione as métricas para comparar",
            options=comparison_options,
            default=["Preço", "ROI"]
        )
        
        chart_cols = []
        charts_per_row = min(len(metrics_to_show), 2)
        
        if metrics_to_show:
            # Criar uma linha para cada conjunto de gráficos (até 2 por linha)
            for i in range(0, len(metrics_to_show), charts_per_row):
                chart_cols.append(st.columns(charts_per_row))
            
            for i, metric in enumerate(metrics_to_show):
                row = i // charts_per_row
                col = i % charts_per_row
                
                with chart_cols[row][col]:
                    # Mapear nome da métrica para nome da coluna no DataFrame
                    column_map = {
                        "Preço": "Price",
                        "Circulating Supply": "Circulating_Supply",
                        "Market Cap": "Market_Cap",
                        "Adoção": "Adoption",
                        "ROI": "ROI"
                    }
                    
                    column = column_map[metric]
                    
                    # Criar gráfico comparativo
                    fig = go.Figure()
                    
                    for model_id, model_info in st.session_state.benchmark_models.items():
                        if model_id in st.session_state.benchmark_results:
                            df = st.session_state.benchmark_results[model_id]['data']
                            
                            if not df.empty:
                                fig.add_trace(
                                    go.Scatter(
                                        x=df['Month'],
                                        y=df[column],
                                        mode='lines',
                                        name=model_info['name'],
                                        line=dict(color=model_info['color'], width=2)
                                    )
                                )
                    
                    fig.update_layout(
                        title=f"Comparação de {metric}",
                        xaxis_title="Mês",
                        yaxis_title=metric,
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                        height=400,
                        margin=dict(l=40, r=40, t=60, b=40)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
        
        # Tabela de comparação de eventos
        st.subheader("Eventos Importantes")
        
        all_events = []
        for model_id, model_info in st.session_state.benchmark_models.items():
            if model_id in st.session_state.benchmark_results:
                for event in st.session_state.benchmark_results[model_id]['events']:
                    all_events.append({
                        "Modelo": model_info['name'],
                        "Mês": event['month'],
                        "Evento": event['name'],
                        "Descrição": event['description'],
                        "Impacto no Preço": f"{event['price_impact']*100:+.1f}%"
                    })
        
        if all_events:
            all_events_df = pd.DataFrame(all_events)
            all_events_df = all_events_df.sort_values("Mês")
            st.dataframe(all_events_df, use_container_width=True)
        else:
            st.info("Nenhum evento importante registrado ainda.")
        
        # Análise de sensibilidade (só aparece quando a simulação estiver completa)
        if not st.session_state.benchmark_running and st.session_state.current_month >= st.session_state.simulation_months:
            st.subheader("Análise de Sensibilidade")
            st.markdown("""
                A análise de sensibilidade mostra como cada modelo responde a diferentes condições de mercado.
                Isso ajuda a entender qual estratégia de tokenomics é mais resiliente a mudanças externas.
            """)
            
            # Criar gráficos de análise de sensibilidade
            sensitivity_fig = go.Figure()
            
            # Criar dados para análise de sensibilidade (simulação simples)
            market_conditions = ["Muito Negativas", "Negativas", "Neutras", "Positivas", "Muito Positivas"]
            
            for model_id, model_info in st.session_state.benchmark_models.items():
                if model_id in st.session_state.benchmark_results:
                    last_price = st.session_state.benchmark_results[model_id]['data'].iloc[-1]['Price']
                    
                    # Simular o preço final sob diferentes condições
                    sensitivity_prices = []
                    for condition in market_conditions:
                        # Fator de ajuste simples baseado nas condições
                        if condition == "Muito Negativas":
                            adj_factor = 0.7  # 30% abaixo
                        elif condition == "Negativas":
                            adj_factor = 0.85  # 15% abaixo
                        elif condition == "Neutras":
                            adj_factor = 1.0  # Sem alteração
                        elif condition == "Positivas":
                            adj_factor = 1.15  # 15% acima
                        else:  # Muito Positivas
                            adj_factor = 1.3  # 30% acima
                        
                        # Ajustar baseado também no tipo de modelo (alguns são mais resilientes)
                        if model_info['type'] == "Token de Governança":
                            # Governança é mais estável em condições negativas
                            if condition in ["Muito Negativas", "Negativas"]:
                                adj_factor = adj_factor * 1.1  # 10% mais resiliente
                        
                        sensitivity_prices.append(last_price * adj_factor)
                    
                    sensitivity_fig.add_trace(
                        go.Bar(
                            x=market_conditions,
                            y=sensitivity_prices,
                            name=model_info['name'],
                            marker_color=model_info['color']
                        )
                    )
            
            sensitivity_fig.update_layout(
                title="Análise de Sensibilidade - Preço Final sob Diferentes Condições",
                xaxis_title="Condições de Mercado",
                yaxis_title="Preço Final Estimado ($)",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                height=500,
                barmode='group'
            )
            
            st.plotly_chart(sensitivity_fig, use_container_width=True)

# Função para calcular as métricas de um modelo para um determinado mês
def simulate_month(model_info, current_month, market_bias, volatility, current_data=None):
    model = model_info['model']
    model_type = model_info['type']
    
    # Se for o primeiro mês, inicializar dados
    if current_data is None or current_data.empty:
        return pd.DataFrame({
            'Month': [0],
            'Price': [1.0],  # Todos modelos começam com o mesmo preço para comparação justa
            'Circulating_Supply': [model.calculate_released_tokens(0).get('total', 0)],
            'Market_Cap': [1.0 * model.calculate_released_tokens(0).get('total', 0)],
            'Adoption': [1.0],  # Nível de adoção/utilização (1-10)
            'ROI': [0.0]  # Retorno sobre investimento (%)
        })
    
    # Obter última linha de dados
    last_row = current_data.iloc[-1].copy()
    
    # Calcular supply circulante baseado no cronograma de vesting
    released_tokens = model.calculate_released_tokens(current_month)
    new_circulating_supply = released_tokens.get('total', 0)
    
    # Calcular demanda de tokens (depende do tipo de modelo)
    if model_type == "Token de Utilidade":
        # Para tokens de utilidade, a demanda é baseada no número de usuários e uso
        current_users = model.initial_users * (1 + model.user_growth_rate) ** current_month
        token_utility_factor = getattr(model, 'token_utility', 5) / 10  # 0.1 a 1.0
        usage_frequency_factor = getattr(model, 'usage_frequency', 5) / 10  # 0.1 a 1.0
        
        # Demanda baseada em usuários, utilidade e frequência
        demand_growth = (0.01 + 0.02 * token_utility_factor + 0.02 * usage_frequency_factor)
        
        # Adicionar aleatoriedade e fatores de mercado
        demand_change = np.random.normal(demand_growth + market_bias, volatility)
        
    else:  # Token de Governança
        # Para tokens de governança, a demanda é baseada em staking e governança
        staking_growth = 0.01  # Crescimento mensal na taxa de staking
        governance_power_factor = getattr(model, 'governance_power', 5) / 10  # 0.1 a 1.0
        staking_lock_factor = min(getattr(model, 'staking_lock', 3) / 12, 1.0)  # 0.08 a 1.0
        
        # Staking mais longo e poder de governança aumentam a demanda
        demand_growth = (0.005 + 0.015 * governance_power_factor + 0.01 * staking_lock_factor)
        
        # Adicionar aleatoriedade e fatores de mercado
        demand_change = np.random.normal(demand_growth + market_bias, volatility * 0.8)  # Governança é menos volátil
    
    # Calcular novo preço baseado na oferta e demanda
    # Se a oferta circulante aumentou muito rapidamente, isso pressiona o preço para baixo
    supply_change = (new_circulating_supply - last_row['Circulating_Supply']) / max(1, last_row['Circulating_Supply'])
    supply_pressure = -0.2 * supply_change if supply_change > 0 else 0
    
    # Fator final de mudança de preço combinando demanda e pressão de oferta
    price_change = demand_change + supply_pressure
    
    # Calcular novo preço
    new_price = max(0.01, last_row['Price'] * (1 + price_change))
    
    # Calcular novo market cap
    new_market_cap = new_price * new_circulating_supply
    
    # Calcular nível de adoção (1-10)
    if model_type == "Token de Utilidade":
        # Adoção cresce com usuários e utilidade
        adoption_base = min(10, last_row['Adoption'] * (1 + 0.05 * token_utility_factor))
        new_adoption = min(10, adoption_base + 0.1 * token_utility_factor)
    else:
        # Adoção cresce com governança e participação
        staking_rate = model.initial_staking_rate + staking_growth * current_month
        governance_factor = governance_power_factor * staking_rate
        adoption_base = min(10, last_row['Adoption'] * (1 + 0.03 * governance_factor))
        new_adoption = min(10, adoption_base + 0.05 * governance_factor)
    
    # Adicionar aleatoriedade à adoção
    new_adoption = max(1, min(10, new_adoption + np.random.normal(0, 0.1)))
    
    # Calcular ROI
    new_roi = (new_price / 1.0 - 1) * 100  # 1.0 é o preço inicial
    
    # Criar nova linha de dados
    new_row = {
        'Month': current_month,
        'Price': new_price,
        'Circulating_Supply': new_circulating_supply,
        'Market_Cap': new_market_cap,
        'Adoption': new_adoption,
        'ROI': new_roi
    }
    
    # Retornar dataframe atualizado
    return pd.concat([current_data, pd.DataFrame([new_row])], ignore_index=True)

# Gerar um evento aleatório para o modelo
def generate_random_event(model_info, current_month):
    model_type = model_info['type']
    
    # Probabilidade de evento baseada no mês (mais provável no início)
    event_probability = 0.15 if current_month < 6 else 0.08
    
    if random.random() > event_probability:
        return None
    
    # Eventos comuns a todos os tipos de token
    common_events = [
        {
            'name': 'Listagem em Exchange',
            'description': 'O token foi listado em uma nova exchange importante.',
            'price_impact': random.uniform(0.05, 0.15)
        },
        {
            'name': 'Parceria Estratégica',
            'description': 'Uma parceria estratégica foi anunciada.',
            'price_impact': random.uniform(0.03, 0.1)
        },
        {
            'name': 'Condições Macroeconômicas',
            'description': 'Mudanças nas condições macroeconômicas afetaram o mercado.',
            'price_impact': random.uniform(-0.1, 0.1)
        }
    ]
    
    # Eventos específicos por tipo
    if model_type == "Token de Utilidade":
        specific_events = [
            {
                'name': 'Novo Caso de Uso',
                'description': 'Um novo caso de uso para o token foi implementado.',
                'price_impact': random.uniform(0.04, 0.12)
            },
            {
                'name': 'Aumento na Base de Usuários',
                'description': 'A base de usuários cresceu significativamente.',
                'price_impact': random.uniform(0.05, 0.15)
            },
            {
                'name': 'Problema Técnico',
                'description': 'Um problema técnico afetou temporariamente a utilidade do token.',
                'price_impact': random.uniform(-0.15, -0.05)
            }
        ]
    else:  # Token de Governança
        specific_events = [
            {
                'name': 'Proposta de Governança Importante',
                'description': 'Uma proposta importante foi aprovada pela governança.',
                'price_impact': random.uniform(0.03, 0.1)
            },
            {
                'name': 'Aumento no APY de Staking',
                'description': 'O rendimento de staking foi aumentado.',
                'price_impact': random.uniform(0.05, 0.12)
            },
            {
                'name': 'Redução no Período de Lock',
                'description': 'O período de lock do staking foi reduzido.',
                'price_impact': random.uniform(-0.08, -0.02)
            }
        ]
    
    # Combinar eventos e escolher aleatoriamente
    all_events = common_events + specific_events
    event = random.choice(all_events)
    
    # Adicionar mês do evento
    event['month'] = current_month
    
    return event

# Atualização do benchmark
if st.session_state.benchmark_running:
    current_time = datetime.now()
    time_diff = (current_time - st.session_state.last_update_time).total_seconds()
    
    # Ajustar velocidade de atualização
    update_interval = 0.5 / st.session_state.speed_multiplier
    
    if time_diff >= update_interval:
        # Atualizar a simulação
        if st.session_state.current_month < st.session_state.simulation_months:
            # Simular cada modelo para o mês atual
            for model_id, model_info in st.session_state.benchmark_models.items():
                # Obter dados atuais
                current_data = st.session_state.benchmark_results[model_id]['data'] if model_id in st.session_state.benchmark_results else None
                
                # Simular mês atual
                new_data = simulate_month(
                    model_info=model_info,
                    current_month=st.session_state.current_month + 1,
                    market_bias=market_bias,
                    volatility=volatility,
                    current_data=current_data
                )
                
                # Verificar se ocorre um evento
                new_event = generate_random_event(model_info, st.session_state.current_month + 1)
                if new_event:
                    st.session_state.benchmark_results[model_id]['events'].append(new_event)
                    
                    # Aplicar impacto do evento no preço
                    latest_price = new_data.iloc[-1]['Price']
                    new_data.iloc[-1, new_data.columns.get_loc('Price')] = latest_price * (1 + new_event['price_impact'])
                    
                    # Recalcular market cap e ROI
                    latest_supply = new_data.iloc[-1]['Circulating_Supply']
                    latest_price = new_data.iloc[-1]['Price']  # Novo preço após o evento
                    new_data.iloc[-1, new_data.columns.get_loc('Market_Cap')] = latest_price * latest_supply
                    new_data.iloc[-1, new_data.columns.get_loc('ROI')] = (latest_price / 1.0 - 1) * 100
                
                # Atualizar dados na sessão
                st.session_state.benchmark_results[model_id]['data'] = new_data
            
            # Incrementar mês atual
            st.session_state.current_month += 1
            st.session_state.last_update_time = current_time
            
        else:
            # Simulação concluída
            st.session_state.benchmark_running = False
            st.success("Benchmark concluído!")