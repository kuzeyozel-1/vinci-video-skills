# Ses tasarımı: marka filmi

© 2026 Vinci Studio. Tüm hakları saklıdır.

Sinematik filmi "pahalı" gösteren şey çoğu zaman görüntü değil, sestir. Katmanlar (alttan üste):

1. **Oda tonu / ortam** (-35 ile -30 dB): mekânın sessizliği. Kesimler arasındaki boşluğu doldurur, dijital sessizlik bırakmaz.
2. **Müzik** (konuşma yoksa ana ses, konuşma varsa 14–15 dB altında): minimal, darbeli, nabız gibi. Giriş 0,5 sn fade in, son 2 sn çözülme.
3. **Foley** (kesimlerle senkron): metal tıkırtısı, eldiven gerilmesi, lamba "klik", kapı, adım, nefes, kumaş. Plan sesi temizse onu kullan (`plan_sesi`). Değilse ayrı kayıttan `efektler` ile yerleştir.
4. **Vuruşlar / geçiş sesleri** (az kullanılır): whoosh, sub-boom ve riser, yalnızca 2–3 kritik anda (açılış, kahraman, logo).
5. **Söz** (isteğe bağlı): tek cümle seslendirme ya da sahnedeki gerçek konuşma ("Hello, ... Bucharest" gibi telefon sesi). Varsa her şey ona göre kısılır.

## Kayıt
- **Foley:** sessiz odada, mikrofonu kaynağa 15–30 cm yakın tut. Her sesten 5–10 tekrar al. Dosya adı ne olduğunu söylesin (`foley-makas-01.wav`).
- **Seslendirme:** `seslendirme` skill'ini kullan. Sakin, alçak ve yakın ses tonu; "fısıltıya yakın güven" tonu bu türde iyi çalışır.
- **Oda tonu:** her mekânda 30 sn, kimse konuşmadan.

## Yerleştirme
- Kesim anlarını `montaj.py` çıktısındaki "kesimler" listesinden al. Foley'i kesimden 20–40 ms ÖNCE başlat; ses görüntüden biraz önce gelince kesim daha sert hissedilir.
- Müziği `vurus.py` vurgularına göre kaydır (`muzik.bas`): en güçlü vurgu, kahraman planının ya da logonun girişine düşsün.
- Son karışım -14 LUFS (sosyal) ya da -16 LUFS (web, TV yakını). `montaj.py` `lufs` alanıyla ayarlanır.

## Telifsiz kaynaklar
`ses-muzik` skill'inde: Mixkit, sentez efektler (`efektler.py`), sentez fon müziği (`fon_muzik.py`), Myinstants (yalnız eğlence işlerinde).
