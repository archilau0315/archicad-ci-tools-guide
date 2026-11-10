#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CI Tools 教程站生成器

输入：clean.json（清洗后的 Markdown）+ raw/（本地图片）
输出：静态多页站点（首页 + 15 个工具分册 + 全量索引）

用法：
    python3 build_site.py <base_dir> <out_dir>
"""
import io, json, os, re, shutil, sys
from collections import defaultdict

# 分册定义：key → (英文名, 中文名, 一句话说明, 图标)
BOOKS = {
    "annotate":    ("Annotate", "文字格式", "全项目文字大小写、字体批量统一", "Aa"),
    "transformer": ("Transformer", "项目镜像", "一键镜像整个项目，含 2D 标注", "⇄"),
    "timetracker": ("Time Tracker", "工时统计", "记录任务工时，与报价对比", "◷"),
    "detail":      ("Detail Elements", "二维详图", "拖拽式参数化详图构件库", "▤"),
    "keynotes":    ("Keynotes", "规范注释", "注释数据库自动挂接与明细表", "❝"),
    "metadata":    ("MetaData", "属性管理", "属性与分类的批量操作面板", "◈"),
    "quantities":  ("Quantities", "工程量算量", "从模型出清单，Recipe 自动分配", "∑"),
    "cabinets":    ("Cabinets", "橱柜木作", "一个对象搞定所有橱柜类型", "▦"),
    "doors":       ("Doors+Windows", "门窗", "异形门窗样式与尺寸捕捉", "⌸"),
    "coverings":   ("Coverings", "覆面层", "墙板柱贴 3D 覆面皮", "▨"),
    "electrical":  ("Electrical", "电气", "智能符号、回路与明细表", "⚡"),
    "stairs":      ("Stairs", "楼梯", "自由楼梯与栏杆关联", "⇱"),
    "structural":  ("Structural", "结构构件", "桁架、框架与连接件", "⌗"),
    "sites":       ("Sites", "场地景观", "边界、退让与植物布置", "⛿"),
    "fitout":      ("Fitout", "室内布置", "房间一键配齐家具", "⌸"),
}
BOOKS_EN = {
    "annotate":    "Batch text case and font formatting across the whole project",
    "transformer": "Mirror an entire project in one click, 2D annotations included",
    "timetracker": "Log time per task and compare against quoted hours",
    "detail":      "Drag-and-drop parametric 2D detail component library",
    "keynotes":    "Note database auto-attached by element attributes, with schedules",
    "metadata":    "Palette for bulk editing properties and classifications",
    "quantities":  "Bill of quantities from a live model, recipes auto-assign values",
    "cabinets":    "One configurable object covers every cabinet type",
    "doors":       "Non-standard door and window styles with size snapping",
    "coverings":   "3D surface skins on walls, slabs, columns and roofs",
    "electrical":  "Smart electrical symbols, circuits and schedules",
    "stairs":      "Free-form stair design with associative railings",
    "structural":  "3D structural components: trusses, frames and fixings",
    "sites":       "Site boundaries, recession planes and plant placement",
    "fitout":      "Furnish a room in one click from a saved set",
}

ORDER = ["annotate", "transformer", "timetracker", "detail", "keynotes",
         "metadata", "quantities", "cabinets", "doors", "coverings",
         "electrical", "stairs", "structural", "sites", "fitout"]

CSS = """
:root{
  --accent:#2f6f8f; --accent2:#c9622a;
  --bg:#fbfbfa; --panel:#fff; --text:rgba(0,0,0,.95);
  --muted:rgba(0,0,0,.55); --line:rgba(0,0,0,.10);
  --ink:#1c1c1a; --paper:#f3f2ee;
  --sidebar-w:262px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;color:var(--text);line-height:1.75;font-size:15px;
  font-family:"Noto Sans SC",-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;
  background:radial-gradient(ellipse 70% 40% at 10% -10%,rgba(47,111,143,.10),transparent),
             radial-gradient(ellipse 54% 42% at 90% 2%,rgba(201,98,42,.07),transparent),var(--bg);
  background-attachment:fixed}
h1,h2,h3,h4{font-family:"Noto Serif SC","Source Han Serif SC","Songti SC",SimSun,Georgia,serif;
  color:var(--ink);letter-spacing:-.01em}
h1{font-size:clamp(26px,4.5vw,40px);font-weight:700;line-height:1.16;margin:0 0 14px}
h2{font-size:clamp(20px,2.8vw,26px);font-weight:700;margin:36px 0 14px;padding-bottom:10px;
  border-bottom:1px solid var(--line)}
h3{font-size:17px;font-weight:600;margin:26px 0 10px}
p{margin:0 0 13px}
a{color:var(--accent);text-decoration:none;border-bottom:1px solid rgba(47,111,143,.3)}
a:hover{border-bottom-color:var(--accent)}
strong{color:var(--ink);font-weight:600}
code{font-family:"Geist Mono",ui-monospace,Consolas,"Microsoft YaHei",monospace;font-size:.88em;
  background:rgba(47,111,143,.08);padding:2px 6px;border-radius:4px;color:#1d4d63;
  font-variant-numeric:tabular-nums}
