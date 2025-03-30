# web_scraper.py

import requests
from bs4 import BeautifulSoup
import wikipediaapi
import re
import time
import os
from dotenv import load_dotenv

load_dotenv()

USER_AGENT = "CareerPathScraper/1.0"
HEADERS = {"User-Agent": USER_AGENT}
SERP_API_KEY = os.getenv("SERP_API_KEY")

def clean_text(text):
    text = re.sub(r"\[\d+\]", "", text)
    text = re.sub(r"\([^)]*\)", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def remove_sections(text, stop_titles=["References", "External links", "See also"]):
    for title in stop_titles:
        index = text.find(title)
        if index != -1:
            text = text[:index]
    return text.strip()

def is_relevant_to_field(text, field):
    field_keywords = field.lower().split()
    relevance_count = sum(1 for word in field_keywords if word in text.lower())
    return relevance_count >= 1

def get_wikipedia_bio(name, field=None):
    wiki = wikipediaapi.Wikipedia(user_agent=USER_AGENT, language='en')
    page = wiki.page(name)
    if page.exists():
        cleaned = clean_text(remove_sections(page.text))
        if field is None or is_relevant_to_field(cleaned, field):
            print(f"Found Wikipedia page for: {name}")
            return cleaned
        else:
            print(f"Wikipedia page for {name} exists but is not relevant to '{field}'")
            return None
    print(f"No Wikipedia page found for: {name}")
    return None

def scrape_wikipedia_category(category_url):
    print(f"Scraping Wikipedia category: {category_url}")
    base_url = "https://en.wikipedia.org"
    start_url = category_url
    names = []

    while start_url:
        url = base_url + start_url
        print(f"Visiting: {url}")
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        page_div = soup.find("div", id="mw-pages")
        if page_div:
            for group in page_div.find_all("div", class_="mw-category-group"):
                for li in group.find_all("li"):
                    name = li.text.strip()
                    href = li.find("a")["href"]
                    if href.startswith("/wiki/") and not href.startswith("/wiki/Category:"):
                        if not any(bad in name.lower() for bad in ["project", "center", "institute", "group", "lab"]):
                            names.append(name)

        next_page_link = None
        for a in soup.select("a[href^='/w/index.php?title=Category']"):
            if "next page" in a.text.lower():
                next_page_link = a["href"]
                break

        start_url = next_page_link if next_page_link else None

    print(f"\nTotal names collected: {len(names)}")

    field = input("Enter the relevant field to filter bios (e.g., data analytics): ")

    with open("scrape.txt", "w", encoding="utf-8") as f:
        for name in names:
            bio = get_wikipedia_bio(name, field)
            if bio:
                f.write(f"\n\n=== {name} ===\n{bio}")
            time.sleep(1)

def is_likely_human_name(name):
    parts = name.strip().split()
    return 1 < len(parts) <= 4 and all(part[0].isupper() for part in parts)

def extract_names_from_webpage(url):

    import spacy
    nlp = spacy.load("en_core_web_trf")

    print(f"\n🌐 Scraping names from selected link: {url}")
    try:
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get all visible text from page
        text = soup.get_text(" ", strip=True)
        doc = nlp(text)

        # Extract PERSON entities
        names = set(
            ent.text.strip()
            for ent in doc.ents
            if ent.label_ == "PERSON" and is_likely_human_name(ent.text)
        )

        print(f"Found {len(names)} person names using NER.")

        field = input("Enter the relevant field to filter bios (e.g., data analytics): ")

        with open("scrape.txt", "w", encoding="utf-8") as f:
            for name in sorted(names):
                bio = get_wikipedia_bio(name, field)
                if bio:
                    f.write(f"\n\n=== {name} ===\n{bio}")
                time.sleep(1)

    except Exception as e:
        print(f"Error scraping page: {e}")


def search_top_people(field):
    if not SERP_API_KEY:
        print("Please set the SERPAPI_API_KEY environment variable.")
        return

    print(f"\nSearching with SerpAPI for top people in '{field}'...")
    params = {
        "engine": "google",
        "q": f"top influential people in {field}",
        "api_key": SERP_API_KEY
    }
    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()

    links = []
    if "organic_results" in data:
        for i, result in enumerate(data["organic_results"][:5], 1):
            link = result.get("link")
            title = result.get("title")
            if link:
                print(f"{i}. {title}\n   {link}\n")
                links.append(link)

    if not links:
        print("No links found from SerpAPI search.")
        return

    choice = input("Enter the number of the link you want to scrape names from: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(links):
        selected_url = links[int(choice) - 1]
        extract_names_from_webpage(selected_url)
    else:
        print("Invalid choice.")

def main():
    mode = input("Choose mode: 'wikipedia' or 'web': ").strip().lower()
    if mode == "wikipedia":
        user_input = input("Enter a Wikipedia category path (e.g., /wiki/Category:Artificial_intelligence_researchers): ")
        scrape_wikipedia_category(user_input.strip())
    elif mode == "web":
        field = input("Enter a field of interest (e.g., data analytics): ")
        search_top_people(field)
    else:
        print("Invalid mode. Please enter 'wikipedia' or 'web'.")

if __name__ == "__main__":
    main()
