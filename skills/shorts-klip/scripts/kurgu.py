# © 2026 Vinci Studio. Tüm hakları saklıdır. Kullanım koşulları: repodaki LICENSE dosyası.
"""Klip kurgusu: iş dosyasından (isler/*.json) 1080x1920 Shorts üretir.

Kareler Python'da birleştirilir (yayıncı kamerası + oyun, kanca başlığı, zıplayan altyazılar,
yakınlaştırma vuruşları, geçiş flaşı); ses ffmpeg ile karıştırılır (yayın sesi + efektler).
Yazılar ölçülüp satıra bölündüğü için kenardan taşamaz; taşarsa iş durur.

Kullanım (proje klasöründe): ~/.vinci-video/.venv/bin/python <skill>/scripts/kurgu.py isler/ornek.json [--kontrol]
Yollar (kaynak, sesler, cikis) çalıştırılan klasöre göredir; font ve hazır efektler ~/.vinci-video'dan gelir.
"""
import itertools
import os
import json
import math
import subprocess
import sys
import tempfile
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

KOK = Path.cwd()
EV = Path(os.environ.get("VINCI_VIDEO_EV", Path.home() / ".vinci-video"))
W, H, FPS = 1080, 1920, 30
KENAR = 80  # yazılar için yan güvenli boşluk
TURUNCU = (255, 122, 26)
SARI = (255, 221, 0)


def bul(*adaylar: Path) -> Path:
    """Önce proje klasörü, sonra ~/.vinci-video: projeye özel dosya ortak olanı ezer."""
    for a in adaylar:
        if a.exists():
            return a
    raise FileNotFoundError(" | ".join(map(str, adaylar)))


MONT = str(bul(KOK / "fontlar/Montserrat.ttf", EV / "fontlar/Montserrat.ttf"))
ANTON = str(bul(KOK / "fontlar/Anton-Regular.ttf", EV / "fontlar/Anton-Regular.ttf"))
EMOJI = next((y for y in ["/System/Library/Fonts/Apple Color Emoji.ttc", "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"] if Path(y).exists()), None)


def buyuk(s: str) -> str:
    return s.replace("i", "İ").replace("ı", "I").upper()


@lru_cache(maxsize=8)
def font(yol: str, boy: int, agirlik: int | None = None):
    f = ImageFont.truetype(yol, boy)
    if agirlik:
        f.set_variation_by_axes([agirlik])
    return f


def emoji_mi(kelime: str) -> bool:
    return bool(kelime) and all(ord(c) > 0x2100 and not c.isalpha() for c in kelime.replace("*", ""))


def olc(d, kelime: str, f) -> float:
    k = kelime.replace("*", "")
    return f.size * 1.05 * len(k) if emoji_mi(k) else d.textlength(k, font=f)


def satir_genisligi(d, satir: str, f) -> float:
    kelimeler = satir.replace(NBSP, " ").split(" ")
    return sum(olc(d, k, f) for k in kelimeler) + d.textlength(" ", font=f) * (len(kelimeler) - 1)


NBSP = "\u00a0"


def yapistir(metin: str) -> list[str]:
    kelimeler = []
    for k in metin.split():
        if emoji_mi(k) and kelimeler:
            kelimeler[-1] += NBSP + k
        else:
            kelimeler.append(k)
    return kelimeler


def satirla(metin: str, f, genislik: int) -> list[str]:
    d = ImageDraw.Draw(Image.new("L", (1, 1)))
    satirlar, simdiki = [], ""
    for kelime in yapistir(metin):
        aday = f"{simdiki} {kelime}".strip()
        if satir_genisligi(d, aday, f) <= genislik:
            simdiki = aday
        else:
            if simdiki:
                satirlar.append(simdiki)
            simdiki = kelime
    if simdiki:
        satirlar.append(simdiki)
    for s in satirlar:
        if satir_genisligi(d, s, f) > genislik:
            raise ValueError(f"Tek kelime bile sığmıyor: {s!r}")
    return satirlar


