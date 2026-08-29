import csv
from collections import defaultdict
from pathlib import Path

DATASET = Path("../idoft/pr-data.csv")
OUTPUT = Path("subjects/candidate_projects.csv")

PROJECT_COL = "Project URL"
SHA_COL = "SHA Detected"
MODULE_COL = "Module Path"
TEST_COL = "Fully-Qualified Test Name (packageName.ClassName.methodName)"
CATEGORY_COL = "Category"
STATUS_COL = "Status"


def is_od(category: str) -> bool:
    """Return True for Order-Dependent related categories."""
    category = category.strip().upper()
    return category.startswith("OD")


def is_id(category: str) -> bool:
    """Return True for Implementation-Dependent category."""
    return category.strip().upper() == "ID"


with DATASET.open(newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))


# Group tests that can potentially be examined from ONE checkout/build.
groups = defaultdict(list)

for row in rows:
    project = row[PROJECT_COL].strip()
    sha = row[SHA_COL].strip()
    module = row[MODULE_COL].strip()

    if not project or not sha:
        continue

    groups[(project, sha, module)].append(row)


candidates = []

for (project, sha, module), tests in groups.items():

    categories = sorted(
        {
            row[CATEGORY_COL].strip()
            for row in tests
            if row[CATEGORY_COL].strip()
        }
    )

    statuses = sorted(
        {
            row[STATUS_COL].strip()
            for row in tests
            if row[STATUS_COL].strip()
        }
    )

    od_count = sum(
        1 for row in tests
        if is_od(row[CATEGORY_COL])
    )

    id_count = sum(
        1 for row in tests
        if is_id(row[CATEGORY_COL])
    )

    # Simple ranking score for our exploratory experiment.
    score = 0

    # Multiple flaky tests from one checkout are valuable.
    score += len(tests) * 2

    # Root Maven modules tend to be easier to work with.
    if module in ("", "."):
        score += 5

    # Having both OD and ID allows us to use
    # iDFlakies + NonDex within the same checkout.
    if od_count > 0 and id_count > 0:
        score += 15

    # Even multiple tests from either category are useful.
    score += min(od_count, 5)
    score += min(id_count, 5)

    candidates.append({
        "Score": score,
        "Project URL": project,
        "SHA": sha,
        "Module": module or ".",
        "Total Tests": len(tests),
        "OD Tests": od_count,
        "ID Tests": id_count,
        "Categories": "; ".join(categories),
        "Statuses": "; ".join(statuses) if statuses else "-"
    })


candidates.sort(
    key=lambda x: (
        -x["Score"],
        -x["Total Tests"],
        x["Project URL"]
    )
)


# Save results for the GitHub experiment repository.
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

with OUTPUT.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=candidates[0].keys())
    writer.writeheader()
    writer.writerows(candidates)


print(
    f'{"SCORE":<7}'
    f'{"TOTAL":<7}'
    f'{"OD":<5}'
    f'{"ID":<5}'
    f'{"MODULE":<22}'
    f'{"CATEGORIES":<35}'
    f'PROJECT'
)

print("-" * 145)

for candidate in candidates[:30]:

    print(
        f'{candidate["Score"]:<7}'
        f'{candidate["Total Tests"]:<7}'
        f'{candidate["OD Tests"]:<5}'
        f'{candidate["ID Tests"]:<5}'
        f'{candidate["Module"][:21]:<22}'
        f'{candidate["Categories"][:34]:<35}'
        f'{candidate["Project URL"]}'
    )

    print(f'       SHA: {candidate["SHA"]}')
    print(f'       Status: {candidate["Statuses"]}')
    print()


print(f"\nSaved {len(candidates)} candidates to:")
print(OUTPUT)
