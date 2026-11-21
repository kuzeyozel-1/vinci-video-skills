---
name: transkript
description: Video ve ses dosyalarını yerelde, internete göndermeden yazıya döker (faster-whisper large-v3-turbo): kelime zamanları, dil tespiti, SRT altyazı. Altyazı zamanlama, klip anı seçme, seslendirme kesme ve çıktı sesini doğrulama için kullan. "Yazıya dök", "transkript", "altyazı çıkar", "ne diyor" denince kullan.
license: Proprietary. © 2026 Vinci Studio. Tüm hakları saklıdır. Bkz. LICENSE.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, WebFetch, WebSearch
metadata:
  sahip: Vinci Studio
  surum: "1.0.0"
---

# Transkript (yerel Whisper)

```bash
~/.vinci-video/.venv/bin/python scripts/transkript.py <dosya|klasör> [--dil tr] [--cikti transkript/] [--srt] [--vadsiz] [--yeniden]
```
- Çıktı: `transkript/<ad>.json` (segmentler + kelimeler: `k` kelime, `b` başlangıç, `s` bitiş). `--srt` ile `.srt` de üretir.
- `--dil` verilmezse dili kendisi bulur. Kısa ve gürültülü kliplerde dili zorla (`--dil tr`).
- `--vadsiz`: kısa kesitlerde VAD bazı replikleri (oyun içi NPC sesleri) kaçırır; kapatınca zamanlar da daha doğru olur.
- Model `~/.vinci-video/models/large-v3-turbo` (1,6 GB). CPU'da int8 ile 1 dk ses ≈ 15–30 sn sürer.

## Kullanım ipuçları
- **Çıktı doğrulama:** render'ın sesini yazıya dök. Beklenen cümleler var mı, tekrar eden ya da kayıp cümle var mı?
- **Altyazı zamanı:** kelime zamanları ±0,2 sn oynar. Kritik yerde ses enerjisine bak: `ffmpeg -i x.wav -af astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level -f null -`.
- **Halüsinasyon:** sessiz ya da müzikli bölümlerde "Altyazı M.K." gibi uydurma metin çıkabilir. Gerçek konuşma değilse atla.
- **Uzun dosya:** saatlik yayında zamanlar kayabilir. Önce bölümü kes, sonra kısa kesiti yazıya dök.
