
# -------------------------
# 4. PROCESSOR ENGINE
# -------------------------
from logger import log_message
from parser import parse_line
from reader import read_input
from validator import validate_record


def process_leads(raw_text):
    lines = read_input(raw_text)

    results = []
    skipped = 0

    log_message(f"Processing started. Total lines: {len(lines)}")

    for line in lines:

        record = parse_line(line)

        if record is None:
            skipped += 1
            log_message(f"Invalid record skipped: {line}", level="WARNING")
            continue

        if validate_record(record):
            results.append(record)
            log_message(f"Valid record: {record['name']}")
        else:
            skipped += 1
            log_message(f"Invalid record skipped: {line}", level="WARNING")

    summary = {
        "valid_leads": results,
        "total": len(lines),
        "valid": len(results),
        "skipped": skipped
    }

    log_message(
        f"Processing complete. Valid: {len(results)}, Skipped: {skipped}",
        level="INFO"
    )

    return summary