# Dersler: Vinci video işlerinden çıkanlar

© 2026 Vinci Studio. Tüm hakları saklıdır.

Her madde gerçek bir işte yaşandı. Yeni bir ders öğrenince ilgili başlığın altına tarihli bir satır ekle.

## Kurgu ve render
- **Aynı girdiyi tek filter_complex içinde birden çok kez kullanma** (`[1:a]` iki kez). Ses yanlış kaynaktan geldi ve kapanışta başka bir cümle duyuldu. Her parçayı ayrı dosyaya kes, concat demuxer ile birleştir, çıktının sesini Whisper ile doğrula. (Kas 2026)
- **ffmpeg'de `-ss/-to` mutlaka `-i`'den önce gelir**, özellikle `afade` kullanırken. Sonra konursa fade zamanları kayar ve dosya sessiz çıkar (-91 dB). (Kas 2026)
- **Altyazı zamanını kelime zamanına değil, sesin enerji (dB) başlangıcına göre ayarla.** Whisper kelime başlangıçları 100–300 ms erken ya da geç olabilir. (Kas 2026)
- **Hız değişimi:** konuşma 1,25x yapılınca bütün zamanlar (data-start, duration, media-start) eski/K olur. Tek bir `K` sabiti tut, B-roll'u da aynı hızla hazırla, müzik süresini yeniden hesapla. Müşteri 1,5x'i fazla hızlı buldu, 1,25x'te karar kılındı. (Kas 2026)
- **Uzun render'ı arka planda çalıştır** (`nohup` iptal olabiliyor). Önce `--start/--end` ile 3 saniyelik test yap. Render sırasında Chrome'daki canlı stüdyo önizlemesini kapat; CPU'yu yiyor. (Kas 2026)

## Hyperframes / GSAP
- `gsap.defaults({immediateRender:false})` kullan. Başlangıç durumlarını `tl.set(..., 0)` ile zaman çizelgesinin İÇİNDE ver. Kök timeline duraklatılmış olmalı, alt timeline'lar değil. (Kas 2026)
- Okların ve işaretlerin üstüne bindiği kart videolarına Ken Burns (kayan zoom) uygulama; oklar hedeften kayar. (Kas 2026)
- Sahne süresini uzatınca sahneyi, `tl.set` listesini ve ses zamanlarını birlikte kaydır. Regex ile toplu kaydırırken `back.out(1.7)` gibi sayıları bozma. (Kas 2026)
- Koyu zeminde düz renkli logo kaybolur. Beyaz yuvarlak ya da kare bir karo içine koy. WCAG kontrastı yeşil/mavi yazıyı yakalar: yeşil `#5EE39A`, mavi `#8CC0FB`. (Kas 2026)
- Para/jeton yağmurunda her öğenin sütunu ve başlangıcı farklı olmalı. Düz düşsün (`power2.in`), son 0,35 sn'de solsun. `i*137` gibi çapraz çizgi oluşturan desenden kaçın. (Kas 2026)

## Shorts (yayın kesiti)
- **Gece yayınlama.** Gece 01:00'de yüklenen klipler akışta neredeyse hiç test edilmedi (1–12 izlenme). Hazır klibi en yakın 12–15 ya da 19–22 aralığına koy, günde en fazla 3 yükleme yap, aralarını aç. (Kas 2026)
- **Toplu yükleme yapma.** Bir günde 11 yükleme günlük sınıra takıldı ve kliplerin çoğu hiç test edilmedi. (Kas 2026)
- **Başlıkta önce oyun/olay, sonra kişi gelir** ("GTA 6'da Hulk çıktı" ✓, "Yayıncı X şunu yaptı" ✗). Oyun-önce başlıklar 1.000+ izlenme aldı, kişi-önce başlıklar takıldı. (Kas 2026)
- **"İzlemeye devam" oranı %75 üstü iyidir, %60 altında kanca bozuktur.** %45 ve %25 ile kaydırılan kliplerin hepsi yavaş başlıyordu. (Kas 2026)
- **Sıradan an komik değildir.** "Komik değil" diye reddedilen klip tepkisiz bir andı. Ses patlaması, şaşkınlık ya da beklenmedik son ara. (Kas 2026)
- **Canlı yayında ses kayması:** YouTube canlıda görüntü ve ses ayrı listelerde gelir; parçaları sıra numarasına göre eşle (`canli.sh`). Yine de 4 sn kayma görüldü; ekrandaki altyazıyla doğrula. (Kas 2026)
- **Açıklamaya dış link koyma:** kanal doğrulanana kadar YouTube uyarı veriyor. "Kaynak: X (Kick yayını)" yazmak yeterli. (Kas 2026)
- **Sadece altyazılı yeniden kullanım "özgün olmayan içerik" sayılabilir** ve para kazanmayı engeller. Kendi sesinle Türkçe yorum, seslendirme ya da kurgu katkısı ekle. (Kas 2026)

## Ses
- **Klon ses kişiye benzemedi** (Chatterbox, yerel). Kanal sahibi "hiç benzemiyor" dedi. En iyisi kişinin kendi sesi: okuma metnini bir kez kaydet, replikleri kelime zamanından kes (`seslendirme`). (Kas 2026)
- Klon modeller "GTA 6" gibi rakam ve kısaltmaları yanlış okuyor ("Kıta ağaçta" diye duyuldu). Yapay ses şartsa rakamı yazıyla ver. (Kas 2026)
- Fon müziği "duyulmuyor" diye geri döndü: data-volume 0.12'den 0.35'e çıkarıldı (konuşmanın 14–15 dB altı). (Kas 2026)

## Renk
- iPhone klipleri HLG HDR olarak geliyor. ffmpeg ile SDR'a çevirip bt709 olarak etiketle; yoksa Hyperframes üst katmanları düşürür. (Kas 2026)

## Yapay zekâ ile üretim
- **Ürün doğruluğu gereken videoda tüm senaryoyu ve gerçek referans fotoğrafları TEK üretime ver** (Seedance 2.5, omni_reference). Parçalı kare ve klip üretimi tutarsız ve "CGI gibi" çıktı, kredi boşa gitti. (Kas 2026)
- Görüntü modelleri ürünü (saat kadranı, logo) yeniden çiziyor. Marketing Studio kadrana başka bir markanın logosunu ekledi. Her karede logo ve yazı kontrolü yap. (Kas 2026)
- Modeller "X yok" yasağını dinlemez. Olumlu yaz: "dövme yok" yerine "temiz, pürüzsüz kol". (Kas 2026)
- Kapanış yazısı ve URL'yi modele yazdırma. Hyperframes'te kodla ekle; bedava ve kusursuz olur. (Kas 2026)
- Kredi pahalı ve hata payı yok: istemin son halini göstermeden üretim başlatma. (Kas 2026)