def yazi_gorseli(metin: str, boy: int, renk=(255, 255, 255), vurgu=SARI, kontur=10, genislik=W - 2 * KENAR, yol=MONT, agirlik=900, buyut=True) -> Image.Image:
    """*yıldızlı* kelimeler vurgu renginde, emoji kelimeleri renkli emoji. Çıktı: ortalanmış, saydam zeminli RGBA."""
    f = font(yol, boy, agirlik)
    satirlar = satirla(buyuk(metin) if buyut else metin, f, genislik)
    d0 = ImageDraw.Draw(Image.new("L", (1, 1)))
    yuk = int(boy * 1.12)
    img = Image.new("RGBA", (genislik + 2 * kontur, yuk * len(satirlar) + 2 * kontur + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    bosluk = d0.textlength(" ", font=f)
    for i, s in enumerate(satirlar):
        parcalar = s.replace(NBSP, " ").split(" ")
        x = (img.width - satir_genisligi(d0, s, f)) / 2
        y = kontur + i * yuk
        for p in parcalar:
            vur = p.startswith("*") or p.endswith("*")
            p = p.replace("*", "")
            if emoji_mi(p):
                for c in p:
                    em = emoji_gorseli(c, int(boy * 0.95))
                    img.alpha_composite(em, (int(x), int(y + boy * 0.12)))
                    x += boy * 1.05
            else:
                d.text((x, y), p, font=f, fill=vurgu if vur else renk, stroke_width=kontur, stroke_fill=(0, 0, 0))
                x += d0.textlength(p, font=f)
            x += bosluk
    return img.crop(img.getbbox())


@lru_cache(maxsize=16)
def emoji_gorseli(e: str, boy: int = 150) -> Image.Image:
    if EMOJI is None:
        raise RuntimeError("Renkli emoji fontu yok (macOS Apple Color Emoji ya da Noto Color Emoji kur)")
    f = ImageFont.truetype(EMOJI, 160)
    img = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    ImageDraw.Draw(img).text((100, 100), e, font=f, embedded_color=True, anchor="mm")
    img = img.crop(img.getbbox())
    return img.resize((boy, int(boy * img.height / img.width)), Image.LANCZOS)


def golgeli(img: Image.Image, kayma: int = 9, bulan: int = 7) -> Image.Image:
    """Yazının altına yumuşak gölge; açık zeminde de okunur."""
    pay = kayma + bulan * 2
    out = Image.new("RGBA", (img.width + 2 * pay, img.height + 2 * pay), (0, 0, 0, 0))
    g = Image.new("RGBA", img.size, (0, 0, 0, 0))
    g.putalpha(img.split()[-1].point(lambda p: p * 200 // 255))
    out.alpha_composite(g, (pay, pay + kayma))
    out = out.filter(ImageFilter.GaussianBlur(bulan))
    out.alpha_composite(img, (pay, pay))
    return out


def kanca_kutusu(metin: str, boy: int) -> Image.Image:
    """Profesyonel Shorts kancası: beyaz yuvarlak kutu, siyah yazı, vurgu kelimesi kırmızı."""
    yazi = yazi_gorseli(metin, boy, renk=(10, 10, 10), vurgu=(226, 30, 40), kontur=0, genislik=W - 2 * KENAR - 60, yol=ANTON, agirlik=None)
    px, py = 34, 20
    kutu = Image.new("RGBA", (yazi.width + 2 * px, yazi.height + 2 * py), (0, 0, 0, 0))
    ImageDraw.Draw(kutu).rounded_rectangle([0, 0, kutu.width - 1, kutu.height - 1], radius=26, fill=(255, 255, 255, 255))
    kutu.alpha_composite(yazi, (px, py))
    return golgeli(kutu, 10, 10)


def kelime_parcalari(a: dict) -> list[tuple[float, float, str]]:
    """Altyazıyı 1-3 kelimelik parçalara böler; süre harf sayısına göre paylaştırılır (akan altyazı)."""
    if a.get("aksiyon"):
        return [(a["bas"], a["son"], a["metin"])]
    sinir = a.get("parca_harf", 18)

    def uzunluk(p):
        return sum(len(x.replace("*", "")) for x in p) + len(p) - 1

    # Önce noktalamadan (, ? ! .) böl; *çok kelimeli vurgu* tek birim sayılır, ortasından bölünmez.
    birimler, acik = [], False
    for k in yapistir(a["metin"]):
        soz = k.split(NBSP)[0].rstrip(",?!.")  # emoji yapışık olabilir
        if acik:
            birimler[-1].append(k)
        else:
            birimler.append([k])
        if not acik and soz.startswith("*") and not (len(soz) > 1 and soz.endswith("*")):
            acik = True
        elif acik and soz.endswith("*"):
            acik = False
    cumleler, simdiki = [], []
    for b in birimler:
        simdiki.append(b)
        if b[-1].split(NBSP)[0].rstrip("*")[-1:] in (",", "?", "!", "."):
            cumleler.append(simdiki)
            simdiki = []
    if simdiki:
        cumleler.append(simdiki)
    parcalar = []
    for c in cumleler:
        kelimeler = [k for b in c for k in b]
        if uzunluk(kelimeler) <= sinir:
            parcalar.append(kelimeler)
            continue
        # Uzun cümle: birim sınırlarından, en uzun parçayı en kısa yapan bölme (birim sayısı küçük, hepsi denenir).
        n = min(len(c), math.ceil(uzunluk(kelimeler) / sinir))
        en_iyi = None
        for kesim in itertools.combinations(range(1, len(c)), n - 1):
            sinirlar = (0, *kesim, len(c))
            pp = [[k for b in c[i:j] for k in b] for i, j in zip(sinirlar, sinirlar[1:])]
            skor = max(uzunluk(p) for p in pp)
            if en_iyi is None or skor < en_iyi[0]:
                en_iyi = (skor, pp)
        parcalar += en_iyi[1]
    # Çok kısa parçalar ("AL,") ekranda yanıp söner; sığıyorsa sonrakiyle birleşir.
    birlesik = []
    for p in parcalar:
        if birlesik and uzunluk(birlesik[-1] + p) <= 12:
            birlesik[-1] = birlesik[-1] + p
        else:
            birlesik.append(p)
    parcalar = birlesik
    agirlik = [max(3, sum(len(x.replace("*", "")) for x in p)) for p in parcalar]
    toplam, t, out = sum(agirlik), a["bas"], []
    for p, ag in zip(parcalar, agirlik):
        son = t + (a["son"] - a["bas"]) * ag / toplam
        # *vurgu* bir kelimeyi sarıyorsa parçalara bölünürken yıldızlar kelimeyle kalır.
        out.append((t, son, " ".join(p)))
        t = son
    return out


def rgb_kaydir(img: Image.Image, px: int) -> Image.Image:
    """Kromatik sapma: kırmızı sola, mavi sağa kayar (vuruş anı)."""
    if px < 1:
        return img
    a = np.asarray(img).copy()
    a[:, :-px, 0] = a[:, px:, 0]
    a[:, px:, 2] = a[:, :-px, 2]
    return Image.fromarray(a, img.mode)


def hareket_bulanik(img: Image.Image, guc: float) -> Image.Image:
    """Geçişte dikey hareket bulanıklığı + hafif yakınlaşma (whip/zoom geçiş)."""
    if guc < 0.05:
        return img
    z = 1 + 0.16 * guc
    w, h = img.size
    cw, ch = w / z, h / z
    img = img.crop(((w - cw) / 2, (h - ch) / 2, (w + cw) / 2, (h + ch) / 2)).resize((w, h), Image.BILINEAR)
    a = np.asarray(img).astype(np.float32)
    adim = int(70 * guc)
    if adim >= 4:
        acc = np.zeros_like(a)
        n = 0
        for dy in range(-adim, adim + 1, max(1, adim // 4)):
            acc += np.roll(a, dy, axis=0)
            n += 1
        a = acc / n
    return Image.fromarray(a.astype(np.uint8), img.mode)


def ease_out_back(x: float) -> float:
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def kaplama(img: Image.Image, kutu_w: int, kutu_h: int, odak=(0.5, 0.5)) -> Image.Image:
    """object-fit: cover."""
    s = max(kutu_w / img.width, kutu_h / img.height)
    # LANCZOS: kamera kutusu ~3x büyütülüyor; bilinear yumuşatıyordu.
    r = img.resize((math.ceil(img.width * s), math.ceil(img.height * s)), Image.LANCZOS)
    x = int((r.width - kutu_w) * odak[0])
    y = int((r.height - kutu_h) * odak[1])
    return r.crop((x, y, x + kutu_w, y + kutu_h))


def keskin(img: Image.Image, guc: int) -> Image.Image:
    """Büyütülen kaynağa hafif netlik (düşük bit hızlı yayın kayıtları telefonda yumuşak görünüyor)."""
    return img.filter(ImageFilter.UnsharpMask(radius=1.6, percent=guc, threshold=2))


def sesli(yol: Path, tmp: Path) -> str:
    """Sessiz meme klibine boş ses izi ekler; concat her parçada ses ister."""
    var = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", str(yol)], capture_output=True, text=True).stdout.strip()
    if var:
        return str(yol)
    out = tmp / f"sesli-{yol.stem}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(yol), "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-shortest", "-c:v", "copy", "-c:a", "aac", str(out)], check=True)
    return str(out)


def ham_hazirla(is_: dict, tmp: Path) -> tuple[Path, list[float], tuple[int, int]]:
    """Parçaları kesip birleştirir; birleşme anlarını (çıkış zamanı) döner."""
    kaynak = str(KOK / is_["kaynak"])
    parcalar = is_["parcalar"]
    girdiler, filtre, eklemler, t = [], [], [], 0.0
    for i, p in enumerate(parcalar):
        # Araya giren klip (meme vb.) kendi dosyasından gelir; hepsi 1920x1080'e eşitlenir ki birleşsin.
        dosya = sesli(KOK / p["dosya"], tmp) if p.get("dosya") else kaynak
        girdiler += ["-ss", str(p["bas"]), "-to", str(p["son"]), "-i", dosya]
        # "gama": karanlık gece sahnelerini telefonda seçilir yapmak için (1.0 = dokunma).
        eq = f"eq=gamma={is_['gama']}:saturation=1.1," if is_.get("gama") and not p.get("dosya") else ""
        filtre.append(f"[{i}:v]{eq}fps={FPS},scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,"
                      f"setpts=PTS-STARTPTS[v{i}];[{i}:a]aresample=48000,aformat=channel_layouts=stereo,asetpts=PTS-STARTPTS[a{i}]")
        t += p["son"] - p["bas"]
        eklemler.append(t)
    zincir = "".join(f"[v{i}][a{i}]" for i in range(len(parcalar)))
    filtre.append(f"{zincir}concat=n={len(parcalar)}:v=1:a=1[v][a]")
    ham = tmp / "ham.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *girdiler, "-filter_complex", ";".join(filtre), "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-c:a", "pcm_s16le", str(ham.with_suffix(".mov"))], check=True)
    ham = ham.with_suffix(".mov")
    w, h = map(int, subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", str(ham)],
                                   capture_output=True, text=True, check=True).stdout.strip().split(","))
    return ham, eklemler[:-1], (w, h)


def zoom_carpani(t: float, vurgular: list[dict]) -> float:
    z = 1.0
    for v in vurgular:
        if "zoom" not in v:
            continue
        sure = v.get("sure", 0.6)
        x = (t - v["an"]) / sure
        if 0 <= x <= 1:
            # Hızlı giriş, yumuşak çıkış.
            z = max(z, 1 + (v["zoom"] - 1) * (min(1, x / 0.15) if x < 0.15 else (1 - (x - 0.15) / 0.85) ** 2))
    return z


def zemin_bulanik(kare: Image.Image) -> Image.Image:
    return kaplama(kare.resize((kare.width // 6, kare.height // 6)), W // 6, H // 6).filter(ImageFilter.GaussianBlur(4)).resize((W, H), Image.BILINEAR)


def kare_kur(kare: Image.Image, t: float, is_: dict, sabit: dict, eklemler: list[float]) -> Image.Image:
    # Araya giren parçalar (dosya'lı) yayın düzenini değil tam ekran düzenini kullanır.
    duzen = next((p.get("duzen", "tam") for p, (b, e) in zip(is_["parcalar"], sabit["araliklar"]) if b <= t < e and p.get("dosya")), is_.get("duzen", "tam"))
    vurgular = is_.get("vurgu", [])
    z = zoom_carpani(t, vurgular)
    sx, sy = kare.width / 1920, kare.height / 1080  # iş dosyasındaki kutular 1920x1080'e göre yazılır

    def kutu(k):
        return (int(k[0] * sx), int(k[1] * sy), int((k[0] + k[2]) * sx), int((k[1] + k[3]) * sy))

    # Sansür: kaynak karede belirtilen kutular (çıkış zamanına göre) kalın buğuyla örtülür.
    for b in is_.get("bulanik", []):
        if b["bas"] <= t < b["son"]:
            k = kutu(b["kutu"])
            parca = kare.crop(k)
            kucuk = parca.resize((max(1, parca.width // 24), max(1, parca.height // 24)), Image.BILINEAR)
            kare = kare.copy()
            kare.paste(kucuk.resize(parca.size, Image.BILINEAR).filter(ImageFilter.GaussianBlur(18)), k[:2])
    oyun = kare.crop(kutu(is_["oyun"])) if is_.get("oyun") and duzen == is_.get("duzen") else kare
    if z > 1.001:
        ow, oh = oyun.size
        cw, ch = ow / z, oh / z
        oyun = oyun.crop(((ow - cw) / 2, (oh - ch) / 2, (ow + cw) / 2, (oh + ch) / 2))

    if duzen == "bolunmus":
        cam_h = sabit["cam_h"]
        tuval = Image.new("RGB", (W, H), (10, 8, 16))
        tuval.paste(keskin(kaplama(oyun, W, H - cam_h), 40), (0, cam_h))
        tuval.paste(keskin(kaplama(kare.crop(kutu(is_["kamera"])), W, cam_h, (0.5, 0.35)), 70), (0, 0))
        ImageDraw.Draw(tuval).rectangle([0, cam_h - 4, W, cam_h + 4], fill=TURUNCU)
        alt_y = cam_h
    elif duzen == "yigin":
        # Üstte tam genişlik 16:9 oyun (aksiyon kırpılmaz), altında yayıncı kamerası; zemin bulanık oyun.
        tuval = Image.blend(zemin_bulanik(oyun), Image.new("RGB", (W, H), (0, 0, 0)), 0.55)
        oy = sabit.get("yigin_y", 330)
        og = kaplama(oyun, W, int(W * 9 / 16))
        tuval.paste(og, (0, oy))
        cam_h = sabit["cam_h"]
        tuval.paste(kaplama(kare.crop(kutu(is_["kamera"])), W, cam_h, (0.5, 0.5)), (0, oy + og.height))
        ImageDraw.Draw(tuval).rectangle([0, oy + og.height - 4, W, oy + og.height + 4], fill=TURUNCU)
        alt_y = oy + og.height
        duzen = "bolunmus"  # altyazı birleşim çizgisine ortalansın
    elif duzen == "dikey":
        # Kamerasız kaynak: oyunun ortasından dikey kesit ekranın çoğunu doldurur, altyazı kesitin alt kısmında.
        tuval = Image.blend(zemin_bulanik(kare), Image.new("RGB", (W, H), (0, 0, 0)), 0.45)
        gh = is_.get("dikey_h", 1240)
        oy = (H - gh) // 2 - 80
        tuval.paste(kaplama(oyun, W, gh), (0, oy))
        alt_y = oy + gh - 330
    else:
        tuval = zemin_bulanik(kare)
        tuval = Image.blend(tuval, Image.new("RGB", (W, H), (0, 0, 0)), 0.45)
        og = kaplama(oyun, W, int(W * 9 / 16))
        oy = (H - og.height) // 2 - 60
        tuval.paste(og, (0, oy))
        alt_y = oy + og.height + 40
    # Sarsıntı (bağırma anları) ve kırmızı kenar parlaması; yazılar sarsılmasın diye yazılardan önce.
    for v in vurgular:
        x = t - v["an"]
        if v.get("sarsinti") and 0 <= x < v.get("sure", 0.6):
            g = v["sarsinti"] * (1 - x / v.get("sure", 0.6))
            rng = np.random.default_rng(int(t * FPS))
            dx, dy = (rng.uniform(-1, 1, 2) * g).astype(int)
            kaymis = Image.new("RGB", (W, H), (0, 0, 0))
            kaymis.paste(tuval.resize((int(W * 1.04), int(H * 1.04))), (int(-W * 0.02) + dx, int(-H * 0.02) + dy))
            tuval = kaymis
    pro = sabit["pro"]
    if pro:
        # Geçiş: birleşmenin iki yanında ~0,25 sn yakınlaşan hareket bulanıklığı (beyaz flaş yerine).
        for e in eklemler:
            d = t - e
            if -0.12 <= d < 0.14:
                tuval = hareket_bulanik(tuval, 1 - abs(d) / 0.14)
        # Vuruş: kromatik sapma + istenirse renkli ton (Live Speedy tarzı tepki boyası).
        for v in vurgular:
            x = t - v["an"]
            sure = v.get("sure", 0.6)
            if (v.get("flas") or v.get("rgb")) and 0 <= x < 0.35:
                tuval = rgb_kaydir(tuval, int(v.get("rgb", 14) * (1 - x / 0.35)))
            if v.get("renk") and 0 <= x < sure:
                ton = Image.new("RGB", (W, H), tuple(v["renk"]))
                tuval = Image.blend(tuval, ton, 0.38 * (1 - x / sure) if x > 0.1 else 0.38)
    tuval = tuval.convert("RGBA")
    for v in vurgular:
        x = t - v["an"]
        if v.get("kirmizi") and 0 <= x < v.get("sure", 0.6):
            tuval.alpha_composite(sabit["vinyet"].copy() if x < 0.05 else Image.blend(Image.new("RGBA", (W, H), (0, 0, 0, 0)), sabit["vinyet"], 1 - x / v.get("sure", 0.6)))

    # Geçiş flaşı: her birleşmede 0,18 sn beyaz parlama.
    for e in ([] if pro else eklemler):
        if 0 <= t - e < 0.18:
            a = int(200 * (1 - (t - e) / 0.18))
            tuval.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, a)))
    flas_sure = 0.08 if pro else 0.15
    for v in vurgular:
        if v.get("flas") and 0 <= t - v["an"] < flas_sure:
            tuval.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(170 * (1 - (t - v["an"]) / flas_sure)))))

    tuval.alpha_composite(sabit["ust_golge"])
    # Üst bilgi: yayıncı etiketi her zaman, kanca başlığı ilk saniyelerde zıplayarak.
    etiket = sabit["etiket"]
    tuval.alpha_composite(etiket, ((W - etiket.width) // 2, 70))
    kanca_son = is_.get("kanca_sure", 3.0)
    if t < kanca_son:
        x = min(1, t / (0.25 if pro else 0.35))
        s = max(0.05, ease_out_back(x))
        kg = sabit["kanca"]
        g = kg.resize((max(1, int(kg.width * s)), max(1, int(kg.height * s))), Image.BILINEAR)
        if t > kanca_son - 0.25:
            alfa = (kanca_son - t) / 0.25
            g.putalpha(g.split()[-1].point(lambda p: int(p * alfa)))
        tuval.alpha_composite(g, ((W - g.width) // 2, is_.get("kanca_y", 150) + (kg.height - g.height) // 2))

    # Altyazı: bölünmüş düzende iki görüntünün birleşim çizgisinde, tam düzende videonun altında.
    for bas, son, ag in sabit["altyazi"]:
        if bas <= t < son:
            x = min(1, (t - bas) / (0.1 if pro else 0.16))
            s = (0.6 + 0.4 * ease_out_back(x)) if pro else (0.7 + 0.3 * ease_out_back(x))
            g = ag.resize((max(1, int(ag.width * s)), max(1, int(ag.height * s))), Image.BILINEAR)
            # "alt": altyazı birleşim çizgisinin hemen altında başlar (oyundaki aksiyonu kapatmasın).
            if is_.get("altyazi_hiza") == "alt":
                y = alt_y + 14
            else:
                y = alt_y - g.height // 2 if duzen == "bolunmus" else alt_y
            tuval.alpha_composite(g, ((W - g.width) // 2, int(y)))

    for v in vurgular:
        if v.get("emoji") and 0 <= t - v["an"] < v.get("emoji_sure", 1.2):
            x = min(1, (t - v["an"]) / 0.2)
            em = emoji_gorseli(v["emoji"])
            s = ease_out_back(x)
            g = em.resize((max(1, int(em.width * s)), max(1, int(em.height * s))))
            ex, ey = v.get("emoji_yer", [W - 260, 420])
            tuval.alpha_composite(g, (ex, ey))

    tuval.alpha_composite(sabit["filigran"], (W - sabit["filigran"].width - 30, H - 470))
    return tuval.convert("RGB")


def ses_karistir(ham: Path, is_: dict, eklemler: list[float], cikis: Path, video: Path):
    efektler = [(e - 0.12, "whoosh", 0.8) for e in eklemler]
    efektler += [(v["an"], v["ses"], v.get("ses_gucu", 0.9)) for v in is_.get("vurgu", []) if v.get("ses")]
    girdiler = ["-i", str(video), "-i", str(ham)]
    filtre = [f"[1:a]aresample=48000,aformat=channel_layouts=stereo,volume={is_.get('yayin_ses', 1.0)}[y]"]
    etiketler = ["[y]"]
    for i, (an, ad, guc) in enumerate(efektler):
        yol = bul(KOK / "sesler" / f"{ad}.wav", EV / "sesler" / f"{ad}.wav")
        girdiler += ["-i", str(yol)]
        ms = max(0, int(an * 1000))
        filtre.append(f"[{i + 2}:a]aresample=48000,volume={guc},adelay={ms}|{ms}[e{i}]")
        etiketler.append(f"[e{i}]")
    # Seslendirme (gerçek ses): konuşurken yayın sesi kısılır (sidechain).
    sesler = is_.get("seslendirme", [])
    if sesler:
        n = len(girdiler) // 2
        sl = []
        for j, s in enumerate(sesler):
            girdiler += ["-i", str(KOK / s["dosya"])]
            ms = max(0, int(s["an"] * 1000))
            filtre.append(f"[{n + j}:a]aresample=48000,aformat=channel_layouts=stereo,volume={s.get('guc', 1.6)},adelay={ms}|{ms}[s{j}]")
            sl.append(f"[s{j}]")
        filtre.append(f"{''.join(sl)}amix=inputs={len(sl)}:normalize=0,asplit=2[vo][vk]")
        filtre.append(f"[y][vk]sidechaincompress=threshold=0.02:ratio=10:attack=15:release=350[yd]")
        etiketler[0] = "[yd]"
        etiketler.append("[vo]")
    filtre.append(f"{''.join(etiketler)}amix=inputs={len(etiketler)}:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *girdiler, "-filter_complex", ";".join(filtre), "-map", "0:v", "-map", "[a]",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(cikis)], check=True)


def kontrol_sayfasi(cikis: Path, is_: dict):
    """Her altyazının ortasından bir kare + güvenli alan çizgileri; gözle kontrol için."""
    anlar = [(a["bas"] + a["son"]) / 2 for a in is_.get("altyazi", [])][:9] or [1.0]
    kareler = []
    for an in anlar:
        p = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(an), "-i", str(cikis), "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True, check=True)
        import io
        k = Image.open(io.BytesIO(p.stdout)).convert("RGB")
        d = ImageDraw.Draw(k)
        d.line([(KENAR, 0), (KENAR, H)], fill=(0, 255, 0), width=3)
        d.line([(W - KENAR, 0), (W - KENAR, H)], fill=(0, 255, 0), width=3)
        d.rectangle([0, H - 420, W, H], outline=(255, 0, 0), width=4)  # Shorts arayüzünün kapattığı alt bölge
        kareler.append(k.resize((360, 640)))
    sayfa = Image.new("RGB", (360 * min(3, len(kareler)), 640 * math.ceil(len(kareler) / 3)), (0, 0, 0))
    for i, k in enumerate(kareler):
        sayfa.paste(k, ((i % 3) * 360, (i // 3) * 640))
    yol = cikis.with_name(cikis.stem + "-kontrol.jpg")
    sayfa.save(yol, quality=85)
    return yol


def main():
    is_yolu = Path(sys.argv[1])
    is_ = json.loads(is_yolu.read_text())
    cikis = KOK / is_.get("cikis", f"cikti/{is_yolu.stem}.mp4")
    cikis.parent.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        ham, eklemler, (sw, sh) = ham_hazirla(is_, tmp)
        etiket_metni = f"{is_['yayinci']} · {is_.get('platform', 'KICK')}"
        # "pro" (varsayılan): kutulu kanca, akan Anton altyazı, bulanık geçiş, kromatik vuruş. "klasik": 19 Kas öncesi görünüm.
        pro = is_.get("stil", "pro") == "pro"
        if pro:
            altyazi = []
            for a in is_.get("altyazi", []):
                for bas, son, metin in kelime_parcalari(a):
                    if a.get("aksiyon"):
                        g = yazi_gorseli(f"[{metin}]", a.get("boy", 96), kontur=10, yol=ANTON, agirlik=None, vurgu=(255, 255, 255))
                    else:
                        # Parça tek satıra sığana kadar küçülür (en az 96); yine sığmazsa iki satıra iner.
                        boy = a.get("boy", 128)
                        while boy > 96 and len(satirla(buyuk(metin), font(ANTON, boy), W - 2 * KENAR)) > 1:
                            boy -= 8
                        g = yazi_gorseli(metin, boy, kontur=13, yol=ANTON, agirlik=None)
                    altyazi.append((bas, son, golgeli(g)))
            kanca = kanca_kutusu(is_["kanca"], is_.get("kanca_boy", 92))
        else:
            altyazi = [(a["bas"], a["son"], yazi_gorseli(a["metin"], a.get("boy", 84), kontur=11)) for a in is_.get("altyazi", [])]
            kanca = yazi_gorseli(is_["kanca"], is_.get("kanca_boy", 118), kontur=14, yol=ANTON, agirlik=None)
        sabit = {
            "pro": pro,
            "cam_h": int(is_.get("kamera_oran", 0.4) * H),
            "etiket": yazi_gorseli(etiket_metni, 40, renk=TURUNCU, kontur=6, agirlik=800),
            "kanca": kanca,
            "altyazi": altyazi,
            # Kanal imzası (ör. "@kozzyclipp"); boşsa hiç basılmaz.
            "filigran": yazi_gorseli(is_["filigran"], 30, renk=(255, 255, 255), kontur=4, agirlik=700, buyut=False) if is_.get("filigran") else Image.new("RGBA", (1, 1)),
        }
        ust = np.zeros((H, W, 4), dtype=np.uint8)
        ust[:420, :, 3] = (np.linspace(170, 0, 420) ** 1.0).astype(np.uint8)[:, None]
        sabit["ust_golge"] = Image.fromarray(ust, "RGBA")
        yy, xx = np.mgrid[0:H, 0:W]
        uzak = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
        vin = np.zeros((H, W, 4), dtype=np.uint8)
        vin[..., 0] = 230
        vin[..., 3] = (np.clip((uzak - 0.55) / 0.6, 0, 1) * 200).astype(np.uint8)
        sabit["vinyet"] = Image.fromarray(vin, "RGBA")
        sabit["filigran"].putalpha(sabit["filigran"].split()[-1].point(lambda p: p * 150 // 255))
        b = 0.0
        sabit["araliklar"] = []
        for p in is_["parcalar"]:
            sabit["araliklar"].append((b, b + p["son"] - p["bas"]))
            b += p["son"] - p["bas"]
        sure = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(ham)], capture_output=True, text=True, check=True).stdout)
        video = tmp / "video.mp4"
        oku = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(ham), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
        yaz = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                                "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-color_primaries", "bt709",
                                "-color_trc", "bt709", "-colorspace", "bt709", str(video)], stdin=subprocess.PIPE)
        boyut = sw * sh * 3
        n = 0
        while True:
            veri = oku.stdout.read(boyut)
            if len(veri) < boyut:
                break
            kare = Image.frombuffer("RGB", (sw, sh), veri)
            yaz.stdin.write(kare_kur(kare, n / FPS, is_, sabit, eklemler).tobytes())
            n += 1
            if n % 150 == 0:
                print(f"{n / FPS:.0f}/{sure:.0f} sn", flush=True)
        yaz.stdin.close()
        yaz.wait()
        oku.wait()
        ses_karistir(ham, is_, eklemler, cikis, video)
    print("bitti:", cikis)
    if "--kontrol" in sys.argv:
        print("kontrol:", kontrol_sayfasi(cikis, is_))


if __name__ == "__main__":
    main()
