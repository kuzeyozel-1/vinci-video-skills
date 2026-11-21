---
name: roportaj-video
description: Röportaj, müşteri/hasta yorumu (testimonial), konuşan kafa videosu: HDR→SDR renk, konuşma hızlandırma, B-roll, öncesi/sonrası karşılaştırma, hassas bölge bulanıklaştırma, başka dilde konuşmaya altyazı, logo ve kapaklar. "Müşteri yorumu", "hasta videosu", "röportaj kurgusu", "before/after" denince kullan.
license: Proprietary. © 2026 Vinci Studio. Tüm hakları saklıdır. Bkz. LICENSE.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, WebFetch, WebSearch
metadata:
  sahip: Vinci Studio
  surum: "1.0.0"
---

# Röportaj ve müşteri yorumu

## Akış
1. **Ham malzemeyi tanı:** her klibin süresi, yönü (dikey çekim 90° yan kayıtlı olabilir), HDR'ı ve dili. `transkript` ile hepsini yazıya dök; dili Whisper söyler. Müşterinin "Türkçe" sandığı konuşma İspanyolca çıkabilir. Ortam sesindeki halüsinasyon metinleri altyazıya girmez.
2. **HDR → SDR:** `scripts/hdr2sdr.sh girdi.mov cikti.mp4`. iPhone HLG'si çevrilmezse renk soluk kalır ve HyperFrames üst katmanları düşer. Önce/sonra karesine bak.
3. **Konuşma kurgusu:** en güçlü 3–5 cümle. Sırası: duygu → sonuç → tavsiye. Cümleleri ayrı dosyalara kes, concat demuxer ile birleştir (aynı girdiyi tek filter_complex içinde birden çok kullanma).
4. **Hız:** konuşma yavaşsa 1,15–1,25x (`setpts=PTS/K,atempo=K`). 1,5x fazla bulunur. Tek bir `K` sabiti tut; bütün B-roll'u aynı K ile hazırla.
5. **B-roll ve öncesi/sonrası:** aynı açıdan çekilmiş çiftleri eşle ve "Before / After" etiketi koy. İçeriğe bağlı ok ve işaretler kullan (`hyperframes-registry`: hw-arrow, hw-callout-circle, hw-underline). Ok olan karta Ken Burns verme.
6. **Gizlilik:** yalnız gereken bölgeyi bulanıklaştır (`gblur` + maske ya da kırpılmış bölge). Fazla bulanık "kapatmışsınız" diye geri döner; eksik bulanık yayından kalkar. Her planda karede kontrol et. Hasta/müşteri adını yazıya geçirme.
7. **Altyazı:** konuşmanın dilinde ya da istenen dilde. Zamanı Whisper kelime başlangıcına değil, sesin enerji başlangıcına oturt. Font: kalın sans + italik serif vurgu.
8. **Müzik:** sakin fon (`ses-muzik/scripts/fon_muzik.py`), konuşmanın 14–15 dB altında.
9. **Kapaklar:** giriş kapağı ve kapanışta logo. Logo müşterinin dosyasından; düşük çözünürlüklü JPEG ise alfa temizlenip 3x büyütülür, vektör istenir.
10. **Çıktının sesini yazıya dök** ve cümlelerin sırasını doğrula. Sonra önizleme ve onay.

## Uyarılar
- Sağlık reklamlarında (önce/sonra, hasta yorumu) ülkenin mevzuatı kısıtlayıcı olabilir. Yayından önce müşteriye hatırlat ve hastanın yazılı onayını iste.
- Kaynak sloganlar başka bir markaya ait olabilir; müşterinin kendi sloganını kullan.
