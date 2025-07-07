import json

with open("data/sample_queries.json") as f:
    data = json.load(f)

seen = set()
unique = []
for item in data:
    key = (item["query"].strip().lower(), item["intent"])
    if key not in seen:
        seen.add(key)
        unique.append(item)

with open("data/sample_queries.json", "w") as f:
    json.dump(unique, f, indent=2)

print(f"Deduplicated: {len(data)} -> {len(unique)} unique queries.")
