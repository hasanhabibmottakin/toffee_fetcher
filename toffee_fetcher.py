import requests
import json
from datetime import datetime
import os

API_URL = "https://toffeelive.com/api/web/playback/Ai51-JQBv9knK3AH_jWs"
AUTHORIZATION = "Bearer eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJodHRwczovL3RvZmZlZWxpdmUuY29tIiwiY291bnRyeSI6IkJEIiwiZF9pZCI6IjdhYjc4MDI2LTcwNTgtNGIxNy1hNzVkLWQ1MDlhZTllMmUwZSIsImV4cCI6MTc1MzQyNDg5MSwiaWF0IjoxNzUwNzk1MDkxLCJpc3MiOiJ0b2ZmZWVsaXZlLmNvbSIsImp0aSI6IjZlZmZjOGQ2LTA3OTYtNDhhMS1hOWFjLTc1ZGExNWY4ODMzNF8xNzUwNzk1MDkxIiwicHJvdmlkZXIiOiJ0b2ZmZWUiLCJyX2lkIjoiN2FiNzgwMjYtNzA1OC00YjE3LWE3NWQtZDUwOWFlOWUyZTBlIiwic19pZCI6IjdhYjc4MDI2LTcwNTgtNGIxNy1hNzVkLWQ1MDlhZTllMmUwZSIsInRva2VuIjoiYWNjZXNzIiwidHlwZSI6ImRldmljZSJ9.p2KSolKuN8yU5uSnA6igRxU-jADOoXIPk865CkxHkCEXbfL0sMnC8Pg3feghHEMzfHi3Y7lY-msNVjzKfSPyoQ"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Authorization": AUTHORIZATION,
    "Accept": "*/*",
    "Referer": "https://toffeelive.com/",
    "Origin": "https://toffeelive.com",
    "Content-Type": "application/json"
}

def get_cookie():
    try:
        response = requests.post(API_URL, headers=HEADERS, json={}, allow_redirects=False)
        cookie = response.cookies.get_dict()
        if cookie:
            cookie_str = '; '.join([f"{k}={v}" for k, v in cookie.items()])
            with open("cookie.txt", "w") as f:
                f.write(cookie_str)
            return cookie_str
    except Exception as e:
        print("Error fetching cookie:", e)
    return None

def load_channels():
    if not os.path.exists("api.json"):
        return None
    with open("api.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_outputs():
    cookie = get_cookie()
    if not cookie:
        print("❌ Failed to get cookie")
        return

    channels = load_channels()
    if not channels:
        print("❌ api.json missing")
        return

    for ch in channels:
        ch["cookie"] = cookie

    # ns.m3u (raw list as JSON, saved in .m3u extension)
    with open("ns.m3u", "w", encoding="utf-8") as f:
        f.write(json.dumps(channels, ensure_ascii=False, indent=2))

    # channels.json (full metadata)
    meta = {
        "name": "Toffee App All Channel Link with Headers",
        "owner": "BD Cooder Boy \nTelegram: https://t.me/fredflixceo",
        "channels_amount": len(channels),
        "updated_on": datetime.now().strftime("%d-%m-%Y %I:%M %p"),
        "channels": channels
    }
    with open("channels.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    # ott.m3u
    with open("ott.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for ch in channels:
            f.write(f'#EXTINF:-1 group-title="{ch["category_name"]}" tvg-chno="" tvg-id="" tvg-logo="{ch["logo"]}", {ch["name"]}\n')
            f.write('#EXTVLCOPT:http-user-agent=Toffee (Linux;Android 14) AndroidXMedia3/1.1.1/64103898/4d2ec9b8c7534adc\n')
            f.write(f'#EXTHTTP:{{"cookie":"{ch["cookie"]}"}}\n')
            f.write(f'{ch["link"]}\n\n')

    print("✅ Files updated: ns.m3u, channels.json, ott.m3u")

if __name__ == "__main__":
    save_outputs()
