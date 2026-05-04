import requests
from scout_logic import analyze_job, is_junk_title
from scraper_tools import get_full_desc
import time
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv('ADZUNA_APP_ID')
APP_KEY = os.getenv('ADZUNA_APP_KEY')
DATABASE_URL = os.getenv('DB_URL')

master_list = []
ground_total = 0

current_page = 1

while True:
    print(f" \n--- Page {current_page} ---\n")

    base_url = f"https://api.adzuna.com/v1/api/jobs/at/search/{current_page}"

    query_params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "what": "data engineer",
        "results_per_page": 50,
        "content-type": "application/json",
    }

    print(f"Fetching data for page {current_page}...")

    response = requests.get(base_url, params=query_params)
    if response.status_code == 200:
        page_matches = []
        print("Success!")
        data = response.json()
        # Adzuna puts the jobs inside a list called 'results'
        jobs = data.get('results', [])

        if len(jobs) == 0:
            break

        jobs_found = 0
        for job in jobs:
            prepared_job = {
                'title': job.get('title'),
                'desc': job.get('description'),
                'link': job.get('redirect_url')
            }

            if is_junk_title(prepared_job) is True:
                continue

            prepared_job['desc'] = get_full_desc(prepared_job['link'])
            if prepared_job['desc'] is None:
                continue

            result = analyze_job(prepared_job)
            if result is not None and result['is_junior'] == True:
                master_list.append(result)
                page_matches.append(result)
                ground_total += 1
                jobs_found += 1


        if len(page_matches) > 0:
            print(f"Found {len(page_matches)} matches for page {current_page}")
            for match in page_matches:
                print(match)

        print(f"Page {current_page}: Analyzed {len(jobs)} jobs, found {jobs_found} relevant jobs")
    else:
        print(f"Failed to connect. Status Code: {response.status_code}")
        print(f"Error Message: {response.text}")

    current_page += 1

    time.sleep(2)

print(f"Found {ground_total} relevant jobs")


if len(master_list) > 0:
    raw_scouted_jobs = pd.DataFrame(master_list)

    engine = create_engine(DATABASE_URL)


    raw_scouted_jobs.to_sql('job_scout_db', engine, index=False, if_exists='append')



