pre{background:var(--paper);border:1px solid var(--line);border-radius:8px;padding:14px 16px;
  overflow-x:auto;margin:14px 0;font-size:13px;line-height:1.6}
pre code{background:none;padding:0;color:var(--ink)}
ul,ol{margin:0 0 14px;padding-left:22px}
li{margin-bottom:6px}
li::marker{color:var(--accent)}
table{border-collapse:collapse;width:100%;margin:14px 0;font-size:13.5px}
th,td{padding:9px 12px;text-align:left;border:1px solid var(--line);vertical-align:top}
th{background:var(--paper);font-weight:600;color:var(--ink)}
.table-wrap{overflow-x:auto;margin:16px 0;border-radius:8px;border:1px solid var(--line)}
.table-wrap table{margin:0;border:none}
img{max-width:100%;height:auto;display:block;margin:18px 0;border-radius:8px;
  border:1px solid var(--line);background:var(--paper)}
figure{margin:20px 0}
figcaption{font-size:12.5px;color:var(--muted);margin-top:-10px}

/* 布局 */
.layout{display:grid;grid-template-columns:var(--sidebar-w) 1fr;gap:0;min-height:100vh}
.sidebar{position:sticky;top:0;height:100vh;overflow-y:auto;background:var(--panel);
  border-right:1px solid var(--line);padding:22px 0 40px}
.brand{padding:0 20px 18px;border-bottom:1px solid var(--line);margin-bottom:14px}
.brand a{color:var(--ink);border:none;display:block}
.brand-t{font-family:"Noto Serif SC","Songti SC",serif;font-size:17px;font-weight:700;
  color:var(--ink);line-height:1.3}
.brand-s{font-size:11.5px;color:var(--muted);letter-spacing:.06em;text-transform:uppercase;margin-top:3px}
.nav-h{font-size:11px;font-weight:600;letter-spacing:.09em;text-transform:uppercase;
  color:var(--muted);padding:14px 20px 6px}
.nav-h.en-only{display:none}
html[data-lang="en"] .nav-h.zh-only{display:none}
html[data-lang="en"] .nav-h.en-only{display:block}
.sidebar a{display:block;padding:7px 20px;font-size:13.5px;color:var(--muted);
  border-left:2px solid transparent;transition:background .18s,color .18s}
.sidebar a:hover{background:rgba(47,111,143,.06);color:var(--accent)}
.sidebar a.on{background:rgba(47,111,143,.09);color:var(--accent);
  border-left-color:var(--accent);font-weight:500}
.sidebar a .ic{display:inline-block;width:18px;font-size:11px;color:var(--accent);
  margin-right:6px;text-align:center}
.main{padding:0 40px 80px;max-width:900px}
.crumb{font-size:12.5px;color:var(--muted);padding:22px 0 4px}
.crumb a{color:var(--muted);border:none}
.crumb a:hover{color:var(--accent)}
.hero{padding:26px 0 30px;border-bottom:1px solid var(--line);margin-bottom:28px}
.hero .kicker{display:inline-block;font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;
  color:var(--accent);border:1px solid rgba(47,111,143,.28);border-radius:9999px;
  padding:3px 11px;margin-bottom:14px}
.hero p{font-size:16px;color:var(--muted);max-width:62ch;margin:0}
.meta{display:flex;gap:18px;flex-wrap:wrap;margin-top:16px;font-size:12.5px;color:var(--muted)}
.meta b{color:var(--ink);font-weight:600}
article{padding-bottom:40px}
.art{border-top:1px solid var(--line);padding-top:26px;margin-top:26px}
.art-h{display:flex;align-items:baseline;gap:10px;margin-bottom:6px}
.art-h h3{margin:0;font-size:18px}
.art-h .no{font-family:"Geist Mono",monospace;font-size:11.5px;color:var(--accent);
  background:rgba(47,111,143,.09);padding:2px 8px;border-radius:5px;flex-shrink:0}
.art-src{font-size:11.5px;color:var(--muted);margin-bottom:12px}
.pill{display:inline-block;font-size:11px;padding:2px 9px;border-radius:9999px;
  background:rgba(0,0,0,.05);color:var(--muted);margin-right:6px}
.vb{display:inline-block;margin-left:8px;padding:1px 6px;border-radius:4px;
  background:#f1e7d8;color:#8a5a1e;border:1px solid #e2d2ba;
  font-size:11px;font-weight:600;line-height:1.6;vertical-align:middle;
  letter-spacing:.02em;white-space:nowrap}
