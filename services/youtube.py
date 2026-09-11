"""
YouTube qidiruv xizmati.

MUHIM: Bu modul faqat video/qo'shiq HAVOLASINI topadi va yuboradi.
Video kontentini yuklab olish yoki saqlash amalga oshirilmaydi - bu
YouTube foydalanish shartlari va mualliflik huquqini buzadi.
"""
import urllib.parse

import aiohttp

from config import YOUTUBE_API_KEY


async def search_youtube(query: str) -> tuple[str, str]:
    """
    (sarlavha, havola) qaytaradi.

    Agar YOUTUBE_API_KEY sozlangan bo'lsa, YouTube Data API orqali eng
    mos videoni topadi. Aks holda, oddiy qidiruv natijalari havolasini
    yaratadi - foydalanuvchi o'zi kerakli videoni tanlaydi.
    """
    if YOUTUBE_API_KEY:
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": 1,
            "key": YOUTUBE_API_KEY,
        }
        url = "https://www.googleapis.com/youtube/v3/search?" + urllib.parse.urlencode(params)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=8)) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        items = data.get("items", [])
                        if items:
                            video_id = items[0]["id"]["videoId"]
                            title = items[0]["snippet"]["title"]
                            return title, f"https://www.youtube.com/watch?v={video_id}"
        except Exception:
            pass

    search_url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(query)
    return query, search_url
