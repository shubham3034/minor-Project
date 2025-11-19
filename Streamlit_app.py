import streamlit as st
import pandas as pd
import numpy as np

# --- 1. Ecosystem Health Model Parameters ---
# Define weights and optimal ranges based on environmental science principles.
# The weights quantify the relative importance of each abiotic factor on biotic health.
WEIGHTS = {
    'pH': 1.5,           # Positive impact, moderate weight
    'DO_mgL': 2.5,       # Strongest positive impact (crucial for aquatic life)
    'Temp_C': -1.0,      # Negative impact, moderate weight
    'Nitrates_ppm': -2.0 # Strongest negative impact (pollution)
}

# Optimal/Acceptable ranges for calculating the score contribution
RANGES = {
    'pH': {'optimal_low': 6.5, 'optimal_high': 7.5},
    'DO_mgL': {'optimal_low': 6.0, 'optimal_high': 12.0},
    'Temp_C': {'optimal_low': 10.0, 'optimal_high': 20.0},
    'Nitrates_ppm': {'optimal_low': 0.0, 'optimal_high': 5.0}
}

# --- 2. Core Health Calculation Function ---

def calculate_health_score(pH, DO_mgL, Temp_C, Nitrates_ppm):
    """
    Calculates the Ecosystem Health Score (0-10) based on weighted deviations
    from optimal abiotic conditions.
    """
    
    # 1. Initialize Score and Maximum Possible Score
    score = 0
    max_score = sum(abs(w) for w in WEIGHTS.values()) # Total weight magnitude
    
    # 2. Calculate contribution for each factor
    
    # pH Contribution (Positive Factor)
    pH_range = RANGES['pH']
    if pH >= pH_range['optimal_low'] and pH <= pH_range['optimal_high']:
        score += WEIGHTS['pH']
    elif pH > pH_range['optimal_high'] or pH < pH_range['optimal_low']:
        # Score decreases linearly as pH moves away from optimal center (7.0)
        deviation = abs(pH - 7.0)
        score += WEIGHTS['pH'] * max(0.0, 1.0 - deviation / 1.5) # Scale deviation
        
    # Dissolved Oxygen (DO) Contribution (Critical Positive Factor)
    DO_range = RANGES['DO_mgL']
    if DO_mgL >= DO_range['optimal_low']:
        score += WEIGHTS['DO_mgL']
    elif DO_mgL < DO_range['optimal_low']:
        # Score decreases sharply below critical threshold (e.g., 6.0 mg/L)
        score += WEIGHTS['DO_mgL'] * (DO_mgL / DO_range['optimal_low']) * 0.5
        
    # Temperature (Temp_C) Contribution (Negative Factor)
    Temp_range = RANGES['Temp_C']
    if Temp_C <= Temp_range['optimal_high']:
        score += abs(WEIGHTS['Temp_C'])
    else:
        # Score decreases linearly as temperature rises above optimal
        deviation = Temp_C - Temp_range['optimal_high']
        score += abs(WEIGHTS['Temp_C']) * max(0.0, 1.0 - deviation / 15.0)
        
    # Nitrates (Nitrates_ppm) Contribution (Critical Negative Factor/Pollution)
    Nitrate_range = RANGES['Nitrates_ppm']
    if Nitrates_ppm <= Nitrate_range['optimal_high']:
        score += abs(WEIGHTS['Nitrates_ppm'])
    else:
        # Score decreases sharply as nitrates rise above critical threshold
        deviation = Nitrates_ppm - Nitrate_range['optimal_high']
        score += abs(WEIGHTS['Nitrates_ppm']) * max(0.0, 1.0 - deviation / 20.0)
        
    # 3. Normalize and Scale (0-10)
    # Total score is calculated based on how many "points" were achieved relative to the max possible.
    final_score = np.clip((score / max_score) * 10, 0.0, 10.0)
    
    return final_score

# --- 3. Streamlit Application Layout ---

