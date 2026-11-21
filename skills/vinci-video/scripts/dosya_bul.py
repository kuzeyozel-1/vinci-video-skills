# © 2026 Vinci Studio. Tüm hakları saklıdır. Kullanım koşulları: repodaki LICENSE dosyası.
"""Kullanıcı yalnız dosya adını (ya da bir parçasını) söylediğinde dosyayı bilgisayarda bulur. Klasör sorma; önce bunu çalıştır.

Kullanım: python3 dosya_bul.py "roportaj"          -> en yeni 10 eşleşme (tam yol, boyut, tarih)
          python3 dosya_bul.py "kayit" --tur ses   (tür: video | ses | gorsel | hepsi; varsayılan hepsi)
Arama sırası: macOS Spotlight (mdfind, saniyeler sürer) + bilinen klasörler (İndirilenler, Masaüstü, Filmler, Belgeler,
Resimler, iCloud Drive, Sesli Notlar, ~/dev, takılı diskler). Türkçe harfler ve büyük/küçük harf önemsiz.
Birden çok eşleşme varsa en yenisi en üstte; tek ve açık eşleşmede doğrudan kullan, değilse ilk 3'ü kullanıcıya göster.
"""
import platform
import subprocess
import sys
import time
from pathlib import Path

TURLER = {
    "video": {".mp4", ".mov", ".m4v", ".mkv", ".webm", ".avi", ".mxf", ".braw", ".r3d", ".mts"},
    "ses": {".wav", ".m4a", ".mp3", ".aac", ".flac", ".aif", ".aiff", ".ogg", ".caf"},
    "gorsel": {".jpg", ".jpeg", ".png", ".heic", ".webp", ".tif", ".tiff", ".psd", ".svg", ".gif", ".dng", ".cr3", ".arw"},
}
EV = Path.home()
KLASORLER = [Path.cwd(), EV / "Downloads", EV / "Desktop", EV / "Movies", EV / "Documents", EV / "Pictures", EV / "Music",
             EV / "Library/Mobile Documents/com~apple~CloudDocs", EV / "Library/Containers/com.apple.VoiceMemos/Data",
             EV / "Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings", EV / "dev",
             *[p for p in Path("/Volumes").glob("*") if p.is_dir() and not p.is_symlink() and p.resolve() != Path("/")]]


def sade(s: str) -> str:
    s = s.replace("İ", "i").replace("I", "ı").lower()
    return s.translate(str.maketrans("çğıöşü", "cgiosu")).replace("_", " ").replace("-", " ")


def uygun(p: Path, aranan: str, uzantilar) -> bool:
    return aranan in sade(p.name) and (uzantilar is None or p.suffix.lower() in uzantilar) and p.is_file()


def spotlight(ham: str) -> list[Path]:
    if platform.system() != "Darwin":
        return []
    try:
        r = subprocess.run(["mdfind", "-name", ham], capture_output=True, text=True, timeout=20)
        return [Path(x) for x in r.stdout.splitlines() if x]
    except Exception:
        return []


def tara(ham: str, aranan: str, uzantilar) -> list[Path]:
    """Spotlight bulamazsa: bilinen klasörlerde `find` (her klasöre en çok 8 sn; izin isteyen ya da iCloud'dan inen
    klasörlerde takılırsa geçilir)."""
    desen = {f"*{ham}*", f"*{aranan}*"}
    ifade = sum([["-iname", d, "-o"] for d in desen], [])[:-1]
    bulunan = []
    for kok in KLASORLER:
        if not kok.exists():
            continue
        try:
            r = subprocess.run(["find", str(kok), "-maxdepth", "7", "(", "-name", "node_modules", "-o", "-name", ".*", "-o", "-name", "Caches", ")",
                                "-prune", "-o", "-type", "f", "(", *ifade, ")", "-print"], capture_output=True, text=True, timeout=8)
            cikti = r.stdout
        except subprocess.TimeoutExpired as e:
            cikti = (e.stdout or b"").decode(errors="ignore") if isinstance(e.stdout, bytes) else (e.stdout or "")
        bulunan += [Path(x) for x in cikti.splitlines() if x and uygun(Path(x), aranan, uzantilar)]
    return bulunan


def main():
    ham = sys.argv[1]
    tur = sys.argv[sys.argv.index("--tur") + 1] if "--tur" in sys.argv else "hepsi"
    uzantilar = None if tur == "hepsi" else TURLER[tur]
    aranan = sade(Path(ham).stem if Path(ham).suffix else ham)
    adaylar = {p for p in spotlight(ham) if uygun(p, aranan, uzantilar)}
    if len(adaylar) < 3:
        adaylar |= set(tara(ham, aranan, uzantilar))
    if not adaylar:
        sys.exit(f"'{ham}' bulunamadı. Adın başka bir parçasını dene ya da kullanıcıdan dosyayı sürükleyip bırakmasını iste.")
    for p in sorted(adaylar, key=lambda p: -p.stat().st_mtime)[:10]:
        st = p.stat()
        print(f"{st.st_size / 1048576:8.1f} MB  {time.strftime('%Y-%m-%d %H:%M', time.localtime(st.st_mtime))}  {p}")


if __name__ == "__main__":
    main()
