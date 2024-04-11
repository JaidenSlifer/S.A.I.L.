// This function is called when the form is submitted
function handleAnalyzeClick(event) {
    event.preventDefault();  // Prevent the default form submission
    
    const ticker = document.getElementById('tickerInput').value;
    const resultsDiv = document.getElementById('results');

    // Use the Fetch API to send a POST request to the server
    fetch('/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ ticker: ticker })
    })
    .then(response => response.json())  // Parse the JSON response
    .then(data => {
        // Dynamically update the 'results' div with the response data
        resultsDiv.innerHTML = `
            <p>Sentiment Analysis: ${data.sentiment}</p>
            <p>Recommendation: ${data.recommendation}</p>
            <img src="${data.chart}" alt="Stock Chart">
        `;
    })
    .catch(error => {
        resultsDiv.innerHTML = `<p>Error: ${error}</p>`;
    });
}

// Add event listener to the form
document.getElementById('tickerForm').addEventListener('submit', handleAnalyzeClick);
