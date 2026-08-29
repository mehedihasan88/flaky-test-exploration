import csv
from pathlib import Path

DATASET = Path("../idoft/pr-data.csv")

with DATASET.open(newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    print("IDoFT pr-data.csv columns:\n")

    for i, column in enumerate(reader.fieldnames, start=1):
        print(f"{i}. {column}")
