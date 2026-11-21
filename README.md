# Vinci Video

**Vinci Studio'nun video kurgu sistemi. Claude'a takılır, Claude'u Vinci'nin kurgucusu yapar.**

© 2026 Vinci Studio. Tüm hakları saklıdır. Özel ve gizlidir. Kullanım koşulları için [LICENSE](LICENSE).

Ham çekimden teslime kadar her adım burada: Reels ve Shorts, sinematik marka filmi, anlatımlı 3D ve motion videolar,
çok dilli seslendirme, röportaj ve müşteri yorumu, altyazı, ses ve müzik, yapay zekâ ile üretim. Hepsinde Vinci'nin
kalite kapısı ve gerçek işlerden çıkan dersler var. Varsayılan çıktı Instagram Reels'tir (9:16, 1080×1920).

## Skill'ler

| Skill | Ne yapar |
|---|---|
| `vinci-video` | Giriş noktası: yönlendirme, Reels standartları, çalışma kuralları, kalite kapısı, dersler, **dosyayı adından bulma** |
| `marka-filmi` | Profesyonel çekimden sinematik marka filmi: çekim listesi, ses tasarımı, renk ön ayarları, ritme oturan otomatik montaj, logo kapanışı |
| `anlatimli-video` | 3D, motion graphics, açıklayıcı videolar; İngilizce ve çok dilli seslendirme, her dil için ayrı render |
| `shorts-klip` | Yayın/oyun/podcast kesitinden dikey klip: tarama, bölünmüş düzen, kanca, akan altyazı, vuruş efektleri |
| `reels-video` | Kodla tanıtım/reklam reels'i (HyperFrames + GSAP) |
| `roportaj-video` | Röportaj ve müşteri yorumu: HDR→SDR, hız, öncesi/sonrası, gizlilik bulanığı, altyazı |
| `transkript` | Yerel Whisper ile yazıya dökme, kelime zamanları, SRT |
| `seslendirme` | Kendi sesinle seslendirme: okuma metni, replik kesme, ducking |
| `ses-muzik` | Telifsiz efekt ve fon müziği sentezi, seviye ve karışım kuralları |
| `ai-video` | Yapay zekâ ile video üretimi: kredi disiplini ve doğruluk kontrolü |

HyperFrames skill'leri (`hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `media-use` ve diğerleri) kurulumda
kendi resmî kaynağından indirilir.

## Kurulum (yeni cihaz)

Gerekenler: macOS ya da Linux, [Claude Code](https://claude.com/claude-code). GitHub girişi gerekmez.

```bash
git clone https://github.com/kuzeyozel-1/vinci-video-skills.git ~/dev/vinci-video-skills
cd ~/dev/vinci-video-skills && ./install.sh
```

Kurulum eksik araçları (ffmpeg, Node 22+, Python, yt-dlp) Homebrew ile tamamlar. Ardından Python ortamını, Whisper
modelini (1,6 GB), fontları, ses efektlerini, HyperFrames skill'lerini ve Vinci skill'lerini kurar. Tekrar çalıştırmak
güvenlidir. Bitince Claude Code'u yeniden başlat.

| Komut | Ne yapar |
|---|---|
| `./install.sh --guncelle` | Depoyu çeker ve skill'leri yeniler |
| `./install.sh --modelsiz` | Whisper modelini indirmez (transkript gerekmiyorsa) |
| `./paketle.sh` | claude.ai için skill başına .zip üretir (Ayarlar → Yetenekler → Skills). Web'de ffmpeg ve Whisper olmadığı için tam güç Claude Code'dadır. |

**Eklenti olarak kurmak istersen** (Claude Code içinde):
```
/plugin marketplace add kuzeyozel-1/vinci-video-skills
/plugin install vinci-video@vinci-studio
```
Bu durumda ortak dosyalar için yine `./install.sh --eklenti` çalıştır. Skill'ler eklentiden gelir, `~/.claude/skills`'e kopyalanmaz.

## Kullanım

Claude'a doğal dille söylemen yeterli. Dosya yolu vermene gerek yok, **dosyanın adını söylemen yeterli**:

- "röportaj videosundan 30 saniyelik İngilizce altyazılı reels yap"
- "dünkü klinik çekimlerinden marka filmi çıkar, soğuk mavi renk, sonda logo"
- "bu metni İngilizce ve İspanyolca seslendirip 3D anlatımlı video yap"
- "kayit.m4a'dan 'ne alaka ya' repliğini kes"
- "yayının son 10 dakikasından komik bir Shorts çıkar"

Claude para ya da kredi harcayan adımlardan, yayından ve müşteriye göndermeden önce onay ister. Her işten önce bir önizleme gösterir.

## Ortak dosyalar

`~/.vinci-video/` (değiştirmek için `VINCI_VIDEO_EV` ortam değişkenini ayarla):

| Yol | İçerik |
|---|---|
| `.venv/` | Python ortamı: faster-whisper, numpy, pillow |
| `models/large-v3-turbo/` | Whisper modeli |
| `fontlar/` | Anton, Montserrat |
| `sesler/` | Sentez efektler |

## Erişim ve lisans

Depo herkese açık olarak görüntülenebilir, ancak içerik Vinci Studio'nun mülküdür. Görüntülenebilir olması kullanım izni
vermez. Kopyalama, dağıtma, değiştirerek yayımlama ve yapay zekâ eğitimi [LICENSE](LICENSE) gereği yazılı izne bağlıdır.
Skill'ler araç kısıtlaması olmadan çalışır (`allowed-tools`): Claude video işlerinde komut çalıştırmak ve dosya yazmak
için ayrıca izin istemez. Yayın ve harcama onayı yine kullanıcıdadır.

## Üçüncü taraf

Bu depo yalnız Vinci Studio'nun kendi içeriğini barındırır. Kurulumun indirdiği araçlar ve lisansları [UCUNCU-TARAF.md](UCUNCU-TARAF.md)'de.
