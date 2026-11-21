---
name: ses-muzik
description: Telifsiz ses efekti ve fon müziği: sentezlenmiş efektler (whoosh, boom, pop, ding, buzzer, plak cızırtısı, bruh), sentez ambient müzik, telifsiz müzik kaynakları, ses seviyesi ve karışım kuralları. "Ses efekti", "müzik ekle", "fon müziği", "ses seviyesi" denince kullan.
license: Proprietary. © 2026 Vinci Studio. Tüm hakları saklıdır. Bkz. LICENSE.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, WebFetch, WebSearch
metadata:
  sahip: Vinci Studio
  surum: "1.0.0"
---

# Ses efekti ve müzik

## Sentez (telif riski sıfır)
- Efektler: `~/.vinci-video/.venv/bin/python scripts/efektler.py [klasör]` → `whoosh, boom, pop, ding, yanlis, cizik, bruh` (kurulumda `~/.vinci-video/sesler` altına üretilir).
- Fon müziği: `~/.vinci-video/.venv/bin/python scripts/fon_muzik.py cikti.wav 45` → sakin, sıcak pad ve çan notaları (klinik, spa, kurumsal). Süre videoyla aynı olsun.

## Dış kaynaklar
- **Mixkit:** atıf istemez, ticari kullanım serbest. `mixkit.co/free-stock-music/<tür>/`.
- **Myinstants:** meme efektleri, yalnız eğlence ve kısa video işlerinde. Marka filminde kullanma.
- **HeyGen müzik kataloğu ve efektler:** `media-use` (giriş gerekir).
- **Trend şarkı:** videoya gömme. Instagram veya TikTok'ta paylaşırken uygulamanın kütüphanesinden ekle. Shorts'ta şarkı gelirin yarısını alır.

## Seviye ve karışım
- Son karışım: sosyal medya -14 LUFS, TP -1,5 dB (`loudnorm=I=-14:TP=-1.5:LRA=11`). Web ve TV için -16.
- Müzik konuşmanın 14–15 dB altında olur. "Duyulmuyor" derlerse fazla kısıktır (22 dB altı).
- Seslendirme varken müzik ve yayın sesi sidechain ile kısılır: `sidechaincompress=threshold=0.02:ratio=10:attack=15:release=350`.
- Efektler 0.6–0.9 seviyesinde, kesimden 20–40 ms önce başlar. Aynı efekti üst üste 3 kez kullanma.
- Ölçüm: `ffmpeg -i x.mp4 -af ebur128 -f null - 2>&1 | grep "I:"`.
