const questionText = {
        "Q1": "Q1. 해당 코드를 변경했던 이유는 무엇인가?",
        "Q2": "Q2. 해당 패키지를 변경했던 이슈는 무엇인가?",
        "Q3": "Q3. 해당 이슈가 변경한 소스 코드는 무엇인가?",
        "Q4": "Q4. 해당 이슈가 변경한 소스 코드는 주로 어떤 패키지인가?",
        "Q5": "Q5. 해당 이슈가 변경한 테스트 케이스는 무엇인가?",
        "Q6": "Q6. 해당 이슈가 변경한 테스트 케이스는 어떤 소스 코드를 대상으로 하는가?",
        "Q7": "Q7. 해당 이슈가 변경한 테스트 케이스는 어떤 패키지를 대상으로 하는가?",
        "Q8": "Q8. 해당 소스 코드와 연결된 API 문서는 무엇인가?",
};

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('nextBtn').addEventListener('click', showNextAnswer);
    document.getElementById('beforeBtn').addEventListener('click', showPreviousAnswer);
    
    let currentQuestionIndex = 0;
    const questionKeys = Object.keys(questionText);

    // next btn
    async function showNextAnswer() {
        currentQuestionIndex = (currentQuestionIndex + 1) % questionKeys.length;
        const nextQuestionId = questionKeys[currentQuestionIndex];

        document.getElementById('textBox').value = questionText[nextQuestionId];

        await fetchAnswer(questionText[nextQuestionId]);
    }

    // before btn
    async function showPreviousAnswer() {
        currentQuestionIndex = (currentQuestionIndex - 1 + questionKeys.length) % questionKeys.length;
        const prevQuestionId = questionKeys[currentQuestionIndex];

        document.getElementById('textBox').value = questionText[prevQuestionId];

        await fetchAnswer(questionText[prevQuestionId]);
    }
});


async function fetchAnswer(question) {
    try {
        const response = await fetch(`/result?question=${encodeURIComponent(question)}`);
        
        const htmlContent = await response.text();  // HTML 형태로 응답 받음

        // 받은 HTML에서 답변만 추출
        const parser = new DOMParser();
        const doc = parser.parseFromString(htmlContent, 'text/html');
        
        // 'answerBox' 내부만 갱신
        const answerContent = doc.querySelector('#answerBox').innerHTML;

        // 기존 내용을 덮어쓰지 않고 'answerBox'에 새 답변을 삽입
        document.getElementById('answerBox').innerHTML = answerContent;

    } catch (error) {
        console.error("답변을 가져오는 중 오류가 발생했습니다.", error);
        document.getElementById('answerBox').innerHTML = "답변을 가져오는 중 오류가 발생했습니다.";
    }
}
