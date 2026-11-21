#!/usr/bin/env bash
# © 2026 Vinci Studio. Tüm hakları saklıdır. Kullanım koşulları: repodaki LICENSE dosyası.
# Tarayıcıdan yükleme için 10 MB altı kopya: süreye göre bit hızı, iki geçiş. Kullanım (proje klasöründe): <skill>/scripts/yukle.sh cikti/ad.mp4
set -euo pipefail
IN=$1; mkdir -p yukle; OUT=yukle/$(basename "$IN")
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN")
VB=$(python3 -c "print(min(3400, int(9.3 * 8192 / $D - 200)))")
ffmpeg -v error -y -i "$IN" -c:v libx264 -b:v ${VB}k -pass 1 -passlogfile /tmp/kozzy2p -an -f mp4 /dev/null
ffmpeg -v error -y -i "$IN" -c:v libx264 -b:v ${VB}k -pass 2 -passlogfile /tmp/kozzy2p -c:a aac -b:a 160k -movflags +faststart "$OUT"
ls -la "$OUT" | awk '{print $5/1048576 " MB", $NF}'
