# kurgu.py iş dosyası

© 2026 Vinci Studio. Tüm hakları saklıdır.

```json
{
  "kaynak": "kaynak/ad.mp4",
  "yayinci": "ISHOWSPEED", "platform": "YOUTUBE",
  "kanca": "GTA 6'DA DİLENCİYE *YARDIM* ETME 💀", "kanca_sure": 3.0, "kanca_y": 1010, "kanca_boy": 92,
  "duzen": "bolunmus",
  "kamera": [0, 460, 390, 240], "kamera_oran": 0.4,
  "oyun": [390, 80, 1150, 1000],
  "gama": 1.15,
  "parcalar": [{"bas": 3.7, "son": 7.1}, {"bas": 9.6, "son": 12.0}, {"dosya": "memeler/bruh.mp4", "bas": 0, "son": 1.2}],
  "seslendirme": [{"an": 0.0, "dosya": "sesler/vo/giris.wav", "guc": 1.6}],
  "altyazi": [
    {"bas": 0.05, "son": 1.2, "metin": "BAK ŞİMDİ,"},
    {"bas": 11.5, "son": 13.7, "metin": "BURGERİ KAPIP KAÇIYOR", "aksiyon": true},
    {"bas": 14.0, "son": 15.1, "metin": "*NE?!*", "boy": 160}
  ],
  "vurgu": [
    {"an": 0.05, "ses": "pop", "zoom": 1.12, "sure": 0.5},
    {"an": 14.0, "ses": "boom", "zoom": 1.32, "sure": 0.7, "sarsinti": 26, "renk": [225, 30, 50], "flas": true, "rgb": 16},
    {"an": 15.6, "ses": "bruh", "emoji": "😂", "emoji_yer": [820, 420]}
  ],
  "bulanik": [{"bas": 2.0, "son": 4.5, "kutu": [800, 300, 200, 200]}],
  "filigran": "@kanaladi",
  "cikis": "cikti/ad.mp4"
}
```

| Alan | Anlamı |
|---|---|
| `duzen` | `bolunmus`: üstte kamera, altta oyun. `yigin`: üstte tam 16:9 oyun, altında kamera. `dikey`: kamerasız, oyunun dikey kesiti. `tam`: bulanık zemin üstünde 16:9. |
| `kamera` / `oyun` | Kaynaktaki kutular, **1920×1080'e göre** piksel `[x, y, w, h]`. Başka çözünürlükteki kaynak otomatik ölçeklenir. Oyun kutusu yayın logosunu ve HUD'u dışarıda bırakır. |
| `kamera_oran` | Bölünmüş düzende kameranın ekran yüksekliğindeki payı (0.4). |
| `parcalar` | Kaynaktan alınan dilimler. `dosya` verilirse araya giren klip (meme) olur. Birleşmelerde otomatik geçiş + whoosh. |
| `altyazi`, `vurgu` | Zamanlar **çıkış videosuna** göre (birleştirilmiş zaman). |
| `altyazi[].aksiyon` | Köşeli parantezli eylem yazısı: `[BURGERİ KAPIP KAÇIYOR]`. |
| `altyazi[].boy` / `parca_harf` | Yazı boyu ve akan parça başına harf sınırı (18). |
| `altyazi_hiza` | `alt`: altyazı birleşim çizgisinin altına iner, aksiyonu kapatmaz. |
| `vurgu` | `ses` (efekt adı), `zoom` + `sure`, `flas`, `rgb` (kromatik kayma px), `renk` (renkli ton), `sarsinti`, `kirmizi` (kenar parlaması), `emoji`. |
| `seslendirme` | Gerçek ses replikleri. Konuşurken yayın sesi sidechain ile kısılır. |
| `bulanik` | Sansür kutuları (kaynak koordinatı, çıkış zamanı). |
| `stil` | `pro` (varsayılan): kutulu kanca, akan Anton altyazı, bulanık geçiş, kromatik vuruş. `klasik`: sade. |
| `gama` | Karanlık gece sahnesini telefonda seçilir yapar (1.1–1.3). |
| `yayin_ses` | Kaynak sesinin seviyesi (1.0). |
| `filigran` | Sağ altta soluk kanal imzası. Boş bırakılırsa basılmaz. |

Hazır efektler (`~/.vinci-video/sesler`): `whoosh`, `boom`, `pop`, `ding`, `yanlis`, `cizik`, `bruh`. Projeye `sesler/<ad>.wav` koyarak yenisini ekleyebilirsin.
