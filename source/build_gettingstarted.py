#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成 ProKit AC30 入门页，保留旧版 CI Tools 安装文档为折叠归档。"""
import io
import os
import re
from textwrap import dedent

from rebrand_prokit import rebrand_misc

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.abspath(os.path.join(HERE, "..", "site", "gettingstarted.html"))
DOWNLOAD = "https://www.graphisoft.com/en-at/downloads/add-ons/prokit/"
CORE = "https://help.graphisoft.com/AC/30/INT/Topics/960_Prokit/ProKit_Core/prokit_core_tools.html"
MARK = "<!-- prokit-gettingstarted-p2 -->"
LEGACY_START = "<!-- legacy-ci-tools:start -->"
LEGACY_END = "<!-- legacy-ci-tools:end -->"

HERO = """<div class="hero">
  <span class="kicker">AC30 · ProKit</span>
  <h1><span class="zh-only">Getting Started · 入门与安装</span><span class="en-only">Getting Started · Setup and Verification</span></h1>
  <p class="zh-only block">两个安装包、授权判断、安装自检、图库与版本兼容；旧版 CI Tools 文档保留在页尾归档</p>
  <p class="en-only block">Installers, eligibility, setup checks, libraries and version compatibility, with the legacy CI Tools archive below</p>
  <div class="meta">
    <span><b>33</b> <span class="zh-only">篇教程</span><span class="en-only">articles</span></span>
    <span><b>6</b> <span class="zh-only">篇 AC30 主线</span><span class="en-only">AC30 essentials</span></span>
    <span><b>27</b> <span class="zh-only">篇旧版归档</span><span class="en-only">legacy articles</span></span>
  </div>
</div>
"""

CSS = """
/* AC30 入门主线与旧版归档（P2） */
.legacy-install{margin-top:40px;border-top:1px solid var(--line);padding-top:20px}
.legacy-install>summary{cursor:pointer;font-family:"Noto Serif SC",serif;font-size:20px;
  font-weight:700;color:var(--ink);padding:8px 0}
.legacy-note{padding:12px 14px;border-left:3px solid var(--accent2);background:var(--paper);
  font-size:13px;margin:14px 0 22px}
"""

