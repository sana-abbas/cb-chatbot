const API_URL = 'https://chatbot-api-205295349076.us-central1.run.app/chat';
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const loading = document.getElementById('loading');
const languageDisplay = document.getElementById('detected-language');

function createMessageElement(text, isUser) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    messageDiv.textContent = text;
    return messageDiv;
}

function formatBotResponse(response) {
    return `Roman Urdu: ${response['roman-urdu']}\n\nTranslation: ${response.translation}`;
}

async function handleUserMessage() {
    const prompt = userInput.value.trim();
    if (!prompt) return;

    // Add user message
    chatMessages.appendChild(createMessageElement(prompt, true));
    userInput.value = '';
    loading.style.display = 'block';

    try {
        const response = await fetch(API_URL, {
            // method: 'POST',
            // headers: {
            //     'Content-Type': 'application/json',
            // },
            // body: JSON.stringify({ prompt }),
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Origin': window.location.origin,
            },
            mode: 'cors', // Explicitly set CORS mode
            credentials: 'same-origin', // Changed from 'include' to 'same-origin'
            body: JSON.stringify({ prompt }),
        });

        if (!response.ok) throw new Error('API request failed');
        
        const data = await response.json();
        languageDisplay.textContent = `Detected language: ${data.response.speaker_language}`;
        
        // Add bot response
        const formattedResponse = formatBotResponse(data.response);
        chatMessages.appendChild(createMessageElement(formattedResponse, false));
        
    } catch (error) {
        console.error('Error:', error);
        chatMessages.appendChild(createMessageElement('Sorry, there was an error processing your request.', false));
    } finally {
        loading.style.display = 'none';
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

sendButton.addEventListener('click', handleUserMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleUserMessage();
});