.vb-old{background:#f7e3e3;color:#9a3b3b;border-color:#e6c6c6}
.vb-note{margin:14px 0 0;padding:10px 14px;border-radius:10px;
  background:#fdf8f1;border:1px solid #f0e2cc;color:#7a5a2c;font-size:13.5px;line-height:1.7}
.vb-note b{color:#8a5a1e}

/* 首页卡片 */
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:14px;margin:20px 0}
.card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:18px 20px;
  box-shadow:0 1px 2px rgba(0,0,0,.04),0 8px 24px rgba(0,0,0,.05);
  transition:transform .22s cubic-bezier(.2,0,0,1),box-shadow .22s,border-color .22s}
.card:hover{transform:translateY(-2px);border-color:rgba(47,111,143,.32);
  box-shadow:0 4px 18px rgba(47,111,143,.09)}
.card a{color:inherit;border:none;display:block}
.card-h{display:flex;align-items:baseline;gap:8px;margin-bottom:5px}
.card-h .ic{font-size:13px;color:var(--accent);width:16px;text-align:center}
.card-h b{font-size:15.5px;color:var(--ink);font-weight:600}
.card-h span{font-size:12px;color:var(--muted)}
.card p{font-size:13px;color:var(--muted);margin:0 0 8px;line-height:1.55}
.card .n{font-family:"Geist Mono",monospace;font-size:11px;color:var(--accent)}
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:20px 0}
.step{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:16px}
.step .sn{font-family:"Geist Mono",monospace;font-size:11px;color:var(--accent);letter-spacing:.08em}
.step h4{margin:6px 0 6px;font-size:15px;font-weight:600}
.step p{font-size:13px;color:var(--muted);margin:0 0 8px}
.step code{font-size:11.5px;display:block;padding:6px 9px;background:var(--panel);
  border:1px solid var(--line);border-radius:6px;line-height:1.5;word-break:break-word}
.toc-list{list-style:none;padding:0;margin:16px 0;display:grid;
  grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:2px 24px}
.toc-list li{margin:0}
.toc-list a{display:block;padding:6px 0;font-size:13.5px;color:var(--muted);border-bottom:1px solid var(--line)}
.toc-list a:hover{color:var(--accent)}
.toc-list .tg{font-family:"Geist Mono",monospace;font-size:11px;color:var(--accent);margin-right:8px}
.foot{border-top:1px solid var(--line);padding:22px 0;font-size:12.5px;color:var(--muted);margin-top:40px}
/* ===== 双语切换 ===== */
.lang-switch { position:fixed; top:16px; right:16px; z-index:120;
  background:rgba(255,255,255,0.94); border:1px solid var(--line); border-radius:9999px;
  padding:4px; display:flex; gap:2px; box-shadow:0 4px 20px rgba(0,0,0,.10);
  backdrop-filter:blur(16px); -webkit-backdrop-filter:blur(16px); }
.lang-switch button { border:none; background:none; cursor:pointer; font-family:inherit;
  font-size:12px; font-weight:500; color:var(--muted); padding:6px 14px; border-radius:9999px;
  min-width:44px; min-height:32px; transition:background .2s,color .2s; }
.lang-switch button:hover { background:rgba(47,111,143,.08); color:var(--accent); }
.lang-switch button.active { background:var(--accent); color:#fff; }
.lang-switch button:focus-visible { outline:2px solid var(--accent); outline-offset:2px; }

/* 原文对照 */
.orig-toggle { margin-top:14px; border-top:1px solid var(--line); padding-top:10px; }
.orig-toggle > summary { cursor:pointer; font-size:12.5px; color:var(--muted);
  list-style:none; display:inline-flex; align-items:center; gap:6px;
  padding:5px 0; transition:color .2s; }
.orig-toggle > summary::-webkit-details-marker { display:none; }
.orig-toggle > summary::before { content:'▸'; transition:transform .2s; display:inline-block; }
.orig-toggle[open] > summary::before { transform:rotate(90deg); }
.orig-toggle > summary:hover { color:var(--accent); }
.orig-body { margin-top:10px; padding:14px 16px; background:var(--paper);
  border-left:2px solid var(--line); border-radius:0 8px 8px 0; font-size:13.5px; }
.orig-body img { margin:12px 0; }
.orig-label { font-size:11px; letter-spacing:.08em; text-transform:uppercase;
  color:var(--muted); margin-bottom:8px; font-weight:600; }
/* 双语切换：默认中文，英文模式整体反转。特异性需高于 .block 规则 */
html:not([data-lang="en"]) .zh-only { display:inline; }
html:not([data-lang="en"]) .zh-only.block { display:block; }
html:not([data-lang="en"]) .en-only { display:none; }
html[data-lang="en"] .zh-only,
html[data-lang="en"] .zh-only.block { display:none !important; }
html[data-lang="en"] .en-only { display:inline; }
html[data-lang="en"] .en-only.block { display:block; }
@media(max-width:640px){
  .lang-switch { top:auto; bottom:16px; right:16px; }
}

.missing{margin:16px 0;padding:12px 14px;border:1px dashed rgba(0,0,0,.18);border-radius:8px;
  background:var(--paper);color:var(--muted);font-size:12.5px}
.menubtn{display:none}
@media(max-width:1000px){
  .layout{grid-template-columns:1fr}
  .sidebar{position:static;height:auto;border-right:none;border-bottom:1px solid var(--line);
    padding:16px 0;max-height:60vh}
  .sidebar .nav-h,.sidebar a{font-size:13px}
  .main{padding:0 18px 60px}
  .steps{grid-template-columns:1fr}
}
@media(max-width:640px){
  .main{padding:0 15px 48px}
  h2{margin:26px 0 12px}
  .grid{grid-template-columns:1fr}
  .toc-list{grid-template-columns:1fr}
}
"""

JS = """
(function(){
  // 侧栏当前项高亮
  var here = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.sidebar a').forEach(function(a){
    var href = (a.getAttribute('href')||'').split('/').pop();
    if(href === here) a.classList.add('on');
  });
  // 移动端目录折叠
  var btn = document.getElementById('menubtn');
  var sb = document.getElementById('sidebar');
  if(btn && sb){
    btn.addEventListener('click', function(){
      var open = sb.classList.toggle('open');
      btn.textContent = open ? '收起目录' : '展开目录';
    });
  }
  // 目录内搜索
  var si = document.getElementById('q');
  if(si){
    si.addEventListener('input', function(){
      var q = si.value.toLowerCase().trim();
      document.querySelectorAll('.toc-list li').forEach(function(li){
        var t = li.textContent.toLowerCase();
        li.style.display = (q && t.indexOf(q) < 0) ? 'none' : '';
      });
    });
  }
})();


