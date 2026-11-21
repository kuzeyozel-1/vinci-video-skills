# © 2026 Vinci Studio. Tüm hakları saklıdır. Kullanım koşulları: repodaki LICENSE dosyası.
"""Telifsiz ses efektleri: hepsi burada sentezlenir, dış kütüphaneye bağımlı değil.
Kullanım: ~/.vinci-video/.venv/bin/python efektler.py [hedef_klasör]   (varsayılan ~/.vinci-video/sesler)
"""
import os
import sys
import wave
from pathlib import Path

import numpy as np

SR = 48000
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(os.environ.get("VINCI_VIDEO_EV", Path.home() / ".vinci-video")) / "sesler"


def kaydet(ad: str, x: np.ndarray):
    x = x / (np.abs(x).max() + 1e-9) * 0.9
    OUT.mkdir(parents=True, exist_ok=True)
    with wave.open(str(OUT / f"{ad}.wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())


def zarf(n, atak, bitis):
    e = np.ones(n)
    a, b = int(atak * SR), int(bitis * SR)
    e[:a] = np.linspace(0, 1, a)
    e[-b:] *= np.linspace(1, 0, b) ** 2
    return e


def whoosh(sure=0.45):
    n = int(sure * SR)
    t = np.arange(n) / SR
    gurultu = np.random.default_rng(1).standard_normal(n)
    # Süpürme: zamanla açılan basit tek kutuplu alçak geçiren filtre.
    kesim = 0.02 + 0.5 * np.sin(np.pi * t / sure) ** 2
    y = np.zeros(n)
    for i in range(1, n):
        y[i] = y[i - 1] + kesim[i] * (gurultu[i] - y[i - 1])
    return y * zarf(n, 0.12, 0.2)


def boom(sure=0.9):
    n = int(sure * SR)
    t = np.arange(n) / SR
    f = 120 * np.exp(-t * 6) + 38
    faz = 2 * np.pi * np.cumsum(f) / SR
    tik = np.random.default_rng(2).standard_normal(n) * np.exp(-t * 90) * 0.4
    return (np.sin(faz) * np.exp(-t * 3.2) + tik) * zarf(n, 0.002, 0.3)


def pop(sure=0.12):
    n = int(sure * SR)
    t = np.arange(n) / SR
    f = 900 * np.exp(-t * 30) + 300
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 40)


def ding(sure=0.8):
    n = int(sure * SR)
    t = np.arange(n) / SR
    return sum(np.sin(2 * np.pi * f * t) * a for f, a in [(1318, 1), (2637, 0.35), (3951, 0.15)]) * np.exp(-t * 6) * zarf(n, 0.003, 0.2)


def yanlis(sure=0.7):
    # "Başarısız" buzzer'ı: iki kare dalga, düşen perde.
    n = int(sure * SR)
    t = np.arange(n) / SR
    f = np.where(t < sure / 2, 220, 165)
    return np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.5 * zarf(n, 0.005, 0.08)


def kayit_cizik(sure=0.5):
    n = int(sure * SR)
    t = np.arange(n) / SR
    f = 1400 * np.exp(-t * 7) + 80
    tiz = np.sin(2 * np.pi * np.cumsum(f) / SR)
    g = np.random.default_rng(3).standard_normal(n) * 0.5
    return (tiz + g) * zarf(n, 0.005, 0.15)


def bruh(sure=0.6):
    # Alçak, kısa "bruh" benzeri formant vuruşu.
    n = int(sure * SR)
    t = np.arange(n) / SR
    f0 = 95 * np.exp(-t * 0.8)
    kaynak = np.sign(np.sin(2 * np.pi * np.cumsum(f0) / SR))
    return (kaynak * (0.6 + 0.4 * np.sin(2 * np.pi * 600 * t))) * zarf(n, 0.01, 0.3) * 0.6


if __name__ == "__main__":
    for ad, fn in [("whoosh", whoosh), ("boom", boom), ("pop", pop), ("ding", ding), ("yanlis", yanlis), ("cizik", kayit_cizik), ("bruh", bruh)]:
        kaydet(ad, fn())
    print("ok", sorted(p.name for p in OUT.glob("*.wav")))
