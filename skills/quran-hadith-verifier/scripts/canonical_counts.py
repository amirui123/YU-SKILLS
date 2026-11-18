#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
canonical_counts.py — شمارش کانونی آیات قرآن کریم (۱۱۴ سوره / ۶۲۳۶ آیه)
ضدباگ: B2 (شماره آیه اشتباه)
درس‌گرفته از باگ شمارش آیات و شماره‌گذاری کانونی حفص از عاصم.
"""

from typing import Dict, Any, Optional, Tuple

# جدول کانونی ۱۱۴ سوره قرآن (رسم‌الخط عثمان طه / روایت حفص از عاصم)
# (شماره سوره, نام عربی, نام فارسی/آوانویسی, تعداد آیات, محل نزول)
SURAH_DATA: Dict[int, Dict[str, Any]] = {
    1: {"name_ar": "الفاتحة", "name_fa": "حمد", "name_en": "Al-Fatiha", "ayah_count": 7, "type": "Meccan"},
    2: {"name_ar": "البقرة", "name_fa": "بقره", "name_en": "Al-Baqarah", "ayah_count": 286, "type": "Medinan"},
    3: {"name_ar": "آل عمران", "name_fa": "آل عمران", "name_en": "Ali 'Imran", "ayah_count": 200, "type": "Medinan"},
    4: {"name_ar": "النساء", "name_fa": "نساء", "name_en": "An-Nisa", "ayah_count": 176, "type": "Medinan"},
    5: {"name_ar": "المائدة", "name_fa": "مائده", "name_en": "Al-Ma'idah", "ayah_count": 120, "type": "Medinan"},
    6: {"name_ar": "الأنعام", "name_fa": "انعام", "name_en": "Al-An'am", "ayah_count": 165, "type": "Meccan"},
    7: {"name_ar": "الأعراف", "name_fa": "اعراف", "name_en": "Al-A'raf", "ayah_count": 206, "type": "Meccan"},
    8: {"name_ar": "الأنفال", "name_fa": "انفال", "name_en": "Al-Anfal", "ayah_count": 75, "type": "Medinan"},
    9: {"name_ar": "التوبة", "name_fa": "توبه", "name_en": "At-Tawbah", "ayah_count": 129, "type": "Medinan"},
    10: {"name_ar": "يونس", "name_fa": "یونس", "name_en": "Yunus", "ayah_count": 109, "type": "Meccan"},
    11: {"name_ar": "هود", "name_fa": "هود", "name_en": "Hud", "ayah_count": 123, "type": "Meccan"},
    12: {"name_ar": "يوسف", "name_fa": "یوسف", "name_en": "Yusuf", "ayah_count": 111, "type": "Meccan"},
    13: {"name_ar": "الرعد", "name_fa": "رعد", "name_en": "Ar-Ra'd", "ayah_count": 43, "type": "Medinan"},
    14: {"name_ar": "إبراهيم", "name_fa": "ابراهیم", "name_en": "Ibrahim", "ayah_count": 52, "type": "Meccan"},
    15: {"name_ar": "الحجر", "name_fa": "حجر", "name_en": "Al-Hijr", "ayah_count": 99, "type": "Meccan"},
    16: {"name_ar": "النحل", "name_fa": "نحل", "name_en": "An-Nahl", "ayah_count": 128, "type": "Meccan"},
    17: {"name_ar": "الإسراء", "name_fa": "اسراء", "name_en": "Al-Isra", "ayah_count": 111, "type": "Meccan"},
    18: {"name_ar": "الكهف", "name_fa": "کهف", "name_en": "Al-Kahf", "ayah_count": 110, "type": "Meccan"},
    19: {"name_ar": "مريم", "name_fa": "مریم", "name_en": "Maryam", "ayah_count": 98, "type": "Meccan"},
    20: {"name_ar": "طه", "name_fa": "طه", "name_en": "Ta-Ha", "ayah_count": 135, "type": "Meccan"},
    21: {"name_ar": "الأنبياء", "name_fa": "انبیاء", "name_en": "Al-Anbiya", "ayah_count": 112, "type": "Meccan"},
    22: {"name_ar": "الحج", "name_fa": "حج", "name_en": "Al-Hajj", "ayah_count": 78, "type": "Medinan"},
    23: {"name_ar": "المؤمنون", "name_fa": "مؤمنون", "name_en": "Al-Mu'minun", "ayah_count": 118, "type": "Meccan"},
    24: {"name_ar": "النور", "name_fa": "نور", "name_en": "An-Nur", "ayah_count": 64, "type": "Medinan"},
    25: {"name_ar": "الفرقان", "name_fa": "فرقان", "name_en": "Al-Furqan", "ayah_count": 77, "type": "Meccan"},
    26: {"name_ar": "الشعراء", "name_fa": "شعراء", "name_en": "Ash-Shu'ara", "ayah_count": 227, "type": "Meccan"},
    27: {"name_ar": "النمل", "name_fa": "نمل", "name_en": "An-Naml", "ayah_count": 93, "type": "Meccan"},
    28: {"name_ar": "القصص", "name_fa": "قصص", "name_en": "Al-Qasas", "ayah_count": 88, "type": "Meccan"},
    29: {"name_ar": "العنكبوت", "name_fa": "عنکبوت", "name_en": "Al-'Ankabut", "ayah_count": 69, "type": "Meccan"},
    30: {"name_ar": "الروم", "name_fa": "روم", "name_en": "Ar-Rum", "ayah_count": 60, "type": "Meccan"},
    31: {"name_ar": "لقمان", "name_fa": "لقمان", "name_en": "Luqman", "ayah_count": 34, "type": "Meccan"},
    32: {"name_ar": "السجدة", "name_fa": "سجده", "name_en": "As-Sajdah", "ayah_count": 30, "type": "Meccan"},
    33: {"name_ar": "الأحزاب", "name_fa": "احزاب", "name_en": "Al-Ahzab", "ayah_count": 73, "type": "Medinan"},
    34: {"name_ar": "سبأ", "name_fa": "سبأ", "name_en": "Saba", "ayah_count": 54, "type": "Meccan"},
    35: {"name_ar": "فاطر", "name_fa": "فاطر", "name_en": "Fatir", "ayah_count": 45, "type": "Meccan"},
    36: {"name_ar": "يس", "name_fa": "یس", "name_en": "Ya-Sin", "ayah_count": 83, "type": "Meccan"},
    37: {"name_ar": "الصافات", "name_fa": "صافات", "name_en": "As-Saffat", "ayah_count": 182, "type": "Meccan"},
    38: {"name_ar": "ص", "name_fa": "ص", "name_en": "Sad", "ayah_count": 88, "type": "Meccan"},
    39: {"name_ar": "الزمر", "name_fa": "زمر", "name_en": "Az-Zumar", "ayah_count": 75, "type": "Meccan"},
    40: {"name_ar": "غافر", "name_fa": "غافر", "name_en": "Ghafir", "ayah_count": 85, "type": "Meccan"},
    41: {"name_ar": "فصلت", "name_fa": "فصلت", "name_en": "Fussilat", "ayah_count": 54, "type": "Meccan"},
    42: {"name_ar": "الشورى", "name_fa": "شوری", "name_en": "Ash-Shura", "ayah_count": 53, "type": "Meccan"},
    43: {"name_ar": "الزخرف", "name_fa": "زخرف", "name_en": "Az-Zukhruf", "ayah_count": 89, "type": "Meccan"},
    44: {"name_ar": "الدخان", "name_fa": "دخان", "name_en": "Ad-Dukhan", "ayah_count": 59, "type": "Meccan"},
    45: {"name_ar": "الجاثية", "name_fa": "جاثیه", "name_en": "Al-Jathiyah", "ayah_count": 37, "type": "Meccan"},
    46: {"name_ar": "الأحقاف", "name_fa": "احقاف", "name_en": "Al-Ahqaf", "ayah_count": 35, "type": "Meccan"},
    47: {"name_ar": "محمد", "name_fa": "محمد", "name_en": "Muhammad", "ayah_count": 38, "type": "Medinan"},
    48: {"name_ar": "الفتح", "name_fa": "فتح", "name_en": "Al-Fath", "ayah_count": 29, "type": "Medinan"},
    49: {"name_ar": "الحجرات", "name_fa": "حجرات", "name_en": "Al-Hujurat", "ayah_count": 18, "type": "Medinan"},
    50: {"name_ar": "ق", "name_fa": "ق", "name_en": "Qaf", "ayah_count": 45, "type": "Meccan"},
    51: {"name_ar": "الذاريات", "name_fa": "ذاریات", "name_en": "Adh-Dhariyat", "ayah_count": 60, "type": "Meccan"},
    52: {"name_ar": "الطور", "name_fa": "طور", "name_en": "At-Tur", "ayah_count": 49, "type": "Meccan"},
    53: {"name_ar": "النجم", "name_fa": "نجم", "name_en": "An-Najm", "ayah_count": 62, "type": "Meccan"},
    54: {"name_ar": "القمر", "name_fa": "قمر", "name_en": "Al-Qamar", "ayah_count": 55, "type": "Meccan"},
    55: {"name_ar": "الرحمن", "name_fa": "الرحمن", "name_en": "Ar-Rahman", "ayah_count": 78, "type": "Medinan"},
    56: {"name_ar": "الواقعة", "name_fa": "واقعه", "name_en": "Al-Waqi'ah", "ayah_count": 96, "type": "Meccan"},
    57: {"name_ar": "الحديد", "name_fa": "حدید", "name_en": "Al-Hadid", "ayah_count": 29, "type": "Medinan"},
    58: {"name_ar": "المجادلة", "name_fa": "مجادله", "name_en": "Al-Mujadila", "ayah_count": 22, "type": "Medinan"},
    59: {"name_ar": "الحشر", "name_fa": "حشر", "name_en": "Al-Hashr", "ayah_count": 24, "type": "Medinan"},
    60: {"name_ar": "الممتحنة", "name_fa": "ممتحنه", "name_en": "Al-Mumtahanah", "ayah_count": 13, "type": "Medinan"},
    61: {"name_ar": "الصف", "name_fa": "صف", "name_en": "As-Saff", "ayah_count": 14, "type": "Medinan"},
    62: {"name_ar": "الجمعة", "name_fa": "جمعه", "name_en": "Al-Jumu'ah", "ayah_count": 11, "type": "Medinan"},
    63: {"name_ar": "المنافقون", "name_fa": "منافقون", "name_en": "Al-Munafiqun", "ayah_count": 11, "type": "Medinan"},
    64: {"name_ar": "التغابن", "name_fa": "تغابن", "name_en": "At-Taghabun", "ayah_count": 18, "type": "Medinan"},
    65: {"name_ar": "الطلاق", "name_fa": "طلاق", "name_en": "At-Talaq", "ayah_count": 12, "type": "Medinan"},
    66: {"name_ar": "التحريم", "name_fa": "تحریم", "name_en": "At-Tahrim", "ayah_count": 12, "type": "Medinan"},
    67: {"name_ar": "الملك", "name_fa": "ملک", "name_en": "Al-Mulk", "ayah_count": 30, "type": "Meccan"},
    68: {"name_ar": "القلم", "name_fa": "قلم", "name_en": "Al-Qalam", "ayah_count": 52, "type": "Meccan"},
    69: {"name_ar": "الحاقة", "name_fa": "حاقه", "name_en": "Al-Haqqah", "ayah_count": 52, "type": "Meccan"},
    70: {"name_ar": "المعارج", "name_fa": "معارج", "name_en": "Al-Ma'arij", "ayah_count": 44, "type": "Meccan"},
    71: {"name_ar": "نوح", "name_fa": "نوح", "name_en": "Nuh", "ayah_count": 28, "type": "Meccan"},
    72: {"name_ar": "الجن", "name_fa": "جن", "name_en": "Al-Jinn", "ayah_count": 28, "type": "Meccan"},
    73: {"name_ar": "المزمل", "name_fa": "مزمل", "name_en": "Al-Muzzammil", "ayah_count": 20, "type": "Meccan"},
    74: {"name_ar": "المدثر", "name_fa": "مدثر", "name_en": "Al-Muddaththir", "ayah_count": 56, "type": "Meccan"},
    75: {"name_ar": "القيامة", "name_fa": "قیامت", "name_en": "Al-Qiyamah", "ayah_count": 40, "type": "Meccan"},
    76: {"name_ar": "الإنسان", "name_fa": "انسان", "name_en": "Al-Insan", "ayah_count": 31, "type": "Medinan"},
    77: {"name_ar": "المرسلات", "name_fa": "مرسلات", "name_en": "Al-Mursalat", "ayah_count": 50, "type": "Meccan"},
    78: {"name_ar": "النبأ", "name_fa": "نبأ", "name_en": "An-Naba", "ayah_count": 40, "type": "Meccan"},
    79: {"name_ar": "النازعات", "name_fa": "نازعات", "name_en": "An-Nazi'at", "ayah_count": 46, "type": "Meccan"},
    80: {"name_ar": "عبس", "name_fa": "عبس", "name_en": "Abasa", "ayah_count": 42, "type": "Meccan"},
    81: {"name_ar": "التكوير", "name_fa": "تکویر", "name_en": "At-Takwir", "ayah_count": 29, "type": "Meccan"},
    82: {"name_ar": "الانفطار", "name_fa": "انفطار", "name_en": "Al-Infitar", "ayah_count": 19, "type": "Meccan"},
    83: {"name_ar": "المطففين", "name_fa": "مطففین", "name_en": "Al-Mutaffifin", "ayah_count": 36, "type": "Meccan"},
    84: {"name_ar": "الانشقاق", "name_fa": "انشقاق", "name_en": "Al-Inshiqaq", "ayah_count": 25, "type": "Meccan"},
    85: {"name_ar": "البروج", "name_fa": "بروج", "name_en": "Al-Buruj", "ayah_count": 22, "type": "Meccan"},
    86: {"name_ar": "الطارق", "name_fa": "طارق", "name_en": "At-Tariq", "ayah_count": 17, "type": "Meccan"},
    87: {"name_ar": "الأعلى", "name_fa": "اعلی", "name_en": "Al-A'la", "ayah_count": 19, "type": "Meccan"},
    88: {"name_ar": "الغاشية", "name_fa": "غاشیه", "name_en": "Al-Ghashiyah", "ayah_count": 26, "type": "Meccan"},
    89: {"name_ar": "الفجر", "name_fa": "فجر", "name_en": "Al-Fajr", "ayah_count": 30, "type": "Meccan"},
    90: {"name_ar": "البلد", "name_fa": "بلد", "name_en": "Al-Balad", "ayah_count": 20, "type": "Meccan"},
    91: {"name_ar": "الشمس", "name_fa": "شمس", "name_en": "Ash-Shams", "ayah_count": 15, "type": "Meccan"},
    92: {"name_ar": "الليل", "name_fa": "لیل", "name_en": "Al-Layl", "ayah_count": 21, "type": "Meccan"},
    93: {"name_ar": "الضحى", "name_fa": "ضحی", "name_en": "Ad-Duha", "ayah_count": 11, "type": "Meccan"},
    94: {"name_ar": "الشرح", "name_fa": "شرح", "name_en": "Ash-Sharh", "ayah_count": 8, "type": "Meccan"},
    95: {"name_ar": "التين", "name_fa": "تین", "name_en": "At-Tin", "ayah_count": 8, "type": "Meccan"},
    96: {"name_ar": "العلق", "name_fa": "علق", "name_en": "Al-'Alaq", "ayah_count": 19, "type": "Meccan"},
    97: {"name_ar": "القدر", "name_fa": "قدر", "name_en": "Al-Qadr", "ayah_count": 5, "type": "Meccan"},
    98: {"name_ar": "البينة", "name_fa": "بینه", "name_en": "Al-Bayyinah", "ayah_count": 8, "type": "Medinan"},
    99: {"name_ar": "الزلزلة", "name_fa": "زلزال", "name_en": "Az-Zalzalah", "ayah_count": 8, "type": "Medinan"},
    100: {"name_ar": "العاديات", "name_fa": "عادیات", "name_en": "Al-'Adiyat", "ayah_count": 11, "type": "Meccan"},
    101: {"name_ar": "القارعة", "name_fa": "قارعه", "name_en": "Al-Qari'ah", "ayah_count": 11, "type": "Meccan"},
    102: {"name_ar": "التكاثر", "name_fa": "تکاثر", "name_en": "At-Takathur", "ayah_count": 8, "type": "Meccan"},
    103: {"name_ar": "العصر", "name_fa": "عصر", "name_en": "Al-'Asr", "ayah_count": 3, "type": "Meccan"},
    104: {"name_ar": "الهمزة", "name_fa": "همزه", "name_en": "Al-Humazah", "ayah_count": 9, "type": "Meccan"},
    105: {"name_ar": "الفيل", "name_fa": "فیل", "name_en": "Al-Fil", "ayah_count": 5, "type": "Meccan"},
    106: {"name_ar": "قريش", "name_fa": "قریش", "name_en": "Quraysh", "ayah_count": 4, "type": "Meccan"},
    107: {"name_ar": "الماعون", "name_fa": "ماعون", "name_en": "Al-Ma'un", "ayah_count": 7, "type": "Meccan"},
    108: {"name_ar": "الكوثر", "name_fa": "کوثر", "name_en": "Al-Kawthar", "ayah_count": 3, "type": "Meccan"},
    109: {"name_ar": "الكافرون", "name_fa": "کافرون", "name_en": "Al-Kafirun", "ayah_count": 6, "type": "Meccan"},
    110: {"name_ar": "النصر", "name_fa": "نصر", "name_en": "An-Nasr", "ayah_count": 3, "type": "Medinan"},
    111: {"name_ar": "المسد", "name_fa": "مسد", "name_en": "Al-Masad", "ayah_count": 5, "type": "Meccan"},
    112: {"name_ar": "الإخلاص", "name_fa": "توحید", "name_en": "Al-Ikhlas", "ayah_count": 4, "type": "Meccan"},
    113: {"name_ar": "الفلق", "name_fa": "فلق", "name_en": "Al-Falaq", "ayah_count": 5, "type": "Meccan"},
    114: {"name_ar": "الناس", "name_fa": "ناس", "name_en": "An-Nas", "ayah_count": 6, "type": "Meccan"},
}

TOTAL_SURAHS = 114
TOTAL_AYAHS = sum(s["ayah_count"] for s in SURAH_DATA.values())


def get_surah_info(surah: int) -> Optional[Dict[str, Any]]:
    """اطلاعات کامل یک سوره را برمی‌گرداند."""
    return SURAH_DATA.get(surah)


def get_ayah_count(surah: int) -> Optional[int]:
    """تعداد آیات یک سوره را برمی‌گرداند."""
    info = get_surah_info(surah)
    return info["ayah_count"] if info else None


def validate_surah_ayah(surah: int, ayah: int) -> Tuple[bool, str]:
    """
    اعتبارسنجی کانونی شماره سوره و آیه.
    ضدباگ: B2
    """
    if not isinstance(surah, int) or surah < 1 or surah > TOTAL_SURAHS:
        return False, f"شماره سوره نامعتبر است: {surah}. قرآن دارای ۱۱۴ سوره است."

    info = SURAH_DATA[surah]
    max_ayahs = info["ayah_count"]

    if not isinstance(ayah, int) or ayah < 1:
        return False, f"شماره آیه نامعتبر است: {ayah}. شماره آیه باید مثبت باشد."

    if ayah > max_ayahs:
        return False, f"سوره {info['name_ar']} ({info['name_fa']}) فقط {max_ayahs} آیه دارد، اما آیه {ayah} درخواست شده است."

    return True, f"سوره {info['name_ar']} ({surah})، آیه {ayah} معتبر است (از مجموع {max_ayahs} آیه)."


def find_surah_by_name(name: str) -> Optional[Tuple[int, Dict[str, Any]]]:
    """جست‌وجوی سوره با نام عربی، فارسی یا انگلیسی."""
    name_clean = name.strip().replace("سوره", "").strip()
    for num, data in SURAH_DATA.items():
        if (
            name_clean == data["name_ar"]
            or name_clean == data["name_fa"]
            or name_clean.lower() == data["name_en"].lower()
            or name_clean in data["name_ar"]
            or name_clean in data["name_fa"]
        ):
            return num, data
    return None


if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="اعتبارسنجی کانونی شمارش آیات قرآن")
    parser.add_argument("--surah", type=int, help="شماره سوره (۱ تا ۱۱۴)")
    parser.add_argument("--ayah", type=int, help="شماره آیه")
    parser.add_argument("--verify-total", action="store_true", help="بررسی جمع کل آیات")

    args = parser.parse_args()

    if args.verify_total:
        print(f"تعداد سوره‌ها: {TOTAL_SURAHS}")
        print(f"مجموع کل آیات: {TOTAL_AYAHS}")
        assert TOTAL_AYAHS == 6236, f"خطا در مجموع آیات: {TOTAL_AYAHS} != 6236"
        print("تأیید شد: مجموع دقیقاً ۶۲۳۶ آیه است.")
        sys.exit(0)

    if args.surah is not None and args.ayah is not None:
        valid, msg = validate_surah_ayah(args.surah, args.ayah)
        print(f"نتیجه: {'معتبر ✅' if valid else 'نامعتبر ❌'}")
        print(msg)
        sys.exit(0 if valid else 1)

    print(f"کل سوره‌ها: {TOTAL_SURAHS} | مجموع آیات: {TOTAL_AYAHS}")
