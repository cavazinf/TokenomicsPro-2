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
    page_title="Marketing & Crescimento | Tokenomics Lab",
    page_icon="📈",
    layout="wide"
)

# Sidebar
st.sidebar.title("Tokenomics Lab")
st.sidebar.image("https://cdn.jsdelivr.net/npm/cryptocurrency-icons@0.18.1/svg/icon/btc.svg", width=50)

# Main content
st.title("Marketing & Crescimento")
st.markdown("""
    Desenvolva estratégias de marketing e planeje o crescimento do seu projeto.
    Um plano de marketing bem elaborado é essencial para atrair usuários e investidores.
""")

# Check if model exists in session state
if 'model' not in st.session_state:
    st.warning("Você ainda não criou um modelo de tokenomics. Vá para a página de Simulação para criar um modelo primeiro.")
    
    # Button to go to simulation page
    if st.button("Ir para Simulação"):
        st.switch_page("pages/simulation.py")
        
    st.stop()

# Initialize marketing data in session state if not exists
if 'marketing' not in st.session_state:
    today = datetime.now()
    st.session_state.marketing = {
        "budget": 250000,
        "allocation": {
            "social_media": 30,
            "community": 20,
            "influencers": 15,
            "content": 10,
            "events": 10,
            "partnerships": 10,
            "ads": 5
        },
        "kpis": {
            "twitter_followers": 0,
            "discord_members": 0,
            "telegram_members": 0,
            "website_visitors": 0,
            "app_downloads": 0,
            "token_holders": 0
        },
        "growth_targets": {
            "month_3": {
                "twitter_followers": 5000,
                "discord_members": 3000,
                "telegram_members": 3000,
                "website_visitors": 10000,
                "app_downloads": 2000,
                "token_holders": 1000
            },
            "month_6": {
                "twitter_followers": 15000,
                "discord_members": 10000,
                "telegram_members": 8000,
                "website_visitors": 50000,
                "app_downloads": 10000,
                "token_holders": 5000
            },
            "month_12": {
                "twitter_followers": 50000,
                "discord_members": 25000,
                "telegram_members": 20000,
                "website_visitors": 200000,
                "app_downloads": 50000,
                "token_holders": 20000
            }
        },
        "marketing_channels": [],
        "content_strategy": [],
        "community_building": [],
        "milestones": [
            {
                "name": "Lançamento do Token",
                "date": (today + timedelta(days=90)).strftime("%Y-%m-%d"),
                "description": "Lançamento oficial do token em exchanges",
                "budget": 50000
            }
        ]
    }

# Marketing Configuration
st.header("Configuração de Marketing e Crescimento")

# Marketing Budget
st.subheader("Orçamento de Marketing")

marketing_budget = st.number_input(
    "Orçamento Total de Marketing (USD)",
    min_value=0,
    value=st.session_state.marketing["budget"],
    step=10000,
    help="Orçamento total de marketing para o projeto."
)

# Budget Allocation
st.subheader("Alocação de Orçamento")
st.markdown("Defina como você planeja distribuir seu orçamento de marketing entre diferentes canais.")

col1, col2 = st.columns(2)

with col1:
    social_media_pct = st.slider(
        "Mídias Sociais (%)",
        min_value=0,
        max_value=100,
        value=st.session_state.marketing["allocation"]["social_media"],
        help="Porcentagem do orçamento alocada para marketing em mídias sociais."
    )
    
    community_pct = st.slider(
        "Construção de Comunidade (%)",
        min_value=0,
        max_value=100,
        value=st.session_state.marketing["allocation"]["community"],
        help="Porcentagem do orçamento alocada para construção de comunidade."
    )
    
    influencers_pct = st.slider(
        "Influenciadores & KOLs (%)",
        min_value=0,
        max_value=100,
        value=st.session_state.marketing["allocation"]["influencers"],
        help="Porcentagem do orçamento alocada para parcerias com influenciadores e líderes de opinião."
    )
    
    content_pct = st.slider(
        "Criação de Conteúdo (%)",
        min_value=0,
        max_value=100,
        value=st.session_state.marketing["allocation"]["content"],
        help="Porcentagem do orçamento alocada para criação de conteúdo e marketing de conteúdo."
    )

