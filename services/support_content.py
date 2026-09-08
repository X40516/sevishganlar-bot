"""
🫂 Dardlashamiz bo'limi uchun hissiy qo'llab-quvvatlash kontenti.
Hozircha faqat o'zbek tilida (his-tuyg'u nozikligi tufayli avtomatik
tarjima qilinmagan - alohida so'ralsa qo'shiladi).
"""

CRISIS_KEYWORDS = [
    "o'zimni o'ldirmoqchi", "ozimni oldirmoqchi", "jonimga qasd",
    "yashagim kelmayapti", "o'lsam yaxshi", "olsam yaxshi",
    "o'zimga zarar", "ozimga zarar", "hayotdan charchadim",
    "suicid", "o'zimni jarohatla", "ozimni jarohatla",
    "yashashni xohlamayman", "tugatgim keladi",
]

CRISIS_RESPONSE = (
    "Bu og'ir gaplar va menga ishonib aytganingiz uchun rahmat 🙏\n\n"
    "Iltimos, hozir yolg'iz qolmang — ishonchli katta odam, oila a'zosi yoki "
    "yaqin do'stingizga zudlik bilan murojaat qiling. Shuningdek, psixolog yoki "
    "shifokor kabi mutaxassis yordamiga murojaat qilish juda muhim.\n\n"
    "Sizning hayotingiz qadrli va his qilayotgan og'irlik vaqtinchalik ❤️"
)

CATEGORIES: dict[str, dict] = {
    "sadness": {
        "keywords": ["xafa", "yig'la", "yigla", "og'ir", "achinaman", "ranjidim", "ko'nglim g'ash"],
        "responses": [
            "Buni his qilayotganingiz uchun afsusdaman. Xohlasangiz, nima bo'lganini aytib bering — tinglayman 🤍",
            "Xafagarchilik og'ir yuk. Menga gapirib, biroz yengillashishga harakat qiling.",
            "Sizni tushunaman. Bunday paytlarda his-tuyg'ularingizni ichingizga yutmang.",
        ],
    },
    "loneliness": {
        "keywords": ["yolg'iz", "yolgiz", "hech kim yo'q", "tanho", "hech kim tushunmaydi"],
        "responses": [
            "Yolg'izlik og'ir his. Shu daqiqada men shu yerdaman va sizni tinglayapman.",
            "Hech kim yo'q deb his qilish qiyin. Ammo yonimda gaplashadigan birov bor — men.",
        ],
    },
    "fear": {
        "keywords": ["qo'rqaman", "qorqaman", "qo'rqinch", "qorqinch", "vahima", "xavotirdaman"],
        "responses": [
            "Qo'rquv tabiiy tuyg'u. Nimadan qo'rqayotganingizni aytib bersangiz, birga o'ylab ko'ramiz.",
            "Xavotir olayotganingizni tushunaman. Chuqur nafas oling — men shu yerdaman.",
        ],
    },
    "stress": {
        "keywords": ["stress", "charchadim", "toliqdim", "bosim ostidaman", "holdan toydim"],
        "responses": [
            "Charchagan bo'lsangiz kerak. O'zingizga biroz dam bering, buni his qilish normal.",
            "Bosim ostida bo'lish og'ir. Nima sizni eng ko'p charchatayotganini aytib bering.",
        ],
    },
    "anger": {
        "keywords": ["jahlim chiqdi", "g'azab", "gazab", "achchiqlanaman", "asabim"],
        "responses": [
            "Jahlingiz chiqishi tushunarli. Nima bo'lganini aytib bering, birga tushunishga harakat qilamiz.",
            "G'azablanish — ba'zan adolatsizlikka tabiiy reaksiya. Gapiring, tinglayman.",
        ],
    },
    "breakup": {
        "keywords": ["ayrildik", "ajrashdik", "tashladi", "munosabat tugadi", "sevgilim ketdi"],
        "responses": [
            "Bu juda og'ir tajriba. His-tuyg'ularingiz haqli — o'zingizga vaqt bering.",
            "Ayriliq og'ir. Sizga shu daqiqada eng kerakli narsa — o'zingizga mehribon bo'lish.",
        ],
    },
    "happy": {
        "keywords": ["xursandman", "baxtliman", "zo'r kun", "ajoyib his"],
        "responses": [
            "Buni eshitish meni ham xursand qildi! 😊 Davom eting, aytib bering!",
            "Zo'r! Sizning quvonchingizni his qilyapman ❤️",
        ],
    },
}

ADVICE_BY_CATEGORY: dict[str, list[str]] = {
    "sadness": [
        "Hozircha o'zingizga vaqt bering. Yoqtirgan bir narsa bilan shug'ullaning yoki ishonchli birovga gapirib bering.",
    ],
    "loneliness": [
        "Ishonchli bir do'stingizga yoki oila a'zoingizga qo'ng'iroq qilib ko'rsangiz-chi? Kichik qadam katta farq qilishi mumkin.",
    ],
    "fear": [
        "Qo'rquvni yozib chiqish yoki ishonchli odam bilan bo'lishish yordam berishi mumkin.",
    ],
    "stress": [
        "Biroz dam oling, chuqur nafas oling. Vazifalaringizni kichik qismlarga bo'lib bajaring.",
    ],
    "anger": [
        "Birozdan keyin gaplashish, hozir esa sokinlashish uchun vaqt olish yordam beradi.",
    ],
    "breakup": [
        "O'zingizga mehribon bo'ling. Yaqinlaringiz bilan vaqt o'tkazish yordam beradi.",
    ],
    "happy": [
        "Bu quvonchni yaqinlaringiz bilan ham baham ko'ring!",
    ],
}

ADVICE_TRIGGERS = ["nima qilay", "nima qilishim kerak", "yordam ber", "maslahat ber", "endi nima"]

DEFAULT_RESPONSES = [
    "Tinglayapman, davom eting.",
    "Buni menga aytganingiz uchun rahmat. Ko'proq gapirib bering.",
    "Sizni tushunishga harakat qilyapman. Davom eting.",
    "Hozir qanday his qilayotganingizni yanada batafsil aytib bera olasizmi?",
]


def is_crisis(text: str) -> bool:
    lowered = text.lower()
    return any(keyword in lowered for keyword in CRISIS_KEYWORDS)


def detect_category(text: str) -> str | None:
    lowered = text.lower()
    for category, data in CATEGORIES.items():
        if any(keyword in lowered for keyword in data["keywords"]):
            return category
    return None


def is_advice_request(text: str) -> bool:
    lowered = text.lower()
    return any(trigger in lowered for trigger in ADVICE_TRIGGERS)


def get_support_response(text: str, last_category: str | None) -> tuple[str, str | None]:
    """
    Foydalanuvchi matniga mos javobni qaytaradi.
    Qaytaradi: (javob_matni, yangi_kategoriya)
    """
    import random

    if is_crisis(text):
        return CRISIS_RESPONSE, last_category

    category = detect_category(text)
    if category:
        return random.choice(CATEGORIES[category]["responses"]), category

    if is_advice_request(text) and last_category and last_category in ADVICE_BY_CATEGORY:
        return random.choice(ADVICE_BY_CATEGORY[last_category]), last_category

    return random.choice(DEFAULT_RESPONSES), last_category
