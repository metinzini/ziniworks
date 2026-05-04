import requests
import json
import os
from datetime import datetime, timezone

BIN_ID = os.environ["BIN_ID"]
API_KEY_JSONBIN = os.environ["API_KEY_JSONBIN"]
GROQ_API_KEY = os.environ["GROQ_API_KEY"]

BIN_URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
HEADERS_JSONBIN = {"X-Master-Key": API_KEY_JSONBIN}
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def fetch_bin():
    r = requests.get(f"{BIN_URL}/latest", headers=HEADERS_JSONBIN)
    r.raise_for_status()
    record = r.json().get("record", {})
    posts = record.get("posts", []) if isinstance(record, dict) else record
    comments = record.get("comments", []) if isinstance(record, dict) else []
    return posts, comments

def save_bin(posts, comments):
    r = requests.put(
        BIN_URL,
        headers={**HEADERS_JSONBIN, "Content-Type": "application/json"},
        data=json.dumps({"posts": posts, "comments": comments})
    )
    r.raise_for_status()

def generate_post():
    prompt = """Sen ziniworks.fun adlı bir kişisel blogun yazarısın. Bugün tamamen istediğin bir konuda blog yazısı yazacaksın. Konu tamamen sana kalmış — teknoloji, felsefe, günlük bir gözlem, absürt bir düşünce, bilim, tarih, hiçbir şey — ne istersen.

ÖNEMLİ KURALLAR:
- Türkçe içerik EN AZ 3 paragraf olsun, her paragraf en az 4 cümle içersin
- İngilizce içerik de EN AZ 3 paragraf olsun
- Türkçe içerikte SADECE Türkçe kelimeler kullan, kesinlikle yabancı karakter veya kelime karıştırma
- İngilizce içerikte SADECE İngilizce yaz
- Gerçek kelimeler kullan, kelime UYDURMAYACAKSIN
- Yazım hatası yapmamaya dikkat et
- Samimi, akıcı ve düşündürücü bir dil kullan

Sadece aşağıdaki JSON formatında yanıt ver, başka hiçbir şey yazma, markdown bloğu da kullanma:

{
  "title_tr": "Türkçe başlık",
  "title_en": "English title",
  "hook_tr": "Okuyucuyu çeken tek cümlelik Türkçe özet",
  "hook_en": "One sentence English hook",
  "content_tr": "Türkçe içerik (markdown destekli, 150-300 kelime)",
  "content_en": "English content (markdown supported, 150-300 words)",
  "color": "#hexrenk (koyu bir renk, slider arka planı için, örnek: #0d1b2a)"
}

Yazı samimi, düşündürücü ve kısa olsun. Clickbait olmasın."""

    r = requests.post(
        GROQ_URL,
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 2000,
            "temperature": 0.9
        }
    )
    r.raise_for_status()
    raw = r.json()["choices"][0]["message"]["content"].strip()

    if "```" in raw:
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    return json.loads(raw)

def main():
    print(f"[{datetime.now(timezone.utc).isoformat()}] Autopost başlıyor...")
    posts, comments = fetch_bin()
    print(f"Mevcut yazı sayısı: {len(posts)}")
    post_data = generate_post()
    print(f"Yazı üretildi: {post_data['title_tr']}")
    new_post = {
        "id": f"p{int(datetime.now(timezone.utc).timestamp() * 1000)}",
        "title_tr": post_data["title_tr"],
        "title_en": post_data["title_en"],
        "hook_tr": post_data["hook_tr"],
        "hook_en": post_data["hook_en"],
        "content_tr": post_data["content_tr"],
        "content_en": post_data["content_en"],
        "color": post_data.get("color", "#0a0a0a"),
        "date": datetime.now(timezone.utc).isoformat(),
        "auto": True
    }
    posts.append(new_post)
    save_bin(posts, comments)
    print(f"Yayinlandi! ID: {new_post['id']}")

if __name__ == "__main__":
    main()
