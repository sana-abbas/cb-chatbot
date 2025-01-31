# Multilingual Chatbot API

A cloud-native API for handling multilingual chatbot requests using OpenAI's GPT-3.5-turbo model, deployed on Google Cloud Run.

## Features
- JSON response format with romanized Urdu, English translation, and detected language
- Supports multiple input languages
- Scalable cloud deployment
- Simple REST API interface

## Prerequisites
- Google Cloud account with billing enabled
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed
- [Docker](https://docs.docker.com/get-docker/) installed
- OpenAI API key

## Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/your-organization/cb-chatbot.git
cd cb-chatbot
```

### 2. Environment Setup
Create `.env` file:
```bash
OPENAI_API_KEY=your-openai-api-key
```

### 3. Build Docker Image
```bash
docker build -t chatbot-api .
```

### 4. Test Locally
```bash
docker run -p 8080:8080 --env-file .env chatbot-api
```

Test with:
```bash
curl -X POST http://localhost:8080/chat -H "Content-Type: application/json" -d '{"prompt": "Your message here"}'
```

### 5. Deploy to Google Cloud Run

#### Authenticate with GCP
```bash
gcloud auth login
gcloud config set project codeblossom
```

#### Build and Submit Container
```bash
gcloud builds submit --tag gcr.io/codeblossom/chatbot-api
```

#### Deploy Service
```bash
gcloud run deploy chatbot-api \
  --image gcr.io/codeblossom/chatbot-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY="your-api-key"
```

## API Documentation

### Endpoints
- `POST /chat` - Main chat endpoint
- `GET /` - Health check endpoint

### Request Format
```json
{
  "prompt": "Your message here"
}
```

### Response Format
```json
{
  "response": {
    "roman-urdu": "Romanized Urdu response",
    "translation": "English translation",
    "speaker_language": "Detected input language"
  }
}
```

## Testing

### PowerShell Examples
```powershell
# Health check
Invoke-RestMethod -Uri "https://chatbot-api-xxxxx.a.run.app" -Method Get

# Chat request
$headers = @{"Content-Type" = "application/json"}
$body = @{"prompt" = "Hello kya haal hain apkay?"} | ConvertTo-Json
Invoke-RestMethod -Uri "https://chatbot-api-xxxxx.a.run.app/chat" -Method Post -Headers $headers -Body $body
```

## Environment Variables
| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | Your OpenAI API key |
| `PORT` | No | Server port (default: 8080) |

## Troubleshooting

### Common Issues
1. **Docker Build Failures**
   - Verify Dockerfile exists in project root
   - Check file permissions: `chmod 644 *`

2. **Missing Dependencies**
   - Run `pip install -r requirements.txt` locally to verify

3. **API Key Errors**
   - Confirm key is set in deployment: `gcloud run services describe chatbot-api`

4. **CORS Issues**
   - Add CORS middleware if accessing from web frontend

### View Logs
```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=chatbot-api" --limit 50
```

## Security Best Practices
1. Use Google Secret Manager for API keys in production:
```bash
gcloud secrets create openai-key --data-file=.env
```

2. Enable service authentication:
```bash
gcloud run services update chatbot-api --no-allow-unauthenticated
```

3. Regular dependency updates:
```bash
pip list --outdated
```

## Maintenance
- Update dependencies: `pip freeze > requirements.txt`
- Redeploy changes: Repeat build/deploy steps
- Monitor costs: https://console.cloud.google.com/billing