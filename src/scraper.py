import requests
from bs4 import BeautifulSoup
import wikipediaapi

base_url = "https://en.wikipedia.org"
start_url = "/wiki/Category:Artificial_intelligence_researchers"
names = []

while start_url:
    url = base_url + start_url
    print(f"Scraping: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Look in the correct container
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
    for a in soup.select("a[href^='/w/index.php?title=Category:Artificial_intelligence_researchers&pagefrom=']"):
        if "next page" in a.text.lower():
            next_page_link = a["href"]
            break

    if next_page_link:
        start_url = next_page_link
    else:
        start_url = None

print(f"\nTotal names collected: {len(names)}\n")

wiki = wikipediaapi.Wikipedia(user_agent="AIResearchScraper/1.0", language='en')

# Open output file
with open("output.txt", "w", encoding='utf-8') as file:
    for name in names:
        try:
            page = wiki.page(name)
            if page.exists():
                file.write(f"\n\n=== {name} ===\n")
                file.write(page.text)  
            else:
                print(f"Page not found: {name}")
        except Exception as e:
            print(f"Error on {name}: {e}")

file.close()