document.addEventListener('DOMContentLoaded', () => {
    const videoForm = document.getElementById('videoForm');
    const apiKeyInput = document.getElementById('apiKey');
    const promptInput = document.getElementById('prompt');
    const generateBtn = document.getElementById('generateBtn');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const videoContainer = document.getElementById('videoContainer');

    // Use the hardcoded API key provided by the user
    const hardcodedApiKey = 'AIzaSyAC0P-NExutRiIQbQPkcbSwZCdz-C8SPEI';
    apiKeyInput.value = hardcodedApiKey;

    videoForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const apiKey = apiKeyInput.value.trim();
        const prompt = promptInput.value.trim();

        if (!apiKey || !prompt) {
            alert('Please ensure both API Key and Prompt are filled out.');
            return;
        }

        // Show loading spinner and disable button
        generateBtn.disabled = true;
        generateBtn.innerHTML = 'Generating...';
        loadingSpinner.style.display = 'block';
        videoContainer.innerHTML = ''; // Clear previous results

        try {
            // NOTE: The Gemini API for video generation is not publicly available as of this implementation.
            // This is a placeholder for the actual API endpoint and request structure.
            // You would need to replace 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent'
            // with the correct video generation model endpoint when it becomes available.
            
            const API_URL = `https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${apiKey}`;

            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    contents: [{
                        parts: [{
                            text: `Generate a video based on the following prompt: ${prompt}`
                        }]
                    }]
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error.message || 'An unknown error occurred.');
            }

            const data = await response.json();

            // Placeholder for handling the video data.
            // The actual response structure for video will be different.
            // You would typically get a video URL or video data to embed.
            const videoUrl = data.candidates[0].content.parts[0].text; // This is a placeholder assumption

            const videoElement = document.createElement('video');
            videoElement.src = videoUrl; // Assuming the API returns a direct link to a video file
            videoElement.controls = true;
            videoElement.autoplay = true;
            videoElement.muted = true; // Muted autoplay is usually allowed by browsers
            videoElement.style.width = '100%';
            videoElement.style.borderRadius = '8px';
            
            videoContainer.appendChild(videoElement);

        } catch (error) {
            console.error('Error:', error);
            videoContainer.innerHTML = `<p class="error">Failed to generate video. Error: ${error.message}. Please check the console for more details.</p>`;
        } finally {
            // Hide loading spinner and re-enable button
            generateBtn.disabled = false;
            generateBtn.innerHTML = 'Generate Video';
            loadingSpinner.style.display = 'none';
        }
    });
});
