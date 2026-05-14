import streamlit as st
import pandas as pd

st.set_page_config(page_title="Interview Readiness Evaluator", page_icon="🎯", layout="wide")

# Title
st.title("🎯 AI Interview Readiness Evaluator")
st.subheader("Get your Interview Readiness Score in under 2 minutes!")

st.write("Rate yourself quickly and receive personalized suggestions.")

# Sidebar
st.sidebar.header("Candidate Profile")
name = st.sidebar.text_input("Enter your Name")
role = st.sidebar.selectbox(
    "Target Role",
    ["Software Developer", "Data Analyst", "AI Engineer", "Web Developer", "Cloud Engineer"]
)

# Main Form
with st.form("assessment_form"):

    st.header("1️⃣ Technical Skills")
    technical = st.slider("Rate your technical knowledge", 1, 10, 5)
    coding = st.slider("Problem-solving / coding confidence", 1, 10, 5)

    st.header("2️⃣ Resume Assessment")
    resume_updated = st.radio("Is your resume updated?", ["Yes", "No"])
    ats_friendly = st.radio("Is your resume ATS-friendly?", ["Yes", "No"])

    st.header("3️⃣ Communication Skills")
    communication = st.slider("Communication confidence", 1, 10, 5)
    mock_interview = st.radio("Have you attended mock interviews?", ["Yes", "No"])

    st.header("4️⃣ Portfolio")
    portfolio = st.radio("Do you have a portfolio/GitHub/Projects?", ["Yes", "No"])
    project_quality = st.slider("Project quality confidence", 1, 10, 5)

    submit = st.form_submit_button("Evaluate Now")

def calculate_score():
    score = 0

    # Technical
    score += technical * 4
    score += coding * 4

    # Resume
    if resume_updated == "Yes":
        score += 10
    if ats_friendly == "Yes":
        score += 10

    # Communication
    score += communication * 3
    if mock_interview == "Yes":
        score += 10

    # Portfolio
    if portfolio == "Yes":
        score += 10
    score += project_quality * 3

    return min(score, 100)

def generate_feedback(score):
    feedback = []

    if technical < 6:
        feedback.append("Improve technical concepts and coding practice.")

    if coding < 6:
        feedback.append("Practice DSA/problem-solving daily.")

    if resume_updated == "No":
        feedback.append("Update your resume with latest achievements.")

    if ats_friendly == "No":
        feedback.append("Make your resume ATS-friendly using proper keywords.")

    if communication < 6:
        feedback.append("Practice speaking, mock HR interviews, and confidence building.")

    if mock_interview == "No":
        feedback.append("Attend mock interviews to improve confidence.")

    if portfolio == "No":
        feedback.append("Create a GitHub portfolio or showcase projects.")

    if project_quality < 6:
        feedback.append("Build stronger real-world projects.")

    if score >= 80:
        level = "Excellent 🚀"
    elif score >= 60:
        level = "Good 👍"
    elif score >= 40:
        level = "Average ⚠️"
    else:
        level = "Needs Improvement ❌"

    return level, feedback

if submit:
    if not name:
        st.warning("Please enter your name.")
    else:
        score = calculate_score()
        level, feedback = generate_feedback(score)

        st.success(f"{name}, your Interview Readiness Score is: {score}/100")

        st.metric("Overall Readiness", level)

        st.progress(score / 100)

        st.subheader("📊 Score Breakdown")
        breakdown = pd.DataFrame({
            "Category": ["Technical Skills", "Resume", "Communication", "Portfolio"],
            "Approx Score": [
                technical * 8,
                (10 if resume_updated == "Yes" else 0) + (10 if ats_friendly == "Yes" else 0),
                (communication * 3) + (10 if mock_interview == "Yes" else 0),
                (10 if portfolio == "Yes" else 0) + (project_quality * 3)
            ]
        })

        st.table(breakdown)

        st.subheader("💡 Personalized Improvement Plan")
        for item in feedback:
            st.write("✅", item)

        if score >= 80:
            st.balloons()