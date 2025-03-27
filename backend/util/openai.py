import openai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API key is missing")
openai.api_key = api_key

def get_answer_from_openai(question_text: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": question_text},
            ],
        )
        answer = response['choices'][0]['message']['content'].strip()
        return answer

    except Exception as e:
        print(f"Error while fetching answer from OpenAI: {e}")
        raise
