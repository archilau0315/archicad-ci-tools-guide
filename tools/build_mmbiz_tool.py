# -*- coding: utf-8 -*-
"""生成「微信图片回填工具」页面。

背景：公众号编辑器会过滤外链图片，图片必须先落到微信自己的图床（mmbiz.qpic.cn）。
未认证订阅号没有上传 API，所以用「后台批量上传 → 复制 → 回填地址」的折中办法：
把手工步骤压缩成一次多选上传 + 两次粘贴。

用法：
    python build_mmbiz_tool.py            # 默认读 CI Tools完全指南_公众号文章.md
    python build_mmbiz_tool.py 其他.md
"""
import io
import os
import re
import sys

import build_article as B

# 小尺寸截图适当放大，保证菜单文字可读（值直接写进 img 的 inline style）
WIDTH_HINT = {
    "07_tools_menu.jpg": "min-width:min(100%,520px)",
    "05_cabinet_types.jpg": "min-width:min(100%,560px)",
}

IMG_STYLE = ("max-width:100%;height:auto;display:block;"
             "margin:24px auto;border-radius:8px;")


def slotify(body):
    """把正文里的本地图片替换成待回填的空图位，返回 (body, slots)"""
    slots = []

    def repl(m):
        src, alt = m.group(1), m.group(2)
        name = os.path.basename(src)
        remote = B.IMG_MAP.get(name, name)
        n = len(slots) + 1
        style = IMG_STYLE + (WIDTH_HINT.get(remote, "") + ";" if remote in WIDTH_HINT else "")
        slots.append({"n": n, "file": name, "local": "images/" + name, "remote": remote})
        return (f'<img data-slot="{n}" data-name="{remote}" data-file="{name}" src=""'
                f' alt="{alt}" style="{style}">')

    body = re.sub(r'<img src="([^"]+)" alt="([^"]*)">', repl, body)
    return body, slots


PAGE_CSS = """
* { box-sizing:border-box; }
body { margin:0; background:#f4f5f7; color:#25272b;
  font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;
  font-size:15px; line-height:1.75; }
.wrap { max-width:1040px; margin:0 auto; padding:28px 20px 120px; }
h1 { font-size:23px; margin:0 0 6px; }
.sub { color:#6b7078; font-size:13.5px; margin-bottom:22px; }
.card { background:#fff; border:1px solid #e6e8ec; border-radius:12px;
  padding:20px 22px; margin-bottom:18px; }
.card h2 { font-size:16.5px; margin:0 0 12px; display:flex; align-items:center; gap:8px; }
.num { display:inline-flex; width:24px; height:24px; border-radius:50%;
  background:#2f6f8f; color:#fff; font-size:13px; align-items:center;
  justify-content:center; flex:0 0 24px; }
ol, ul { margin:8px 0 0; padding-left:22px; }
li { margin-bottom:6px; }
kbd { background:#eef0f3; border:1px solid #dcdfe4; border-bottom-width:2px;
  border-radius:5px; padding:1px 6px; font-size:12.5px; font-family:inherit; }
#pastebin { min-height:110px; border:2px dashed #c3cad2; border-radius:10px;
  padding:14px; background:#fafbfc; color:#6b7078; font-size:13.5px; outline:none; }
#pastebin:focus { border-color:#2f6f8f; background:#fff; }
.thumbs { display:grid; grid-template-columns:repeat(auto-fill,minmax(120px,1fr)); gap:10px; }
.thumb { border:1px solid #e6e8ec; border-radius:8px; overflow:hidden; background:#fafbfc; }
.thumb img { width:100%; height:74px; object-fit:cover; display:block; }
.thumb span { display:block; font-size:11.5px; color:#6b7078; padding:4px 6px;
  white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.status { font-size:13.5px; padding:10px 14px; border-radius:8px; margin-top:12px;
  background:#f6f7f8; color:#4a4f56; }
.status.ok { background:#eaf6ee; color:#1e6b38; }
.status.warn { background:#fdf3e7; color:#8a5418; }
.map { display:grid; grid-template-columns:44px 1fr 1fr; gap:8px 12px;
  align-items:center; margin-top:14px; font-size:13px; }
.map .h { font-weight:600; color:#4a4f56; font-size:12.5px; }
.map select { width:100%; padding:5px 8px; border:1px solid #d8dce2;
  border-radius:6px; font-size:12.5px; background:#fff; }
.map img { width:100%; height:52px; object-fit:cover; border-radius:6px;
  border:1px solid #e6e8ec; background:#fafbfc; }
.bar { position:fixed; left:0; right:0; bottom:0; z-index:50; display:flex; gap:16px;
  align-items:center; justify-content:center; flex-wrap:wrap;
  background:#fff; border-top:1px solid #e6e8ec; padding:12px 20px;
  box-shadow:0 -2px 12px rgba(0,0,0,.06); }
button { font:inherit; font-weight:600; cursor:pointer; border:none; border-radius:8px;
  padding:10px 22px; background:#2f6f8f; color:#fff; white-space:nowrap; }
button:hover { background:#28607c; }
button:disabled { opacity:.45; cursor:not-allowed; }
.article-box { border:1px solid #e6e8ec; border-radius:10px; padding:20px;
  max-height:420px; overflow:auto; background:#fff; }
.miss { background:#fff3f3 !important; border-color:#e7a6a6 !important; }
"""

