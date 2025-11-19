# app.py
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import io
from datetime import datetime

st.set_page_config(page_title="Eco-Interact Simulator", layout="centered")

# --- Simple CSS Styling (uses Streamlit markdown with unsafe HTML) ---
st.markdown("""
<style>
.header {
  background: linear-gradient(90deg,#2b8cff,#69e6a5);
  padding: 18px;
  border-radius: 12px;
  color: white;
  text-align: center;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.card {
  background: #ffffff;
  padding: 12px;
  border-radius: 10px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  margin-bottom: 12px;
}
.small {
  font-size: 14px;
  color: #444;
}
</style>
<div class="header">
  <h1>Eco-Interact — Biotic & Abiotic Interaction Simulator</h1>
  <div class="small">Adjust abiotic parameters and observe modeled impacts on plants, animals, and ecosystem stability.</div>
</div>
""", unsafe_allow_html=True)

st.write("")  # spacing

# --- Sidebar controls ---
with st.sidebar:
    st.header("Simulation Controls")
    temp = st.slider("Temperature (°C)", min_value=-10.0, max_value=50.0, value=25.0, step=0.5)
    co2 = st.slider("CO₂ concentration (ppm)", min_value=250, max_value=1000, value=415, step=5)
    rainfall = st.slider("Monthly rainfall (mm)", min_value=0, max_value=1000, value=120, step=5)
    humidity = st.slider("Relative humidity (%)", min_value=0, max_value=100, value=60, step=1)
    soil_ph = st.slider("Soil pH", min_value=3.5, max_value=9.0, value=6.8, step=0.1)
    disturbance = st.selectbox("Human disturbance level", ["Low", "Moderate", "High"])
    run_sim = st.button("Run Simulation")

# Default simulation run when user first loads
if not run_sim:
    st.info("Adjust sliders in the left panel and click **Run Simulation**.")

# --- Helper model functions (simple interpretable formulas) ---
def plant_growth_index(temp, co2, rainfall, humidity, soil_ph):
    # Optimal ranges for a generic plant species
    # Score components scaled to 0-100
    # Temperature effect (optimal 20-30C)
    t_score = max(0, 100 - abs(temp - 25) * 4)
    # CO2 effect (benefit up to a point, then saturates)
    c_score = np.clip((co2 - 250) / (1000 - 250) * 100, 0, 100)
    # Rainfall effect (optimal around 50-300 mm monthly)
    r_score = max(0, 100 - (max(0, rainfall - 175) + max(0, 50 - rainfall)) * 0.25)
    # Humidity effect (optimal 40-80)
    h_score = max(0, 100 - abs(humidity - 60) * 1.5)
    # Soil pH effect optimal ~6.5-7.5
    ph_score = max(0, 100 - abs(soil_ph - 7.0) * 25)
    # Weighted sum
    idx = 0.28*t_score + 0.18*c_score + 0.22*r_score + 0.17*h_score + 0.15*ph_score
    return np.clip(idx, 0, 100)

def animal_survival_prob(temp, rainfall, humidity, plant_index, disturbance):
    # Animals depend on vegetation; disturbance reduces survival
    d_factor = {"Low": 1.0, "Moderate": 0.8, "High": 0.6}[disturbance]
    # Temperature suitability (optimal 15-30)
    t = max(0, 100 - abs(temp - 22) * 3)
    # Rainfall broad support
    r = max(0, 100 - abs(rainfall - 120) * 0.3)
    # Humidity
    h = max(0, 100 - abs(humidity - 55) * 1.2)
    base = 0.5 * (t + r) * 0.01 + 0.5 * h * 0.01
    # incorporate plant availability
    base = base * (0.5 + 0.5*(plant_index/100))
    prob = base * d_factor * 100
    return np.clip(prob, 0, 100)

