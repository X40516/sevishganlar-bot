"""
Ko'p tillilik uchun tarjimalar: uz, ru, en, kk.
"""

LANGUAGES = {
    "uz": "🇺🇿 O'zbekcha",
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 English",
    "kk": "🇰🇿 Қазақша",
}

TEXTS: dict[str, dict[str, str]] = {
    "uz": {
        "menu_support": "🫂 Dardlashamiz",
        "support_intro": "🫂 Men seni tinglashga tayyorman. Ichingda nima bo'lsa, bemalol aytishing mumkin. Seni hukm qilmayman. Gapirib olishing mumkin ❤️",
        "adult_content_warning": "🚫 Bu bot bunday kontentni qo'llab-quvvatlamaydi. Iltimos, hurmatli munosabatda bo'ling.",
        "menu_pair": "💑 Juftimni ulash",
        "menu_couple": "❤️ Juftim",
        "menu_letter": "💌 Xat yuborish",
        "menu_games": "🎲 Juftlik o'yinlari",
        "menu_question": "💭 Bugungi savol",
        "menu_gift": "🎁 Virtual sovg'alar",
        "menu_memories": "📸 Xotiralar",
        "menu_days": "❤️ Birga bo'lgan kunlar",
        "menu_notif": "🔔 Bildirishnomalar",
        "menu_settings": "⚙️ Sozlamalar",
        "menu_help": "ℹ️ Yordam",
        "home_button": "🏠 Bosh menyu",
        "back_button": "⬅️ Orqaga",
        "home_menu": "🏠 Asosiy menyu:",
        "welcome": (
            "❤️ Xush kelibsiz, @JuftimBotbot ga!\n\n"
            "Bu bot orqali juftingiz bilan:\n"
            "💌 xatlar yuborishingiz\n"
            "🎲 o'yinlar o'ynashingiz\n"
            "💭 savollarga javob berishingiz\n"
            "🎁 virtual sovg'alar yuborishingiz\n"
            "📸 xotiralar saqlashingiz mumkin.\n\n"
            "Boshlash uchun '💑 Juftimni ulash' tugmasini bosing."
        ),
        "already_paired": "❤️ Siz allaqachon juftlikka ulangansiz.",
        "invite_invalid": "❌ Bu taklif havolasi yaroqsiz yoki muddati o'tgan.",
        "invite_self": "❌ O'zingizni o'zingiz taklif qila olmaysiz.",
        "invite_ask": "❤️ Sizni {name} juftlikka qo'shilishga taklif qildi. Qabul qilasizmi?",
        "invite_accept": "❤️ Qabul qilish",
        "invite_reject": "❌ Rad etish",
        "invite_rejected": "❌ Taklif rad etildi.",
        "pair_success": "🎉 Tabriklaymiz!\n❤️ Juftlik muvaffaqiyatli ulandi!",
        "help_text": (
            "ℹ️ @JuftimBotbot qanday ishlaydi:\n\n"
            "1️⃣ '💑 Juftimni ulash' tugmasini bosing va taklif havolasini oling.\n"
            "2️⃣ Havolani sevgilingizga yuboring.\n"
            "3️⃣ U havolani ochib, taklifni qabul qilsin.\n"
            "4️⃣ Endi ikkalangiz xatlar, o'yinlar, sovg'alar va xotiralar orqali muloqot qila olasiz!\n\n"
            "Buyruqlar:\n"
            "/start — botni qayta boshlash\n"
            "/admin — admin panel (faqat administratorlar uchun)"
        ),
        "no_couple": "❌ Avval juftingiz bilan ulanishingiz kerak.",
        "couple_invite_prompt": "💑 Juftingizni @JuftimBotbot ga taklif qiling.",
        "couple_link_btn": "🔗 Taklif havolasi",
        "couple_code_btn": "📋 Kodim",
        "couple_link_sent": "🔗 Taklif havolangiz:\n{link}\n\nBu havolani sevgilingizga yuboring.",
        "couple_code_sent": "📋 Kodingiz: {code}\n\nJuftingiz botga shu buyruqni yuborsin:\n/start {code}",
        "couple_info": "❤️ Sizning juftingiz:\n👤 {name}\n{sana}",
        "couple_date_set": "📅 Birga bo'lgan sana: {date}\n❤️ Birga bo'lgan kunlar: {days} kun",
        "couple_date_unset": "📅 Birga bo'lgan sana: belgilanmagan",
        "couple_set_date_btn": "📅 Sanani belgilash",
        "couple_send_letter_btn": "💌 Xat yuborish",
        "couple_memories_btn": "📸 Xotiralar",
        "couple_unpair_btn": "💔 Juftlikni ajratish",
        "couple_unpair_confirm": "⚠️ Haqiqatan ham juftlikni ajratmoqchimisiz?",
        "couple_unpair_yes": "💔 Ha, ajratish",
        "couple_unpair_no": "❌ Yo'q",
        "couple_unpaired": "💔 Juftlik ajratildi.",
        "couple_partner_unpaired": "💔 Juftingiz aloqani uzdi. Yangi juftlik uchun taklif havolasi yaratishingiz mumkin.",
        "letters_prompt": "💌 Juftingizga nima yubormoqchisiz?",
        "letters_text_btn": "📝 Matnli xat",
        "letters_photo_btn": "📸 Rasm + xabar",
        "letters_love_btn": "❤️ Sevgi xabari",
        "letters_send_btn": "📤 Yuborish",
        "letters_edit_btn": "✏️ O'zgartirish",
        "letters_cancel_btn": "❌ Bekor qilish",
        "letters_write_text": "✍️ Matningizni yozing:",
        "letters_send_photo": "📸 Rasm yuboring (izoh bilan birga yuborishingiz mumkin):",
        "letters_preview": "💌 Xatingiz:\n\n{text}\n\nJuftingizga yuborilsinmi?",
        "letters_cancelled": "❌ Bekor qilindi.",
        "letters_sent": "✅ Xat yuborildi!",
        "letters_received": "💌 Sizga juftingizdan yangi xat keldi!",
        "letters_reply_btn": "❤️ Javob berish",
        "games_prompt": "🎲 O'yinlardan birini tanlang:",
        "game_know_btn": "❤️ Bir-biringizni qanchalik bilasiz?",
        "game_who_btn": "😂 Kim ko'proq?",
        "game_truth_dare_btn": "💭 Haqiqat yoki tanlov",
        "game_compat_btn": "🔥 Moslik testi",
        "game_quiz_btn": "🧠 Juftlik viktorinasi",
        "question_prompt": "💭 Bugungi savol:\n{question}",
        "question_answer_btn": "📝 Javob berish",
        "question_view_btn": "👀 Juftimning javobini ko'rish",
        "question_another_btn": "🔄 Boshqa savol",
        "question_write_answer": "✍️ Javobingizni yozing:",
        "question_saved_waiting": "✅ Javobingiz saqlandi! Juftingiz javob berishini kutmoqdamiz. 💭",
        "gifts_prompt": "🎁 Sovg'a tanlang:",
        "gift_sent": "✅ Sovg'a yuborildi!",
        "gift_received": "🎁 Sizga juftingizdan sovg'a keldi!\n\n{emoji} {name}",
        "memories_prompt": "📸 Xotiralar bo'limi:",
        "memories_add_btn": "➕ Xotira qo'shish",
        "memories_view_btn": "📖 Xotiralarni ko'rish",
        "memories_delete_btn": "🗑 Xotirani o'chirish",
        "memory_send_photo": "📸 Rasm yuboring:",
        "memory_send_caption": "✏️ Izoh yozing (yoki '-' yuborib o'tkazib yuboring):",
        "memory_saved": "✅ Xotira saqlandi!",
        "days_unset": "❤️ Birga bo'lgan sanangizni belgilang.",
        "days_set_btn": "📅 Sanani belgilash",
        "days_change_btn": "📅 Sanani o'zgartirish",
        "days_together": "❤️ Sizlar birga bo'lganingizga:\n{total} kun\n{breakdown}",
        "days_ask": "📅 Sanani kiriting (KK.OO.YYYY formatida, masalan: 01.05.2023):",
        "days_saved": "✅ Sana saqlandi: {date}",
        "settings_prompt": "⚙️ Sozlamalar:",
        "settings_notif_btn": "🔔 Bildirishnomalar",
        "settings_lang_btn": "🌐 Til",
        "settings_profile_btn": "👤 Profil",
        "settings_couple_btn": "❤️ Juftlik sozlamalari",
        "settings_about_btn": "ℹ️ Bot haqida",
        "notif_prompt": "🔔 Bildirishnomalar (yoqish/o'chirish uchun bosing):",
        "notif_daily_question": "💭 Bugungi savol",
        "notif_daily_message": "❤️ Kunlik romantik xabar",
        "notif_new_letter": "💌 Yangi xat",
        "notif_gift": "🎁 Sovg'a",
        "notif_special_date": "📅 Maxsus sana",
        "lang_prompt": "🌐 Tilni tanlang:",
        "lang_changed": "✅ Til o'zgartirildi.",
        "profile_text": "👤 Ism: {name}\n🆔 Username: {username}\n❤️ Juftlik holati: {status}\n📅 Juftlik sanasi: {date}",
        "profile_paired": "❤️ Ulangan",
        "profile_not_paired": "❌ Ulanmagan",
        "profile_no_date": "belgilanmagan",
        "about_text": (
            "ℹ️ @JuftimBotbot — sevishgan juftliklar uchun maxsus bot.\n\n"
            "Xatlar, o'yinlar, kunlik savollar, sovg'alar va xotiralar orqali "
            "munosabatlaringizni yanada mustahkamlang. 💕"
        ),
    },
    "ru": {
        "menu_support": "🫂 Поговорим",
        "support_intro": "🫂 Я готов(а) тебя выслушать. Можешь спокойно рассказать всё, что на душе. Я не буду тебя осуждать. Можешь выговориться ❤️",
        "adult_content_warning": "🚫 Этот бот не поддерживает подобный контент. Пожалуйста, будьте уважительны.",
        "menu_pair": "💑 Связать пару",
        "menu_couple": "❤️ Моя пара",
        "menu_letter": "💌 Отправить письмо",
        "menu_games": "🎲 Игры для пар",
        "menu_question": "💭 Вопрос дня",
        "menu_gift": "🎁 Виртуальные подарки",
        "menu_memories": "📸 Воспоминания",
        "menu_days": "❤️ Дней вместе",
        "menu_notif": "🔔 Уведомления",
        "menu_settings": "⚙️ Настройки",
        "menu_help": "ℹ️ Помощь",
        "home_button": "🏠 Главное меню",
        "back_button": "⬅️ Назад",
        "home_menu": "🏠 Главное меню:",
        "welcome": (
            "❤️ Добро пожаловать в @JuftimBotbot!\n\n"
            "С этим ботом вы и ваша пара сможете:\n"
            "💌 отправлять письма\n"
            "🎲 играть в игры\n"
            "💭 отвечать на вопросы\n"
            "🎁 отправлять виртуальные подарки\n"
            "📸 сохранять воспоминания.\n\n"
            "Нажмите '💑 Связать пару', чтобы начать."
        ),
        "already_paired": "❤️ Вы уже связаны с парой.",
        "invite_invalid": "❌ Эта ссылка-приглашение недействительна или истекла.",
        "invite_self": "❌ Вы не можете пригласить самого себя.",
        "invite_ask": "❤️ {name} пригласил(а) вас в пару. Принимаете?",
        "invite_accept": "❤️ Принять",
        "invite_reject": "❌ Отклонить",
        "invite_rejected": "❌ Приглашение отклонено.",
        "pair_success": "🎉 Поздравляем!\n❤️ Пара успешно создана!",
        "help_text": (
            "ℹ️ Как работает @JuftimBotbot:\n\n"
            "1️⃣ Нажмите '💑 Связать пару' и получите ссылку-приглашение.\n"
            "2️⃣ Отправьте её своей второй половинке.\n"
            "3️⃣ Пусть он(а) откроет её и примет приглашение.\n"
            "4️⃣ Теперь вы можете общаться через письма, игры, подарки и воспоминания!\n\n"
            "Команды:\n"
            "/start — перезапустить бота\n"
            "/admin — админ-панель (только для администраторов)"
        ),
        "no_couple": "❌ Сначала нужно связаться с парой.",
        "couple_invite_prompt": "💑 Пригласите свою пару в @JuftimBotbot.",
        "couple_link_btn": "🔗 Ссылка-приглашение",
        "couple_code_btn": "📋 Мой код",
        "couple_link_sent": "🔗 Ваша ссылка-приглашение:\n{link}\n\nОтправьте её своей второй половинке.",
        "couple_code_sent": "📋 Ваш код: {code}\n\nПусть ваша пара отправит боту команду:\n/start {code}",
        "couple_info": "❤️ Ваша пара:\n👤 {name}\n{sana}",
        "couple_date_set": "📅 Дата вместе: {date}\n❤️ Дней вместе: {days}",
        "couple_date_unset": "📅 Дата вместе: не указана",
        "couple_set_date_btn": "📅 Указать дату",
        "couple_send_letter_btn": "💌 Отправить письмо",
        "couple_memories_btn": "📸 Воспоминания",
        "couple_unpair_btn": "💔 Разорвать пару",
        "couple_unpair_confirm": "⚠️ Вы точно хотите разорвать пару?",
        "couple_unpair_yes": "💔 Да, разорвать",
        "couple_unpair_no": "❌ Нет",
        "couple_unpaired": "💔 Пара разорвана.",
        "couple_partner_unpaired": "💔 Ваша пара разорвала связь. Вы можете создать новое приглашение.",
        "letters_prompt": "💌 Что хотите отправить своей паре?",
        "letters_text_btn": "📝 Текстовое письмо",
        "letters_photo_btn": "📸 Фото + сообщение",
        "letters_love_btn": "❤️ Романтичное сообщение",
        "letters_send_btn": "📤 Отправить",
        "letters_edit_btn": "✏️ Изменить",
        "letters_cancel_btn": "❌ Отменить",
        "letters_write_text": "✍️ Напишите текст:",
        "letters_send_photo": "📸 Отправьте фото (можно с подписью):",
        "letters_preview": "💌 Ваше письмо:\n\n{text}\n\nОтправить паре?",
        "letters_cancelled": "❌ Отменено.",
        "letters_sent": "✅ Письмо отправлено!",
        "letters_received": "💌 Вам пришло новое письмо от пары!",
        "letters_reply_btn": "❤️ Ответить",
        "games_prompt": "🎲 Выберите игру:",
        "game_know_btn": "❤️ Насколько хорошо вы знаете друг друга?",
        "game_who_btn": "😂 Кто больше?",
        "game_truth_dare_btn": "💭 Правда или действие",
        "game_compat_btn": "🔥 Тест на совместимость",
        "game_quiz_btn": "🧠 Викторина для пар",
        "question_prompt": "💭 Вопрос дня:\n{question}",
        "question_answer_btn": "📝 Ответить",
        "question_view_btn": "👀 Посмотреть ответ пары",
        "question_another_btn": "🔄 Другой вопрос",
        "question_write_answer": "✍️ Напишите ваш ответ:",
        "question_saved_waiting": "✅ Ваш ответ сохранён! Ждём ответа вашей пары. 💭",
        "gifts_prompt": "🎁 Выберите подарок:",
        "gift_sent": "✅ Подарок отправлен!",
        "gift_received": "🎁 Вам пришёл подарок от пары!\n\n{emoji} {name}",
        "memories_prompt": "📸 Раздел воспоминаний:",
        "memories_add_btn": "➕ Добавить воспоминание",
        "memories_view_btn": "📖 Посмотреть воспоминания",
        "memories_delete_btn": "🗑 Удалить воспоминание",
        "memory_send_photo": "📸 Отправьте фото:",
        "memory_send_caption": "✏️ Напишите подпись (или '-' чтобы пропустить):",
        "memory_saved": "✅ Воспоминание сохранено!",
        "days_unset": "❤️ Укажите дату начала отношений.",
        "days_set_btn": "📅 Указать дату",
        "days_change_btn": "📅 Изменить дату",
        "days_together": "❤️ Вы вместе уже:\n{total} дней\n{breakdown}",
        "days_ask": "📅 Введите дату (в формате ДД.ММ.ГГГГ, например: 01.05.2023):",
        "days_saved": "✅ Дата сохранена: {date}",
        "settings_prompt": "⚙️ Настройки:",
        "settings_notif_btn": "🔔 Уведомления",
        "settings_lang_btn": "🌐 Язык",
        "settings_profile_btn": "👤 Профиль",
        "settings_couple_btn": "❤️ Настройки пары",
        "settings_about_btn": "ℹ️ О боте",
        "notif_prompt": "🔔 Уведомления (нажмите, чтобы включить/выключить):",
        "notif_daily_question": "💭 Вопрос дня",
        "notif_daily_message": "❤️ Ежедневное романтичное сообщение",
        "notif_new_letter": "💌 Новое письмо",
        "notif_gift": "🎁 Подарок",
        "notif_special_date": "📅 Особая дата",
        "lang_prompt": "🌐 Выберите язык:",
        "lang_changed": "✅ Язык изменён.",
        "profile_text": "👤 Имя: {name}\n🆔 Username: {username}\n❤️ Статус пары: {status}\n📅 Дата пары: {date}",
        "profile_paired": "❤️ В паре",
        "profile_not_paired": "❌ Не в паре",
        "profile_no_date": "не указана",
        "about_text": (
            "ℹ️ @JuftimBotbot — специальный бот для влюблённых пар.\n\n"
            "Укрепляйте отношения через письма, игры, ежедневные вопросы, "
            "подарки и воспоминания. 💕"
        ),
    },
    "en": {
        "menu_support": "🫂 Let's Talk",
        "support_intro": "🫂 I'm here to listen. You can share whatever is on your mind. I won't judge you. Feel free to talk it out ❤️",
        "adult_content_warning": "🚫 This bot does not support that kind of content. Please keep things respectful.",
        "menu_pair": "💑 Link Partner",
        "menu_couple": "❤️ My Partner",
        "menu_letter": "💌 Send Letter",
        "menu_games": "🎲 Couple Games",
        "menu_question": "💭 Question of the Day",
        "menu_gift": "🎁 Virtual Gifts",
        "menu_memories": "📸 Memories",
        "menu_days": "❤️ Days Together",
        "menu_notif": "🔔 Notifications",
        "menu_settings": "⚙️ Settings",
        "menu_help": "ℹ️ Help",
        "home_button": "🏠 Main Menu",
        "back_button": "⬅️ Back",
        "home_menu": "🏠 Main menu:",
        "welcome": (
            "❤️ Welcome to @JuftimBotbot!\n\n"
            "With this bot, you and your partner can:\n"
            "💌 send letters\n"
            "🎲 play games\n"
            "💭 answer daily questions\n"
            "🎁 send virtual gifts\n"
            "📸 save memories.\n\n"
            "Tap '💑 Link Partner' to get started."
        ),
        "already_paired": "❤️ You are already linked with a partner.",
        "invite_invalid": "❌ This invite link is invalid or expired.",
        "invite_self": "❌ You can't invite yourself.",
        "invite_ask": "❤️ {name} invited you to be their partner. Do you accept?",
        "invite_accept": "❤️ Accept",
        "invite_reject": "❌ Decline",
        "invite_rejected": "❌ Invitation declined.",
        "pair_success": "🎉 Congratulations!\n❤️ You are now linked as a couple!",
        "help_text": (
            "ℹ️ How @JuftimBotbot works:\n\n"
            "1️⃣ Tap '💑 Link Partner' to get your invite link.\n"
            "2️⃣ Send the link to your partner.\n"
            "3️⃣ They open it and accept the invitation.\n"
            "4️⃣ Now you can connect through letters, games, gifts and memories!\n\n"
            "Commands:\n"
            "/start — restart the bot\n"
            "/admin — admin panel (admins only)"
        ),
        "no_couple": "❌ You need to link with a partner first.",
        "couple_invite_prompt": "💑 Invite your partner to @JuftimBotbot.",
        "couple_link_btn": "🔗 Invite Link",
        "couple_code_btn": "📋 My Code",
        "couple_link_sent": "🔗 Your invite link:\n{link}\n\nSend this link to your partner.",
        "couple_code_sent": "📋 Your code: {code}\n\nHave your partner send this to the bot:\n/start {code}",
        "couple_info": "❤️ Your partner:\n👤 {name}\n{sana}",
        "couple_date_set": "📅 Anniversary: {date}\n❤️ Days together: {days}",
        "couple_date_unset": "📅 Anniversary: not set",
        "couple_set_date_btn": "📅 Set Date",
        "couple_send_letter_btn": "💌 Send Letter",
        "couple_memories_btn": "📸 Memories",
        "couple_unpair_btn": "💔 Unlink Partner",
        "couple_unpair_confirm": "⚠️ Are you sure you want to unlink your partner?",
        "couple_unpair_yes": "💔 Yes, unlink",
        "couple_unpair_no": "❌ No",
        "couple_unpaired": "💔 Partnership ended.",
        "couple_partner_unpaired": "💔 Your partner ended the connection. You can create a new invite link.",
        "letters_prompt": "💌 What would you like to send your partner?",
        "letters_text_btn": "📝 Text Letter",
        "letters_photo_btn": "📸 Photo + Message",
        "letters_love_btn": "❤️ Love Message",
        "letters_send_btn": "📤 Send",
        "letters_edit_btn": "✏️ Edit",
        "letters_cancel_btn": "❌ Cancel",
        "letters_write_text": "✍️ Write your message:",
        "letters_send_photo": "📸 Send a photo (you can add a caption):",
        "letters_preview": "💌 Your letter:\n\n{text}\n\nSend it to your partner?",
        "letters_cancelled": "❌ Cancelled.",
        "letters_sent": "✅ Letter sent!",
        "letters_received": "💌 You received a new letter from your partner!",
        "letters_reply_btn": "❤️ Reply",
        "games_prompt": "🎲 Choose a game:",
        "game_know_btn": "❤️ How Well Do You Know Each Other?",
        "game_who_btn": "😂 Who's More?",
        "game_truth_dare_btn": "💭 Truth or Dare",
        "game_compat_btn": "🔥 Compatibility Test",
        "game_quiz_btn": "🧠 Couple Quiz",
        "question_prompt": "💭 Question of the day:\n{question}",
        "question_answer_btn": "📝 Answer",
        "question_view_btn": "👀 View Partner's Answer",
        "question_another_btn": "🔄 Another Question",
        "question_write_answer": "✍️ Write your answer:",
        "question_saved_waiting": "✅ Your answer is saved! Waiting for your partner to answer. 💭",
        "gifts_prompt": "🎁 Choose a gift:",
        "gift_sent": "✅ Gift sent!",
        "gift_received": "🎁 You received a gift from your partner!\n\n{emoji} {name}",
        "memories_prompt": "📸 Memories section:",
        "memories_add_btn": "➕ Add Memory",
        "memories_view_btn": "📖 View Memories",
        "memories_delete_btn": "🗑 Delete Memory",
        "memory_send_photo": "📸 Send a photo:",
        "memory_send_caption": "✏️ Write a caption (or send '-' to skip):",
        "memory_saved": "✅ Memory saved!",
        "days_unset": "❤️ Set the date you got together.",
        "days_set_btn": "📅 Set Date",
        "days_change_btn": "📅 Change Date",
        "days_together": "❤️ You've been together for:\n{total} days\n{breakdown}",
        "days_ask": "📅 Enter the date (DD.MM.YYYY, e.g. 01.05.2023):",
        "days_saved": "✅ Date saved: {date}",
        "settings_prompt": "⚙️ Settings:",
        "settings_notif_btn": "🔔 Notifications",
        "settings_lang_btn": "🌐 Language",
        "settings_profile_btn": "👤 Profile",
        "settings_couple_btn": "❤️ Partner Settings",
        "settings_about_btn": "ℹ️ About",
        "notif_prompt": "🔔 Notifications (tap to toggle):",
        "notif_daily_question": "💭 Question of the day",
        "notif_daily_message": "❤️ Daily romantic message",
        "notif_new_letter": "💌 New letter",
        "notif_gift": "🎁 Gift",
        "notif_special_date": "📅 Special date",
        "lang_prompt": "🌐 Choose your language:",
        "lang_changed": "✅ Language changed.",
        "profile_text": "👤 Name: {name}\n🆔 Username: {username}\n❤️ Partner status: {status}\n📅 Anniversary: {date}",
        "profile_paired": "❤️ Linked",
        "profile_not_paired": "❌ Not linked",
        "profile_no_date": "not set",
        "about_text": (
            "ℹ️ @JuftimBotbot — a special bot for couples in love.\n\n"
            "Strengthen your relationship through letters, games, daily questions, "
            "gifts and memories. 💕"
        ),
    },
    "kk": {
        "menu_support": "🫂 Сырласайық",
        "support_intro": "🫂 Мен сені тыңдауға дайынмын. Ішіңде не болса да, еркін айта аласың. Сені кінәламаймын. Жүрегіңді бос ала аласың ❤️",
        "adult_content_warning": "🚫 Бұл бот мұндай контентті қолдамайды. Өтінеміз, құрметпен қарым-қатынас жасаңыз.",
        "menu_pair": "💑 Жұбымды қосу",
        "menu_couple": "❤️ Жұбым",
        "menu_letter": "💌 Хат жіберу",
        "menu_games": "🎲 Жұп ойындары",
        "menu_question": "💭 Күнделікті сұрақ",
        "menu_gift": "🎁 Виртуалды сыйлықтар",
        "menu_memories": "📸 Естеліктер",
        "menu_days": "❤️ Бірге өткен күндер",
        "menu_notif": "🔔 Хабарландырулар",
        "menu_settings": "⚙️ Баптаулар",
        "menu_help": "ℹ️ Көмек",
        "home_button": "🏠 Басты мәзір",
        "back_button": "⬅️ Артқа",
        "home_menu": "🏠 Басты мәзір:",
        "welcome": (
            "❤️ @JuftimBotbot ботына қош келдіңіз!\n\n"
            "Бұл бот арқылы жұбыңызбен:\n"
            "💌 хаттар жібере аласыз\n"
            "🎲 ойындар ойнай аласыз\n"
            "💭 сұрақтарға жауап бере аласыз\n"
            "🎁 виртуалды сыйлықтар жібере аласыз\n"
            "📸 естеліктер сақтай аласыз.\n\n"
            "Бастау үшін '💑 Жұбымды қосу' түймесін басыңыз."
        ),
        "already_paired": "❤️ Сіз әлдеқашан жұппен қосылғансыз.",
        "invite_invalid": "❌ Бұл шақыру сілтемесі жарамсыз немесе мерзімі өтіп кеткен.",
        "invite_self": "❌ Өзіңізді өзіңіз шақыра алмайсыз.",
        "invite_ask": "❤️ {name} сізді жұп болуға шақырды. Қабылдайсыз ба?",
        "invite_accept": "❤️ Қабылдау",
        "invite_reject": "❌ Бас тарту",
        "invite_rejected": "❌ Шақыру қабылданбады.",
        "pair_success": "🎉 Құттықтаймыз!\n❤️ Жұп сәтті қосылды!",
        "help_text": (
            "ℹ️ @JuftimBotbot қалай жұмыс істейді:\n\n"
            "1️⃣ '💑 Жұбымды қосу' түймесін басып, шақыру сілтемесін алыңыз.\n"
            "2️⃣ Сілтемені жаныңызға жіберіңіз.\n"
            "3️⃣ Ол сілтемені ашып, шақыруды қабылдасын.\n"
            "4️⃣ Енді екеуіңіз хаттар, ойындар, сыйлықтар және естеліктер арқылы байланыса аласыздар!\n\n"
            "Командалар:\n"
            "/start — ботты қайта бастау\n"
            "/admin — әкімші панелі (тек әкімшілер үшін)"
        ),
        "no_couple": "❌ Алдымен жұбыңызбен қосылу керек.",
        "couple_invite_prompt": "💑 Жұбыңызды @JuftimBotbot ботына шақырыңыз.",
        "couple_link_btn": "🔗 Шақыру сілтемесі",
        "couple_code_btn": "📋 Менің кодым",
        "couple_link_sent": "🔗 Сіздің шақыру сілтемеңіз:\n{link}\n\nБұл сілтемені жаныңызға жіберіңіз.",
        "couple_code_sent": "📋 Сіздің кодыңыз: {code}\n\nЖұбыңыз ботқа мына команданы жіберсін:\n/start {code}",
        "couple_info": "❤️ Сіздің жұбыңыз:\n👤 {name}\n{sana}",
        "couple_date_set": "📅 Бірге болған күн: {date}\n❤️ Бірге өткен күндер: {days}",
        "couple_date_unset": "📅 Бірге болған күн: белгіленбеген",
        "couple_set_date_btn": "📅 Күнді белгілеу",
        "couple_send_letter_btn": "💌 Хат жіберу",
        "couple_memories_btn": "📸 Естеліктер",
        "couple_unpair_btn": "💔 Жұпты ажырату",
        "couple_unpair_confirm": "⚠️ Жұпты шынымен ажыратқыңыз келе ме?",
        "couple_unpair_yes": "💔 Иә, ажырату",
        "couple_unpair_no": "❌ Жоқ",
        "couple_unpaired": "💔 Жұп ажыратылды.",
        "couple_partner_unpaired": "💔 Жұбыңыз байланысты үзді. Жаңа жұп үшін шақыру сілтемесін жасай аласыз.",
        "letters_prompt": "💌 Жұбыңызға не жібергіңіз келеді?",
        "letters_text_btn": "📝 Мәтінді хат",
        "letters_photo_btn": "📸 Сурет + хабар",
        "letters_love_btn": "❤️ Махаббат хабары",
        "letters_send_btn": "📤 Жіберу",
        "letters_edit_btn": "✏️ Өзгерту",
        "letters_cancel_btn": "❌ Бас тарту",
        "letters_write_text": "✍️ Мәтініңізді жазыңыз:",
        "letters_send_photo": "📸 Сурет жіберіңіз (жазумен бірге жіберуге болады):",
        "letters_preview": "💌 Сіздің хатыңыз:\n\n{text}\n\nЖұбыңызға жіберілсін бе?",
        "letters_cancelled": "❌ Бас тартылды.",
        "letters_sent": "✅ Хат жіберілді!",
        "letters_received": "💌 Сізге жұбыңыздан жаңа хат келді!",
        "letters_reply_btn": "❤️ Жауап беру",
        "games_prompt": "🎲 Ойындардың бірін таңдаңыз:",
        "game_know_btn": "❤️ Бір-біріңізді қаншалықты білесіздер?",
        "game_who_btn": "😂 Кім көбірек?",
        "game_truth_dare_btn": "💭 Шындық немесе әрекет",
        "game_compat_btn": "🔥 Үйлесімділік тесті",
        "game_quiz_btn": "🧠 Жұп викторинасы",
        "question_prompt": "💭 Күнделікті сұрақ:\n{question}",
        "question_answer_btn": "📝 Жауап беру",
        "question_view_btn": "👀 Жұбымның жауабын көру",
        "question_another_btn": "🔄 Басқа сұрақ",
        "question_write_answer": "✍️ Жауабыңызды жазыңыз:",
        "question_saved_waiting": "✅ Жауабыңыз сақталды! Жұбыңыздың жауабын күтеміз. 💭",
        "gifts_prompt": "🎁 Сыйлық таңдаңыз:",
        "gift_sent": "✅ Сыйлық жіберілді!",
        "gift_received": "🎁 Сізге жұбыңыздан сыйлық келді!\n\n{emoji} {name}",
        "memories_prompt": "📸 Естеліктер бөлімі:",
        "memories_add_btn": "➕ Естелік қосу",
        "memories_view_btn": "📖 Естеліктерді көру",
        "memories_delete_btn": "🗑 Естелікті өшіру",
        "memory_send_photo": "📸 Сурет жіберіңіз:",
        "memory_send_caption": "✏️ Жазу жазыңыз (немесе өткізіп жіберу үшін '-' жіберіңіз):",
        "memory_saved": "✅ Естелік сақталды!",
        "days_unset": "❤️ Бірге болған күніңізді белгілеңіз.",
        "days_set_btn": "📅 Күнді белгілеу",
        "days_change_btn": "📅 Күнді өзгерту",
        "days_together": "❤️ Сіздер бірге болғаныңызға:\n{total} күн\n{breakdown}",
        "days_ask": "📅 Күнді енгізіңіз (КК.АА.ЖЖЖЖ форматында, мысалы: 01.05.2023):",
        "days_saved": "✅ Күн сақталды: {date}",
        "settings_prompt": "⚙️ Баптаулар:",
        "settings_notif_btn": "🔔 Хабарландырулар",
        "settings_lang_btn": "🌐 Тіл",
        "settings_profile_btn": "👤 Профиль",
        "settings_couple_btn": "❤️ Жұп баптаулары",
        "settings_about_btn": "ℹ️ Бот туралы",
        "notif_prompt": "🔔 Хабарландырулар (қосу/өшіру үшін басыңыз):",
        "notif_daily_question": "💭 Күнделікті сұрақ",
        "notif_daily_message": "❤️ Күнделікті романтикалық хабар",
        "notif_new_letter": "💌 Жаңа хат",
        "notif_gift": "🎁 Сыйлық",
        "notif_special_date": "📅 Ерекше күн",
        "lang_prompt": "🌐 Тілді таңдаңыз:",
        "lang_changed": "✅ Тіл өзгертілді.",
        "profile_text": "👤 Аты: {name}\n🆔 Username: {username}\n❤️ Жұп мәртебесі: {status}\n📅 Жұп күні: {date}",
        "profile_paired": "❤️ Қосылған",
        "profile_not_paired": "❌ Қосылмаған",
        "profile_no_date": "белгіленбеген",
        "about_text": (
            "ℹ️ @JuftimBotbot — ғашық жұптарға арналған арнайы бот.\n\n"
            "Хаттар, ойындар, күнделікті сұрақтар, сыйлықтар және естеліктер арқылы "
            "қарым-қатынасыңызды нығайтыңыз. 💕"
        ),
    },
}


def t(lang: str, key: str, **kwargs) -> str:
    """Berilgan til va kalit bo'yicha tarjima matnini qaytaradi."""
    lang_dict = TEXTS.get(lang, TEXTS["uz"])
    text = lang_dict.get(key) or TEXTS["uz"].get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text
