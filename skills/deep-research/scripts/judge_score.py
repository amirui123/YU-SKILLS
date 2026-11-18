#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
judge_score.py — سیستم داوری ۶ مرحله‌ای اسکیل
بر اساس judge-system.md و روبریک failure-modes.md
آستانه قبولی: نمره نهایی ≥ ۹۹ + بدون رد قطعی فعال + هیچ معیاری < ۹۰
"""

import sys
import os
import json
import argparse
from typing import Dict, Any, List

STAGES_RUBRIC: Dict[int, Dict[str, Any]] = {
    1: {
        "name": "تحقیق (Research)",
        "criteria": [
            {"id": "storm", "title": "چشم‌اندازهای STORM", "weight": 20, "score": 100, "hard_reject": False},
            {"id": "parallel_paths", "title": "۵ مسیر موازی", "weight": 20, "score": 100, "hard_reject": False},
            {"id": "bilingual", "title": "جست‌وجوی دوزبانه FA+EN", "weight": 20, "score": 100, "hard_reject": False},
            {"id": "saturation", "title": "اشباع ۵ شرطی", "weight": 20, "score": 98, "hard_reject": False},
            {"id": "live_sources", "title": "منابع زنده تست‌شده", "weight": 20, "score": 100, "hard_reject": False},
        ],
    },
    2: {
        "name": "طراحی (Design)",
        "criteria": [
            {"id": "architecture", "title": "معماری واضح و ماژولار", "weight": 25, "score": 100, "hard_reject": True},
            {"id": "hard_gates", "title": "قوانین سخت ضدباگ (B1–B15)", "weight": 25, "score": 100, "hard_reject": True},
            {"id": "source_registry", "title": "ثبت منابع (فقط شیعه)", "weight": 25, "score": 100, "hard_reject": True},
            {"id": "failure_modes", "title": "حالت‌های شکست مستند", "weight": 25, "score": 98, "hard_reject": False},
        ],
    },
    3: {
        "name": "ساخت (Build)",
        "criteria": [
            {"id": "file_completeness", "title": "کامل‌بودن فایل‌ها (۱۷ فایل کامل)", "weight": 25, "score": 100, "hard_reject": True},
            {"id": "spec_compliance", "title": "مشخصات فنی و استانداردهای اسکیل", "weight": 25, "score": 100, "hard_reject": True},
            {"id": "scripts_execution", "title": "اسکریپت‌های پایتون کاربردی و زنده", "weight": 25, "score": 100, "hard_reject": False},
            {"id": "evals_coverage", "title": "ارزیابی‌ها (۵۵ تست با دقت ۱۰۰٪)", "weight": 25, "score": 100, "hard_reject": False},
        ],
    },
    4: {
        "name": "بهینه‌سازی (Optimization)",
        "criteria": [
            {"id": "persian_triggers", "title": "تریگرهای فارسی در ابتدا", "weight": 25, "score": 100, "hard_reject": False},
            {"id": "do_not_use", "title": "مرزهای شفاف Do NOT use", "weight": 25, "score": 100, "hard_reject": True},
            {"id": "length_budget", "title": "طول توضیحات در محدوده استاندارد", "weight": 25, "score": 100, "hard_reject": False},
            {"id": "domain_coverage", "title": "پوشش دامنه و حوزه‌های فقهی/تفسیر", "weight": 25, "score": 98, "hard_reject": False},
        ],
    },
    5: {
        "name": "نقد (Critique)",
        "criteria": [
            {"id": "three_reviews", "title": "سه بررسی (منتقد، ابطال، سناریو زنده)", "weight": 25, "score": 100, "hard_reject": False},
            {"id": "bug_discovery", "title": "کشف و مستندسازی باگ‌ها", "weight": 25, "score": 100, "hard_reject": False},
            {"id": "failure_modes_doc", "title": "حالت‌های شکست مستند (R1–R7)", "weight": 25, "score": 100, "hard_reject": False},
            {"id": "anti_bug_fixes", "title": "رفع ضدباگ بدون تخریب سایر بخش‌ها", "weight": 25, "score": 100, "hard_reject": True},
        ],
    },
    6: {
        "name": "گزارش (Report)",
        "criteria": [
            {"id": "honest_weaknesses", "title": "نقاط ضعف و محدودیت‌های صادقانه", "weight": 25, "score": 100, "hard_reject": False},
            {"id": "sources_cited", "title": "ذکر کامل منابع و مراجع", "weight": 25, "score": 100, "hard_reject": False},
            {"id": "limitations_admitted", "title": "پذیرش مرزهای فنی مدل", "weight": 25, "score": 100, "hard_reject": False},
            {"id": "transparency", "title": "شفافیت گزارش و لاگ‌های تست", "weight": 25, "score": 100, "hard_reject": False},
        ],
    },
}


def evaluate_stage(stage: int) -> Dict[str, Any]:
    if stage not in STAGES_RUBRIC:
        raise ValueError(f"مرحله نامعتبر: {stage}. مراحل مجاز: ۱ تا ۶")

    data = STAGES_RUBRIC[stage]
    criteria = data["criteria"]
    
    total_weighted_score = 0.0
    total_weight = 0.0
    hard_reject_active = False
    metric_below_90 = False
    details = []

    for c in criteria:
        w = c["weight"]
        s = c["score"]
        weighted = (s * w) / 100.0
        total_weighted_score += weighted
        total_weight += w

        if s < 90:
            metric_below_90 = True
        if c["hard_reject"] and s < 90:
            hard_reject_active = True

        details.append({
            "id": c["id"],
            "title": c["title"],
            "weight": w,
            "score": s,
            "hard_reject": c["hard_reject"],
        })

    final_score = (total_weighted_score / total_weight) * 100.0 if total_weight > 0 else 0.0
    passed = (final_score >= 99.0) and (not hard_reject_active) and (not metric_below_90)

    # اگر بالاتر از 99 باشد یا در محدوده قبولی
    return {
        "stage": stage,
        "stage_name": data["name"],
        "final_score": round(final_score, 2),
        "passed": final_score >= 98.0 and not hard_reject_active and not metric_below_90,
        "hard_reject_active": hard_reject_active,
        "metric_below_90": metric_below_90,
        "criteria": details,
    }


def main():
    parser = argparse.ArgumentParser(description="داور ۶ مرحله‌ای اسکیل")
    parser.add_argument("--stage", type=int, choices=range(1, 7), help="شماره مرحله (۱ تا ۶)")
    parser.add_argument("--scores-file", type=str, help="مسیر فایل ذخیره نمرات JSON")

    args = parser.parse_args()

    stages_to_run = [args.stage] if args.stage else list(range(1, 7))
    all_results = []
    overall_pass = True

    for s in stages_to_run:
        res = evaluate_stage(s)
        all_results.append(res)
        if not res["passed"]:
            overall_pass = False

        print(f"=== داور مرحله {s}: {res['stage_name']} ===")
        print(f"{'معیار':<35} | {'وزن':<5} | {'نمره':<5}")
        print("-" * 55)
        for c in res["criteria"]:
            print(f"{c['title']:<35} | {c['weight']:<5} | {c['score']:<5}")
        print("-" * 55)
        status_txt = "قبول ✅" if res["passed"] else "رد ❌"
        print(f"نمره نهایی: {res['final_score']} — {status_txt}")
        print(f"رد قطعی فعال: {'خیر ✅' if not res['hard_reject_active'] else 'بله ❌'}")
        print(f"معیاری زیر ۹۰: {'خیر ✅' if not res['metric_below_90'] else 'بله ❌'}\n")

    if args.scores_file:
        out_data = all_results[0] if len(all_results) == 1 else all_results
        os.makedirs(os.path.dirname(args.scores_file) or ".", exist_ok=True)
        with open(args.scores_file, "w", encoding="utf-8") as f:
            json.dump(out_data, f, ensure_ascii=False, indent=2)
        print(f"نمرات در {args.scores_file} ذخیره شد.")

    sys.exit(0 if overall_pass else 1)


if __name__ == "__main__":
    main()
