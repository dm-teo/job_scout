import requests
from bs4 import BeautifulSoup

def get_full_desc(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9,de;q=0.8',
        'Referer': 'https://www.google.com/',
    }

    try:
        # 2. THE REQUEST: Visit the page
        response = requests.get(url, headers=headers, timeout=10)

        # 2. THE REQUEST: Visit the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # 4. THE CLEANUP: Remove scripts and styles that aren't human text
        for garbage in soup(['script', 'style', 'nav', 'footer']):
            garbage.decompose()

        # 5. THE OUTPUT: Get the clean text
        # separator=' ' ensures words don't get stuck together
        clean_text = soup.get_text(separator=' ', strip=True)

        return clean_text

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None