// ===== 双语切换 =====
(function(){
  var KEY = 'citools-lang';
  function apply(lang){
    document.documentElement.setAttribute('data-lang', lang);
    document.documentElement.setAttribute('lang', lang === 'zh' ? 'zh-CN' : 'en');
    var bz = document.getElementById('lang-zh'), be = document.getElementById('lang-en');
    if (bz) { bz.classList.toggle('active', lang === 'zh'); bz.setAttribute('aria-pressed', lang === 'zh' ? 'true':'false'); }
    if (be) { be.classList.toggle('active', lang === 'en'); be.setAttribute('aria-pressed', lang === 'en' ? 'true':'false'); }
    try { localStorage.setItem(KEY, lang); } catch(e){}
  }
  var lang = 'zh';
  try {
    var m = location.search.match(/[?&]lang=(zh|en)/);
    if (m) { lang = m[1]; }
    else if (localStorage.getItem(KEY)) { lang = localStorage.getItem(KEY); }
  } catch(e){}
  apply(lang);
  var bz = document.getElementById('lang-zh'), be = document.getElementById('lang-en');
  if (bz) bz.addEventListener('click', function(){ apply('zh'); });
  if (be) be.addEventListener('click', function(){ apply('en'); });
})();
"""


_ARTS = {}
_LINKIMG_LOCAL = {}
_ZH = {}


def load_zh(base):
    """载入中文译文：{articleId: {"title": ..., "md": ...}}"""
    p = f"{base}/zh_translations.json"
    if os.path.exists(p):
        try:
            _ZH.clear()
            _ZH.update(json.load(io.open(p, encoding="utf-8")))
        except Exception as e:
            print(f"  ! 中文译文载入失败: {e}")
    print(f"  中文译文已载入: {len(_ZH)} 篇")


def load_linkimg_map(base):
    """载入 图片即链接 的本地路径映射"""
    p = f"{base}/linkimg_ext.json"
    if os.path.exists(p):
        try:
            for k, v in json.load(io.open(p, encoding="utf-8")).items():
                if os.path.exists(f"{base}/raw/{v}"):
                    _LINKIMG_LOCAL[k] = f"img/{v}"
        except Exception:
            pass


def local_imgs(aid):
    """文章内图片 URL 列表（顺序与清洗时的 IMG 占位一致）"""
    body = _ARTS.get(aid, {}).get("body", "")
    urls = []
    for m in re.finditer(r'<img[^>]*src="([^"]+)"', body):
        u = m.group(1)
        if u.startswith("/"): u = "https://cadimage.zendesk.com" + u
        if u not in urls: urls.append(u)
    return urls



def zh_title_of(aid, fallback):
    """取中文标题，缺失则回退英文"""
    t = _ZH.get(aid)
    return t.get("title", fallback) if t else fallback


VB_RE = re.compile(r'ARCHICAD\s*(\d{2})|\bAC\s?(\d{2})\b', re.I)
VB_MAX_OLD = 26          # 只标 AC26 及更早；AC27 与 AC28 界面基本一致
VB_HISTORY = ("及更早版本", "迁移到", "更新概览", "网络研讨会录像")


def ver_badge(text):
    """标题里带旧版本号的，生成一个角标；AC27+ 不标。"""
    m = VB_RE.search(text or "")
    if not m:
        return ""
    ver = int(m.group(1) or m.group(2))
    if ver > VB_MAX_OLD:
        return ""
    cls = "vb vb-old" if any(h in text for h in VB_HISTORY) else "vb"
    tip = "该文基于旧版界面，操作路径可能已变" if cls.endswith("old") else "基于该版本的界面编写"
    return f'<span class="{cls}" title="{tip}">AC{ver}</span>'


VB_NOTE = """  <p class="vb-note">
    <span class="zh-only">标 <b>AC19–AC23</b> 的文章基于旧版界面编写：功能思路仍通用，但按钮位置和菜单名可能与当前版本不同。</span>
    <span class="en-only">Articles tagged <b>AC19–AC23</b> were written for older interfaces — the concepts still apply, but UI paths may differ from the current version.</span>
  </p>"""


def nav_item(href, ic, zh, en, cls=""):
    return (f'<a class="{cls}" href="{href}"><span class="ic">{ic}</span>'
            f'<span class="zh-only">{zh}</span>'
            f'<span class="en-only">{en}</span></a>')


def build_sidebar(active):
    """侧栏导航（双语）"""
    items = ['<div class="brand"><a href="index.html">'
             '<div class="brand-t"><span class="zh-only">CI Tools 完全指南</span>'
             '<span class="en-only">CI Tools Handbook</span></div>'
             '<div class="brand-s">Archicad Plugin Manual</div></a></div>',
             '<div class="nav-h zh-only block">开始</div><div class="nav-h en-only block">Start</div>',
             nav_item("index.html", "◈", "总览与快速开始", "Overview"),
             nav_item("all.html", "☰", "全量文章索引", "All Articles"),
             nav_item("guide.html", "★", "中文主线速查", "Quick Guide")]
    items.append('<div class="nav-h zh-only block">16 个工具</div><div class="nav-h en-only block">16 Tools</div>')
    for k in ORDER:
        en, zh, desc, ic = BOOKS[k]
        cls = " on" if k == active else ""
        items.append(nav_item(f"{k}.html", ic, f"{en} · {zh}", en, cls))
    items.append('<div class="nav-h zh-only block">关于</div><div class="nav-h en-only block">About</div>')
    items.append(nav_item("about.html", "ⓘ", "来源与说明", "Sources"))
    return '\n'.join(items)

def render_md(md):
    """Markdown → HTML（轻量，够用即可）"""
    lines = md.split("\n")
    out, i = [], 0
    in_list = False
    def close_list():
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False
    while i < len(lines):
        ln = lines[i]
        # 表格
        if ln.startswith("|") and i + 1 < len(lines) and re.match(r'^\|[\s:|-]+\|$', lines[i+1]):
            close_list()
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(lines[i]); i += 1
            def cells(r):
                return [c.strip().replace("|", "\\|") for c in r.strip().strip("|").split("|")]
            hdr = cells(rows[0])
            body = [cells(r) for r in rows[2:]]
            out.append('<div class="table-wrap"><table><thead><tr>' +
                       "".join(f"<th>{c}</th>" for c in hdr) + "</tr></thead><tbody>" +
                       "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in body) +
                       "</tbody></table></div>")
            continue
        # 代码块
        if ln.startswith("```"):
            close_list()
            i += 1; buf = []
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i]); i += 1
            i += 1
            out.append("<pre><code>" + "\n".join(buf) + "</code></pre>")
            continue
        # 标题
        m = re.match(r'^(#{1,6})\s+(.*)', ln)
        if m:
            close_list()
            lvl = len(m.group(1))
            out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>")
            i += 1; continue
        # 列表
        if re.match(r'^\s*[-*]\s+', ln):
            if not in_list:
                out.append("<ul>"); in_list = True
            out.append(f"<li>{inline(re.sub(r'^\s*[-*]\s+','',ln))}</li>")
            i += 1; continue
        if re.match(r'^\s*\d+\.\s+', ln):
            if not in_list:
                out.append("<ul>"); in_list = True
            out.append(f"<li>{inline(re.sub(r'^\s*\d+\.\s+','',ln))}</li>")
            i += 1; continue
        close_list()
        if ln.strip():
            out.append(f"<p>{inline(ln)}</p>")
        i += 1
    close_list()
    return "\n".join(out)


def inline(t):
    t = re.sub(r'!\[([^\]]*)\]\(([^)\s]+)\)', r'<img src="\2" alt="\1" loading="lazy">', t)
    # 图片即链接：%%IMGLINK<图片url>|<外链>%% → <a><img src=本地></a>
    t = re.sub(r'%%IMGLINK([^|%]+)\|([^%]+)%%',
               lambda m: f'<a href="{m.group(2)}" target="_blank" rel="noopener">'
                         f'<img src="{_LINKIMG_LOCAL.get(m.group(1), m.group(1))}" '
                         f'alt="" loading="lazy"></a>', t)
    t = re.sub(r'%%LINKIMG(https?://[^%]+)%%',
               lambda m: f'<a href="{m.group(1)}" target="_blank" rel="noopener">'
                         f'<img src="{_LINKIMG_LOCAL.get(m.group(1), m.group(1))}" '
                         f'alt="" loading="lazy"></a>', t)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank" rel="noopener">\1</a>', t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', t)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    return t


def page(title, body, active="", desc="", extra_head=""):
    side = build_sidebar(active)
    return f"""<!DOCTYPE html>
