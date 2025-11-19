import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import altair as alt # For better interactive charts

# --- 1. Data Generation and Model Training ---

@st.cache_resource # Cache the model training for fast reloading
def train_model():
    """Generates synthetic data and trains a Linear Regression model."""
    
    # 1. Simulate the Abiotic/Biotic Data
    np.random.seed(42)
    N = 100 # Number of samples (monitoring days)

    # Abiotic Input Variables (X)
    data = pd.DataFrame({
        'pH': np.round(np.random.uniform(6.0, 8.5, N), 1),
        'DO_mgL': np.round(np.random.uniform(3.0, 12.0, N), 1), # Dissolved Oxygen
        'Temp_C': np.round(np.random.uniform(10.0, 30.0, N), 1),
        'Nitrates_ppm': np.round(np.random.uniform(0.5, 15.0, N), 1)
    })

    # Biotic Output Variable (Y) - Ecosystem Health Score (0-10)
    # The score is negatively affected by high Temp/Nitrates and positively by high pH/DO.
    # We add random noise to simulate real-world variability.
    health_score = (
        2 * data['DO_mgL'] 
        + 1.5 * data['pH'] 
        - 0.5 * data['Temp_C'] 
        - 0.8 * data['Nitrates_ppm']
        + np.random.normal(loc=0, scale=1.5, size=N) # Noise
    )
    # Scale the score to roughly fit 0-10 range and clip
    data['Health_Score'] = np.clip(health_score / 2, 0, 10).round(2)
    
    # 2. Prepare Data for Model
    X = data[['pH', 'DO_mgL', 'Temp_C', 'Nitrates_ppm']]
    Y = data['Health_Score']

    # Split data (though less crucial for this simple demo, good practice)
    X_train, _, Y_train, _ = train_test_split(X, Y, test_size=0.2, random_state=42)
    
    # 3. Train Model
    model = LinearRegression()
    model.fit(X_train, Y_train)
    
    return model, X, Y, data

# Train the model and get data when the app starts
model, X_df, Y_df, full_data = train_model()

# --- 2. Streamlit Application Functions ---

def display_model_insights():
    """Displays the statistical results of the model."""
    
    st.header("Model Insights: Abiotic Factor Influence")
    
    # Calculate R-squared and MSE on the training data
    Y_pred_train = model.predict(X_df)
    r2 = r2_score(Y_df, Y_pred_train)
    mse = mean_squared_error(Y_df, Y_pred_train)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Model $R^2$ Score (Accuracy)", f"{r2:.3f}")
        st.caption("A value closer to 1.0 indicates that the abiotic factors explain a large portion of the variance in the Health Score.")
        
    with col2:
        st.metric("Mean Squared Error (MSE)", f"{mse:.3f}")
        st.caption("Lower values indicate better prediction accuracy. The scale depends on the Health Score range (0-10).")

    st.subheader("Factor Coefficients (Impact Analysis)")
    
    # Create a DataFrame for easy viewing of coefficients
    coefficients_df = pd.DataFrame({
        'Abiotic Factor': X_df.columns,
        'Coefficient Value': model.coef_.round(3)
    })
    
    # Determine the impact type based on the sign
    coefficients_df['Impact on Health'] = coefficients_df['Coefficient Value'].apply(
        lambda x: "Positive (Beneficial)" if x > 0 else "Negative (Harmful)"
    )
    
    st.dataframe(coefficients_df.sort_values('Coefficient Value', ascending=False), 
                 use_container_width=True, 
                 hide_index=True)
    
    st.markdown("""
    > **Interpretation:** The magnitude and sign of the Coefficient Value show the factor's influence. For example, a **positive coefficient** for **DO** means that as Dissolved Oxygen increases, the Health Score *increases*, indicating a **beneficial** effect on aquatic biota.
    """)
    

