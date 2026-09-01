"""
Sevgi mavzusidagi qiziqarli viktorina (quiz) o'yini.
Har bir savol uchun 3 variant, to'g'ri javob belgilangan.
"""

QUESTIONS = [
    {
        "question": "Sevgida eng muhimi nima deb o'ylaysiz?",
        "options": [
            ("Ishonch", True),
            ("Sovg'alar", False),
            ("Moda", False),
        ],
    },
    {
        "question": "Munosabatlarda janjal chiqsa, birinchi qadam nima bo'lishi kerak?",
        "options": [
            ("Jim qolish", False),
            ("Ochiq gaplashish", True),
            ("Ijtimoiy tarmoqqa yozish", False),
        ],
    },
    {
        "question": "Sizningcha, sevgi tili (love language) nechta turga bo'linadi?",
        "options": [
            ("3", False),
            ("5", True),
            ("7", False),
        ],
    },
    {
        "question": "Uzoq munosabatlarda (masofaviy) eng muhim narsa nima?",
        "options": [
            ("Muntazam muloqot", True),
            ("Qimmat sovg'alar", False),
            ("Ijtimoiy tarmoqda ko'rsatish", False),
        ],
    },
    {
        "question": "Sevgilingizni qanday xursand qilish eng samarali?",
        "options": [
            ("Uni tinglash va tushunish", True),
            ("Faqat pul sarflash", False),
            ("Uni e'tiborsiz qoldirish", False),
        ],
    },
]

TITLES = [
    (5, "💘 Sevgi ustasi! Siz munosabatlarni juda yaxshi tushunasiz."),
    (3, "😊 Yaxshi natija! Siz sevgi haqida ko'p narsani bilasiz."),
    (0, "🙂 Yomon emas! Yana ko'proq o'rganishga arziydi."),
]


def get_title(score: int) -> str:
    for threshold, title in TITLES:
        if score >= threshold:
            return title
    return TITLES[-1][1]
