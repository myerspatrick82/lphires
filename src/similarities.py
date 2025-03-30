import os
from dotenv import load_dotenv
import requests

load_dotenv()

API_KEY = os.environ.get("PERPLEXITY_API_KEY")  
API_URL = "https://api.perplexity.ai/chat/completions"

def main():
    with open("summarizations.txt", "r", encoding="utf-8") as f:
        summaries = f.read()

    instruction = """
    Given a list of notable individuals in a specific field, analyze and synthesize the shared career roadmaps they followed. I want you to extract the common educational paths, job titles, institutions, and key transitions they made—especially the sequence of steps that led them to become leaders or frontier figures in their domain.

    Specifically:
    - Identify which schools, degrees, or academic backgrounds most commonly appear.
    - Note any early career roles, postdocs, or visiting fellowships that were pivotal.
    - Highlight common employers (e.g., research labs, companies, startups) they moved through.
    - Focus on job functions and strategic positioning (e.g., founding journals, joining policy bodies).
    - Build a chronological roadmap showing typical stages (from undergrad to frontier leadership).
    - Do NOT summarize each person individually. Instead, generalize and group patterns.
    - Use bullet points, stage headers (like “Stage 1: Undergraduate Foundations”), and include specific institutions or titles when possible.
    - Prioritize signal over fluff. Avoid generic advice.

    Here is the list of individuals to analyze:
    """

    full_prompt = instruction + "\n" + summaries

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "sonar",
        "messages": [{"role": "user", "content": full_prompt}],
        "temperature": 0.3
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        reply = result["choices"][0]["message"]["content"]
        print("📋 Perplexity Career Path Output:\n")
        print(reply)

        with open("career_path_analysis.txt", "w", encoding="utf-8") as f:
            f.write(reply)
    else:
        print(f"Request failed: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    main()