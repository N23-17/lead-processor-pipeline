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