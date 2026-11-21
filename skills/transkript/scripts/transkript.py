# © 2026 Vinci Studio. Tüm hakları saklıdır. Kullanım koşulları: repodaki LICENSE dosyası.
"""Video/ses dosyalarını yerelde yazıya döker (faster-whisper large-v3-turbo, kelime zamanlı). İnternete veri gitmez.

Kullanım:
  ~/.vinci-video/.venv/bin/python transkript.py <dosya ya da klasör> [--dil tr] [--cikti transkript/] [--vadsiz] [--srt]
Çıktı: <cikti>/<ad>.json  {"dosya", "dil", "sure", "segmentler": [{"bas","son","metin","kelimeler":[{"k","b","s"}]}]}
       --srt verilirse yanına <ad>.srt (satır başına en çok ~42 karakter).
"""
import json
import os
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np
from faster_whisper import WhisperModel

MODEL = Path(os.environ.get("VINCI_VIDEO_EV", Path.home() / ".vinci-video")) / "models/large-v3-turbo"
UZANTI = {".mp4", ".mov", ".m4a", ".wav", ".mp3", ".mkv", ".webm", ".aac", ".flac"}


def arg(ad, varsayilan=None):
    return sys.argv[sys.argv.index(ad) + 1] if ad in sys.argv else varsayilan


def ses(dosya: Path, tmp: Path) -> np.ndarray:
    # Dosya yolu yerine numpy dizisi veriyoruz: bazı Python sürümlerinde faster-whisper'ın kendi okuyucusu (av) hata veriyor.
    wav = tmp / f"{dosya.stem}.16k.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(dosya), "-map", "0:a:0", "-ac", "1", "-ar", "16000", str(wav)], check=True)
    with wave.open(str(wav)) as w:
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0


def zaman(t: float) -> str:
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def srt(segmentler, sinir=42) -> str:
    bloklar, simdiki = [], []
    for s in segmentler:
        for k in s["kelimeler"]:
            if simdiki and len(" ".join(x["k"] for x in simdiki + [k])) > sinir:
                bloklar.append(simdiki)
                simdiki = []
            simdiki.append(k)
            if k["k"][-1:] in ".?!":
                bloklar.append(simdiki)
                simdiki = []
    if simdiki:
        bloklar.append(simdiki)
    return "\n".join(f"{i}\n{zaman(b[0]['b'])} --> {zaman(b[-1]['s'])}\n{' '.join(x['k'] for x in b)}\n" for i, b in enumerate(bloklar, 1))


def main():
    girdi = Path(sys.argv[1])
    dosyalar = sorted(p for p in girdi.iterdir() if p.suffix.lower() in UZANTI) if girdi.is_dir() else [girdi]
    cikti = Path(arg("--cikti", "transkript"))
    cikti.mkdir(parents=True, exist_ok=True)
    tmp = cikti / ".ses"
    tmp.mkdir(exist_ok=True)
    vad = "--vadsiz" not in sys.argv  # kısa kesitlerde VAD bazı replikleri kaçırır; --vadsiz zamanları da düzeltir
    model = WhisperModel(str(MODEL), device="cpu", compute_type="int8")
    for d in dosyalar:
        out = cikti / f"{d.stem}.json"
        if out.exists() and "--yeniden" not in sys.argv:
            print("var, geçildi:", out)
            continue
        a = ses(d, tmp)
        segs, info = model.transcribe(a, language=arg("--dil"), vad_filter=vad, word_timestamps=True, beam_size=5, condition_on_previous_text=vad)
        seg = [{"bas": round(s.start, 2), "son": round(s.end, 2), "metin": s.text.strip(),
                "kelimeler": [{"k": w.word.strip(), "b": round(w.start, 2), "s": round(w.end, 2)} for w in (s.words or [])]} for s in segs]
        out.write_text(json.dumps({"dosya": d.name, "dil": info.language, "sure": round(len(a) / 16000, 2), "segmentler": seg}, ensure_ascii=False, indent=1))
        if "--srt" in sys.argv:
            out.with_suffix(".srt").write_text(srt(seg))
        print(f"{d.name}: {info.language}, {len(seg)} segment -> {out}", flush=True)
        for s in seg:
            print(f"  {s['bas']:7.2f}-{s['son']:7.2f}  {s['metin']}")


if __name__ == "__main__":
    main()
