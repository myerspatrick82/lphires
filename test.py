import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key = os.environ.get("PERPLEXITY_API_KEY"),
    base_url="https://api.perplexity.ai"
)

# response = client.responses.create(
#     model = "gpt-4o",
#     instructions="You are a career career path recommender that takes in a career and builds a path from the top down from people in the field",
#     input="I want to be a software engineer",
# )

messages = [
    {
        "role": "system",
        "content": (
            "You are an artificial intelligence assistant and you need to "
            "engage in a helpful, detailed, polite conversation with a user."
        )
    },
    {
        "role": "user",
        "content": (
            "How many stars are in the universe?"
        ),
    },
]

response = client.chat.completions.create(
    model="sonar",
    messages=messages
)

print(response)