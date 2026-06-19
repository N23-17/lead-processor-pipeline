
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import re
import requests
import datetime
import os
APP_VERSION = "1.0.0"


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
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = f"[{timestamp}] [{level}] {message}"

    print(log_entry)

    with open("pipeline.log", "a") as file:
        file.write(log_entry + "\n")

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

    # DEBUG (temporary but useful)
    if not url:
        return {
            "status": "not_configured",
            "debug": "N8N_WEBHOOK_URL is missing in environment"
        }

    try:
        response = requests.post(
            url,
            json=data,
            timeout=10
        )

        return {
            "status": "sent",
            "status_code": response.status_code
        }

    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }

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
def process_endpoint(data: LeadInput):

    try:

        result = process_leads(
            data.raw_text
        )

        return {
            "success": True,
            "data": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )