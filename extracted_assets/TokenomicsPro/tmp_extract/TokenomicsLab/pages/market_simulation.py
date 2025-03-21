import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
import random
from datetime import datetime, timedelta
import math

st.set_page_config(
    page_title="Simulação de Mercado | Tokenomics Lab",
    page_icon="📈",
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

# Inicializar estados da sessão para a simulação
if 'simulation_running' not in st.session_state:
    st.session_state.simulation_running = False
if 'simulation_day' not in st.session_state:
    st.session_state.simulation_day = 1
if 'simulation_data' not in st.session_state:
    st.session_state.simulation_data = None
if 'events' not in st.session_state:
    st.session_state.events = []
if 'speed_multiplier' not in st.session_state:
    st.session_state.speed_multiplier = 1
if 'last_update_time' not in st.session_state:
    st.session_state.last_update_time = datetime.now()
if 'sentiment' not in st.session_state:
    st.session_state.sentiment = 0.5  # Sentimento de mercado (0 = muito negativo, 1 = muito positivo)
if 'initial_price' not in st.session_state:
    st.session_state.initial_price = 5.0
if 'initial_holders' not in st.session_state:
    st.session_state.initial_holders = 10000

# Título e introdução
st.title("Simulação de Mercado")
st.markdown("""
    Esta simulação mostra como seu token pode se comportar no mercado ao longo de 30 dias, com base em diferentes fatores
    e na volatilidade do mercado. Eventos aleatórios podem ocorrer, afetando tanto o preço quanto o número de holders.
""")

# Layout principal
col_params, col_chart = st.columns([1, 3])

with col_params:
    st.subheader("Configurações da Simulação")
    
    initial_price = st.number_input(
        "Preço Inicial ($)",
        min_value=0.01,
        max_value=1000.0,
        value=st.session_state.initial_price,
        step=0.1
    )
    st.session_state.initial_price = initial_price
    
    initial_holders = st.number_input(
        "Holders Iniciais",
        min_value=100,
        max_value=100000,
        value=st.session_state.initial_holders,
        step=100
    )
    st.session_state.initial_holders = initial_holders
    
    market_volatility = st.slider(
        "Volatilidade do Mercado",
        min_value=1,
        max_value=10,
        value=5,
        help="Quanto maior a volatilidade, mais imprevisível será o comportamento do preço"
    )
    
    market_sentiment = st.slider(
        "Sentimento do Mercado",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.sentiment,
        step=0.1,
        format="%.1f",
        help="0 = Extremamente negativo, 1 = Extremamente positivo"
    )
    st.session_state.sentiment = market_sentiment
    
    event_frequency = st.slider(
        "Frequência de Eventos",
        min_value=1,
        max_value=10,
        value=5,
        help="Quanto maior, mais eventos aleatórios ocorrerão"
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
    
    # Botões para controlar a simulação
    col_start, col_reset = st.columns(2)
    
    with col_start:
        start_button = st.button(
            "Iniciar Simulação" if not st.session_state.simulation_running else "Pausar Simulação",
            use_container_width=True
        )
        if start_button:
            if not st.session_state.simulation_running:
                # Verificar se tem créditos suficientes
                if spend_credits("Simulação de Mercado", 3):
                    st.session_state.simulation_running = True
                    if st.session_state.simulation_data is None:
                        st.session_state.simulation_data = initialize_simulation(initial_price, initial_holders)
                    st.session_state.last_update_time = datetime.now()
                    st.rerun()
            else:
                st.session_state.simulation_running = False
    
    with col_reset:
        if st.button("Reiniciar Simulação", use_container_width=True):
            st.session_state.simulation_running = False
            st.session_state.simulation_day = 1
            st.session_state.simulation_data = None
            st.session_state.events = []
            st.rerun()

    # Exibir métricas atuais (se a simulação estiver rodando)
    if st.session_state.simulation_data is not None and len(st.session_state.simulation_data) > 0:
        st.subheader("Métricas Atuais")
        
        last_row = st.session_state.simulation_data.iloc[-1]
        
        metric_cols1, metric_cols2 = st.columns(2)
        with metric_cols1:
            st.metric(
                "Dia",
                f"{int(last_row['Day'])} de 30"
            )
            
            price_delta = None
            if len(st.session_state.simulation_data) > 1:
                prev_price = st.session_state.simulation_data.iloc[-2]['Price']
                price_delta = f"{(last_row['Price'] - prev_price) / prev_price * 100:.2f}%"
            
            st.metric(
                "Preço",
                f"${last_row['Price']:.2f}",
                delta=price_delta
            )
            
            st.metric(
                "Holders",
                f"{last_row['Holders']:.0f}"
            )
        
        with metric_cols2:
            st.metric(
                "Volume 24h",
                f"${last_row['Volume']/1000:.1f}K"
            )
            
            st.metric(
                "Market Cap",
                f"${last_row['Market_Cap']/1000000:.1f}M"
            )
            
            sentiment_text = "Neutro"
            if 'Sentiment' in last_row:
                if last_row['Sentiment'] > 0.7:
                    sentiment_text = "Muito Positivo"
                elif last_row['Sentiment'] > 0.55:
                    sentiment_text = "Positivo"
                elif last_row['Sentiment'] < 0.3:
                    sentiment_text = "Muito Negativo"
                elif last_row['Sentiment'] < 0.45:
                    sentiment_text = "Negativo"
            
            st.metric(
                "Sentimento",
                sentiment_text
            )

# Função para inicializar a simulação
def initialize_simulation(initial_price=5.0, initial_holders=10000):
    # Parâmetros iniciais
    price = initial_price
    holders = initial_holders
    volume = price * holders * 0.5 * random.uniform(0.8, 1.2)  # Volume inicial aleatório
    market_cap = price * holders * 100  # Supply implícito de 100 tokens por holder
    
    # Criar dataframe inicial
    data = {
        'Day': [0],
        'Price': [price],
        'Holders': [holders],
        'Volume': [volume],
        'Market_Cap': [market_cap],
        'Price_Change': [0.0],
        'Sentiment': [st.session_state.sentiment]
    }
    
    return pd.DataFrame(data)

# Função para atualizar a simulação
def update_simulation(df, volatility, sentiment, event_frequency, day):
    last_row = df.iloc[-1].copy()
    
    # Calcular novas métricas
    volatility_factor = volatility / 10.0  # 0.1 a 1.0
    sentiment_bias = (sentiment - 0.5) * 0.02  # -0.01 a 0.01 (bias diário)
    
    # Verificar se há eventos ativos que afetam o sentimento
    event_sentiment_effect = 0
    price_event_effect = 0
    holder_event_effect = 0
    
    for event in st.session_state.events:
        if event['active']:
            event_sentiment_effect += event['sentiment_effect']
            price_event_effect += event['price_effect']
            holder_event_effect += event['holder_effect']
    
    # Atualizar sentimento com base em eventos e alguma aleatoriedade
    new_sentiment = min(1.0, max(0.0, last_row['Sentiment'] + 
                                event_sentiment_effect + 
                                random.uniform(-0.05, 0.05) * volatility_factor))
    
    # Gerar movimento de preço (random walk com viés baseado no sentimento)
    sentiment_price_bias = (new_sentiment - 0.5) * 0.04  # -0.02 a 0.02 (efeito diário)
    price_change_pct = np.random.normal(sentiment_price_bias, 0.02 * volatility_factor) + price_event_effect
    
    # Calcular novo preço
    new_price = max(0.01, last_row['Price'] * (1 + price_change_pct))
    
    # Calcular novos holders (com correlação com sentimento e preço)
    sentiment_holder_effect = (new_sentiment - 0.5) * 0.03  # -0.015 a 0.015
    price_momentum = 0
    if len(df) > 5:
        recent_prices = df.tail(5)['Price'].values
        price_momentum = (recent_prices[-1] / recent_prices[0] - 1) * 0.02  # Efeito de momentum
    
    holder_change_pct = np.random.normal(sentiment_holder_effect + price_momentum, 0.01 * volatility_factor) + holder_event_effect
    
    new_holders = max(100, last_row['Holders'] * (1 + holder_change_pct))
    
    # Volume correlacionado com volatilidade, preço e mudança no número de holders
    volume_factor = abs(price_change_pct) * 5 + abs(holder_change_pct) * 3
    new_volume = new_price * new_holders * 0.2 * (0.8 + volume_factor + random.uniform(0, 0.5) * volatility_factor)
    
    # Market cap
    new_market_cap = new_price * new_holders * 100  # Assumindo 100 tokens por holder
    
    # Criar nova linha
    new_row = {
        'Day': day,
        'Price': new_price,
        'Holders': new_holders,
        'Volume': new_volume,
        'Market_Cap': new_market_cap,
        'Price_Change': price_change_pct * 100,
        'Sentiment': new_sentiment
    }
    
    # Atualizar dataframe
    return pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

# Função para gerar eventos aleatórios
def generate_random_event(event_frequency):
    # Probabilidade de evento baseada na frequência (5% a 15% por dia)
    event_probability = 0.05 + (event_frequency / 100)
    
    if random.random() > event_probability:
        return None
    
    events = [
        {
            'name': 'Listagem em Exchange Tier 1',
            'description': 'O token foi listado em uma grande exchange!',
            'price_effect': random.uniform(0.03, 0.1),
            'holder_effect': random.uniform(0.02, 0.05),
            'sentiment_effect': random.uniform(0.05, 0.15),
            'duration': random.randint(2, 4)
        },
        {
            'name': 'Parceria Estratégica Anunciada',
            'description': 'Uma parceria importante foi anunciada, gerando entusiasmo no mercado.',
            'price_effect': random.uniform(0.02, 0.07),
            'holder_effect': random.uniform(0.01, 0.03),
            'sentiment_effect': random.uniform(0.03, 0.1),
            'duration': random.randint(1, 3)
        },
        {
            'name': 'Problema de Segurança',
            'description': 'Um possível exploit foi identificado no contrato do token.',
            'price_effect': random.uniform(-0.15, -0.05),
            'holder_effect': random.uniform(-0.08, -0.03),
            'sentiment_effect': random.uniform(-0.2, -0.1),
            'duration': random.randint(2, 5)
        },
        {
            'name': 'Grande Venda de Whale',
            'description': 'Um grande detentor vendeu uma quantidade significativa de tokens.',
            'price_effect': random.uniform(-0.12, -0.03),
            'holder_effect': random.uniform(-0.02, 0),
            'sentiment_effect': random.uniform(-0.1, -0.02),
            'duration': random.randint(1, 2)
        },
        {
            'name': 'Menção por Influenciador',
            'description': 'Um influenciador com grande audiência mencionou positivamente o projeto.',
            'price_effect': random.uniform(0.05, 0.15),
            'holder_effect': random.uniform(0.02, 0.07),
            'sentiment_effect': random.uniform(0.05, 0.15),
            'duration': random.randint(1, 3)
        },
        {
            'name': 'Atualização do Projeto',
            'description': 'Uma atualização importante do projeto foi lançada com novos recursos.',
            'price_effect': random.uniform(0.01, 0.05),
            'holder_effect': random.uniform(0.01, 0.03),
            'sentiment_effect': random.uniform(0.02, 0.08),
            'duration': random.randint(2, 5)
        },
        {
            'name': 'Mercado em Queda Geral',
            'description': 'Todo o mercado de criptomoedas está enfrentando uma correção.',
            'price_effect': random.uniform(-0.08, -0.02),
            'holder_effect': random.uniform(-0.04, -0.01),
            'sentiment_effect': random.uniform(-0.15, -0.05),
            'duration': random.randint(3, 7)
        },
        {
            'name': 'Mercado em Alta Geral',
            'description': 'Todo o mercado de criptomoedas está em alta.',
            'price_effect': random.uniform(0.02, 0.06),
            'holder_effect': random.uniform(0.01, 0.03),
            'sentiment_effect': random.uniform(0.05, 0.15),
            'duration': random.randint(3, 7)
        },
        {
            'name': 'Notícias Regulatórias Positivas',
            'description': 'Anunciada nova regulamentação favorável para criptomoedas.',
            'price_effect': random.uniform(0.03, 0.08),
            'holder_effect': random.uniform(0.02, 0.05),
            'sentiment_effect': random.uniform(0.05, 0.12),
            'duration': random.randint(3, 6)
        },
        {
            'name': 'Notícias Regulatórias Negativas',
            'description': 'Anunciada nova regulamentação desfavorável para criptomoedas.',
            'price_effect': random.uniform(-0.1, -0.03),
            'holder_effect': random.uniform(-0.05, -0.02),
            'sentiment_effect': random.uniform(-0.15, -0.05),
            'duration': random.randint(3, 6)
        }
    ]
    
    # Escolher evento aleatoriamente
    event = random.choice(events)
    event['active'] = True
    event['days_left'] = event['duration']
    event['start_day'] = st.session_state.simulation_day
    
    return event

# Área de exibição do gráfico (na coluna principal)
with col_chart:
    # Placeholder para o gráfico
    chart_placeholder = st.empty()
    
    # Placeholder para eventos
    events_container = st.container()
    
    with events_container:
        events_title = st.empty()
        events_list = st.empty()

# Atualização da simulação
if st.session_state.simulation_running:
    current_time = datetime.now()
    time_diff = (current_time - st.session_state.last_update_time).total_seconds()
    
    # Ajustar velocidade de atualização
    update_interval = 1.0 / st.session_state.speed_multiplier
    
    if time_diff >= update_interval:
        # Atualizar simulação
        if st.session_state.simulation_day <= 30:  # Fixar em 30 dias como no exemplo de referência
            
            # Gerenciar eventos existentes
            for event in st.session_state.events:
                if event['active']:
                    event['days_left'] -= 1
                    if event['days_left'] <= 0:
                        event['active'] = False
            
            # Verificar se ocorre um novo evento
            new_event = generate_random_event(event_frequency)
            if new_event:
                st.session_state.events.append(new_event)
            
            # Atualizar dados
            if st.session_state.simulation_data is not None:
                st.session_state.simulation_data = update_simulation(
                    st.session_state.simulation_data,
                    market_volatility,
                    market_sentiment,
                    event_frequency,
                    st.session_state.simulation_day
                )
                st.session_state.simulation_day += 1
                st.session_state.last_update_time = current_time
        else:
            # Simulação concluída
            st.session_state.simulation_running = False
            st.success("Simulação de 30 dias concluída!")

# Exibir dados da simulação
if st.session_state.simulation_data is not None:
    df = st.session_state.simulation_data
    
    # Criar gráfico animado
    fig = go.Figure()
    
    # Ajustar range para preço e holders terem escalas adequadas
    price_range = [df['Price'].min() * 0.9, df['Price'].max() * 1.1]
    holder_range = [df['Holders'].min() * 0.9, df['Holders'].max() * 1.1]
    
    # Adicionar linha de preço
    fig.add_trace(
        go.Scatter(
            x=df['Day'],
            y=df['Price'],
            mode='lines+markers',
            name='Preço ($)',
            line=dict(color='#0068c9', width=3),
            marker=dict(size=6, color='#0068c9'),
            yaxis='y'
        )
    )
    
    # Adicionar linha de holders
    fig.add_trace(
        go.Scatter(
            x=df['Day'],
            y=df['Holders'],
            mode='lines+markers',
            name='Holders',
            line=dict(color='#ff9e0a', width=3),
            marker=dict(size=6, color='#ff9e0a'),
            yaxis='y2'
        )
    )
    
    # Adicionar marcadores para eventos
    for event in st.session_state.events:
        if 'start_day' in event:
            event_day = event['start_day']
            if event_day in df['Day'].values:
                event_price = df[df['Day'] == event_day]['Price'].values[0]
                event_color = 'green' if event.get('price_effect', 0) > 0 else 'red'
                event_size = 12 + abs(event.get('price_effect', 0)) * 50
                
                fig.add_trace(
                    go.Scatter(
                        x=[event_day],
                        y=[event_price],
                        mode='markers',
                        marker=dict(
                            size=event_size,
                            symbol='star',
                            color=event_color,
                            line=dict(color='white', width=1)
                        ),
                        name=event['name'],
                        text=event['description'],
                        hoverinfo='text+name',
                        showlegend=False
                    )
                )
    
    # Configurar layout com eixos y duplos
    fig.update_layout(
        title='Simulação de Mercado - 30 Dias',
        xaxis=dict(
            title='Dia',
            gridcolor='lightgray',
            range=[0, 30],  # Fixar em 30 dias
            tickmode='linear',
            dtick=5,  # Mostrar tick a cada 5 dias
        ),
        yaxis=dict(
            title='Preço ($)',
            titlefont=dict(color='#0068c9'),
            tickfont=dict(color='#0068c9'),
            gridcolor='lightgray',
            side='left',
            range=price_range
        ),
        yaxis2=dict(
            title='Holders',
            titlefont=dict(color='#ff9e0a'),
            tickfont=dict(color='#ff9e0a'),
            anchor='x',
            overlaying='y',
            side='right',
            range=holder_range
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        margin=dict(l=60, r=60, t=50, b=50),
        hovermode='x unified',
        height=500,
        plot_bgcolor='rgba(240,240,240,0.3)',
        paper_bgcolor='rgba(0,0,0,0)',
        updatemenus=[dict(
            type="buttons",
            showactive=False,
            y=1.05,
            x=1.15,
            xanchor="right",
            yanchor="top",
            pad=dict(t=0, r=10),
            buttons=[dict(
                label="Animar",
                method="animate",
                args=[None, dict(
                    frame=dict(duration=500, redraw=True),
                    fromcurrent=True,
                    transition=dict(duration=300, easing="quadratic-in-out")
                )]
            )]
        )]
    )
    
    # Exibir gráfico
    chart_placeholder.plotly_chart(fig, use_container_width=True)
    
    # Mostrar eventos ativos
    active_events = [e for e in st.session_state.events if e['active']]
    if active_events:
        events_title.subheader("Eventos Ativos")
        
        event_text = ""
        for event in active_events:
            effect_emoji = "🔺" if event['price_effect'] > 0 else "🔻"
            days_text = f"Dia {event['start_day']} - Resta{' ' if event['days_left'] == 1 else 'm '}{event['days_left']} dia{'' if event['days_left'] == 1 else 's'}"
            event_text += f"**{event['name']}** {effect_emoji} - {days_text}\n\n"
            event_text += f"_{event['description']}_\n\n"
            
            price_effect = event['price_effect'] * 100
            holder_effect = event['holder_effect'] * 100
            
            effect_color_price = "green" if price_effect > 0 else "red"
            effect_color_holder = "green" if holder_effect > 0 else "red"
            
            event_text += f"Efeito no preço: <span style='color:{effect_color_price};'>**{price_effect:.1f}%**</span> | "
            event_text += f"Efeito nos holders: <span style='color:{effect_color_holder};'>**{holder_effect:.1f}%**</span>\n\n"
            event_text += "---\n\n"
        
        events_list.markdown(event_text, unsafe_allow_html=True)

# Exibir informações adicionais na área inferior da tela
st.markdown("---")
col_info1, col_info2 = st.columns(2)

with col_info1:
    st.subheader("Sobre a Simulação")
    st.markdown("""
    Esta simulação mostra como o token poderia se comportar no mercado ao longo de 30 dias, 
    com base no sentimento do mercado, volatilidade e eventos aleatórios.
    
    **Métricas simuladas:**
    - Preço do token e sua evolução diária
    - Número de holders (detentores do token)
    - Volume de negociação
    - Market cap (capitalização de mercado)
    - Sentimento do mercado
    """)

with col_info2:
    st.subheader("Como Usar")
    st.markdown("""
    1. Ajuste os parâmetros de simulação no painel esquerdo
    2. Clique em "Iniciar Simulação" (custa 3 créditos)
    3. Observe a evolução do preço e holders em tempo real
    4. Eventos aleatórios podem ocorrer e afetar o mercado
    5. A simulação vai até o dia 30
    
    **Dica:** Aumente a velocidade da simulação se quiser ver os resultados mais rapidamente
    ou diminua para analisar melhor as mudanças diárias.
    """)