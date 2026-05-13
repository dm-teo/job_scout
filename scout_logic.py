import re

from sqlalchemy import desc


def is_junk_title(job_data):
    title = job_data['title'].lower()
    garbage_titles = ["frontend", "react", "css", "javascript", "senior", "lead", "architect", "head", "principal", "manager", "director", "phd", "vp", "scientist", "chemical", "laboratory", "expertin"]

    if any(word in title for word in garbage_titles):
        return True
    return False

def analyze_job(job_data):
    title = job_data['title'].lower()
    if job_data['desc'] is None:
        return None
    else:
        desc = job_data['desc'].lower()
        restriction = ["zugriff", "verweigert"]
        if any(word in desc for word in restriction):
            return None
    score = 0


    skill_keywords = ['sql', 'mysql', 'postgres', 'python', 'dbt', 'database', 'data modeller', 'data engineer', 'ETL', 'Automation']

    junior_words = ["junior", "intern", "entry", "trainee", "internship", "working student", "graduate"]

    pattern = re.compile(r'\b([3-9]|1(0-9))\s*(years|jahre|yrs)\b', re.IGNORECASE)
    if re.search(pattern, desc):
        score -= 100
        return None

    junior_pattern = re.compile(r'\b(0|1|2|no|none|zero)\s*(years|jahre|experience|berufserfahrung)\b', re.IGNORECASE)

    if any(word in title or word in desc for word in junior_words) or re.search(junior_pattern, desc):
        is_junior = True
    else:
        return None

    is_remote = "remote" in desc or "home office" in desc or "hybrid" in desc

    for word in skill_keywords:
        if word in desc:
            score += 10

    return {
        "title": job_data['title'],
        "is_junior": is_junior,
        "is_remote": is_remote,
        "score": score,
        "link": job_data['link'],
        "description": job_data['desc']
    }





