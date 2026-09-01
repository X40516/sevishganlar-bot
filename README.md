# Sevishganlar Bot 💕

Faqat juftliklar (sevishganlar) uchun mo'ljallangan Telegram bot.

## Imkoniyatlar

- **🔞 18+ yosh tasdiqlash** — botdan foydalanishdan oldin foydalanuvchi yoshini tasdiqlaydi
- **🔗 Ulanish (pairing)** — noyob kod orqali partneringiz bilan ulanasiz
- **💌 Sevgi xabari / 😊 Kompliment** — partneringizga to'g'ridan-to'g'ri yuboriladi
- **📜 Romantik iqtiboslar**
- **🎲 Uchrashuv g'oyalari**
- **💑 Necha kun birgamiz** — yodgorlik sanasidan hisoblab beradi

## Buyruqlar

| Buyruq | Tavsif |
|---|---|
| `/start` | Botni boshlash, yosh tasdiqlash |
| `/menu` | Sevishganlar menyusini ko'rsatish |
| `/pair <kod>` | Partneringiz bilan ulanish |
| `/anniversary YYYY-MM-DD` | Yodgorlik sanasini kiritish |
| `/help` | Yordam |

## O'rnatish

1. Repozitoriyani yuklab oling:
   ```bash
   git clone <repo-url>
   cd sevishganlar-bot
   ```

2. Kutubxonalarni o'rnating:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. `.env.example` dan nusxa oling va tokeningizni kiriting:
   ```bash
   cp .env.example .env
   ```

4. Botni ishga tushiring:
   ```bash
   python bot.py
   ```

## Deploy qilish

Botni 24/7 ishlab turishi uchun [Railway](https://railway.com/) yoki [Render](https://render.com/) kabi xizmatlarga joylashtiring.

## Xavfsizlik

Bot faqat foydalanuvchi o'zi "18 yoshdan katta" deb tasdiqlagandan keyingina sevishganlar funksiyalariga kirish huquqini beradi.