<html lang="zh-CN" data-lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{desc}">
<title>{title} · CI Tools 完全指南</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource/noto-serif-sc@5.3.0/chinese-simplified-700.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource-variable/geist-mono@5.2.5/index.css">
<style>{CSS}</style>
<link rel="stylesheet" href="search.css">
</head>
<body>
<div class="layout">
<aside class="sidebar" id="sidebar">
{side}
</aside>
<div class="lang-switch" role="group" aria-label="Language">
  <button type="button" id="lang-zh" class="active" aria-pressed="true">中文</button>
  <button type="button" id="lang-en" aria-pressed="false">EN</button>
</div>
<main class="main">
{extra_head}
{body}
<footer class="foot">
<span class="zh-only">CI Tools 完全指南 · 内容整理自 Central Innovation / Graphisoft 官方 MyCi 知识库（2026-10 更新）· 2026-11-05</span>
<span class="en-only">CI Tools Handbook · Content from the official Central Innovation / Graphisoft MyCi knowledge base (updated 2026-10) · 2026-11-05</span>
</footer>
</main>
</div>
<script>{JS}</script>
<script src="search-index.js"></script>
<script src="search.js"></script>
</body>
</html>"""


def main():
    base, out = sys.argv[1], sys.argv[2]
    clean = json.load(io.open(f"{base}/clean.json", encoding="utf-8"))
    arts = json.load(io.open(f"{base}/articles.json", encoding="utf-8"))
    _ARTS.clear(); _ARTS.update(arts)
    load_linkimg_map(base)
    load_zh(base)

    os.makedirs(out, exist_ok=True)
    os.makedirs(f"{out}/img", exist_ok=True)

    # 分组
    groups = defaultdict(list)
    for aid, v in clean.items():
        groups[v["cat"]].append(aid)

    # 写各分册
    stats = []
    for cat in ORDER:
        aids = groups.get(cat, [])
        if not aids: continue
        en, zh, desc, ic = BOOKS[cat]
        aids.sort(key=lambda a: (clean[a]["title"][:2].isdigit() is False, clean[a]["title"]))
        arts_html = []
        for i, aid in enumerate(aids, 1):
            v = clean[aid]
            md = v["md"]
            # 图片占位替换
            imgs = local_imgs(aid)
            for k, u in enumerate(imgs):
                fn = f"{aid}_{k}.jpg"
                if os.path.exists(f"{base}/raw/{fn}"):
                    md = md.replace(f"%%IMG{k}%%", f"\n\n![{v['title']} 示意图](img/{fn})\n\n")
                else:
                    md = md.replace(f"%%IMG{k}%%",
                        f"\n\n<div class=\"missing\">▢ 该图在官方源站已失效（原始链接 404）</div>\n\n")
            # 图片即链接的占位：渲染成可点图片
            def linkimg_sub(mo):
                url = mo.group(1)
                return f'<p><a href="{url}" target="_blank" rel="noopener">'
            # 中文译文优先，缺失则回退英文原文
            zt = _ZH.get(aid)
            if zt:
                zh_md = zt.get("md", "")
                for k, u in enumerate(local_imgs(aid)):
                    fn = f"{aid}_{k}.jpg"
                    if os.path.exists(f"{base}/raw/{fn}"):
                        zh_md = zh_md.replace(f"%%IMG{k}%%", f"\n\n![{v['title']} 示意图](img/{fn})\n\n")
                    else:
                        zh_md = zh_md.replace(f"%%IMG{k}%%", f"\n\n<div class=\"missing\">▢ 该图在官方源站已失效</div>\n\n")
                main_html = render_md(zh_md)
                zh_title = zt.get("title", v["title"])
            else:
                main_html = render_md(md)
                zh_title = v["title"]
            orig_html = render_md(md)
            src = f'<a href="{v["url"]}" target="_blank" rel="noopener">MyCi 官方原文 ↗</a>' if v.get("url") else ""
            arts_html.append(f"""
