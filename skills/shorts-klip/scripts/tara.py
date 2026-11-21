# © 2026 Vinci Studio. Tüm hakları saklıdır. Kullanım koşulları: repodaki LICENSE dosyası.
"""Kaynak videoyu tarar: konuşma dökümü (faster-whisper, kelime zamanlı) + ses patlamaları (bağırma, gülme).
Çıktı (çalıştırılan klasörde) `isler/<kaynak>-tarama.json`; klip anını seçmek ve altyazı çevirisi için kullanılır.
Kullanım: ~/.vinci-video/.venv/bin/python <skill>/scripts/tara.py kaynak/video.mp4 [--dil en] [--vadsiz]
"""
import json
import os
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

KOK = Path.cwd()
MODEL = Path(os.environ.get("VINCI_VIDEO_EV", Path.home() / ".vinci-video")) / "models/large-v3-turbo"


def ses_oku(video: Path) -> np.ndarray:
    wav = video.with_suffix(".16k.wav")
    if not wav.exists():
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(video), "-map", "0:a:0", "-ac", "1", "-ar", "16000", str(wav)], check=True)
    with wave.open(str(wav)) as w:
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0


def patlamalar(ses: np.ndarray, sr=16000, pencere=0.5, adet=12) -> list[dict]:
    """Yarım saniyelik pencerelerde RMS; medyanın çok üstündeki tepeler (en az 4 sn arayla)."""
    n = int(sr * pencere)
    rms = np.sqrt(np.array([np.mean(ses[i:i + n] ** 2) for i in range(0, len(ses) - n, n)]) + 1e-12)
    db = 20 * np.log10(rms)
    taban = np.median(db)
    sira = np.argsort(db)[::-1]
    secilen = []
    for i in sira:
        t = i * pencere
        if db[i] - taban < 6:
            break
        if all(abs(t - s["an"]) >= 4 for s in secilen):
            secilen.append({"an": round(t, 1), "db_ust": round(float(db[i] - taban), 1)})
        if len(secilen) >= adet:
            break
    return sorted(secilen, key=lambda s: s["an"])


def main():
    video = Path(sys.argv[1])
    dil = sys.argv[sys.argv.index("--dil") + 1] if "--dil" in sys.argv else None
    ses = ses_oku(video)
    from faster_whisper import WhisperModel
    model = WhisperModel(str(MODEL), device="cpu", compute_type="int8")
    # --vadsiz: kısa kesitlerde VAD oyun içi NPC repliklerini kaçırıyor; kapatınca zamanlar da daha doğru.
    vad = "--vadsiz" not in sys.argv
    segs, info = model.transcribe(ses, language=dil, vad_filter=vad, word_timestamps=True, beam_size=5, condition_on_previous_text=vad)
    dokum = [{"bas": round(s.start, 2), "son": round(s.end, 2), "metin": s.text.strip(),
              "kelimeler": [{"k": w.word.strip(), "b": round(w.start, 2), "s": round(w.end, 2)} for w in (s.words or [])]} for s in segs]
    out = KOK / "isler" / f"{video.stem}-tarama.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({"kaynak": str(video), "dil": info.language, "sure": round(len(ses) / 16000, 1),
                               "patlamalar": patlamalar(ses), "dokum": dokum}, ensure_ascii=False, indent=1))
    print(out, info.language, len(dokum), "cümle")
    for s in dokum:
        print(f"{s['bas']:7.1f}  {s['metin']}")


if __name__ == "__main__":
    main()
