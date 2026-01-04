#!/usr/bin/env python3
import json
import re
import subprocess
from pathlib import Path

import pandas as pd

import sys
if sys.prefix == sys.base_prefix:
    print("WARNING: virtual environment not active")


REPO_ROOT = Path("/home/alan/kinghorninformationsources.github.io")

INPUT_ODS = REPO_ROOT / "data" / "photo_names_sorted.ods"
OUTPUT_JS = REPO_ROOT / "js" / "people-data.js"

# Where your gallery images live
FULL_DIR = REPO_ROOT / "photos-with-names" / "full"
THUMB_DIR = REPO_ROOT / "photos-with-names" / "thumbnails"

# Default thumbnail settings (match your earlier approach)
THUMB_MAX = "420x"      # max width 420, keep aspect
JPEG_QUALITY = "82"

# -------- HELPERS --------
def norm_photo_file(s: str) -> str:
    """
    Normalise photo file names coming from the spreadsheet:
    - trim whitespace
    - remove any leading folder like 'full/' or 'thumbnails/'
    - if no extension, assume .jpg
    - DO NOT change case (GitHub Pages is case-sensitive)
    """
    s = (s or "").strip()

    # Remove accidental leading folders
    s = re.sub(r"^(?:full/|thumbnails/)+", "", s, flags=re.IGNORECASE)

    # Add .jpg if no extension present
    if s and not re.search(r"\.[A-Za-z0-9]{2,4}$", s):
        s += ".jpg"

    return s

def magick_available() -> bool:
    try:
        subprocess.run(["magick", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except Exception:
        return False

def ensure_thumbnails(files: list[str]) -> None:
    """
    Create thumbnails only for files that exist in FULL_DIR
    and are missing in THUMB_DIR.
    """
    if not magick_available():
        print("NOTE: ImageMagick 'magick' not found. Skipping thumbnail generation.")
        return

    THUMB_DIR.mkdir(parents=True, exist_ok=True)

    to_make = []
    for fn in sorted(set(files)):
        if not fn:
            continue
        full_path = FULL_DIR / fn
        thumb_path = THUMB_DIR / fn

        if not full_path.exists():
            # Don't error; just warn
            print(f"WARNING: full image missing: {full_path}")
            continue

        if not thumb_path.exists():
            to_make.append(fn)

    if not to_make:
        print("Thumbnails: all present (no new thumbnails needed).")
        return

    print(f"Thumbnails: generating {len(to_make)} new thumbnail(s)…")

    # Create one by one (safer with odd filenames)
    for fn in to_make:
        full_path = FULL_DIR / fn
        thumb_path = THUMB_DIR / fn
        try:
            subprocess.run(
                [
                    "magick",
                    str(full_path),
                    "-thumbnail", THUMB_MAX,
                    "-strip",
                    "-quality", JPEG_QUALITY,
                    str(thumb_path),
                ],
                check=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"ERROR: failed to thumbnail {fn}: {e}")

def main():
    if not INPUT_ODS.exists():
        raise SystemExit(f"ERROR: Cannot find {INPUT_ODS.resolve()}")

    # Read the .ods
    df = pd.read_excel(INPUT_ODS, engine="odf")

    required_cols = ["Surname", "Full Name", "Photo File Name"]
    for c in required_cols:
        if c not in df.columns:
            raise SystemExit(f"ERROR: Column '{c}' not found in {INPUT_ODS.name}. Found: {list(df.columns)}")

    records = []
    photo_files = []

    for _, row in df.iterrows():
        surname = str(row.get("Surname", "") or "").strip()
        full_name = str(row.get("Full Name", "") or "").strip()
        photo_file_raw = str(row.get("Photo File Name", "") or "").strip()

        # Skip obvious empty rows
        if not surname and not full_name and not photo_file_raw:
            continue

        photo_file = norm_photo_file(photo_file_raw)

        records.append({
            "surname": surname,
            "fullName": full_name,
            "photoFile": photo_file
        })

        if photo_file:
            photo_files.append(photo_file)

    # Write JS file
    OUTPUT_JS.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_JS.open("w", encoding="utf-8") as f:
        f.write("const people = [\n")
        for rec in records:
            f.write("  " + json.dumps(rec, ensure_ascii=False) + ",\n")
        f.write("];\n")

    print(f"Wrote {len(records)} records to {OUTPUT_JS}")

    # Optional: generate missing thumbnails
    # Comment this out if you don't want it automatic
    ensure_thumbnails(photo_files)

if __name__ == "__main__":
    main()


