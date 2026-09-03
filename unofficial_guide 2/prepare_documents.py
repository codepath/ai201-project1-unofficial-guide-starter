"""
Filters the University of Oregon RateMyProfessors dataset (Kaggle:
kaggle.com/datasets/eastonsell/university-of-oregon-ratemyprofessors)
down to a diverse sample of individual reviews and exports them as .txt
files for the pipeline.

Setup:
    1. Download the dataset from the Kaggle link above (Download button,
       or `kaggle datasets download -d eastonsell/university-of-oregon-ratemyprofessors`
       if you have the Kaggle CLI configured).
    2. Unzip it. You should see a `professors.json` file and a `reviews/`
       folder containing one <legacyId>.json file per professor.
    3. Place both `professors.json` and the `reviews/` folder next to this
       script (or update PROFESSORS_PATH / REVIEWS_DIR below).
    4. python prepare_documents.py

The exact field name used for the free-text comment isn't published outside
the file itself, so this script inspects the first review it loads and
prints its keys — check that output once to confirm COMMENT_FIELD_CANDIDATES
below actually matches, and adjust if needed.
"""

import json
import os
import re
import random

PROFESSORS_PATH = "professors.json"
REVIEWS_DIR = "reviews"
OUT_DIR = "documents"

NUM_PROFESSORS_TO_SAMPLE = 15   # spread across departments for variety
REVIEWS_PER_PROFESSOR = 2       # keep total doc count reasonable
MIN_COMMENT_LEN = 40

# Try these field names in order — RMP's GraphQL Rating node has historically
# used "comment" for the free-text field.
COMMENT_FIELD_CANDIDATES = ["comment", "comments", "rComments", "text", "review"]
COURSE_FIELD_CANDIDATES = ["class", "courseCode", "course"]


def safe_filename(s: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]", "_", str(s))[:60]


def find_field(obj: dict, candidates: list[str]):
    for key in candidates:
        if key in obj and obj[key]:
            return key
    return None


def main():
    with open(PROFESSORS_PATH, "r", encoding="utf-8") as f:
        professors = json.load(f)
    print(f"Loaded {len(professors)} professors.")

    # Spread the sample across departments rather than picking randomly,
    # so we don't end up with 15 professors all from the same department.
    by_dept = {}
    for p in professors:
        dept = p.get("department", "unknown")
        by_dept.setdefault(dept, []).append(p)

    depts = list(by_dept.keys())
    random.seed(42)
    random.shuffle(depts)

    sampled_profs = []
    for dept in depts:
        if len(sampled_profs) >= NUM_PROFESSORS_TO_SAMPLE:
            break
        candidates = [p for p in by_dept[dept] if p.get("numRatings", 0) >= REVIEWS_PER_PROFESSOR]
        if candidates:
            sampled_profs.append(random.choice(candidates))

    print(f"Sampled {len(sampled_profs)} professors across {len(set(p.get('department') for p in sampled_profs))} departments.")

    os.makedirs(OUT_DIR, exist_ok=True)
    doc_count = 0
    comment_field = None
    course_field = None
    printed_keys = False

    for prof in sampled_profs:
        legacy_id = prof.get("legacyId")
        review_path = os.path.join(REVIEWS_DIR, f"{legacy_id}.json")
        if not os.path.exists(review_path):
            continue

        with open(review_path, "r", encoding="utf-8") as f:
            reviews = json.load(f)

        # reviews might be a list directly, or wrapped in a dict — handle both
        if isinstance(reviews, dict) and "reviews" in reviews:
            reviews = reviews["reviews"]

        if not reviews:
            continue

        if not printed_keys:
            print("\n--- First review object's keys (verify comment field) ---")
            print(list(reviews[0].keys()))
            comment_field = find_field(reviews[0], COMMENT_FIELD_CANDIDATES)
            course_field = find_field(reviews[0], COURSE_FIELD_CANDIDATES)
            print(f"Detected comment field: {comment_field}")
            print(f"Detected course field: {course_field}\n")
            printed_keys = True

            if comment_field is None:
                print("⚠️  Could not auto-detect the comment field. Open one "
                      "reviews/<id>.json file yourself, find the free-text "
                      "field name, and add it to COMMENT_FIELD_CANDIDATES.")
                return

        random.shuffle(reviews)
        taken = 0
        for review in reviews:
            if taken >= REVIEWS_PER_PROFESSOR:
                break
            comment = review.get(comment_field, "")
            if not comment or len(comment) < MIN_COMMENT_LEN:
                continue

            doc_count += 1
            course = review.get(course_field, "") if course_field else ""
            name = f"{prof.get('firstName','')}_{prof.get('lastName','')}"
            filename = f"{doc_count:02d}_{safe_filename(name)}_{safe_filename(course)}.txt"

            header = f"Professor: {prof.get('firstName','')} {prof.get('lastName','')}\n" \
                     f"Department: {prof.get('department','')}\n" \
                     f"Course: {course}\n\n"

            with open(os.path.join(OUT_DIR, filename), "w", encoding="utf-8") as f:
                f.write(header + str(comment))

            taken += 1

    print(f"\n✅ Wrote {doc_count} review files to '{OUT_DIR}/'.")
    if doc_count < 10:
        print("⚠️  Fewer than 10 documents — increase NUM_PROFESSORS_TO_SAMPLE "
              "or REVIEWS_PER_PROFESSOR and re-run.")


if __name__ == "__main__":
    main()