<div class="art" id="a-{aid}">
  <div class="art-h"><span class="no">{i:02d}</span>
    <h3 class="zh-only block">{zh_title}{ver_badge(zh_title)}</h3>
    <h3 class="en-only block">{v['title']}{ver_badge(v['title'])}</h3>
  </div>
  <div class="art-src">{src}</div>
  <div class="zh-only">{main_html}</div>
  <div class="en-only">{orig_html}</div>
  <details class="orig-toggle">
    <summary><span class="zh-only">英文原文对照</span><span class="en-only">Official English Original</span></summary>
    <div class="orig-body">
      <div class="orig-label"><span class="zh-only">官方英文原文</span><span class="en-only">Official English Original</span></div>
      {orig_html}
    </div>
  </details>
</div>""")
        pager = []
        for idx, k in enumerate(ORDER):
            if k in groups:
                pager.append((k, groups[k]))
        body = f"""
<div class="crumb"><a href="index.html"><span class="zh-only">总览</span><span class="en-only">Overview</span></a>
  / <span class="zh-only">{en} · {zh}</span><span class="en-only">{en}</span></div>
<div class="hero">
  <span class="kicker"><span class="zh-only">工具分册</span><span class="en-only">Reference Chapter</span></span>
  <h1>{en} · <span class="zh-only">{zh}</span></h1>
  <p class="zh-only">{desc}</p>
  <p class="en-only">{BOOKS_EN[cat]}</p>
  <div class="meta">
    <span><b>{len(aids)}</b> <span class="zh-only">篇教程</span><span class="en-only">articles</span></span>
    <span><b>{sum(clean[a]['len'] for a in aids)/10000:.1f}</b> <span class="zh-only">万字</span><span class="en-only">10k words</span></span>
    <span><b>{sum(len(local_imgs(a)) for a in aids)}</b> <span class="zh-only">张图</span><span class="en-only">images</span></span>
  </div>
{VB_NOTE if any(ver_badge(zh_title_of(a, clean[a]['title'])) for a in aids) else ''}
</div>
<article>
{"".join(arts_html)}
</article>
"""
        html = page(f"{en} · {zh}", body, active=cat,
                    desc=f"{en}（{zh}）完整中文教程：{desc}")
        io.open(f"{out}/{cat}.html", "w", encoding="utf-8").write(html)
        stats.append((cat, en, zh, len(aids), sum(len(local_imgs(a)) for a in aids)))

    print(f"生成分册 {len(stats)} 个")
    for cat, en, zh, n, im in stats:
        print(f"  {cat}.html  {en} · {zh}  {n} 篇 {im} 图")
    print("已生成 index.html / all.html")

    # 索引数据交给调用方
    gmap = {k: [{"id": a, "title": clean[a]["title"], "len": clean[a]["len"],
                 "url": clean[a]["url"]} for a in groups.get(k, [])] for k in ORDER}
    io.open(f"{base}/index_data.json", "w", encoding="utf-8").write(json.dumps({
        "groups": gmap, "stats": stats,
    }, ensure_ascii=False, indent=1))
    build_home(out, base, clean, gmap)
    build_all(out, base, gmap)
    build_guide(out, base)
    build_search_index(out)


def build_search_index(out):
    """生成全站搜索索引（search-index.js）"""
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from build_search_index import build
        build(out)
    except Exception as e:
        print(f"  ! 搜索索引生成失败: {e}")




def build_home(out, base, clean, g):
    """首页：总览 + 快速开始 + 工具卡片 + 分册目录"""
    total_art = sum(len(v) for v in g.values())
    total_img = sum(len(local_imgs(a)) for lst in g.values() for a in [x["id"] for x in lst])
    total_chars = sum(x["len"] for lst in g.values() for x in lst)

    cards = []
    for k in ORDER:
        en, zh, desc, ic = BOOKS[k]
        n = len(g.get(k, []))
        im = sum(len(local_imgs(a["id"])) for a in g.get(k, []))
        cards.append(f"""