def ecosystem_stability(plant_index, animal_prob, disturbance):
    # Stability roughly average of plant and animal metrics reduced by disturbance
    d_penalty = {"Low": 0, "Moderate": 10, "High": 25}[disturbance]
    base = (plant_index + animal_prob) / 2
    stab = base - d_penalty
    return np.clip(stab, 0, 100)

# --- Run simulation when requested ---
if run_sim:
    plant_index = plant_growth_index(temp, co2, rainfall, humidity, soil_ph)
    animal_prob = animal_survival_prob(temp, rainfall, humidity, plant_index, disturbance)
    stability = ecosystem_stability(plant_index, animal_prob, disturbance)

    # Summary cards
    col1, col2, col3 = st.columns(3)
    col1.metric("Plant Growth Index", f"{plant_index:.1f}/100")
    col2.metric("Animal Survival Prob.", f"{animal_prob:.1f}%")
    col3.metric("Ecosystem Stability", f"{stability:.1f}/100")

    st.markdown("<div class='card'><b>Interpretation:</b></div>", unsafe_allow_html=True)

    # Interpretations
    if plant_index > 70:
        st.success("Plants are likely to thrive under these abiotic conditions.")
    elif plant_index > 40:
        st.info("Plants will grow moderately; some stress expected.")
    else:
        st.warning("Plants will struggle — consider changes in abiotic factors or conservation measures.")

    if animal_prob > 65:
        st.success("Animal populations likely sustainable.")
    elif animal_prob > 35:
        st.info("Animal survival is uncertain; population fluctuations possible.")
    else:
        st.warning("Animal survival probability is low — risk of local decline/extirpation.")

    if stability > 65:
        st.success("Ecosystem appears stable.")
    elif stability > 40:
        st.info("Ecosystem is moderately stable but vulnerable to shocks.")
    else:
        st.error("Ecosystem stability is low — high risk of collapse with further stressors.")

    # Time series simulation: vary one abiotic param to show sensitivity
    st.subheader("Sensitivity visualization")
    vary_param = st.selectbox("Vary parameter for sensitivity plot", ["Temperature", "CO₂", "Rainfall", "Humidity", "Soil pH"])
    n = 60
    if vary_param == "Temperature":
        xs = np.linspace(-5, 45, n)
        y = [plant_growth_index(x, co2, rainfall, humidity, soil_ph) for x in xs]
        df = pd.DataFrame({"Temperature (°C)": xs, "Plant Growth Index": y})
        fig = px.line(df, x="Temperature (°C)", y="Plant Growth Index", title="Plant index vs Temperature")
    elif vary_param == "CO₂":
        xs = np.linspace(250, 1000, n)
        y = [plant_growth_index(temp, x, rainfall, humidity, soil_ph) for x in xs]
        df = pd.DataFrame({"CO₂ (ppm)": xs, "Plant Growth Index": y})
        fig = px.line(df, x="CO₂ (ppm)", y="Plant Growth Index", title="Plant index vs CO₂")
    elif vary_param == "Rainfall":
        xs = np.linspace(0, 800, n)
        y = [plant_growth_index(temp, co2, x, humidity, soil_ph) for x in xs]
        df = pd.DataFrame({"Rainfall (mm/mo)": xs, "Plant Growth Index": y})
        fig = px.line(df, x="Rainfall (mm/mo)", y="Plant Growth Index", title="Plant index vs Rainfall")
    elif vary_param == "Humidity":
        xs = np.linspace(0, 100, n)
        y = [plant_growth_index(temp, co2, rainfall, x, soil_ph) for x in xs]
        df = pd.DataFrame({"Humidity (%)": xs, "Plant Growth Index": y})
        fig = px.line(df, x="Humidity (%)", y="Plant Growth Index", title="Plant index vs Humidity")
    else:
        xs = np.linspace(3.5, 9.0, n)
        y = [plant_growth_index(temp, co2, rainfall, humidity, x) for x in xs]
        df = pd.DataFrame({"Soil pH": xs, "Plant Growth Index": y})
        fig = px.line(df, x="Soil pH", y="Plant Growth Index", title="Plant index vs Soil pH")

    st.plotly_chart(fig, use_container_width=True)

    # Show the current parameter table
    st.subheader("Simulation parameters & numeric results")
    table = {
        "Parameter": ["Temperature (°C)", "CO₂ (ppm)", "Rainfall (mm/mo)", "Humidity (%)", "Soil pH", "Human disturbance"],
        "Value": [temp, co2, rainfall, humidity, soil_ph, disturbance]
    }
    st.table(pd.DataFrame(table))

    results_df = pd.DataFrame({
        "Metric": ["Plant Growth Index", "Animal Survival Probability (%)", "Ecosystem Stability"],
        "Value": [f"{plant_index:.2f}", f"{animal_prob:.2f}", f"{stability:.2f}"]
    })
    st.table(results_df)

    # --- Full Project Report (downloadable) ---
    st.subheader("Full Project Report (copy-paste ready)")
    report_text = f"""
Eco-Interact: Biotic–Abiotic Interaction Simulation Portal
---------------------------------------------------------
Date: {datetime.now().strftime('%Y-%m-%d')}

1. Title
Eco-Interact — Biotic and Abiotic Component Simulator: Need for Environmental Awareness

2. Objective
To build an interactive simulator to visualize how abiotic factors (temperature, CO₂ concentration, rainfall, humidity, soil pH, and human disturbance) influence biotic components (plant growth and animal survival) and overall ecosystem stability.

3. Tools & Technologies
- Python 3.x
- Streamlit
- Plotly
- NumPy, Pandas

4. System Design & Modules
- UI / Controls: sliders and selectors for abiotic inputs.
- Model Engine: deterministic, interpretable formulas to calculate Plant Growth Index, Animal Survival Probability, Ecosystem Stability.
- Visualization: interactive charts to show sensitivity.
- Reporting: downloadable project report and numeric tables.

5. Methodology
- Define optimal ranges for generic plant and animal metrics.
- Use weighted linear combination and distance-from-optimum penalties to compute indices (0–100).
- Integrate human disturbance as a multiplicative penalty on animal survival and stability.
- Provide sensitivity plots by varying one abiotic parameter while holding others constant.

6. Algorithms & Formulas (summary)
- Plant Growth Index = weighted sum of sub-scores for temperature, CO₂, rainfall, humidity, soil pH (scaled to 0–100).
- Animal Survival Probability = function of temperature, rainfall, humidity, plant availability and disturbance.
- Ecosystem Stability = mean(Plant Index, Animal Prob) - Disturbance penalty.

7. UI Screens & Flow
- Sidebar: inputs (sliders)
- Main: metrics, interpretation messages, sensitivity chart, tables, download.

8. Expected Outcomes
- Demonstrable relationship between abiotic stressors and biotic responses.
- Awareness messages for conservation decisions.

9. Limitations
- The model is illustrative and generic; species-specific responses vary.
- No stochastic population dynamics or spatial modeling included.

10. Extensions (future work)
- Add species-specific modules, stochastic population dynamics, GIS-based spatial layers, real climate data ingestion, multi-species food webs.

11. Conclusion
The Eco-Interact portal provides an educational, interactive way to see how abiotic changes affect ecosystems, promoting environmental awareness.

12. Code & Deployment
- Single-file Streamlit app (app.py).
- Requirements: streamlit, plotly, pandas, numpy.

"""
    st.text_area("Report (editable)", value=report_text, height=350)
    # Download button (txt)
    st.download_button("Download report (.txt)", data=report_text.encode("utf-8"), file_name="Eco-Interact_Project_Report.txt", mime="text/plain")

    st.success("Simulation completed. Use the parameters to explore scenarios. To deploy, follow the instructions in the repository README or the steps in this app's documentation.")

# --- Footer ---
st.markdown("<div style='padding:10px; font-size:12px; color:#666'>Made for MCA minor project — interactive educational simulator</div>", unsafe_allow_html=True)
