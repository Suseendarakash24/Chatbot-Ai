import pandas as pd
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2428",
    database="job_market_intelligence"
)

cursor = conn.cursor()

df = pd.read_csv(
    r"D:\JobMarketIntelligence\Data\india_job_market_2024_2026.csv"
)

skill_map = {}

# ---------------------
# LOAD UNIQUE SKILLS
# ---------------------

all_skills = set()

for skills in df["Skills_Required"]:

    for skill in str(skills).split(","):

        skill = skill.strip()

        if skill:
            all_skills.add(skill)

for skill in sorted(all_skills):

    cursor.execute(
        """
        INSERT INTO dim_skill(skill_name)
        VALUES(%s)
        """,
        (skill,)
    )

    skill_map[skill] = cursor.lastrowid

# ---------------------
# BUILD MAP AGAIN
# ---------------------

cursor.execute(
    """
    SELECT skill_id, skill_name
    FROM dim_skill
    """
)

for skill_id, skill_name in cursor.fetchall():

    skill_map[skill_name] = skill_id

# ---------------------
# JOB SKILL BRIDGE
# ---------------------

for _, row in df.iterrows():

    job_id = row["Job_ID"]

    skills = str(
        row["Skills_Required"]
    ).split(",")

    for skill in skills:

        skill = skill.strip()

        if skill:

            cursor.execute(
                """
                INSERT INTO bridge_job_skill
                (
                job_id,
                skill_id
                )
                VALUES(%s,%s)
                """,
                (
                    job_id,
                    skill_map[skill]
                )
            )

conn.commit()

print("SKILLS LOADED")

cursor.close()
conn.close()