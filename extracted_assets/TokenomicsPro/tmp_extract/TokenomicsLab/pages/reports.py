import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from io import BytesIO
import base64
from datetime import datetime
import time

# Import local modules
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.tokenomics import TokenomicsModel, create_model_from_dict
from utils.export import generate_pdf_report, get_download_link

st.set_page_config(
    page_title="Relatórios | Tokenomics Lab",
    page_icon="📝",
    layout="wide"
)

# Sidebar
st.sidebar.title("Tokenomics Lab")
st.sidebar.image("https://cdn.jsdelivr.net/npm/cryptocurrency-icons@0.18.1/svg/icon/btc.svg", width=50)

# Main content
st.title("Relatórios de Tokenomics")
st.markdown("""
    Gere relatórios detalhados sobre seu modelo de tokenomics para compartilhar com
    investidores, equipe e comunidade.
""")

# Check if model exists in session state
if 'model' not in st.session_state or 'simulation_result' not in st.session_state:
    st.warning("Você ainda não simulou nenhum modelo. Vá para a página de Simulação para criar um modelo primeiro.")
    
    # Button to go to simulation page
    if st.button("Ir para Simulação"):
        st.switch_page("pages/simulation.py")
        
    st.stop()

# Get model and simulation result from session state
model = st.session_state.model
df = st.session_state.simulation_result

# Report configuration
st.header("Configuração do Relatório")

col1, col2 = st.columns(2)

with col1:
    report_title = st.text_input(
        "Título do Relatório", 
        value=f"Análise de Tokenomics: {model.name if model else 'Meu Projeto'}",
        help="Título principal que aparecerá no relatório."
    )
    
    author = st.text_input(
        "Autor", 
        value="TokenomicsLab",
        help="Nome do autor ou organização que está gerando o relatório."
    )

with col2:
    report_date = st.date_input(
        "Data do Relatório",
        value=datetime.now().date(),
        help="Data em que o relatório está sendo gerado."
    )
    
    include_disclaimer = st.checkbox(
        "Incluir Aviso Legal", 
        value=True,
        help="Adicione um aviso legal padrão no final do relatório."
    )

# Report sections
st.subheader("Seções do Relatório")

include_overview = st.checkbox("Visão Geral do Modelo", value=True)
include_distribution = st.checkbox("Distribuição de Tokens", value=True)
include_vesting = st.checkbox("Cronograma de Vesting", value=True)
include_price = st.checkbox("Simulação de Preço", value=True)
include_metrics = st.checkbox("Métricas Específicas", value=True)
include_recommendations = st.checkbox("Recomendações", value=False)

# Custom notes
custom_notes = st.text_area(
    "Notas Adicionais",
    value="",
    height=100,
    help="Adicione notas ou comentários personalizados que serão incluídos no relatório."
)

# Report preview
st.header("Prévia do Relatório")

# Prepare preview data
preview_tabs = st.tabs(["Visão Geral", "Gráficos", "Dados"])

