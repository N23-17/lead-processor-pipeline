import re

# -------------------------
# 2. PARSE LINE
# -------------------------
def parse_line(line):
    """
    Extracts name, course, year from messy input
    Supports: comma, semicolon, or space-separated formats
    """
    # Normalize separators
    line = re.sub(r"[;,]", " ", line)
    parts = line.split()

    if len(parts) < 3:
        return None  # invalid line

    name = parts[0]
    course = " ".join(parts[1:-1])
    year = parts[-1]

    return {
        "name": name,
        "course": course,
        "year": year
    }