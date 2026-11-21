---
name: ai-video
description: Yapay zekâ ile video ve görüntü üretimi (Higgsfield, Seedance, Kling, Veo vb.): kredi kontrolü, tek üretimde tüm senaryo ve referanslar, ürün doğruluğu kontrolü, kapanışı kodla ekleme. "AI video", "yapay zekâ ile reklam", "Seedance", "Higgsfield" denince kullan.
license: Proprietary. © 2026 Vinci Studio. Tüm hakları saklıdır. Bkz. LICENSE.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, WebFetch, WebSearch
metadata:
  sahip: Vinci Studio
  surum: "1.0.0"
---

# Yapay zekâ ile video üretimi

**Her üretim kredi harcar. Maliyeti ve istemin son halini göster, açık onay al. Hata payı varsayma.**

## İşe yarayan yöntem
- **Tek üretim, tüm senaryo:** ürün doğruluğu gereken reklamda bütün sahne akışını tek isteme yaz ve gerçek ürün fotoğraflarını referans olarak ver (ör. Seedance 2.5 `omni_reference`, 25 sn, 1080p). Parçalı kare ve klip üretimi tutarsız ve "CGI gibi" çıktı.
- **Önce ucuz taslak:** 480p ya da kısa süreyle kompozisyonu dene, onay gelince tam çözünürlüğe geç (fiyat farkı büyük).
- **Referans:** gerçek stüdyo fotoğrafı. Model ürünü yeniden çizer; referanssız saat, logo ya da yazı tutmaz.
- **İstem dili:** olumlu yaz ("temiz, pürüzsüz kol"). Yasak cümlelerini ("dövme yok") dinlemez. Aynı kişi, araba ve kıyafet her sahnede tekrar tarif edilir.

## Kontrol
- Her sahnede ürün detayını büyütüp kontrol et: kadran, logo, yazı. Bazı modeller başka bir markanın logosunu ekliyor; o modeli kullanma.
- Arka plandaki tabelalarda anlamsız yazı çıkabilir. Kısa kalıyorsa kabul et, değilse kırp.
- Kapanış yazısı, URL ve logo modelde üretilmez; HyperFrames'te kodla eklenir (bedava ve kusursuz).
- Müzik sonradan eklenir (`ses-muzik`), ritim girişi filmin kilit sahnesine oturtulur.

## Kayıt
Her üretimin iş kimliğini, istemini, maliyetini ve sonucunu `isler/uretim-gunlugu.md` dosyasına yaz. Tekrar üretim gerekirse oradan devam et.
