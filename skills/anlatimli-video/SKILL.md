---
name: anlatimli-video
description: Anlatımlı video: 3D sahneler, profesyonel motion graphics (Framer Motion/GSAP tarzı), açıklayıcı ve tanıtım videoları; İngilizce ya da çok dilli seslendirme ve altyazı ile her dil için ayrı render. "Anlatımlı", "explainer", "3D animasyon", "motion graphics", "İngilizce/çok dilli video", "ürün nasıl çalışır" denince kullan.
license: Proprietary. © 2026 Vinci Studio. Tüm hakları saklıdır. Bkz. LICENSE.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, WebFetch, WebSearch
metadata:
  sahip: Vinci Studio
  surum: "1.0.0"
---

# Anlatımlı video (3D + motion + çok dilli)

Araç: **HyperFrames** (HTML + GSAP + Three.js → MP4). Önce `hyperframes` skill'ini oku; 3D için `hyperframes/references/runtimes.md`
ve `path-tracing.md`, hareket dili için `motion.md`, hikâye için `story.md`/`storyboard.md`. Varsayılan çıktı Reels 9:16, istenirse 16:9 ikinci render.

## Akış
1. **Brif → metin.** Bir fikir, bir hedef kitle, bir eylem çağrısı. Reels için 60–90 kelime (~30 sn). Önce hedef dilde yaz; çeviri değil, yerelleştirme yap (deyimler, birimler, para).
   Kanca cümlesi soru ya da şaşırtıcı bir veridir. Metni kullanıcıya onaylat.
2. **Storyboard.** Her cümle bir sahne: `isler/storyboard.md` (sahne, süre, ekranda ne var, hangi hareket). 3–5 sn'lik sahneler.
3. **Seslendirme** (her dil için ayrı dosya, `sesler/vo-<dil>.wav`):
   - Kullanıcının kendi sesi (en iyisi; Türkçe ve konuşabildiği diller): `seslendirme` skill'i.
   - Yerel ve ücretsiz: `npx hyperframes tts` (Kokoro; İngilizce, İspanyolca, Fransızca, İtalyanca, Portekizce, Japonca, Çince, Hintçe; **Türkçe yok**).
   - HeyGen sesleri ve klonlama (`media-use`), ElevenLabs: **ücretli, önce maliyeti söyle, onay al.**
   - Rakam, kısaltma ve marka adlarını yazıyla ver ("GTA six"), yoksa yanlış okunur. Çıktıyı Whisper ile dinle.
4. **Zamanlama.** `transkript` ile VO'nun kelime zamanlarını al. Sahne geçişleri cümle sonlarına, vurgu animasyonları vurgulu kelimelere oturur.
5. **Kompozisyon.** Tek kompozisyon, dil metinleri ayrı dosyada (`dil/tr.json`, `dil/en.json`, ...). Yazılar ve VO yolu dile göre seçilir, böylece aynı kurgu her dilde render edilir.
   Metin uzunluğu dile göre değişir (Almanca ~%30 uzun). Her dilde taşma kontrolü yap.
6. **Altyazı.** Her dil için yanmış (burned-in) altyazı, kelime kelime vurgulu (`hyperframes/references/captions.md`). Ayrıca `.srt` ver (`transkript --srt`).
7. **Render + kontrol.** Her dil için `npx hyperframes check`, `snapshot` ve render. Çıktılar `cikti/<ad>-<dil>.mp4`. Her dilin sesini Whisper ile doğrula.

## 3D
- Three.js sahnesi HyperFrames içinde deterministik olmalı: `Math.random`, `Date.now` ve ağdan yükleme yok. Kamera ve nesne hareketi GSAP timeline'a bağlanır.
- Model: müşterinin GLB/GLTF dosyası. Yoksa Higgsfield `generate_3d` ile görselden GLB üretilebilir (**kredili, onay al**) ya da basit geometri ve malzemeyle stilize anlatım yapılır.
- Görünüm: koyu zemin, tek ana ışık + kenar ışığı, yavaş orbit, sığ alan derinliği hissi. Ürün döner, etiketler çizgiyle bağlanır.
- Ağır sahnelerde önce 3 sn'lik test render'ı al.

## Motion dili (Framer Motion tarzı)
- Yaylı (spring) girişler: `back.out(1.4)`, `expo.out`. Hepsi aynı anda değil, 40–80 ms aralıkla (stagger).
- Kart, ikon ve sayı animasyonları: sayaçlar yuvarlanarak artar, grafikler çizilerek gelir.
- Her sahnede tek bir odak. Geri kalan her şey soluk kalır ya da bulanıklaşır.
- Geçişler: maske ile silme, ölçekle içeri dalma, ortak öğe geçişi (bir sahnedeki kart sonraki sahnede büyür).
- Hazır parça önce: `hyperframes-registry` (başlık, alt yazı bandı, ok, daire, alt çizgi, kamera hareketi, logo kapanışı).

## Kurallar
- Yazı az, ses çok: ekranda en fazla 6–8 kelime olsun.
- Marka renkleri ve fontu müşterinin dosyasından alınır. Logo yeniden çizilmez.
- Kontrast kontrolü (`npm run check`) geçmeden render yapma.
