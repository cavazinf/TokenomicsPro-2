import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.colored_header import colored_header
from streamlit_extras.app_logo import add_logo
import database as db
import os
import json
from datetime import datetime

# Initialize database
db.init_db()

# Set page configuration
st.set_page_config(
    page_title="TokenomicsLab - Innovation",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS styling
st.markdown("""
<style>
    /* Main container */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }

    /* Hero section */
    .hero-section {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }

    /* Feature cards */
    .feature-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 10px 0;
        transition: transform 0.3s;
    }

    .feature-card:hover {
        transform: translateY(-5px);
    }

    /* Section headers */
    .section-header {
        font-size: 2rem;
        font-weight: bold;
        margin: 2rem 0;
        color: #1e3c72;
    }

    /* Call to action button */
    .cta-button {
        background-color: #2a5298;
        color: white;
        padding: 12px 24px;
        border-radius: 25px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        margin: 1rem 0;
        transition: background-color 0.3s;
    }

    .cta-button:hover {
        background-color: #1e3c72;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions (from original code)
def login(username, password):
    """Handle user login"""
    user = db.get_user_by_username(username)
    if user and user.check_password(password):
        st.session_state.authenticated = True
        st.session_state.user = user.to_dict()
        st.session_state.login_error = None
        return True
    else:
        st.session_state.login_error = "Invalid username or password"
        return False

def register(username, email, password, confirm_password):
    """Handle user registration"""
    # Input validation
    if not username or not email or not password:
        st.session_state.registration_error = "All fields are required"
        return False

    if password != confirm_password:
        st.session_state.registration_error = "Passwords do not match"
        return False

    # Check if username already exists
    existing_user = db.get_user_by_username(username)
    if existing_user:
        st.session_state.registration_error = "Username already exists"
        return False

    # Create user
    user = db.create_user(username, email, password)
    if user:
        st.session_state.authenticated = True
        st.session_state.user = user.to_dict()
        st.session_state.registration_error = None
        return True
    else:
        st.session_state.registration_error = "Error creating user account"
        return False

def logout():
    """Handle user logout"""
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.current_page = 'home'

def navigate_to(page):
    """Handle navigation between app sections"""
    st.session_state.current_page = page

def display_login_form():
    """Display login form"""
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.write("")
        st.write("")
        with st.container():
            colored_header("Login to Web3 Startup Platform", description="", color_name="blue-70")

            with st.form("login_form", clear_on_submit=False):
                username = st.text_input("Username", key="login_username")
                password = st.text_input("Password", type="password", key="login_password")

                col1, col2 = st.columns(2)

                with col1:
                    submit = st.form_submit_button("Login")

                with col2:
                    register_button = st.form_submit_button("Register")

            if st.session_state.login_error:
                st.error(st.session_state.login_error)

            if submit:
                if login(username, password):
                    st.rerun()

            if register_button:
                navigate_to('register')
                st.rerun()

def display_registration_form():
    """Display registration form"""
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.write("")
        st.write("")
        with st.container():
            colored_header("Create an Account", description="", color_name="green-70")

            with st.form("registration_form", clear_on_submit=True):
                username = st.text_input("Username", key="reg_username")
                email = st.text_input("Email", key="reg_email")
                password = st.text_input("Password", type="password", key="reg_password")
                confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm_password")

                col1, col2 = st.columns(2)

                with col1:
                    submit = st.form_submit_button("Register")

                with col2:
                    back_button = st.form_submit_button("Back to Login")

            if st.session_state.registration_error:
                st.error(st.session_state.registration_error)

            if submit:
                if register(username, email, password, confirm_password):
                    st.rerun()

            if back_button:
                navigate_to('login')
                st.rerun()

def render_sidebar():
    """Render sidebar with navigation options"""
    with st.sidebar:
        if st.session_state.authenticated:
            st.markdown(f"### Welcome, {st.session_state.user['display_name'] or st.session_state.user['username']}")

            st.markdown("### Main Navigation")

            if st.button("🏠 Dashboard", key="sidebar_dashboard"):
                navigate_to('dashboard')
                st.rerun()

            # Web3 StartupBuilder Section
            st.markdown("### Web3 StartupBuilder")

            if st.button("🚀 Projects", key="sidebar_projects"):
                navigate_to('projects')
                st.rerun()

            if st.button("💰 Token Designer", key="sidebar_token_designer"):
                navigate_to('token_designer')
                st.rerun()

            if st.button("📊 Distribution Planner", key="sidebar_distribution"):
                navigate_to('distribution_planner')
                st.rerun()

            if st.button("📈 Economic Simulator", key="sidebar_simulator"):
                navigate_to('economic_simulator')
                st.rerun()

            if st.button("📚 Learning Hub", key="sidebar_learning"):
                navigate_to('learning_hub')
                st.rerun()

            # TokenomicsLab Section
            st.markdown("### TokenomicsLab")

            if st.button("🧩 Token Supply Distribution", key="sidebar_supply"):
                switch_page("1_Token_Supply_Distribution")

            if st.button("📋 Token Allocation Tracking", key="sidebar_allocation"):
                switch_page("2_Token_Allocation_Tracking")

            if st.button("📉 Economic Simulation", key="sidebar_econ_sim"):
                switch_page("3_Economic_Simulation")

            if st.button("⏱️ Vesting Schedule", key="sidebar_vesting"):
                switch_page("4_Vesting_Schedule")

            if st.button("💵 Price & Market Cap", key="sidebar_price"):
                switch_page("5_Price_Market_Cap")

            if st.button("🔧 Token Design", key="sidebar_design"):
                switch_page("6_Token_Design")

            if st.button("📐 Econometrics", key="sidebar_econometrics"):
                switch_page("7_Econometrics")

            if st.button("🏗️ Tokenization Models", key="sidebar_models"):
                switch_page("8_Tokenization_Models")

            if st.button("💼 Business Model", key="sidebar_business"):
                switch_page("9_Business_Model")

            if st.button("📊 Market Analysis", key="sidebar_market"):
                switch_page("10_Market_Analysis")

            if st.button("📣 Marketing & Growth", key="sidebar_marketing"):
                switch_page("11_Marketing_Growth")

            if st.button("💹 Crypto Trading", key="sidebar_trading"):
                switch_page("12_Crypto_Trading")

            if st.button("🎮 Market Simulation", key="sidebar_market_sim"):
                switch_page("13_Market_Simulation")

            if st.button("🔄 Cryptoeconomic Designer", key="sidebar_crypto"):
                switch_page("14_Cryptoeconomic_Systems_Designer")

            if st.button("⚙️ Tokenomics Engine", key="sidebar_engine"):
                switch_page("15_Tokenomics_Engine")

            # Advanced Features
            st.markdown("### Advanced Features")

            if st.button("🔍 Model Comparison", key="sidebar_comparison"):
                navigate_to('model_comparison')
                st.rerun()

            # Admin section (only for admin users)
            if st.session_state.user.get('is_admin', False):
                st.markdown("### Administration")

                if st.button("👤 User Management", key="sidebar_users"):
                    navigate_to('admin_users')
                    st.rerun()

                if st.button("🔧 System Settings", key="sidebar_settings"):
                    navigate_to('admin_settings')
                    st.rerun()

            # Settings & Logout
            st.markdown("### Settings")

            language = st.selectbox(
                "Language",
                ["English", "Português", "Español"],
                index=["English", "Português", "Español"].index(st.session_state.language)
            )

            if language != st.session_state.language:
                st.session_state.language = language
                st.rerun()

            if st.button("🚪 Logout", key="sidebar_logout"):
                logout()
                st.rerun()

def render_dashboard():
    """Render user dashboard with summary and quick access"""
    st.title("Dashboard")
    st.write("Welcome to your Web3 Startup Platform Dashboard")

    # Quick Stats
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        projects = db.get_projects_by_user(st.session_state.user['id'])
        st.metric("Projects", len(projects) if projects else 0)

    with col2:
        tokenomics_models = db.get_tokenomics_models_by_user(st.session_state.user['id'])
        st.metric("Tokenomics Models", len(tokenomics_models) if tokenomics_models else 0)

    with col3:
        crypto_systems = db.get_cryptoeconomic_systems_by_user(st.session_state.user['id'])
        st.metric("Cryptoeconomic Systems", len(crypto_systems) if crypto_systems else 0)

    with col4:
        # User plan/status
        st.metric("Account Plan", st.session_state.user.get('plan', 'Free').capitalize())

    # Recent Activity & Quick Actions
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Recent Activity")

        # Get recent projects
        recent_projects = db.get_projects_by_user(st.session_state.user['id'])
        if recent_projects:
            recent_projects = sorted(recent_projects, key=lambda x: x.last_edited if x.last_edited else x.created_at, reverse=True)[:5]

            for project in recent_projects:
                with st.container():
                    cols = st.columns([3, 2, 1])
                    cols[0].write(f"**{project.name}**")
                    cols[1].write(f"Status: {project.status.capitalize()}")
                    last_edited = project.last_edited or project.created_at
                    cols[2].write(f"{last_edited.strftime('%Y-%m-%d')}")
                st.divider()
        else:
            st.info("No projects yet. Create your first project from the Projects section.")

    with col2:
        st.subheader("Quick Actions")

        if st.button("Create New Project", key="dashboard_new_project"):
            navigate_to('new_project')
            st.rerun()

        if st.button("Create Tokenomics Model", key="dashboard_new_tokenomics"):
            navigate_to('new_tokenomics')
            st.rerun()

        if st.button("Design Cryptoeconomic System", key="dashboard_new_crypto"):
            navigate_to('new_cryptosystem')
            st.rerun()

        if st.button("Compare Models", key="dashboard_compare"):
            navigate_to('model_comparison')
            st.rerun()

    # Resources section
    st.subheader("Learning Resources")

    resources = db.get_resources()
    if resources:
        cols = st.columns(len(resources))

        for i, resource in enumerate(resources):
            with cols[i]:
                with st.container():
                    st.markdown(f"### {resource.title}")
                    st.write(resource.description)
                    st.markdown(f"**Type:** {resource.type.capitalize()}")
                    if st.button(resource.link_text, key=f"resource_{resource.id}"):
                        # This would normally navigate to the resource
                        st.info(f"Navigating to: {resource.link}")


def render_projects_page():
    """Render projects management page"""
    st.title("Projects")
    st.write("Manage your Web3 startup projects")

    # Project actions bar
    col1, col2 = st.columns([6, 1])

    with col1:
        st.write("Your Web3 startup projects")

    with col2:
        if st.button("+ New Project", key="new_project_btn"):
            navigate_to('new_project')
            st.rerun()

    # Get user's projects
    projects = db.get_projects_by_user(st.session_state.user['id'])

    if not projects:
        st.info("You don't have any projects yet. Click 'New Project' to create one.")
    else:
        # Display projects in a grid
        project_rows = [projects[i:i+3] for i in range(0, len(projects), 3)]

        for row in project_rows:
            cols = st.columns(3)

            for i, project in enumerate(row):
                with cols[i]:
                    with st.container():
                        st.markdown(f"### {project.name}")
                        st.markdown(f"**Status:** {project.status.capitalize()}")
                        st.markdown(f"**Progress:** {project.token_design_progress}%")
                        st.markdown(f"**Last edited:** {project.last_edited.strftime('%Y-%m-%d') if project.last_edited else 'Never'}")

                        col1, col2 = st.columns(2)

                        with col1:
                            if st.button("Edit", key=f"edit_{project.id}"):
                                st.session_state.current_project = project.id
                                navigate_to('edit_project')
                                st.rerun()

                        with col2:
                            if st.button("Delete", key=f"delete_{project.id}"):
                                if db.delete_project(project.id):
                                    st.success("Project deleted successfully")
                                    st.rerun()
                                else:
                                    st.error("Failed to delete project")

def render_new_project_page():
    """Render new project creation page"""
    st.title("Create New Project")

    with st.form("new_project_form"):
        project_name = st.text_input("Project Name")

        submitted = st.form_submit_button("Create Project")

        if submitted and project_name:
            new_project = db.create_project(project_name, st.session_state.user['id'])

            if new_project:
                st.success("Project created successfully!")
                st.session_state.current_project = new_project.id
                navigate_to('edit_project')
                st.rerun()
            else:
                st.error("Failed to create project. Please try again.")

def render_model_comparison_page():
    """Render tokenomics model comparison page"""
    st.title("Tokenomics Model Comparison")
    st.write("Compare different tokenomics models to find the optimal strategy")

    # Get user's tokenomics models
    models = db.get_tokenomics_models_by_user(st.session_state.user['id'])

    if not models:
        st.info("You don't have any tokenomics models to compare. Create models first.")

        if st.button("Create Tokenomics Model"):
            navigate_to('new_tokenomics')
            st.rerun()
    else:
        # Setup comparison
        st.subheader("Select Models to Compare")

        # Create a multiselect with model options
        model_options = {model.id: model.name for model in models}
        selected_models = st.multiselect(
            "Select Models",
            options=list(model_options.keys()),
            format_func=lambda x: model_options[x]
        )

        if len(selected_models) >= 2:
            # Comparison parameters
            st.subheader("Comparison Parameters")

            col1, col2 = st.columns(2)

            with col1:
                simulation_months = st.slider("Simulation Months", min_value=12, max_value=60, value=36)

            with col2:
                initial_price = st.number_input("Initial Token Price ($)", min_value=0.0001, value=1.0)

            volatility = st.slider("Market Volatility", min_value=0.0, max_value=1.0, value=0.2, step=0.05)

            # Run comparison
            if st.button("Run Comparison"):
                st.subheader("Comparison Results")

                # Get selected model details
                selected_model_objects = [next(model for model in models if model.id == model_id) for model_id in selected_models]

                # Create comparison dataframes (simplified for this example)
                price_data = []
                circulating_supply_data = []
                market_cap_data = []

                for model in selected_model_objects:
                    # Create sample data for demonstration
                    price = initial_price
                    prices = [price]
                    supply = model.total_supply * 0.05  # 5% initial circulating supply
                    supplies = [supply]

                    for month in range(1, simulation_months + 1):
                        release_rate = min(0.05 + (month / 100), 0.9)  # Sample vesting curve
                        new_supply = model.total_supply * release_rate
                        random_growth = np.random.uniform(-volatility, volatility + 0.05)
                        price = price * (1 + random_growth)

                        prices.append(price)
                        supplies.append(new_supply)

                    # Add to comparison data
                    price_data.append({
                        'model_name': model.name,
                        'prices': prices
                    })

                    circulating_supply_data.append({
                        'model_name': model.name,
                        'supplies': supplies
                    })

                    market_cap_data.append({
                        'model_name': model.name,
                        'market_caps': [p * s for p, s in zip(prices, supplies)]
                    })

                # Create and display comparison charts
                tabs = st.tabs(["Price Comparison", "Circulating Supply", "Market Cap"])

                with tabs[0]:
                    price_fig = go.Figure()
                    for data in price_data:
                        price_fig.add_trace(go.Scatter(
                            x=list(range(simulation_months + 1)),
                            y=data['prices'],
                            mode='lines',
                            name=data['model_name']
                        ))

                    price_fig.update_layout(
                        title="Price Comparison",
                        xaxis_title="Month",
                        yaxis_title="Price ($)",
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1
                        )
                    )

                    st.plotly_chart(price_fig, use_container_width=True)

                with tabs[1]:
                    supply_fig = go.Figure()
                    for data in circulating_supply_data:
                        supply_fig.add_trace(go.Scatter(
                            x=list(range(simulation_months + 1)),
                            y=data['supplies'],
                            mode='lines',
                            name=data['model_name']
                        ))

                    supply_fig.update_layout(
                        title="Circulating Supply Comparison",
                        xaxis_title="Month",
                        yaxis_title="Circulating Supply",
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1
                        )
                    )

                    st.plotly_chart(supply_fig, use_container_width=True)

                with tabs[2]:
                    mcap_fig = go.Figure()
                    for data in market_cap_data:
                        mcap_fig.add_trace(go.Scatter(
                            x=list(range(simulation_months + 1)),
                            y=data['market_caps'],
                            mode='lines',
                            name=data['model_name']
                        ))

                    mcap_fig.update_layout(
                        title="Market Cap Comparison",
                        xaxis_title="Month",
                        yaxis_title="Market Cap ($)",
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1
                        )
                    )

                    st.plotly_chart(mcap_fig, use_container_width=True)

                # Comparison summary
                st.subheader("Comparison Summary")

                summary_data = []
                for i, model in enumerate(selected_model_objects):
                    final_price = price_data[i]['prices'][-1]
                    initial_price_value = price_data[i]['prices'][0]
                    price_growth = ((final_price / initial_price_value) - 1) * 100

                    max_price = max(price_data[i]['prices'])
                    max_price_month = price_data[i]['prices'].index(max_price)

                    final_mcap = market_cap_data[i]['market_caps'][-1]

                    summary_data.append({
                        'Model': model.name,
                        'Final Price': f"${final_price:.4f}",
                        'Price Growth': f"{price_growth:.2f}%",
                        'Peak Price': f"${max_price:.4f} (Month {max_price_month})",
                        'Final Market Cap': f"${final_mcap:,.2f}"
                    })

                # Create summary dataframe
                summary_df = pd.DataFrame(summary_data)
                st.table(summary_df)

                # Recommendation
                st.subheader("Recommendations")

                # Find best model based on price growth
                best_model_index = [((price_data[i]['prices'][-1] / price_data[i]['prices'][0]) - 1) * 100 for i in range(len(selected_model_objects))].index(max([((price_data[i]['prices'][-1] / price_data[i]['prices'][0]) - 1) * 100 for i in range(len(selected_model_objects))]))
                best_model = selected_model_objects[best_model_index]

                st.markdown(f"**Best Performing Model:** {best_model.name}")
                st.markdown("**Key Insights:**")
                st.markdown("- The best performing model showed higher price stability and growth")
                st.markdown("- Consider optimizing token release schedules to smooth out price volatility")
                st.markdown("- Monitor market cap growth to ensure sustainable valuation")
        else:
            st.info("Please select at least 2 models to compare")

def render_admin_users_page():
    """Render admin user management page"""
    st.title("User Management")

    if not st.session_state.user.get('is_admin', False):
        st.error("You do not have permission to access this page")
        return

    st.subheader("All Users")

    users = db.get_all_users()

    if not users:
        st.info("No users found")
    else:
        # Create dataframe for user display
        user_data = []
        for user in users:
            user_data.append({
                'ID': user.id,
                'Username': user.username,
                'Email': user.email,
                'Display Name': user.display_name,
                'Plan': user.plan,
                'Admin': "Yes" if user.is_admin else "No",
                'Created': user.created_at.strftime('%Y-%m-%d')
            })

        user_df = pd.DataFrame(user_data)
        st.dataframe(user_df, use_container_width=True)

        # User actions
        st.subheader("User Actions")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Create New User")

            with st.form("admin_create_user"):
                new_username = st.text_input("Username")
                new_email = st.text_input("Email")
                new_password = st.text_input("Password", type="password")
                new_display_name = st.text_input("Display Name")
                new_plan = st.selectbox("Plan", ["free", "premium", "enterprise"])
                new_is_admin = st.checkbox("Admin User")

                submitted = st.form_submit_button("Create User")

                if submitted:
                    if not new_username or not new_email or not new_password:
                        st.error("All fields are required")
                    else:
                        new_user = db.create_user(
                            new_username,
                            new_email,
                            new_password,
                            display_name=new_display_name,
                            is_admin=new_is_admin,
                            plan=new_plan
                        )

                        if new_user:
                            st.success("User created successfully")
                            st.rerun()
                        else:
                            st.error("Failed to create user")

        with col2:
            st.subheader("Update User")

            user_to_update = st.selectbox(
                "Select User",
                options=[user.id for user in users],
                format_func=lambda x: next(user.username for user in users if user.id == x)
            )

            selected_user = next(user for user in users if user.id == user_to_update)

            with st.form("admin_update_user"):
                update_email = st.text_input("Email", value=selected_user.email)
                update_display_name = st.text_input("Display Name", value=selected_user.display_name or "")
                update_plan = st.selectbox("Plan", ["free", "premium", "enterprise"], index=["free", "premium", "enterprise"].index(selected_user.plan))
                update_is_admin = st.checkbox("Admin User", value=selected_user.is_admin)
                update_password = st.text_input("New Password (leave blank to keep current)", type="password")

                submitted = st.form_submit_button("Update User")

                if submitted:
                    update_data = {
                        'email': update_email,
                        'display_name': update_display_name,
                        'plan': update_plan,
                        'is_admin': update_is_admin
                    }

                    if update_password:
                        update_data['password'] = update_password

                    updated_user = db.update_user(selected_user.id, **update_data)

                    if updated_user:
                        st.success("User updated successfully")
                        st.rerun()
                    else:
                        st.error("Failed to update user")


# Main app render function
def main():
    if not st.session_state.authenticated:
        # User not logged in, show login or registration form
        if st.session_state.current_page == 'register':
            display_registration_form()
        else:
            display_login_form()
    else:
        # User is logged in, show appropriate content
        render_sidebar()

        # Hero Section (New Homepage Content)
        st.markdown("""
        <div class="hero-section">
            <h1>TokenomicsLab Innovation</h1>
            <p style="font-size: 1.2rem;">Revolucionando o Design de Tokenomics para Web3</p>
        </div>
        """, unsafe_allow_html=True)

        # Main Features Section
        st.markdown("<h2 class='section-header'>Recursos Principais</h2>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div class="feature-card">
                <h3>Token Supply & Distribution</h3>
                <p>Design inteligente da distribuição de tokens com visualizações avançadas</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="feature-card">
                <h3>Simulação Econômica</h3>
                <p>Modele diferentes cenários econômicos para seu token</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class="feature-card">
                <h3>Análise de Mercado</h3>
                <p>Insights profundos sobre tendências e comportamento do mercado</p>
            </div>
            """, unsafe_allow_html=True)

        # Platform Benefits
        st.markdown("<h2 class='section-header'>Por que TokenomicsLab?</h2>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div class="feature-card">
                <h3>Design Intuitivo</h3>
                <p>Interface amigável e ferramentas poderosas para criar tokenomics eficientes</p>
            </div>
            <div class="feature-card">
                <h3>Análise Avançada</h3>
                <p>Ferramentas de simulação e análise para otimizar seu modelo econômico</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="feature-card">
                <h3>Suporte Completo</h3>
                <p>Guias detalhados e recursos educacionais para cada etapa</p>
            </div>
            <div class="feature-card">
                <h3>Integração Web3</h3>
                <p>Conecte-se facilmente com outras ferramentas e plataformas Web3</p>
            </div>
            """, unsafe_allow_html=True)

        # Call to Action
        st.markdown("""
        <div style="text-align: center; margin: 3rem 0;">
            <h2>Comece Agora</h2>
            <p>Transforme suas ideias em um modelo tokenômico sólido</p>
            <a href="#" class="cta-button">Iniciar Projeto</a>
        </div>
        """, unsafe_allow_html=True)


        if st.session_state.current_page == 'dashboard':
            render_dashboard()
        elif st.session_state.current_page == 'projects':
            render_projects_page()
        elif st.session_state.current_page == 'new_project':
            render_new_project_page()
        elif st.session_state.current_page == 'model_comparison':
            render_model_comparison_page()
        elif st.session_state.current_page == 'admin_users':
            render_admin_users_page()
        else:
            # Default to dashboard for any unimplemented pages
            render_dashboard()

if __name__ == "__main__":
    main()