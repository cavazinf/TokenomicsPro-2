import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import time

# Set page configuration
st.set_page_config(
    page_title="Market Simulation - TokenomicsLab",
    page_icon="📊",
    layout="wide",
)

# Initialize language if not set
if 'language' not in st.session_state:
    st.session_state.language = 'English'

# Page title and description based on language
if st.session_state.language == 'English':
    title = "Market & Valuation"
    description = """
    Simulate market behavior, value your token, and analyze market scenarios.
    """
    subtitle = "Exchange tokens, complete tasks and make a name for yourself in the market."
elif st.session_state.language == 'Português':
    title = "Mercado & Avaliação"
    description = """
    Simule o comportamento do mercado, avalie seu token e analise cenários de mercado.
    """
    subtitle = "Troque tokens, complete tarefas e faça seu nome no mercado."
elif st.session_state.language == 'Español':
    title = "Mercado & Valoración"
    description = """
    Simula el comportamiento del mercado, valora tu token y analiza escenarios de mercado.
    """
    subtitle = "Intercambia tokens, completa tareas y hazte un nombre en el mercado."
else:
    title = "Market & Valuation"
    description = """
    Simulate market behavior, value your token, and analyze market scenarios.
    """
    subtitle = "Exchange tokens, complete tasks and make a name for yourself in the market."

st.title(title)
st.markdown(description)
st.markdown(f"**{subtitle}**")

# Define multi-language labels and texts
if st.session_state.language == 'English':
    # Tabs
    simulation_tab = "Market Simulation"
    valuation_tab = "Valuation"
    stress_test_tab = "Market Stress Test"
    research_tab = "Market Research"
    
    # Simulation labels
    player_participation = "Player Participation"
    market_volatility = "Market Volatility"
    simulation_speed = "Simulation Speed"
    day_label = "Day"
    of_label = "of"
    price_label = "Price"
    holders_label = "Holders"
    volume_label = "Volume"
    market_cap_label = "Market Cap"
    start_button = "Start"
    pause_button = "Pause"
    reset_button = "Reset"
    simulation_description = "This simulation shows how the token could behave in the market based on player participation and market volatility. Random events can also occur affecting the price."
    
    # Event messages
    event_large_buy = "A whale has purchased a large amount of tokens!"
    event_large_sell = "A major holder has dumped their tokens!"
    event_positive_news = "Positive news about the project has been released!"
    event_negative_news = "Negative rumors are circulating about the project!"
    event_market_crash = "The crypto market is experiencing a general downturn!"
    event_market_rally = "The entire crypto market is rallying!"
    event_partnership = "A new strategic partnership has been announced!"
    event_technical_issue = "A technical issue has been discovered in the project!"
    
elif st.session_state.language == 'Português':
    # Tabs
    simulation_tab = "Simulação de Mercado"
    valuation_tab = "Avaliação"
    stress_test_tab = "Teste de Estresse de Mercado"
    research_tab = "Pesquisa de Mercado"
    
    # Simulation labels
    player_participation = "Participação do Jogador"
    market_volatility = "Volatilidade do Mercado"
    simulation_speed = "Velocidade da Simulação"
    day_label = "Dia"
    of_label = "de"
    price_label = "Preço"
    holders_label = "Holders"
    volume_label = "Volume"
    market_cap_label = "Market Cap"
    start_button = "Iniciar"
    pause_button = "Pausar"
    reset_button = "Reiniciar"
    simulation_description = "Esta simulação mostra como o token pode se comportar no mercado com base na participação do jogador e na volatilidade do mercado. Eventos aleatórios também podem ocorrer afetando o preço."
    
    # Event messages
    event_large_buy = "Uma baleia comprou uma grande quantidade de tokens!"
    event_large_sell = "Um grande detentor despejou seus tokens!"
    event_positive_news = "Notícias positivas sobre o projeto foram divulgadas!"
    event_negative_news = "Rumores negativos estão circulando sobre o projeto!"
    event_market_crash = "O mercado de criptomoedas está experimentando uma queda geral!"
    event_market_rally = "Todo o mercado de criptomoedas está em alta!"
    event_partnership = "Uma nova parceria estratégica foi anunciada!"
    event_technical_issue = "Um problema técnico foi descoberto no projeto!"
    
