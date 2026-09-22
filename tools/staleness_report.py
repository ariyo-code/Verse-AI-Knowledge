#!/usr/bin/env python3
"""Reports knowledge cards that have not been reviewed recently."""

from pathlib import Path
import json
from datetime import date, datetime

ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT/"knowledge/api_catalog.json").read_text(encoding="utf-8"))
verified = datetime.strptime(catalog["last_verified"], "%Y-%m-%d").date()
age = (date.today() - verified).days

print(f"Catalog last verified: {verified} ({age} days ago)")
if age > 30:
    print("WARNING: API knowledge is older than 30 days. Recheck Epic documentation.")
else:
    print("Catalog freshness: OK (<31 days)")
