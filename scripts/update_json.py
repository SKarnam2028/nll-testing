import csv, json, requests, sys

CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ6bqRAX_vzRAkaQh6sk4dmebL7eEl0DlFmzul5reiWK29Pkjs1yjfyKkc2zUgDqTmNCB8272upK-2H/pub?output=csv"

r = requests.get(CSV_URL)
r.encoding = "utf-8"

rows = csv.DictReader(r.text.splitlines())

lexicon = []

for row in rows:
    if not row["Headword"]:
        continue

    entry = {
        "headword": row["Headword"],
        "domains": [row["Domain 1"], row["Domain 2"], row["Domain 3"]],
        "terms": []
    }

    for i in range(1, 11):
        term = row.get(f"Latin Term {i}")
        if term:
            entry["terms"].append({
                "latin": term,
                "macronized": row.get(f"Macronized {i}", ""),
                "grammar": row.get(f"Grammar {i}", ""),
                "citation": row.get(f"Citation {i}", ""),
                "notes": row.get(f"Notes {i}", "")
            })

    lexicon.append(entry)

with open("lexicon.json", "w", encoding="utf-8") as f:
    json.dump(lexicon, f, ensure_ascii=False, indent=2)

print(f"Wrote {len(lexicon)} entries")