# 编号、锚点、中英标题、中文正文、英文正文、来源链接
ARTICLES = [
    ("01", "prokit-package", "先确认安装包与授权", "Choose a package and check eligibility", """
<p>AC30 起，原 CI Tools 由 <strong>Graphisoft ProKit</strong> 接续，并分为 Core 与 Suite 两个安装包。先确认订阅计划与所在市场，再决定下载哪一个；不是所有人都需要同时安装两个包。</p>
<div class="table-wrap"><table><thead><tr><th>安装包</th><th>包含工具</th><th>授权与市场</th></tr></thead><tbody>
<tr><td><strong>ProKit Core</strong></td><td>Annotate、Detail Elements、Time Tracker、Transformer</td><td>Studio：AT、BE、DK、FI、FR、DE、NL、NO、SE、CH；Collaborate：前述国家及 AU、NZ；Max：全球</td></tr>
<tr><td><strong>ProKit Suite</strong></td><td>Cabinets、Coverings、Doors + Windows、Electrical、Fitout、Keynotes、Metadata、Quantities、Site、Stairs、Structure</td><td>随 Archicad Collaborate / Max 订阅全球提供</td></tr>
</tbody></table></div>
<p>Core 并非在所有市场提供。LaunchPad、NZ Bracing、Labeller 不在两个安装包的单列清单中，不要因为旧项目用过它们，就默认 AC30 安装后仍会出现。</p>
""", """
<p>With AC30, the former CI Tools continue as <strong>Graphisoft ProKit</strong>, split into Core and Suite installers. Check your Archicad plan and market before downloading; you may need one package or both.</p>
<div class="table-wrap"><table><thead><tr><th>Package</th><th>Tools</th><th>Plans and markets</th></tr></thead><tbody>
<tr><td><strong>ProKit Core</strong></td><td>Annotate, Detail Elements, Time Tracker, Transformer</td><td>Studio: AT, BE, DK, FI, FR, DE, NL, NO, SE, CH; Collaborate: those markets plus AU and NZ; Max: worldwide</td></tr>
<tr><td><strong>ProKit Suite</strong></td><td>Cabinets, Coverings, Doors + Windows, Electrical, Fitout, Keynotes, Metadata, Quantities, Site, Stairs, Structure</td><td>Available worldwide with Archicad Collaborate and Max</td></tr>
</tbody></table></div>
<p>Core is not available in every market. LaunchPad, NZ Bracing and Labeller are not listed as part of either installer, so do not assume that they will appear after an AC30 installation.</p>
""", DOWNLOAD),
    ("02", "prokit-download", "从官方页面下载匹配版本", "Download the matching release", """
<p>只从 <a href="https://www.graphisoft.com/en-at/downloads/add-ons/prokit/" target="_blank" rel="noopener">Graphisoft ProKit 官方下载页</a> 获取安装包。本页核实的版本为 <strong>3001-1.2</strong>，发布日期为 <strong>2026-10-07</strong>；再次安装时，以官网当前列出的版本为准。</p>
<div class="table-wrap"><table><thead><tr><th>安装包</th><th>平台</th><th>官网标注大小</th></tr></thead><tbody>
<tr><td>Core</td><td>Windows（.exe）</td><td>81 MB</td></tr>
<tr><td>Core</td><td>macOS · Apple silicon</td><td>76 MB</td></tr>
<tr><td>Core</td><td>macOS · Intel</td><td>67 MB</td></tr>
<tr><td>Suite</td><td>以官网下载项为准</td><td>约 1 GB</td></tr>
</tbody></table></div>
<ol><li>确认目标为 <strong>Archicad 30</strong>，不要下载旧版 CI Tools 安装器代替。</li><li>按电脑平台选择 Core；Apple silicon 与 Intel 不要混选。</li><li>Core 下载页提供 INT / FRA / GER 语言包，按项目所用环境选择。</li><li>如已获 Suite 授权，再下载 Suite 安装包。</li></ol>
""", """
<p>Use only the <a href="https://www.graphisoft.com/en-at/downloads/add-ons/prokit/" target="_blank" rel="noopener">official Graphisoft ProKit download page</a>. The release verified for this guide is <strong>3001-1.2</strong>, dated <strong>2026-10-07</strong>; check the download page for the current release when reinstalling.</p>
<div class="table-wrap"><table><thead><tr><th>Package</th><th>Platform</th><th>Listed size</th></tr></thead><tbody>
<tr><td>Core</td><td>Windows (.exe)</td><td>81 MB</td></tr>
<tr><td>Core</td><td>macOS · Apple silicon</td><td>76 MB</td></tr>
<tr><td>Core</td><td>macOS · Intel</td><td>67 MB</td></tr>
<tr><td>Suite</td><td>See the download page</td><td>About 1 GB</td></tr>
</tbody></table></div>
<ol><li>Confirm that the target is <strong>Archicad 30</strong>; do not substitute a legacy CI Tools installer.</li><li>Select Core for your platform, keeping Apple silicon and Intel downloads separate.</li><li>Core is offered in INT, FRA and GER language packages; choose the one used by your project environment.</li><li>Download Suite as well if your plan includes it.</li></ol>
""", DOWNLOAD),
    ("03", "prokit-install", "安装 Core 与 Suite", "Install Core and Suite", """
<p>旧版依赖 Ci Installer 的流程不适用于这里的 AC30 主线。使用刚下载的 Graphisoft 安装包，并按安装器当下显示的提示操作。</p>
<ol><li>关闭正在运行的 Archicad 30，避免安装期间文件被占用。</li><li>运行 Core 安装包；如果要求选择 Archicad 实例，请选择正在使用的 Archicad 30。</li><li>按安装器提示完成安装，不要根据旧教程猜测或跳过新界面步骤。</li><li>需要 Suite 且已获授权时，再运行 Suite 安装包并重复检查。</li><li>启动 Archicad 30，查看是否出现 <strong>ProKit</strong> 菜单。Core 的常用入口为 <code>ProKit &gt; Annotate &gt; Replace</code>、<code>ProKit &gt; Transformer</code> 和 <code>ProKit &gt; Time Tracker &gt; Timer Palette</code>。</li></ol>
<p>只安装一个获授权的包也可以。Suite 命令名称以安装后的 ProKit 菜单为准，不要用旧版菜单名称推断新界面。</p>
""", """
<p>The legacy Ci Installer workflow does not describe this AC30 process. Run the Graphisoft packages you just downloaded and follow the prompts shown by the current installers.</p>
<ol><li>Close Archicad 30 before installation so that its files are not in use.</li><li>Run the Core installer. If asked to select an Archicad instance, choose the Archicad 30 installation you use.</li><li>Complete the installer as presented; do not guess or skip steps based on a legacy tutorial.</li><li>If you need Suite and your plan includes it, run the Suite installer and repeat the checks.</li><li>Start Archicad 30 and look for the <strong>ProKit</strong> menu. Core commands include <code>ProKit &gt; Annotate &gt; Replace</code>, <code>ProKit &gt; Transformer</code> and <code>ProKit &gt; Time Tracker &gt; Timer Palette</code>.</li></ol>
<p>Installing only the package covered by your plan is valid. For Suite, use the command names shown in the installed ProKit menu rather than assuming they match legacy menus.</p>
""", DOWNLOAD),
    ("04", "prokit-environment", "应用工作环境并检查图库包", "Apply the work environment and check libraries", """
<p>安装程序与项目环境是两件事。安装完成后，还要让当前项目能看到工具命令与所需图库。</p>
<ol><li>在 Archicad 的 Work Environment 中选择安装后出现的 <strong>ProKit 工作环境</strong>并应用。新配置文件的确切名称以安装结果为准；旧教程中的 <strong>Ci Tools Profile</strong> 仅用于 AC29 及更早版本。</li><li>打开 Library Manager，检查当前项目是否已加载所装工具需要的 ProKit 图库包；包名与数量以实际安装内容为准。</li><li><strong>Detail Elements 必须有 Detail Elements 图库包</strong>。工具入口在工具箱的 <strong>Detail Element</strong>，不是只在 ProKit 菜单里查找。</li><li>若工具箱没有 Detail Element，在 Toolbox Settings 中启用它，再保存工作环境，避免切换项目后丢失设置。</li></ol>
<p>不要直接照搬旧版 <code>Ci Tools Macros.libpack</code> 的名称或加载清单。若图库显示缺失，先回到归档文章判断旧项目原用的版本，再处理 AC30 项目。</p>
""", """
<p>Installing the add-on and preparing the project environment are separate tasks. After installation, the active project must also have access to the commands and required libraries.</p>
<ol><li>In Archicad's Work Environment, apply the installed <strong>ProKit work environment</strong>. Its exact profile name depends on the installed result; <strong>Ci Tools Profile</strong> in older tutorials applies to AC29 and earlier.</li><li>Open Library Manager and check that the project has the ProKit library packs required by the installed tools. Use the names and set supplied by your installation.</li><li><strong>Detail Elements requires the Detail Elements library pack</strong>. Its tool is <strong>Detail Element</strong> in the toolbox, not only a command in the ProKit menu.</li><li>If Detail Element is absent, enable it in Toolbox Settings and save the work environment so the setting survives a project change.</li></ol>
<p>Do not copy legacy <code>Ci Tools Macros.libpack</code> names or loading lists into AC30. For missing libraries in an older project, first identify its original version using the archive below.</p>
""", CORE),
    ("05", "prokit-check", "装完自检：按症状逐项排查", "Verify the installation by symptom", """
<p>建议先在一个空白测试项目中自检，不要直接拿正式项目试命令。</p>
<div class="table-wrap"><table><thead><tr><th>检查项 / 症状</th><th>优先处理</th></tr></thead><tbody>
<tr><td>没有 ProKit 菜单</td><td>确认安装目标是正在启动的 Archicad 30；重新运行对应安装包，并检查是否应用了 ProKit 工作环境。</td></tr>
<tr><td>有 Core，没有 Suite</td><td>先核对 Collaborate / Max 订阅与 Suite 安装记录，不要把 Core 当成 Suite 的替代品。</td></tr>
<tr><td>菜单存在，但 Detail Element 不在工具箱</td><td>在 Toolbox Settings 启用 Detail Element，加载 Detail Elements 图库包，然后保存工作环境。</td></tr>
<tr><td>图库对象缺失或不可用</td><td>在 Library Manager 检查缺失项，核对已加载的 ProKit 图库包与安装版本。</td></tr>
<tr><td>只有部分市场或计划可用</td><td>回到第 1 篇核对 Core 的国家与计划限制；这不是靠重装就能绕过的设置。</td></tr>
</tbody></table></div>
<p>自检通过的最小结果：ProKit 菜单可见、已安装工具的命令可打开、工具箱与图库无缺项。团队内记录 Archicad 版本、ProKit 版本和所装包，便于后续排错。</p>
""", """
<p>Run these checks in a blank test project before trying commands on production work.</p>
<div class="table-wrap"><table><thead><tr><th>Check / symptom</th><th>First action</th></tr></thead><tbody>
<tr><td>No ProKit menu</td><td>Confirm that you installed into the Archicad 30 instance being launched, rerun the relevant installer, and check the applied work environment.</td></tr>
<tr><td>Core is present but Suite is not</td><td>Check the Collaborate / Max plan and Suite installation. Core is not a substitute for Suite.</td></tr>
<tr><td>The menu exists but Detail Element is absent</td><td>Enable Detail Element in Toolbox Settings, load its library pack, and save the work environment.</td></tr>
<tr><td>Library objects are missing or unusable</td><td>Review missing items in Library Manager and match the loaded ProKit packs to the installed release.</td></tr>
<tr><td>Availability differs by market or plan</td><td>Recheck the Core restrictions in article 1; reinstalling does not remove plan or market limits.</td></tr>
</tbody></table></div>
<p>A minimal successful check means the ProKit menu is visible, installed commands open, and the toolbox and libraries have no missing items. Record the Archicad version, ProKit release and installed packages for team support.</p>
""", CORE),
    ("06", "prokit-collaboration", "团队协作与版本兼容警告", "Team collaboration and version compatibility", """
<p><strong>不要另存回旧版本。</strong>官方明确建议：使用了 ProKit 工具的项目不要 back-save 到旧 Archicad 版本。另存可能让工具数据、对象或设置无法正确保留。</p>
<p><strong>协作者必须使用匹配的插件版本。</strong>跨 Archicad 版本协作时，两端要按官方要求使用匹配的 ProKit 版本，否则可能出现 ProKit 警告或兼容问题。开始共享前，至少统一以下信息：</p>
<ul><li>Archicad 主版本与更新状态；</li><li>ProKit 的 Core / Suite 安装情况与版本号；</li><li>项目加载的图库包及缺失项检查结果；</li><li>负责升级与验证的人员，避免多人各自升级后立即互传。</li></ul>
<p>旧版归档包含 BIMcloud / BIM Server、离线安装和订阅激活教程，但它们是 AC24–AC29 的历史资料。<strong>不要把其中的旧部署步骤当作已经核实的 AC30 流程</strong>；服务器部署按团队当前环境与 Graphisoft 现行管理说明执行。</p>
""", """
<p><strong>Do not back-save.</strong> Graphisoft advises against saving projects that use ProKit tools back to an older Archicad version. Tool data, objects or settings may not survive that conversion correctly.</p>
<p><strong>Collaborators must use matching add-on versions.</strong> When working across Archicad versions, use the matching ProKit releases required by Graphisoft; otherwise ProKit warnings or compatibility problems may occur. Align at least these details before sharing:</p>
<ul><li>Archicad major version and update state;</li><li>Installed Core / Suite packages and ProKit release numbers;</li><li>Loaded library packs and missing-item checks;</li><li>Who owns the upgrade and verification, rather than everyone upgrading independently.</li></ul>
<p>The legacy archive includes BIMcloud / BIM Server, offline installation and subscription activation articles for AC24–AC29. <strong>Do not treat those legacy deployment steps as verified AC30 procedures</strong>; follow the current Graphisoft administration guidance for your team environment.</p>
""", DOWNLOAD),
]


