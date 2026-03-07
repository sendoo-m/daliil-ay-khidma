"""
fix_namespaces.py  v2
=====================
python fix_namespaces.py
"""

import os
import re
from pathlib import Path

TEMPLATES_DIR = "templates"
EXTENSIONS    = [".html", ".htm"]

SPECIFIC_REPLACEMENTS = [
    # ── أخطاء شائعة ──────────────────────────────────
    # admin_index بدون namespace → admin_home
    ("dashboard:admin_index",  "dashboard:admin_home"),
    ("'admin_index'",          "'dashboard:admin_home'"),

    # toggle_status → toggle  (الاسم في urls.py أقصر)
    ("admin_dashboard:user_toggle_status",      "dashboard:admin_user_toggle"),
    ("admin_dashboard:business_toggle_status",  "dashboard:admin_business_toggle"),
    ("admin_dashboard:product_toggle_status",   "dashboard:admin_product_toggle"),
    ("admin_dashboard:deal_toggle_status",      "dashboard:admin_deal_toggle"),

    # ── field names ───────────────────────────────────
    (".views_count",  ".view_count"),
    (".clicks_count", ".click_count"),

    # ── owner namespace ───────────────────────────────
    ("'owner:dashboard'",     "'dashboard:owner_dashboard'"),
    ("'owner:business_list'", "'dashboard:business_list'"),
    ("'owner:product_list'",  "'dashboard:product_list'"),
    ("'owner:deal_list'",     "'dashboard:deal_list'"),
    ("'owner:review_list'",   "'dashboard:review_list'"),

    # ── dashboard shortcuts ───────────────────────────
    ("'dashboard:home'",  "'dashboard:index'"),
    ("'dashboard:stats'", "'dashboard:notifications'"),
]


def fix_file(path: Path) -> tuple[int, int]:
    try:
        content = path.read_text(encoding="utf-8")
    except Exception:
        return 0, 1

    original = content

    # 1. Specific first
    for old, new in SPECIFIC_REPLACEMENTS:
        content = content.replace(old, new)

    # 2. General: admin_dashboard:X → dashboard:admin_X
    content = re.sub(r"admin_dashboard:(\w+)", r"dashboard:admin_\1", content)

    if content == original:
        return 0, 0

    path.write_text(content, encoding="utf-8")
    count = len(re.findall(r"admin_dashboard:", original))
    return max(count, 1), 0


def main():
    base = Path(TEMPLATES_DIR)
    if not base.exists():
        print(f"ERROR: '{TEMPLATES_DIR}' not found")
        return

    files  = [p for p in base.rglob("*") if p.suffix in EXTENSIONS]
    total  = len(files)
    fixed  = 0
    errors = 0

    print(f"Scanning {total} files in '{TEMPLATES_DIR}/'...\n")

    for f in files:
        count, err = fix_file(f)
        errors += err
        if err:
            print(f"  ERROR: {f}")
        elif count > 0:
            fixed += 1
            print(f"  OK: {f.relative_to(base)} ({count} replacements)")

    print(f"""
Done!
  Files scanned : {total}
  Files fixed   : {fixed}
  Errors        : {errors}
""")

if __name__ == "__main__":
    main()