with col2:
    events_pct = st.slider(
        "Eventos & Conferências (%)",
        min_value=0,
        max_value=100,
        value=st.session_state.marketing["allocation"]["events"],
        help="Porcentagem do orçamento alocada para participação em eventos e conferências."
    )
    
    partnerships_pct = st.slider(
        "Parcerias Estratégicas (%)",
        min_value=0,
        max_value=100,
        value=st.session_state.marketing["allocation"]["partnerships"],
        help="Porcentagem do orçamento alocada para desenvolvimento de parcerias estratégicas."
    )
    
    ads_pct = st.slider(
        "Publicidade Paga (%)",
        min_value=0,
        max_value=100,
        value=st.session_state.marketing["allocation"]["ads"],
        help="Porcentagem do orçamento alocada para campanhas de publicidade paga."
    )

# Calculate total allocation
total_allocation = social_media_pct + community_pct + influencers_pct + content_pct + events_pct + partnerships_pct + ads_pct

if total_allocation != 100:
    st.warning(f"A alocação total é {total_allocation}%. O total deve ser 100%.")

# KPIs
st.subheader("Indicadores-Chave de Desempenho (KPIs)")
st.markdown("Configure seus KPIs atuais e metas de crescimento.")

# Current KPIs
st.markdown("**KPIs Atuais**")
col1, col2, col3 = st.columns(3)

with col1:
    twitter_followers = st.number_input(
        "Seguidores no Twitter",
        min_value=0,
        value=st.session_state.marketing["kpis"]["twitter_followers"],
        step=100,
        help="Número atual de seguidores no Twitter."
    )
    
    discord_members = st.number_input(
        "Membros no Discord",
        min_value=0,
        value=st.session_state.marketing["kpis"]["discord_members"],
        step=100,
        help="Número atual de membros no servidor Discord."
    )

with col2:
    telegram_members = st.number_input(
        "Membros no Telegram",
        min_value=0,
        value=st.session_state.marketing["kpis"]["telegram_members"],
        step=100,
        help="Número atual de membros no canal do Telegram."
    )
    
    website_visitors = st.number_input(
        "Visitantes Mensais do Site",
        min_value=0,
        value=st.session_state.marketing["kpis"]["website_visitors"],
        step=100,
        help="Número atual de visitantes mensais do site."
    )

with col3:
    app_downloads = st.number_input(
        "Downloads do Aplicativo",
        min_value=0,
        value=st.session_state.marketing["kpis"]["app_downloads"],
        step=100,
        help="Número atual de downloads do aplicativo."
    )
    
    token_holders = st.number_input(
        "Detentores do Token",
        min_value=0,
        value=st.session_state.marketing["kpis"]["token_holders"],
        step=100,
        help="Número atual de detentores do token."
    )

# Growth Targets
st.markdown("**Metas de Crescimento**")

tab1, tab2, tab3 = st.tabs(["3 Meses", "6 Meses", "12 Meses"])

with tab1:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        twitter_3m = st.number_input(
            "Meta de Seguidores no Twitter (3m)",
            min_value=0,
            value=st.session_state.marketing["growth_targets"]["month_3"]["twitter_followers"],
            step=500,
            help="Meta de seguidores no Twitter para 3 meses."
        )
        
        discord_3m = st.number_input(
            "Meta de Membros no Discord (3m)",
            min_value=0,
            value=st.session_state.marketing["growth_targets"]["month_3"]["discord_members"],
            step=500,
            help="Meta de membros no Discord para 3 meses."
        )
    
    with col2:
        telegram_3m = st.number_input(
            "Meta de Membros no Telegram (3m)",
            min_value=0,
            value=st.session_state.marketing["growth_targets"]["month_3"]["telegram_members"],
            step=500,
            help="Meta de membros no Telegram para 3 meses."
        )
        
        website_3m = st.number_input(
            "Meta de Visitantes do Site (3m)",
            min_value=0,
            value=st.session_state.marketing["growth_targets"]["month_3"]["website_visitors"],
            step=1000,
            help="Meta de visitantes mensais do site para 3 meses."
        )
    
    with col3:
        app_3m = st.number_input(
            "Meta de Downloads do App (3m)",
            min_value=0,
            value=st.session_state.marketing["growth_targets"]["month_3"]["app_downloads"],
            step=500,
            help="Meta de downloads do aplicativo para 3 meses."
        )
        
        holders_3m = st.number_input(
            "Meta de Detentores do Token (3m)",
            min_value=0,
            value=st.session_state.marketing["growth_targets"]["month_3"]["token_holders"],
            step=500,
            help="Meta de detentores do token para 3 meses."
        )

