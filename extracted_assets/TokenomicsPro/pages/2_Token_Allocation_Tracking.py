import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils import calculate_allocation_amounts, get_color_scale
from datetime import datetime, timedelta

# Set page configuration
st.set_page_config(
    page_title="Token Allocation Tracking - TokenomicsLab",
    page_icon="📊",
    layout="wide"
)

# Page title and description
st.title("Token Allocation Tracking")
st.markdown("""
This section allows you to track the distribution of tokens across different allocation categories over time.
Monitor token releases, circulation, and the status of each allocation category.
""")

# Check if tokenomics data is initialized
if 'tokenomics_data' not in st.session_state:
    st.error("Please start from the main page to initialize your token data.")
    st.stop()

# Initialize tracking data in session state if it doesn't exist
if 'allocation_tracking' not in st.session_state:
    st.session_state.allocation_tracking = {
        'categories': {},
        'history': []
    }
    
    # Initialize categories from allocation data
    for category, percentage in st.session_state.tokenomics_data['allocation_categories'].items():
        token_amount = st.session_state.tokenomics_data['total_supply'] * percentage / 100
        st.session_state.allocation_tracking['categories'][category] = {
            'total_allocation': token_amount,
            'released': 0,
            'locked': token_amount,
            'last_release_date': None
        }

# Get data from session state
token_name = st.session_state.tokenomics_data['token_name']
token_symbol = st.session_state.tokenomics_data['token_symbol']
total_supply = st.session_state.tokenomics_data['total_supply']
allocations = st.session_state.tokenomics_data['allocation_categories']
tracking_data = st.session_state.allocation_tracking

# Calculate allocation amounts
allocation_amounts = calculate_allocation_amounts(total_supply, allocations)

# Current circulation statistics
total_released = sum(cat_data['released'] for cat_data in tracking_data['categories'].values())
total_locked = sum(cat_data['locked'] for cat_data in tracking_data['categories'].values())
circulation_percentage = (total_released / total_supply) * 100 if total_supply > 0 else 0

# Display key metrics
st.subheader("Token Circulation Overview")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Supply", f"{total_supply:,}")
    
with col2:
    st.metric("Circulating Supply", f"{total_released:,.0f}", f"{circulation_percentage:.2f}%")
    
with col3:
    st.metric("Locked Supply", f"{total_locked:,.0f}", f"{100-circulation_percentage:.2f}%")

# Tracking table
st.subheader("Allocation Tracking")

# Create tracking dataframe
tracking_df = []
for category, data in tracking_data['categories'].items():
    tracking_df.append({
        'Category': category,
        'Total Allocation': data['total_allocation'],
        'Released': data['released'],
        'Locked': data['locked'],
        'Release %': (data['released'] / data['total_allocation'] * 100) if data['total_allocation'] > 0 else 0,
        'Last Release Date': data['last_release_date'] if data['last_release_date'] else 'No releases yet'
    })

tracking_df = pd.DataFrame(tracking_df)
st.dataframe(
    tracking_df.style.format({
        'Total Allocation': '{:,.0f}',
        'Released': '{:,.0f}',
        'Locked': '{:,.0f}',
        'Release %': '{:.2f}%'
    }),
    use_container_width=True
)

# Visualization of current status
st.subheader("Token Distribution Status")
col1, col2 = st.columns(2)

with col1:
    # Stacked bar chart showing released vs locked per category
    status_data = []
    for idx, row in tracking_df.iterrows():
        status_data.append({
            'Category': row['Category'],
            'Status': 'Released',
            'Amount': row['Released']
        })
        status_data.append({
            'Category': row['Category'],
            'Status': 'Locked',
            'Amount': row['Locked']
        })
    
    status_df = pd.DataFrame(status_data)
    
    fig = px.bar(
        status_df,
        x='Category',
        y='Amount',
        color='Status',
        title="Released vs Locked Tokens per Category",
        barmode='stack',
        color_discrete_map={'Released': '#2ca02c', 'Locked': '#d62728'}
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Pie chart of circulating vs locked supply
    circulation_data = pd.DataFrame({
        'Status': ['Circulating Supply', 'Locked Supply'],
        'Amount': [total_released, total_locked]
    })
    
    fig = px.pie(
        circulation_data,
        values='Amount',
        names='Status',
        title="Circulating vs Locked Supply",
        color='Status',
        color_discrete_map={'Circulating Supply': '#2ca02c', 'Locked Supply': '#d62728'}
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)

# Token release form
st.subheader("Record Token Release")
col1, col2 = st.columns(2)

with col1:
    release_category = st.selectbox(
        "Select Category",
        options=list(tracking_data['categories'].keys())
    )
    
    # Calculate maximum available to release
    max_available = tracking_data['categories'][release_category]['locked']
    
    release_amount = st.number_input(
        "Release Amount",
        min_value=0.0,
        max_value=float(max_available),
        value=0.0,
        step=1000.0
    )

with col2:
    release_date = st.date_input(
        "Release Date",
        value=datetime.now()
    )
    
    release_note = st.text_area(
        "Release Notes",
        placeholder="Enter additional information about this release"
    )

if st.button("Record Release"):
    if release_amount <= 0:
        st.error("Release amount must be greater than zero.")
    elif release_amount > max_available:
        st.error(f"Release amount cannot exceed available locked tokens ({max_available:,.0f}).")
    else:
        # Update category data
        tracking_data['categories'][release_category]['released'] += release_amount
        tracking_data['categories'][release_category]['locked'] -= release_amount
        tracking_data['categories'][release_category]['last_release_date'] = release_date.strftime('%Y-%m-%d')
        
        # Add to history
        tracking_data['history'].append({
            'date': release_date.strftime('%Y-%m-%d'),
            'category': release_category,
            'amount': release_amount,
            'notes': release_note
        })
        
        st.session_state.allocation_tracking = tracking_data
        st.success(f"Recorded release of {release_amount:,.0f} tokens from {release_category}.")
        st.rerun()

# Release history
if tracking_data['history']:
    st.subheader("Release History")
    
    history_df = pd.DataFrame(tracking_data['history'])
    history_df = history_df.sort_values('date', ascending=False)
    
    st.dataframe(
        history_df.style.format({
            'amount': '{:,.0f}'
        }),
        use_container_width=True
    )
    
    # Visualization of release history
    if len(history_df) > 1:
        # Prepare cumulative data
        history_df['date'] = pd.to_datetime(history_df['date'])
        history_df = history_df.sort_values('date')
        history_df['cumulative'] = history_df['amount'].cumsum()
        
        fig = px.line(
            history_df,
            x='date',
            y='cumulative',
            markers=True,
            title="Cumulative Token Release Over Time"
        )
        st.plotly_chart(fig, use_container_width=True)

# Reset tracking data (with warning)
st.markdown("---")
if st.button("Reset Tracking Data", help="This will clear all release history and reset the tracking data."):
    confirm = st.checkbox("Confirm reset (this cannot be undone)")
    
    if confirm:
        # Reset tracking data
        st.session_state.allocation_tracking = {
            'categories': {},
            'history': []
        }
        
        # Reinitialize categories from allocation data
        for category, percentage in st.session_state.tokenomics_data['allocation_categories'].items():
            token_amount = st.session_state.tokenomics_data['total_supply'] * percentage / 100
            st.session_state.allocation_tracking['categories'][category] = {
                'total_allocation': token_amount,
                'released': 0,
                'locked': token_amount,
                'last_release_date': None
            }
        
        st.success("Tracking data has been reset.")
        st.rerun()
