import streamlit as st
import pdfplumber

from database import (
    get_roles,
    get_role_skills,
    get_role_average_salary,
    get_role_opportunities
)

from resume_extractor import (
    extract_email,
    extract_phone,
    extract_name,
    extract_skills
)

from career_engine import calculate_match



st.set_page_config(
    page_title="Job Market Intelligence Platform",
    layout="wide"
)

st.markdown("""
# 🚀 Job Market Intelligence Platform

### Resume Analyzer
""")

# -----------------------------
# Role Selection
# -----------------------------

roles = get_roles()

target_role = st.selectbox(
    "🎯 Select Your Target Role",
    roles
)

# -----------------------------
# Resume Upload
# -----------------------------

uploaded_file = st.file_uploader(
    "📄 Upload Your Resume (PDF)",
    type=["pdf"]
)

if uploaded_file:

    st.success(
        "Resume Uploaded Successfully"
    )

    text = ""

    with pdfplumber.open(uploaded_file) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    # -----------------------------
    # Resume Information
    # -----------------------------

    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)

    # -----------------------------
    # Skills Detection
    # -----------------------------

    skills = extract_skills(text)

    # -----------------------------
    # Role Analysis
    # -----------------------------

    required_skills = get_role_skills(
        target_role
    )

    average_salary = get_role_average_salary(
        target_role
    )

    opportunities = get_role_opportunities(
        target_role
    )

    match_score, matched_skills, missing_skills = calculate_match(
        skills,
        required_skills
    )


    # -----------------------------
    # Dashboard KPI Section
    # -----------------------------

    st.subheader("📊 Career Intelligence Dashboard")

    kpi1, kpi2, kpi3,= st.columns(3)

    kpi1.metric(
        "Match Score",
        f"{match_score}%"
    )

    kpi2.metric(
        "Average Salary",
        f"{average_salary} LPA"
    )

    kpi3.metric(
        "Target Role",
        target_role
    )

    st.markdown("---")

    # -----------------------------
    # Resume Information
    # -----------------------------

    st.subheader("👤 Resume Information")

    col1, col2, col3 = st.columns(3)

    col1.info(f"Name\n\n{name}")
    col2.info(f"Email\n\n{email}")
    col3.info(f"Phone\n\n{phone}")

    st.markdown("---")

    # -----------------------------
    # Skills Section
    # -----------------------------

    skills_col, missing_col = st.columns(2)

    with skills_col:

        st.subheader("✅ Detected Skills")

        for skill in skills:
            st.success(skill)

    with missing_col:

        st.subheader("❌ Missing Skills")

        for skill in missing_skills:
            st.warning(skill)

    st.markdown("---")

    # -----------------------------
    # Required Skills
    # -----------------------------

    st.subheader(
        f"📚 Required Skills For {target_role}"
    )

    for skill in required_skills:
        st.info(skill)

    st.markdown("---")

    # -----------------------------
    # Matched Skills
    # -----------------------------

    st.subheader("🎯 Matched Skills")

    for skill in matched_skills:
        st.success(skill)

    st.markdown("---")

    # -----------------------------
    # Relevant Opportunities
    # -----------------------------

    st.subheader("💼 Relevant Opportunities")

    if opportunities:

        for company, city in opportunities:

            st.info(
                f"{company} - {city}"
            )

    else:

        st.warning(
            "No opportunities found for this role."
        )

    st.markdown("---")

    # -----------------------------
    # Recommendations
    # -----------------------------

    st.subheader("💡 Recommendations")

    if len(missing_skills) == 0:

        st.success(
            "Excellent! Your resume already matches this role very well."
        )

    else:

        for skill in missing_skills[:5]:

            st.write(
                f"• Learn {skill} to improve your ATS score and match percentage."
            )

    st.markdown("---")

    # -----------------------------
    # Resume Summary
    # -----------------------------

    st.subheader("📝 Resume Summary")

    summary = f"""
🎯 Target Role: {target_role}

📊 Match Score: {match_score}%

💰 Average Salary: {average_salary} LPA

📚 Missing Skills: {len(missing_skills)}

Focus on improving the missing skills to increase
your chances of getting shortlisted.
"""

    st.info(summary)