with tab2:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        twitter_6m = st.number_input(
            "Meta de Seguidores no Twitter (6m)",
            min_value=0,
            value=st.session_state.marketing["growth_targets"]["month_6"]["twitter_followers"],
            step=1000,
            help="Meta de seguidores no Twitter para 6 meses."
        )
        
        discord_6m = st.number_input(
            "Meta de Membros no Discord (6m)",
            min_value=0,
            value=st.session_state.marketing["growth_targets"]["month_6"]["discord_members"],
            step=1000,
            help="Meta de membros no Discord para 6 meses."
        )
    
    with col2:
        telegram_6m = st.number_input(
            "Meta de Membros no Telegram (6m)",
            min_value=0,
            value=st.session_state.marketing["growth_targets"]["month_6"]["telegram_members"],
            step=1000,
            help="Meta de membros no Telegram para 6 meses."
        )
        
        website_6m = st.number_input(
            "Meta de Visitantes do Site (6m)",
            min_value=0,
            value=st.session_state.marketing["growth_targets"]["month_6"]["website_visitors"],
            step=5000,
            help="Meta de visitantes mensais do site para 6 meses."
        )
    
    with col3:
        app_6m = st.number_input(
            "Meta de Downloads do App (6m)",
            min_value=0,
            value=st.session_state.marketing["growth_targets"]["month_6"]["app_downloads"],
            step=1000,
            help="Meta de downloads do aplicativo para 6 meses."
        )
        
        holders_6m = st.number_input(
            "Meta de Detentores do Token (6m)",
            min_value=0,
            value=st.session_state.marketing["growth_targets"]["month_6"]["token_holders"],
            step=1000,
            help="Meta de detentores do token para 6 meses."
        )

with tab3:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        twitter_12m = st.number_input(
            "Meta de Seguidores no Twitter (12m)",
            min_value=0,
            value=st.session_state.marketing["growth_targets"]["month_12"]["twitter_followers"],
            step=5000,
            help="Meta de seguidores no Twitter para 12 meses."
        )
        
        discord_12m = st.number_input(
            "Meta de Membros no Discord (12m)",
            min_value=0,
            value=st.session_state.marketing["growth_targets"]["month_12"]["discord_members"],
            step=5000,
            help="Meta de membros no Discord para 12 meses."
        )
    
    with col2:
        telegram_12m = st.number_input(
            "Meta de Membros no Telegram (12m)",
            min_value=0,
            value=st.session_state.marketing["growth_targets"]["month_12"]["telegram_members"],
            step=5000,
            help="Meta de membros no Telegram para 12 meses."
        )
        
        website_12m = st.number_input(
            "Meta de Visitantes do Site (12m)",
            min_value=0,
            value=st.session_state.marketing["growth_targets"]["month_12"]["website_visitors"],
            step=10000,
            help="Meta de visitantes mensais do site para 12 meses."
        )
    
    with col3:
        app_12m = st.number_input(
            "Meta de Downloads do App (12m)",
            min_value=0,
            value=st.session_state.marketing["growth_targets"]["month_12"]["app_downloads"],
            step=5000,
            help="Meta de downloads do aplicativo para 12 meses."
        )
        
        holders_12m = st.number_input(
            "Meta de Detentores do Token (12m)",
            min_value=0,
            value=st.session_state.marketing["growth_targets"]["month_12"]["token_holders"],
            step=5000,
            help="Meta de detentores do token para 12 meses."
        )

# Marketing Channels & Strategy
st.subheader("Canais e Estratégias de Marketing")

# Marketing Channels
st.markdown("**Canais de Marketing**")
st.markdown("Adicione os canais de marketing que você planeja utilizar.")

# Dynamic form for marketing channels
if st.button("Adicionar Canal de Marketing"):
    st.session_state.marketing["marketing_channels"].append({
        "name": "",
        "platform": "Twitter",
        "target_audience": "",
        "strategy": "",
        "budget_percentage": 0.0
    })

# Display existing marketing channels
channels_to_remove = []

