Lead Processor API

A FastAPI-powered lead processing service that:

Cleans raw text input
Extracts structured lead data
Validates records
Logs processing activity
Integrates with n8n workflows

Features

FastAPI backend
Automatic Swagger documentation
Input validation with Pydantic
Lead parsing engine
Logging system
n8n webhook integration

Installation
    pip install -r requirements.txt
Run
    python -m uvicorn app:app --reload

API Documentation

Visit:

http://127.0.0.1:8000/docs

Example Request
{
  "raw_text": "Imran, Computer Science, 1\nJohn; IT; 2"
}

Deployment (Render)

Set the following environment variables in your Render service settings:

- `API_KEYS` — comma-separated API keys allowed to access the API (e.g. `dev-key-123,another-key`).
- `N8N_WEBHOOK_URL` — optional webhook URL for n8n integration (leave empty to disable).

Locally on Windows (PowerShell) set for the session:

```powershell
$env:API_KEYS = 'dev-key-123'
$env:N8N_WEBHOOK_URL = ''
python -m uvicorn app:app --reload
```

Verify the `x-api-key` header matches one of the values in `API_KEYS` when calling `/process`.