elif st.session_state.language == 'Español':
    # Tabs
    simulation_tab = "Simulación de Mercado"
    valuation_tab = "Valoración"
    stress_test_tab = "Prueba de Estrés de Mercado"
    research_tab = "Investigación de Mercado"
    
    # Simulation labels
    player_participation = "Participación del Jugador"
    market_volatility = "Volatilidad del Mercado"
    simulation_speed = "Velocidad de Simulación"
    day_label = "Día"
    of_label = "de"
    price_label = "Precio"
    holders_label = "Holders"
    volume_label = "Volumen"
    market_cap_label = "Cap. de Mercado"
    start_button = "Iniciar"
    pause_button = "Pausar"
    reset_button = "Reiniciar"
    simulation_description = "Esta simulación muestra cómo el token podría comportarse en el mercado según la participación del jugador y la volatilidad del mercado. También pueden ocurrir eventos aleatorios que afecten el precio."
    
    # Event messages
    event_large_buy = "¡Una ballena ha comprado una gran cantidad de tokens!"
    event_large_sell = "¡Un titular importante ha descargado sus tokens!"
    event_positive_news = "¡Se han publicado noticias positivas sobre el proyecto!"
    event_negative_news = "¡Circulan rumores negativos sobre el proyecto!"
    event_market_crash = "¡El mercado de criptomonedas está experimentando una caída general!"
    event_market_rally = "¡Todo el mercado de criptomonedas está en alza!"
    event_partnership = "¡Se ha anunciado una nueva asociación estratégica!"
    event_technical_issue = "¡Se ha descubierto un problema técnico en el proyecto!"
    
else:
    # Tabs
    simulation_tab = "Market Simulation"
    valuation_tab = "Valuation"
    stress_test_tab = "Market Stress Test"
    research_tab = "Market Research"
    
    # Simulation labels
    player_participation = "Player Participation"
    market_volatility = "Market Volatility"
    simulation_speed = "Simulation Speed"
    day_label = "Day"
    of_label = "of"
    price_label = "Price"
    holders_label = "Holders"
    volume_label = "Volume"
    market_cap_label = "Market Cap"
    start_button = "Start"
    pause_button = "Pause"
    reset_button = "Reset"
    simulation_description = "This simulation shows how the token could behave in the market based on player participation and market volatility. Random events can also occur affecting the price."
    
    # Event messages
    event_large_buy = "A whale has purchased a large amount of tokens!"
    event_large_sell = "A major holder has dumped their tokens!"
    event_positive_news = "Positive news about the project has been released!"
    event_negative_news = "Negative rumors are circulating about the project!"
    event_market_crash = "The crypto market is experiencing a general downturn!"
    event_market_rally = "The entire crypto market is rallying!"
    event_partnership = "A new strategic partnership has been announced!"
    event_technical_issue = "A technical issue has been discovered in the project!"

# Initialize simulation state in session_state
if 'market_simulation' not in st.session_state:
    st.session_state.market_simulation = {
        'running': False,
        'day': 1,
        'total_days': 30,
        'price': 5.23,
        'holders': 10000,
        'volume': 26200,
        'market_cap': 0,  # Will be calculated
        'history': [],
        'events': [],
        'player_participation': 5,
        'market_volatility': 5,
        'simulation_speed': 1,
    }
    
    # Initialize with first day data
    initial_market_cap = st.session_state.market_simulation['price'] * st.session_state.market_simulation['holders'] * 67  # Rough estimate that each holder has ~67 tokens on average
    
    st.session_state.market_simulation['market_cap'] = initial_market_cap
    st.session_state.market_simulation['history'].append({
        'day': 1,
        'price': st.session_state.market_simulation['price'],
        'holders': st.session_state.market_simulation['holders'],
        'volume': st.session_state.market_simulation['volume'],
        'market_cap': initial_market_cap,
        'event': None
    })