for i, channel in enumerate(st.session_state.marketing["marketing_channels"]):
    with st.expander(f"Canal {i+1}: {channel['name'] or 'Novo Canal'}"):
        col1, col2 = st.columns(2)
        
        with col1:
            channel["name"] = st.text_input(
                "Nome do Canal", 
                value=channel["name"],
                key=f"channel_name_{i}"
            )
            
            channel["platform"] = st.selectbox(
                "Plataforma", 
                ["Twitter", "Discord", "Telegram", "YouTube", "TikTok", "Instagram", "LinkedIn", "Reddit", "Facebook", "Medium", "Blog", "Podcast", "Email", "Outro"],
                index=["Twitter", "Discord", "Telegram", "YouTube", "TikTok", "Instagram", "LinkedIn", "Reddit", "Facebook", "Medium", "Blog", "Podcast", "Email", "Outro"].index(channel["platform"]) if channel["platform"] in ["Twitter", "Discord", "Telegram", "YouTube", "TikTok", "Instagram", "LinkedIn", "Reddit", "Facebook", "Medium", "Blog", "Podcast", "Email", "Outro"] else 0,
                key=f"channel_platform_{i}"
            )
            
            channel["target_audience"] = st.text_input(
                "Público-Alvo", 
                value=channel["target_audience"],
                key=f"channel_audience_{i}"
            )
            
        with col2:
            channel["strategy"] = st.text_area(
                "Estratégia", 
                value=channel["strategy"],
                height=100,
                key=f"channel_strategy_{i}"
            )
            
            channel["budget_percentage"] = st.slider(
                "% do Orçamento", 
                min_value=0.0, 
                max_value=100.0, 
                value=channel["budget_percentage"],
                step=0.5,
                key=f"channel_budget_{i}"
            )
        
        if st.button("Remover Canal", key=f"remove_channel_{i}"):
            channels_to_remove.append(i)

# Remove channels marked for removal
if channels_to_remove:
    st.session_state.marketing["marketing_channels"] = [channel for i, channel in enumerate(st.session_state.marketing["marketing_channels"]) 
                                if i not in channels_to_remove]

# Content Strategy
st.markdown("**Estratégia de Conteúdo**")
st.markdown("Defina sua estratégia de criação e distribuição de conteúdo.")

content_strategy = st.text_area(
    "Estratégia de Conteúdo",
    value="\n".join(st.session_state.marketing.get("content_strategy", [])),
    height=150,
    help="Liste os principais elementos da sua estratégia de conteúdo, um por linha."
)

# Community Building
st.markdown("**Construção de Comunidade**")
st.markdown("Defina suas estratégias para construir e engajar sua comunidade.")

community_building = st.text_area(
    "Estratégias de Construção de Comunidade",
    value="\n".join(st.session_state.marketing.get("community_building", [])),
    height=150,
    help="Liste suas estratégias para construção de comunidade, uma por linha."
)

# Marketing Milestones
st.subheader("Marcos de Marketing")
st.markdown("Defina marcos importantes para o seu plano de marketing.")

# Dynamic form for milestones
if st.button("Adicionar Marco"):
    today = datetime.now()
    st.session_state.marketing["milestones"].append({
        "name": "",
        "date": today.strftime("%Y-%m-%d"),
        "description": "",
        "budget": 0
    })

# Display existing milestones
milestones_to_remove = []

for i, milestone in enumerate(st.session_state.marketing["milestones"]):
    with st.expander(f"Marco {i+1}: {milestone['name'] or 'Novo Marco'}"):
        col1, col2 = st.columns(2)
        
        with col1:
            milestone["name"] = st.text_input(
                "Nome do Marco", 
                value=milestone["name"],
                key=f"milestone_name_{i}"
            )
            
            milestone_date = st.date_input(
                "Data", 
                value=datetime.strptime(milestone["date"], "%Y-%m-%d") if isinstance(milestone["date"], str) else milestone["date"],
                key=f"milestone_date_{i}"
            )
            milestone["date"] = milestone_date.strftime("%Y-%m-%d")
            
        with col2:
            milestone["description"] = st.text_area(
                "Descrição", 
                value=milestone["description"],
                height=100,
                key=f"milestone_desc_{i}"
            )
            
            milestone["budget"] = st.number_input(
                "Orçamento ($)", 
                min_value=0, 
                value=milestone["budget"],
                step=1000,
                key=f"milestone_budget_{i}"
            )
        
        if st.button("Remover Marco", key=f"remove_milestone_{i}"):
            milestones_to_remove.append(i)

