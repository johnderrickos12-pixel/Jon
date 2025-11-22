const express = require('express');
const cors = require('cors');
const { GoogleGenerativeAI } = require('@google/generative-ai');

const app = express();
const port = process.env.PORT || 3000;

// Middleware to allow cross-origin requests and parse JSON
app.use(cors());
app.use(express.json());

// POST endpoint to handle video generation requests
app.post('/generate', async (req, res) => {
    const { prompt, apiKey } = req.body;

    if (!prompt || !apiKey) {
        return res.status(400).json({ error: 'Missing prompt or API key.' });
    }

    try {
        // Initialize the Google Gemini AI client
        const genAI = new GoogleGenerativeAI(apiKey);
        const model = genAI.getGenerativeModel({ model: "gemini-pro" });

        // Generate the content based on the prompt
        const result = await model.generateContent(prompt);
        const response = await result.response;
        const text = response.text();

        // Send the generated text back to the frontend
        res.json({ generatedContent: text });

    } catch (error) {
        console.error('Error calling Google Gemini API:', error);
        res.status(500).json({ error: 'An error occurred while communicating with the Gemini API.' });
    }
});

app.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
});
