import csv
from pathlib import Path

DATASET = Path("../idoft/pr-data.csv")
OUTPUT = Path("subjects/fastjson_tests.csv")

PROJECT = "https://github.com/alibaba/fastjson"
SHA = "e05e9c5e4be580691cc55a59f3256595393203a1"

TEST_COL = "Fully-Qualified Test Name (packageName.ClassName.methodName)"

with DATASET.open(newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

selected = [
    row for row in rows
    if row["Project URL"].strip() == PROJECT
    and row["SHA Detected"].strip() == SHA
]

selected.sort(key=lambda row: (row["Category"], row[TEST_COL]))

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

with OUTPUT.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            TEST_COL,
            "Category",
            "Status",
            "PR Link",
            "Notes",
        ],
    )

    writer.writeheader()

    for row in selected:
        writer.writerow({
            TEST_COL: row[TEST_COL],
            "Category": row["Category"],
            "Status": row["Status"],
            "PR Link": row["PR Link"],
            "Notes": row["Notes"],
        })

print(f"Found {len(selected)} Fastjson flaky-test entries.\n")

for row in selected:
    print(f'{row["Category"]:<12} {row[TEST_COL]}')

    if row["Status"]:
        print(f'             Status: {row["Status"]}')

    if row["Notes"]:
        print(f'             Notes: {row["Notes"]}')

print(f"\nSaved to: {OUTPUT}")
