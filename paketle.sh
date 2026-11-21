#!/usr/bin/env bash
# © 2026 Vinci Studio. Tüm hakları saklıdır. Kullanım koşulları: LICENSE.
# claude.ai (web/masaüstü) için her skill'i ayrı .zip yapar: Ayarlar → Yetenekler → Skills → Yükle.
# Not: web ortamında Python ortamı, Whisper modeli ve ffmpeg yoktur; tam güç Claude Code + install.sh ile gelir.
set -euo pipefail
cd "$(dirname "$0")"; rm -rf dist; mkdir -p dist
for d in skills/*/; do ad=$(basename "$d"); (cd skills && zip -qr "../dist/$ad.zip" "$ad" -x '*.DS_Store' '*__pycache__*'); cp LICENSE "dist/" ; echo "dist/$ad.zip"; done
