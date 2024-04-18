document.getElementById('tickerForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const ticker = document.getElementById('tickerInput').value;
    fetch('/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ ticker: ticker })
    })
    .then(response => response.json())
    .then(data => {
        window.location.href = data.redirect_url; // Redirects to the display page with parameters
    })
    .catch(error => console.error('Error:', error));
});
