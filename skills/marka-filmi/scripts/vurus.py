# © 2026 Vinci Studio. Tüm hakları saklıdır. Kullanım koşulları: repodaki LICENSE dosyası.
"""Müzikte vuruşları bulur: kesimleri ritme oturtmak için (tempo, vuruş ızgarası, güçlü vurgular).

Kullanım: ~/.vinci-video/.venv/bin/python vurus.py muzik.wav [--json vurus.json]
Çıktı: tahmini BPM, her vuruşun zamanı, en güçlü 12 vurgu (drop, davul girişi). Planların `son` değerlerini bunlara yasla.
"""
import json
import subprocess
import sys

import numpy as np

SR, PENCERE, ADIM = 22050, 1024, 512


def oku(yol: str) -> np.ndarray:
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", yol, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"], capture_output=True, check=True)
    return np.frombuffer(p.stdout, dtype=np.int16).astype(np.float32) / 32768.0


def main():
    x = oku(sys.argv[1])
    n = 1 + (len(x) - PENCERE) // ADIM
    kareler = np.lib.stride_tricks.as_strided(x, (n, PENCERE), (x.strides[0] * ADIM, x.strides[0])) * np.hanning(PENCERE)
    spek = np.log1p(np.abs(np.fft.rfft(kareler, axis=1)) * 10)
    aki = np.maximum(0, np.diff(spek, axis=0)).sum(axis=1)  # spektral akı: yeni ses enerjisi
    aki = (aki - aki.mean()) / (aki.std() + 1e-9)
    kare_sn = ADIM / SR
    # Tempo: akının özilintisinde 70–180 BPM aralığındaki en güçlü gecikme.
    ozi = np.correlate(aki, aki, "full")[len(aki) - 1:]
    gmin, gmax = int(60 / 180 / kare_sn), int(60 / 70 / kare_sn)
    gecikme = gmin + int(np.argmax(ozi[gmin:gmax]))
    bpm = 60 / (gecikme * kare_sn)
    # Izgaranın fazı: vuruş noktalarındaki akı toplamı en yüksek olan kayma.
    faz = max(range(gecikme), key=lambda f: aki[f::gecikme].sum())
    vuruslar = [round((faz + k * gecikme) * kare_sn, 3) for k in range((len(aki) - faz) // gecikme + 1)]
    # Güçlü vurgular: yerel tepe, en az 1 sn arayla.
    tepe = [i for i in range(1, len(aki) - 1) if aki[i] > aki[i - 1] and aki[i] >= aki[i + 1] and aki[i] > 2.0]
    secilen = []
    for i in sorted(tepe, key=lambda i: -aki[i]):
        t = i * kare_sn
        if all(abs(t - s) >= 1.0 for s in secilen):
            secilen.append(round(t, 3))
        if len(secilen) >= 12:
            break
    sonuc = {"bpm": round(bpm, 1), "vurus_araligi": round(60 / bpm, 3), "vuruslar": vuruslar, "vurgular": sorted(secilen)}
    print(f"BPM ≈ {sonuc['bpm']}  (vuruş arası {sonuc['vurus_araligi']} sn)")
    print("vurgular:", " ".join(f"{t:.2f}" for t in sonuc["vurgular"]))
    print("ilk 16 vuruş:", " ".join(f"{t:.2f}" for t in vuruslar[:16]))
    if "--json" in sys.argv:
        with open(sys.argv[sys.argv.index("--json") + 1], "w") as f:
            json.dump(sonuc, f, indent=1)


if __name__ == "__main__":
    main()
