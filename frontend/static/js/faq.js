let selectedQuestionId = null;
let originalText = ""; // 원본 질문 텍스트 저장

// input에 질문 text 삽입
document.querySelectorAll('.faq-question').forEach(function(question) {
    question.addEventListener('click', function () {
        selectedQuestionId = question.id;
        originalText = question.innerText;

        document.getElementById('replacement').value = originalText; 
    });
});

// 전송 누르면 페이지 이동
document.getElementById('submitButton').addEventListener('click', function () {
  const userInput = document.getElementById('replacement').value;

  // 차이 추출
  const diff = getDiffPart(originalText, userInput);
  const replacementValue = diff || originalText;

  // 수정된 전체 질문 텍스트도 함께 전송
  window.location.href = `/result?question=${encodeURIComponent(selectedQuestionId)}&replacement=${encodeURIComponent(replacementValue)}&modifiedText=${encodeURIComponent(userInput)}`;
});

// 원본 텍스트와 사용자 입력 텍스트의 차이점(수정된 부분)만 추출
function getDiffPart(original, modified) {
    // 단어 단위로 자름
    const originalWords = original.split(/\s+/); // 기존 질문
    const modifiedWords = modified.split(/\s+/); // user가 수정한 텍스트

    // 앞에서부터 비교 -> 다른 단어(즉, 수정된 단어) 찾기
    for (let i = 0; i < Math.min(originalWords.length, modifiedWords.length); i++) {
        if (originalWords[i] !== modifiedWords[i]) {
            return modifiedWords[i];  // 수정된 단어 반환
        }
    }

    // 마지막에 추가된 단어 (for문에서 놓칠 수도 있기 때문에 추가해 줌)
    if (modifiedWords.length > originalWords.length) {
        return modifiedWords[modifiedWords.length - 1]; // 마지막에 추가된 단어 반환
    }

    return null;
}
