# © 2026 Vinci Studio. Tüm hakları saklıdır. Kullanım koşulları: repodaki LICENSE dosyası.
"""Vinci renk ön ayarları (ffmpeg filtreleri). montaj.py bunları kullanır; tek dosyaya da uygulanabilir.

Kullanım: python3 renk.py girdi.mp4 cikti.mp4 klinik-soguk [--gren] [--kare 3]   (--kare: karşılaştırma için 3. sn'den önce/sonra jpg)
          python3 renk.py --liste
Önce/sonra karesine bakmadan ön ayarı onaylama; cilt tonu griye ya da turuncuya kaçıyorsa `dogal` ile başla.
"""
import subprocess
import sys

RENKLER = {
    # Sağlık / klinik marka filmi: soğuk mavi-camgöbeği, derin ama boğulmamış siyahlar, hafif vinyet.
    "klinik-soguk": "eq=contrast=1.10:saturation=0.92:gamma=0.97,"
                    "colorbalance=rs=-0.04:gs=0.01:bs=0.07:rm=-0.02:bm=0.03:rh=0.02:gh=0.01:bh=-0.01,"
                    "curves=all='0/0.02 0.3/0.26 0.7/0.74 1/0.98',vignette=angle=PI/5",
    # Lüks ürün, saat, mücevher, restoran: sıcak ışık, altın vurgular, yumuşak kontrast.
    "sicak-luks": "eq=contrast=1.08:saturation=1.05:gamma=0.98,"
                  "colorbalance=rs=0.03:bs=-0.04:rm=0.02:bm=-0.02:rh=0.05:gh=0.02:bh=-0.05,"
                  "curves=all='0/0.03 0.25/0.22 0.75/0.78 1/0.97',vignette=angle=PI/5",
    # Gece / şehir / otomobil: yüksek kontrast, mavi gölge, sıcak tepe ışığı.
    "gece-neon": "eq=contrast=1.15:saturation=1.18:gamma=0.92,"
                 "colorbalance=rs=-0.03:bs=0.09:rh=0.05:bh=-0.03,vignette=angle=PI/4.5",
    # Belgesel / röportaj: neredeyse dokunulmamış, sadece canlılık.
    "dogal": "eq=contrast=1.04:saturation=1.04",
    # Sinematik genel amaçlı: teal gölge + sıcak ten (turuncu-camgöbeği), en çok istenen "film" görünümü.
    "teal-turuncu": "eq=contrast=1.08:saturation=1.0,"
                    "colorbalance=rs=-0.06:gs=0.0:bs=0.06:rm=0.02:bm=-0.02:rh=0.06:gh=0.02:bh=-0.06,"
                    "curves=all='0/0.02 0.5/0.5 1/0.97',vignette=angle=PI/5",
}
GREN = "noise=alls=5:allf=t+u"


def filtre(ad: str | None, gren: bool = False) -> str:
    parcalar = [RENKLER[ad]] if ad else []
    if gren:
        parcalar.append(GREN)
    return ",".join(parcalar)


def main():
    if sys.argv[1] == "--liste":
        for k, v in RENKLER.items():
            print(f"{k:14} {v}")
        return
    girdi, cikti, ad = sys.argv[1:4]
    vf = filtre(ad, "--gren" in sys.argv)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", girdi, "-vf", vf, "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p",
                    "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-c:a", "copy", cikti], check=True)
    if "--kare" in sys.argv:
        an = sys.argv[sys.argv.index("--kare") + 1]
        for etiket, yol in (("once", girdi), ("sonra", cikti)):
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", an, "-i", yol, "-frames:v", "1", f"{cikti}.{etiket}.jpg"], check=True)
        print("karşılaştır:", f"{cikti}.once.jpg", f"{cikti}.sonra.jpg")
    print("ok", cikti)


if __name__ == "__main__":
    main()
