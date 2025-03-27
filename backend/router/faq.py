from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from util import openai

router = APIRouter()

templates = Jinja2Templates(directory="../frontend/templates")

faq = {
        "Q1": "Q1. 해당 코드를 변경했던 이유는 무엇인가?",
        "Q2": "Q2. 해당 패키지를 변경했던 이슈는 무엇인가?",
        "Q3": "Q3. 해당 이슈가 변경한 소스 코드는 무엇인가?",
        "Q4": "Q4. 해당 이슈가 변경한 소스 코드는 주로 어떤 패키지인가?",
        "Q5": "Q5. 해당 이슈가 변경한 테스트 케이스는 무엇인가?",
        "Q6": "Q6. 해당 이슈가 변경한 테스트 케이스는 어떤 소스 코드를 대상으로 하는가?",
        "Q7": "Q7. 해당 이슈가 변경한 테스트 케이스는 어떤 패키지를 대상으로 하는가?",
        "Q8": "Q8. 해당 소스 코드와 연결된 API 문서는 무엇인가?",
    }

@router.get("/", response_class=HTMLResponse)
async def get_faq_page(request: Request):
    return templates.TemplateResponse("faq.html", {"request": request, "faq": faq})

@router.get("/result")
async def get_answer(question: str, request: Request):
    try:
        question_text = faq.get(question.strip())
        if not question_text:
            raise HTTPException(status_code=404, detail="Question not found")

        answer = openai.get_answer_from_openai(question_text)

        return templates.TemplateResponse("result.html", {
            "request": request, 
            "question": question_text, 
            "answer": answer,
            })

    except Exception as e:
        print(f"General error: {e}")
        raise HTTPException(status_code=500, detail="Error generating answer")