---
name: shorts-klip
description: Yayın, oyun, podcast ya da uzun videodan dikey kısa klip (Reels/Shorts/TikTok) üretir. Whisper taraması, ses patlaması tespiti, bölünmüş kamera+oyun düzeni, kutulu kanca başlığı, akan Anton altyazı, zoom/flaş/kromatik vuruş, efekt sesleri, kendi sesiyle seslendirme ve -14 LUFS. "Klip çıkar", "yayından kesit", "Shorts yap", "Kick/Twitch/YouTube kesiti" denince kullan.
license: Proprietary. © 2026 Vinci Studio. Tüm hakları saklıdır. Bkz. LICENSE.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, WebFetch, WebSearch
metadata:
  sahip: Vinci Studio
  surum: "1.0.0"
---

# Shorts / Reels klip hattı

`PY=~/.vinci-video/.venv/bin/python`. Bu skill'deki scriptler `scripts/` klasöründe. Hepsi **proje klasöründen** çalıştırılır;
yollar o klasöre göredir. Font ve hazır efektler `~/.vinci-video`'dan gelir. Projede `sesler/<ad>.wav` varsa ortak olanın yerine o kullanılır.

## Akış
1. **Kaynak al.** Yöntemler `references/kaynak.md`'de: yt-dlp ile bölüm indirme, Kick arşivi, canlı yayının son dakikaları için `scripts/canli.sh`.
2. **Tara.** `$PY scripts/tara.py kaynak/ad.mp4 [--dil en] [--vadsiz]` → `isler/ad-tarama.json`: konuşma dökümü (kelime zamanlı) ve ses patlamaları (bağırma, gülme).
3. **Anı seç.** Patlama + şaşkınlık + beklenmedik son. Sıradan an seçme. Klip 13–20 sn ya da 50–60 sn olmalı (30–45 sn ölü bölge).
4. **İş dosyası yaz:** `isler/ad.json`. Bütün alanlar `references/is-dosyasi.md`'de. Altyazılar Türkçe, kısa ve büyük harf; `*kelime*` sarı vurgu olur.
5. **Kurgu.** `$PY scripts/kurgu.py isler/ad.json --kontrol` → `cikti/ad.mp4` + `cikti/ad-kontrol.jpg`. Kontrol sayfasını mutlaka aç: yeşil çizgiler yazı sınırı, kırmızı kutu platform arayüzünün kapattığı alt bölge.
6. **Doğrula.** Canlı kaynakta ses kayması için `$PY scripts/esitle.py kaynak.mp4 x y w h` ya da ekrandaki altyazıyla karşılaştır. Çıktının sesini `transkript` ile kontrol et.
7. **Yükleme kopyası.** `scripts/yukle.sh cikti/ad.mp4` → `yukle/ad.mp4` (10 MB altı).
8. **Yayın.** Yalnız kullanıcı onayıyla, gündüz saatlerinde (12–15 ya da 19–22), günde en fazla 3. Ayrıntısı `references/strateji.md`'de.

## Para kazanma notu
Sadece altyazı eklenmiş başkasının videosu "özgün olmayan içerik" sayılır. Her klipte gerçek katkı olsun:
kendi sesinle yorum ya da seslendirme (`seslendirme` skill'i, iş dosyasında `seslendirme` alanı), kurgu ve bağlam.
Açıklamada kaynağı belirt.
