"""
18+ / nomaqbul kontentni aniqlash uchun oddiy kalit-so'z filtri.
Bu bot butunlay 18+ kontentni taqiqlaydi.
"""

ADULT_KEYWORDS = [
    "18+", "porn", "porno", "sex", "seks", "секс", "порно",
    "yalang'och", "yalangoch", "интим", "intim", "nude",
    "xxx", "эротика", "erotika",
]


def is_adult_content(text: str) -> bool:
    if not text:
        return False
    lowered = text.lower()
    return any(keyword in lowered for keyword in ADULT_KEYWORDS)
