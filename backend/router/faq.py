from fastapi import APIRouter, Query, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from util import openai

router = APIRouter()

templates = Jinja2Templates(directory="../frontend/templates")

# FAQ와 해당하는 Cypher Query 매핑
faq = {
    "Q1": "Q1. SearchRequest.java 파일을 변경했던 이슈는 무엇인가?",
    "Q2": "Q2. clients.json.jackson 패키지를 변경했던 이슈는 무엇인가?",
    "Q3": "Q3. 858번 이슈가 변경한 소스 코드는 무엇인가?",
    "Q4": "Q4. 858번 이슈가 변경한 소스 코드는 주로 어떤 패키지인가?",
    "Q5": "Q5. 693번 이슈가 변경한 테스트 케이스는 무엇인가?",
    "Q6": "Q6. 371번 이슈가 변경한 테스트 케이스는 어떤 소스 코드를 대상으로 하는가?",
    "Q7": "Q7. 362번 이슈가 변경한 테스트 케이스는 어떤 패키지를 대상으로 하는가?",
    "Q8": "Q8. Aggregate.java 코드와 연결된 API 문서는 무엇인가?",
}

faq_cypher_queries = {
    "Q1": """
        OPTIONAL MATCH (s:SOURCE_CODE {file_name:'filenameinput'})
        OPTIONAL MATCH (s:TEST_CODE {file_name:'filenameinput'})
        WITH COALESCE(s, t) AS foundNode
        MATCH (issueNode:ISSUE)-[MODIFY]-(foundNode)
        RETURN issueNode
    """,
    "Q2": """
        OPTIONAL MATCH (s:SOURCE_CODE {package: "packageinput"})
        OPTIONAL MATCH (s:TEST_CODE {package: "packageinput"})
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
        MATCH (i:ISSUE {issue_number:'issueNum'})-[:MODIFY]->(testNode:TEST_CODE)
        return (testNode)
    """,
    "Q6": """
        MATCH (i:ISSUE {issue_number:'issueNum'})-[:MODIFY]->(testNode: TEST_CODE)
        MATCH (sourceNode:SOURCE_CODE)-[:TESTED]-(testNode)
        RETURN sourceNode
    """,
    "Q7": """
        MATCH (i:ISSUE {issue_number:'issueNum'})-[:MODIFY]->(connectedNode: TEST_CODE)
        MATCH (sourceNode:SOURCE_CODE)-[:TESTED]-(testNode)
        RETURN package, occurrenceCount
    """,
    "Q8": """
        MATCH (s:SOURCE_CODE {file_name:"filenameinput"})
        MATCH (s)-[:TESTED]-(t)
        MATCH (s)-[:TESTED]-(apiNode)
        RETURN apiNode
    """,
}

@router.get("/", response_class=HTMLResponse)
async def get_faq_page(request: Request):
    return templates.TemplateResponse("faq.html", {"request": request, "faq": faq})

@router.get("/result", response_class=HTMLResponse)
async def get_answer(
    question: str = Query(...),
    replacement: str = Query(...),
    modifiedText: str = Query(...),  # 새로 추가된 수정된 전체 질문
    request: Request = None
):
    try:
        question_id = question.split('.')[0].strip()
        cypher_query = faq_cypher_queries.get(question_id)

        if not cypher_query:
            raise HTTPException(status_code=404, detail=f"Query not found for {question_id}.")

        # placeholder 결정
        if "filenameinput" in cypher_query:
            placeholder = "filenameinput"
        elif "packageinput" in cypher_query:
            placeholder = "packageinput"
        elif "issueNum" in cypher_query:
            placeholder = "issueNum"
        else:
            raise HTTPException(status_code=400, detail="No placeholder matched.")

        modified_query = openai.get_answer_from_openai(cypher_query, placeholder, replacement)

        return templates.TemplateResponse("result.html", {
            "request": request,
            "question": modifiedText,  # 💡 전체 질문을 여기서 표시
            "answer": modified_query,
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating answer: {e}")
