#!/usr/bin/env python3
import sys, json

def normalize(obj):
    if isinstance(obj, dict):
        # Sort keys and normalize values
        return {k: normalize(obj[k]) for k in sorted(obj)}
    elif isinstance(obj, list):
        # Normalize each item first
        normalized_items = [normalize(x) for x in obj]

        # If items are dicts, try to sort by a stable key
        if all(isinstance(x, dict) for x in normalized_items):
            for key in ("path", "tagPath", "name"):
                if all(key in x for x in normalized_items):
                    return sorted(normalized_items, key=lambda d: d[key])
            # Fallback: sort by string form
            return sorted(normalized_items, key=lambda d: json.dumps(d, sort_keys=True))
        
        # If items are primitives, just sort them directly
        if all(isinstance(x, (str, int, float, bool, type(None))) for x in normalized_items):
            return sorted(normalized_items)

        # Mixed types: sort by string form
        return sorted(normalized_items, key=lambda x: str(x))

    else:
        return obj

def normalize_file(infile, outfile):
    with open(infile, "r", encoding="utf-8") as f:
        data = json.load(f)
    normalized = normalize(data)
    with open(outfile, "w", encoding="utf-8") as f:
        json.dump(normalized, f, indent=2, ensure_ascii=False)
        f.write("\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python normalize_json.py input.json [output.json]")
        sys.exit(1)

    infile = sys.argv[1]
    outfile = sys.argv[2] if len(sys.argv) > 2 else infile
    normalize_file(infile, outfile)
