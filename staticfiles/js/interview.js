async function fetchResponses(userId) {
    const response = await fetch(`http://127.0.0.1:8000/api/user_responses/${userId}/`);
    const data = await response.json();

    let resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "<h2>Your Interview History</h2>";  // Keep the heading

    data.forEach(response => {
        let entry = document.createElement("div");
        entry.innerHTML = `
            <h3>Question: ${response.question}</h3>
            <p><strong>Answer:</strong> ${response.answer}</p>
            <p><strong>Score:</strong> ${response.score} / 10</p>
            <p><strong>Feedback:</strong> ${response.feedback}</p>
            ${response.score < 7 ? `<button onclick="retryAnswer(${response.id}, '${response.question}')">Retry</button>` : ''}
            <hr>
        `;
        resultsDiv.appendChild(entry);
    });
}

// Function to allow retrying an answer
function retryAnswer(responseId, question) {
    let newAnswer = prompt(`Retry your answer for: ${question}`);

    if (newAnswer) {
        fetch(`http://127.0.0.1:8000/api/retry_answer/${responseId}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ answer: newAnswer })
        })
        .then(res => res.json())
        .then(data => {
            alert(`New Score: ${data.score}\nFeedback: ${data.feedback}`);
            fetchResponses(1);  // Reload responses
        });
    }
}

// Call this function when the page loads (Replace `1` with actual user ID)
document.addEventListener("DOMContentLoaded", () => {
    fetchResponses(1);
});