PAGE_JS = r"""
const tpl = document.getElementById('tpl');
const slots = Array.from(tpl.content.querySelectorAll('img[data-slot]'));
const pastebin = document.getElementById('pastebin');
const statusEl = document.getElementById('status');
const mapEl = document.getElementById('map');
const previewEl = document.getElementById('preview');
const copyBtn = document.getElementById('copyBtn');
let urls = [];
let mapping = slots.map((_, i) => i);

function setStatus(msg, kind) {
  statusEl.className = 'status' + (kind ? ' ' + kind : '');
  statusEl.innerHTML = msg;
}

/* 从粘贴内容里按出现顺序抓出微信图床地址 */
function extractUrls(html, text) {
  const found = [];
  if (html) {
    const doc = new DOMParser().parseFromString(html, 'text/html');
    doc.querySelectorAll('img').forEach(img => {
      const u = img.getAttribute('src') || img.getAttribute('data-src') || '';
      if (u.indexOf('mmbiz.qpic.cn') > -1) found.push(u);
    });
  }
  if (!found.length) {
    const re = /https?:\/\/mmbiz\.qpic\.cn\/[^\s"'<>)\\]+/g;
    let m;
    while ((m = re.exec((html || '') + ' ' + (text || ''))) !== null) found.push(m[0]);
  }
  return found.filter((u, i) => found.indexOf(u) === i);
}

function renderMap() {
  mapEl.innerHTML = '';
  const head = ['#', '文章图位（应出现）', '已识别的上传图'];
  head.forEach(t => {
    const d = document.createElement('div');
    d.className = 'h'; d.textContent = t; mapEl.appendChild(d);
  });
  slots.forEach((slot, i) => {
    const n = document.createElement('div');
    n.textContent = i + 1;
    n.style.cssText = 'font-weight:600;color:#2f6f8f';
    mapEl.appendChild(n);

    const local = document.createElement('img');
    local.src = 'images/' + slot.dataset.file;
    local.title = slot.dataset.name;
    mapEl.appendChild(local);

    const sel = document.createElement('select');
    sel.innerHTML = '<option value="-1">— 未选 —</option>' +
      urls.map((u, k) => '<option value="' + k + '">图 ' + (k + 1) + '：' + u.slice(-28) + '</option>').join('');
    sel.value = String(mapping[i]);
    sel.onchange = () => { mapping[i] = parseInt(sel.value, 10); renderPreview(); };
    mapEl.appendChild(sel);
  });
}

function renderPreview() {
  const box = document.getElementById('previewBody');
  box.innerHTML = '';
  const frag = tpl.content.cloneNode(true);
  const imgs = frag.querySelectorAll('img[data-slot]');
  let filled = 0;
  imgs.forEach((img, i) => {
    const k = mapping[i];
    if (k > -1 && urls[k]) { img.src = urls[k]; filled++; }
  });
  box.appendChild(frag);
  copyBtn.disabled = filled !== slots.length;
  const ok = filled === slots.length;
  setStatus(ok
    ? '✓ ' + filled + ' / ' + slots.length + ' 个图位已就位，可以复制了。'
    : '已识别 <b>' + urls.length + '</b> 张上传图，已填 <b>' + filled + '</b> / ' +
      slots.length + ' 个图位。缺的请在右侧下拉框手动指定。');
  previewEl.style.display = 'block';
}

/* 供自动化测试调用 */
window.__extract = function (html, text) {
  urls = extractUrls(html, text);
  mapping = slots.map((_, i) => i);
  renderMap(); renderPreview();
  return urls;
};

pastebin.addEventListener('paste', e => {
  const html = e.clipboardData.getData('text/html');
  const text = e.clipboardData.getData('text/plain');
  e.preventDefault();
  pastebin.textContent = '';
  urls = extractUrls(html, text);
  mapping = slots.map((_, i) => i);
  if (!urls.length) {
    setStatus('没抓到 mmbiz 图片地址。确认复制的是公众号编辑器里的图片（不是本地文件路径），再试一次。', 'warn');
    return;
  }
  renderMap(); renderPreview();
});

pastebin.addEventListener('dragover', e => e.preventDefault());

function inlineStyles(root) {
  const rules = [];
  const sheet = document.getElementById('articleCss').sheet;
  for (const r of sheet.cssRules) if (r.type === 1) rules.push(r);
  for (const rule of rules) {
    if (!rule.selectorText) continue;
    let matched;
    try { matched = root.querySelectorAll(rule.selectorText); } catch (err) { continue; }
    for (const el of matched) {
      for (let i = 0; i < rule.style.length; i++) {
        const p = rule.style[i];
        if (!el.style.getPropertyValue(p)) {
          el.style.setProperty(p, rule.style.getPropertyValue(p), rule.style.getPropertyPriority(p));
        }
      }
    }
  }
}

copyBtn.addEventListener('click', async () => {
  const art = document.getElementById('previewBody');
  const clone = art.cloneNode(true);
  inlineStyles(clone);
  clone.querySelectorAll('*').forEach(el => {
    el.removeAttribute('id');
    el.removeAttribute('class');
    Array.from(el.attributes).forEach(a => {
      if (a.name.indexOf('data-') === 0) el.removeAttribute(a.name);
    });
  });
  const html = clone.innerHTML;
  const text = clone.innerText;
  try {
    await navigator.clipboard.write([new ClipboardItem({
      'text/html': new Blob([html], { type: 'text/html' }),
      'text/plain': new Blob([text], { type: 'text/plain' })
    })]);
  } catch (e) {
    const r = document.createRange();
    r.selectNodeContents(art);
    const s = window.getSelection();
    s.removeAllRanges(); s.addRange(r);
    document.execCommand('copy');
  }
  copyBtn.textContent = '✓ 已复制，去公众号粘贴';
  setTimeout(() => { copyBtn.textContent = '📋 复制最终版（含微信图片）'; }, 2200);
});
"""


