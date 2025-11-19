import streamlit as st
import pandas as pd
import random

# --- Quiz Data Structure ---
quiz_data = [
    {
        "question": "Which of these is an **abiotic** component essential for plant growth?",
        "options": ["Worms", "Decomposers", "Sunlight", "Fungi"],
        "answer": "Sunlight",
        "topic": "Abiotic"
    },
    {
        "question": "Organisms that produce their own food (like plants) are called what?",
        "options": ["Consumers", "Producers", "Decomposers", "Scavengers"],
        "answer": "Producers",
        "topic": "Biotic"
    },
    {
        "question": "Temperature, wind, and rainfall are all examples of what kind of factor?",
        "options": ["Biotic", "Anthropogenic", "Abiotic", "Geological"],
        "answer": "Abiotic",
        "topic": "Abiotic"
    },
    {
        "question": "What role do **bacteria and fungi** primarily play in an ecosystem?",
        "options": ["Primary Consumers", "Producers", "Decomposers", "Predators"],
        "answer": "Decomposers",
        "topic": "Biotic"
    }
]

# --- Streamlit App Functions ---

def main_page():
    """Defines the main content and navigation structure."""
    
    st.set_page_config(
        page_title="Environmental Awareness Project",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.sidebar.title("App Navigation")
    selection = st.sidebar.radio("Go to:", ["Home & Concepts", "Interactive Quiz", "Awareness & Action"])
    
    st.title("🌱 Biotic & Abiotic Components: Environmental Awareness")
    
    st.markdown("---")
    
    if selection == "Home & Concepts":
        display_concepts()
    elif selection == "Interactive Quiz":
        run_quiz()
    elif selection == "Awareness & Action":
        display_awareness()

def display_concepts():
    """Displays informational content about biotic and abiotic components."""
    
    st.header("1. Core Environmental Concepts")
    st.info("The **environment** is a complex system defined by the interplay between living and non-living elements. Understanding this interaction is key to global sustainability.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🌿 Biotic Components (The Living Factors)")
        st.markdown("""
        These include all **living or once-living** organisms in an ecosystem. They can be categorized by their role in the food chain:
        * **Producers:** (e.g., Plants, Algae) Create their own food via photosynthesis.
        * **Consumers:** (e.g., Animals) Rely on other organisms for food.
        * **Decomposers:** (e.g., Bacteria, Fungi) Break down dead matter, recycling nutrients.
        """)
        # If you want to add an image later, use: st.image("your_image_name.png", caption="Food Web Diagram")
        
    with col2:
        st.subheader("🧊 Abiotic Components (The Non-Living Factors)")
        st.markdown("""
        These are the **non-living chemical and physical** parts of the environment that influence living organisms. They provide the fundamental conditions for life.
        * **Energy:** Sunlight (primary source).
        * **Climate:** Temperature, humidity, wind, rainfall.
        * **Substances:** Water, Oxygen, Carbon Dioxide, Soil/Minerals.
        """)
        # If you want to add an image later, use: st.image("your_image_name.png", caption="Abiotic Factors")
    
    st.markdown("---")
    st.header("2. The Need for Awareness")
    st.warning("Ecosystems thrive on **equilibrium**. Human activities often disrupt the balance of biotic (e.g., deforestation) and abiotic (e.g., pollution affecting air quality) components, leading to major environmental crises.")

def run_quiz():
    """Handles the interactive quiz logic and scoring."""
    
    st.header("🧠 Test Your Knowledge: Environmental Quiz")
    
    if 'score' not in st.session_state:
        st.session_state.score = 0
        st.session_state.attempted = 0
    
    st.metric("Current Score", f"{st.session_state.score}/{len(quiz_data)}")

    # Display quiz questions
    st.markdown("---")
    
    # Shuffle questions to make it feel fresh each run
    random.shuffle(quiz_data)
    
    for i, q in enumerate(quiz_data):
        st.subheader(f"Question {i+1}: {q['question']}")
        
        # Use a unique key for each question's radio button and check button
        radio_key = f"q_radio_{i}"
        check_key = f"q_check_{i}"
        
        # Check if the question has been answered in the current session state
        answered_key = f"q_answered_{i}"
        if answered_key not in st.session_state:
            st.session_state[answered_key] = False

        user_choice = st.radio("Select your answer:", q['options'], key=radio_key, disabled=st.session_state[answered_key])
        
        if not st.session_state[answered_key]:
            if st.button("Submit Answer", key=check_key):
                st.session_state[answered_key] = True  # Mark as answered
                st.session_state.attempted += 1

                if user_choice == q['answer']:
                    st.success("✅ Correct! That's a great understanding of environmental factors.")
                    st.session_state.score += 1
                else:
                    st.error(f"❌ Incorrect. The correct answer is: **{q['answer']}**")
                
                # Update the score metric immediately
                st.experimental_rerun() # Reruns the script to update the score display

    st.markdown("---")
    # Only show the final results if all questions have been attempted
    if st.session_state.attempted == len(quiz_data) and len(quiz_data) > 0:
        st.balloons()
        final_percentage = (st.session_state.score / len(quiz_data)) * 100
        st.metric("Final Quiz Result", f"{st.session_state.score}/{len(quiz_data)} ({final_percentage:.1f}%)")
        st.write("Congratulations on completing the quiz! Your knowledge is a powerful tool for environmental advocacy.")
    elif st.session_state.attempted > 0:
        st.info(f"You have answered {st.session_state.attempted} out of {len(quiz_data)} questions.")


def display_awareness():
    """Provides statistics and calls to action for environmental awareness."""
    
    st.header("🌍 Be the Change: Practical Environmental Action")
    st.subheader("Why Awareness Matters")
    st.markdown("""
    Environmental awareness is the understanding of the environment and the threats it faces. It translates knowledge into **responsible action**.
    """)
    
    st.markdown("---")
    
    st.subheader("Simple Steps You Can Take:")
    
    steps = {
        "Reduce": "Minimize consumption, buy durable goods, and avoid single-use plastics.",
        "Reuse": "Find new purposes for old items (upcycling).",
        "Recycle": "Properly sort waste to conserve natural resources and energy.",
        "Refuse": "Say NO to products that harm the environment (e.g., plastic bags, excessive packaging).",
    }
    
    for action, detail in steps.items():
        st.success(f"**{action}:** {detail}")
        
    st.markdown("---")
    
    st.subheader("Further Reading & Resources")
    st.write("Explore reputable sources like the UN Environment Programme (UNEP) and local conservation groups to stay informed and find volunteer opportunities.")
    
# --- Run the App ---
if __name__ == "__main__":
    main_page()
