import requests
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DISCORD_URL = os.getenv("DISCORD_WEBHOOK_URL")
DB_URL = os.getenv("DB_URL")


def send_discord_message(title, description, color):
    if not description or description.strip() == "":
        description = "No details provided."

    title = str(title) if title else "Notification"

    payload = {
        "embeds": [
            {
                "title": title,
                "description": description,
                "color": int(color)
            }
        ]
    }

    print(f"--- Sending Payload: {payload} ---")
    response = requests.post(DISCORD_URL, json=payload)

    print(f"Discord Response Code: {response.status_code}")
    if response.status_code != 204:
        print(f"Discord Error Body: {response.text}")


if __name__ == "__main__":
    print("Connecting to DB...")
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        print("Connected! Running Query...")

        cur.execute("SELECT job_title, link FROM analytics.fct_job_leads WHERE load_date = CURRENT_DATE LIMIT 5;")
        new_jobs = cur.fetchall()

        cur.close()
        conn.close()

        if new_jobs:
            print(f"Found {len(new_jobs)} jobs.")
            job_list = ""
            for job in new_jobs:
                title = job[0] if job[0] else "Unknown Title"
                link = job[1] if job[1] else "#"
                job_list += f"🔹 **{title}** \n<{link}>\n\n"

            send_discord_message("✅ New Jobs Found", job_list, 3066993)
        else:
            print("No jobs found for today.")
            send_discord_message("😴 Daily Update", "No new jobs found for today's date.", 8421504)

    except Exception as e:
        print(f"Logic Error: {e}")
        send_discord_message("❌ Notifier Error", f"The script crashed with error: {str(e)}", 15158332)