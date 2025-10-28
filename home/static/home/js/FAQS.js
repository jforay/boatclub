// Get all the FAQ question elements
const faqQuestions = document.querySelectorAll('.faq-question');

// Add a click event listener to each question
faqQuestions.forEach(question => {
    question.addEventListener('click', () => {
        // Toggle the visibility of the corresponding answer
        const answer = question.nextElementSibling;
        if (answer.style.display === 'block') {
            answer.style.display = 'none';
        } else {
            answer.style.display = 'block';
        }
    });
});
