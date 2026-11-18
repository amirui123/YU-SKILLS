#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
spec_check.py — بررسی مشخصات فنی اسکیل
بررسی نام، ساختار پوشه، متادیتا، طول توضیحات، فایل‌های مرجع، اسکریپت‌ها و فایل ارزیابی.
"""

import sys
import os
import json
import re

def check_skill(skill_dir: str) -> bool:
    print(f"=== بررسی مشخصات فنی اسکیل (Spec Check) ===")
    print(f"مسیر اسکیل: {skill_dir}\n")

    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.exists(skill_md):
        print(f"❌ خطا: فایل SKILL.md در {skill_dir} یافت نشد.")
        return False

    with open(skill_md, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()

    # استخراج Frontmatter
    frontmatter_match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not frontmatter_match:
        print("❌ خطا: Frontmatter در ابتدای SKILL.md یافت نشد.")
        return False

    fm_text = frontmatter_match.group(1)
    
    # نام
    name_match = re.search(r"^name:\s*([^\n\r]+)", fm_text, re.MULTILINE)
    if not name_match:
        print("❌ خطا: فیلد name در frontmatter یافت نشد.")
        return False
    name = name_match.group(1).strip().strip('"').strip("'")

    # نام پوشه
    folder_name = os.path.basename(os.path.normpath(skill_dir))

    # توضیحات
    desc_match = re.search(r"^description:\s*(\"[^\"]+\"|'[^']+'|[^\n\r]+)", fm_text, re.MULTILINE)
    desc = desc_match.group(1).strip().strip('"').strip("'") if desc_match else ""

    checks = []

    # ۱. نام ≤ ۶۴ کاراکتر
    c1 = len(name) <= 64
    checks.append(("نام ≤ ۶۴ کاراکتر", c1, f"{name} ({len(name)} کاراکتر)"))

    # ۲. نام برابر با نام پوشه
    c2 = (name == folder_name)
    checks.append(("نام = نام پوشه", c2, f"'{name}' == '{folder_name}'"))

    # ۳. توضیح ≤ ۱۰۲۴ کاراکتر
    c3 = len(desc) <= 1024
    checks.append(("توضیح ≤ ۱۰۲۴ کاراکتر", c3, f"{len(desc)} کاراکتر"))

    # ۴. توضیح شامل Use when
    c4 = "Use when" in desc
    checks.append(("توضیح شامل Use when", c4, "موجود است" if c4 else "یافت نشد"))

    # ۵. توضیح شامل Do NOT use
    c5 = "Do NOT use" in desc
    checks.append(("توضیح شامل Do NOT use", c5, "موجود است" if c5 else "یافت نشد"))

    # ۶. بدنه ≤ ۵۰۰ خط
    c6 = len(lines) <= 500
    checks.append(("بدنه ≤ ۵۰۰ خط", c6, f"{len(lines)} خط"))

    # ۷. بررسی مراجع
    ref_dir = os.path.join(skill_dir, "references")
    ref_files = [f for f in os.listdir(ref_dir) if f.endswith(".md")] if os.path.exists(ref_dir) else []
    c7 = len(ref_files) >= 10
    checks.append(("مراجع موجود (حداقل ۱۰ فایل)", c7, f"{len(ref_files)} فایل یافت شد"))

    # ۸. بررسی اسکریپت‌ها
    script_dir = os.path.join(skill_dir, "scripts")
    script_files = [f for f in os.listdir(script_dir) if f.endswith(".py")] if os.path.exists(script_dir) else []
    c8 = len(script_files) >= 5
    checks.append(("اسکریپت‌ها موجود (حداقل ۵ فایل)", c8, f"{len(script_files)} فایل یافت شد"))

    # ۹. بررسی JSON ارزیابی
    eval_json = os.path.join(skill_dir, "evals", "evals.json")
    eval_valid = False
    eval_count = 0
    if os.path.exists(eval_json):
        try:
            with open(eval_json, "r", encoding="utf-8") as ef:
                edata = json.load(ef)
                eval_count = len(edata.get("tests", []))
                eval_valid = (eval_count >= 50)
        except Exception:
            eval_valid = False
    c9 = eval_valid
    checks.append(("فایل ارزیابی معتبر (≥ ۵۰ تست)", c9, f"{eval_count} تست معتبر"))

    all_passed = True
    for label, passed, detail in checks:
        icon = "✅" if passed else "❌"
        print(f"[{icon}] {label}: {detail}")
        if not passed:
            all_passed = False

    print("\n" + "=" * 50)
    if all_passed:
        print("نتیجه spec_check: همه بررسی‌ها با موفقیت قبول شدند ✅")
    else:
        print("نتیجه spec_check: نقص در مشخصات فنی اسکیل ❌")
    print("=" * 50)

    return all_passed

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "skills/quran-hadith-verifier"
    ok = check_skill(target)
    sys.exit(0 if ok else 1)
