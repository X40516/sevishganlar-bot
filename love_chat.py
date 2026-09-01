"""
Sevgi mavzusidagi erkin suhbat uchun kalit so'zga asoslangan javoblar.
Faqat 18+ tasdiqlangan foydalanuvchilar uchun ishlatiladi (bot.py da tekshiriladi).
"""

import random

RULES: list[tuple[list[str], list[str]]] = [
    (
        ["salom", "assalomu", "hi", "hello"],
        [
            "Salom, sevgilim haqida gaplashamizmi? 💕",
            "Salom! Yuragingizda nima bor, ayting-chi 😊",
        ],
    ),
    (
        ["sevaman", "yaxshi ko'raman", "sevgim"],
        [
            "Bu juda chiroyli tuyg'u 💖 Buni partneringizga aytdingizmi?",
            "Sevgi eng qimmatli narsa ❤️ Davom eting, tinglayapman.",
        ],
    ),
    (
        ["sog'indim", "sogindim", "sog'inch"],
        [
            "Sog'inch — sevgining bir belgisi 🥹 Unga shuni yozib yuboring.",
            "Sog'inganingizni unga aytdingizmi? Bu uni juda xursand qiladi 💌",
        ],
    ),
    (
        ["janjal", "gina", "ranjidim", "xafa"],
        [
            "Janjallar har bir munosabatda bo'ladi 💭 Muhimi — ochiq gaplashish.",
            "Xafagarchilikni ichingizga yutmang, tinch holda gaplashib oling 🤍",
        ],
    ),
    (
        ["turmush", "oila", "uylanish", "turmushga"],
        [
            "Oila qurish katta qadam 🏡 Ikkalangiz ham tayyor bo'lishi muhim.",
            "Bu haqida partneringiz bilan ochiq gaplashib ko'rdingizmi?",
        ],
    ),
    (
        ["rashk", "hasad"],
        [
            "Biroz rashk normal, lekin ishonch munosabatning asosi 🤝",
            "Rashkni his qilsangiz, buni yashirmasdan gaplashib oling.",
        ],
    ),
    (
        ["ajrashish", "ajraldik", "ajralish"],
        [
            "Bu og'ir mavzu 💔 O'zingizga vaqt bering va yaqinlaringiz bilan gaplashing.",
        ],
    ),
    (
        ["kompliment", "maqtov"],
        [
            "Kompliment kerakmi? Menyudagi '😊 Kompliment' tugmasini bosing! 😉",
        ],
    ),
    (
        ["rahmat", "tashakkur"],
        [
            "Arzimaydi! Sevgi haqida yana gaplashishni xohlasangiz, shu yerdaman 💕",
        ],
    ),
]

DEFAULT_RESPONSES: list[str] = [
    "Qiziq, sevgi haqida ko'proq gapirib bering 💭",
    "Bu haqida qanday his qilyapsiz?",
    "Sevgi murakkab, lekin chiroyli narsa ❤️ Davom eting.",
    "Tinglayapman, davom eting 😊",
    "Munosabatingiz haqida ko'proq aytib bering.",
]


def get_response(text: str) -> str:
    lowered = text.lower()
    for keywords, responses in RULES:
        if any(keyword in lowered for keyword in keywords):
            return random.choice(responses)
    return random.choice(DEFAULT_RESPONSES)
