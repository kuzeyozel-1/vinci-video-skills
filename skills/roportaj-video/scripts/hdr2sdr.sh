#!/usr/bin/env bash
# © 2026 Vinci Studio. Tüm hakları saklıdır. Kullanım koşulları: repodaki LICENSE dosyası.
# iPhone/aynasız HLG (HDR) çekimi SDR bt709'a çevirir. Çevrilmezse renkler soluk/griye kaçar ve
# Hyperframes üst katmanları (yazı, logo) render'da düşebilir. Kullanım: hdr2sdr.sh girdi.mov cikti.mp4
set -euo pipefail
IN=$1; OUT=$2
TRC=$(ffprobe -v error -select_streams v:0 -show_entries stream=color_transfer -of default=nw=1:nk=1 "$IN" | head -1)
if [ "$TRC" != "arib-std-b67" ] && [ "$TRC" != "smpte2084" ]; then
  echo "HDR değil ($TRC); yalnız bt709 etiketiyle kopyalanıyor"
  ffmpeg -v error -y -i "$IN" -c:v libx264 -crf 16 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 -c:a aac -b:a 192k "$OUT"
  exit 0
fi
if ffmpeg -hide_banner -filters 2>/dev/null | grep -q " zscale "; then
  VF="zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p"
else
  # zscale yoksa: HLG ters OETF (BT.2100) -> kazanç 2.8, doygunluk 1.6 (onaylı klinik videosuyla ölçüldü; daha yükseği teni turuncuya kaçırıyor). Gamut dönüşümü yaklaşık: sonucu mutlaka karede kontrol et -> gama 2.2.
  E="val/maxval"
  L="if(lte($E,0.5),pow($E,2)/3,(exp(($E-0.55991073)/0.17883277)+0.28466892)/12)"
  X="clip(pow(clip($L*2.8,0,1),0.4545)*maxval,0,maxval)"
  VF="scale=in_color_matrix=bt2020:out_color_matrix=bt709,format=gbrp,lutrgb=r='$X':g='$X':b='$X',eq=saturation=1.6,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p"
fi
ffmpeg -v error -y -i "$IN" -vf "$VF" -c:v libx264 -crf 16 -preset medium -color_primaries bt709 -color_trc bt709 -colorspace bt709 -c:a aac -b:a 192k -movflags +faststart "$OUT"
echo "ok $OUT"
