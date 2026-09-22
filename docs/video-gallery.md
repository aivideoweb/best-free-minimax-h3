# 视频案例展示页 / Video gallery

[打开视频案例展示页](https://boogeyyagaa.github.io/minimax-h3-video-gallery/) · [English](https://boogeyyagaa.github.io/minimax-h3-video-gallery/?lang=en)

展示页提供 15 个视频案例、六类场景筛选和中英文切换。桌面三列、平板两列、手机单列；点击图片弹出播放器，按 Esc、点击关闭按钮或遮罩关闭，播放随即停止。

The gallery includes 15 videos, six workflow filters and Chinese/English switching. Click a preview to open the player; Escape, the close button or the backdrop closes it and stops playback.

README 中的案例图片现已直接链接到 MP4，不依赖本展示页。浏览器可能直接播放，也可能下载。此独立展示页保留供已有链接访问。

README previews now link directly to MP4 files. The browser may play or download the video. This standalone gallery remains available for existing links.

## 发布与更新 / Publishing and updates

页面托管在 [BoogeyYagaa/minimax-h3-video-gallery](https://github.com/BoogeyYagaa/minimax-h3-video-gallery)，源码与案例仍由本仓库维护。

更新本仓库后，在个人展示仓库 **Actions → Publish video gallery → Run workflow** 重新发布。部署任务会读取本仓库 `main` 分支，生成案例数据并发布 `site/`，无需手工复制文件。

The personal hosting repository builds this repository’s `main` branch. After updating the source, run **Publish video gallery** in the hosting repository’s Actions tab. No manual copying is required.

## 本地预览 / Local preview

在仓库根目录执行 / Run from the repository root:

```sh
python3 scripts/build_gallery.py
python3 -m http.server 8794 --directory site
```

然后打开 / Then open `http://localhost:8794`.

## 持续维护 / Maintenance

案例来自 `docs/x-community-sources.json`，场景分类来自 `data/workflows.json`。修改这些文件后运行构建脚本；部署时也会重新生成 `site/cases.json`。不需要维护第二份案例列表。

Cases and workflow assignments are generated from the existing catalogs during deployment. Do not edit `site/cases.json` directly.

视频直接引用作者的媒体地址，不复制或重新托管。外部链接失效或浏览器不支持播放时，播放器保留原帖入口。案例暂未提供独立字幕轨或完整文字稿。

Videos use the creators’ external media URLs. If a URL expires or playback is unsupported, use the original-post link in the player. Separate captions or transcripts are not yet available.
