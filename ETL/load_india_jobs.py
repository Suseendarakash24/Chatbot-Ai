import pandas as pd
import mysql.connector

 

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2428",
    database="job_market_intelligence"
)

cursor = conn.cursor()

 
# READ DATASET
 

df = pd.read_csv(
    r"D:\JobMarketIntelligence\Data\india_job_market_2024_2026.csv"
)

print("Rows Loaded:", len(df))

 
# DIM COMPANY
 

companies = df[["Company", "Company_Type"]].drop_duplicates()

company_map = {}

for _, row in companies.iterrows():

    cursor.execute(
        """
        INSERT INTO dim_company
        (company_name, company_type)
        VALUES (%s,%s)
        """,
        (
            row["Company"],
            row["Company_Type"]
        )
    )

    company_map[row["Company"]] = cursor.lastrowid

 
# DIM CITY
 

cities = df[
    ["City", "Location_Tier"]
].drop_duplicates()

city_map = {}

for _, row in cities.iterrows():

    cursor.execute(
        """
        INSERT INTO dim_city
        (city_name, location_tier)
        VALUES (%s,%s)
        """,
        (
            row["City"],
            row["Location_Tier"]
        )
    )

    city_map[row["City"]] = cursor.lastrowid

 
# DIM INDUSTRY
 

industries = df[
    ["Industry"]
].drop_duplicates()

industry_map = {}

for _, row in industries.iterrows():

    cursor.execute(
        """
        INSERT INTO dim_industry
        (industry_name)
        VALUES (%s)
        """,
        (
            row["Industry"],
        )
    )

    industry_map[row["Industry"]] = cursor.lastrowid

 
# FACT JOBS
 

for _, row in df.iterrows():

    cursor.execute(
        """
        INSERT INTO fact_jobs
        (
        job_id,
        job_title,
        company_id,
        city_id,
        industry_id,
        experience_level,
        job_type,
        work_mode,
        salary_lpa,
        openings,
        applicants,
        company_rating,
        education_required,
        date_posted
        )

        VALUES
        (
        %s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,
        %s,%s,%s,%s
        )
        """,

        (
            row["Job_ID"],
            row["Job_Title"],

            company_map[row["Company"]],
            city_map[row["City"]],
            industry_map[row["Industry"]],

            row["Experience_Level"],
            row["Job_Type"],
            row["Work_Mode"],

            row["Salary_LPA"],

            row["Openings"],
            row["Applicants"],

            row["Company_Rating"],

            row["Education_Required"],

            row["Date_Posted"]
        )
    )

conn.commit()

print("FACT JOBS LOADED")

cursor.close()
conn.close()