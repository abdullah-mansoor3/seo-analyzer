import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import json

def is_valid_url(url, base_domain):
    parsed = urlparse(url)
    return parsed.scheme in ["http", "https"] and parsed.netloc.endswith(base_domain)

def extract_info_from_page(soup, url):
    return {
        "url": url,
        "title": soup.title.string if soup.title else "",
        "meta_description": soup.find("meta", attrs={"name": "description"})["content"] if soup.find("meta", attrs={"name": "description"}) else "",
        "h1": [h.get_text(strip=True) for h in soup.find_all("h1")],
        "h2": [h.get_text(strip=True) for h in soup.find_all("h2")],
        "canonical": soup.find("link", rel="canonical")["href"] if soup.find("link", rel="canonical") else "",
        "alt_texts": [img.get("alt") for img in soup.find_all("img") if img.get("alt")],
        "internal_links": [],
        "external_links": [],
        "text_content": soup.get_text(separator=" ", strip=True)[:5000],  # limit text
        "structured_data": [json.loads(tag.string) for tag in soup.find_all("script", type="application/ld+json") if tag.string],
    }

def crawl_site(start_url, max_pages=50):
    base_domain = urlparse(start_url).netloc
    visited = set()
    queue = [start_url]
    data = []

    while queue and len(visited) < max_pages:
        url = queue.pop(0)
        if url in visited:
            continue

        try:
            print(f"Crawling: {url}")
            response = requests.get(url, timeout=10)
            if response.status_code != 200 or 'text/html' not in response.headers.get('Content-Type', ''):
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            info = extract_info_from_page(soup, url)

            links = set()
            for a_tag in soup.find_all("a", href=True):
                href = a_tag['href']
                full_url = urljoin(url, href)
                if is_valid_url(full_url, base_domain):
                    links.add(full_url)
                    info["internal_links"].append(full_url)
                else:
                    info["external_links"].append(full_url)

            queue.extend(links - visited)
            visited.add(url)
            data.append(info)

        except Exception as e:
            print(f"Error crawling {url}: {e}")

    return data

def save_results(data, domain):
    os.makedirs(f"./data/sites/{domain}", exist_ok=True)
    with open(f"./data/sites/{domain}/crawl.json", "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    url = input("Enter a URL to crawl: ").strip()
    results = crawl_site(url)
    domain = urlparse(url).netloc
    save_results(results, domain)
