#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""生成《国际歌 76 个版本》的封面与 15 秒竖版短视频。

用法：
    python build_release.py

输出（放到 ../发布包/）：
    封面-1080x1920.png
    封面-1080x1080.png
    预告-15s.mp4         1080x1920 / H.264 / AAC / -14 LUFS
依赖：Pillow + ffmpeg（C:\\Tools\\ffmpeg\\bin）
"""
import os
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FFMPEG = r"C:\Tools\ffmpeg\bin\ffmpeg.exe"
FFPROBE = r"C:\Tools\ffmpeg\bin\ffprobe.exe"
FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"
FONT_REG = r"C:\Windows\Fonts\msyh.ttc"

HERE = Path(__file__).resolve().parent          # songs-repo/tools/
REPO = HERE.parent                               # songs-repo/
OUT = REPO.parent / "发布包"                       # 工作目录下的发布包/
WORK = OUT / "_work"

W, H = 1080, 1920
INK = (236, 232, 246)
INK2 = (168, 159, 192)
MUTED = (111, 103, 135)
ACCENT = (168, 85, 247)
BG_TOP = (42, 27, 69)
BG_BOT = (14, 11, 20)


def font(path, size):
    return ImageFont.truetype(path, size, index=0)


def vgrad(w, h, top, bot):
    img = Image.new("RGB", (1, h))
    px = img.load()
    for y in range(h):
        t = y / max(1, h - 1)
        px[0, y] = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
    return img.resize((w, h), Image.BILINEAR)


def draw_tracked(draw, xy, text, fnt, fill, tracking=0):
    """字间距（PIL 没有原生 letterspacing）"""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking
    return x


def centered(draw, y, text, fnt, fill, tracking=0):
    if tracking:
        width = sum(draw.textlength(c, font=fnt) for c in text) + tracking * (len(text) - 1)
    else:
        width = draw.textlength(text, font=fnt)
    x = (W - width) / 2
    draw_tracked(draw, (x, y), text, fnt, fill, tracking)
    return width


def make_waveform(track, width=980, height=200):
    out = WORK / "wave.png"
    subprocess.run(
        [FFMPEG, "-y", "-v", "error", "-i", str(track), "-filter_complex",
         f"showwavespic=s={width}x{height}:colors=#a855f7:split_channels=0",
         "-frames:v", "1", str(out)],
        check=True,
    )
    return Image.open(out).convert("RGBA")


def build_cover(wave, size, name):
    w, h = size
    img = vgrad(w, h, BG_TOP, BG_BOT).convert("RGBA")
    d = ImageDraw.Draw(img)

    # 顶部一条淡淡的高光
    glow = Image.new("RGBA", (w, 520), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for i in range(520):
        a = int(46 * (1 - i / 520) ** 2)
        gd.line([(0, i), (w, i)], fill=(124, 58, 237, a))
    img.alpha_composite(glow, (0, 0))

    scale = h / H  # 以 1920 版为基准等比缩放

    f_kicker = font(FONT_REG, int(40 * scale))
    f_title = font(FONT_BOLD, int(210 * scale))
    f_latin = font(FONT_REG, int(38 * scale))
    f_num = font(FONT_BOLD, int(58 * scale))
    f_sub = font(FONT_REG, int(42 * scale))
    f_url = font(FONT_REG, int(34 * scale))

    y = int(230 * scale)
    centered(d, y, "AI 演绎 · 词曲公有领域", f_kicker, INK2, tracking=2)

    y = int(330 * scale)
    centered(d, y, "国际歌", f_title, INK)

    y = int(600 * scale)
    centered(d, y, "L'INTERNATIONALE", f_latin, ACCENT, tracking=6)

    # 波形
    wave_h = int(210 * scale)
    wave_w = int(w * 0.9)
    wv = wave.resize((wave_w, wave_h), Image.LANCZOS)
    wx = (w - wave_w) // 2
    wy = int(820 * scale)
    img.alpha_composite(wv, (wx, wy))

    d = ImageDraw.Draw(img)
    y = wy + wave_h + int(90 * scale)
    centered(d, y, "76 个版本", f_num, INK)

    y += int(100 * scale)
    centered(d, y, "来自一段录音的 76 种可能", f_sub, INK2)

    y += int(90 * scale)
    centered(d, y, "7 小时 15 分 · 400 MB · CC0", f_sub, MUTED)

    y = h - int(190 * scale)
    centered(d, y, "在线试听", f_url, ACCENT, tracking=2)
    y += int(52 * scale)
    centered(d, y, "diyiritian-ops.github.io/internationale", f_url, MUTED)

    path = OUT / name
    img.convert("RGB").save(path, quality=95)
    print(f"  ✓ {path.name}  {img.size[0]}x{img.size[1]}")
    return path


def build_video(cover, track, out_name, seconds=15.0):
    """封面缓慢推近 + 真实音频段落 + 淡入淡出"""
    src_start = 42.0  # 从 42 秒处取一段（副歌附近，具体看曲目）
    out = OUT / out_name
    zoom = (
        f"scale={W*2}:{H*2},zoompan=z='min(zoom+0.00035,1.10)':"
        f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={int(seconds*30)}:s={W}x{H}:fps=30"
    )
    afade_out = seconds - 1.2
    cmd = [
        FFMPEG, "-y", "-v", "error",
        "-loop", "1", "-t", f"{seconds}", "-i", str(cover),
        "-ss", f"{src_start}", "-t", f"{seconds}", "-i", str(track),
        "-filter_complex",
        f"[0:v]{zoom},format=yuv420p[v];"
        f"[1:a]afade=t=in:st=0:d=1.0,afade=t=out:st={afade_out}:d=1.2,"
        f"loudnorm=I=-14:TP=-1.5:LRA=11[a]",
        "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart", "-shortest",
        str(out),
    ]
    subprocess.run(cmd, check=True)
    dur = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(out)], capture_output=True, text=True).stdout.strip()
    mb = out.stat().st_size / 1048576
    print(f"  ✓ {out.name}  {float(dur):.1f}s  {mb:.1f} MB")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    WORK.mkdir(parents=True, exist_ok=True)
    track = REPO / "songs" / "cherry-cherie" / "00.m4a"
    if not track.exists():
        print("找不到源曲目", track)
        sys.exit(1)

    print("波形…")
    wave = make_waveform(track)

    print("封面…")
    c1 = build_cover(wave, (1080, 1920), "封面-1080x1920.png")
    build_cover(wave, (1080, 1080), "封面-1080x1080.png")

    print("视频…")
    build_video(c1, track, "预告-15s.mp4", 15.0)

    for f in WORK.glob("*"):
        f.unlink()
    WORK.rmdir()
    print(f"\n全部完成 → {OUT}")


if __name__ == "__main__":
    main()
