# ziniworks autopost

Her gün saat 10:00 UTC (Türkiye 13:00) otomatik yazı yayınlar.

## Kurulum

### 1. GitHub'a yükle
Bu 4 dosyayı yeni bir GitHub reposuna at:
- autopost.py
- requirements.txt
- railway.toml
- Procfile

### 2. Groq API key al (ücretsiz)
- console.groq.com → API Keys → Create API Key

### 3. Railway'de deploy et
- railway.app → New Project → Deploy from GitHub repo

### 4. Railway'de Variables ekle
BIN_ID          → 69f0ce83aaba88219749fb08
API_KEY_JSONBIN → JSONBin master key'in
GROQ_API_KEY    → Groq'tan aldığın key

### 5. Manuel test
Railway → Deployments → en son deploy → Redeploy
Loglardan "Yayinlandi!" yazısını görürsen çalışıyor.

## Saat değiştirmek
railway.toml içindeki cronSchedule:
"0 10 * * *"  → 10:00 UTC (TR 13:00)
"0 7 * * *"   → 07:00 UTC (TR 10:00)
"0 19 * * *"  → 19:00 UTC (TR 22:00)
