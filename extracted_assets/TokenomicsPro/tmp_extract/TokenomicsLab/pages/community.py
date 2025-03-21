import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os

# Import local modules
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.tokenomics import TokenomicsModel

st.set_page_config(
    page_title="Comunidade | Tokenomics Lab",
    page_icon="👥",
    layout="wide"
)

# Sidebar
st.sidebar.title("Tokenomics Lab")
st.sidebar.image("https://cdn.jsdelivr.net/npm/cryptocurrency-icons@0.18.1/svg/icon/btc.svg", width=50)

# Main content
st.title("Gestão de Comunidade")
st.markdown("""
    Gerencie aspectos relacionados à comunidade do seu projeto, incluindo incentivos,
    engajamento, governança, educação e crescimento da comunidade.
""")

# Check if model exists in session state
if 'model' not in st.session_state:
    st.warning("Você ainda não criou um modelo de tokenomics. Vá para a página de Simulação para criar um modelo primeiro.")
    
    # Button to go to simulation page
    if st.button("Ir para Simulação"):
        st.switch_page("pages/simulation.py")
        
    st.stop()

# Initialize community data in session state if not exists
if 'community' not in st.session_state:
    st.session_state.community = {
        "channels": [],
        "growth_targets": {
            "month_3": {
                "telegram": 3000,
                "discord": 2000,
                "twitter": 5000,
                "dau": 1000
            },
            "month_6": {
                "telegram": 8000,
                "discord": 5000,
                "twitter": 15000,
                "dau": 3000
            },
            "month_12": {
                "telegram": 20000,
                "discord": 15000,
                "twitter": 50000,
                "dau": 10000
            }
        },
        "engagement_activities": [],
        "content_calendar": [],
        "governance": {
            "model": "token-voting",
            "quorum": 30,
            "voting_period": 7,
            "proposal_threshold": 1.0,
            "forum": ""
        },
        "team": [],
        "community_metrics": {
            "current": {
                "telegram": 0,
                "discord": 0,
                "twitter": 0,
                "dau": 0
            },
            "historical": []
        }
    }

# Community Management Configuration
st.header("Configuração da Comunidade")

# Community Channels
st.subheader("Canais da Comunidade")
st.markdown("Configure os canais de comunicação e interação com sua comunidade.")

# Dynamic form for community channels
if st.button("Adicionar Canal"):
    st.session_state.community["channels"].append({
        "name": "",
        "platform": "Telegram",
        "url": "",
        "description": "",
        "primary": False,
        "language": "Português"
    })

# Display existing channels
channels_to_remove = []

for i, channel in enumerate(st.session_state.community["channels"]):
    with st.expander(f"Canal {i+1}: {channel['name'] or 'Novo Canal'}"):
        col1, col2 = st.columns(2)
        
        with col1:
            channel["name"] = st.text_input(
                "Nome do Canal", 
                value=channel["name"],
                key=f"chan_name_{i}"
            )
            
            channel["platform"] = st.selectbox(
                "Plataforma", 
                ["Telegram", "Discord", "Twitter", "Reddit", "Medium", "GitHub", "Website", "Outro"],
                index=["Telegram", "Discord", "Twitter", "Reddit", "Medium", "GitHub", "Website", "Outro"].index(channel["platform"]) if channel["platform"] in ["Telegram", "Discord", "Twitter", "Reddit", "Medium", "GitHub", "Website", "Outro"] else 0,
                key=f"chan_platform_{i}"
            )
            
            channel["url"] = st.text_input(
                "URL", 
                value=channel["url"],
                key=f"chan_url_{i}"
            )
        
        with col2:
            channel["description"] = st.text_area(
                "Descrição", 
                value=channel["description"],
                height=100,
                key=f"chan_desc_{i}"
            )
            
            channel["primary"] = st.checkbox(
                "Canal Principal", 
                value=channel["primary"],
                key=f"chan_primary_{i}"
            )
            
            channel["language"] = st.selectbox(
                "Idioma Principal", 
                ["Português", "Inglês", "Espanhol", "Chinês", "Russo", "Multilíngue"],
                index=["Português", "Inglês", "Espanhol", "Chinês", "Russo", "Multilíngue"].index(channel["language"]) if channel["language"] in ["Português", "Inglês", "Espanhol", "Chinês", "Russo", "Multilíngue"] else 0,
                key=f"chan_lang_{i}"
            )
        
        if st.button("Remover Canal", key=f"remove_chan_{i}"):
            channels_to_remove.append(i)

# Remove channels marked for removal
if channels_to_remove:
    st.session_state.community["channels"] = [chan for i, chan in enumerate(st.session_state.community["channels"]) 
                                if i not in channels_to_remove]

