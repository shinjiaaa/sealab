document.querySelectorAll('.faq-question').forEach(function(question) {
  question.addEventListener('click', function() {
      const questionId = question.id;
      window.location.href = `/result?question=${encodeURIComponent(questionId)}`;
  });
});