def render_article(item):
    no, anchor, zh, en, body_zh, body_en, source = item
    return f'''<div class="art" id="a-{anchor}">
  <div class="art-h"><span class="no">{no}</span>
    <h3 class="zh-only block">{zh}</h3>
    <h3 class="en-only block">{en}</h3>
  </div>
  <div class="art-src"><a href="{source}" target="_blank" rel="noopener">Graphisoft ProKit ↗</a></div>
  <div class="zh-only block">{dedent(body_zh).strip()}</div>
  <div class="en-only block">{dedent(body_en).strip()}</div>
</div>'''


def legacy_body(text):
    if LEGACY_START in text:
        return text.split(LEGACY_START, 1)[1].split(LEGACY_END, 1)[0].strip()
    match = re.search(r"<article>\s*(.*?)\s*</article>", text, re.S)
    if not match:
        raise RuntimeError("gettingstarted.html 缺少 article 正文")
    return match.group(1).strip()


def main():
    text = io.open(PAGE, encoding="utf-8").read()
    legacy = legacy_body(text)
    old_count = len(re.findall(r'<div class="art" id="a-', legacy))
    if old_count != 27:
        raise RuntimeError(f"旧版归档应为 27 篇，实际 {old_count} 篇")

    start = text.index("<article>")
    end = text.index("</article>", start) + len("</article>")
    shell = text[:start] + "<article>\n</article>" + text[end:]
    shell, _ = rebrand_misc("gettingstarted.html", shell)
    shell = re.sub(
        r'<meta name="description" content="[^"]*">',
        '<meta name="description" content="ProKit AC30 入门：Core 与 Suite 授权、下载、安装、工作环境、图库、自检和版本兼容，附旧版 CI Tools 归档">',
        shell, count=1)
    shell, count = re.subn(r'<div class="hero">.*?(?=<article>)', HERO, shell, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError("hero 替换失败")
    if ".legacy-install{" not in shell:
        shell = shell.replace("</style>", CSS + "</style>", 1)

    toc = ['<h2><span class="zh-only">ProKit · AC30 安装与自检</span>'
           '<span class="en-only">ProKit for AC30 · Setup and Verification</span></h2>',
           '<ul class="toc-list">']
    for no, anchor, zh, en, _, _, _ in ARTICLES:
        toc.append(f'<li><a href="#a-{anchor}"><span class="tg">{no}</span>'
                   f'<span class="zh-only">{zh}</span><span class="en-only">{en}</span></a></li>')
    toc.append('</ul>')
    articles = "\n".join(render_article(item) for item in ARTICLES)
    archive = f'''<details class="legacy-install">
<summary><span class="zh-only">旧版 CI Tools 安装文档 · AC24–AC29（27 篇）</span><span class="en-only">Legacy CI Tools installation archive · AC24–AC29 (27 articles)</span></summary>
<p class="legacy-note"><span class="zh-only">以下保留旧版原文、旧锚点和配图，供老项目查证；不作为 AC30 ProKit 的安装依据。</span><span class="en-only">The original text, anchors and images are retained for legacy projects; they are not the AC30 ProKit setup procedure.</span></p>
{LEGACY_START}
{legacy}
{LEGACY_END}
</details>'''
    body = "\n".join([MARK] + toc + [articles, archive])
    shell = shell.replace("<article>\n</article>", "<article>\n" + body + "\n</article>", 1)
    io.open(PAGE, "w", encoding="utf-8").write(shell)
    total = len(re.findall(r'<div class="art" id="a-', shell))
    print(f"入门页完成：6 篇 AC30 主线 + {old_count} 篇归档 = {total} 篇 → {PAGE}")


if __name__ == "__main__":
    main()