# Remove milestones marked for removal
if milestones_to_remove:
    st.session_state.marketing["milestones"] = [milestone for i, milestone in enumerate(st.session_state.marketing["milestones"]) 
                                if i not in milestones_to_remove]

# Save button
if st.button("Salvar Plano de Marketing", type="primary"):
    # Update marketing data in session state
    st.session_state.marketing["budget"] = marketing_budget
    st.session_state.marketing["allocation"] = {
        "social_media": social_media_pct,
        "community": community_pct,
        "influencers": influencers_pct,
        "content": content_pct,
        "events": events_pct,
        "partnerships": partnerships_pct,
        "ads": ads_pct
    }
    
    st.session_state.marketing["kpis"] = {
        "twitter_followers": twitter_followers,
        "discord_members": discord_members,
        "telegram_members": telegram_members,
        "website_visitors": website_visitors,
        "app_downloads": app_downloads,
        "token_holders": token_holders
    }
    
    st.session_state.marketing["growth_targets"] = {
        "month_3": {
            "twitter_followers": twitter_3m,
            "discord_members": discord_3m,
            "telegram_members": telegram_3m,
            "website_visitors": website_3m,
            "app_downloads": app_3m,
            "token_holders": holders_3m
        },
        "month_6": {
            "twitter_followers": twitter_6m,
            "discord_members": discord_6m,
            "telegram_members": telegram_6m,
            "website_visitors": website_6m,
            "app_downloads": app_6m,
            "token_holders": holders_6m
        },
        "month_12": {
            "twitter_followers": twitter_12m,
            "discord_members": discord_12m,
            "telegram_members": telegram_12m,
            "website_visitors": website_12m,
            "app_downloads": app_12m,
            "token_holders": holders_12m
        }
    }
    
    st.session_state.marketing["content_strategy"] = [strategy.strip() for strategy in content_strategy.split("\n") if strategy.strip()]
    st.session_state.marketing["community_building"] = [strategy.strip() for strategy in community_building.split("\n") if strategy.strip()]
    
    st.success("Plano de marketing salvo com sucesso!")

# Visualizations
st.header("Visualizações do Plano de Marketing")

