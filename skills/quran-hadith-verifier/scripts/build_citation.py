#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_citation.py — ساخت ارجاع استاندارد شیعه و قالب‌بندی خروجی
ضدباگ: B6 (نسبت اشتباه)، B7 (ورود منابع اهل‌سنت)، B3 (درجه‌بندی ساختگی)
منطبق با references/citation-rules.md و references/formatting-layer.md
"""

from typing import Optional, Dict, Any

try:
    from .canonical_counts import validate_surah_ayah, get_surah_info
except ImportError:
    from canonical_counts import validate_surah_ayah, get_surah_info


# فهرست منابع مجاز شیعه (فقط شیعه)
AUTHORIZED_SHIA_BOOKS = [
    "الکافی", "کافی", "الكافي",
    "من لا یحضره الفقیه", "من لا يحضره الفقيه", "الفقیه",
    "تهذیب الاحکام", "تهذيب الأحكام", "التهذیب",
    "الاستبصار", "الإستبصار",
    "وسائل الشیعه", "وسائل الشيعة",
    "بحار الانوار", "بحار الأنوار",
    "نهج البلاغه", "نهج البلاغة",
    "صحیفه سجادیه", "الصحيفة السجادية",
    "الامالی", "الأمالي للصدوق", "امالی صدوق", "امالی طوسی", "امالی مفید",
    "عیون اخبار الرضا", "عيون أخبار الرضا",
    "البرهان فی تفسیر القرآن", "البرهان",
    "نور الثقلین", "تفسیر نور الثقلین",
    "المیزان فی تفسیر القرآن", "المیزان",
    "تفسیر نمونه", "نمونه",
    "تفسیر نور", "نور",
    "مجمع البیان", "مجمع البيان",
    "التبیان", "التبیان فی تفسیر القرآن",
    "تفسیر قمی", "تفسیر علی بن ابراهیم قمی",
    "تفسیر عیاشی",
]

# منابع ممنوع اهل‌سنت (فقط شیعه — گیت سخت)
FORBIDDEN_SUNNI_SOURCES = [
    "بخاری", "صحیح بخاری", "صحيح البخاري", "bukhari",
    "مسلم", "صحیح مسلم", "صحيح مسلم", "sahih muslim",
    "ترمذی", "جامع الترمذی", "سنن ترمذی", "tirmidhi",
    "ابوداود", "سنن ابوداود", "ابو داود", "abu dawood",
    "نسائی", "سنن نسائی", "النسائي", "nasai",
    "ابن ماجه", "سنن ابن ماجه", "ibn majah",
    "مسند احمد", "احمد بن حنبل", "musnad ahmad",
    "تفسیر طبری", "جامع البیان", "طبری", "tabari",
    "تفسیر ابن کثیر", "ابن کثیر", "ibn kathir",
    "تفسیر قرطبی", "الجامع لاحکام القرآن", "qurtubi",
    "تفسیر سیوطی", "الدر المنثور", "suyuti",
]

# مراجع معتبر درجه‌بندی سند شیعه
AUTHORIZED_GRADERS = [
    "مجلسی", "علامه مجلسی", "مرآة العقول", "ملاذ الاخیار",
    "وحید بهبهانی", "بهبهانی",
    "نجاشی", "رجال النجاشی",
    "شیخ طوسی", "رجال الطوسی", "الفهرست",
    "کشی", "رجال الکشی",
    "ابن داود", "علامه حلی",
    "خویی", "آیت‌الله خویی", "معجم رجال الحدیث",
    "مامقانی", "تنقیح المقال",
    "شهید ثانی", "شیخ بهایی",
]


class SunniSourceError(ValueError):
    """خطای نقض گیت سخت: منابع اهل‌سنت کاملاً ممنوع است."""
    pass


def check_shia_only(book_or_source: str) -> None:
    """بررسی گیت فقط-شیعه."""
    if not book_or_source:
        return
    lowered = book_or_source.lower()
    for forbidden in FORBIDDEN_SUNNI_SOURCES:
        if forbidden in lowered:
            raise SunniSourceError(
                f"نقض گیت فقط-شیعه: منبع '{book_or_source}' از منابع اهل‌سنت است. "
                "طبق قانون سخت اسکیل، ارجاع یا نقل از منابع اهل‌سنت کاملاً ممنوع است."
            )


def build_quran_citation(
    surah: int,
    ayah_start: int,
    ayah_end: Optional[int] = None,
    translator: Optional[str] = "فولادوند",
) -> str:
    """
    ساخت ارجاع استاندارد قرآن کریم.
    فرمت: 📖 (قرآن ۲:۲۵۵) | ترجمه: فولادوند
    """
    valid, msg = validate_surah_ayah(surah, ayah_start)
    if not valid:
        raise ValueError(msg)

    surah_info = get_surah_info(surah)
    surah_name = surah_info["name_fa"] if surah_info else str(surah)

    if ayah_end and ayah_end > ayah_start:
        valid_end, msg_end = validate_surah_ayah(surah, ayah_end)
        if not valid_end:
            raise ValueError(msg_end)
        ayah_part = f"{surah}:{ayah_start}-{ayah_end}"
    else:
        ayah_part = f"{surah}:{ayah_start}"

    trans_part = f" | ترجمه: {translator}" if translator else ""
    return f"📖 (قرآن {ayah_part}) [{surah_name}]{trans_part}"


def build_hadith_citation(
    book: str,
    author: str,
    volume: Optional[int] = None,
    page: Optional[int] = None,
    hadith_num: Optional[int] = None,
    chapter: Optional[str] = None,
    grader: Optional[str] = None,
    grade: Optional[str] = None,
) -> Dict[str, str]:
    """
    ساخت ارجاع استاندارد حدیث شیعه + درجه‌بندی سند.
    ضدباگ B3 (درجه‌بندی ساختگی) + B6 (نسبت اشتباه) + B7 (فقط شیعه)
    """
    check_shia_only(book)
    check_shia_only(author)

    # ساخت متن ارجاع
    parts = [f"{book}، {author}"]
    if volume is not None:
        parts.append(f"ج {volume}")
    if page is not None:
        parts.append(f"ص {page}")
    if hadith_num is not None:
        parts.append(f"ح {hadith_num}")
    if chapter:
        parts.append(f"باب {chapter}")

    citation_line = f"📚 ارجاع: {'، '.join(parts)}"

    # بررسی و ساخت وضعیت سند
    if grade and grade.strip():
        # بررسی وجود مرجع معتبر
        grader_valid = False
        if grader:
            for auth in AUTHORIZED_GRADERS:
                if auth in grader:
                    grader_valid = True
                    break

        if grader_valid:
            sanad_line = f"🧾 وضعیت سند: {grade} ({grader})"
        else:
            # اگر مرجع ذکر نشده یا نامعتبر است، حدس مجاز نیست
            sanad_line = f"🧾 وضعیت سند: {grade} (مرجع رجالی مشخص نیست — احتیاط رجالی)"
    else:
        sanad_line = "🧾 وضعیت سند: درجه‌بندی یافت نشد (نیاز به بررسی رجالی)"

    return {
        "citation": citation_line,
        "sanad_status": sanad_line,
        "formatted": f"{citation_line}\n{sanad_line}",
    }


def format_smart_multilingual(
    quote_en: str,
    text_ar: str,
    text_fa: str,
    explanation_fa: str,
    source_name: str,
) -> str:
    """
    قالب‌بندی حالت اسمارت سه‌زبانه (references/smart-multilingual.md):
    منبع انگلیسی ← EN ← AR ← FA ← توضیح فارسی
    """
    check_shia_only(source_name)
    blocks = [
        f"🌐 نقل‌قول دقیق انگلیسی ({source_name}):",
        f"> {quote_en.strip()}",
        "",
        "📖 عربی:",
        f"> {text_ar.strip()}",
        "",
        "🔤 فارسی:",
        text_fa.strip(),
        "",
        "📝 توضیح فارسی:",
        explanation_fa.strip(),
    ]
    return "\n".join(blocks)


if __name__ == "__main__":
    # تست سریع
    print(build_quran_citation(2, 255, translator="فولادوند"))
    h = build_hadith_citation(
        book="الکافی",
        author="شیخ کلینی",
        volume=1,
        page=34,
        hadith_num=1,
        chapter="فضل العلم",
        grader="علامه مجلسی (مرآة العقول)",
        grade="صحیح",
    )
    print(h["formatted"])
