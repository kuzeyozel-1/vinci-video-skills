---
name: reels-video
description: Tanıtım ve reklam reels'i, uygulama/ürün tanıtımı, kodla animasyon (HyperFrames + GSAP): kart animasyonları, sayaçlar, telefon ekranı maketi, para yağmuru, meme klibi ve ses efektiyle eğlenceli tanıtım. "Reels yap", "tanıtım videosu", "uygulama videosu", "reklam reels" denince kullan.
license: Proprietary. © 2026 Vinci Studio. Tüm hakları saklıdır. Bkz. LICENSE.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, WebFetch, WebSearch
metadata:
  sahip: Vinci Studio
  surum: "1.0.0"
---

# Tanıtım reels'i (HyperFrames)

Önce `hyperframes` ve `hyperframes-cli` skill'lerini oku. Proje: `npx hyperframes init <ad>` → kökte `index.html`, 1080×1920, 30 fps.
Döngü: düzenle → `npm run check` → `npx hyperframes snapshot --at 1,5,9` → kareye bak → `npx hyperframes render`.

## Yapı (20–45 sn)
1. **Kanca (0–2 sn):** sorun ya da şaşırtıcı iddia; büyük yazı ve vuruş sesi (`bass-drop`, fade-out ile).
2. **Çözüm:** ürün veya uygulama ekranı, telefon maketi içinde kayan ekran kaydı.
3. **3 fayda:** kartlar sırayla girer (whoosh), sayılar yuvarlanarak artar (yazar kasa sesi).
4. **Kanıt:** yorum, puan, rakam.
5. **CTA:** logo + tek eylem ("Linke tıkla" yerine yoruma "LİNK" yazdırma çağrısı daha iyi çalışır). CTA soldurulmaz.

## Ses
- Efekt: Myinstants (`https://www.myinstants.com/en/search/?name=<kelime>`; sayfadaki `/media/sounds/*.mp3` yollarını `grep -o` ile çıkar, `curl -A "Mozilla/5.0"` ile indir). İyi çalışanlar: `2-whoosh`, `coin-drop`, `cash-register`, `anime-pop`, `bass-drop-vine-boom`. Türkiye'de bilinenler: `eyvah-tufan-eyvah`, `vay-anam-babam-be`, `bruh`. Küfürlü olanları kullanma.
- Müzik: Mixkit (atıf istemez, ticari kullanım serbest; `mixkit.co/free-stock-music/<tür>/` sayfasındaki `data-audio-player-preview-url-value` mp3'leri) ya da `ses-muzik/scripts/fon_muzik.py`.
- Klip sesi: `ffmpeg -vn` ile mp3'e ayır, `<audio>` olarak ekle, `<video muted>`.

## HyperFrames notları
- Her `<audio>` öğesinin bir id'si olmalı ve track-index değerleri benzersiz olmalı: `<audio id src data-start data-duration data-track-index data-volume data-fade-out>`.
- Sahneler `.clip.scene` + `data-start/duration`. Süre uzatırken sahneyi, `tl.set` listesini ve ses zamanlarını birlikte kaydır.
- `gsap.defaults({immediateRender:false})`, başlangıç durumları `tl.set(...,0)` ile timeline içinde.
- Koyu zeminde logo kaybolursa beyaz karo içine koy. Kontrast denetimi: yeşil `#5EE39A`, mavi `#8CC0FB`.
- Hareketli başlık sabit görselin (telefonun) üstüne kayarken telefon başlığı örtmesin.
- Render ön planda ya da `run_in_background` ile; önce `--start/--end` 3 sn test.
