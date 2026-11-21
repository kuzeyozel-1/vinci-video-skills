#!/usr/bin/env bash
# © 2026 Vinci Studio. Tüm hakları saklıdır. Kullanım koşulları: repodaki LICENSE dosyası.
# YouTube canlı yayınının geri sarma penceresinden (~15 dk) bir dilim çeker; 2 sn'lik HLS parçaları 16 paralel.
# Görüntü ve ses ayrı listelerde: ikisi parça sıra numarasına (/sq/N/) göre eşlenir, yoksa ses kayar (bir kez 92 sn kaydı).
# Kullanım: <skill>/scripts/canli.sh <youtube adresi> <kaç dk önceden> <kaç dk> <çıktı.mp4> [görüntü formatı, vars. 311=720p60; 312=1080p60]
set -euo pipefail
URL=$1; GERI=$2; SURE=$3; OUT=$4; VF=${5:-311}
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
yt-dlp --no-update -g -f "$VF" "$URL" 2>/dev/null > "$TMP/v.url"
yt-dlp --no-update -g -f 234 "$URL" 2>/dev/null > "$TMP/a.url"
curl -s "$(cat "$TMP/v.url")" | grep -v '^#' > "$TMP/v.list"
curl -s "$(cat "$TMP/a.url")" | grep -v '^#' > "$TMP/a.list"
sq() { sed -E 's#.*/sq/([0-9]+)/.*#\1#'; }
SON=$(tail -1 "$TMP/v.list" | sq); ASON=$(tail -1 "$TMP/a.list" | sq); [ "$ASON" -lt "$SON" ] && SON=$ASON
BAS=$(( SON - GERI * 30 )); BIT=$(( BAS + SURE * 30 - 1 ))
cek() {  # $1 v|a
  awk -v b="$BAS" -v e="$BIT" '{ if (match($0, /\/sq\/[0-9]+\//)) { n = substr($0, RSTART + 4, RLENGTH - 5) + 0; if (n >= b && n <= e) print n, $0 } }' "$TMP/$1.list" | \
    xargs -P 16 -n 2 sh -c 'curl -s --max-time 20 --retry 4 --retry-all-errors -o "'"$TMP/$1"'-$0.ts" "$1"' || true
  ls "$TMP"/"$1"-*.ts | sort -V | xargs cat > "$TMP/$1.ts"
}
cek v; cek a
ffmpeg -v error -y -i "$TMP/v.ts" -i "$TMP/a.ts" -map 0:v -map 1:a -c copy -shortest "$OUT"
ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT"
