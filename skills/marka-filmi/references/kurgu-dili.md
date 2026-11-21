# Kurgu dili: marka filmi

© 2026 Vinci Studio. Tüm hakları saklıdır.

## Ritim
- Plan süresi: detay planı 0,8–1,5 sn, insan planı 1,5–2,5 sn, kahraman planı 2–3 sn. Film ilerledikçe hızlan, kahramanda nefes al, kapanışta yavaşla.
- Kesimleri müzik vuruşuna ya da vuruşun yarısına oturt (`vurus.py`). Her 4 kesimden birini vuruştan biraz önce yap ki film makine gibi durmasın.
- Hareketten harekete kes: el hareketi bir planda başlar, sonraki planda biter.

## Geçişler
- %90 düz kesim. Efektli geçiş en fazla 2 kez kullanılır.
- **Çerçeve içinde çerçeve:** yeni plan küçük bir pencere olarak açılıp büyür (referans filmde 16. sn). Hyperframes'te yapılır.
- **Işık patlaması / flare geçişi:** lamba ya da güneşten beyaza, oradan yeni plana.
- **Siyaha kesme:** bölüm sonu ve logo öncesi.

## Tipografi
- İnce ya da orta kalınlıkta, geniş harf aralıklı sans (Montserrat 300–500, büyük harf). Lüks işlerde italik serif vurgusu (Playfair Display italic).
- Yazı ekranda en az 1,2 sn kalır, harf harf değil kelime kelime ya da toptan belirir.
- Beyaz yazının arkasına yumuşak gölge koy; parlak planda kaybolmasın.
- Slogan üç vuruşlu olur: "Focus. Control. Precision." Markanın kendi sloganını kullan, uydurma.

## Logo kapanışı
- Siyah zemin, beyaz logo. Logo çizgiyle çizilerek ya da ışıkla açılarak belirir (Hyperframes: SVG `stroke-dashoffset` ya da maske).
- Altında küçük, soluk bir satır: şehir, web adresi ya da "Stay tuned".
- Toplam 2–3 sn, son 0,3 sn sabit kalır.

## Renk
- Bütün filmde tek ön ayar kullan (`renk.py`). Dış mekân planları gün ışığı olduğu için doğal olarak daha sıcak kalır; bu kontrast istenen bir şeydir.
- Ten rengi kontrolü: kahraman planında cilt griye ya da turuncuya kaçıyorsa o plana `"renk": "dogal"` ver.
