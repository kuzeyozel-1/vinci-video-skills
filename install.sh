#!/usr/bin/env bash
# © 2026 Vinci Studio. Tüm hakları saklıdır. Kullanım koşulları: LICENSE.
# Vinci Video kurulumu (macOS / Linux). Tekrar çalıştırmak güvenlidir: var olanı atlar, eksik olanı tamamlar.
#
#   ./install.sh                 her şeyi kur (skill'ler + Python ortamı + Whisper modeli + fontlar + efektler + HyperFrames skill'leri)
#   ./install.sh --modelsiz      Whisper modelini (1,6 GB) indirme
#   ./install.sh --eklenti       skill'leri ~/.claude/skills'e kopyalama (Claude Code eklentisi olarak kuracaksan)
#   ./install.sh --guncelle      git pull + skill'leri yenile
set -euo pipefail

REPO="$(cd "$(dirname "$0")" && pwd)"
EV="${VINCI_VIDEO_EV:-$HOME/.vinci-video}"
SKILLS="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
HF="https://huggingface.co/mobiuslabsgmbh/faster-whisper-large-v3-turbo/resolve/main"
ARGS=" $* "
secenek() { [[ "$ARGS" == *" $1 "* ]]; }
adim() { printf "\n\033[1;36m▸ %s\033[0m\n" "$1"; }
uyari() { printf "\033[1;33m! %s\033[0m\n" "$1"; }

if secenek --guncelle; then adim "Güncelleniyor"; git -C "$REPO" pull --ff-only; fi

adim "Gerekli araçlar"
EKSIK=()
for a in ffmpeg ffprobe node npx python3 curl git; do command -v "$a" >/dev/null || EKSIK+=("$a"); done
command -v yt-dlp >/dev/null || EKSIK+=("yt-dlp")
if ((${#EKSIK[@]})); then
  uyari "Eksik: ${EKSIK[*]}"
  if command -v brew >/dev/null; then
    echo "Homebrew ile kuruluyor..."; brew install ffmpeg node python yt-dlp git || true
  else
    echo "Kur ve tekrar çalıştır:  macOS: brew install ffmpeg node python yt-dlp   |  Ubuntu: sudo apt install ffmpeg nodejs npm python3-venv && pipx install yt-dlp"
    exit 1
  fi
fi
NODE_ANA=$(node -v | sed 's/v\([0-9]*\).*/\1/'); ((NODE_ANA >= 22)) || uyari "Node $NODE_ANA bulundu; HyperFrames Node 22+ ister."

adim "Python ortamı ($EV/.venv)"
mkdir -p "$EV"/{fontlar,sesler,models}
if [ ! -x "$EV/.venv/bin/python" ]; then
  if command -v uv >/dev/null; then uv venv -q --python 3.11 "$EV/.venv"; else python3 -m venv "$EV/.venv"; fi
fi
if command -v uv >/dev/null; then
  uv pip install -q --python "$EV/.venv/bin/python" faster-whisper numpy pillow
else
  "$EV/.venv/bin/python" -m pip install -q --upgrade pip faster-whisper numpy pillow
fi
"$EV/.venv/bin/python" -c "import faster_whisper, numpy, PIL; print('python tamam')"

adim "Fontlar (SIL OFL, Google Fonts)"
[ -s "$EV/fontlar/Anton-Regular.ttf" ] || curl -fsSL -o "$EV/fontlar/Anton-Regular.ttf" https://github.com/google/fonts/raw/main/ofl/anton/Anton-Regular.ttf
[ -s "$EV/fontlar/Montserrat.ttf" ] || curl -fsSL -o "$EV/fontlar/Montserrat.ttf" "https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat%5Bwght%5D.ttf"
ls "$EV/fontlar"

adim "Ses efektleri (sentez)"
"$EV/.venv/bin/python" "$REPO/skills/ses-muzik/scripts/efektler.py" "$EV/sesler"

if ! secenek --modelsiz; then
  adim "Whisper large-v3-turbo modeli (~1,6 GB, kesilirse kaldığı yerden devam eder)"
  M="$EV/models/large-v3-turbo"; mkdir -p "$M"
  for f in config.json tokenizer.json vocabulary.json preprocessor_config.json; do
    [ -s "$M/$f" ] || curl -fsSL -o "$M/$f" "$HF/$f"
  done
  if [ ! -s "$M/model.bin" ] || [ "$(wc -c < "$M/model.bin")" -lt 1617884929 ]; then
    # Tek bağlantı yavaş olabiliyor; 8 paralel parça + devam desteği.
    TOPLAM=1617884929; N=8; SZ=$(( (TOPLAM + N - 1) / N )); mkdir -p "$M/parts"
    for i in $(seq 0 $((N-1))); do
      s=$((i*SZ)); e=$((s+SZ-1)); [ $e -ge $TOPLAM ] && e=$((TOPLAM-1))
      curl -fsSL -C - --retry 20 --retry-delay 2 -r "$s-$e" -o "$M/parts/p$i" "$HF/model.bin" &
    done
    wait
    cat $(for i in $(seq 0 $((N-1))); do echo "$M/parts/p$i"; done) > "$M/model.bin"
    if [ "$(wc -c < "$M/model.bin")" -eq "$TOPLAM" ]; then rm -rf "$M/parts"; echo "model tamam"; else uyari "Model eksik indi; install.sh'i tekrar çalıştır."; fi
  else
    echo "model zaten var"
  fi
fi

adim "HyperFrames skill'leri (Apache-2.0, HeyGen; kendi kaynağından)"
npx -y hyperframes@latest skills update hyperframes hyperframes-cli hyperframes-registry media-use figma slideshow remotion-to-hyperframes \
  || uyari "HyperFrames skill'leri kurulamadı; sonra 'npx hyperframes skills update' çalıştır."

if ! secenek --eklenti; then
  adim "Vinci skill'leri → $SKILLS"
  mkdir -p "$SKILLS"
  for d in "$REPO"/skills/*/; do
    ad=$(basename "$d"); rm -rf "${SKILLS:?}/$ad"; cp -R "$d" "$SKILLS/$ad"; echo "  $ad"
  done
  chmod +x "$SKILLS"/*/scripts/*.sh 2>/dev/null || true
fi

adim "Bitti"
cat <<EOF
Kurulan: $(ls "$REPO/skills" | tr '\n' ' ')
Ortak dosyalar: $EV
Claude Code'u yeniden başlat; video işinde "vinci-video" skill'i otomatik devreye girer.
Güncelleme: ./install.sh --guncelle
EOF
