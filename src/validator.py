# -------------------------
# 3. VALIDATION
# -------------------------
def validate_record(record):
    """
    Ensures data integrity
    """
    if not record:
        return False

    if not record["name"].isalpha():
        return False

    if not record["year"].isdigit():
        return False

    return True