with preview_tabs[0]:
    st.subheader(report_title)
    st.markdown(f"**Autor:** {author}")
    st.markdown(f"**Data:** {report_date}")
    
    st.markdown("### Resumo Executivo")
    
    # Model type
    model_type = "Básico"
    if hasattr(model, 'initial_users'):
        model_type = "Utility Token"
    elif hasattr(model, 'initial_staking_rate'):
        model_type = "Governance Token"
    
    # Key metrics
    latest_price = df['Price'].iloc[-1]
    initial_price = df['Price'].iloc[0]
    price_change = ((latest_price - initial_price) / initial_price) * 100
    
    latest_supply = df['Circulating_Supply'].iloc[-1]
    total_supply = model.total_supply
    supply_percent = (latest_supply / total_supply) * 100
    
    latest_mcap = df['Market_Cap'].iloc[-1]
    
    st.markdown(f"""
    Este relatório apresenta uma análise detalhada do modelo de tokenomics para **{model.name}**.
    O modelo é baseado em um token do tipo **{model_type}** com uma oferta total de **{total_supply:,} tokens**.
    
    **Principais métricas após {df['Month'].max()} meses:**
    - Preço do Token: **${latest_price:.4f}** ({price_change:.1f}% desde o início)
    - Oferta em Circulação: **{latest_supply:,.0f} tokens** ({supply_percent:.1f}% do total)
    - Market Cap Projetado: **${latest_mcap:,.2f}**
    """)
    
    if include_overview:
        st.markdown("### Visão Geral do Modelo")
        
        st.markdown(f"""
        O modelo **{model.name}** foi configurado com as seguintes características:
        
        - **Tipo de Token:** {model_type}
        - **Oferta Total:** {total_supply:,} tokens
        - **Número de Categorias de Distribuição:** {len(model.distribution)}
        """)
        
        if hasattr(model, 'initial_users'):
            st.markdown(f"""
            - **Usuários Iniciais:** {model.initial_users:,}
            - **Taxa de Crescimento de Usuários:** {model.user_growth_rate:.1%} ao mês
            """)
        
        if hasattr(model, 'initial_staking_rate'):
            st.markdown(f"""
            - **Taxa Inicial de Staking:** {model.initial_staking_rate:.1%}
            - **APY de Staking:** {model.staking_apy:.1%}
            """)
    
    if include_distribution:
        st.markdown("### Distribuição de Tokens")
        
        st.markdown("A alocação de tokens foi distribuída entre as seguintes categorias:")
        
        for category, percentage in model.distribution.items():
            st.markdown(f"- **{category}:** {percentage:.1f}%")
    
    if include_vesting:
        st.markdown("### Cronograma de Vesting")
        
        if model.vesting_schedules:
            for category, schedule in model.vesting_schedules.items():
                st.markdown(f"**{category}:**")
                
                for month, percentage in schedule:
                    st.markdown(f"- Mês {month}: {percentage:.1f}%")
        else:
            st.markdown("Não há cronogramas de vesting definidos para este modelo.")
    
    if custom_notes:
        st.markdown("### Notas Adicionais")
        st.markdown(custom_notes)
    
    if include_disclaimer:
        st.markdown("### Aviso Legal")
        st.markdown("""
        *Este relatório é apenas para fins informativos e não constitui aconselhamento financeiro ou de investimento. 
        As projeções e simulações são baseadas em modelos teóricos e não garantem resultados futuros. 
        Todos os investimentos envolvem riscos e os leitores devem realizar sua própria pesquisa e consultar profissionais qualificados antes de tomar decisões financeiras.*
        """)