# Budget Allocation
if total_allocation > 0:
    st.subheader("Alocação de Orçamento")
    
    allocation_labels = [
        "Mídias Sociais", 
        "Comunidade", 
        "Influenciadores", 
        "Conteúdo",
        "Eventos",
        "Parcerias",
        "Anúncios"
    ]
    
    allocation_values = [
        social_media_pct,
        community_pct,
        influencers_pct,
        content_pct,
        events_pct,
        partnerships_pct,
        ads_pct
    ]
    
    # Create pie chart
    fig = px.pie(
        values=allocation_values,
        names=allocation_labels,
        title=f"Alocação do Orçamento de Marketing (${marketing_budget:,})",
        color_discrete_sequence=px.colors.sequential.Blues_r,
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display budget amounts
    st.markdown("**Valores Alocados por Categoria:**")
    
    budget_data = []
    for label, pct in zip(allocation_labels, allocation_values):
        amount = marketing_budget * (pct / 100)
        budget_data.append({"Categoria": label, "Porcentagem": pct, "Valor ($)": amount})
    
    budget_df = pd.DataFrame(budget_data)
    st.dataframe(budget_df, hide_index=True)

# Growth Targets Visualization
st.subheader("Metas de Crescimento")

# Prepare data for visualization
growth_metrics = ["Seguidores no Twitter", "Membros no Discord", "Membros no Telegram", 
                  "Visitantes Mensais", "Downloads do App", "Detentores do Token"]

current_values = [
    twitter_followers,
    discord_members,
    telegram_members,
    website_visitors,
    app_downloads,
    token_holders
]

month_3_values = [
    twitter_3m,
    discord_3m,
    telegram_3m,
    website_3m,
    app_3m,
    holders_3m
]

month_6_values = [
    twitter_6m,
    discord_6m,
    telegram_6m,
    website_6m,
    app_6m,
    holders_6m
]

month_12_values = [
    twitter_12m,
    discord_12m,
    telegram_12m,
    website_12m,
    app_12m,
    holders_12m
]

# Create a stacked bar chart for each metric
for i, metric in enumerate(growth_metrics):
    col1, col2 = st.columns([3, 1])
    
    with col1:
        fig = go.Figure()
        
        periods = ["Atual", "3 Meses", "6 Meses", "12 Meses"]
        values = [current_values[i], month_3_values[i], month_6_values[i], month_12_values[i]]
        
        # Set color scale based on growth
        colors = ['#c5e5ff', '#83c9ff', '#0068c9', '#004080']
        
        fig.add_trace(go.Bar(
            x=periods,
            y=values,
            text=values,
            textposition='auto',
            marker_color=colors
        ))
        
        fig.update_layout(
            title=f"Crescimento projetado: {metric}",
            xaxis_title="Período",
            yaxis_title="Valor",
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Calculate growth percentages
        if current_values[i] > 0:
            growth_3m = ((month_3_values[i] / current_values[i]) - 1) * 100
            growth_6m = ((month_6_values[i] / current_values[i]) - 1) * 100
            growth_12m = ((month_12_values[i] / current_values[i]) - 1) * 100
            
            st.markdown(f"**Crescimento projetado:**")
            st.markdown(f"3 meses: **{growth_3m:.1f}%**")
            st.markdown(f"6 meses: **{growth_6m:.1f}%**")
            st.markdown(f"12 meses: **{growth_12m:.1f}%**")
        else:
            st.markdown("Defina valores atuais para calcular o crescimento percentual.")

# Timeline of Milestones
if st.session_state.marketing["milestones"]:
    st.subheader("Linha do Tempo de Marcos de Marketing")
    
    # Sort milestones by date
    sorted_milestones = sorted(st.session_state.marketing["milestones"], 
                             key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"))
    
    milestone_names = [m["name"] for m in sorted_milestones]
    milestone_dates = [datetime.strptime(m["date"], "%Y-%m-%d") for m in sorted_milestones]
    milestone_budgets = [m["budget"] for m in sorted_milestones]
    
    # Criar dataframe para timeline
    timeline_df = pd.DataFrame({
        'Start': milestone_dates,
        'Milestone': milestone_names,
        'Budget': milestone_budgets,
        # Adicionar end date (aqui colocamos +30 dias após a data de início para visualização)
        'End': [date + timedelta(days=30) for date in milestone_dates]
    })
    
    fig = px.timeline(
        timeline_df,
        x_start='Start',
        x_end='End',
        y='Milestone',
        color='Budget',
        color_continuous_scale=px.colors.sequential.Blues,
        labels={"color": "Orçamento ($)"}
    )
    
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(
        title="Linha do Tempo de Marcos de Marketing",
        xaxis_title="Data",
        yaxis_title="Marco",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display milestone details
    st.markdown("**Detalhes dos Marcos:**")
    
    for milestone in sorted_milestones:
        with st.expander(f"{milestone['name']} - {milestone['date']}"):
            st.markdown(f"**Descrição:** {milestone['description']}")
            st.markdown(f"**Orçamento:** ${milestone['budget']:,}")

# Marketing Channels Analysis
if st.session_state.marketing["marketing_channels"]:
    st.subheader("Análise de Canais de Marketing")
    
    # Prepare data for visualization
    channel_names = [c["name"] for c in st.session_state.marketing["marketing_channels"]]
    channel_platforms = [c["platform"] for c in st.session_state.marketing["marketing_channels"]]
    channel_budgets = [c["budget_percentage"] * marketing_budget / 100 for c in st.session_state.marketing["marketing_channels"]]
    
    # Create a horizontal bar chart
    fig = px.bar(
        y=channel_names,
        x=channel_budgets,
        color=channel_platforms,
        labels={"y": "Canal", "x": "Orçamento ($)"},
        title="Alocação de Orçamento por Canal",
        orientation='h'
    )
    
    fig.update_layout(height=400)
    
    st.plotly_chart(fig, use_container_width=True)

# Community and Content Strategy
col1, col2 = st.columns(2)

with col1:
    if st.session_state.marketing["content_strategy"]:
        st.subheader("Estratégia de Conteúdo")
        
        for i, strategy in enumerate(st.session_state.marketing["content_strategy"]):
            st.markdown(f"**{i+1}.** {strategy}")

with col2:
    if st.session_state.marketing["community_building"]:
        st.subheader("Estratégia de Comunidade")
        
        for i, strategy in enumerate(st.session_state.marketing["community_building"]):
            st.markdown(f"**{i+1}.** {strategy}")