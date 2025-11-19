import streamlit as st

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(page_title="GreenScore Calculator", page_icon="🌿", layout="wide")

st.title("🌍 GreenScore – Personal Environmental Impact Calculator")
st.write("""
This simple tool calculates your daily environmental impact score based on 
your lifestyle habits such as water usage, electricity consumption, fuel usage, and waste generation.  
A lower score means a greener lifestyle.
""")

st.divider()

# ---------------------------------------------------
# USER INPUT SECTION
# ---------------------------------------------------
st.header("📥 Enter Your Daily Usage")

col1, col2 = st.columns(2)

with col1:
    water = st.slider("Daily Water Usage (Liters)", 20, 500, 100)
    electricity = st.slider("Daily Electricity Usage (kWh)", 1, 50, 10)

with col2:
    fuel = st.slider("Daily Fuel Usage (Liters)", 0, 20, 2)
    waste = st.slider("Daily Waste Generated (kg)", 0, 5, 1)

st.divider()

# ---------------------------------------------------
# SCORE CALCULATION
# ---------------------------------------------------
st.header("📊 Your GreenScore")

# Lower is better
score = (
    (water / 500) * 25 +
    (electricity / 50) * 25 +
    (fuel / 20) * 25 +
    (waste / 5) * 25
)

score = round(score, 2)

# ---------------------------------------------------
# SCORE DISPLAY
# ---------------------------------------------------
if score <= 25:
    remark = "🌟 Excellent! Very Eco-friendly Lifestyle."
    color = "green"
elif score <= 50:
    remark = "👍 Good. Some improvements can be made."
    color = "orange"
elif score <= 75:
    remark = "⚠️ Not great. Start reducing your environmental footprint."
    color = "red"
else:
    remark = "🚨 High impact! Immediate lifestyle changes recommended."
    color = "darkred"

st.markdown(
    f"""
    <div style='padding:15px; background-color:{color}; color:white; border-radius:10px;'>
        <h2 style='text-align:center;'>GreenScore: {score} / 100</h2>
        <h4 style='text-align:center;'>{remark}</h4>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# ---------------------------------------------------
# RECOMMENDATIONS
# ---------------------------------------------------
st.header("💡 Personalized Recommendations")

st.write("Based on your impact score, here are some tips:")

if score <= 25:
    st.success("You are already following a very sustainable lifestyle. Keep inspiring others!")
elif score <= 50:
    st.write("""
    - Reduce unnecessary water usage  
    - Switch to LED lights  
    - Use public transport more often  
    - Recycle plastic and paper  
    """)
elif score <= 75:
    st.write("""
    - Reduce shower duration  
    - Turn off appliances when not needed  
    - Carpool or use bicycles  
    - Start composting organic waste  
    """)
else:
    st.write("""
    - Immediately reduce water & electricity usage  
    - Consider renewable energy sources  
    - Avoid single-use plastics completely  
    - Use public transport or electric alternatives  
    """)

st.divider()

# ---------------------------------------------------
# ABOUT THE PROJECT
# ---------------------------------------------------
st.header("📚 About This Project")
st.write("""
This tool helps users understand how their everyday habits affect the environment.
It promotes awareness about ecological balance by scoring lifestyle choices
based on water, energy, fuel, and waste consumption.
""")

st.info("You can host this online on Streamlit Cloud using this exact file.")

