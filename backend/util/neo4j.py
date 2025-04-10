from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

neo4j_password = os.getenv("NEO4J_PASSWORD")

uri = "bolt://localhost:7687"
username = "neo4j"

# Neo4j 드라이버 설정
driver = GraphDatabase.driver(uri, auth=(username, neo4j_password))

# Cypher Query 실행
def run_cypher_query(query):
    try:
        with driver.session() as session:
            result = session.run(query)
            return [record.data() for record in result] # 쿼리 실행
    except Exception as e:
        print("쿼리 실행 중 오류 발생:", e)
        return {"error": str(e)}
