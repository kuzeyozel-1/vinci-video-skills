---
name: seslendirme
description: Kişinin kendi sesiyle seslendirme: okuma metni hazırlama, tek seferde kayıt, replikleri Whisper kelime zamanından kesme, temizleme, seviye ayarı ve videoda yayın/müzik sesini kısma (ducking). Çok dilli seslendirme seçenekleri. "Benim sesimle", "seslendirme", "voiceover", "VO" denince kullan.
license: Proprietary. © 2026 Vinci Studio. Tüm hakları saklıdır. Bkz. LICENSE.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, WebFetch, WebSearch
metadata:
  sahip: Vinci Studio
  surum: "1.0.0"
---

# Seslendirme (gerçek ses önce)

Ses klonu kişiye benzemedi ve reddedildi. **Varsayılan, kişinin kendi kaydı.** Yapay ses yalnız istenirse ve onayla kullanılır.

## Akış
1. **Okuma metni yaz:** `sesler/<kisi>/okuma-metni.md`. Her replik ayrı satırda, numaralı olsun. Klipte kullanılacak cümlelerin yanında genel replikler de bulunsun: giriş ("Selam ben ..."), tepki ("Ne alaka ya?", "Hayır hayır hayır"), soru ("Sence sonu nasıl bitti? Yorumlara yaz"), kapanış ("Abone olmayı unutma"). Kanalın imza cümlesini de ekle.
2. **Kayıt:** kişi telefonun Sesli Notlar uygulamasıyla, sessiz odada, ağza 20 cm uzaklıktan, her cümle arasında 1 sn bekleyerek kaydeder. Dosyanın adını söylemesi yeterli: `vinci-video/scripts/dosya_bul.py`.
3. **Yazıya dök:** `transkript` → `transkript/kayit.json`.
4. **Repliği bul:** `python3 scripts/bul.py transkript/kayit.json "ne alaka ya"` → başlangıç ve bitiş. Tüm cümleler için `--liste`.
5. **Kes:** `scripts/kes.sh kayit.m4a 11.80 12.82 sesler/vo/ne-alaka.wav`. Gürültüyü bastırır, fade ve -16 LUFS uygular; sessiz çıkarsa uyarır.
6. **Yerleştir:**
   - `shorts-klip`: iş dosyasında `"seslendirme": [{"an": 0.0, "dosya": "sesler/vo/giris.wav", "guc": 1.6}]`. Yayın sesi konuşurken otomatik kısılır (sidechain).
   - `marka-filmi`: `efektler` listesine ekle.
   - HyperFrames: `<audio>` ile; müziğin `data-volume` değerini konuşma boyunca düşür.
7. **Doğrula:** çıktının sesini Whisper ile dinle ve replikler duyuluyor mu kontrol et.

## Kayıt bankası
Her kayıttan çıkan iyi replikleri `sesler/<kisi>/replikler.md` dosyasına yaz (metin + dosya + süre). Aynı tepki cümlesi birçok klipte kullanılabilir.

## Çok dilli
- Kişi o dili konuşabiliyorsa kendi sesi en iyisidir. Metni hedef dilde yaz, telaffuz notu ekle.
- Ücretsiz yerel: `npx hyperframes tts` (Kokoro; Türkçe yok).
- Ücretli: HeyGen ses/klon ve dublaj, ElevenLabs. **Maliyeti söyle, onay al.** Klonda rakamları yazıyla yaz.
- Yapay ses kullanılan videoda platformun "yapay/değiştirilmiş içerik" işaretini aç. Gerçek ses için gerekmez.
