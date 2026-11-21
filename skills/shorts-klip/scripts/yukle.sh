#!/usr/bin/env bash
# © 2026 Vinci Studio. Tüm hakları saklıdır. Kullanım koşulları: repodaki LICENSE dosyası.
# Tarayıcıdan yükleme için 10 MB altı kopya: süreye göre bit hızı, iki geçişli HEVC. Kullanım (proje klasöründe): <skill>/scripts/yukle.sh cikti/ad.mp4
set -euo pipefail
IN=$1; mkdir -p yukle; OUT=yukle/$(basename "$IN")
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN")
VB=$(python3 -c "print(min(8000, int(9.3 * 8192 / $D - 200)))")
# HEVC (H.265): aynı 10 MB'ta H.264'ten belirgin daha net. YouTube/Instagram kabul eder; hvc1 etiketi Apple uyumu için.
X265="-c:v libx265 -preset slow -b:v ${VB}k -tag:v hvc1 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709"
ffmpeg -v error -y -i "$IN" $X265 -x265-params "pass=1:stats=/tmp/kozzy2p.log:log-level=error" -an -f mp4 /dev/null
ffmpeg -v error -y -i "$IN" $X265 -x265-params "pass=2:stats=/tmp/kozzy2p.log:log-level=error" -c:a aac -b:a 160k -movflags +faststart "$OUT"
ls -la "$OUT" | awk '{print $5/1048576 " MB", $NF}'
