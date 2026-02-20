import streamlit as st
from llm import generate_learning_path
from recommendation import recommend_courses

st.set_page_config(page_title="AI Learning Path Generator", layout="wide")

st.title("🎓 AI Learning Path Generator")
st.write("Get a personalized roadmap based on your level, interests, and career goals.")

# --- User Inputs ---
col1, col2 = st.columns(2)

with col1:
    level = st.selectbox(
        "Your Current Level",
        ["Beginner", "Intermediate", "Advanced"]
    )

    interests = st.text_input(
        "Your Interests (comma separated)",
        placeholder="e.g. Machine Learning, Python, Data Science"
    )

with col2:
    goal = st.text_area(
        "Your Career Goal",
        placeholder="e.g. Become an AI Engineer in 6 months"
    )

# --- Generate Button ---
if st.button("🚀 Generate Learning Path"):

    if not level or not interests or not goal:
        st.warning("Please fill all fields.")
    else:
        with st.spinner("Generating your personalized roadmap..."):

            result = generate_learning_path(level, interests, goal)

        st.success("Learning Path Generated!")

        st.markdown("## 🗺 Your Structured Roadmap")
        st.write(result)
