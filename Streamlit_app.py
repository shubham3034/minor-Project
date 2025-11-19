import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Environmental Impact & Awareness Portal",
    page_icon="🌱",
    layout="wide",
)

# -------------------------------
# TITLE
# -------------------------------
st.title("🌍 Environmental Impact Calculator & Awareness Portal")
st.write("This tool helps users understand how daily human activities affect biotic and abiotic components of the environment.")

# -------------------------------
# SIDEBAR MENU
# -------------------------------
menu = st.sidebar.radio(
    "Navigation",
    ["Home", "Environmental Calculator", "Biotic & Abiotic Info", "Awareness Tips"]
)

# -------------------------------
# HOME PAGE
# -------------------------------
if menu == "Home":
    st.header("🌱 Introduction")
    st.write("""
    Environmental awareness is the foundation of conserving biotic and abiotic components.
    
    **Biotic components** include:
    - Plants  
    - Animals  
    - Microorganisms  

    **Abiotic components** include:
    - Air  
    - Water  
    - Soil  
    - Temperature  
    - Sunlight  

    This project provides:
    - A calculator to show how your lifestyle affects the environment  
    - Educational content  
    - Awareness-building tips  
    """)

# -------------------------------
# ENVIRONMENTAL IMPACT CALCULATOR
# -------------------------------
elif menu == "Environmental Calculator":
    st.header("♻️ Environmental Impact Calculator")

    st.write("Enter your daily habits to estimate environmental impact.")

    col1, col2 = st.columns(2)

    with col1:
        electricity = st.number_input("Daily Electricity Usage (kWh)", 0.0, 50.0, 5.0)
        water = st.number_input("Daily Water Usage (litres)", 0.0, 2000.0, 200.0)

    with col2:
        travel = st.number_input("Daily Travel Distance (km)", 0.0, 200.0, 10.0)
        waste = st.number_input("Daily Waste Generated (kg)", 0.0, 10.0, 1.0)

    if st.button("Calculate Impact"):
        # Simple environmental impact scoring formula
        impact_score = (electricity * 0.8) + (water * 0.02) + (travel * 1.2) + (waste * 5)

        st.subheader("Your Daily Environmental Impact Score:")
        st.success(f"**{impact_score:.2f} points**")

        # Chart Data
        df = pd.DataFrame({
            "Component": ["Electricity", "Water", "Travel", "Waste"],
            "Impact Value": [
                electricity * 0.8,
                water * 0.02,
                travel * 1.2,
                waste * 5
            ]
        })

        fig = px.bar(df, x="Component", y="Impact Value", title="Environmental Impact Breakdown")
        st.plotly_chart(fig)

# -------------------------------
# EDUCATION SECTION
# -------------------------------
elif menu == "Biotic & Abiotic Info":
    st.header("📘 Biotic & Abiotic Components")

    st.subheader("🌿 Biotic Components (Living)")
    st.info("""
    - Plants  
    - Animals  
    - Microorganisms  
    - Humans  
    """)
    
    st.subheader("🌎 Abiotic Components (Non-living)")
    st.info("""
    - Air  
    - Water  
    - Soil  
    - Temperature  
    - Light  
    - Minerals  
    """)

    st.write("""
    Both components interact constantly. Disruption in abiotic factors (pollution, climate change)
    affects biotic life and ecological balance.
    """)

# -------------------------------
# AWARENESS TIPS SECTION
# -------------------------------
elif menu == "Awareness Tips":
    st.header("🌟 Environmental Awareness Tips")

    tips = [
        "Reduce electricity usage by turning off unused appliances.",
        "Use public transport or carpool whenever possible.",
        "Avoid single-use plastics.",
        "Recycle household waste.",
        "Plant at least one tree every year.",
        "Save water by reducing shower time.",
        "Use energy-efficient lighting.",
        "Support eco-friendly brands."
    ]

    for t in tips:
        st.markdown(f"✔️ {t}")
