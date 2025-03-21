import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from io import BytesIO
import base64
from datetime import datetime
import os
from typing import Dict, List, Tuple, Optional, Union, Any

# Import local modules
from models.tokenomics import TokenomicsModel
from utils.visualization import (
    create_matplotlib_distribution_chart,
    create_matplotlib_price_chart,
    create_matplotlib_market_cap_chart
)

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
    from reportlab.platypus import PageBreak
    from reportlab.lib.units import inch
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    

def get_download_link(object_to_download, download_filename, download_link_text):
    """
    Generates a link to download the given object.
    
    Args:
        object_to_download: The object to be downloaded.
        download_filename (str): Filename and extension of file.
        download_link_text (str): Text to display for download link.
        
    Returns:
        str: HTML code for download link
    """
    if isinstance(object_to_download, str):
        object_to_download = object_to_download.encode()
    
    b64 = base64.b64encode(object_to_download).decode()
    
    # Some browsers don't support data attribute for downloads so we need to create a download link
    download_str = f"data:file/{download_filename.split('.')[-1]};base64,{b64}"
    
    href = f'<a href="{download_str}" download="{download_filename}">{download_link_text}</a>'
    
    return href


def generate_pdf_report(
    model: TokenomicsModel, 
    df: pd.DataFrame, 
    report_title: str, 
    author: str, 
    date_str: str,
    include_overview: bool = True,
    include_distribution: bool = True,
    include_vesting: bool = True,
    include_price: bool = True,
    include_metrics: bool = True,
    include_disclaimer: bool = True,
    custom_notes: str = ""
) -> bytes:
    """
    Generate a PDF report for tokenomics model
    
    Args:
        model (TokenomicsModel): Tokenomics model
        df (pd.DataFrame): Simulation dataframe
        report_title (str): Title of the report
        author (str): Author name
        date_str (str): Date string
        include_overview (bool): Include model overview section
        include_distribution (bool): Include token distribution section
        include_vesting (bool): Include vesting schedule section
        include_price (bool): Include price simulation section
        include_metrics (bool): Include model-specific metrics section
        include_disclaimer (bool): Include disclaimer section
        custom_notes (str): Additional custom notes
        
    Returns:
        bytes: PDF file as bytes
    """
    if not REPORTLAB_AVAILABLE:
        return b"ReportLab library not available. Please install it with: pip install reportlab"
    
    # Create a buffer to store the PDF
    buffer = BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Get the styles
    styles = getSampleStyleSheet()
    
    # Add custom styles
    styles.add(ParagraphStyle(
        name='TitleStyle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=12,
        textColor=colors.HexColor('#0068c9')
    ))
    
    styles.add(ParagraphStyle(
        name='SubtitleStyle',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=10,
        textColor=colors.HexColor('#444444')
    ))
    
    styles.add(ParagraphStyle(
        name='SectionStyle',
        parent=styles['Heading3'],
        fontSize=14,
        spaceAfter=8,
        textColor=colors.HexColor('#0068c9')
    ))
    
    styles.add(ParagraphStyle(
        name='NormalStyle',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6
    ))
    
    styles.add(ParagraphStyle(
        name='SmallStyle',
        parent=styles['Normal'],
        fontSize=9,
        spaceAfter=4
    ))
    
    styles.add(ParagraphStyle(
        name='DisclaimerStyle',
        parent=styles['Normal'],
        fontSize=8,
        spaceAfter=0,
        textColor=colors.HexColor('#666666')
    ))
    
    # Create the elements for the PDF
    elements = []
    
    # Add title
    elements.append(Paragraph(report_title, styles['TitleStyle']))
    
    # Add author and date
    elements.append(Paragraph(f"Autor: {author} | Data: {date_str}", styles['NormalStyle']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Add executive summary
    elements.append(Paragraph("Resumo Executivo", styles['SubtitleStyle']))
    
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
    
    summary_text = f"""
    Este relatório apresenta uma análise detalhada do modelo de tokenomics para <b>{model.name}</b>.
    O modelo é baseado em um token do tipo <b>{model_type}</b> com uma oferta total de <b>{total_supply:,}</b> tokens.
    """
    elements.append(Paragraph(summary_text, styles['NormalStyle']))
    
    elements.append(Paragraph("Principais métricas após {} meses:".format(df['Month'].max()), styles['NormalStyle']))
    
    # Create metrics table
    metrics_data = [
        ["Métrica", "Valor"],
        ["Preço do Token", "${:.4f} ({:.1f}% desde o início)".format(latest_price, price_change)],
        ["Oferta em Circulação", "{:,.0f} tokens ({:.1f}% do total)".format(latest_supply, supply_percent)],
        ["Market Cap Projetado", "${:,.2f}".format(latest_mcap)]
    ]
    
    t = Table(metrics_data, colWidths=[2.5*inch, 3*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#0068c9')),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
        ('ALIGN', (0, 0), (1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (1, 0), 12),
        ('BACKGROUND', (0, 1), (1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
    ]))
    
    elements.append(t)
    elements.append(Spacer(1, 0.3*inch))
    
    # Add model overview
    if include_overview:
        elements.append(Paragraph("Visão Geral do Modelo", styles['SubtitleStyle']))
        
        overview_text = f"""
        O modelo <b>{model.name}</b> foi configurado com as seguintes características:
        <br/><br/>
        <b>Tipo de Token:</b> {model_type}<br/>
        <b>Oferta Total:</b> {total_supply:,} tokens<br/>
        <b>Número de Categorias de Distribuição:</b> {len(model.distribution)}
        """
        
        if hasattr(model, 'initial_users'):
            overview_text += f"""
            <br/><b>Usuários Iniciais:</b> {model.initial_users:,}<br/>
            <b>Taxa de Crescimento de Usuários:</b> {model.user_growth_rate:.1%} ao mês
            """
        
        if hasattr(model, 'initial_staking_rate'):
            overview_text += f"""
            <br/><b>Taxa Inicial de Staking:</b> {model.initial_staking_rate:.1%}<br/>
            <b>APY de Staking:</b> {model.staking_apy:.1%}
            """
            
        elements.append(Paragraph(overview_text, styles['NormalStyle']))
        elements.append(Spacer(1, 0.2*inch))
    
    # Add token distribution section
    if include_distribution:
        elements.append(Paragraph("Distribuição de Tokens", styles['SubtitleStyle']))
        
        elements.append(Paragraph("A alocação de tokens foi distribuída entre as seguintes categorias:", styles['NormalStyle']))
        
        # Create distribution table
        dist_data = [["Categoria", "Porcentagem"]]
        
        for category, percentage in model.distribution.items():
            dist_data.append([category, f"{percentage:.1f}%"])
        
        t = Table(dist_data, colWidths=[3.5*inch, 2*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#0068c9')),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
            ('ALIGN', (0, 0), (1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (1, 0), 12),
            ('BACKGROUND', (0, 1), (1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
        ]))
        
        elements.append(t)
        elements.append(Spacer(1, 0.2*inch))
        
        # Add distribution chart
        fig = create_matplotlib_distribution_chart(model.distribution)
        
        # Save chart to buffer
        img_buffer = BytesIO()
        fig.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
        plt.close(fig)
        
        # Create image for ReportLab
        img = Image(img_buffer, width=6*inch, height=4*inch)
        elements.append(img)
        elements.append(Spacer(1, 0.2*inch))
    
    # Add vesting schedule section
    if include_vesting and model.vesting_schedules:
        elements.append(Paragraph("Cronograma de Vesting", styles['SubtitleStyle']))
        
        for category, schedule in model.vesting_schedules.items():
            elements.append(Paragraph(f"Cronograma de Vesting para {category}:", styles['NormalStyle']))
            
            # Create vesting table
            vesting_data = [["Mês", "Porcentagem", "Porcentagem Acumulada"]]
            
            cumulative = 0
            for month, percentage in sorted(schedule, key=lambda x: x[0]):
                cumulative += percentage
                vesting_data.append([str(month), f"{percentage:.1f}%", f"{cumulative:.1f}%"])
            
            t = Table(vesting_data, colWidths=[1.5*inch, 2*inch, 2*inch])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (2, 0), colors.HexColor('#0068c9')),
                ('TEXTCOLOR', (0, 0), (2, 0), colors.white),
                ('ALIGN', (0, 0), (2, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (2, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (2, 0), 12),
                ('BACKGROUND', (0, 1), (2, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ALIGN', (1, 1), (2, -1), 'RIGHT'),
            ]))
            
            elements.append(t)
            elements.append(Spacer(1, 0.2*inch))
    
    # Add price simulation section
    if include_price:
        elements.append(PageBreak())
        elements.append(Paragraph("Simulação de Preço", styles['SubtitleStyle']))
        
        # Add price chart
        fig = create_matplotlib_price_chart(df)
        
        # Save chart to buffer
        img_buffer = BytesIO()
        fig.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
        plt.close(fig)
        
        # Create image for ReportLab
        img = Image(img_buffer, width=6*inch, height=3*inch)
        elements.append(img)
        elements.append(Spacer(1, 0.2*inch))
        
        # Add market cap chart
        fig = create_matplotlib_market_cap_chart(df)
        
        # Save chart to buffer
        img_buffer = BytesIO()
        fig.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
        plt.close(fig)
        
        # Create image for ReportLab
        img = Image(img_buffer, width=6*inch, height=3*inch)
        elements.append(img)
        elements.append(Spacer(1, 0.2*inch))
    
    # Add model-specific metrics section
    if include_metrics:
        elements.append(Paragraph("Métricas Específicas", styles['SubtitleStyle']))
        
        if 'Users' in df.columns and 'Token_Demand' in df.columns:
            # Utility token metrics
            elements.append(Paragraph("Métricas de Utility Token:", styles['NormalStyle']))
            
            metrics_text = f"""
            <b>Usuários Finais:</b> {df['Users'].iloc[-1]:,.0f} (crescimento de {((df['Users'].iloc[-1] / df['Users'].iloc[0]) - 1) * 100:.1f}%)<br/>
            <b>Demanda Final de Tokens:</b> {df['Token_Demand'].iloc[-1]:,.0f} tokens<br/>
            """
            
            elements.append(Paragraph(metrics_text, styles['NormalStyle']))
            elements.append(Spacer(1, 0.2*inch))
            
        elif 'Staking_Rate' in df.columns and 'Staked_Tokens' in df.columns:
            # Governance token metrics
            elements.append(Paragraph("Métricas de Governance Token:", styles['NormalStyle']))
            
            metrics_text = f"""
            <b>Taxa Final de Staking:</b> {df['Staking_Rate'].iloc[-1]:.1%}<br/>
            <b>Tokens em Staking:</b> {df['Staked_Tokens'].iloc[-1]:,.0f} tokens ({df['Staked_Tokens'].iloc[-1] / df['Circulating_Supply'].iloc[-1] * 100:.1f}% da oferta circulante)<br/>
            """
            
            elements.append(Paragraph(metrics_text, styles['NormalStyle']))
            elements.append(Spacer(1, 0.2*inch))
    
    # Add custom notes
    if custom_notes:
        elements.append(Paragraph("Notas Adicionais", styles['SubtitleStyle']))
        elements.append(Paragraph(custom_notes, styles['NormalStyle']))
        elements.append(Spacer(1, 0.2*inch))
    
    # Add disclaimer
    if include_disclaimer:
        elements.append(Spacer(1, 0.3*inch))
        elements.append(Paragraph("Aviso Legal", styles['SmallStyle']))
        disclaimer_text = """
        Este relatório é apenas para fins informativos e não constitui aconselhamento financeiro ou de investimento. 
        As projeções e simulações são baseadas em modelos teóricos e não garantem resultados futuros. 
        Todos os investimentos envolvem riscos e os leitores devem realizar sua própria pesquisa e consultar profissionais qualificados antes de tomar decisões financeiras.
        """
        elements.append(Paragraph(disclaimer_text, styles['DisclaimerStyle']))
    
    # Build the PDF document
    doc.build(elements)
    
    # Get PDF from buffer
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes


def generate_html_report(
    model: TokenomicsModel, 
    df: pd.DataFrame, 
    report_title: str, 
    author: str, 
    date_str: str,
    include_overview: bool = True,
    include_distribution: bool = True,
    include_vesting: bool = True,
    include_price: bool = True,
    include_metrics: bool = True,
    include_disclaimer: bool = True,
    custom_notes: str = ""
) -> str:
    """
    Generate an HTML report for tokenomics model
    
    Args:
        model (TokenomicsModel): Tokenomics model
        df (pd.DataFrame): Simulation dataframe
        report_title (str): Title of the report
        author (str): Author name
        date_str (str): Date string
        include_overview (bool): Include model overview section
        include_distribution (bool): Include token distribution section
        include_vesting (bool): Include vesting schedule section
        include_price (bool): Include price simulation section
        include_metrics (bool): Include model-specific metrics section
        include_disclaimer (bool): Include disclaimer section
        custom_notes (str): Additional custom notes
        
    Returns:
        str: HTML report as string
    """
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
    
    # Create distribution pie chart
    fig = create_matplotlib_distribution_chart(model.distribution)
    
    # Save chart to buffer
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    plt.close(fig)
    
    # Encode the image
    distribution_img = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    # Create price chart
    fig = create_matplotlib_price_chart(df)
    
    # Save chart to buffer
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    plt.close(fig)
    
    # Encode the image
    price_img = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    # Create market cap chart
    fig = create_matplotlib_market_cap_chart(df)
    
    # Save chart to buffer
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    plt.close(fig)
    
    # Encode the image
    mcap_img = base64.b64encode(buf.getvalue()).decode('utf-8')
    
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
            <p><strong>Autor:</strong> {author} | <strong>Data:</strong> {date_str}</p>
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
        html_content += f"""
        <h2>Simulação de Preço</h2>
        
        <div class="chart">
            <img src="data:image/png;base64,{price_img}" alt="Evolução do Preço do Token">
        </div>
        
        <div class="chart">
            <img src="data:image/png;base64,{mcap_img}" alt="Evolução do Market Cap">
        </div>
        """
    
    if include_metrics:
        html_content += """
        <h2>Métricas Específicas</h2>
        """
        
        if 'Users' in df.columns and 'Token_Demand' in df.columns:
            # Utility token metrics
            user_growth = ((df['Users'].iloc[-1] / df['Users'].iloc[0]) - 1) * 100
            
            html_content += f"""
            <h3>Métricas de Utility Token</h3>
            <ul>
                <li><strong>Usuários Finais:</strong> {df['Users'].iloc[-1]:,.0f} (crescimento de {user_growth:.1f}%)</li>
                <li><strong>Demanda Final de Tokens:</strong> {df['Token_Demand'].iloc[-1]:,.0f} tokens</li>
            </ul>
            """
            
        elif 'Staking_Rate' in df.columns and 'Staked_Tokens' in df.columns:
            # Governance token metrics
            staked_percent = df['Staked_Tokens'].iloc[-1] / df['Circulating_Supply'].iloc[-1] * 100
            
            html_content += f"""
            <h3>Métricas de Governance Token</h3>
            <ul>
                <li><strong>Taxa Final de Staking:</strong> {df['Staking_Rate'].iloc[-1]:.1%}</li>
                <li><strong>Tokens em Staking:</strong> {df['Staked_Tokens'].iloc[-1]:,.0f} tokens ({staked_percent:.1f}% da oferta circulante)</li>
            </ul>
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
    
    return html_content
