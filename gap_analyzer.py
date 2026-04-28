import json
import re
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text

engine = create_engine('postgresql://postgres:postmarsql062005_dbadmin@localhost:5432/job_scout_db')
tech_data = json.load(open('tech_dictionary.json'))
my_data = json.load(open('my_profile.json'))

query = text("""
    select description from analytics.stg_jobs
""")

df = pd.read_sql_query(query, engine)
descriptions = df['description'].tolist()
big_blob = " ".join(descriptions)

market_demand = {}
tech_gap = {}

print(f"Analyzing {len(big_blob)} characters of job data...")

for categ_name, tech_list in tech_data.items():
    for tech in tech_list:
        pattern = r'\b' + re.escape(tech) + r'\b'
        count = len(re.findall(pattern, big_blob, re.IGNORECASE))
        market_demand[tech] = count

owned_skills = []
for family in my_data['skill_families']:
    for skill in family['skills_to_show']:
        owned_skills.append(skill)

for skill in market_demand:
    if skill not in owned_skills and market_demand[skill] > 5:
        tech_gap[skill] = market_demand[skill]

gap_df = pd.DataFrame(list(tech_gap.items()), columns=['Tech', 'Mentions'])
gap_df = gap_df.sort_values(by='Mentions', ascending=False)

plt.figure(figsize=(12, 6))
sns.barplot(data=gap_df, x='Mentions', y='Tech', palette='viridis')
plt.title("Top Technology Gaps in the Austrian IT Market")
plt.tight_layout()
plt.savefig("tech_gap.png")
plt.close()


print(gap_df.head(10))