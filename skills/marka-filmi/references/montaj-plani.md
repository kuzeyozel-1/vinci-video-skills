# montaj.py plan dosyası

© 2026 Vinci Studio. Tüm hakları saklıdır.

```json
{
  "cikis": "cikti/klinik-film-v1.mp4",
  "boyut": [1080, 1920],
  "fps": 30,
  "renk": "klinik-soguk",
  "gren": false,
  "zoom": [1.0, 1.06],
  "plan_sesi": 0.4,
  "lufs": -14,
  "planlar": [
    {"dosya": "ham/A001.mov", "bas": 3.2, "son": 4.6, "zoom": [1.0, 1.1], "odak": [0.5, 0.4]},
    {"dosya": "ham/A004.mov", "bas": 10.0, "son": 12.4, "hiz": 0.5},
    {"dosya": "ham/A009.mov", "bas": 1.0, "son": 3.5, "zoom": [1.0, 1.0], "renk": "dogal", "ses": 0.8},
    {"siyah": 0.4}
  ],
  "son_kart": "logo/render/logo-outro.mp4",
  "muzik": {"dosya": "sesler/muzik.wav", "bas": 12.5, "ses": 0.8, "fade_in": 0.5, "fade_out": 2.0},
  "efektler": [
    {"dosya": "sesler/foley-tik.wav", "an": 1.38, "ses": 0.9},
    {"dosya": "sesler/seslendirme-01.wav", "an": 21.0, "ses": 1.2}
  ]
}
```

| Alan | Anlamı |
|---|---|
| `boyut` | Çıkış: 9:16 için `[1080,1920]`, 16:9 için `[1920,1080]`, kare için `[1080,1080]`. Kaynak "cover" ile doldurulur. |
| `renk` | `renk.py` ön ayarı. Planda `"renk"` ile ezilebilir, `null` verilirse dokunulmaz. |
| `gren` | Hafif film greni. Lüks ve gece işlerinde güzel durur. |
| `zoom` | `[başlangıç, bitiş]` ölçek. Planın süresi boyunca yavaş itiş. `[1,1]` sabit plan demek. |
| `odak` | Kırpmanın merkezi `[x, y]` (0–1). Dikey kırpmada yüzü ya da detayı içeride tut. |
| `hiz` | 0.5 = yarı hız. 120 fps kaynakta pürüzsüz olur, 30 fps kaynakta takılır. Ses `atempo` ile uyarlanır. |
| `plan_sesi` / `ses` | Çekim sesinin seviyesi (0 = sessiz). Foley gibi çalışır. |
| `siyah` | Saniye cinsinden siyah ara. |
| `son_kart` | Sona eklenen hazır video (logo kapanışı). Kendi sesi varsa korunur. |
| `muzik.bas` | Müziğin kaçıncı saniyesinden başlanacağı. En güçlü vurguyu filmdeki doğru ana getirmek için kaydır. |
| `efektler` | Film zamanına göre yerleştirilen sesler: foley, seslendirme, vuruş. |

Çıktıda yazan "kesimler" listesi her planın bittiği saniyedir. Efektleri ve müziği bunlara göre yerleştir.
`--kontrol` her planın orta karesinden bir pano üretir (`-kontrol.jpg`). Kadraj, renk ve odak hatası oradan görülür.
