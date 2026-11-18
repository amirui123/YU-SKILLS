#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
normalize_arabic.py — نرمال‌سازی متن عربی و قرآن/حدیث
ضدباگ: B5 (خرابی متن عربی در جست‌وجو و تطبیق)
بدون نیاز به کتابخانه‌های سنگین خارجی؛ سازگار با پایتون استاندارد.
"""

import re
import unicodedata
from typing import Optional

# علائم اعراب و حرکات عربی (Tashkeel)
TASHKEEL_REGEX = re.compile(
    r"[\u0617-\u061A"  # علائم قرآنی کوچک
    r"\u064B-\u0652"  # فتحتان، ضمتان، کسرَتان، فتحه، ضمه، کسره، شدّه، سکون
    r"\u0653-\u0656"  # مدّه، همزه بالا، همزه پایین، علامت زیر
    r"\u0657-\u065E"  # علائم صوت
    r"\u0670"         # الف خنجری (ألف مقصورة خنجرية)
    r"\u06D6-\u06DC"  # علائم وقف و قراءت قرآن
    r"\u06DF-\u06E8"  # علائم قرآنی تکمیلی
    r"\u06EA-\u06ED"  # علائم تکمیلی
    r"\u08E3-\u08FF]" # علائم یونیکد قرآنی افزوده
)

# تطویل / کشیده (ـ)
TATWEEL_REGEX = re.compile(r"\u0640")

# فاصله‌های مجازی و نامرئی
ZERO_WIDTH_REGEX = re.compile(r"[\u200B-\u200F\u202A-\u202E\uFEFF]")


def strip_tashkeel(text: str) -> str:
    """حذف تمام اعراب، حرکات و علائم قراءت قرآن."""
    if not text:
        return ""
    # نرمال‌سازی یونیکد
    decomposed = unicodedata.normalize("NFKD", text)
    cleaned = TASHKEEL_REGEX.sub("", decomposed)
    return unicodedata.normalize("NFC", cleaned)


def normalize_alif(text: str) -> str:
    """یکسان‌سازی تمام اشکال الف (أ، إ، آ، ٱ ← ا)."""
    text = re.sub(r"[أإآٱ]", "ا", text)
    return text


def normalize_ya(text: str) -> str:
    """یکسان‌سازی اشکال یاء و الف مقصوره (ى، ي، ی ← ي)."""
    text = re.sub(r"[ىيی]", "ي", text)
    return text


def normalize_ta_marbuta(text: str) -> str:
    """یکسان‌سازی تاء مربوطه و هاء (ة ← ه)."""
    text = re.sub(r"ة", "ه", text)
    return text


def normalize_kaf(text: str) -> str:
    """یکسان‌سازی ک/ك."""
    text = re.sub(r"[کك]", "ك", text)
    return text


def normalize_whitespace(text: str) -> str:
    """حذف فاصله‌های مجازی و یکسان‌سازی فاصله‌ها."""
    text = ZERO_WIDTH_REGEX.sub("", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def normalize_arabic(
    text: str,
    remove_diacritics: bool = True,
    unify_alif: bool = True,
    unify_ya: bool = True,
    unify_ta: bool = True,
    remove_kashida: bool = True,
    unify_kaf: bool = True,
) -> str:
    """
    نرمال‌سازی همه‌جانبه متن عربی برای مقایسه و جست‌وجوی دقیق.
    ضدباگ B5
    """
    if not text:
        return ""

    res = text
    if remove_kashida:
        res = TATWEEL_REGEX.sub("", res)
    if remove_diacritics:
        res = strip_tashkeel(res)
    if unify_alif:
        res = normalize_alif(res)
    if unify_ya:
        res = normalize_ya(res)
    if unify_ta:
        res = normalize_ta_marbuta(res)
    if unify_kaf:
        res = normalize_kaf(res)

    res = normalize_whitespace(res)
    return res


def are_arabic_texts_equivalent(text1: str, text2: str) -> bool:
    """
    آیا دو متن عربی پس از نرمال‌سازی یکسان هستند؟
    برای اعتبارسنجی نقل‌ها در برابر منبع بدون گیر دادن به اختلاف حرکات.
    """
    n1 = normalize_arabic(text1)
    n2 = normalize_arabic(text2)
    return n1 == n2


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="نرمال‌سازی متون عربی و قرآنی")
    parser.add_argument("--text", type=str, help="متن عربی ورودی")
    parser.add_argument("--compare", type=str, nargs=2, help="مقایسه دو متن عربی")

    args = parser.parse_args()

    if args.compare:
        t1, t2 = args.compare
        eq = are_arabic_texts_equivalent(t1, t2)
        print(f"متن ۱: {t1}")
        print(f"متن ۲: {t2}")
        print(f"نرمال ۱: {normalize_arabic(t1)}")
        print(f"نرمال ۲: {normalize_arabic(t2)}")
        print(f"نتیجه برابری: {'یکسان ✅' if eq else 'متفاوت ❌'}")
        sys.exit(0 if eq else 1)

    if args.text:
        print("متن اصلی:")
        print(args.text)
        print("متن نرمال‌شده:")
        print(normalize_arabic(args.text))
        sys.exit(0)

    # تست خودکار نمونه
    sample = "اللهُ لاَ إِلَٰهَ إِلاَّ هُوَ الْحَيُّ الْقَيُّومُ ۚ"
    norm = normalize_arabic(sample)
    print(f"نمونه: {sample}")
    print(f"نرمال: {norm}")
    assert norm == "الله لا اله الا هو الحي القيوم"
    print("تست نرمال‌سازی با موفقیت انجام شد ✅")
