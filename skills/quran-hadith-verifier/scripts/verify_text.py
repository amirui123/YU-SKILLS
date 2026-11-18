#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_text.py — تطابق کاراکتری متن نقل‌شده با منبع کانونی
ضدباگ: B1 (هلوسینیشن)، B5 (خرابی متن عربی)، B11 (حدیث جعلی)
اگر تطابق نباشد ← رد + اعلام صریح «تأیید نشد».
"""

import difflib
import sys
import os
from typing import Dict, Any, Optional, List

try:
    from .normalize_arabic import normalize_arabic, strip_tashkeel
except ImportError:
    from normalize_arabic import normalize_arabic, strip_tashkeel


# عبارات کلیدی احادیث جعلی مشهور (تله‌های هلوسینیشن — طبق references/fabricated-hadith.md)
_RAW_FABRICATED_PATTERNS = [
    "احبوا العرب لثلاث",
    "لو لم ابعث لبعث يا عمر",
    "لو لم ابعث لبعثت يا عمر",
    "ابوبكر اساسها وعمر حيطانها",
    "ابو بكر اساسها وعمر حيطانها",
    "ما في الجنة شجرة الا مكتوب",
    "اصحابي كالنجوم",
    "انا خاتم النبيين لا نبي بعدي الا ان يشاء الله",
    "اطلبوا العلم ولو بالصين",
    "علماء امتي كانبياء بني اسرائيل",
    "من عشق فعف فمات فهو شهيد",
]

# پیش‌نرمال‌سازی الگوها برای تطابق ۱۰۰٪ دقیق
KNOWN_FABRICATED_PATTERNS: List[str] = [
    normalize_arabic(p) for p in _RAW_FABRICATED_PATTERNS
]


def check_known_fabrication(text: str) -> Optional[str]:
    """بررسی سریع در فهرست احادیث جعلی مشهور."""
    norm = normalize_arabic(text)
    for pat in KNOWN_FABRICATED_PATTERNS:
        if pat in norm:
            return f"هشدار: متن حاوی عبارت جعلی مشهور است: '{pat}' (طبق فهرست احادیث موضوعه و جعلی)."
    return None


def verify_text(
    quoted_text: str,
    source_text: str,
    strict_diacritics: bool = False,
    min_similarity: float = 0.98,
) -> Dict[str, Any]:
    """
    تطابق کاراکتری متن نقل‌شده با متن بازیابی‌شده از منبع.
    
    خروجی:
    - verified: آیا متن تأیید است؟
    - status: 'VERIFIED' | 'TAMPERED_OR_CORRUPTED' | 'NOT_FOUND' | 'FABRICATED_DETECTED'
    - similarity: نسبت شباهت (۰ تا ۱)
    - diff: تفاوت متنی
    - message: پیام واضح به فارسی
    """
    if not quoted_text or not quoted_text.strip():
        return {
            "verified": False,
            "status": "NOT_FOUND",
            "similarity": 0.0,
            "diff": "",
            "message": "متن نقل‌شده خالی است.",
        }

    if not source_text or not source_text.strip():
        return {
            "verified": False,
            "status": "NOT_FOUND",
            "similarity": 0.0,
            "diff": "",
            "message": "متن منبع خالی یا بازیابی‌نشده است. (نقض گیت: بازیابی قبل از نقل)",
        }

    # بررسی تله جعلی
    fab_warn = check_known_fabrication(quoted_text)
    if fab_warn:
        return {
            "verified": False,
            "status": "FABRICATED_DETECTED",
            "similarity": 0.0,
            "diff": "",
            "message": f"تأیید نشد ❌ — {fab_warn}",
        }

    # تطابق دقیق کاراکتری
    q_clean = quoted_text.strip()
    s_clean = source_text.strip()

    if q_clean == s_clean:
        return {
            "verified": True,
            "status": "VERIFIED",
            "match_type": "EXACT",
            "similarity": 1.0,
            "diff": "",
            "message": "تطابق کامل کاراکتری با منبع تأیید شد ✅",
        }

    # تطابق پس از نرمال‌سازی عربی
    q_norm = normalize_arabic(q_clean)
    s_norm = normalize_arabic(s_clean)

    if q_norm == s_norm:
        if strict_diacritics:
            return {
                "verified": False,
                "status": "TAMPERED_OR_CORRUPTED",
                "match_type": "DIACRITICS_MISMATCH",
                "similarity": 0.98,
                "diff": "اختلاف در اعراب/حرکات با منبع رسمی عثمانی.",
                "message": "متن حروفی یکسان است ولی اعراب با منبع منطبق نیست.",
            }
        return {
            "verified": True,
            "status": "VERIFIED",
            "match_type": "NORMALIZED_EXACT",
            "similarity": 1.0,
            "diff": "",
            "message": "متن پس از نرمال‌سازی با منبع کانونی کاملاً منطبق است ✅",
        }

    # بررسی کلمه به کلمه (Token-level matching)
    q_words = q_norm.split()
    s_words = s_norm.split()

    if q_words != s_words:
        diff_words = [w for w in q_words if w not in s_words]
        missing_words = [w for w in s_words if w not in q_words]
        
        matcher = difflib.SequenceMatcher(None, q_norm, s_norm)
        similarity = matcher.ratio()

        diff_lines = list(
            difflib.unified_diff(
                q_norm.splitlines(keepends=True),
                s_norm.splitlines(keepends=True),
                fromfile="نقل_شده",
                tofile="منبع_اصلی",
            )
        )
        diff_str = "".join(diff_lines)

        if diff_words or missing_words:
            return {
                "verified": False,
                "status": "TAMPERED_OR_CORRUPTED",
                "match_type": "WORD_SUBSTITUTION_OR_OMISSION",
                "similarity": round(similarity, 4),
                "diff_words": diff_words,
                "missing_words": missing_words,
                "diff": diff_str,
                "message": f"تأیید نشد ❌ — عدم تطابق کلمات با متن معتبر (کلمات مغایر: {', '.join(diff_words[:3]) if diff_words else 'کلمات حذف‌شده'}).",
            }

    # محاسبه شباهت عمومی
    matcher = difflib.SequenceMatcher(None, q_norm, s_norm)
    similarity = matcher.ratio()

    diff_lines = list(
        difflib.unified_diff(
            q_norm.splitlines(keepends=True),
            s_norm.splitlines(keepends=True),
            fromfile="نقل_شده",
            tofile="منبع_اصلی",
        )
    )
    diff_str = "".join(diff_lines)

    if similarity >= min_similarity:
        return {
            "verified": True,
            "status": "VERIFIED",
            "match_type": "HIGH_SIMILARITY",
            "similarity": round(similarity, 4),
            "diff": diff_str,
            "message": f"متن با ضریب اطمینان {similarity:.2%} با منبع همخوانی دارد ✅ (تفاوت جزئی در نگارش).",
        }
    else:
        return {
            "verified": False,
            "status": "TAMPERED_OR_CORRUPTED" if similarity >= 0.3 else "NOT_FOUND",
            "match_type": "MISMATCH",
            "similarity": round(similarity, 4),
            "diff": diff_str,
            "message": f"تأیید نشد ❌ — مغایرت با منبع کانونی (میزان شباهت: {similarity:.2%}).",
        }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="تطابق کاراکتری متن با منبع")
    parser.add_argument("--quoted", type=str, required=True, help="متن نقل‌شده")
    parser.add_argument("--source", type=str, required=True, help="متن بازیابی‌شده از منبع")
    parser.add_argument("--strict", action="store_true", help="سخت‌گیری در اعراب")

    args = parser.parse_args()

    result = verify_text(args.quoted, args.source, strict_diacritics=args.strict)
    print(f"وضعیت: {result['status']}")
    print(f"تأیید: {result['verified']}")
    print(f"پیام: {result['message']}")
    if result.get("diff"):
        print(f"تفاوت:\n{result['diff']}")

    sys.exit(0 if result["verified"] else 1)
