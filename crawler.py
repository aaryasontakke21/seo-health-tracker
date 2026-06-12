import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import pandas as pd
import time

# The website we want to crawl
START_URL = "https://wagepath.com/"
MAX_PAGES = 1000

def get_domain(url):
    return urlparse(url).netloc

def crawl_site(start_url, max_pages):
    domain = get_domain(start_url)
    visited = set()
    to_visit = [start_url]
    results = []

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)

        if url in visited:
            continue

        try:
            response = requests.get(url, timeout=10)
            status_code = response.status_code
        except requests.RequestException:
            status_code = "Error"
            response = None

        visited.add(url)

        title = ""
        meta_description = ""
        h1 = ""
        indexability = "Indexable"

        if response is not None and status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Get title tag
            if soup.title and soup.title.string:
                title = soup.title.string.strip()

            # Get meta description
            meta_tag = soup.find("meta", attrs={"name": "description"})
            if meta_tag and meta_tag.get("content"):
                meta_description = meta_tag.get("content").strip()

            # Get first H1
            h1_tag = soup.find("h1")
            if h1_tag:
                h1 = h1_tag.get_text().strip()

            # Check meta robots for noindex
            robots_tag = soup.find("meta", attrs={"name": "robots"})
            if robots_tag and "noindex" in robots_tag.get("content", "").lower():
                indexability = "Non-Indexable"

            # Find all links on this page
            for link in soup.find_all("a", href=True):
                full_url = urljoin(url, link["href"])
                if get_domain(full_url) == domain and full_url not in visited and full_url not in to_visit:
                    to_visit.append(full_url)
        else:
            indexability = "Non-Indexable"

        results.append({
            "Address": url,
            "Title 1": title,
            "Meta Description 1": meta_description,
            "H1-1": h1,
            "Status Code": status_code,
            "Indexability": indexability
        })

        print(f"Crawled {len(visited)} pages: {url}")
        time.sleep(0.2)  # Be polite to the server

    return pd.DataFrame(results)

if __name__ == "__main__":
    print(f"Starting crawl of {START_URL}...")
    df = crawl_site(START_URL, MAX_PAGES)
    df.to_csv("crawl_export.csv", index=False)
    print(f"✅ Done! Crawled {len(df)} pages and saved to crawl_export.csv")