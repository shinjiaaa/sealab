import openai
import os
from dotenv import load_dotenv
import re

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API key is missing")
openai.api_key = api_key

# Cypher Query 수정 요청
def get_answer_from_openai(original_query, placeholder, replacement):
    prompt = f"Replace '{placeholder}' in the following Cypher query with '{replacement}', and ONLY return the updated Cypher query:\n\n{original_query}"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    content = response['choices'][0]['message']['content']

    # Cypher Query 블럭 존재하면 -> 블럭 내 Cypher Query 추출
    cypher_match = re.search(r"```(?:cypher)?\n(.*?)```", content, re.DOTALL)
    if cypher_match:
        return cypher_match.group(1).strip()

    # 아니면 그냥 RETURN 문 있는 줄부터 추출
    lines = content.split('\n') # content(GPT한테 받은 텍스트)를 줄 단위로 쪼갬
    for i, line in enumerate(lines): # 몇 번째 줄인지(i), 내용(line) 가져오기 - 줄마다 반복
        if line.strip().lower().startswith("match") or line.strip().lower().startswith("optional match"): # 그 줄이 "" 안에 있는 내용일 경우 (Cypher Query)
            return '\n'.join(lines[i:]).strip() #해당 줄부터 끝까지 이어 붙여서 반환 (이걸 Cypher Query 전체라고 판단하는 것)

    return content.strip() # "" 텍스트 못 찾았을 경우 전체 텍스트 반환
