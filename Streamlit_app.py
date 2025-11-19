import streamlit as st

# Set page title and icon
st.set_page_config(page_title="Biotic & Abiotic Environment", page_icon="🌍")

# Title and introduction
st.title("Biotic and Abiotic Components of Environment")
st.subheader("An Interactive Awareness Initiative")

# Sidebar for navigation
option = st.sidebar.selectbox(
    "Choose a section", 
    ["Introduction", "Biotic Components", "Abiotic Components", "Awareness Quiz", "How You Can Help"]
)

# Introduction Section
if option == "Introduction":
    st.markdown("""
    ### What is Environment?
    The environment consists of biotic (living) and abiotic (non-living) components that interact and support all life forms.
    - **Biotic**: Plants, animals, microorganisms.
    - **Abiotic**: Air, water, soil, sunlight, temperature.
    """)
    st.image("https://images.unsplash.com/photo-1503551723145-6c040742065b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8ZW52aXJvbm1lbnR8ZW58MHx8MHx8fDA%3D&w=1000&q=80", caption="Nature and Environment")

# Biotic Components Section
elif option == "Biotic Components":
    st.markdown("""
    ### Biotic Components (Living)
    - **Producers**: Plants (make food via photosynthesis).
    - **Consumers**: Animals (herbivores, carnivores, omnivores).
    - **Decomposers**: Fungi, bacteria (break down dead matter).
    - **Examples**: Trees, birds, fish, insects, humans.
    """)
    st.image("https://images.unsplash.com/photo-1505238680356-667803448bb6?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8ZmxvcmF8ZW58MHx8MHx8fDA%3D&w=1000&q=80", caption="Biotic Diversity")

# Abiotic Components Section
elif option == "Abiotic Components":
    st.markdown("""
    ### Abiotic Components (Non-Living)
    - **Air**: Essential for respiration and photosynthesis.
    - **Water**: Supports all life forms.
    - **Soil**: Provides nutrients and support for plants.
    - **Sunlight**: Energy source for photosynthesis.
    - **Temperature & Climate**: Affect ecosystem dynamics.
    """)
    st.image("https://images.unsplash.com/photo-1505238680356-667803448bb6?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8ZmxvcmF8ZW58MHx8MHx8fDA%3D&w=1000&q=80", caption="Abiotic Factors")

# Awareness Quiz Section
elif option == "Awareness Quiz":
    st.markdown("### Test Your Knowledge")
    q1 = st.radio("Which of the following is a biotic factor?", ["Rainfall", "Plants", "Soil", "Air"])
    q2 = st.radio("Which is an abiotic factor?", ["Birds", "Sunlight", "Fish", "Trees"])
    q3 = st.radio("Which component recycles nutrients in the ecosystem?", ["Sunlight", "Water", "Decomposers", "Air"])

    if st.button("Submit Quiz"):
        score = 0
        if q1 == "Plants":
            score += 1
        if q2 == "Sunlight":
            score += 1
        if q3 == "Decomposers":
            score += 1
        st.success(f"Your score: {score}/3")
        if score == 3:
            st.balloons()
            st.markdown("🎉 Excellent! You understand the environment well.")
        elif score >= 1:
            st.markdown("Good effort! Keep learning about the environment.")
        else:
            st.markdown("Keep exploring! The environment is fascinating.")

# How You Can Help Section
elif option == "How You Can Help":
    st.markdown("""
    ### Environmental Awareness Tips
    - Reduce, reuse, and recycle waste.
    - Conserve water and energy.
    - Plant trees and maintain green spaces.
    - Avoid single-use plastics.
    - Spread awareness and join local eco-friendly initiatives.
    """)
    st.image("https://images.unsplash.com/photo-1505238680356-667803448bb6?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8ZmxvcmF8ZW58MHx8MHx8fDA%3D&w=1000&q=80", caption="Go Green")

# Footer
st.sidebar.info("Created by MCA Student - Minor Project using Python & Streamlit")
