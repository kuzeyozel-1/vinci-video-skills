# © 2026 Vinci Studio. Tüm hakları saklıdır. Kullanım koşulları: repodaki LICENSE dosyası.
"""Transkriptte bir cümleyi bulur, kesilecek zamanı verir (kelime zamanlarından).
Kullanım: python3 bul.py transkript/kayit.json "ne alaka ya"     (büyük/küçük harf ve noktalama önemsiz)
          python3 bul.py transkript/kayit.json --liste           (tüm cümleler ve zamanları)
"""
import json
import re
import sys

veri = json.load(open(sys.argv[1]))
kelimeler = [k for s in veri["segmentler"] for k in s["kelimeler"]]


def sade(x: str) -> str:
    return re.sub(r"[^\wçğıöşü' ]", "", x.replace("İ", "i").replace("I", "ı").lower()).strip()


if sys.argv[2] == "--liste":
    for s in veri["segmentler"]:
        print(f"{s['bas']:7.2f}-{s['son']:7.2f}  {s['metin']}")
    sys.exit()
aranan = sade(sys.argv[2]).split()
bulundu = False
for i in range(len(kelimeler) - len(aranan) + 1):
    if [sade(k["k"]) for k in kelimeler[i:i + len(aranan)]] == aranan:
        b, s = kelimeler[i]["b"], kelimeler[i + len(aranan) - 1]["s"]
        print(f"{b:.2f} {s:.2f}   ({s - b:.2f} sn)  {' '.join(k['k'] for k in kelimeler[i:i + len(aranan)])}")
        bulundu = True
if not bulundu:
    sys.exit("bulunamadı; --liste ile cümlelere bak (Whisper kelimeyi farklı yazmış olabilir)")