def build(md_path="CI Tools完全指南_公众号文章.md", out_path="微信图片回填工具.html"):
    md = io.open(md_path, encoding="utf-8").read()
    body, slots = slotify(B.convert(md))
    title = re.search(r"^# (.+)$", md, re.M)
    title = title.group(1) if title else "文章"

    # 文章 CSS 里的 img[src*=...] 规则在替换地址后失效，宽度已写进 inline style，故去掉
    article_css = re.sub(r'^img\[src[^\n]*\n', '', B.CSS, flags=re.M)

    thumbs = "\n".join(
        f'<div class="thumb"><img src="{s["local"]}" alt=""><span>{s["n"]}. {s["remote"]}</span></div>'
        for s in slots
    )

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>微信图片回填工具 · {title}</title>
<style>{PAGE_CSS}</style>
<style id="articleCss">{article_css}</style>
</head>
<body>
<div class="wrap">
<h1>微信图片回填工具</h1>
<div class="sub">公众号会过滤外链图片，图片必须先落进微信自己的图床。三步走完，图片就不会再变空白。</div>

<div class="card">
  <h2><span class="num">1</span>在公众号后台把 10 张图一次传上去</h2>
  <ol>
    <li>公众号后台 → 新建图文 → 光标点进正文区。</li>
    <li>点编辑器工具栏的「图片」→「本地上传」→ 进到本文件夹的 <code>images</code> 目录，
        <b>按住 Ctrl 依次点选 01 → 10 这 10 个文件</b>（顺序很重要，决定后面的图位对应）。</li>
    <li>点「确定」，等 10 张图全部上传完（缩略图都出来，不要中途刷新）。</li>
    <li>正文里现在有 10 张图了，<kbd>Ctrl+A</kbd> 全选 → <kbd>Ctrl+C</kbd> 复制。</li>
    <li>回到本页，粘贴到下面的虚线框里。</li>
  </ol>
  <div class="thumbs" style="margin-top:14px">{thumbs}</div>
</div>

<div class="card">
  <h2><span class="num">2</span>粘贴刚才复制的内容</h2>
  <div id="pastebin" contenteditable="true">在这里按 Ctrl+V ……（只用来读地址，粘完不会留下内容）</div>
  <div id="status" class="status">等待粘贴。识别到 10 张微信图床图片后，会自动填进文章图位。</div>
</div>

<div class="card">
  <h2><span class="num">3</span>核对图位并复制最终版</h2>
  <div class="map" id="map"></div>
  <div id="preview" class="article-box" style="display:none;margin-top:16px">
    <div id="previewBody"></div>
  </div>
</div>

<div class="bar">
  <button id="copyBtn" disabled>📋 复制最终版（含微信图片）</button>
  <span class="sub" style="margin:0">复制后回公众号编辑器：<kbd>Ctrl+A</kbd> 删除刚才的 10 张图 → <kbd>Ctrl+V</kbd></span>
</div>
</div>

<template id="tpl">{body}</template>
<script>{PAGE_JS}</script>
</body>
</html>"""
    io.open(out_path, "w", encoding="utf-8").write(html)
    print(f"已生成 {out_path}  [图位 {len(slots)} 个]")
    for s in slots:
        print(f"  {s['n']:>2}. {s['remote']:<24} ← {s['file']}")
    return out_path


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    src = args[0] if args else "CI Tools完全指南_公众号文章.md"
    out = "微信图片回填工具.html"
    if "--out" in sys.argv:
        i = sys.argv.index("--out")
        if i + 1 < len(sys.argv):
            out = sys.argv[i + 1]
    build(os.path.abspath(src), out)
