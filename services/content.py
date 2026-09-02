"""
Bot uchun statik kontent to'plamlari: xabarlar, savollar, o'yin savollari, sovg'alar.
"""

LOVE_MESSAGES = [
    "Sen mening kunimni yorug' qilasan ☀️💕",
    "Seni o'ylab kulib qo'ydim 😊❤️",
    "Sen bilan bo'lgan har bir lahza qadrli 💖",
    "Seni sog'indim 🥰",
    "Sen mening baxtimsan 💗",
    "Qalbimda faqat sen bor 💘",
    "Sensiz kun kunga o'xshamaydi 🌙💕",
    "Sen mening eng chiroyli tasodifimsan ✨❤️",
]

DAILY_ROMANTIC_MESSAGES = [
    "❤️ Bugun juftingizga uni qadrlashingizni aytishni unutmang.",
    "💌 Kichik bir e'tibor katta baxt keltiradi — bugun buni sinab ko'ring.",
    "🌹 Sevgi kichik ishlarda yashiringan — bugun bir marta kutilmagan iltifot ayting.",
    "☕ Ertalabki bitta xabar kunni yaxshi boshlashga yordam beradi.",
    "💞 Sevgi — tinglash va tushunishdan boshlanadi. Bugun buni his qildiring.",
    "😊 Juftingizga oddiy 'rahmat' ayting — bu ko'p narsani anglatadi.",
    "🌙 Kun oxirida juftingizga qanday o'tganini so'rang.",
]

DAILY_QUESTIONS = [
    "Agar juftingiz bilan istalgan joyga sayohat qila olsangiz, qayerga borardingiz?",
    "Juftingizda eng ko'p yoqtirgan xususiyatingiz nima?",
    "Birinchi marta uchrashganingizda nima his qilgan edingiz?",
    "Sizningcha, baxtli munosabatning siri nimada?",
    "Juftingiz bilan birga o'tkazgan eng yodda qolgan kuningiz qaysi?",
    "Agar bir kunlik ta'til olsangiz, uni juftingiz bilan qanday o'tkazardingiz?",
    "Juftingizni qanday so'z bilan ta'riflagan bo'lardingiz?",
    "Sizni eng ko'p kim kuldirdi bugun?",
    "Kelajakda birga qilishni orzu qilgan bitta narsangiz nima?",
    "Juftingiz sizga qanday yordam berdi eng qiyin damda?",
    "Sevimli qo'shiq yoki film qaysi ikkalangiz uchun ham maxsus?",
    "Agar hozir birga bo'lsangiz, nima qilardingiz?",
    "Juftingizga hali aytmagan bir narsangiz bormi?",
    "Sizni eng ko'p xursand qiladigan kichik ish nima?",
    "Munosabatingizda eng ko'p minnatdor bo'lgan narsangiz nima?",
]

PARTNER_QUESTIONS = [
    "Juftingizning eng sevimli taomi nima?",
    "Juftingiz qaysi rangni yaxshi ko'radi?",
    "Juftingizning bolalikdagi orzusi nima edi?",
    "Juftingiz eng ko'p qo'rqadigan narsa nima?",
    "Juftingizning sevimli mavsumi qaysi?",
    "Juftingiz stress bosganda nima qiladi?",
    "Juftingizning sevimli filmi yoki seriali qaysi?",
    "Juftingiz uchun eng katta baxt nima?",
]

WHO_MORE_STATEMENTS = [
    "Kim ko'proq kech qoladi?",
    "Kim ko'proq oshxonada vaqt o'tkazadi?",
    "Kim tezroq g'azablanadi?",
    "Kim ko'proq sovg'a beradi?",
    "Kim ko'proq romantik?",
    "Kim ko'proq gapiradi?",
    "Kim ko'proq uxlashni yaxshi ko'radi?",
    "Kim ko'proq sayohat qilishni xohlaydi?",
]

TRUTH_PROMPTS = [
    "Juftingizda birinchi marta nimaga e'tibor bergansiz?",
    "Hayotingizda eng katta orzuingiz nima?",
    "Juftingiz haqida hech kimga aytmagan narsangiz bormi?",
    "Munosabatingizda o'zgartirmoqchi bo'lgan bitta narsa bormi?",
    "Eng ko'p sog'ingan lahzangiz qaysi?",
]

DARE_PROMPTS = [
    "Juftingizga hozir bitta kompliment ayting.",
    "Juftingizga eng sevimli xotirangizni tasvirlab bering.",
    "Juftingizga nega uni sevishingizni ayting.",
    "Juftingizga kelajak haqida bitta orzuingizni ayting.",
    "Juftingizga hozir bitta qo'shiq nomini yuboring, u sizni eslatadi.",
]

COMPAT_QUESTIONS = [
    ("Kechqurunni qanday o'tkazishni yoqtirasiz?", ["Uyda tinch o'tirish", "Do'stlar bilan tashqarida", "Sayr qilish"]),
    ("Sayohatda sizga qaysi biri muhimroq?", ["Reja tuzish", "Erkin, spontan yurish", "Aralash"]),
    ("Nizoni qanday hal qilasiz?", ["Darhol gaplashaman", "Biroz o'ylab olaman", "Vaqt o'tkazib gaplashaman"]),
    ("Sevgi tilingiz qaysiga yaqinroq?", ["So'zlar", "Vaqt sarflash", "Sovg'alar"]),
    ("Dam olish kunlarida nima qilishni yoqtirasiz?", ["Uyda dam olish", "Faol dam olish", "Ijtimoiy tadbirlar"]),
]

QUIZ_QUESTIONS = [
    ("Sevgida eng muhimi nima?", [("Ishonch", True), ("Sovg'alar", False), ("Moda", False)]),
    ("Janjal chiqsa, birinchi qadam nima bo'lishi kerak?", [("Jim qolish", False), ("Ochiq gaplashish", True), ("Ijtimoiy tarmoqqa yozish", False)]),
    ("Sevgi tili nechta turga bo'linadi?", [("3", False), ("5", True), ("7", False)]),
    ("Uzoq munosabatlarda eng muhimi nima?", [("Muntazam muloqot", True), ("Qimmat sovg'alar", False), ("Ko'rsatish", False)]),
    ("Sevgilini qanday xursand qilish samarali?", [("Tinglash va tushunish", True), ("Faqat pul sarflash", False), ("E'tiborsiz qoldirish", False)]),
]

GIFTS = [
    ("Yurak", "❤️"),
    ("Atirgul", "🌹"),
    ("Ayiqcha", "🧸"),
    ("Sevgi xati", "💌"),
    ("Yulduz", "⭐"),
    ("Tort", "🎂"),
]
