#!/usr/bin/env python3
import json
import re
import subprocess
import sys
from pathlib import Path

import pandas as pd

if sys.prefix == sys.base_prefix:
    print("WARNING: virtual environment not active")

REPO_ROOT = Path(__file__).resolve().parents[1]

INPUT_ODS = REPO_ROOT / "data" / "photo_names_sorted.ods"

OUTPUT_JS = REPO_ROOT / "js" / "people-data.js"
OUTPUT_JSON = REPO_ROOT / "photos-with-names" / "people-index.json"

FULL_DIR = REPO_ROOT / "photos-with-names" / "full"
THUMB_DIR = REPO_ROOT / "photos-with-names" / "thumbnails"

THUMB_MAX = "420x"
JPEG_QUALITY = "82"


# -------- HELPERS --------

def norm_photo_file(s: str) -> str:
    s = (s or "").strip()

    s = re.sub(r"^(?:full/|thumbnails/)+", "", s, flags=re.IGNORECASE)

    if s and not re.search(r"\.[A-Za-z0-9]{2,4}$", s):
        s += ".jpg"

    return s


def find_imagemagick_cmd():
    import shutil
    return shutil.which("magick") or shutil.which("convert")


def imagemagick_available(cmd):
    try:
        subprocess.run([cmd, "-version"],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL,
                       check=True)
        return True
    except Exception:
        return False


def ensure_thumbnails(files):

    im_cmd = find_imagemagick_cmd()

    if not im_cmd or not imagemagick_available(im_cmd):
        print("NOTE: ImageMagick not found — skipping thumbnail generation.")
        return

    THUMB_DIR.mkdir(parents=True, exist_ok=True)

    to_make = []

    for fn in sorted(set(files)):
        if not fn:
            continue

        full_path = FULL_DIR / fn
        thumb_path = THUMB_DIR / fn

        if not full_path.exists():
            print(f"WARNING: full image missing: {full_path}")
            continue

        if not thumb_path.exists():
            to_make.append(fn)

    if not to_make:
        print("Thumbnails: all present.")
        return

    print(f"Thumbnails: generating {len(to_make)} new thumbnail(s)…")

    for fn in to_make:

        full_path = FULL_DIR / fn
        thumb_path = THUMB_DIR / fn

        thumb_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            subprocess.run([
                im_cmd,
                str(full_path),
                "-thumbnail", THUMB_MAX,
                "-strip",
                "-quality", JPEG_QUALITY,
                str(thumb_path),
            ], check=True)

        except subprocess.CalledProcessError as e:
            print(f"ERROR: failed to thumbnail {fn}: {e}")


# -------- MAIN LOGIC --------

def load_records():

    if not INPUT_ODS.exists():
        raise SystemExit(f"ERROR: Cannot find {INPUT_ODS}")

    df = pd.read_excel(INPUT_ODS, engine="odf")

    required_cols = ["Surname", "Full Name", "Photo File Name"]

    for c in required_cols:
        if c not in df.columns:
            raise SystemExit(
                f"ERROR: Column '{c}' not found in {INPUT_ODS.name}"
            )

    records = []
    photo_files = []

    for _, row in df.iterrows():

        surname = str(row.get("Surname", "") or "").strip()
        full_name = str(row.get("Full Name", "") or "").strip()
        photo_file_raw = str(row.get("Photo File Name", "") or "").strip()

        if not surname and not full_name and not photo_file_raw:
            continue

        photo_file = norm_photo_file(photo_file_raw)

        rec = {
            "surname": surname,
            "fullName": full_name,
            "photoFile": photo_file
        }

        records.append(rec)

        if photo_file:
            photo_files.append(photo_file)

    return records, photo_files


def write_people_js(records):

    OUTPUT_JS.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_JS.open("w", encoding="utf-8") as f:

        f.write("const people = [\n")

        for rec in records:
            f.write("  " + json.dumps(rec, ensure_ascii=False) + ",\n")

        f.write("];\n")

    print(f"Wrote {len(records)} records → {OUTPUT_JS}")


def write_people_json(records):

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)

    OUTPUT_JSON.write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"Wrote {len(records)} records → {OUTPUT_JSON}")


def main():

    records, photo_files = load_records()

    write_people_js(records)

    write_people_json(records)

    ensure_thumbnails(photo_files)


if __name__ == "__main__":
    main()
