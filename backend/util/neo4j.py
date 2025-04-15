from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

neo4j_password = os.getenv("NEO4J_PASSWORD")

uri = "bolt://localhost:7687"
username = "neo4j"

# Neo4j 드라이버 설정
driver = GraphDatabase.driver(uri, auth=(username, neo4j_password))

# Cypher Query 실행 함수
def run_cypher_query(query):
    try:
        with driver.session() as session:
            result = session.run(query)
            records = [record.data() for record in result]
            return records
    except Exception as e:
        print("쿼리 실행 중 오류 발생:", e)
        return {"error": str(e)}

# 동적 자연어 변환 함수
def convert_to_natural_language(records):
    sentences = []
    for record in records:
        parts = []
        for key, value in record.items():
            if isinstance(value, dict):
                subparts = []
                for sub_key, sub_value in value.items():
                    subparts.append(f"{sub_key}는 '{sub_value}'")
                parts.append(f"이고, ".join(subparts))
            else:
                parts.append(f"{key}는 '{value}'입니다.")
        sentence = "이고, ".join(parts)
        sentences.append(sentence)
    return sentences

# 예시 실행
if __name__ == "__main__":
    cypher_query = "MATCH (n) RETURN n LIMIT 5"  # 예시 쿼리
    result = run_cypher_query(cypher_query)

    if "error" not in result:
        natural_language = convert_to_natural_language(result)
        for sentence in natural_language:
            print(sentence)
