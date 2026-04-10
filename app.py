import streamlit as st
import random

# --- CONFIGURATION & DATA ---
# In a real app, you would load this from a JSON or Database
PYQ_DATA = [
    {"id": 1, "class": 11, "subject": "Math", "topic": "Trigonometry", "shift": "24 Jan 2026 S1", "difficulty": 1, "q": "Find the value of...", "options": ["A", "B", "C", "D"], "correct": "A", "solution": "Detailed steps for Trig..."},
    {"id": 2, "class": 11, "subject": "Math", "topic": "Conics", "shift": "27 Jan 2024 S2", "difficulty": 2, "q": "The equation of the parabola is...", "options": ["A", "B", "C", "D"], "correct": "B", "solution": "Using Data 1 formula for conics..."},
    {"id": 3, "class": 12, "subject": "Math", "topic": "Calculus", "shift": "29 Jan 2026 S1", "difficulty": 3, "q": "Integrate the following...", "options": ["A", "B", "C", "D"], "correct": "C", "solution": "Integration by parts..."},
]

def calculate_percentile(score, shift_99_score):
    # Simplified linear estimation for the mock
    percentile = (score / shift_99_score) * 99
    return min(99.99, max(0, percentile))

# --- UI SETUP ---
st.set_page_config(page_title="JEE PYQ Portal", layout="wide")
st.title("🚀 JEE Main PYQ Mock Portal (2021-2026)")

tabs = st.tabs(["📝 Mock Tests", "🤖 AI Doubt Solver", "📊 Performance"])

# --- TAB 1: MOCK TESTS ---
with tabs[0]:
    mode = st.radio("Select Mode", ["Only Class 11", "Full Paper (11+12)"])
    
    # Filter Questions
    if mode == "Only Class 11":
        questions = [q for q in PYQ_DATA if q["class"] == 11]
    else:
        # Sort by difficulty: Easy (1) to Tough (3)
        questions = sorted(PYQ_DATA, key=lambda x: x["difficulty"])

    st.subheader(f"Mock Test: {mode}")
    user_answers = {}

    for i, q in enumerate(questions):
        st.write(f"**Q{i+1}:** {q['q']} :blue[(Shift: {q['shift']})]")
        user_answers[q['id']] = st.radio(f"Select Option for Q{i+1}", q['options'], key=f"q_{q['id']}")
        if st.button(f"View Solution Q{i+1}"):
            st.info(q['solution'])
        st.divider()

    if st.button("Submit Test"):
        score = 0
        for q in questions:
            if user_answers[q['id']] == q['correct']:
                score += 4
            else:
                score -= 1
        
        st.success(f"Your Total Score: {score}/300")
        
        # Display 99%tile stats (Historical Data)
        shift_99 = 185  # Example score for 99%tile in a moderate shift
        st.metric("99%tile Score for this Shift", f"{shift_99} Marks")
        
        my_percentile = calculate_percentile(score, shift_99)
        st.metric("Your Estimated Percentile", f"{my_percentile:.2f}")

# --- TAB 2: AI DOUBT SOLVER ---
with tabs[1]:
    st.header("💬 AI Doubt Solver")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a doubt about a PYQ..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Placeholder for AI Response (Connect to API here)
        response = f"To solve this, use the property from your 'Data 1' notes..."
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
