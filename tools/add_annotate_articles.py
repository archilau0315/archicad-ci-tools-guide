# -*- coding: utf-8 -*-
"""
给 Annotate 分册补 3 篇基于 AC30 ProKit 官方帮助补写的文章。

背景：站上原有 4 篇来自旧版 Cadimage 文档，只覆盖大小写与字体，
缺少画笔/填充/线型替换，也没有 AC30 合并后的 Replace 总入口。

幂等：已存在 a-prokit-* 块则跳过插入，只校正计数。
"""
import io
import os
import re

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(HERE, "site")

HELP = "https://help.graphisoft.com/AC/30/INT/Topics/960_Prokit/ProKit_Core/Annotate/"

ARTICLES = [
    {
        "id": "a-prokit-annotate-replace",
        "no": "05",
        "zh": "ProKit Annotate 的 Replace：一个对话框管五类替换",
        "en": "The Replace Dialog: One Place for All Five Replacement Types",
        "src": HELP + "annotation_replacement.html",
        "zh_body": """
<p>从 Archicad 30 起，ProKit 把 Annotate 的替换动作收进了一个对话框。以前要分三次做的事——改大小写、换字体、换填充画笔线型——现在在同一张表里勾选。这是本分册前四篇（旧版 Cadimage 界面）之后变化最大的一处。</p>
<p>打开方式：菜单 <em>ProKit &gt; Annotate &gt; Replace</em>。<strong>AC28 及更早版本没有这个合并对话框</strong>，菜单在 <em>CI Tools &gt; Annotate</em> 下的 <em>Convert Case…</em> 和 <em>Replace Attributes…</em> 两个分项里，操作逻辑一致但入口是分开的。</p>
<p><img src="img/prokit-AnnotateReplacement.png" alt="Annotation Replacement 主对话框，分属性替换、文本替换、作用范围三段" loading="lazy"></p>
<p>对话框分三段，从上到下依次是"改什么属性"、"改什么文本"、"作用到哪"。</p>
<h4>属性替换：三个勾，加一个容易漏的库部件开关</h4>
<ul>
<li><em>Replace Fills</em> / <em>Replace Pens</em> / <em>Replace Lines</em>：分别对应填充、画笔、线型。每个右侧都有 <em>Edit Rules…</em>，点进去定义具体换什么（见下一篇）。</li>
<li><em>Include Library Part Attributes</em>：勾上才会连图库部件内部引用的属性一起换。</li>
</ul>
<p>最后这一条最容易漏。不勾的话，墙、板、线这些元素自己的填充画笔换了，但门窗、家具、符号那些图库对象里用的填充和画笔还是老样子，图面看着就花。国内项目接手境外模板时，这条基本都要勾。</p>
<h4>文本替换：字体、大小写、以及"改到哪一层文字"</h4>
<ul>
<li><em>Replace fonts</em>：套用字体替换规则，右侧 <em>Edit Rules…</em> 进入字体管理器。</li>
<li><em>Change case to</em>：下拉选一个统一的大小写标准，全项目套用。</li>
<li><em>With exceptions</em>：保留单位缩写、专有名词的原样，右侧同样可以编辑例外清单。</li>
</ul>
<p>下面三个开关决定"文字改到多深"，这是新旧文档里都没讲清的地方：</p>
<ul>
<li><em>Include custom Property text</em>：连自定义属性的文本值一起改。</li>
<li><em>Include placed library part text</em>：连已放置图库部件的字符串参数一起改。</li>
<li><em>Only text displayed by library part</em>：只处理 2D 里真正显示出来的那些字。勾上它更安全——对象内部为其他用途藏着的字符串不会被误改。</li>
</ul>
<p>官方另有一条提醒：字体替换对某些图库部件可能无效，取决于这些部件的参数是怎么定义的。遇到个别对象字没变，先怀疑这一点，不是工具没跑。</p>
<h4>作用范围：先想清楚再点 Replace</h4>
<ul>
<li><em>Apply replacement to</em>：可选当前视图（<em>Current Drawing</em>，例如正在看的平面图、当前楼层），或扩到全项目。</li>
<li>三个附加勾选：<em>Include hidden items</em>（隐藏图层上的、被隐藏的）、<em>Include locked items</em>（显式锁定的）、<em>Include items on locked layers</em>（锁定图层上的全部元素）。</li>
</ul>
<p><img src="img/prokit-ApplyReplacement.png" alt="Apply replacement to 范围选项" loading="lazy"></p>
<h4>执行与复用</h4>
<p>点 <em>Replace</em> 才开始跑；<strong>只执行勾了的那几类，没勾的原样不动</strong>。所以完全可以只勾 <em>Replace Pens</em> 单独做一件事。跑错了直接 Undo，整批是一次可回退的动作。</p>
<p>左下角两个图标用于导入和导出<strong>整套</strong>替换规则，文件扩展名 <em>.conversion</em>。一个项目调好的规则可以存下来，下个项目直接套，不用重新配。</p>
<p>一句话记住这个分工：<strong>规则在管理器里定义，Replace 对话框只决定用哪些规则、作用到哪</strong>。</p>
""",
        "en_body": """
<p>Archicad 30 consolidates all Annotate replacements into a single dialog: <em>ProKit &gt; Annotate &gt; Replace</em>. In AC28 and earlier the same operations live under separate <em>CI Tools &gt; Annotate</em> menu items.</p>
<p>The dialog has three sections. <strong>Attribute replacement</strong> offers checkboxes for Fills, Pens and Lines, each with its own <em>Edit Rules…</em> manager; <em>Include Library Part Attributes</em> extends replacement to attributes used inside library parts — easy to overlook, and usually required when adopting a foreign template.</p>
<p><strong>Text replacement</strong> handles fonts, a uniform case standard, and case exceptions, plus three depth options: custom Property text, placed library part strings, and <em>Only text displayed by library part</em>, the safest choice for object parameters.</p>
<p><strong>Apply replacement to</strong> sets the scope (current drawing or whole project) and whether hidden, locked items and locked layers are included. Only ticked types run; the whole operation can be undone. The icons at the bottom left import and export the complete rule set as a <em>.conversion</em> file.</p>
""",
    },
    {
        "id": "a-prokit-attr-mgr",
        "no": "06",
        "zh": "替换画笔、填充与线型（Attribute Replacement Manager）",
        "en": "Replacing Pens, Fills and Line Types",
        "src": HELP + "AnnotateReplaceAttributes.html",
        "zh_body": """
<p>上一篇的 Replace 对话框只负责"用哪些规则"，真正定义规则的是这张表。站上原有机篇文章只讲了文字和字体，画笔、填充、线型这三类一直没有对应内容，这一篇补上。</p>
<p>两种方式打开：</p>
<ul>
<li>菜单 <em>ProKit &gt; Annotate &gt; Manage Attribute Replacements</em></li>
<li>或在 Replace 对话框里点 <em>Attribute replacement</em> 右侧的 <em>Edit Rules…</em></li>
</ul>
<p><img src="img/prokit-ProKitReplacementMgr.png" alt="Attribute Replacement Manager：顶部三个类型图标，Original / Replacement 两列规则表" loading="lazy"></p>
<h4>三种类型，三套互不干扰的规则</h4>
<p>顶部三个图标切换画笔、填充、线型。切到哪个，看到的就是那个类型自己的规则清单——换画笔不会碰填充的规则。</p>
<h4>规则就是一对一</h4>
<p>每一行是一条映射：<em>Original</em> 列选"要找的属性"，<em>Replacement</em> 列选"换成什么"。例如把 Pen 75 换成 Pen 20。行首带色块或图案预览，改完一眼能看出前后差别。</p>
<p>不想动的行，让 <em>Original</em> 和 <em>Replacement</em> 保持一致即可，等于这条规则空转。<strong>别删</strong>——删了容易被后面的兜底规则接管。</p>
<p><img src="img/prokit-ProKitPenReplace.png" alt="画笔替换：左侧原画笔色块，右侧替换后色块" loading="lazy"></p>
<h4>建规则的两种方式</h4>
<ul>
<li>底部 <em>+</em>：手工加一条空规则。</li>
<li><em>Create from…</em>：从项目里<strong>已经在用</strong>的属性自动生成整张清单。这个更实用，下一篇单独讲。</li>
</ul>
<h4>兜底规则：一把梭，慎用</h4>
<p>底部 <em>If no rules apply, replace with</em> —— 勾上并选一个属性，所有<strong>没有</strong>被上面清单覆盖的同类属性，全部换成它。</p>
<p>这功能很猛，也容易翻车：本来特意留着做强调的几个颜色，会被一起吃掉。只在明确要"全部归一"的时候勾。做正常替换时，这个框应该保持不勾。</p>
<p><img src="img/prokit-ProKitAttribReplacement.png" alt="属性替换区域与库部件开关" loading="lazy"></p>
<h4>导入导出：三个扩展名</h4>
<ul>
<li><em>.convertpen</em> 画笔转换文件</li>
<li><em>.convertfill</em> 填充转换文件</li>
<li><em>.convertline</em> 线型转换文件</li>
</ul>
<p>也可以从 Replace 对话框把全部规则一起存成一个 <em>.conversion</em>。<strong>导入是追加，不覆盖</strong>现有清单，重复导入会出现重复行，用之前先看一眼。</p>
<h4>国内项目里最实用的三个场景</h4>
<ol>
<li><strong>接境外模板</strong>：澳洲、欧洲模板动辄三四十套填充，压成国标常用的那几套，一次性把图面拉回国内出图习惯。</li>
<li><strong>出图归一</strong>：方案阶段用彩色画笔区分层次，出施工图要转灰阶。一条规则批量换，比逐个视图改画笔集快得多，也不会漏视图。</li>
<li><strong>清理线型</strong>：外来图纸常带几十种自定义线型，只留实线、虚线、点划线三种，图纸立刻干净。</li>
</ol>
<p>最后一条要记牢：<strong>定义规则不会改任何东西</strong>。规则存在项目里，必须回到 Replace 对话框点 <em>Replace</em> 才执行。</p>
""",
        "en_body": """
<p>Rules themselves are defined here, not in the Replace dialog. Open it via <em>ProKit &gt; Annotate &gt; Manage Attribute Replacements</em>, or from <em>Edit Rules…</em> next to Attribute replacement.</p>
<p>Three icons at the top switch between pens, fills and line types; each type keeps its own independent rule list. Every rule is a one-to-one pair: pick the attribute to find in <em>Original</em> and the replacement in <em>Replacement</em> — for example Pen 75 to Pen 20. Rows you do not want to change should keep both sides identical rather than being deleted.</p>
<p>Add rules with <em>+</em>, or use <em>Create from…</em> to build the list from attributes already used in the project. The optional <em>If no rules apply, replace with</em> catch-all replaces every uncovered attribute of that type with a single choice — powerful, but it will swallow colours you meant to keep.</p>
<p>Rule sets export and import as <em>.convertpen</em>, <em>.convertfill</em> and <em>.convertline</em>, or all together as a <em>.conversion</em> file. Imported rules are appended, never overwritten. Defining rules changes nothing on its own — you must still click Replace.</p>
""",
    },
    {
        "id": "a-prokit-create-from",
        "no": "07",
        "zh": "Create from：从项目现有属性自动生成替换清单",
        "en": "Create from: Building the Rule List from Attributes in Use",
        "src": HELP + "AnnotateReplaceAttributes.html",
        "zh_body": """
<p>这是 Annotate 里最省时间、也最少被提到的一个功能。</p>
<h4>先看问题</h4>
<p>接手一个别人的项目：画笔两百多个、填充六七十套，其中一大半你根本不知道用在哪、还有没有在用。手工抄清单不现实；让工具把属性表全列出来，又是一堆没人用的空画笔，照样没法下手。</p>
<p><em>Create from…</em> 解决的就是这个：<strong>只列真正在用的那些</strong>。</p>
<h4>操作顺序</h4>
<ol>
<li>打开 Attribute Replacement Manager，先切到要处理的类型——比如画笔。</li>
<li>点底部 <em>Create from…</em> 下拉，选范围：当前视图（<em>Current Drawing</em>，正在看的那张图、那一层），或扩到全项目。</li>
<li>工具把该范围内元素实际用到的属性全部列成规则行：<em>Original</em> 自动填好，<em>Replacement</em> 默认与之一致，也就是<strong>先全部保持原样</strong>。</li>
<li>你只改要动的那几行。</li>
<li>点 <em>OK</em> 回到 Replace 对话框，确认勾上了对应类型，再点 <em>Replace</em>。</li>
</ol>
<p><img src="img/prokit-ProKitCreateFromAttribs.png" alt="Create from 下拉：选择从哪个范围收集项目已在用的属性" loading="lazy"></p>
<h4>为什么这个顺序是对的</h4>
<ul>
<li>清单里只有真正在用的属性，没有噪音，几十行就能看完。</li>
<li>默认"原样保留"，你是<strong>先看清楚再动手</strong>，比一上来就开兜底规则安全得多。</li>
<li>和兜底规则配合最顺：常用的几十个一一指定，剩下零散没管的用 <em>If no rules apply</em> 收口。</li>
</ul>
<h4>跑完怎么验收</h4>
<ul>
<li>跑错了直接 Undo，一次 Replace 是一个可回退动作，不用逐条改回来。</li>
<li>看结果：切到平面图比线宽和颜色；或者建一个按属性统计的明细表核对，具体做法在 Quantities 那一册里。</li>
<li>如果发现某些对象没变，先查 Replace 对话框里 <em>Include Library Part Attributes</em> 有没有勾。</li>
</ul>
<p>注意：<em>Create from</em> 只负责生成规则清单，<strong>不会执行替换</strong>。它和 Replace 是两步，别指望点完就生效。</p>
""",
        "en_body": """
<p><em>Create from…</em> builds the rule list from attributes actually used in the project, instead of the full attribute table with all its unused entries.</p>
<p>Choose the attribute type with the icon tabs, then pick a range from the <em>Create from…</em> dropdown — the current drawing or the whole project. Every attribute in use is listed with <em>Original</em> filled in and <em>Replacement</em> matching it, meaning nothing changes yet. Edit only the rows you want, click OK, then run <em>Replace</em> from the Annotation Replacement dialog.</p>
<p>This sequence is safer than starting with a catch-all rule, and pairs well with one: specify the common attributes individually and let <em>If no rules apply</em> handle the rest. A whole Replace can be undone in one step. <em>Create from</em> only generates the list — it never performs a replacement.</p>
""",
    },
]