def run_predictor():
    """Interactive section where users can set abiotic values to predict health."""
    
    st.header("Interactive Abiotic Predictor (The 'What-If' Tool)")
    st.info("Adjust the abiotic conditions below and see the predicted health of the aquatic ecosystem.")
    
    # --- Input Sliders ---
    st.subheader("Set Abiotic Conditions:")
    
    # Use columns for a compact layout
    col_sliders = st.columns(4)
    
    with col_sliders[0]:
        user_pH = st.slider("Water pH", min_value=6.0, max_value=8.5, value=7.5, step=0.1)
    
    with col_sliders[1]:
        user_DO = st.slider("Dissolved Oxygen (mg/L)", min_value=3.0, max_value=12.0, value=7.0, step=0.1)
        
    with col_sliders[2]:
        user_Temp = st.slider("Water Temperature (°C)", min_value=10.0, max_value=30.0, value=20.0, step=0.1)
        
    with col_sliders[3]:
        user_Nitrates = st.slider("Nitrates (ppm)", min_value=0.5, max_value=15.0, value=5.0, step=0.1)
    
    # --- Prediction ---
    
    # Prepare user input for the model
    user_input = pd.DataFrame({
        'pH': [user_pH],
        'DO_mgL': [user_DO],
        'Temp_C': [user_Temp],
        'Nitrates_ppm': [user_Nitrates]
    })
    
    predicted_health = model.predict(user_input)[0]
    
    st.markdown("---")
    
    # --- Output & Awareness Message ---
    
    health_score_display = f"{predicted_health:.2f} / 10"
    
    # Define thresholds for awareness messaging
    if predicted_health > 7.5:
        st.success(f"## Predicted Ecosystem Health: HIGH ({health_score_display})")
        st.markdown("### 🐠 Excellent conditions! Biotic diversity and health are maximized under these favorable abiotic factors.")
    elif predicted_health > 5.0:
        st.warning(f"## Predicted Ecosystem Health: MODERATE ({health_score_display})")
        st.markdown("### 🐟 Stress detected. One or more abiotic factors are nearing critical limits. Monitoring is required.")
    else:
        st.error(f"## Predicted Ecosystem Health: POOR ({health_score_display})")
        st.markdown("### 💀 **DANGER!** These abiotic conditions (low DO, high Nitrates/Temp) are highly stressful and unsustainable for most aquatic biota. **Urgent action is needed.**")


def display_eda():
    """Displays exploratory data analysis visualizations."""
    
    st.header("Exploratory Data Analysis (EDA)")
    st.markdown("View the correlation between a key abiotic input and the biotic health score across the dataset.")
    
    # Interactive selection for X-axis variable
    x_var = st.selectbox(
        "Select Abiotic Factor to Correlate with Health Score:",
        ['DO_mgL', 'pH', 'Temp_C', 'Nitrates_ppm']
    )
    
    # Altair Scatter Plot
    chart = alt.Chart(full_data).mark_circle(size=60).encode(
        x=alt.X(x_var, title=x_var + (' (mg/L)' if x_var == 'DO_mgL' else ' (°C)' if x_var == 'Temp_C' else '')),
        y=alt.Y('Health_Score', title='Ecosystem Health Score (0-10)'),
        tooltip=[x_var, 'Health_Score'],
        color=alt.Color('Health_Score', scale=alt.Scale(range=['red', 'yellow', 'green']))
    ).properties(
        title=f'Relationship between {x_var} and Ecosystem Health'
    ).interactive() # Add interactive zooming/panning
    
    # Add a trend line (simple linear fit)
    trend_line = chart.transform_regression(x_var, 'Health_Score').mark_line(color='blue')
    
    st.altair_chart(chart + trend_line, use_container_width=True)

# --- 3. Main Streamlit App Layout ---

def main():
    st.set_page_config(
        page_title="Abiotic Impact Case Study",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.sidebar.title("Aquatic Ecosystem Analysis")
    st.sidebar.markdown("This project uses a predictive model to demonstrate how key non-living (abiotic) factors influence the living (biotic) health of a river.")
    
    selection = st.sidebar.radio(
        "Go to:", 
        ["Case Study Overview", "Interactive Predictor", "Model Insights & EDA"]
    )
    
    st.title("🌊 Abiotic Stress: A Case Study on Aquatic Ecosystem Health")
    st.markdown("---")

    if selection == "Case Study Overview":
        st.header("Case Study: Modeling River Health")
        st.markdown("""
        The health of an aquatic ecosystem (like a river) is directly tied to its **abiotic components**. This study simulates environmental monitoring data to show the quantitative impact of factors like **Dissolved Oxygen ($\text{DO}$), $\text{pH}$, Temperature, and Pollutants (Nitrates)** on a calculated **Ecosystem Health Score** (representing biotic components like fish and invertebrate diversity).
        
        This model utilizes **Multiple Linear Regression** to quantify these relationships, serving as a powerful tool for **environmental awareness**.
        """)
        
        st.subheader("Simulated Dataset Snapshot")
        st.dataframe(full_data.head(10), use_container_width=True)
        st.caption(f"Total {len(full_data)} data points simulated. Data ranges are based on typical river health parameters.")
        
    elif selection == "Interactive Predictor":
        run_predictor()
        
    elif selection == "Model Insights & EDA":
        display_model_insights()
        st.markdown("---")
        display_eda()

# Run the app
if __name__ == "__main__":
    main()
