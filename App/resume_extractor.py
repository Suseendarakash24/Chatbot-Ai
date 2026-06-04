import re


def extract_email(text):

    emails = re.findall(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    return emails[0] if emails else "Not Found"


def extract_phone(text):

    phones = re.findall(
        r"\+?\d[\d\s\-]{8,15}",
        text
    )

    return phones[0] if phones else "Not Found"


def extract_name(text):

    lines = text.split("\n")

    for line in lines[:5]:

        if len(line.strip()) > 3:

            return line.strip()

    return "Not Found"


def extract_skills(text):

    skills_master = [

        "Python",
        "SQL",
        "Power BI",
        "Excel",
        "Java",
        "JavaScript",
        "React",
        "Node.js",
        "AWS",
        "Azure",
        "Docker",
        "Kubernetes",
        "Machine Learning",
        "Data Analysis",
        "Pandas",
        "NumPy",
        "Git",
        "HTML",
        "CSS",
        "Tableau",
        "Statistics",
        "TensorFlow",
        "PyTorch",
        "Linux",
        "MongoDB",
        "MySQL",
        "PostgreSQL",
        "Flask",
        "Django"
    ]

    found_skills = []

    text_lower = text.lower()

    for skill in skills_master:

        if skill.lower() in text_lower:

            found_skills.append(skill)

    return sorted(list(set(found_skills)))


def skill_gap_analysis(
    resume_skills,
    required_skills
):

    missing = []

    for skill in required_skills:

        if skill not in resume_skills:

            missing.append(skill)

    return missing