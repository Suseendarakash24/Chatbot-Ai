def calculate_match(
    resume_skills,
    required_skills
):

    matched = []

    missing = []

    for skill in required_skills:

        if skill in resume_skills:
            matched.append(skill)
        else:
            missing.append(skill)

    if len(required_skills) == 0:
        return 0, [], []

    score = (
        len(matched)
        /
        len(required_skills)
    ) * 100

    return round(score, 2), matched, missing