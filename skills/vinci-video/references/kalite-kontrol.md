# Kalite kontrol listesi (Vinci)

© 2026 Vinci Studio. Tüm hakları saklıdır.

Bu liste her teslimden önce baştan sona uygulanır. "Check geçti" demek yetmez: kareye bak, sesi dinle ya da yazıya dök.

## Görüntü
- **Güvenli alan, 9:16 (1080×1920):** yazılar soldan ve sağdan en az 80 px içeride olmalı. Alttaki ~420 px'e önemli yazı koyma (Shorts/Reels arayüzü orayı kapatır). Sağ kenar butonların yeri.
- **Taşma:** tek kelime bile kenara değiyorsa küçült ya da satırı böl. Uzun Türkçe kelimelere dikkat et ("KAÇIRIYORLAR").
- **Çakışma:** yayın logosu, köşe sayaçları, platform filigranı, emoji ve başlık birbirine binmemeli. Kaynaktaki oyun ya da yayın arayüzünü kırp.
- **Emoji:** aynı emoji ekranda en fazla iki kez görünür. Emoji satırda tek başına kalmaz, önceki kelimeye yapışır.
- **Renk:** iPhone ve aynasız makine çekimleri çoğu zaman HLG HDR'dır. Önce SDR'a çevir (`roportaj-video/scripts/hdr2sdr.sh`), yoksa soluk görünür ve Hyperframes üst katmanları düşer.
- **Gece sahneleri:** telefonda seçilmiyorsa hafif gama ver (`gama: 1.15–1.3`).
- **Gizlilik:** çıplaklık ve hassas bölgeler bulanık, plaka ve yüz isteğe göre. Bulanığın konumunu her plan için karede kontrol et. Fazlasını değil, yalnız gerekeni kapat; müşteri "her şey kapanmış" diye geri çevirebilir.

## Ses
- **Senkron:** canlı yayın kaynaklarında ses birkaç saniye kayabilir (4 sn, hatta 92 sn görüldü). Ekrandaki altyazı ya da dudak hareketiyle Whisper kelime zamanını karşılaştır.
- **Doğru cümle doğru yerde:** çıktının sesini yazıya dök (`transkript`). Beklenen cümleler sırayla geçiyor mu, tekrar eden ("Hola" iki kez) ya da kayıp cümle var mı?
- **Seviye:** sosyal medya için -14 LUFS, true peak -1,5 dB. Seslendirme varken yayın/ortam sesi sidechain ile kısılır.
- **Müzik:** konuşmanın 14–15 dB altında olmalı. "Müzik duyulmuyor" geri bildirimi gelirse 22 dB fazla kısıktır. Şarkı içeren müzik Shorts gelirinin yarısını alır; mümkünse enstrümantal kullan.
- **Kesim yerleri:** her kesime 30–60 ms fade ver, tık sesi kalmasın.

## Kurgu
- **Kanca:** ilk kare en çarpıcı an olmalı. Ölü giriş, logo ya da "merhaba" ile başlama.
- **Tempo:** Shorts'ta her ~3 saniyede görsel değişim olmalı (zoom, kesme, yazı, efekt). Marka filminde plan süresi 1–2,5 sn, kesimler ritme oturur.
- **Süre:** Shorts için tatlı noktalar 13–20 sn ya da 50–60 sn. 30–45 sn ölü bölgedir. Marka filmi 25–35 sn.
- **Kapanış:** CTA'yı soldurma, kapanış kartı net okunur kalsın.

## Teslim
- **Dosya adı:** `<marka>-<konu>-<dil>-v<N>.mp4`. Eski sürümler silinmez.
- **Yükleme kopyası:** tarayıcıdan yükleme için 10 MB altı (`shorts-klip/scripts/yukle.sh`).
- **Önizleme:** kontrol sayfasını (`-kontrol.jpg`) ve videoyu kullanıcıya göster, onayı al. Ondan sonra yayınla ya da gönder.
