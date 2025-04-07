let selectedQuestionId = null;
let originalText = ""; // 원본 질문 텍스트 저장

document.querySelectorAll('.faq-question').forEach(function(question) {
    question.addEventListener('click', function () {
        selectedQuestionId = question.id;
        originalText = question.innerText;

        document.getElementById('replacement').value = originalText;
    });
});

document.getElementById('submitButton').addEventListener('click', function () {
  const userInput = document.getElementById('replacement').value;

  // 차이 추출
  const diff = getDiffPart(originalText, userInput);
  const replacementValue = diff || originalText;

  // 🌟 수정된 전체 질문 텍스트도 함께 전송
  window.location.href = `/result?question=${encodeURIComponent(selectedQuestionId)}&replacement=${encodeURIComponent(replacementValue)}&modifiedText=${encodeURIComponent(userInput)}`;
});


/**
 * 원본 텍스트와 사용자 입력 텍스트의 차이점(수정된 부분)만 추출
 */
function getDiffPart(original, modified) {
    // 단어 단위로 자름
    const originalWords = original.split(/\s+/);
    const modifiedWords = modified.split(/\s+/);

    // 처음 다른 부분을 찾음
    for (let i = 0; i < Math.min(originalWords.length, modifiedWords.length); i++) {
        if (originalWords[i] !== modifiedWords[i]) {
            return modifiedWords[i];  // 수정된 단어 반환
        }
    }

    // 혹시 마지막에서 추가됐을 경우
    if (modifiedWords.length > originalWords.length) {
        return modifiedWords[modifiedWords.length - 1];
    }

    return null;
}
