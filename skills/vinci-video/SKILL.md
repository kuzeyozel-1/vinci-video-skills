---
name: vinci-video
description: Vinci Studio video kurgu sistemi, giriş noktası. Her video işinde önce bunu kullan (Shorts/Reels, marka filmi, reklam, röportaj/müşteri yorumu, anlatımlı 3D/motion video, çok dilli seslendirme, altyazı, müzik, AI video). Doğru alt skill'e yönlendirir, Vinci çalışma kurallarını, kalite kapısını ve birikmiş dersleri taşır. Kullanıcı yalnız dosya adı söylerse dosyayı kendisi bulur.
license: Proprietary. © 2026 Vinci Studio. Tüm hakları saklıdır. Bkz. LICENSE.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, WebFetch, WebSearch
metadata:
  sahip: Vinci Studio
  surum: "1.0.0"
---

# Vinci Video: giriş

Vinci Studio'nun video kurgu hattı. Amaç tek: **izleyeni ilk saniyede tutan, hatasız, markaya yakışan video.**
Ham çekimden teslime kadar her adım bu repodaki skill'lerle yapılır. Kurulum `install.sh` ile yapılır, ortak dosyalar
`~/.vinci-video/` altındadır: Python ortamı `.venv`, Whisper modeli `models`, fontlar `fontlar` ve hazır efektler `sesler`.

```bash
PY=~/.vinci-video/.venv/bin/python      # tüm Python scriptleri bununla çalışır
```

## 1. Dosya bulma: klasör sorma

Kullanıcı "röportaj videosunu al", "kayıt.m4a", "dünkü çekimler" gibi yalnız ad söyleyebilir. **Asla "hangi klasörde?" diye sorma.**
Önce bu skill klasöründeki bulucuyu çalıştır:

```bash
python3 <bu skill>/scripts/dosya_bul.py "roportaj" --tur video     # tür: video | ses | gorsel | hepsi
```

- Tek ve açık bir eşleşme çıkarsa doğrudan kullan.
- Birden çok eşleşme çıkarsa en yeni 2–3 tanesini kısaca göster: "şunu mu kastettin?"
- Hiç eşleşme yoksa adın başka bir parçasını dene. O da olmazsa dosyayı terminale sürükleyip bırakmasını iste.
- Sürükle-bırak yolları kaçışlı gelir (`Köknar\ Cd.\ 11.m4a`). Ters eğik çizgileri temizle, yolu tırnak içinde kullan.
- Sesli Notlar'dan gelen geçici dosyalar silinebilir. Bulur bulmaz proje klasörüne kopyala.

## 2. Varsayılan çıktı: Instagram Reels

Kullanıcı aksini söylemedikçe her iş **Reels** olarak üretilir:
- **Format:** 9:16, 1080×1920, 30 fps, H.264 + AAC, -14 LUFS. 16:9 sürümü yalnız istenirse ya da web/portföy için üretilir.
- **Süre:** 15–35 sn ideal, 90 sn üst sınır. İlk 1,5 sn kanca.
- **Reels güvenli alanı:** üstte ~220 px (hesap adı, ses etiketi), altta ~420 px (açıklama, butonlar), sağda ~140 px (beğeni/yorum sütunu) yazıdan boş kalır. Önemli her şey ortadaki 1080×1280 alanda olur.
- **Kapak karesi:** videonun içinden temiz, yazısız ve güçlü bir kare seç, `cikti/<ad>-kapak.jpg` olarak kaydet. Profil ızgarasında 3:4 kırpıldığı için ana konu ortada olmalı.
- **Açıklama metni:** ilk satır kanca. Sonra 1–2 cümle, CTA ("Randevu için DM", "Yorumlara yaz") ve en fazla 5 hashtag. Metni dosyaya yaz (`cikti/<ad>-aciklama.txt`), kullanıcı kopyalasın.
- **Müzik:** telifli trend şarkı videoya gömülmez; gerekiyorsa paylaşırken Instagram kütüphanesinden eklenir. Videoda foley, efekt ve telifsiz fon olur.
- Aynı içerikten TikTok ve YouTube Shorts kopyası istenirse aynı dosya kullanılabilir (Shorts için ≤60 sn tercih edilir).