# Community Growth Targets
st.subheader("Metas de Crescimento da Comunidade")
st.markdown("Defina metas de crescimento para sua comunidade em diferentes horizontes de tempo.")

tab1, tab2, tab3 = st.tabs(["3 Meses", "6 Meses", "12 Meses"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        telegram_3m = st.number_input(
            "Meta de Usuários Telegram (3m)",
            min_value=0,
            value=st.session_state.community["growth_targets"]["month_3"]["telegram"],
            step=100,
            help="Meta de membros no Telegram para 3 meses."
        )
        
        discord_3m = st.number_input(
            "Meta de Usuários Discord (3m)",
            min_value=0,
            value=st.session_state.community["growth_targets"]["month_3"]["discord"],
            step=100,
            help="Meta de membros no Discord para 3 meses."
        )
    
    with col2:
        twitter_3m = st.number_input(
            "Meta de Seguidores Twitter (3m)",
            min_value=0,
            value=st.session_state.community["growth_targets"]["month_3"]["twitter"],
            step=100,
            help="Meta de seguidores no Twitter para 3 meses."
        )
        
        dau_3m = st.number_input(
            "Meta de Usuários Ativos Diários (3m)",
            min_value=0,
            value=st.session_state.community["growth_targets"]["month_3"]["dau"],
            step=100,
            help="Meta de usuários ativos diários para 3 meses."
        )

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        telegram_6m = st.number_input(
            "Meta de Usuários Telegram (6m)",
            min_value=0,
            value=st.session_state.community["growth_targets"]["month_6"]["telegram"],
            step=100,
            help="Meta de membros no Telegram para 6 meses."
        )
        
        discord_6m = st.number_input(
            "Meta de Usuários Discord (6m)",
            min_value=0,
            value=st.session_state.community["growth_targets"]["month_6"]["discord"],
            step=100,
            help="Meta de membros no Discord para 6 meses."
        )
    
    with col2:
        twitter_6m = st.number_input(
            "Meta de Seguidores Twitter (6m)",
            min_value=0,
            value=st.session_state.community["growth_targets"]["month_6"]["twitter"],
            step=100,
            help="Meta de seguidores no Twitter para 6 meses."
        )
        
        dau_6m = st.number_input(
            "Meta de Usuários Ativos Diários (6m)",
            min_value=0,
            value=st.session_state.community["growth_targets"]["month_6"]["dau"],
            step=100,
            help="Meta de usuários ativos diários para 6 meses."
        )

with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        telegram_12m = st.number_input(
            "Meta de Usuários Telegram (12m)",
            min_value=0,
            value=st.session_state.community["growth_targets"]["month_12"]["telegram"],
            step=100,
            help="Meta de membros no Telegram para 12 meses."
        )
        
        discord_12m = st.number_input(
            "Meta de Usuários Discord (12m)",
            min_value=0,
            value=st.session_state.community["growth_targets"]["month_12"]["discord"],
            step=100,
            help="Meta de membros no Discord para 12 meses."
        )
    
    with col2:
        twitter_12m = st.number_input(
            "Meta de Seguidores Twitter (12m)",
            min_value=0,
            value=st.session_state.community["growth_targets"]["month_12"]["twitter"],
            step=100,
            help="Meta de seguidores no Twitter para 12 meses."
        )
        
        dau_12m = st.number_input(
            "Meta de Usuários Ativos Diários (12m)",
            min_value=0,
            value=st.session_state.community["growth_targets"]["month_12"]["dau"],
            step=100,
            help="Meta de usuários ativos diários para 12 meses."
        )

# Current Community Metrics
st.subheader("Métricas Atuais da Comunidade")
st.markdown("Insira as métricas atuais da sua comunidade.")

col1, col2, col3, col4 = st.columns(4)

with col1:
    current_telegram = st.number_input(
        "Usuários Telegram Atual",
        min_value=0,
        value=st.session_state.community["community_metrics"]["current"]["telegram"],
        step=10,
        help="Número atual de membros no Telegram."
    )

with col2:
    current_discord = st.number_input(
        "Usuários Discord Atual",
        min_value=0,
        value=st.session_state.community["community_metrics"]["current"]["discord"],
        step=10,
        help="Número atual de membros no Discord."
    )

with col3:
    current_twitter = st.number_input(
        "Seguidores Twitter Atual",
        min_value=0,
        value=st.session_state.community["community_metrics"]["current"]["twitter"],
        step=10,
        help="Número atual de seguidores no Twitter."
    )

with col4:
    current_dau = st.number_input(
        "Usuários Ativos Diários Atual",
        min_value=0,
        value=st.session_state.community["community_metrics"]["current"]["dau"],
        step=10,
        help="Número atual de usuários ativos diários."
    )

# Community Engagement Activities
st.subheader("Atividades de Engajamento")
st.markdown("Adicione atividades para engajar sua comunidade.")

# Dynamic form for engagement activities
if st.button("Adicionar Atividade de Engajamento"):
    st.session_state.community["engagement_activities"].append({
        "name": "",
        "description": "",
        "frequency": "Semanal",
        "audience": "Toda a comunidade",
        "rewards": "",
        "platform": "Discord"
    })

# Display existing engagement activities
activities_to_remove = []

for i, activity in enumerate(st.session_state.community["engagement_activities"]):
    with st.expander(f"Atividade {i+1}: {activity['name'] or 'Nova Atividade'}"):
        col1, col2 = st.columns(2)
        
        with col1:
            activity["name"] = st.text_input(
                "Nome da Atividade", 
                value=activity["name"],
                key=f"act_name_{i}"
            )
            
            activity["description"] = st.text_area(
                "Descrição", 
                value=activity["description"],
                height=100,
                key=f"act_desc_{i}"
            )
            
            activity["frequency"] = st.selectbox(
                "Frequência", 
                ["Diária", "Semanal", "Quinzenal", "Mensal", "Trimestral", "Única"],
                index=["Diária", "Semanal", "Quinzenal", "Mensal", "Trimestral", "Única"].index(activity["frequency"]) if activity["frequency"] in ["Diária", "Semanal", "Quinzenal", "Mensal", "Trimestral", "Única"] else 1,
                key=f"act_freq_{i}"
            )
        
        with col2:
            activity["audience"] = st.text_input(
                "Público-Alvo", 
                value=activity["audience"],
                key=f"act_audience_{i}"
            )
            
            activity["rewards"] = st.text_input(
                "Recompensas", 
                value=activity["rewards"],
                key=f"act_rewards_{i}"
            )
            
            activity["platform"] = st.selectbox(
                "Plataforma Principal", 
                ["Discord", "Telegram", "Twitter", "Website", "Múltiplas"],
                index=["Discord", "Telegram", "Twitter", "Website", "Múltiplas"].index(activity["platform"]) if activity["platform"] in ["Discord", "Telegram", "Twitter", "Website", "Múltiplas"] else 0,
                key=f"act_platform_{i}"
            )
        
        if st.button("Remover Atividade", key=f"remove_act_{i}"):
            activities_to_remove.append(i)

# Remove activities marked for removal
if activities_to_remove:
    st.session_state.community["engagement_activities"] = [act for i, act in enumerate(st.session_state.community["engagement_activities"]) 
                                          if i not in activities_to_remove]

# Content Calendar
st.subheader("Calendário de Conteúdo")
st.markdown("Planeje seu calendário de conteúdo para a comunidade.")

# Dynamic form for content calendar entries
if st.button("Adicionar Item no Calendário"):
    today = datetime.now()
    st.session_state.community["content_calendar"].append({
        "title": "",
        "date": today.strftime("%Y-%m-%d"),
        "content_type": "Blog Post",
        "description": "",
        "audience": "Toda a comunidade",
        "channels": []
    })

# Display existing calendar entries
calendar_to_remove = []

for i, entry in enumerate(st.session_state.community["content_calendar"]):
    with st.expander(f"Conteúdo {i+1}: {entry['title'] or 'Novo Conteúdo'} - {entry['date']}"):
        col1, col2 = st.columns(2)
        
        with col1:
            entry["title"] = st.text_input(
                "Título", 
                value=entry["title"],
                key=f"cal_title_{i}"
            )
            
            entry_date = st.date_input(
                "Data", 
                value=datetime.strptime(entry["date"], "%Y-%m-%d") if isinstance(entry["date"], str) else entry["date"],
                key=f"cal_date_{i}"
            )
            entry["date"] = entry_date.strftime("%Y-%m-%d")
            
            entry["content_type"] = st.selectbox(
                "Tipo de Conteúdo", 
                ["Blog Post", "Tweet Thread", "Vídeo", "AMA", "Newsletter", "Infográfico", "Tutorial", "Evento", "Outro"],
                index=["Blog Post", "Tweet Thread", "Vídeo", "AMA", "Newsletter", "Infográfico", "Tutorial", "Evento", "Outro"].index(entry["content_type"]) if entry["content_type"] in ["Blog Post", "Tweet Thread", "Vídeo", "AMA", "Newsletter", "Infográfico", "Tutorial", "Evento", "Outro"] else 0,
                key=f"cal_type_{i}"
            )
        
        with col2:
            entry["description"] = st.text_area(
                "Descrição", 
                value=entry["description"],
                height=100,
                key=f"cal_desc_{i}"
            )
            
            entry["audience"] = st.text_input(
                "Público-Alvo", 
                value=entry["audience"],
                key=f"cal_audience_{i}"
            )
            
            # Channels selection based on the available channels
            channel_options = [channel["name"] for channel in st.session_state.community["channels"] if channel["name"]]
            if channel_options:
                selected_channels = st.multiselect(
                    "Canais de Distribuição",
                    options=channel_options,
                    default=entry["channels"],
                    key=f"cal_channels_{i}"
                )
                entry["channels"] = selected_channels
        
        if st.button("Remover do Calendário", key=f"remove_cal_{i}"):
            calendar_to_remove.append(i)

# Remove calendar entries marked for removal
if calendar_to_remove:
    st.session_state.community["content_calendar"] = [entry for i, entry in enumerate(st.session_state.community["content_calendar"]) 
                                      if i not in calendar_to_remove]

# Governance Configuration
st.subheader("Configuração de Governança Comunitária")
st.markdown("Configure como sua comunidade participa da governança do projeto.")

col1, col2 = st.columns(2)

with col1:
    governance_model = st.selectbox(
        "Modelo de Governança",
        ["Votação baseada em tokens", "Votação quadrática", "Multisig comunitário", "DAO", "Conselho de governança"],
        index=["Votação baseada em tokens", "Votação quadrática", "Multisig comunitário", "DAO", "Conselho de governança"].index(
            "Votação baseada em tokens" if st.session_state.community["governance"]["model"] == "token-voting" else
            "Votação quadrática" if st.session_state.community["governance"]["model"] == "quadratic" else
            "Multisig comunitário" if st.session_state.community["governance"]["model"] == "multisig" else
            "DAO" if st.session_state.community["governance"]["model"] == "dao" else
            "Conselho de governança"
        ),
        help="Método de tomada de decisão da comunidade."
    )
    
    # Map selection to internal value
    gov_model_map = {
        "Votação baseada em tokens": "token-voting",
        "Votação quadrática": "quadratic",
        "Multisig comunitário": "multisig",
        "DAO": "dao",
        "Conselho de governança": "council"
    }
    governance_model_internal = gov_model_map[governance_model]
    
    quorum = st.slider(
        "Quórum (%)",
        min_value=1,
        max_value=100,
        value=st.session_state.community["governance"]["quorum"],
        step=1,
        help="Percentagem mínima de participação necessária para validar uma votação."
    )
    
    voting_period = st.slider(
        "Período de Votação (dias)",
        min_value=1,
        max_value=30,
        value=st.session_state.community["governance"]["voting_period"],
        step=1,
        help="Duração do período de votação em dias."
    )

with col2:
    proposal_threshold = st.number_input(
        "Limite para Propostas (%)",
        min_value=0.0,
        max_value=10.0,
        value=st.session_state.community["governance"]["proposal_threshold"],
        step=0.1,
        help="Percentagem mínima de tokens que um endereço precisa ter para submeter uma proposta."
    )
    
    governance_forum = st.text_input(
        "Fórum de Governança (URL)",
        value=st.session_state.community["governance"]["forum"],
        help="URL do fórum de discussão para propostas de governança."
    )

# Community Team
st.subheader("Equipe de Comunidade")
st.markdown("Configure a equipe responsável pela gestão da comunidade.")

# Dynamic form for team members
if st.button("Adicionar Membro da Equipe"):
    st.session_state.community["team"].append({
        "name": "",
        "role": "Community Manager",
        "responsibilities": "",
        "channels": [],
        "contact": ""
    })

# Display existing team members
team_to_remove = []

for i, member in enumerate(st.session_state.community["team"]):
    with st.expander(f"Membro {i+1}: {member['name'] or 'Novo Membro'} - {member['role']}"):
        col1, col2 = st.columns(2)
        
        with col1:
            member["name"] = st.text_input(
                "Nome", 
                value=member["name"],
                key=f"team_name_{i}"
            )
            
            member["role"] = st.selectbox(
                "Cargo", 
                ["Community Manager", "Moderador", "Content Creator", "Developer Relations", "Ambassador", "Outro"],
                index=["Community Manager", "Moderador", "Content Creator", "Developer Relations", "Ambassador", "Outro"].index(member["role"]) if member["role"] in ["Community Manager", "Moderador", "Content Creator", "Developer Relations", "Ambassador", "Outro"] else 0,
                key=f"team_role_{i}"
            )
            
            member["contact"] = st.text_input(
                "Contato", 
                value=member["contact"],
                key=f"team_contact_{i}"
            )
        
        with col2:
            member["responsibilities"] = st.text_area(
                "Responsabilidades", 
                value=member["responsibilities"],
                height=100,
                key=f"team_resp_{i}"
            )
            
            # Channels selection based on the available channels
            channel_options = [channel["name"] for channel in st.session_state.community["channels"] if channel["name"]]
            if channel_options:
                selected_channels = st.multiselect(
                    "Canais Gerenciados",
                    options=channel_options,
                    default=member["channels"],
                    key=f"team_channels_{i}"
                )
                member["channels"] = selected_channels
        
        if st.button("Remover Membro", key=f"remove_team_{i}"):
            team_to_remove.append(i)

# Remove team members marked for removal
if team_to_remove:
    st.session_state.community["team"] = [member for i, member in enumerate(st.session_state.community["team"]) 
                              if i not in team_to_remove]

# Save button
if st.button("Salvar Configurações de Comunidade", type="primary"):
    # Update community data in session state
    st.session_state.community["growth_targets"] = {
        "month_3": {
            "telegram": telegram_3m,
            "discord": discord_3m,
            "twitter": twitter_3m,
            "dau": dau_3m
        },
        "month_6": {
            "telegram": telegram_6m,
            "discord": discord_6m,
            "twitter": twitter_6m,
            "dau": dau_6m
        },
        "month_12": {
            "telegram": telegram_12m,
            "discord": discord_12m,
            "twitter": twitter_12m,
            "dau": dau_12m
        }
    }
    
    st.session_state.community["community_metrics"]["current"] = {
        "telegram": current_telegram,
        "discord": current_discord,
        "twitter": current_twitter,
        "dau": current_dau
    }
    
    # Add current metrics to historical data
    today = datetime.now().strftime("%Y-%m-%d")
    st.session_state.community["community_metrics"]["historical"].append({
        "date": today,
        "telegram": current_telegram,
        "discord": current_discord,
        "twitter": current_twitter,
        "dau": current_dau
    })
    
    st.session_state.community["governance"] = {
        "model": governance_model_internal,
        "quorum": quorum,
        "voting_period": voting_period,
        "proposal_threshold": proposal_threshold,
        "forum": governance_forum
    }
    
    st.success("Configurações de comunidade salvas com sucesso!")

# Visualizations
st.header("Visualizações de Comunidade")

# Community Growth Targets Visualization
st.subheader("Metas de Crescimento da Comunidade")

# Create data for chart
periods = ["Atual", "3 Meses", "6 Meses", "12 Meses"]

telegram_values = [
    current_telegram,
    telegram_3m,
    telegram_6m,
    telegram_12m
]

discord_values = [
    current_discord,
    discord_3m,
    discord_6m,
    discord_12m
]

twitter_values = [
    current_twitter,
    twitter_3m,
    twitter_6m,
    twitter_12m
]

dau_values = [
    current_dau,
    dau_3m,
    dau_6m,
    dau_12m
]

# Create growth chart
fig = go.Figure()

fig.add_trace(go.Bar(
    x=periods,
    y=telegram_values,
    name='Telegram',
    marker_color='#0088cc'
))

fig.add_trace(go.Bar(
    x=periods,
    y=discord_values,
    name='Discord',
    marker_color='#5865F2'
))

fig.add_trace(go.Bar(
    x=periods,
    y=twitter_values,
    name='Twitter',
    marker_color='#1DA1F2'
))

fig.add_trace(go.Bar(
    x=periods,
    y=dau_values,
    name='Usuários Ativos Diários',
    marker_color='#ff4b4b'
))

fig.update_layout(
    title="Metas de Crescimento da Comunidade",
    xaxis_title="Período",
    yaxis_title="Número de Usuários",
    barmode='group',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5
    )
)

st.plotly_chart(fig, use_container_width=True)

# Community Channels Visualization
if st.session_state.community["channels"]:
    st.subheader("Canais de Comunidade")
    
    # Filter channels with names
    valid_channels = [channel for channel in st.session_state.community["channels"] if channel["name"]]
    
    if valid_channels:
        # Create dataframe for visualization
        channel_data = []
        for channel in valid_channels:
            channel_data.append({
                "Nome": channel["name"],
                "Plataforma": channel["platform"],
                "Idioma": channel["language"],
                "Principal": "Sim" if channel["primary"] else "Não",
                "URL": channel["url"]
            })
        
        channel_df = pd.DataFrame(channel_data)
        
        # Display as table
        st.dataframe(channel_df, hide_index=True)
        
        # Create pie chart of platforms
        platform_counts = {}
        for channel in valid_channels:
            platform = channel["platform"]
            platform_counts[platform] = platform_counts.get(platform, 0) + 1
        
        fig = px.pie(
            values=list(platform_counts.values()),
            names=list(platform_counts.keys()),
            title="Distribuição de Canais por Plataforma",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        
        st.plotly_chart(fig, use_container_width=True)

# Content Calendar Visualization
if st.session_state.community["content_calendar"]:
    st.subheader("Calendário de Conteúdo")
    
    # Filter entries with titles
    valid_entries = [entry for entry in st.session_state.community["content_calendar"] if entry["title"]]
    
    if valid_entries:
        # Sort by date
        sorted_entries = sorted(valid_entries, key=lambda x: x["date"])
        
        # Create gantt chart for content calendar
        entry_data = []
        for i, entry in enumerate(sorted_entries):
            start_date = datetime.strptime(entry["date"], "%Y-%m-%d")
            # Assume content is available for 7 days (for visualization purposes)
            end_date = start_date + timedelta(days=7)
            
            entry_data.append({
                "Conteúdo": entry["title"],
                "Tipo": entry["content_type"],
                "Início": start_date,
                "Fim": end_date,
                "Público": entry["audience"]
            })
        
        entry_df = pd.DataFrame(entry_data)
        
        # Create gantt chart
        fig = px.timeline(
            entry_df, 
            x_start="Início", 
            x_end="Fim", 
            y="Conteúdo",
            color="Tipo",
            hover_data=["Público"],
            title="Calendário de Conteúdo"
        )
        
        fig.update_yaxes(autorange="reversed")
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display upcoming content
        st.subheader("Próximos Conteúdos")
        
        today = datetime.now()
        upcoming_entries = [entry for entry in sorted_entries if datetime.strptime(entry["date"], "%Y-%m-%d") >= today]
        
        if upcoming_entries:
            upcoming_data = []
            for entry in upcoming_entries[:5]:  # Show next 5 entries
                upcoming_data.append({
                    "Data": entry["date"],
                    "Título": entry["title"],
                    "Tipo": entry["content_type"],
                    "Canais": ", ".join(entry["channels"])
                })
            
            upcoming_df = pd.DataFrame(upcoming_data)
            st.dataframe(upcoming_df, hide_index=True)
        else:
            st.info("Não há conteúdo programado para datas futuras.")

# Engagement Activities Visualization
if st.session_state.community["engagement_activities"]:
    st.subheader("Atividades de Engajamento")
    
    # Filter activities with names
    valid_activities = [activity for activity in st.session_state.community["engagement_activities"] if activity["name"]]
    
    if valid_activities:
        # Create frequency chart
        frequency_counts = {}
        for activity in valid_activities:
            freq = activity["frequency"]
            frequency_counts[freq] = frequency_counts.get(freq, 0) + 1
        
        fig = px.bar(
            x=list(frequency_counts.keys()),
            y=list(frequency_counts.values()),
            title="Atividades por Frequência",
            labels={"x": "Frequência", "y": "Número de Atividades"},
            color=list(frequency_counts.keys()),
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display activities table
        activity_data = []
        for activity in valid_activities:
            activity_data.append({
                "Nome": activity["name"],
                "Frequência": activity["frequency"],
                "Plataforma": activity["platform"],
                "Público": activity["audience"],
                "Recompensas": activity["rewards"]
            })
        
        activity_df = pd.DataFrame(activity_data)
        st.dataframe(activity_df, hide_index=True)

# Team Visualization
if st.session_state.community["team"]:
    st.subheader("Equipe de Comunidade")
    
    # Filter team members with names
    valid_members = [member for member in st.session_state.community["team"] if member["name"]]
    
    if valid_members:
        # Create role distribution chart
        role_counts = {}
        for member in valid_members:
            role = member["role"]
            role_counts[role] = role_counts.get(role, 0) + 1
        
        fig = px.pie(
            values=list(role_counts.values()),
            names=list(role_counts.keys()),
            title="Distribuição de Cargos na Equipe",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display team table
        team_data = []
        for member in valid_members:
            team_data.append({
                "Nome": member["name"],
                "Cargo": member["role"],
                "Canais": ", ".join(member["channels"]),
                "Contato": member["contact"]
            })
        
        team_df = pd.DataFrame(team_data)
        st.dataframe(team_df, hide_index=True)

# Governance Visualization
st.subheader("Governança Comunitária")

# Create data for governance visualization
gov_metrics = [
    {"Métrica": "Modelo de Governança", "Valor": governance_model},
    {"Métrica": "Quórum", "Valor": f"{quorum}%"},
    {"Métrica": "Período de Votação", "Valor": f"{voting_period} dias"},
    {"Métrica": "Limite para Propostas", "Valor": f"{proposal_threshold}%"}
]

if governance_forum:
    gov_metrics.append({"Métrica": "Fórum de Governança", "Valor": governance_forum})

# Create a table for governance metrics
fig = go.Figure(data=[go.Table(
    header=dict(
        values=["<b>Parâmetro de Governança</b>", "<b>Valor</b>"],
        fill_color='#0068c9',
        align='center',
        font=dict(color='white', size=14)
    ),
    cells=dict(
        values=[
            [m["Métrica"] for m in gov_metrics],
            [m["Valor"] for m in gov_metrics]
        ],
        fill_color=['#f5f7fa', '#edf3f9'],
        align='left',
        font=dict(size=12)
    )
)])

fig.update_layout(
    margin=dict(l=10, r=10, t=10, b=10),
    height=200
)

st.plotly_chart(fig, use_container_width=True)

# Community Growth Rate Calculation
st.subheader("Taxa de Crescimento Projetada")

# Calculate growth rates
growth_rates = []

if current_telegram > 0:
    telegram_growth_3m = ((telegram_3m / current_telegram) - 1) * 100
    telegram_growth_6m = ((telegram_6m / current_telegram) - 1) * 100
    telegram_growth_12m = ((telegram_12m / current_telegram) - 1) * 100
    
    growth_rates.append({
        "Canal": "Telegram",
        "Crescimento 3 Meses (%)": telegram_growth_3m,
        "Crescimento 6 Meses (%)": telegram_growth_6m,
        "Crescimento 12 Meses (%)": telegram_growth_12m
    })

if current_discord > 0:
    discord_growth_3m = ((discord_3m / current_discord) - 1) * 100
    discord_growth_6m = ((discord_6m / current_discord) - 1) * 100
    discord_growth_12m = ((discord_12m / current_discord) - 1) * 100
    
    growth_rates.append({
        "Canal": "Discord",
        "Crescimento 3 Meses (%)": discord_growth_3m,
        "Crescimento 6 Meses (%)": discord_growth_6m,
        "Crescimento 12 Meses (%)": discord_growth_12m
    })

if current_twitter > 0:
    twitter_growth_3m = ((twitter_3m / current_twitter) - 1) * 100
    twitter_growth_6m = ((twitter_6m / current_twitter) - 1) * 100
    twitter_growth_12m = ((twitter_12m / current_twitter) - 1) * 100
    
    growth_rates.append({
        "Canal": "Twitter",
        "Crescimento 3 Meses (%)": twitter_growth_3m,
        "Crescimento 6 Meses (%)": twitter_growth_6m,
        "Crescimento 12 Meses (%)": twitter_growth_12m
    })

if current_dau > 0:
    dau_growth_3m = ((dau_3m / current_dau) - 1) * 100
    dau_growth_6m = ((dau_6m / current_dau) - 1) * 100
    dau_growth_12m = ((dau_12m / current_dau) - 1) * 100
    
    growth_rates.append({
        "Canal": "Usuários Ativos Diários",
        "Crescimento 3 Meses (%)": dau_growth_3m,
        "Crescimento 6 Meses (%)": dau_growth_6m,
        "Crescimento 12 Meses (%)": dau_growth_12m
    })

if growth_rates:
    # Display growth rates
    growth_df = pd.DataFrame(growth_rates)
    st.dataframe(growth_df, hide_index=True)
    
    # Create growth rate chart
    fig = go.Figure()
    
    for rate in growth_rates:
        fig.add_trace(go.Scatter(
            x=["3 Meses", "6 Meses", "12 Meses"],
            y=[rate["Crescimento 3 Meses (%)"], rate["Crescimento 6 Meses (%)"], rate["Crescimento 12 Meses (%)"]],
            mode='lines+markers',
            name=rate["Canal"]
        ))
    
    fig.update_layout(
        title="Taxa de Crescimento da Comunidade",
        xaxis_title="Período",
        yaxis_title="Crescimento (%)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        hovermode="x unified"
    )
    
    fig.update_yaxes(ticksuffix="%")
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Informe os valores atuais das métricas de comunidade para visualizar as taxas de crescimento.")

# Community Action Plan
st.header("Plano de Ação Comunitário")

# Generate action plan based on the community data
action_items = []

# Check if channels are defined
if not st.session_state.community["channels"]:
    action_items.append("Criar canais oficiais da comunidade em pelo menos 2-3 plataformas diferentes (ex: Discord, Telegram, Twitter).")

# Check if growth targets are reasonable
if current_telegram > 0 and telegram_3m > 0:
    telegram_growth_3m = ((telegram_3m / current_telegram) - 1) * 100
    if telegram_growth_3m > 1000:  # More than 10x growth in 3 months
        action_items.append("Revisar as metas de crescimento para o Telegram, pois parecem muito otimistas. Considere um crescimento mais gradual.")

# Check if team is defined
if not st.session_state.community["team"]:
    action_items.append("Definir a equipe de comunidade com papéis claros e responsabilidades para garantir uma gestão eficaz.")

# Check if engagement activities are defined
if not st.session_state.community["engagement_activities"]:
    action_items.append("Planejar atividades de engajamento recorrentes para manter a comunidade ativa e interessada no projeto.")

# Check if content calendar is defined
if not st.session_state.community["content_calendar"]:
    action_items.append("Desenvolver um calendário de conteúdo para os próximos 3 meses para manter a comunidade informada e engajada.")

# Check if governance forum is defined
if not governance_forum:
    action_items.append("Estabelecer um fórum de governança onde a comunidade possa discutir propostas e participar da tomada de decisões.")

# General recommendations
general_recommendations = [
    "Implementar um programa de embaixadores para ampliar o alcance da comunidade em diferentes regiões.",
    "Desenvolver recursos educacionais para ajudar novos membros a entenderem o projeto e seus conceitos-chave.",
    "Realizar AMAs (Ask Me Anything) regulares com a equipe para manter a transparência e conexão com a comunidade.",
    "Criar um programa de recompensas por contribuições (bounties) para incentivar a participação ativa da comunidade.",
    "Implementar um sistema de feedback para que a comunidade possa compartilhar sugestões e ideias para melhorias."
]

# Add general recommendations if needed
while len(action_items) < 5:
    if not general_recommendations:
        break
    action_items.append(general_recommendations.pop(0))

# Display action items
for i, item in enumerate(action_items):
    st.markdown(f"**{i+1}.** {item}")

# Community Timeline
st.subheader("Linha do Tempo da Comunidade")

# Generate timeline based on growth targets
timeline_events = []

# Set reference date as today
today = datetime.now()

# Add current state
timeline_events.append({
    "date": today.strftime("%Y-%m-%d"),
    "event": "Estado Atual",
    "description": f"Telegram: {current_telegram}, Discord: {current_discord}, Twitter: {current_twitter}, DAU: {current_dau}"
})

# Add 3-month milestone
three_months = today + timedelta(days=90)
timeline_events.append({
    "date": three_months.strftime("%Y-%m-%d"),
    "event": "Meta de 3 Meses",
    "description": f"Telegram: {telegram_3m}, Discord: {discord_3m}, Twitter: {twitter_3m}, DAU: {dau_3m}"
})

# Add 6-month milestone
six_months = today + timedelta(days=180)
timeline_events.append({
    "date": six_months.strftime("%Y-%m-%d"),
    "event": "Meta de 6 Meses",
    "description": f"Telegram: {telegram_6m}, Discord: {discord_6m}, Twitter: {twitter_6m}, DAU: {dau_6m}"
})

# Add 12-month milestone
twelve_months = today + timedelta(days=365)
timeline_events.append({
    "date": twelve_months.strftime("%Y-%m-%d"),
    "event": "Meta de 12 Meses",
    "description": f"Telegram: {telegram_12m}, Discord: {discord_12m}, Twitter: {twitter_12m}, DAU: {dau_12m}"
})

# Add content calendar events
for entry in st.session_state.community["content_calendar"]:
    if entry["title"]:
        entry_date = datetime.strptime(entry["date"], "%Y-%m-%d")
        if entry_date > today:
            timeline_events.append({
                "date": entry["date"],
                "event": f"Conteúdo: {entry['title']}",
                "description": f"Tipo: {entry['content_type']}, Canais: {', '.join(entry['channels']) if entry['channels'] else 'Não especificado'}"
            })

# Create timeline visualization
if timeline_events:
    # Sort events by date
    sorted_events = sorted(timeline_events, key=lambda x: x["date"])
    
    # Create dataframe for visualization
    timeline_df = pd.DataFrame(sorted_events)
    timeline_df["date"] = pd.to_datetime(timeline_df["date"])
    
    # Create timeline chart
    fig = px.line_polar(
        r=[1] * len(timeline_df),
        theta=timeline_df["date"],
        line_close=True,
        title="Linha do Tempo da Comunidade"
    )
    
    # Configure hover text
    hovertext = []
    for _, row in timeline_df.iterrows():
        hovertext.append(f"Data: {row['date'].strftime('%d/%m/%Y')}<br>Evento: {row['event']}<br>{row['description']}")
    
    fig.add_trace(go.Scatterpolar(
        r=[1] * len(timeline_df),
        theta=timeline_df["date"],
        mode="markers",
        marker=dict(size=12, color="blue"),
        hoverinfo="text",
        hovertext=hovertext,
        name=""
    ))
    
    fig.update_layout(
        showlegend=False,
        polar=dict(
            radialaxis=dict(visible=False),
            angularaxis=dict(
                tickfont_size=10,
                rotation=90,
                direction="clockwise"
            )
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display timeline as table
    display_df = timeline_df.copy()
    display_df["date"] = display_df["date"].dt.strftime("%d/%m/%Y")
    display_df.columns = ["Data", "Evento", "Descrição"]
    
    st.dataframe(display_df, hide_index=True)