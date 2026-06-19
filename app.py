
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
import re
import requests
import datetime
import os
APP_VERSION = "1.0.0"
# Load API keys from environment, strip whitespace and ignore empty values
VALID_KEYS = [k.strip() for k in os.environ.get("API_KEYS", "").split(",") if k.strip()]



# ==================================================
# FASTAPI
# ==================================================

app = FastAPI(
    title="Lead Processor API",
    version=APP_VERSION
)

# ==================================================
# REQUEST MODEL
# ==================================================

class LeadInput(BaseModel):
    raw_text: str = Field(
        ...,
        min_length=1,
        description="Raw lead data"
    )

# ==================================================
# LOGGER
# ==================================================

def log_message(message, level="INFO"):

    import json

    log_entry = {
        "timestamp": str(datetime.datetime.now()),
        "level": level,
        "message": message
    }

    print(json.dumps(log_entry))

# ==================================================
# INPUT READER
# ==================================================

def read_input(raw_text):
    lines = raw_text.strip().split("\n")

    return [
        line.strip()
        for line in lines
        if line.strip()
    ]

# ==================================================
# PARSER
# ==================================================

def parse_line(line):

    line = re.sub(r"[;,]", " ", line)

    parts = line.split()

    if len(parts) < 3:
        return None

    name = parts[0]
    course = " ".join(parts[1:-1])
    year = parts[-1]

    return {
        "name": name,
        "course": course,
        "year": year
    }

# ==================================================
# VALIDATOR
# ==================================================

def validate_record(record):

    if not record:
        return False

    if not record["name"].replace(" ", "").isalpha():
        return False

    if not record["year"].isdigit():
        return False

    if not record["course"].strip():
        return False

    return True

# ==================================================
# N8N CLIENT
# ==================================================

def send_to_n8n(data):
    import os
    import requests
    url = os.environ.get("N8N_WEBHOOK_URL")

    # Accept either the full result (with 'pipeline_result') or a direct summary dict
    pipeline = data.get("pipeline_result") if isinstance(data, dict) and "pipeline_result" in data else data

    payload = {
        "source": "lead_processor_api",
        "timestamp": str(datetime.datetime.now()),
        "summary": pipeline,
        "metrics": {
            "total": pipeline.get("total") if isinstance(pipeline, dict) else None,
            "valid": pipeline.get("valid") if isinstance(pipeline, dict) else None,
            "skipped": pipeline.get("skipped") if isinstance(pipeline, dict) else None
        }
    }

    if url:
        try:
            response = requests.post(url, json=payload, timeout=10)
            log_message(f"Webhook sent to n8n with payload size: {len(str(payload))}")
            return response.json()
        except Exception as e:
            log_message(f"Failed to send webhook: {str(e)}", "ERROR")
            return None
    else:
        log_message("N8N_WEBHOOK_URL not configured", "WARNING")
        return None

# ==================================================
# MAIN PROCESSOR
# ==================================================

def process_leads(raw_text):

    lines = read_input(raw_text)

    results = []

    skipped = 0

    log_message(
        f"Processing {len(lines)} lines"
    )

    for line in lines:

        record = parse_line(line)

        if record is not None and validate_record(record):

            results.append(record)

            log_message(
                f"Valid record: {record['name']}"
            )

        else:

            skipped += 1

            log_message(
                f"Skipped: {line}",
                "WARNING"
            )

    summary = {
        "valid_leads": results,
        "total": len(lines),
        "valid": len(results),
        "skipped": skipped
    }

    n8n_response = send_to_n8n(summary)

    return {
        "pipeline_result": summary,
        "n8n": n8n_response
    }

# ==================================================
# ROUTES
# ==================================================

@app.get("/")
def home():

    return {
        "status": "online",
        "service": "Lead Processor API"
    }

@app.post("/process")
def process_endpoint(data: LeadInput, x_api_key: str = Header(None)):

    if x_api_key not in VALID_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    log_message(f"Request received: {len(data.raw_text)} chars")

    try:
        result = process_leads(data.raw_text)

        return {
            "success": True,
            "data": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))