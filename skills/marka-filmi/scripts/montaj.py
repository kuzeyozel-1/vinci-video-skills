# © 2026 Vinci Studio. Tüm hakları saklıdır. Kullanım koşulları: repodaki LICENSE dosyası.
"""Marka filmi montajı: plan listesinden (JSON) renklendirilmiş, yavaş itişli (push-in), müzik + foley karışımlı film.

Kullanım (proje klasöründe): python3 montaj.py plan.json [--kontrol]
Plan dosyası alanları için references/montaj-plani.md. Yollar çalıştırılan klasöre göredir.

Her plan ayrı dosyaya kesilir, sonra concat demuxer ile birleşir. Aynı girdiyi tek filter_complex içinde birden çok kez
kullanmak ses karışıklığı yaratır (kapanışta yanlış cümle duyuldu); bu yüzden tek geçiş yok.
"""
import json
import math
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from renk import filtre as renk_filtresi  # noqa: E402


def calis(*a):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *map(str, a)], check=True)


def ses_var(yol: Path) -> bool:
    return bool(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", str(yol)],
                               capture_output=True, text=True).stdout.strip())


def atempo(hiz: float) -> str:
    # atempo tek adımda 0.5–2 arası; dışındakiler zincirlenir.
    adim, h = [], hiz
    while h > 2:
        adim.append("atempo=2.0")
        h /= 2
    while h < 0.5:
        adim.append("atempo=0.5")
        h /= 0.5
    adim.append(f"atempo={h:.4f}")
    return ",".join(adim)


def plan_kes(i: int, p: dict, film: dict, tmp: Path) -> tuple[Path, float]:
    W, H = film.get("boyut", [1080, 1920])
    fps = film.get("fps", 30)
    out = tmp / f"p{i:03d}.mov"
    if "siyah" in p:  # siyah ara (logo öncesi nefes, sahne ayırıcı)
        d = p["siyah"]
        calis("-f", "lavfi", "-i", f"color=c=black:s={W}x{H}:r={fps}:d={d}", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
              "-t", d, "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", out)
        return out, d
    hiz = p.get("hiz", 1.0)
    d = (p["son"] - p["bas"]) / hiz
    z0, z1 = p.get("zoom", film.get("zoom", [1.0, 1.06]))  # varsayılan: tüm planlarda hafif içeri itiş
    ox, oy = p.get("odak", [0.5, 0.5])
    renk = p.get("renk", film.get("renk"))
    vf = [f"setpts=PTS/{hiz}" if hiz != 1 else "setpts=PTS-STARTPTS",
          f"fps={fps}",
          f"scale={W}:{H}:force_original_aspect_ratio=increase",
          f"scale=w='trunc(iw*({z0}+({z1}-{z0})*t/{d:.3f})/2)*2':h='trunc(ih*({z0}+({z1}-{z0})*t/{d:.3f})/2)*2':eval=frame",
          f"crop={W}:{H}:(iw-ow)*{ox}:(ih-oh)*{oy}",
          "setsar=1"]
    rf = renk_filtresi(renk, p.get("gren", film.get("gren", False)))
    if rf:
        vf.append(rf)
    vf.append("format=yuv420p")
    kaynak = Path(p["dosya"])
    seviye = p.get("ses", film.get("plan_sesi", 0.0))
    if ses_var(kaynak) and seviye > 0:
        af = ["-af", f"{atempo(hiz) + ',' if hiz != 1 else ''}aresample=48000,aformat=channel_layouts=stereo,volume={seviye},"
                     f"afade=t=in:d=0.04,afade=t=out:st={max(0, d - 0.06):.3f}:d=0.06"]
        girdi_ses, harita = [], ["-map", "0:v:0", "-map", "0:a:0"]
    else:
        af = []
        girdi_ses, harita = ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"], ["-map", "0:v:0", "-map", "1:a:0"]
    calis("-ss", p["bas"], "-to", p["son"], "-i", kaynak, *girdi_ses, *harita, "-vf", ",".join(vf), *af, "-t", f"{d:.3f}",
          "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", out)
    return out, d


