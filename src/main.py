import csv
import json
import os
import re
import datetime
from reader import read_input
from parser import parse_line
from validator import validate_record
from processor import process_leads
from exporter import export_json, export_csv
from logger import log_message


# -------------------------
# MAIN RUN
# -------------------------
if __name__ == "__main__":

    sample_data = """
    Imran, Computer Science, 1
    John; IT; 2
    Broken Line Example
    Mary Computer Science 3
    """

    result = process_leads(sample_data)

    print("\n=== PROCESS RESULT ===")

    export_json(result, "exports/leads.json")
    export_csv(result, "exports/leads.csv")