with preview_tabs[1]:
    if include_distribution:
        st.subheader("Distribuição de Tokens")
        
        # Distribution pie chart
        fig = px.pie(
            values=list(model.distribution.values()),
            names=list(model.distribution.keys()),
            title="Alocação de Tokens",
            color_discrete_sequence=px.colors.sequential.Blues_r,
            hole=0.4,
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    if include_vesting and model.vesting_schedules:
        st.subheader("Cronograma de Vesting")
        
        # Prepare vesting data
        vesting_data = []
        for category, schedule in model.vesting_schedules.items():
            category_total = model.distribution[category] * model.total_supply / 100
            
            cumulative_pct = 0
            for month, pct in schedule:
                cumulative_pct += pct
                vesting_data.append({
                    'Categoria': category,
                    'Mês': month,
                    'Porcentagem Acumulada': cumulative_pct,
                    'Tokens Liberados': category_total * cumulative_pct / 100
                })

        if vesting_data:
            vesting_df = pd.DataFrame(vesting_data)
            
            # Create line chart
            fig = px.line(
                vesting_df, 
                x='Mês', 
                y='Porcentagem Acumulada', 
                color='Categoria',
                title="Cronograma de Vesting (% Acumulada)",
                labels={'Porcentagem Acumulada': '% Acumulada'},
                color_discrete_sequence=px.colors.qualitative.Set1
            )
            
            fig.update_layout(
                yaxis=dict(ticksuffix="%"),
                hovermode="x unified"
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    if include_price:
        st.subheader("Simulação de Preço")
        
        # Price and supply chart
        fig = make_subplots(
            rows=2, 
            cols=1, 
            shared_xaxes=True, 
            vertical_spacing=0.1,
            subplot_titles=("Preço do Token ($)", "Oferta Circulante de Tokens")
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
            height=500,
            hovermode="x unified",
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )

        # Update y-axes
        fig.update_yaxes(title_text="Preço ($)", row=1, col=1)
        fig.update_yaxes(title_text="Tokens", row=2, col=1)
        fig.update_xaxes(title_text="Mês", row=2, col=1)

        st.plotly_chart(fig, use_container_width=True)
        
        # Market cap chart
        fig = px.area(
            df, 
            x='Month', 
            y='Market_Cap',
            title="Evolução do Market Cap",
            labels={'Month': 'Mês', 'Market_Cap': 'Market Cap ($)'},
            color_discrete_sequence=['#83c9ff']
        )

        fig.update_layout(
            hovermode="x unified"
        )

        st.plotly_chart(fig, use_container_width=True)
    
    if include_metrics:
        st.subheader("Métricas Específicas")
        
        if 'Users' in df.columns and 'Token_Demand' in df.columns:
            # Utility token metrics
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.line(
                    df, 
                    x='Month', 
                    y='Users',
                    title="Crescimento de Usuários",
                    labels={'Month': 'Mês', 'Users': 'Usuários'},
                    color_discrete_sequence=['#0068c9']
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.line(
                    df, 
                    x='Month', 
                    y='Token_Demand',
                    title="Demanda de Tokens",
                    labels={'Month': 'Mês', 'Token_Demand': 'Demanda de Tokens'},
                    color_discrete_sequence=['#ff9e0a']
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Supply vs Demand
            fig = px.line(
                df, 
                x='Month', 
                y=['Circulating_Supply', 'Token_Demand'],
                title="Oferta vs Demanda de Tokens",
                labels={'Month': 'Mês', 'value': 'Tokens', 'variable': 'Métrica'},
                color_discrete_map={
                    'Circulating_Supply': '#0068c9',
                    'Token_Demand': '#ff9e0a'
                }
            )
            
            fig.update_layout(
                hovermode="x unified"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        elif 'Staking_Rate' in df.columns and 'Staked_Tokens' in df.columns:
            # Governance token metrics
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.line(
                    df, 
                    x='Month', 
                    y='Staking_Rate',
                    title="Taxa de Staking",
                    labels={'Month': 'Mês', 'Staking_Rate': 'Taxa de Staking'},
                    color_discrete_sequence=['#0068c9']
                )
                
                fig.update_layout(
                    yaxis=dict(tickformat=".0%")
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.line(
                    df, 
                    x='Month', 
                    y=['Staked_Tokens', 'Liquid_Tokens'],
                    title="Tokens em Staking vs Tokens Líquidos",
                    labels={'Month': 'Mês', 'value': 'Tokens', 'variable': 'Tipo'},
                    color_discrete_map={
                        'Staked_Tokens': '#0068c9',
                        'Liquid_Tokens': '#ff9e0a'
                    }
                )
                
                fig.update_layout(
                    hovermode="x unified"
                )
                
                st.plotly_chart(fig, use_container_width=True)

with preview_tabs[2]:
    st.subheader("Dados da Simulação")
    st.dataframe(df)

# Export options
st.header("Exportar Relatório")

col1, col2 = st.columns(2)

with col1:
    export_format = st.selectbox(
        "Formato de Exportação",
        ["HTML", "PDF", "CSV (apenas dados)"]
    )

# Generate report button
if st.button("Gerar Relatório", type="primary"):
    with st.spinner("Gerando relatório..."):
        # Export based on selected format
        if export_format == "HTML":
            # Generate HTML report
            # Placeholder for actual HTML generation
            
            # Use matplotlib for static charts
            # Distribution pie chart
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.pie(
                list(model.distribution.values()),
                labels=list(model.distribution.keys()),
                autopct='%1.1f%%',
                startangle=90,
                wedgeprops={'edgecolor': 'white'}
            )
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
            plt.title("Distribuição de Tokens")
            
            # Save to BytesIO
            buf = BytesIO()
            plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
            plt.close(fig)
            
            # Encode the image
            distribution_img = base64.b64encode(buf.getvalue()).decode('utf-8')
            
            # Create HTML content
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>{report_title}</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
                    h1 {{ color: #0068c9; }}
                    h2 {{ color: #444; margin-top: 30px; border-bottom: 1px solid #ddd; padding-bottom: 10px; }}
                    .header {{ margin-bottom: 30px; }}
                    .footer {{ margin-top: 50px; font-size: 0.8em; color: #777; border-top: 1px solid #ddd; padding-top: 20px; }}
                    .metrics {{ display: flex; justify-content: space-between; margin: 20px 0; }}
                    .metric {{ background: #f5f7fa; padding: 15px; border-radius: 5px; width: 30%; }}
                    .metric h3 {{ margin: 0; color: #555; font-size: 1em; }}
                    .metric p {{ margin: 5px 0 0 0; font-size: 1.4em; font-weight: bold; color: #0068c9; }}
                    .chart {{ margin: 30px 0; text-align: center; }}
                    .chart img {{ max-width: 100%; }}
                    table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                    th, td {{ text-align: left; padding: 12px; }}
                    th {{ background-color: #0068c9; color: white; }}
                    tr:nth-child(even) {{ background-color: #f5f7fa; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>{report_title}</h1>
                    <p><strong>Autor:</strong> {author} | <strong>Data:</strong> {report_date}</p>
                </div>
                
                <h2>Resumo Executivo</h2>
                <p>
                    Este relatório apresenta uma análise detalhada do modelo de tokenomics para <strong>{model.name}</strong>.
                    O modelo é baseado em um token do tipo <strong>{model_type}</strong> com uma oferta total de <strong>{total_supply:,} tokens</strong>.
                </p>
                
                <div class="metrics">
                    <div class="metric">
                        <h3>Preço do Token</h3>
                        <p>${latest_price:.4f}</p>
                        <span>({price_change:.1f}% desde o início)</span>
                    </div>
                    <div class="metric">
                        <h3>Oferta em Circulação</h3>
                        <p>{latest_supply:,.0f}</p>
                        <span>({supply_percent:.1f}% do total)</span>
                    </div>
                    <div class="metric">
                        <h3>Market Cap Projetado</h3>
                        <p>${latest_mcap:,.2f}</p>
                    </div>
                </div>
            """
            
            if include_overview:
                html_content += f"""
                <h2>Visão Geral do Modelo</h2>
                <p>
                    O modelo <strong>{model.name}</strong> foi configurado com as seguintes características:
                </p>
                <ul>
                    <li><strong>Tipo de Token:</strong> {model_type}</li>
                    <li><strong>Oferta Total:</strong> {total_supply:,} tokens</li>
                    <li><strong>Número de Categorias de Distribuição:</strong> {len(model.distribution)}</li>
                """
                
                if hasattr(model, 'initial_users'):
                    html_content += f"""
                    <li><strong>Usuários Iniciais:</strong> {model.initial_users:,}</li>
                    <li><strong>Taxa de Crescimento de Usuários:</strong> {model.user_growth_rate:.1%} ao mês</li>
                    """
                
                if hasattr(model, 'initial_staking_rate'):
                    html_content += f"""
                    <li><strong>Taxa Inicial de Staking:</strong> {model.initial_staking_rate:.1%}</li>
                    <li><strong>APY de Staking:</strong> {model.staking_apy:.1%}</li>
                    """
                
                html_content += """
                </ul>
                """
            
            if include_distribution:
                html_content += f"""
                <h2>Distribuição de Tokens</h2>
                <p>A alocação de tokens foi distribuída entre as seguintes categorias:</p>
                <ul>
                """
                
                for category, percentage in model.distribution.items():
                    html_content += f"<li><strong>{category}:</strong> {percentage:.1f}%</li>\n"
                
                html_content += """
                </ul>
                
                <div class="chart">
                    <img src="data:image/png;base64,{}" alt="Distribuição de Tokens">
                </div>
                """.format(distribution_img)
            
            if include_vesting and model.vesting_schedules:
                html_content += """
                <h2>Cronograma de Vesting</h2>
                <table>
                    <tr>
                        <th>Categoria</th>
                        <th>Mês</th>
                        <th>Porcentagem</th>
                    </tr>
                """
                
                for category, schedule in model.vesting_schedules.items():
                    for month, percentage in schedule:
                        html_content += f"""
                        <tr>
                            <td>{category}</td>
                            <td>{month}</td>
                            <td>{percentage:.1f}%</td>
                        </tr>
                        """
                
                html_content += """
                </table>
                """
            
            if include_price:
                # Create price chart
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.plot(df['Month'], df['Price'], 'b-', linewidth=2)
                ax.set_title('Evolução do Preço do Token')
                ax.set_xlabel('Mês')
                ax.set_ylabel('Preço ($)')
                ax.grid(True, linestyle='--', alpha=0.7)
                
                # Save to BytesIO
                buf = BytesIO()
                plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
                plt.close(fig)
                
                # Encode the image
                price_img = base64.b64encode(buf.getvalue()).decode('utf-8')
                
                # Create market cap chart
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.fill_between(df['Month'], df['Market_Cap'], alpha=0.5, color='blue')
                ax.plot(df['Month'], df['Market_Cap'], 'b-', linewidth=2)
                ax.set_title('Evolução do Market Cap')
                ax.set_xlabel('Mês')
                ax.set_ylabel('Market Cap ($)')
                ax.grid(True, linestyle='--', alpha=0.7)
                
                # Save to BytesIO
                buf = BytesIO()
                plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
                plt.close(fig)
                
                # Encode the image
                mcap_img = base64.b64encode(buf.getvalue()).decode('utf-8')
                
                html_content += f"""
                <h2>Simulação de Preço</h2>
                
                <div class="chart">
                    <img src="data:image/png;base64,{price_img}" alt="Evolução do Preço do Token">
                </div>
                
                <div class="chart">
                    <img src="data:image/png;base64,{mcap_img}" alt="Evolução do Market Cap">
                </div>
                """
            
            if custom_notes:
                html_content += f"""
                <h2>Notas Adicionais</h2>
                <p>{custom_notes}</p>
                """
            
            if include_disclaimer:
                html_content += """
                <div class="footer">
                    <h3>Aviso Legal</h3>
                    <p>
                        Este relatório é apenas para fins informativos e não constitui aconselhamento financeiro ou de investimento. 
                        As projeções e simulações são baseadas em modelos teóricos e não garantem resultados futuros. 
                        Todos os investimentos envolvem riscos e os leitores devem realizar sua própria pesquisa e consultar profissionais qualificados antes de tomar decisões financeiras.
                    </p>
                </div>
                """
            
            html_content += """
            </body>
            </html>
            """
            
            # Provide download link
            st.markdown(get_download_link(html_content, f"{model.name}_report.html", "HTML"), unsafe_allow_html=True)
            st.success("Relatório HTML gerado com sucesso!")
            
        elif export_format == "PDF":
            # Placeholder for PDF generation
            df_sample = df.head(10)
            
            # Generate PDF report
            pdf_data = generate_pdf_report(
                model, 
                df, 
                report_title, 
                author, 
                str(report_date),
                include_overview,
                include_distribution,
                include_vesting,
                include_price,
                include_metrics,
                include_disclaimer,
                custom_notes
            )
            
            # Provide download link
            st.markdown(get_download_link(pdf_data, f"{model.name}_report.pdf", "PDF"), unsafe_allow_html=True)
            st.success("Relatório PDF gerado com sucesso!")
            
        elif export_format == "CSV (apenas dados)":
            # CSV export
            csv = df.to_csv(index=False)
            
            # Provide download link
            st.download_button(
                label="Baixar dados CSV",
                data=csv,
                file_name=f"{model.name}_simulation_data.csv",
                mime="text/csv",
            )
            st.success("Dados CSV gerados com sucesso!")
