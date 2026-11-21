# Kaynak bulma ve indirme

© 2026 Vinci Studio. Tüm hakları saklıdır.

- **Bölüm indirme:** `yt-dlp --download-sections "*1:02:10-1:05:10" -o kaynak/ad.mp4 <adres>`
- **Kick arşivi:** `https://kick.com/api/v2/channels/<kanal>/videos` → `source` (master.m3u8). Yayın canlıyken bile tüm arşiv gelir; parçalar 10 sn ve ses ile görüntü aynı akışta. Ucuz tarama için `160p30`, seçilen dilim için `1080p60`.
- **YouTube canlı, son dakikalar:** `scripts/canli.sh <adres> <kaç dk önce> <kaç dk> kaynak/ad.mp4 [312=1080p60]`. Görüntü ve ses ayrı listelerden gelir, script bunları sıra numarasıyla eşler. Elle ayrı indirmede 92 sn kayma görüldü.
- **Hazır kesit kanalları:** büyük yayıncıların klip kanallarındaki en çok izlenen anlar, ham 1080p kesit olarak indirilip Türkçeleştirilebilir. Kaynak açıklamada belirtilir.
- **Meme / tepki klipleri:** Vlipsy (ücretsiz sürüm 480p ve logolu; tarayıcıda `video.currentSrc` alınıp `curl -e https://vlipsy.com/` ile indirilir), PlayPhrase (film replikleri). Telifli oldukları için kısa (1–3 sn) kullan.
- Telif: başkasının görüntüsü Content ID'ye takılabilir. Yorum ve kurgu katkısı ekle, kaynağı belirt.
