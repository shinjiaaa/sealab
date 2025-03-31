import openai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API key is missing")
openai.api_key = api_key

def get_answer_from_openai(cypher_query: str, placeholder: str, replacement: str) -> str:
    try:
        prompt = f"Replace '{placeholder}' in the following Cypher query with the actual value (e.g., '{replacement}'):\n\n{cypher_query}"

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[ 
                {"role": "user", "content": prompt},
            ],
        )
        answer = response['choices'][0]['message']['content'].strip()
        return answer

    except Exception as e:
        print(f"Error while fetching answer from OpenAI: {e}")
        raise
