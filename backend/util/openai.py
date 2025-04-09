import openai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API key is missing")
openai.api_key = api_key

import re

def get_answer_from_openai(original_query, placeholder, replacement):
    prompt = f"Replace '{placeholder}' in the following Cypher query with '{replacement}', and ONLY return the updated Cypher query:\n\n{original_query}"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response['choices'][0]['message']['content']

    # Cypher 쿼리만 추출 (```cypher ... ``` 블럭 또는 첫 번째 MATCH~RETURN 등)
    cypher_match = re.search(r"```(?:cypher)?\n(.*?)```", content, re.DOTALL)
    if cypher_match:
        return cypher_match.group(1).strip()

    # 아니면 그냥 RETURN 문 있는 줄부터 추출
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.strip().lower().startswith("match") or line.strip().lower().startswith("optional match"):
            return '\n'.join(lines[i:]).strip()

    return content.strip()
