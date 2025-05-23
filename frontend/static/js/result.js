const questionText = {
    "Q1": "Q1. SearchRequest.java 파일을 변경했던 이슈는 무엇인가?",
    "Q2": "Q2. clients.json.jackson 패키지를 변경했던 이슈는 무엇인가?",
    "Q3": "Q3. 858번 이슈가 변경한 소스 코드는 무엇인가?",
    "Q4": "Q4. 858번 이슈가 변경한 소스 코드는 주로 어떤 패키지인가?",
    "Q5": "Q5. 693번 이슈가 변경한 테스트 케이스는 무엇인가?",
    "Q6": "Q6. 371번 이슈가 변경한 테스트 케이스는 어떤 소스 코드를 대상으로 하는가?",
    "Q7": "Q7. 362번 이슈가 변경한 테스트 케이스는 어떤 패키지를 대상으로 하는가?",
    "Q8": "Q8. Aggregate.jaava 코드와 연결된 API 문서는 무엇인가?",
};

// btn
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

// 
async function fetchAnswer(question) {
    try {
        const response = await fetch(`/result?question=${encodeURIComponent(question)}`); // /result에 get 요청
        const htmlContent = await response.text();  // HTML 전체 반환한 걸 문자열로 저장

        // 저장한 문자열을 다시 HTML로 받기
        const parser = new DOMParser();
        const doc = parser.parseFromString(htmlContent, 'text/html');
        
        // answerBox 안에 있는 내용을 문자열로 추출해서 저장
        const answerContent = doc.querySelector('#answerBox').innerHTML;

        // 추출한 문자열을 화면에 표시 (기존 값 덮어 씌움)
        document.getElementById('answerBox').innerHTML = answerContent;

    } catch (error) {
        console.error("답변을 가져오는 중 오류가 발생했습니다.", error);
        document.getElementById('answerBox').innerHTML = "답변을 가져오는 중 오류가 발생했습니다.";
    }
}