<div class="card"><a href="{k}.html">
  <div class="card-h"><span class="ic">{ic}</span><b>{en}</b><span class="zh-only">{zh}</span></div>
  <p class="zh-only">{desc}</p>
  <p class="en-only">{BOOKS_EN[k]}</p>
  <div class="n"><span class="zh-only">{n} 篇 · {im} 图</span><span class="en-only">{n} articles · {im} images</span></div>
</a></div>""")

    toc = []
    for k in ORDER:
        en, zh, desc, ic = BOOKS[k]
        items = "".join(
            f'<li><a href="{k}.html#a-{x["id"]}"><span class="tg">{i:02d}</span>'
            f'<span class="zh-only">{zh_title_of(x["id"], x["title"])}</span>'
            f'<span class="en-only">{x["title"]}</span></a></li>'
            for i, x in enumerate(g.get(k, []), 1))
        toc.append(f"""
<h2>{en} · <span class="zh-only">{zh}</span> <span class="pill"><span class="zh-only block">{len(g.get(k,[]))} 篇</span><span class="en-only">{len(g.get(k,[]))} articles</span></span></h2>
<ul class="toc-list">{items}</ul>""")

    body = f"""
<div class="hero" style="border-bottom:none;padding-top:34px">
  <span class="kicker"><span class="zh-only">Archicad 插件工具包 · 完整教程</span><span class="en-only">Archicad Plugin Toolkit · Complete Manual</span></span>
  <h1><span class="zh-only">CI Tools 完全指南</span><span class="en-only">CI Tools Complete Handbook</span></h1>
  <p class="zh-only">Central Innovation CI Tools（2026 年起改名 Graphisoft ProKit）官方教程全量中文整理版 —— {total_art} 篇官方文档、{total_img} 张界面截图、{total_chars/10000:.1f} 万字，覆盖 16 个工具的全部功能细节。</p>
  <p class="en-only">The complete bilingual edition of the official Central Innovation CI Tools (renamed Graphisoft ProKit in 2026) manual — {total_art} articles, {total_img} interface screenshots, covering every feature across all 16 tools.</p>
  <div class="meta">
    <span><b>{total_art}</b> <span class="zh-only">篇教程</span><span class="en-only">articles</span></span>
    <span><b>{total_img}</b> <span class="zh-only">张官方截图</span><span class="en-only">screenshots</span></span>
    <span><b>{total_chars/10000:.1f}</b> <span class="zh-only">万字</span><span class="en-only">10k words</span></span>
    <span><b>16</b> <span class="zh-only">个工具</span><span class="en-only">tools</span></span>
  </div>
</div>

