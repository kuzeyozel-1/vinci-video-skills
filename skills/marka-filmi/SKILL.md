---
name: marka-filmi
description: Profesyonel çekim ve ses kayıtlarından sinematik marka filmi (klinik, diş/estetik, ürün, lüks, restoran, mekân, kurumsal). Yakın plan detay, kahraman planı, ses tasarımı (foley + müzik), renk ön ayarları, ritme oturan kesim ve siyah zeminde logo kapanışı. Çekim listesi ve ses kayıt rehberi de içerir. "Marka filmi", "sinematik reels", "tanıtım filmi", "klinik videosu", "çekimden kurgu" denince kullan.
license: Proprietary. © 2026 Vinci Studio. Tüm hakları saklıdır. Bkz. LICENSE.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, WebFetch, WebSearch
metadata:
  sahip: Vinci Studio
  surum: "1.0.0"
---

# Marka filmi (sinematik, 9:16 ya da 16:9)

Hedef görünüm: az söz, çok his. Karanlık zeminde parlayan detaylar, sığ alan derinliği, yavaş içeri itiş, kesimler sesle
birlikte vurur ve film siyahta, sade bir logo animasyonuyla biter. Referans türü: diş ve estetik kliniklerinin
"Focus. Control. Precision." tarzı filmleri, lüks saat ve ürün filmleri.

`PY=~/.vinci-video/.venv/bin/python`. Dosya adı söylenirse `vinci-video/scripts/dosya_bul.py` ile bul.

## Yapı (30 sn için şablon)

| Bölüm | Süre | Ne var | Ses |
|---|---|---|---|
| 1. Soğuk açılış | 0–4 sn | Makro detay: alet, el, ürün, ışık. İlk kare en çarpıcısı. | Tek bir foley vuruşu (metal tıkırtısı, nefes) + müziğin girişi |
| 2. Hazırlık / süreç | 4–12 sn | Eldiven takma, lamba açılışı, ekipman, ekran. Plan başına 1–2 sn. | Foley'ler kesimlerle senkron |
| 3. İnsan / kahraman | 12–20 sn | Doktor veya usta: alt açı, göz teması, maske, odak. 1–2 yavaş plan. | Müzik yükselir |
| 4. Sonuç / yaşam | 20–25 sn | Dış mekân, mutlu müşteri, bina, ürünün kullanımda hali. Gün ışığı kontrastı. | İsteğe bağlı tek cümle seslendirme ya da telefon sesi |
| 5. Kapanış | 25–30 sn | Siyah zemin, beyaz logo animasyonu, kısa slogan ya da "STAY TUNED" | Müzik çözülür, son vuruş |

Ayrıntılı çekim listesi ve kamera ayarları için `references/cekim-rehberi.md`. Ses kaydı ve tasarımı için `references/ses-tasarimi.md`.
Kurgu ritmi, geçişler ve tipografi için `references/kurgu-dili.md`.

## İş akışı

1. **Brif:** marka, his (soğuk/kesin, sıcak/lüks, enerjik), süre, oran (9:16 Reels, 16:9 web), dil ve slogan. Kullanıcıya en fazla 3 kısa soru sor.
2. **Çekim öncesi** (çekim henüz yapılmadıysa): `references/cekim-rehberi.md`'den markaya özel çekim listesi çıkar ve kullanıcıya ver.
3. **Ham malzemeyi tara:**
   - Tüm klipleri listele: süre, çözünürlük, fps, HDR mi?
   - HDR olanları `roportaj-video/scripts/hdr2sdr.sh` ile çevir.
   - Her klipten kare al ve bak. Kullanılabilir anları `isler/secim.md` dosyasına not et: dosya, saniye ve neden.
   - Konuşma varsa `transkript` ile yazıya dök.
4. **Müzik + ritim:** müziği seç (`ses-muzik`). `$PY scripts/vurus.py muzik.wav --json isler/vurus.json` → BPM ve vurgular. Kesimleri vuruşlara yasla.
5. **Plan dosyası:** `isler/film.json` (alanlar `references/montaj-plani.md`). Renk ön ayarı seç (`python3 scripts/renk.py --liste`). Önce tek bir planı `renk.py ... --kare 1` ile dene, önce/sonra karesini göster.
6. **Montaj:** `python3 scripts/montaj.py isler/film.json --kontrol` → `cikti/<ad>.mp4` + `-kontrol.jpg` (her planın orta karesi).
7. **Logo kapanışı:** Hyperframes'te (`hyperframes-registry` → `logo-outro` bloğu ya da kodla). Siyah zemin, beyaz logo, 2–3 sn. Render'ı plan dosyasında `son_kart` olarak ekle. Logoyu asla yeniden çizme; müşterinin dosyasını kullan. PNG düşük çözünürlüklüyse vektör iste.
8. **Kalite kapısı** (`vinci-video`), sonra önizlemeyi kullanıcıya göster. Onay gelmeden müşteriye gönderme.

## Kısa kurallar
- **Yazı az olur:** filmde en fazla 2–3 yazı (slogan, marka, CTA). Altyazı gerekiyorsa sade, ince ve alt-orta konumda.
- **Her plan hareket eder:** varsayılan 1.00→1.06 yavaş itiş. Detay planlarında 1.00→1.10. Kahraman planında hareket yok ya da çok az.
- **Kesim sesle olur:** her kesim bir foley ya da müzik vuruşuna oturur. Sessiz kesim yapma.
- **Siyah nefes:** logodan önce 0,3–0,6 sn siyah (`{"siyah": 0.4}`).
- **Gerçek ses değerlidir:** çekimdeki alet sesleri, nefes ve ortam sesi filmi "pahalı" gösterir. `plan_sesi` ile koru (0.3–0.6).
- **Telif:** müziği lisanslı ya da telifsiz kaynaktan al. Instagram'da yayınlanacaksa trend müziği yayın anında IG kütüphanesinden eklemek de bir seçenek.
