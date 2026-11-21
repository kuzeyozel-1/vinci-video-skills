#!/usr/bin/env bash
# © 2026 Vinci Studio. Tüm hakları saklıdır. Kullanım koşulları: repodaki LICENSE dosyası.
# Kayıttan tek replik keser: temiz giriş/çıkış (fade), gürültü bastırma, NETLİK EQ, konuşma seviyesi (-16 LUFS), 48 kHz stereo wav.
# Netlik EQ: telefon kayıtlarında 250–800 Hz baskın, 0,8–5 kHz ~15 dB zayıf (ölçüldü) -> ses "boğuk". Çamur kesilir, varlık bölgesi açılır.
# EQ istemiyorsan 6. argüman: duz
# Kullanım: kes.sh kayit.m4a <bas_sn> <son_sn> cikti.wav [pay_sn=0.08] [net|duz]
# DİKKAT: -ss/-to MUTLAKA -i'den ÖNCE. Sonra konursa afade zamanları kayar ve dosya sessiz çıkar (-91 dB görüldü).
set -euo pipefail
IN=$1; B=$2; S=$3; OUT=$4; PAY=${5:-0.08}; MOD=${6:-net}
NET="equalizer=f=180:t=q:w=1:g=-3,equalizer=f=350:t=q:w=1.2:g=-7,equalizer=f=1500:t=q:w=1:g=6,equalizer=f=3000:t=q:w=1:g=8,equalizer=f=5000:t=q:w=1:g=5,highshelf=f=8000:g=3,acompressor=threshold=-22dB:ratio=3:attack=5:release=100:makeup=2,"
[ "$MOD" = duz ] && NET=""
B2=$(python3 -c "print(max(0, $B - $PAY))"); S2=$(python3 -c "print($S + $PAY)")
D=$(python3 -c "print(round($S2 - $B2, 3))"); FO=$(python3 -c "print(round(max(0, $S2 - $B2 - 0.06), 3))")
mkdir -p "$(dirname "$OUT")"
ffmpeg -v error -y -ss "$B2" -to "$S2" -i "$IN" \
  -af "highpass=f=100,afftdn=nf=-25,${NET}afade=t=in:st=0:d=0.03,afade=t=out:st=$FO:d=0.06,loudnorm=I=-16:TP=-1.5:LRA=7,aresample=48000" \
  -ac 2 "$OUT"
V=$(ffmpeg -v info -i "$OUT" -af volumedetect -f null - 2>&1 | sed -n 's/.*mean_volume: \(.*\) dB/\1/p')
echo "$OUT  ${D} sn  ortalama ${V} dB"
python3 -c "import sys; sys.exit(0 if float('$V') > -40 else 1)" || { echo "UYARI: çıktı neredeyse sessiz, zamanları kontrol et" >&2; exit 1; }
