import mysql.connector


def get_connection():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="2428",
        database="job_market_intelligence"
    )


def get_roles():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT job_title
        FROM fact_jobs
        ORDER BY job_title
    """)

    roles = [row[0] for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    return roles


def get_role_skills(role):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT DISTINCT ds.skill_name

    FROM fact_jobs fj

    JOIN bridge_job_skill bjs
        ON fj.job_id = bjs.job_id

    JOIN dim_skill ds
        ON ds.skill_id = bjs.skill_id

    WHERE fj.job_title = %s
    """

    cursor.execute(query, (role,))

    skills = [row[0] for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    return skills


def get_role_average_salary(role):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT ROUND(
        AVG(salary_lpa),
        2
    )

    FROM fact_jobs

    WHERE job_title = %s
    """

    cursor.execute(query, (role,))

    result = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return result if result else 0


def get_role_opportunities(role):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        dc.company_name,
        dcity.city_name

    FROM fact_jobs fj

    JOIN dim_company dc
        ON fj.company_id = dc.company_id

    JOIN dim_city dcity
        ON fj.city_id = dcity.city_id

    WHERE fj.job_title = %s

    LIMIT 10
    """

    cursor.execute(query, (role,))

    opportunities = cursor.fetchall()

    cursor.close()
    conn.close()

    return opportunities