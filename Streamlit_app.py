import streamlit as st

# -----------------------------------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------------------------------
st.set_page_config(page_title="Smart Waste Segregation", page_icon="♻️", layout="wide")

st.title("♻️ Smart Waste Segregation Awareness System")
st.write("""
This tool helps users correctly identify the category of waste (Wet, Dry, Hazardous, E-waste) 
and provides proper disposal methods based on the material they enter.
""")

st.divider()

# -----------------------------------------------------------------------------------
# INPUT SECTION
# -----------------------------------------------------------------------------------
st.header("🗑️ Enter the Waste Item")

user_input = st.text_input("Type the name of the waste item:", placeholder="Example: Banana peel, Plastic bottle, Battery")

st.divider()

# -----------------------------------------------------------------------------------
# WASTE CLASSIFICATION LOGIC
# -----------------------------------------------------------------------------------
def classify_waste(item):

    item = item.lower()

    wet = ["food", "banana", "vegetable", "fruit", "peel", "tea", "coffee", "leftover", "flower"]
    dry = ["plastic", "paper", "cardboard", "glass", "can", "bottle", "metal"]
    hazardous = ["battery", "paint", "chemical", "medicine", "thermometer"]
    ewaste = ["mobile", "laptop", "charger", "cable", "earphone", "computer"]

    if any(word in item for word in wet):
        return "Wet Waste", "Use compost bins. Converts into natural fertilizer."
    elif any(word in item for word in dry):
        return "Dry Waste", "Send for recycling. Keep dry and clean before disposal."
    elif any(word in item for word in hazardous):
        return "Hazardous Waste", "Dispose at authorized collection centers. Avoid mixing."
    elif any(word in item for word in ewaste):
        return "E-Waste", "Return to e-waste centers or electronic stores for safe recycling."
    else:
        return "Unknown", "Item not recognized. Try using a more specific name."

# -----------------------------------------------------------------------------------
# OUTPUT SECTION
# -----------------------------------------------------------------------------------
if user_input:
    category, instruction = classify_waste(user_input)

    st.subheader("🧾 Classification Result")
    color = "green" if category != "Unknown" else "red"

    st.markdown(
        f"""
        <div style='padding:20px; background-color:{color}; color:white; border-radius:12px;'>
            <h2 style='text-align:center;'>Category: {category}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("### 📌 Disposal Method")
    st.write(instruction)

st.divider()

# -----------------------------------------------------------------------------------
# EDUCATIONAL SECTION
# -----------------------------------------------------------------------------------
st.header("📘 Waste Categories Explained")

st.write("""
**1. Wet Waste**  
Organic waste like vegetables, fruits, leftover food, flowers, tea waste.

**2. Dry Waste**  
Paper, plastic, cardboard, metals, glass, and packaging materials.

**3. Hazardous Waste**  
Batteries, chemicals, medicines, paints — anything toxic.

**4. E-Waste**  
Electronics such as mobiles, laptops, chargers, earphones, wires.
""")

st.divider()

# -----------------------------------------------------------------------------------
# TIPS
# -----------------------------------------------------------------------------------
st.header("💡 Smart Waste Management Tips")

st.write("""
- Always separate wet and dry waste at home  
- Do not mix batteries or chemicals with general waste  
- Give E-waste only to certified recycling agencies  
- Wash and dry recyclable items before disposal  
- Avoid single-use plastics  
""")

st.divider()

# -----------------------------------------------------------------------------------
# ABOUT THE PROJECT
# -----------------------------------------------------------------------------------
st.header("📚 About This Project")
st.write("""
This system helps promote environmental awareness by teaching proper waste segregation habits.
It identifies waste items and suggests correct disposal methods to reduce pollution.
""")

st.info("This app is optimized for easy deployment on Streamlit Cloud.")
