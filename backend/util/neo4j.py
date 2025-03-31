from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# .env에서 비밀번호를 가져옵니다.
neo4j_password = os.getenv("NEO4J_PASSWORD")

# Neo4j 클라이언트 설정
uri = "bolt://localhost:7687"  # Neo4j 서버 URI
username = "neo4j"  # Neo4j 사용자명

# Neo4j 드라이버 설정
driver = GraphDatabase.driver(uri, auth=(username, neo4j_password))

def run_cypher_query(query: str):
    """Cypher 쿼리를 실행하고 결과를 반환하는 함수"""
    try:
        with driver.session() as session:
            result = session.run(query)
            return [record.data() for record in result]
    except Exception as e:
        print(f"Error while running Cypher query: {e}")
        return None
