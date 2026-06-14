# -------------------------
# 1. READ INPUT
# -------------------------
def read_input(raw_text):
    """
    Splits raw text into clean lines
    """
    lines = raw_text.strip().split("\n")
    return [line.strip() for line in lines if line.strip()]