## 3. Hangi skill?

| İstek | Skill |
|---|---|
| Yayın/oyun/podcast kesitinden dikey Shorts, TikTok, Reels (altyazılı, efektli) | `shorts-klip` |
| Profesyonel çekimden sinematik marka filmi (klinik, ürün, lüks, mekân) | `marka-filmi` |
| Anlatımlı video: 3D, motion graphics, açıklayıcı, İngilizce ya da çok dilli seslendirme | `anlatimli-video` |
| Tanıtım/reklam reels'i, uygulama tanıtımı, kodla animasyon (Hyperframes) | `reels-video` |
| Röportaj, müşteri/hasta yorumu, başka dilde konuşma + altyazı | `roportaj-video` |
| Konuşmayı yazıya dökme, altyazı (SRT), kelime zamanları | `transkript` |
| Kendi sesiyle seslendirme (kayıt, replik kesme, ducking) | `seslendirme` |
| Ses efekti, fon müziği, ses seviyesi, telifsiz kaynaklar | `ses-muzik` |
| Yapay zekâ ile video/görüntü üretimi (Seedance, Higgsfield vb.) | `ai-video` |

HyperFrames skill'leri (`hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `media-use` ve diğerleri) kurulumla
birlikte gelir. HTML/GSAP kompozisyonu yazmadan önce mutlaka onları oku.

## 4. Çalışma kuralları (Vinci)

1. **Kısa, sade Türkçe.** Jargon yok. İlerlemeyi tek satırla bildir, uzun sessiz bekleme yapma (model indirme, render vb.).
2. **Para/kredi harcayan her adımdan önce** maliyeti yaz ve tek net onay al: Higgsfield, ElevenLabs, HeyGen kredisi, ücretli müzik.
3. **Dışarı çıkan her iş önizlemeyle onaya gider:** yayınlama, müşteriye gönderme, push. Yeni bir formatın ilk örneği mutlaka önizlenir.
4. **Ucuz önizleme önce gelir.** Tam render'dan önce kontrol karesini, 3 saniyelik test render'ını ya da tek bir sahneyi göster.
5. **İstenenin dışına taşma.** Öneri varsa tek cümleyle sun, dayatma.
6. **Orijinali asla ezme.** Her sürüm yeni ad alır (`-v2`, `-v3`). Onaylı sürüm `cikti/` altında kalır.
7. **Müşteri ve kişi gizliliği:** hasta/müşteri adını metne yazma. Çıplaklık ve hassas bölgeleri bulanıklaştır, yayından önce karede kontrol et.

## 5. Kalite kapısı (teslimden önce hepsi ✓)

Ayrıntılı liste: `references/kalite-kontrol.md`. Özet:
- [ ] Ses ile görüntü senkron, konuşma ve altyazı aynı anda.
- [ ] Hiçbir yazı kenardan taşmıyor ya da kesilmiyor. Platform arayüzünün kapattığı alt ve sağ bölgelere yazı yok.
- [ ] Logo, emoji ve yazı üst üste binmiyor.
- [ ] İlk 1–2 saniyede kanca var: en çarpıcı an, soru ya da görsel şok.
- [ ] Ses seviyesi sosyal medya için -14 LUFS. Müzik konuşmanın 14–15 dB altında, konuşma her yerde anlaşılır.
- [ ] Renk doğru: HDR çevrilmiş, ten doğal, siyahlar boğulmamış.
- [ ] Çıktının sesi Whisper ile yazıya döküldü ve beklenen cümleler doğru yerde duyuluyor.
- [ ] Kontrol sayfası (kareler) açılıp gözle bakıldı.

## 6. Dersler

Geçmiş işlerden çıkan, tekrar edilmemesi gereken hatalar ve işe yarayan yöntemler: `references/dersler.md`.
Yeni bir ders öğrenince oraya bir satır ekle.

## 7. Proje düzeni (önerilen)

```
<proje>/
  ham/        çekimler (dokunulmaz)
  kaynak/     kesilmiş kaynak dilimler
  isler/      iş/plan JSON dosyaları, taramalar
  sesler/     projeye özel ses (seslendirme, foley)
  cikti/      render'lar + -kontrol.jpg
  yukle/      platforma yükleme kopyaları
```
