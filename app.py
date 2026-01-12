import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ThermoSim: Process Analyzer",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CUSTOM CSS STYLING ---
# This injects custom CSS to change the look and feel (making it unique)
st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1 {
        color: #2E4053; 
        font-family: 'Helvetica Neue', sans-serif;
    }
    .stMetric {
        background-color: #F8F9F9;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #E5E7E9;
    }
    /* Custom button styling */
    div.stButton > button {
        width: 100%;
        background-color: #2874A6;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
    div.stButton > button:hover {
        background-color: #1F618D;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR CONTROLS ---
with st.sidebar:
    st.header("⚙️ Configuration")
    
    process_type = st.selectbox(
        "Thermodynamic Process",
        ["constant_volume", "constant_pressure", "isothermal", "adiabatic", "polytropic"],
        format_func=lambda x: x.replace("_", " ").title()
    )
    
    st.markdown("---")
    
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        T0 = st.number_input("Init Temp ($T_0$)", value=300.0, min_value=273.15, step=10.0, help="Temperature in Kelvin")
    with col_input2:
        V0 = st.number_input("Init Vol ($v_0$)", value=1.0, min_value=0.01, step=0.1, help="Specific Volume in m³/kg")
        
    n_points = st.slider("Resolution (Steps)", 5, 100, 30)
    
    st.markdown("---")
    calc_button = st.button("🚀 Run Simulation")
    
    st.markdown("###### *Powered by CoolProp & FastAPI*")

# --- 4. MAIN DASHBOARD ---
st.title("🔥 ThermoSim: Non-Flow Process Calculator")

# Process Definition Dictionary with LaTeX
process_meta = {
    "constant_volume": {"name": "Isochoric Process", "eq": r"v = C, \quad \frac{P}{T} = C"},
    "constant_pressure": {"name": "Isobaric Process", "eq": r"P = C, \quad \frac{v}{T} = C"},
    "isothermal": {"name": "Isothermal Process", "eq": r"T = C, \quad Pv = C"},
    "adiabatic": {"name": "Adiabatic Process", "eq": r"Pv^\gamma = C, \quad Q = 0"},
    "polytropic": {"name": "Polytropic Process", "eq": r"Pv^n = C"}
}

curr = process_meta[process_type]
st.info(f"**Current Mode:** {curr['name']} — Governing Equation: ${curr['eq']}$")

# --- 5. CALCULATION LOGIC ---
if calc_button:
    # 5a. Backend Connection
    # We use a params dictionary for cleaner URL construction
    api_url = f"http://127.0.0.1:8000/process/{process_type}"
    params = {
        "T0": T0, 
        "V0": V0, 
        "n_points": n_points
    }
    
    with st.spinner("Querying thermodynamic state points..."):
        try:
            response = requests.get(api_url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.ConnectionError:
            st.error("❌ **Connection Failed:** Could not reach the backend. Please ensure `main.py` is running.")
            st.stop()
        except requests.exceptions.RequestException as e:
            st.error(f"❌ **API Error:** {e}")
            st.stop()

    # 5b. Visualization
    if data:
        df = pd.DataFrame(data)
        
        # KEY METRICS ROW
        # We calculate the change (delta) to show trend arrows
        p_start, p_end = df['P'].iloc[0], df['P'].iloc[-1]
        t_start, t_end = df['T'].iloc[0], df['T'].iloc[-1]
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Final Pressure", f"{p_end:.2f} bar", delta=f"{p_end-p_start:.2f} bar")
        m2.metric("Final Temperature", f"{t_end:.1f} K", delta=f"{t_end-t_start:.1f} K")
        m3.metric("Entropy Change", f"{df['s'].iloc[-1]-df['s'].iloc[0]:.4f}", "kJ/kgK")
        m4.metric("Total Steps", f"{len(df)}")
        
        st.markdown("---")

        # TABS LAYOUT for cleaner UI
        tab1, tab2 = st.tabs(["📊 Graphical Analysis", "📋 Data Table"])
        
        with tab1:
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                # T-s Diagram
                fig1 = px.line(df, x="s", y="T", markers=True, 
                               title="<b>Temperature-Entropy (T-s) Diagram</b>",
                               labels={"s": "Entropy (kJ/kg·K)", "T": "Temperature (K)"})
                fig1.update_traces(line_color='#E74C3C', marker=dict(size=6))
                fig1.update_layout(template="simple_white", hovermode="x unified")
                st.plotly_chart(fig1, use_container_width=True)

            with col_chart2:
                # P-v Diagram
                fig2 = px.line(df, x="v", y="P", markers=True, 
                               title="<b>Pressure-Volume (P-v) Diagram</b>",
                               labels={"v": "Specific Volume (m³/kg)", "P": "Pressure (bar)"})
                fig2.update_traces(line_color='#2980B9', marker=dict(size=6))
                fig2.update_layout(template="simple_white", hovermode="x unified")
                st.plotly_chart(fig2, use_container_width=True)

        with tab2:
            st.dataframe(df, use_container_width=True)
            
            # CSV Download
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv,
                file_name=f"{process_type}_process_data.csv",
                mime="text/csv"
            )

else:
    # Initial State / Landing Page Instructions
    st.markdown("""
    ### 👋 Welcome
    Select a **Process Type** from the sidebar and click **Run Simulation** to visualize the thermodynamic path.
    
    This tool calculates state points for water/steam using the **IAPWS-95** formulation via CoolProp.
    """)