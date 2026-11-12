# 在线播放页

单文件、零依赖的播放器：读 `songs.json`，点歌即播。

## 怎么用

| 场景 | 做法 |
|---|---|
| 直接听 | 打开 <https://diyiritian-ops.github.io/internationale/> |
| 本地听 | 必须起个静态服务（`fetch('songs.json')` 走 `file://` 会被浏览器拦）：`npx serve .` 或 `python -m http.server` |
| 换地方托管 | 整个仓库扔上去就行，路径全是相对的 |

## 加歌

1. 把音频放进 `songs/<分组>/<NN>.m4a`
2. 在 `songs.json` 里加一条：

```json
{
  "group": "111",
  "groupTitle": "111 组",
  "index": 14,
  "file": "songs/111/14.m4a",
  "title": "L'Internationale · 111 组 14",
  "seconds": 343.8,
  "mmss": "5:44",
  "bytes": 5500000,
  "source": "111 (14).m4a"
}
```

`index` 决定排序和显示编号，`file` 是相对路径，`source` 只用来对回原始文件名。

## 键盘

| 键 | 作用 |
|---|---|
| `空格` | 播放 / 暂停 |
| `←` `→` | 快退 / 快进 5 秒 |
| `↑` `↓` | 上一首 / 下一首 |
