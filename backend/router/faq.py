from fastapi import APIRouter, Query, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from util import openai
from util.neo4j import run_cypher_query

router = APIRouter()

templates = Jinja2Templates(directory="../frontend/templates")

# FAQ와 해당하는 Cypher Query 매핑
faq = {
    "Q1": "Q1. 해당 코드를 변경했던 이슈는 무엇인가?",
    "Q2": "Q2. 해당 패키지를 변경했던 이슈는 무엇인가?",
    "Q3": "Q3. 해당 이슈가 변경한 소스 코드는 무엇인가?",
    "Q4": "Q4. 해당 이슈가 변경한 소스 코드는 주로 어떤 패키지인가?",
    "Q5": "Q5. 해당 이슈가 변경한 테스트 케이스는 무엇인가?",
    "Q6": "Q6. 해당 이슈가 변경한 테스트 케이스는 어떤 소스 코드를 대상으로 하는가?",
    "Q7": "Q7. 해당 이슈가 변경한 테스트 케이스는 어떤 패키지를 대상으로 하는가?",
    "Q8": "Q8. 해당 소스 코드와 연결된 API 문서는 무엇인가?",
}

faq_cypher_queries = {
    "Q1": """
        OPTIONAL MATCH (s:SOURCE_CODE {file_name:'filenameinput'})
        OPTIONAL MATCH (t:TEST_CODE {file_name:'filenameinput'})
        WITH COALESCE(s, t) AS foundNode
        MATCH (issueNode:ISSUE)-[MODIFY]-(foundNode)
        RETURN issueNode
    """,
    "Q2": """
        OPTIONAL MATCH (s:SOURCE_CODE {package: "packageinput"})
        OPTIONAL MATCH (t:TEST_CODE {package: "packageinput"})
        WITH COALESCE(s, t) AS foundNode
        MATCH (issueNode)-[:MODIFY]-(foundNode)
        WITH issueNode, COUNT(foundNode) AS occurrenceCount
        ORDER BY occurrenceCount DESC
        RETURN issueNode, occurrenceCount
    """,
    "Q3": """
        MATCH (i:ISSUE {issue_number:'issueNum'})-[:MODIFY]->(sourceNode:SOURCE_CODE)
        RETURN sourceNode
    """,
    "Q4": """
        MATCH (i:ISSUE {issue_number:'issueNum'})-[:MODIFY]->(connectedNode)
        RETURN connectedNode.package AS package, COUNT(connectedNode.package) AS packageCount
        ORDER BY packageCount DESC
    """,
    "Q5": """
        MATCH (i:ISSUE {issue_number:'issueNum'})-[:MODIFY]->(testNode:TEST_CASE)
        return (testNode)
    """,
    "Q6": """
        MATCH (i:ISSUE {issue_number:'issueNum'})-[:MODIFY]->(testNode: TEST_CASE)
        MATCH (sourceNode:SOURCE_CODE)-[:TEST]-(testNode)
        RETURN sourceNode
    """,
    "Q7": """
        MATCH (i:ISSUE {issue_number:'issueNum'})-[:MODIFY]->(connectedNode: TEST_CASE)
        MATCH (sourceNode:SOURCE_CODE)-[:TEST]-(testNode)
        WITH sourceNode.package As package, COUNT(*) AS occurrenceCount
        ORDER BY occurrenceCount DESC
        RETURN package, occurrenceCount
    """,
    "Q8": """
        MATCH (s:SOURCE_CODE {file_name:'filenameinput'})
        MATCH (s)-[:TEST]-(t)
        MATCH (t)-[:EXPLAINED]-(apiNode)
        RETURN apiNode
    """,
}

# Faq Page
@router.get("/", response_class=HTMLResponse)
async def get_faq_page(request: Request):
    return templates.TemplateResponse("faq.html", {"request": request, "faq": faq})

# Result Page
@router.get("/result", response_class=HTMLResponse)
async def get_answer(
    question: str = Query(...),
    replacement: str = Query(...),
    modifiedText: str = Query(...),
    request: Request = None
):
    try:
        question_id = question.split('.')[0].strip()
        cypher_query = faq_cypher_queries.get(question_id)

        if not cypher_query:
            raise HTTPException(status_code=404, detail=f"Query not found for {question_id}.")

        if "filenameinput" in cypher_query:
            placeholder = "filenameinput"
        elif "packageinput" in cypher_query:
            placeholder = "packageinput"
        elif "issueNum" in cypher_query:
            placeholder = "issueNum"
        else:
            raise HTTPException(status_code=400, detail="No placeholder matched.")

        # GPT한테 변환된 전체 Cypher 쿼리 받기
        modified_query = openai.get_answer_from_openai(cypher_query, placeholder, replacement)

        # Neo4j에 실행 요청 보내기
        neo4j_result = run_cypher_query(modified_query)

        return templates.TemplateResponse("result.html", {
            "request": request,
            "question": modifiedText, # 최종 질문 (user가 변경한)
            "answer": modified_query, # 최종 답변
            "query_result": neo4j_result,
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating answer: {e}")