def block(a):
    return (
        f'<div class="art" id="{a["id"]}">\n'
        f'  <div class="art-h"><span class="no">{a["no"]}</span>\n'
        f'    <h3 class="zh-only block">{a["zh"]}</h3>\n'
        f'    <h3 class="en-only block">{a["en"]}</h3>\n'
        f'  </div>\n'
        f'  <div class="art-src"><a href="{a["src"]}" target="_blank" rel="noopener">'
        f'基于 Graphisoft 官方帮助（AC30）补写 ↗</a></div>\n'
        f'  <div class="zh-only">{a["zh_body"].strip()}</div>\n'
        f'  <div class="en-only">{a["en_body"].strip()}</div>\n'
        f'</div>\n'
    )


def toc_item(a):
    return (
        f'<li><a href="annotate.html#{a["id"]}"><span class="tg">{a["no"]}</span>'
        f'<span class="zh-only">{a["zh"]}</span><span class="en-only">{a["en"]}</span></a></li>'
    )


def add_articles():
    p = os.path.join(SITE, "annotate.html")
    h = io.open(p, encoding="utf-8").read()
    if 'id="a-prokit-annotate-replace"' in h:
        print("  文章块已存在，跳过插入")
    else:
        payload = "\n".join(block(a) for a in ARTICLES)
        h = h.replace("</article>", payload + "</article>", 1)
        io.open(p, "w", encoding="utf-8").write(h)
        print(f"  已插入 {len(ARTICLES)} 篇")

    # hero 计数：4 篇 / 0.8 万字 / 23 张图 -> 7 / 1.1 / 29
    h = io.open(p, encoding="utf-8").read()
    h = re.sub(r'(<span><b>)4(</b> <span class="zh-only">篇教程)', r"\g<1>7\g<2>", h, count=1)
    h = re.sub(r'(<span><b>)0\.8(</b> <span class="zh-only">万字)', r"\g<1>1.1\g<2>", h, count=1)
    h = re.sub(r'(<span><b>)23(</b> <span class="zh-only">张图)', r"\g<1>29\g<2>", h, count=1)
    io.open(p, "w", encoding="utf-8").write(h)
    print("  hero 计数已校正")


