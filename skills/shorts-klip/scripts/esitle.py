# © 2026 Vinci Studio. Tüm hakları saklıdır. Kullanım koşulları: repodaki LICENSE dosyası.
"""Ses-görüntü kaymasını ölçer: yayıncı kamerasındaki hareket ile ses yüksekliğini çapraz ilişkilendirir.
Kullanım: ~/.vinci-video/.venv/bin/python <skill>/scripts/esitle.py kaynak.mp4 x y w h   (kamera kutusu, 1920x1080'e göre)
Çıktı: saniye cinsinden kayma (+ ise ses görüntüden ileride; düzeltmek için sesi o kadar geciktir).
"""
import subprocess
import sys

import numpy as np

yol = sys.argv[1]
x, y, w, h = map(int, sys.argv[2:6])
fps = 10
p = subprocess.run(["ffmpeg", "-v", "error", "-i", yol, "-vf", f"scale=1920:1080,crop={w}:{h}:{x}:{y},scale=96:64,fps={fps},format=gray",
                    "-f", "rawvideo", "-"], capture_output=True, check=True)
kareler = np.frombuffer(p.stdout, dtype=np.uint8).reshape(-1, 64, 96).astype(np.float32)
hareket = np.abs(np.diff(kareler, axis=0)).mean(axis=(1, 2))
a = subprocess.run(["ffmpeg", "-v", "error", "-i", yol, "-ac", "1", "-ar", "8000", "-f", "s16le", "-"], capture_output=True, check=True)
ses = np.frombuffer(a.stdout, dtype=np.int16).astype(np.float32)
n = 8000 // fps
rms = np.sqrt(np.array([np.mean(ses[i:i + n] ** 2) for i in range(0, len(ses) - n, n)]))[1:]
m = min(len(hareket), len(rms))
h_, r_ = hareket[:m], np.log(rms[:m] + 1)
h_ = (h_ - h_.mean()) / h_.std()
r_ = (r_ - r_.mean()) / r_.std()
en_iyi = []
sinir = min(150 * fps, m // 2)
for lag in range(-sinir, sinir + 1):
    if lag >= 0:
        c = np.mean(h_[lag:] * r_[:m - lag])  # görüntü t+lag  ~  ses t
    else:
        c = np.mean(h_[:m + lag] * r_[-lag:])
    en_iyi.append((c, lag / fps))
en_iyi.sort(reverse=True)
for c, l in en_iyi[:5]:
    print(f"kayma {l:+.1f} sn  ilişki {c:.3f}")
