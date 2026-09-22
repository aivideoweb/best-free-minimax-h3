# 视频案例展示页 / Video gallery

展示页提供 15 个视频案例、六类场景筛选和中英文切换。桌面三列、平板两列、手机单列；点击图片弹出播放器，按 Esc、点击关闭按钮或遮罩关闭，播放随即停止。

The gallery includes 15 videos, six workflow filters and Chinese/English switching. Click a preview to open the player; Escape, the close button or the backdrop closes it and stops playback.

## 公开访问 / Public access

**尚未确认上线。** 自动启用 GitHub Pages 时接口返回 404。仓库管理员需在 **Settings → Pages → Build and deployment → Source** 选择 **GitHub Actions**，再到 Actions 手动运行 **Publish video gallery**。部署成功后，使用任务输出的页面地址。

**Deployment is not yet confirmed.** The Pages setup API returned 404. A repository administrator needs to select **GitHub Actions** in **Settings → Pages → Build and deployment → Source**, then run **Publish video gallery** under Actions. Use the URL reported by the successful deployment.

默认项目地址预计为 `https://aivideoweb.github.io/best-free-minimax-h3/`，以部署输出为准，当前不将其作为已上线入口。

## 当前验证结果 / Current verification

已检查桌面三列、平板两列、手机单列，无横向溢出；筛选、中英文切换、弹窗开关及关闭后停止播放通过。浏览器试播外部视频时收到 403，尚未确认真实视频播放成功；播放器会提示失败并提供原帖链接。HTTP HEAD 的 200 不作为播放成功证据。

Responsive layout, filters, language switching, dialog controls and playback cleanup were checked. External video requests returned HTTP 403 in browser testing, so successful media playback is not yet verified.

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

视频直接引用作者的媒体地址，不复制或重新托管。外部链接失效或浏览器不支持播放时，播放器保留原帖入口。

Videos use the creators’ external media URLs. If a URL expires or playback is unsupported, use the original-post link in the player.
