# © 2026 Vinci Studio. Tüm hakları saklıdır. Kullanım koşulları: repodaki LICENSE dosyası.
"""Sakin, sıcak fon müziği (klinik, spa, kurumsal) üretir. Telifsiz: tamamen sentezlenmiş, örnek/kayıt yok.
Kullanım: ~/.vinci-video/.venv/bin/python fon_muzik.py çıktı.wav [süre_sn]"""
import sys
import numpy as np

SR = 44100
dur = float(sys.argv[2]) if len(sys.argv) > 2 else 40.0
out = sys.argv[1]
rng = np.random.default_rng(7)
N = int(SR * dur)
t = np.arange(N) / SR

def hz(m): return 440.0 * 2 ** ((m - 69) / 12)

# Cmaj9 – Am9 – Fmaj9 – Gsus/G6 ; her akor ~8 sn, uzun geçişli
chords = [[48, 55, 59, 62, 64], [45, 52, 59, 60, 64], [41, 48, 57, 60, 64], [43, 50, 57, 62, 64]]
seg = dur / 4.0
pad = np.zeros(N)
for ci, ch in enumerate(chords):
    c0, c1 = ci * seg - 2.5, (ci + 1) * seg + 2.5          # akorlar birbirine bindirilir
    env = np.clip((t - c0) / 3.0, 0, 1) * np.clip((c1 - t) / 3.0, 0, 1)
    env = env * env * (3 - 2 * env)
    for m in ch:
        for det in (-0.07, 0.0, 0.07):                       # hafif detune: kalın, sıcak
            f = hz(m) * 2 ** (det / 12)
            ph = rng.uniform(0, 2 * np.pi)
            tone = np.sin(2 * np.pi * f * t + ph) + 0.25 * np.sin(2 * np.pi * 2 * f * t + ph) + 0.08 * np.sin(2 * np.pi * 3 * f * t)
            pad += env * tone * 0.02
# yavaş nefes (tremolo)
pad *= 0.86 + 0.14 * np.sin(2 * np.pi * 0.11 * t)

# seyrek yumuşak "çan/piyano" notaları (pentatonik, yavaş)
bells = np.zeros(N)
scale = [72, 74, 76, 79, 81, 84]
pos, step = 1.6, 2.35
k = 0
while pos < dur - 3:
    m = scale[(k * 3 + (k // 2)) % len(scale)]
    f = hz(m)
    i0 = int(pos * SR); L = int(3.6 * SR)
    tt = np.arange(min(L, N - i0)) / SR
    note = (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * 2.01 * f * tt) * np.exp(-tt * 3) + 0.1 * np.sin(2 * np.pi * 3.02 * f * tt) * np.exp(-tt * 5))
    note *= np.exp(-tt * 1.3) * np.minimum(tt / 0.012, 1)
    bells[i0:i0 + len(tt)] += note * 0.16
    pos += step + (0.55 if k % 3 == 2 else 0)
    k += 1

dry = pad + bells
# reverb: üstel sönümlü gürültü impuls yanıtı ile evrişim (FFT)
irn = int(2.8 * SR)
ir = rng.standard_normal(irn) * np.exp(-np.arange(irn) / SR * 2.2)
ir[: int(0.02 * SR)] *= np.linspace(0, 1, int(0.02 * SR))
def conv(x): 
    n = 1 << int(np.ceil(np.log2(len(x) + len(ir))))
    return np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(ir, n), n)[: len(x)]
wetL, wetR = conv(dry), conv(np.roll(dry, int(0.011 * SR)))
wet = np.stack([wetL, wetR], 1)
wet /= np.max(np.abs(wet)) + 1e-9
drys = np.stack([dry, np.roll(dry, int(0.007 * SR))], 1)
drys /= np.max(np.abs(drys)) + 1e-9
mix = 0.45 * drys + 0.75 * wet
# yumuşak alçak geçiren (parlak tonları kıs), giriş/çıkış
a = np.exp(-2 * np.pi * 3800 / SR)
for ch in range(2):
    y = np.zeros(N); s = 0.0
    for i, v in enumerate(mix[:, ch]): s = (1 - a) * v + a * s; y[i] = s
    mix[:, ch] = y
mix *= np.clip(t / 2.5, 0, 1)[:, None] * np.clip((dur - t) / 3.0, 0, 1)[:, None]
mix = mix / np.max(np.abs(mix)) * 0.8
import wave
with wave.open(out, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes())
print("ok", out, dur)
