"use strict";
const $ = (id) => document.getElementById(id);
const repo = "https://github.com/aivideoweb/best-free-minimax-h3/blob/main/";
let data,
  selected = "all",
  active = null,
  trigger = null;
let english = new URLSearchParams(location.search).get("lang") === "en";
const t = (zh, en) => (english ? en : zh);
const el = (tag, text, className) => {
  const node = document.createElement(tag);
  if (text) node.textContent = text;
  if (className) node.className = className;
  return node;
};
function link(text, url) {
  const a = el("a", text);
  a.href = url;
  a.target = "_blank";
  a.rel = "noopener noreferrer";
  return a;
}
function title(entry) {
  return english ? entry.title : entry.title_zh;
}
function caseLinks(entry) {
  return [
    link(t("原帖与作者", "Original post"), entry.source_url),
    link(t("完整提示词", "Full prompt"), entry.prompt_url),
    link(
      t("解析与 5 秒改写", "Notes + 5s practice"),
      repo + "docs/x-community-showcase.md#" + entry.id.toLowerCase(),
    ),
  ];
}
function openPlayer(entry, button) {
  active = entry;
  trigger = button;
  $("player-title").textContent = title(entry);
  $("player-links").replaceChildren(...caseLinks(entry));
  $("playback-status").textContent = t("正在载入视频…", "Loading video…");
  $("video").poster = entry.thumbnail_url;
  $("video").src = entry.video_url;
  $("player").showModal();
  $("video")
    .play()
    .catch(() => {
      if (active === entry && !$("video").error)
        $("playback-status").textContent = t(
          "点击播放器中的播放按钮开始。",
          "Press play in the video controls to start.",
        );
    });
}
function stopPlayer() {
  const old = trigger;
  active = null;
  $("video").pause();
  $("video").removeAttribute("src");
  $("video").removeAttribute("poster");
  $("video").load();
  if (old?.isConnected) old.focus();
}
function closePlayer() {
  $("video").pause();
  $("player").close();
}
$("close").addEventListener("click", closePlayer);
$("player").addEventListener("cancel", (event) => { event.preventDefault(); closePlayer(); });
$("player").addEventListener("close", stopPlayer);
$("player").addEventListener("click", (event) => {
  if (event.target !== $("player")) return;
  const r = $("player").getBoundingClientRect();
  if (
    event.clientX < r.left ||
    event.clientX > r.right ||
    event.clientY < r.top ||
    event.clientY > r.bottom
  )
    closePlayer();
});
$("video").addEventListener("playing", () => {
  $("playback-status").textContent = "";
});
$("video").addEventListener("error", () => {
  if (active)
    $("playback-status").textContent = t(
      "视频暂时无法播放，请通过下方原帖观看。",
      "This video is unavailable. Watch it through the original post below.",
    );
});
function render() {
  document.documentElement.lang = english ? "en" : "zh-CN";
  $("filters").setAttribute("aria-label", t("场景分类", "Workflow filters"));
  $("gallery").setAttribute("aria-label", t("视频案例", "Video examples"));
  document.title = t(
    "MiniMax H3 视频案例 · VideoWeb AI",
    "MiniMax H3 Video Gallery · VideoWeb AI",
  );
  $("language").textContent = t("English", "简体中文");
  $("repo").textContent = t("工具包与提示词 ↗", "Tools & prompts ↗");
  $("repo").href = repo + (english ? "README.md" : "README_zh.md");
  $("heading").textContent = t(
    "先看一个好镜头，再试自己的想法。",
    "Find a shot worth trying.",
  );
  $("intro").textContent = t(
    "按场景选案例，点击图片在线播放；打开解析，学习怎样把创意改成一个 5 秒镜头。",
    "Choose a scene and click a preview to watch. Open the notes to turn an idea into a five-second shot.",
  );
  $("credit").textContent = t(
    "视频来自各自创作者，不代表本目录免费工具的实测结果。原帖、完整提示词和作者信息随案例保留。",
    "Videos belong to their creators and are not tests of the listed free tools. Each case links to its author, original post and full prompt.",
  );
  $("affiliate").textContent = t("联盟推广合作 ↗", "Affiliate cooperation ↗");
  $("close").setAttribute("aria-label", t("关闭播放器", "Close player"));
  $("filters").replaceChildren();
  for (const w of [
    { id: "all", name: "All scenes", name_zh: "全部场景" },
    ...data.workflows,
  ]) {
    const b = el("button", english ? w.name : w.name_zh);
    b.type = "button";
    b.setAttribute("aria-pressed", String(selected === w.id));
    b.onclick = () => {
      selected = w.id;
      render();
      $("filters")
        .querySelectorAll("button")
        [
          [...$("filters").children].findIndex(
            (x) => x.textContent === (english ? w.name : w.name_zh),
          )
        ]?.focus();
    };
    $("filters").append(b);
  }
  const workflow = data.workflows.find((w) => w.id === selected);
  const entries = workflow
    ? workflow.cases.map((id) =>
        data.entries.find((e) => e.id === "XH3-" + String(id).padStart(3, "0")),
      )
    : data.entries;
  $("status").textContent = t(
    `${entries.length} 个视频案例 · 点击图片播放`,
    `${entries.length} video examples · Click a preview to play`,
  );
  $("gallery").replaceChildren();
  for (const entry of entries) {
    const card = el("article", null, "card"),
      button = el("button", null, "preview");
    button.type = "button";
    button.setAttribute("aria-label", t("播放：", "Play: ") + title(entry));
    const img = el("img");
    img.src = entry.thumbnail_url;
    img.alt = title(entry);
    img.loading = "lazy";
    button.append(img, el("span", t("▶ 播放视频", "▶ Play video"), "play"));
    button.onclick = () => openPlayer(entry, button);
    const body = el("div", null, "body");
    body.append(
      el("h2", title(entry)),
      el("div", "@" + entry.author, "author"),
      el("p", english ? entry.lesson : entry.lesson_zh),
    );
    const links = el("div", null, "links");
    links.append(...caseLinks(entry));
    body.append(links);
    card.append(button, body);
    $("gallery").append(card);
  }
}
$("language").onclick = () => {
  english = !english;
  const url = new URL(location.href);
  url.searchParams.set("lang", english ? "en" : "zh");
  history.replaceState(null, "", url);
  if (data) render();
};
fetch("cases.json")
  .then((r) => {
    if (!r.ok) throw Error();
    return r.json();
  })
  .then((value) => {
    data = value;
    render();
  })
  .catch(() => {
    $("status").textContent = t(
      "案例加载失败，请刷新页面，或打开上方仓库查看。",
      "Could not load examples. Reload or visit the repository above.",
    );
  });
