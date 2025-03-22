// Fetch and display interview responses
async function fetchResponses(userId) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/api/user_responses/${userId}/`);
        const data = await response.json();

        let resultsDiv = document.getElementById("results");
        resultsDiv.innerHTML = "<h2>Your Interview History</h2>"; // Preserve the heading

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
    } catch (error) {
        console.error("Error fetching responses:", error);
    }
}

// Function to allow retrying an answer
async function retryAnswer(responseId, question) {
    let newAnswer = prompt(`Retry your answer for: ${question}`);

    if (newAnswer) {
        try {
            const response = await fetch(`http://127.0.0.1:8000/api/retry_answer/${responseId}/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ answer: newAnswer })
            });
            const data = await response.json();

            alert(`New Score: ${data.score}\nFeedback: ${data.feedback}`);
            fetchResponses(1); // Reload responses
        } catch (error) {
            console.error("Error submitting retry answer:", error);
        }
    }
}

// Fetch and display user progress chart
async function fetchProgressData(userId) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/api/user_progress/${userId}/`);
        const data = await response.json();

        const labels = data.map(entry => entry.timestamp); // X-axis (timestamps)
        const scores = data.map(entry => entry.score); // Y-axis (scores)

        const ctx = document.getElementById("progressChart").getContext("2d");

        new Chart(ctx, {
            type: "line",
            data: {
                labels: labels,
                datasets: [{
                    label: "Answer Scores Over Time",
                    data: scores,
                    borderColor: "blue",
                    backgroundColor: "rgba(0, 0, 255, 0.2)",
                    fill: true,
                    borderWidth: 2,
                    tension: 0.2
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: { title: { display: true, text: "Attempts" } },
                    y: { title: { display: true, text: "Score" }, min: 0, max: 10 }
                }
            }
        });
    } catch (error) {
        console.error("Error fetching progress data:", error);
    }
}

// Run these functions when the page loads
document.addEventListener("DOMContentLoaded", () => {
    const userId = 1; // Replace with dynamic user ID if needed
    fetchResponses(userId);
    fetchProgressData(userId);
});
