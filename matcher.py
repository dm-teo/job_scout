import json
from sqlalchemy import create_engine, text
import pandas as pd
import re

def get_matches(target_link):
    profile_data = json.load(open('my_profile.json'))

    engine = create_engine('postgresql://postgres:postmarsql062005_dbadmin@localhost:5432/job_scout_db')



    query = text("""
        select * from analytics.fct_job_leads where link = :target_link;
    """)

    df = pd.read_sql(query, engine, params={'target_link': target_link})

    if df.empty:
        print("Error: Job link not found in database")
        return None

    job_desc = df['description'].iloc[0].lower()

    print(job_desc)

    matched_skills = []
    remaining_skills = []
    for family in profile_data['skill_families']:
        keywords_to_check = family['search_keywords']
        if any(re.search(r'\b' + re.escape(kw.lower()) + r'\b', job_desc) for kw in keywords_to_check):
            matched_skills.append(family)
        else:
            remaining_skills.append(family)

    final_skills = matched_skills + remaining_skills

    relevant_projects = [profile_data['projects'][0]]
    for project in profile_data['projects'][1:]:
        if any(re.search(r'\b' + re.escape(kw.lower()) + r'\b', job_desc) for kw in project['keywords']):
            relevant_projects.append(project)

    return final_skills, relevant_projects, profile_data