def main():
    plan_yolu = Path(sys.argv[1])
    film = json.loads(plan_yolu.read_text())
    cikis = Path(film.get("cikis", f"cikti/{plan_yolu.stem}.mp4"))
    cikis.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        parcalar, t, kesimler = [], 0.0, []
        for i, p in enumerate(film["planlar"]):
            yol, d = plan_kes(i, p, film, tmp)
            parcalar.append(yol)
            t += d
            kesimler.append(round(t, 2))
            print(f"plan {i + 1}/{len(film['planlar'])}  {d:5.2f} sn  -> {t:6.2f}", flush=True)
        if film.get("son_kart"):  # Hyperframes'te render edilmiş logo/kapanış kartı
            yol = tmp / "son.mov"
            W, H = film.get("boyut", [1080, 1920])
            kart = Path(film["son_kart"])
            ses_g = [] if ses_var(kart) else ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
            harita = ["-map", "0:v:0", "-map", "0:a:0" if not ses_g else "1:a:0"]
            calis("-i", kart, *ses_g, *harita, "-vf", f"fps={film.get('fps', 30)},scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p",
                  "-shortest", "-c:v", "libx264", "-crf", "16", "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", yol)
            parcalar.append(yol)
        liste = tmp / "liste.txt"
        liste.write_text("".join(f"file '{p}'\n" for p in parcalar))
        ham = tmp / "ham.mov"
        calis("-f", "concat", "-safe", "0", "-i", liste, "-c", "copy", ham)
        sure = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(ham)],
                                    capture_output=True, text=True, check=True).stdout)

        # Ses: plan sesleri (foley/ortam) + müzik + yerleştirilen efektler/seslendirme; sosyal medya için -14 LUFS.
        girdiler, filtre, etiket = ["-i", ham], ["[0:a]aresample=48000[p]"], ["[p]"]
        m = film.get("muzik")
        if m:
            girdiler += ["-ss", m.get("bas", 0), "-i", m["dosya"]]
            fo = m.get("fade_out", 2.0)
            filtre.append(f"[1:a]aresample=48000,aformat=channel_layouts=stereo,volume={m.get('ses', 0.8)},"
                          f"afade=t=in:d={m.get('fade_in', 0.5)},afade=t=out:st={max(0, sure - fo):.2f}:d={fo},atrim=0:{sure:.3f}[m]")
            etiket.append("[m]")
        for j, e in enumerate(film.get("efektler", [])):
            idx = girdiler.count("-i")
            girdiler += ["-i", e["dosya"]]
            ms = max(0, int(e["an"] * 1000))
            filtre.append(f"[{idx}:a]aresample=48000,aformat=channel_layouts=stereo,volume={e.get('ses', 1.0)},adelay={ms}|{ms}[e{j}]")
            etiket.append(f"[e{j}]")
        filtre.append(f"{''.join(etiket)}amix=inputs={len(etiket)}:normalize=0:duration=first,loudnorm=I={film.get('lufs', -14)}:TP=-1.5:LRA=11[a]")
        calis(*girdiler, "-filter_complex", ";".join(filtre), "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "slow", "-crf", "18",
              "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
              "-c:a", "aac", "-b:a", "192k", "-dn", "-movflags", "+faststart", cikis)
    print("bitti:", cikis, f"{sure:.1f} sn", "kesimler:", kesimler)
    if "--kontrol" in sys.argv:
        orta = []
        b = 0.0
        for k in kesimler:
            orta.append((b + k) / 2)
            b = k
        kareler = cikis.with_name(cikis.stem + "-kontrol.jpg")
        n = len(orta)
        kol = min(6, n)
        sec = "+".join(f"eq(n\\,{int(x * film.get('fps', 30))})" for x in orta)
        calis("-i", cikis, "-vf", f"select='{sec}',scale=270:480,tile={kol}x{math.ceil(n / kol)}", "-frames:v", "1", "-fps_mode", "vfr", kareler)
        print("kontrol:", kareler)


if __name__ == "__main__":
    main()
