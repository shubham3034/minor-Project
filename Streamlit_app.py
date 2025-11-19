import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------------
# CSS STYLING
# ---------------------------------------------
st.markdown("""
    <style>
    .title {
        text-align: center;
        font-size: 40px;
        color: #2E8B57;
        font-weight: 800;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        font-size: 22px;
        color: #444;
        margin-top: -10px;
        margin-bottom: 30px;
    }
    .card {
        padding: 15px;
        background: #f0f8f5;
        border-radius: 10px;
        border: 1px solid #c7e5d0;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------
# PAGE TITLE
# ---------------------------------------------
st.markdown("<div class='title'>Eco-System Simulation Web App</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Biotic & Abiotic Interaction Visualizer</div>", unsafe_allow_html=True)


# ---------------------------------------------
# INPUT SECTION
# ---------------------------------------------
st.markdown("### 🔧 Adjust Abiotic Factors")

temp = st.slider("🌡 Temperature (°C)", 0, 50, 25)
rain = st.slider("🌧 Rainfall (mm)", 0, 300, 120)
co2 = st.slider("🟩 CO₂ Level (ppm)", 200, 800, 400)
ph = st.slider("🧪 Soil pH", 1.0, 14.0, 7.0)


# ---------------------------------------------
# SIMULATION MODEL (Simple Rule-Based)
# ---------------------------------------------
def plant_growth(temp, rain, co2, ph):
    score = 100
    score -= abs(temp - 25) * 2
    score -= abs(rain - 120) * 0.3
    score -= abs(ph - 7) * 8
    score += (co2 - 350) * 0.05
    return max(0, min(100, int(score)))

def biodiversity(temp, rain, ph):
    score = 90
    score -= abs(temp - 22) * 1.5
    score -= abs(rain - 150) * 0.2
    score -= abs(ph - 6.8) * 5
    return max(0, min(100, int(score)))

def ecosystem_stability(pg, bd):
    return int((pg + bd) / 2)


pg = plant_growth(temp, rain, co2, ph)
bd = biodiversity(temp, rain, ph)
es = ecosystem_stability(pg, bd)


# ---------------------------------------------
# RESULTS SECTION
# ---------------------------------------------
st.markdown("### 📊 Simulation Results")
col1, col2, col3 = st.columns(3)

col1.markdown(f"<div class='card'><h3>🌱 Plant Growth</h3><h2>{pg}%</h2></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='card'><h3>🦋 Biodiversity</h3><h2>{bd}%</h2></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='card'><h3>🌍 Ecosystem Stability</h3><h2>{es}%</h2></div>", unsafe_allow_html=True)


# ---------------------------------------------
# AWARENESS MESSAGE
# ---------------------------------------------
st.markdown("### 🌿 Awareness Insight")

if es > 80:
    st.success("The ecosystem is stable. Current abiotic conditions support rich plant and animal life.")
elif es > 50:
    st.warning("The ecosystem is moderately stable. Minor environmental imbalances detected.")
else:
    st.error("The ecosystem is unstable. Abiotic factors are outside optimal ranges.")


# ---------------------------------------------
# GRAPH SECTION
# ---------------------------------------------
st.markdown("### 📈 Visualization")

labels = ["Plant Growth", "Biodiversity", "Stability"]
values = [pg, bd, es]

fig, ax = plt.subplots()
ax.bar(labels, values)
ax.set_ylim(0, 100)
ax.set_ylabel("Score (%)")
ax.set_title("Ecosystem Health Parameters")

st.pyplot(fig)