# Define tabs
tab1, tab2, tab3, tab4 = st.tabs([simulation_tab, valuation_tab, stress_test_tab, research_tab])

with tab1:  # Market Simulation tab
    # Controls section
    controls_col1, controls_col2, controls_col3 = st.columns(3)
    
    with controls_col1:
        player_part = st.slider(
            f"{player_participation}",
            min_value=1,
            max_value=10,
            value=st.session_state.market_simulation['player_participation'],
            help="Higher participation means more active trading and attention to the token"
        )
        if player_part != st.session_state.market_simulation['player_participation']:
            st.session_state.market_simulation['player_participation'] = player_part
    
    with controls_col2:
        market_vol = st.slider(
            f"{market_volatility}",
            min_value=1,
            max_value=10,
            value=st.session_state.market_simulation['market_volatility'],
            help="Higher volatility means larger price swings"
        )
        if market_vol != st.session_state.market_simulation['market_volatility']:
            st.session_state.market_simulation['market_volatility'] = market_vol
    
    with controls_col3:
        sim_speed = st.selectbox(
            f"{simulation_speed}",
            options=[1, 2, 3, 5, 10],
            index=0,
            format_func=lambda x: f"{x}x",
            help="Speed at which the simulation runs"
        )
        if sim_speed != st.session_state.market_simulation['simulation_speed']:
            st.session_state.market_simulation['simulation_speed'] = sim_speed
    
    # Display current day
    day_text = f"{day_label} {st.session_state.market_simulation['day']} {of_label} {st.session_state.market_simulation['total_days']}"
    st.subheader(day_text)
    
    # Current metrics
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    # Calculate price change percentage from previous day
    price_change_pct = 0
    if len(st.session_state.market_simulation['history']) > 1:
        prev_price = st.session_state.market_simulation['history'][-2]['price']
        current_price = st.session_state.market_simulation['price']
        price_change_pct = ((current_price - prev_price) / prev_price) * 100
    
    with metric_col1:
        st.metric(
            price_label,
            f"${st.session_state.market_simulation['price']:.2f}",
            f"{price_change_pct:.4f}%" if price_change_pct != 0 else "0.0000%"
        )
    
    with metric_col2:
        st.metric(
            holders_label,
            f"{st.session_state.market_simulation['holders']:,.2f}K"
        )
    
    with metric_col3:
        st.metric(
            volume_label,
            f"${st.session_state.market_simulation['volume'] / 1000:.1f}K"
        )
    
    with metric_col4:
        st.metric(
            market_cap_label,
            f"${st.session_state.market_simulation['market_cap'] / 1e9:.1f}B"
        )
    
    # Market simulation chart
    if st.session_state.market_simulation['history']:
        df = pd.DataFrame(st.session_state.market_simulation['history'])
        
        # Create a figure with secondary y-axis
        fig = go.Figure()
        
        # Add price line
        fig.add_trace(go.Scatter(
            x=df['day'],
            y=df['price'],
            name=price_label,
            line=dict(color='blue', width=2),
            hovertemplate=f"{price_label}: ${{y:.2f}}<extra></extra>"
        ))
        
        # Add holders line on secondary axis
        fig.add_trace(go.Scatter(
            x=df['day'],
            y=df['holders'],
            name=holders_label,
            line=dict(color='green', width=2),
            yaxis="y2",
            hovertemplate=f"{holders_label}: %{{y:,.0f}}<extra></extra>"
        ))
        
        # Add event markers if there are any
        events_df = df[df['event'].notna()]
        if not events_df.empty:
            fig.add_trace(go.Scatter(
                x=events_df['day'],
                y=events_df['price'],
                mode='markers',
                marker=dict(
                    symbol='star',
                    size=12,
                    color='red',
                ),
                name='Events',
                text=events_df['event'],
                hoverinfo='text'
            ))
        
        # Update layout for dual axis
        fig.update_layout(
            xaxis=dict(title=day_label),
            yaxis=dict(
                title=f"{price_label} ($)",
                titlefont=dict(color="blue"),
                tickfont=dict(color="blue")
            ),
            yaxis2=dict(
                title=holders_label,
                titlefont=dict(color="green"),
                tickfont=dict(color="green"),
                anchor="x",
                overlaying="y",
                side="right"
            ),
            height=500,
            hovermode="x unified",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display events if there are any
        if st.session_state.market_simulation['events']:
            with st.expander("Market Events", expanded=True):
                for i, event in enumerate(reversed(st.session_state.market_simulation['events'][-5:])):
                    st.info(f"Day {event['day']}: {event['message']}")
    
    # Simulation controls
    control_col1, control_col2, control_col3 = st.columns(3)
    
    with control_col1:
        if not st.session_state.market_simulation['running']:
            if st.button(start_button, key="start_sim"):
                st.session_state.market_simulation['running'] = True
                st.rerun()
        else:
            if st.button(pause_button, key="pause_sim"):
                st.session_state.market_simulation['running'] = False
                st.rerun()
    
    with control_col3:
        if st.button(reset_button, key="reset_sim"):
            # Reset simulation state
            st.session_state.market_simulation = {
                'running': False,
                'day': 1,
                'total_days': 30,
                'price': 5.23,
                'holders': 10000,
                'volume': 26200,
                'market_cap': 5.23 * 10000 * 67,  # Rough estimate
                'history': [],
                'events': [],
                'player_participation': 5,
                'market_volatility': 5,
                'simulation_speed': 1,
            }
            
            # Add initial data point
            st.session_state.market_simulation['history'].append({
                'day': 1,
                'price': st.session_state.market_simulation['price'],
                'holders': st.session_state.market_simulation['holders'],
                'volume': st.session_state.market_simulation['volume'],
                'market_cap': st.session_state.market_simulation['market_cap'],
                'event': None
            })
            
            st.rerun()
    
    # Simulation logic - run if simulation is active
    if st.session_state.market_simulation['running']:
        # Don't proceed if we reached the end
        if st.session_state.market_simulation['day'] >= st.session_state.market_simulation['total_days']:
            st.session_state.market_simulation['running'] = False
            st.warning(f"Simulation completed! Click '{reset_button}' to start a new simulation.")
        else:
            # Update simulation day
            st.session_state.market_simulation['day'] += 1
            
            # Calculate price changes based on parameters
            base_volatility = 0.01 * (st.session_state.market_simulation['market_volatility'] / 5)
            participation_factor = st.session_state.market_simulation['player_participation'] / 5
            
            # Base price change is random with influence from volatility
            price_change = np.random.normal(0, base_volatility)
            
            # Apply participation effects
            if participation_factor > 1:
                # Higher participation means more potential for positive movement
                price_change += 0.005 * (participation_factor - 1)
            
            # Random events (with probability based on volatility)
            event = None
            event_message = None
            event_change = 0
            
            # Higher volatility means more events
            event_chance = 0.05 + (st.session_state.market_simulation['market_volatility'] / 100)
            
            if random.random() < event_chance:
                event_type = random.choice([
                    "large_buy", "large_sell", "positive_news", "negative_news", 
                    "market_crash", "market_rally", "partnership", "technical_issue"
                ])
                
                if event_type == "large_buy":
                    event_change = 0.05 * (1 + random.random())
                    event_message = event_large_buy
                elif event_type == "large_sell":
                    event_change = -0.05 * (1 + random.random())
                    event_message = event_large_sell
                elif event_type == "positive_news":
                    event_change = 0.03 * (1 + random.random())
                    event_message = event_positive_news
                elif event_type == "negative_news":
                    event_change = -0.03 * (1 + random.random())
                    event_message = event_negative_news
                elif event_type == "market_crash":
                    event_change = -0.08 * (1 + random.random())
                    event_message = event_market_crash
                elif event_type == "market_rally":
                    event_change = 0.08 * (1 + random.random())
                    event_message = event_market_rally
                elif event_type == "partnership":
                    event_change = 0.06 * (1 + random.random())
                    event_message = event_partnership
                elif event_type == "technical_issue":
                    event_change = -0.06 * (1 + random.random())
                    event_message = event_technical_issue
                
                event = {
                    'day': st.session_state.market_simulation['day'],
                    'type': event_type,
                    'message': event_message,
                    'impact': event_change
                }
                st.session_state.market_simulation['events'].append(event)
            
            # Apply the event changes to the price
            if event:
                price_change += event_change
            
            # Apply price change
            new_price = st.session_state.market_simulation['price'] * (1 + price_change)
            new_price = max(0.01, new_price)  # Prevent price from going too low
            
            # Update holders based on price movement and participation
            holders_change_pct = 0.02 * participation_factor
            if price_change > 0:
                # Price increase generally attracts holders
                holders_change = st.session_state.market_simulation['holders'] * holders_change_pct * random.uniform(0.5, 1.5)
            else:
                # Price decrease might make holders leave
                holders_change = st.session_state.market_simulation['holders'] * -holders_change_pct * random.uniform(0.5, 1.2)
            
            # Event effects on holders
            if event:
                if event_change > 0:
                    # Positive events attract more holders
                    holders_change += st.session_state.market_simulation['holders'] * abs(event_change) * 0.5
                else:
                    # Negative events cause holders to leave
                    holders_change -= st.session_state.market_simulation['holders'] * abs(event_change) * 0.4
            
            new_holders = st.session_state.market_simulation['holders'] + holders_change
            new_holders = max(1000, new_holders)  # Ensure there's a minimum number of holders
            
            # Calculate new volume based on price change and participation
            base_volume = st.session_state.market_simulation['volume']
            volume_factor = (1 + abs(price_change) * 10) * participation_factor
            
            if event:
                # Events increase trading volume
                volume_factor *= (1 + abs(event_change) * 5)
            
            new_volume = base_volume * volume_factor * random.uniform(0.8, 1.2)
            
            # Calculate new market cap
            avg_tokens_per_holder = 67  # Assumed average
            new_market_cap = new_price * new_holders * avg_tokens_per_holder
            
            # Update simulation state
            st.session_state.market_simulation['price'] = new_price
            st.session_state.market_simulation['holders'] = new_holders
            st.session_state.market_simulation['volume'] = new_volume
            st.session_state.market_simulation['market_cap'] = new_market_cap
            
            # Add to history
            st.session_state.market_simulation['history'].append({
                'day': st.session_state.market_simulation['day'],
                'price': new_price,
                'holders': new_holders,
                'volume': new_volume,
                'market_cap': new_market_cap,
                'event': event_message if event else None
            })
            
            # Rerun to update UI
            time.sleep(1 / st.session_state.market_simulation['simulation_speed'])
            st.rerun()
    
    # Simulation description
    st.info(simulation_description)

with tab2:  # Valuation tab
    st.subheader("Token Valuation Models")
    st.markdown("Implement different token valuation models here")

with tab3:  # Market Stress Test tab
    st.subheader("Market Stress Test")
    st.markdown("Implement market stress test functionality here")

with tab4:  # Market Research tab
    st.subheader("Market Research")
    st.markdown("Implement market research functionality here")

# Footer
st.markdown("---")
st.markdown("TokenomicsLab - Market & Valuation Module")