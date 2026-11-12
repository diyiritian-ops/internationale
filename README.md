# 国际歌 · 76 个版本

**一首歌，七十六个样子。**

《国际歌》的旋律和歌词早就属于全人类了（公有领域）。这里放的是 76 个由 AI 生成的演绎版本 —— 不同情绪、不同编曲、不同唱法，总时长 7 小时 15 分，全部可在线播放、可直接下载。

> 想直接听：打开 [在线播放页](https://diyiritian-ops.github.io/internationale/)（手机电脑都行）。
> 想批量拿走：`git clone` 或者点右上角 **Code → Download ZIP**（约 400 MB）。

## 里面有什么

| 分组 | 首数 | 时长 | 说明 |
|---|---|---|---|
| `songs/111/` | 13 | 约 1 小时 15 分 | 第一批实验，偏人声清唱 |
| `songs/222/` | 28 | 约 2 小时 40 分 | 第二批，编曲更满 |
| `songs/cherry-cherie/` | 35 | 约 3 小时 20 分 | 最完整的一组，含一个原始版（`00.m4a`） |

每首 4 分 27 秒到 6 分 29 秒，Opus 编码、48 kHz 立体声、128 kbps，`.m4a` 容器。

> 播放兼容性：Edge / Chrome / Firefox 直接能放。**Safari 可能不出声**（它不认 MP4 里的 Opus），下载下来用任何播放器都能听。

## 怎么听

1. **在线**：<https://diyiritian-ops.github.io/internationale/> —— 点任意一首就播，支持上一首/下一首、拖进度、逐首下载
2. **本地**：下载 ZIP 解压，`songs/` 里全是标准音频文件
3. **自己搭**：整个仓库就是静态页面，扔到任何静态托管上都能跑（`index.html` + `songs.json` + `songs/`）

## 文件说明

```
songs/111/01.m4a … 13.m4a        ← 第一批 13 首
songs/222/01.m4a … 28.m4a        ← 第二批 28 首
songs/cherry-cherie/00.m4a       ← 原始版
songs/cherry-cherie/01.m4a … 35.m4a
songs.json                       ← 清单：分组、标题、时长、大小、原始文件名
index.html                       ← 在线播放页（读 songs.json）
```

`songs.json` 里每首都有 `source` 字段，记录它在本机时的原始文件名，方便你对回自己的记录。

## 怎么来的

这些音频是用自制的批量工具生成的：把一段录音切成 6 秒的小段、逐段送进 Suno 生成，再在 Studio 里按时间线拼回一整首。

工具在这里，开源、单文件、装了就能用：
<https://github.com/diyiritian-ops/suno-uploader>

每首都跑了不同的参数（移调、切片、并发），所以听感差异不小 —— 这也是为什么会有 76 个版本。

## 权利说明

- **词曲**：*L'Internationale*（1871 / 1888）早已进入公有领域。
- **这些录音**：AI 生成的演绎，本项目按 **CC0 1.0** 释出 —— 随便用、随便改、不用署名（见 [LICENSE](LICENSE)）。
- 如果你认为其中某个版本侵犯了你的权利，开个 issue，我删。

详细免责见 [NOTICE.md](NOTICE.md)。

## 相关链接

| 用途 | 链接 |
|---|---|
| 在线播放 | https://diyiritian-ops.github.io/internationale/ |
| 本仓库 | https://github.com/diyiritian-ops/internationale |
| 生成工具（开源） | https://github.com/diyiritian-ops/suno-uploader |
| 工具一键安装 | https://raw.githubusercontent.com/diyiritian-ops/suno-uploader/main/src/Suno-OneClick-Uploader.user.js |
