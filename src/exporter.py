# -------------------------
# 5. EXPORT
# -------------------------

import csv
import json


def export_json(data, filename="leads.json"):
    """
    Saves data into a JSON file
    """

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

    print(f"JSON exported to {filename}")

# -------------------------
# 6. CSV EXPORT (BONUS)
# -------------------------

def export_csv(data, filename="leads.csv"):
    """
    Saves data into a CSV file
    """
    leads = data["valid_leads"]
    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "course", "year"])
        writer.writeheader()
        writer.writerows(leads)

    print(f"CSV exported to {filename}")