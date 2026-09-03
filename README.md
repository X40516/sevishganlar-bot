# @JuftimBotbot 💕

Sevishgan juftliklar uchun to'liq funksional Telegram bot. Ikki foydalanuvchi bir-birini ulaydi va bot orqali xat yozish, o'yinlar, savol-javob, virtual sovg'alar va xotiralarni saqlash imkoniyatiga ega bo'ladi.

## Imkoniyatlar

- **❤️ Juftlik ulash** — deep-link yoki kod orqali ikki foydalanuvchini bog'lash
- **💌 Xat yuborish** — matnli xat, rasm+izoh, yoki tayyor sevgi xabari
- **🎲 5 xil o'yin** — bir-biringizni bilish testi, "kim ko'proq", haqiqat/tanlov, moslik testi, juftlik viktorinasi
- **💭 Kunlik savol** — har kuni yangi savol, ikkalasi javob bergandan keyin javoblar taqqoslanadi
- **🎁 Virtual sovg'alar** — 6 xil sovg'a turi
- **📸 Xotiralar** — rasm va izoh bilan xotiralar albomi, pagination bilan ko'rish
- **❤️ Birga bo'lgan kunlar** — yil/oy/kun hisoblagichi
- **⚙️ Sozlamalar** — bildirishnomalar, profil, juftlik sozlamalari
- **👑 Admin panel** — statistika, broadcast, savol/sovg'a qo'shish, ban qilish
- **🔔 Kunlik avtomatik xabarlar** — scheduler orqali

## Texnologiyalar

- Python 3.11+
- aiogram 3.x
- PostgreSQL + SQLAlchemy 2.0 (async) + asyncpg
- APScheduler

## Loyiha strukturasi

```
juftim-bot/
├── main.py
├── config.py
├── database/
│   ├── models.py
│   ├── database.py
│   └── queries.py
├── handlers/
├── keyboards/
├── services/
│   └── content.py
├── scheduler/
│   └── scheduler.py
├── middlewares/
├── utils/
│   └── helpers.py
├── requirements.txt
├── .env.example
├── Dockerfile
└── railway.toml
```

## Database jadvallari

`users`, `couples`, `pair_invites`, `letters`, `daily_questions`, `question_answers`, `games`, `game_answers`, `gifts`, `gift_transactions`, `memories`, `notifications`, `admin_logs`.

Barcha jadvallar avtomatik yaratiladi (`init_db()` orqali) — qo'lda migratsiya kerak emas.

## O'rnatish (lokal)

1. Repozitoriyani yuklab oling:
   ```bash
   git clone <repo-url>
   cd juftim-bot
   ```

2. Virtual muhit yarating va kutubxonalarni o'rnating:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. `.env.example` dan nusxa oling va to'ldiring:
   ```bash
   cp .env.example .env
   ```

4. Botni ishga tushiring:
   ```bash
   python main.py
   ```

## Railway'da deploy qilish

1. GitHub'ga loyihani joylang.
2. Railway'da yangi loyiha yarating va shu GitHub repo'ni ulang.
3. Loyihaga PostgreSQL qo'shing.
4. Bot xizmatiga `BOT_TOKEN`, `DATABASE_URL`, `ADMIN_ID` qo'shing.
5. Railway avtomatik ravishda `Dockerfile` orqali botni build va deploy qiladi.

## Environment Variables

| O'zgaruvchi | Tavsif |
|---|---|
| `BOT_TOKEN` | Telegram bot tokeni |
| `DATABASE_URL` | PostgreSQL ulanish satri |
| `ADMIN_ID` | Admin panelga kirish huquqiga ega Telegram ID |
| `DAILY_QUESTION_HOUR` | Kunlik savol eslatmasi soati (standart: 10) |
| `DAILY_MESSAGE_HOUR` | Kunlik romantik xabar soati (standart: 19) |

## Admin panel

`/admin` buyrug'i orqali kirish mumkin (faqat `ADMIN_ID`). Statistika, foydalanuvchilar/juftliklar, broadcast, savol/sovg'a qo'shish va ban qilish.