def sync_index_and_all():
    for name in ("index.html", "all.html"):
        p = os.path.join(SITE, name)
        h = io.open(p, encoding="utf-8").read()
        # toc 追加
        if 'annotate.html#a-prokit-annotate-replace' not in h:
            items = "".join(toc_item(a) for a in ARTICLES)
            # 在 Annotate 分册的 toc-list 末尾追加
            m = re.search(r'(<h2>Annotate · .*?</h2>\s*<ul class="toc-list">)(.*?)(</ul>)', h, re.S)
            if m:
                h = h[: m.start(2)] + m.group(2) + items + h[m.end(2):]
                print(f"  {name}: toc 已追加")
            else:
                print(f"  {name}: 未找到 Annotate toc 块")
        io.open(p, "w", encoding="utf-8").write(h)


def fix_counts():
    # 篇数 357 -> 360；图数 1208 -> 1214
    repl = {
        "16 个工具、357 篇文档、1208 张界面截图": "16 个工具、360 篇文档、1214 张界面截图",
        "357 篇官方文档、1208 张": "357 篇官方文档 + 3 篇 AC30 补写、1214 张",
        "357 articles and 1208": "357 official articles plus 3 written for AC30, 1214",
        "— 357 articles, 120": "— 357 official articles plus 3 for AC30, 120",
        "共 357 篇，点标题直达分册的具体文章。": "共 360 篇，点标题直达分册的具体文章。",
        "共 357 篇官方教程，按工具分册列出。": "共 360 篇教程（357 篇官方原文 + 3 篇 AC30 补写），按工具分册列出。",
        "All 357 official articles, listed by tool.": "All 360 articles (357 official plus 3 written for AC30), listed by tool.",
    }
    for name in ("index.html", "all.html"):
        p = os.path.join(SITE, name)
        h = io.open(p, encoding="utf-8").read()
        for a, b in repl.items():
            h = h.replace(a, b)
        h = h.replace("<span><b>357</b> <span class=\"zh-only\">篇教程",
                      "<span><b>360</b> <span class=\"zh-only\">篇教程")
        io.open(p, "w", encoding="utf-8").write(h)

    # index 卡片：4 篇 · 23 图 -> 7 篇 · 29 图
    p = os.path.join(SITE, "index.html")
    h = io.open(p, encoding="utf-8").read()
    h = h.replace('<div class="n"><span class="zh-only">4 篇 · 23 图</span>'
                  '<span class="en-only">4 articles · 23 images</span></div>',
                  '<div class="n"><span class="zh-only">7 篇 · 29 图</span>'
                  '<span class="en-only">7 articles · 29 images</span></div>')
    io.open(p, "w", encoding="utf-8").write(h)
    print("  统计数字已更新")


if __name__ == "__main__":
    add_articles()
    sync_index_and_all()
    fix_counts()
    print("完成")