<h2><span class="zh-only">每次新项目必做 · 3 步</span><span class="en-only">3 steps for every new project</span></h2>
<div class="steps">
  <div class="step">
    <div class="sn">STEP 01</div>
    <h4><span class="zh-only">加载工作环境</span><span class="en-only">Load Work Environment</span></h4>
    <p class="zh-only">菜单栏和工具箱才会出现 CI Tools 条目</p>
    <p class="en-only">Makes the CI Tools entries appear in the menu and toolbox</p>
    <code>File &gt; Work Environment &gt; Ci Tools Profile XX</code>
  </div>
  <div class="step">
    <div class="sn">STEP 02</div>
    <h4><span class="zh-only">加载图库包</span><span class="en-only">Load Library Packs</span></h4>
    <p class="zh-only">AC29 起必须手动加载，否则工具内容为空</p>
    <p class="en-only">From AC29 library packs must be loaded manually, or tools appear empty</p>
    <code>File &gt; Library Manager &gt; Add &gt; Ci Tools Macros.libpack</code>
  </div>
  <div class="step">
    <div class="sn">STEP 03</div>
    <h4><span class="zh-only">加进工具箱</span><span class="en-only">Add to Toolbox</span></h4>
    <p class="zh-only">加完必须保存，否则下次开 Archicad 又没了</p>
    <p class="en-only">Remember to save the work environment, or it resets next launch</p>
    <code>Right-click Toolbox &gt; Toolbox Settings &gt; tick &gt; Save Work Environment</code>
  </div>
</div>

<h2>16 个工具</h2>
<div class="grid">
{"".join(cards)}
</div>

<h2>全量文章目录</h2>
<p style="color:var(--muted);font-size:13.5px">共 {total_art} 篇，点标题直达对应分册的具体文章。</p>
{"".join(toc)}
"""
    io.open(f"{out}/index.html", "w", encoding="utf-8").write(
        page("总览", body, active="index",
             desc="Archicad CI Tools 官方教程全量中文版：16 个工具、357 篇文档、1208 张界面截图"))


def build_all(out, base, g):
    """全量索引页"""
    secs = []
    for k in ORDER:
        en, zh, desc, ic = BOOKS[k]
        rows = "".join(
            f'<li><a href="{k}.html#a-{x["id"]}"><span class="tg">{i:02d}</span>'
            f'<span class="zh-only">{zh_title_of(x["id"], x["title"])}{ver_badge(zh_title_of(x["id"], x["title"]))}</span>'
            f'<span class="en-only">{x["title"]}{ver_badge(x["title"])}</span></a></li>'
            for i, x in enumerate(g.get(k, []), 1))
        secs.append(f"""
<h2>{en} · {zh} <span class="pill">{len(g.get(k,[]))} 篇</span></h2>
<ul class="toc-list">{rows}</ul>""")
    body = f"""
<div class="crumb"><a href="index.html"><span class="zh-only">总览</span><span class="en-only">Overview</span></a>
  / <span class="zh-only">全量文章索引</span><span class="en-only">All Articles</span></div>
<div class="hero">
  <span class="kicker"><span class="zh-only">全量索引</span><span class="en-only">Full Index</span></span>
  <h1><span class="zh-only">全部文章索引</span><span class="en-only">All Articles Index</span></h1>
  <p><span class="zh-only">共 {sum(len(v) for v in g.values())} 篇官方教程，按工具分册列出。</span>
     <span class="en-only">All {sum(len(v) for v in g.values())} official articles, listed by tool.</span></p>
</div>
{"".join(secs)}
"""
    io.open(f"{out}/all.html", "w", encoding="utf-8").write(
        page("全量文章索引", body, active="all",
             desc="CI Tools 官方教程全量文章索引"))


def build_guide(out, base):
    """中文主线速查页（中文完整 / 英文为导航指引）"""
    md = io.open(f"{base}/handbook_main.md", encoding="utf-8").read()
    body = render_md(md)
    en_nav = "".join(
        f'<li><a href="{k}.html"><span class="tg">{BOOKS[k][3]}</span>'
        f'{BOOKS[k][0]} — {BOOKS_EN[k]}</a></li>' for k in ORDER)
    en_body = f"""
<p>This quick guide is written in Chinese. The full official English documentation for
every tool is available in the reference chapters below — each chapter shows the Chinese
translation by default, with the official English original available under
<i>View original English</i> in every article.</p>
<h2>Browse by tool</h2>
<ul class="toc-list">{en_nav}</ul>
<p>Tip: use the <b>中文 / EN</b> switch at the top-right corner to toggle the language of
the interface and the article titles on any page.</p>"""
    html = page("中文主线速查", f"""
<div class="crumb"><a href="index.html">总览</a> / 中文主线速查</div>
<div class="hero">
  <span class="kicker"><span class="zh-only">中文主线</span><span class="en-only">Quick Guide</span></span>
  <h1><span class="zh-only">16 个工具操作要点</span><span class="en-only">CI Tools at a Glance</span></h1>
  <p class="zh-only">每个工具「干什么、入口在哪、关键步骤、坑在哪」的中文主线速查。完整细节见各工具分册（含官方原文与全部截图）。</p>
  <p class="en-only">A Chinese quick-start covering all 16 tools. Full detail lives in the
  reference chapters — each article keeps the official English original available for
  side-by-side reading.</p>
</div>
<article><div class="zh-only">{body}</div><div class="en-only">{en_body}</div></article>
""", active="guide", desc="CI Tools 16 个工具中文主线速查：操作要点、菜单路径、关键步骤")
    io.open(f"{out}/guide.html", "w", encoding="utf-8").write(html)


if __name__ == "__main__":
    main()
