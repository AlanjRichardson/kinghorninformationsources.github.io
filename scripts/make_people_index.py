#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

import sys
if sys.prefix == sys.base_prefix:
    print("WARNING: virtual environment not active")


REPO_ROOT = Path("/home/alan/kinghorninformationsources.github.io")

PEOPLE_JS = REPO_ROOT / "js" / "people-data.js"   # change if yours is elsewhere
OUT_JSON  = REPO_ROOT / "photos-with-names" / "people-index.json"  # output for gallery use

def die(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)

def strip_js_comments(s: str) -> str:
    # Remove //... and /*...*/ comments (simple, good enough for your data file)
    s = re.sub(r"//.*?$", "", s, flags=re.MULTILINE)
    s = re.sub(r"/\*.*?\*/", "", s, flags=re.DOTALL)
    return s

def extract_array_literal(js_text: str) -> str:
    # Find first '[' after 'const people' (or just first '[') and last ']'
    m = re.search(r"\bpeople\b\s*=\s*\[", js_text)
    if m:
        start = js_text.find("[", m.start())
    else:
        start = js_text.find("[")
    end = js_text.rfind("]")
    if start == -1 or end == -1 or end <= start:
        die("Could not locate [ ... ] array in people-data.js")
    return js_text[start:end+1]

def remove_trailing_commas(s: str) -> str:
    # Remove trailing commas before } or ] (JSON doesn't allow them)
    # This is a common, safe cleanup for JS data arrays like yours.
    return re.sub(r",(\s*[}\]])", r"\1", s)

def main():
    if not PEOPLE_JS.exists():
        die(f"Could not find {PEOPLE_JS}")

    js = PEOPLE_JS.read_text(encoding="utf-8", errors="replace")
    js = strip_js_comments(js)

    arr = extract_array_literal(js)
    arr = remove_trailing_commas(arr)

    try:
        data = json.loads(arr)
    except Exception as e:
        # Show a helpful hint around where it failed
        die(f"Could not parse people-data.js array into JSON.\nDetails: {e}")

    if not isinstance(data, list):
        die("Parsed data is not a list")

    # Minimal validation
    for i, row in enumerate(data[:10]):
        if not isinstance(row, dict):
            die(f"Entry {i} is not an object")

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK: wrote {OUT_JSON} with {len(data)} entries")

if __name__ == "__main__":
    main()