def main():
    st.set_page_config(
        page_title="Abiotic Impact Calculator",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("⚖️ Abiotic Balance: Interactive Ecosystem Health Calculator")
    st.subheader("MCA Minor Project: Demonstrating Environmental Sensitivity")
    st.markdown("---")
    
    st.sidebar.title("App Navigation")
    selection = st.sidebar.radio("Go to:", ["Ecosystem Calculator", "Model and Awareness"])

    if selection == "Ecosystem Calculator":
        run_calculator()
    elif selection == "Model and Awareness":
        display_awareness_and_model()


def run_calculator():
    """Interactive section where users set abiotic values to calculate health."""
    
    st.header("Interactive Abiotic Condition Setter")
    st.info("Adjust the abiotic parameters below to see the immediate effect on the calculated Ecosystem Health Score. This demonstrates the fragility of the biotic environment.")
    
    # --- Input Sliders ---
    col_sliders = st.columns(4)
    
    with col_sliders[0]:
        user_pH = st.slider("Water pH (Optimal 6.5-7.5)", min_value=5.0, max_value=9.0, value=7.0, step=0.1)
    
    with col_sliders[1]:
        user_DO = st.slider("Dissolved Oxygen (mg/L) (Critical > 6.0)", min_value=2.0, max_value=15.0, value=7.5, step=0.1)
        
    with col_sliders[2]:
        user_Temp = st.slider("Water Temperature (°C) (Stress > 20)", min_value=5.0, max_value=35.0, value=20.0, step=0.1)
        
    with col_sliders[3]:
        user_Nitrates = st.slider("Nitrates (ppm) (Pollution > 5.0)", min_value=0.0, max_value=30.0, value=2.0, step=0.1)
    
    # --- Calculation and Output ---
    
    # Call the core calculation function
    predicted_health = calculate_health_score(user_pH, user_DO, user_Temp, user_Nitrates)
    
    st.markdown("---")
    
    health_score_display = f"{predicted_health:.2f} / 10"
    
    # --- Output & Awareness Message ---
    
    if predicted_health > 7.5:
        st.success(f"## Predicted Ecosystem Health: HIGH ({health_score_display})")
        st.markdown("### 🐠 **Excellent conditions.** Biotic health is maximized. This represents a well-preserved ecosystem.")
    elif predicted_health > 5.0:
        st.warning(f"## Predicted Ecosystem Health: MODERATE ({health_score_display})")
        st.markdown("### ⚠️ **Stress Detected.** Some abiotic factors are out of the optimal range. Sensitive biotic components (like trout or certain insects) are likely suffering.")
    else:
        st.error(f"## Predicted Ecosystem Health: POOR ({health_score_display})")
        st.markdown("### 💀 **CRITICAL DANGER!** These abiotic conditions (likely low DO, high Nitrates, or high Temp) are lethal to most aquatic life. This is a severe pollution or climate stress event.")
    
    

def display_awareness_and_model():
    """Displays model explanation and awareness info."""
    
    st.header("Model Explanation: The Power of Weights")
    st.markdown("""
    This calculator uses a **Weighted Score Model** based on established environmental science to show the impact of abiotic changes. Each factor is given a weight based on its biological importance:
    """)
    
    weights_df = pd.DataFrame(WEIGHTS.items(), columns=['Abiotic Factor', 'Weight/Impact'])
    weights_df['Type'] = weights_df['Weight/Impact'].apply(lambda x: "Positive (Health Booster)" if x > 0 else "Negative (Stress/Pollution)")
    
    st.dataframe(weights_df, use_container_width=True, hide_index=True)
    
    st.markdown("""
    * **$\text{DO}$ and $\text{Nitrates}$** have the highest weights because Dissolved Oxygen is vital for respiration, and excess Nitrates indicate critical pollution (eutrophication).
    * The final score is a reflection of how far the input values deviate from the established **Optimal Ranges**.
    """)
    
    st.markdown("---")
    
    st.header("🌍 Environmental Awareness: The Call to Action")
    st.markdown("""
    **Awareness is Action.** This simulation highlights how small abiotic changes can have massive impacts on biotic components. To maintain a **HIGH** health score in nature:
    
    * **Manage Runoff:** Reduce the use of fertilizers and limit soil erosion to control Nitrate pollution.
    * **Protect Riparian Zones:** Planting trees and vegetation near water bodies helps regulate temperature and filter pollutants, directly improving **Temp\_C** and **Nitrates\_ppm**.
    * **Educate:** Share the critical relationship between $\text{DO}$ and aquatic life to gain support for conservation efforts.
    """)

# --- Run the App ---
if __name__ == "__main__":
    main()
