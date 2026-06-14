# -------------------------
# 7. LOGGER
# -------------------------

from datetime import datetime


def log_message(message, level="INFO"):
    """
    Simple logging utility
    """

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = f"[{timestamp}] [{level}] {message}"

    print(log_entry)

    # Save to file
    with open("pipeline.log", "a") as file:
        file.write(log_entry + "\n")