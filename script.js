document.getElementById('generate-btn').addEventListener('click', async () => {
    const prompt = document.getElementById('prompt-input').value;
    const apiKey = document.getElementById('api-key-input').value; // Still needed to pass to the backend
    const resultDiv = document.getElementById('result-container');
    const loadingSpinner = document.getElementById('loading-spinner');

    if (!prompt || !apiKey) {
        resultDiv.innerHTML = `<p class="text-red-400">Please enter a prompt and your API key.</p>`;
        return;
    }

    // Show loading spinner and clear previous result
    loadingSpinner.classList.remove('hidden');
    resultDiv.innerHTML = '';

    try {
        const response = await fetch('http://localhost:3000/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt: prompt, apiKey: apiKey }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Something went wrong on the server.');
        }

        const data = await response.json();
        
        // The Gemini API returns markdown. We'll display it raw or you can use a library to render it.
        // For simplicity, we'll format it a bit.
        const formattedText = data.text.replace(/\n/g, '<br>');
        resultDiv.innerHTML = `<p>${formattedText}</p>`;

    } catch (error) {
        resultDiv.innerHTML = `<p class="text-red-400">Error: ${error.message}</p>`;
    } finally {
        // Hide loading spinner
        loadingSpinner.classList.add('hidden');
    }
});
