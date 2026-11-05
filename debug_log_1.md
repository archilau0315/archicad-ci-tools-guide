# 变更日志

## 2026-11-05 09:41 — 新建：CI Tools 完全指南

| 项 | 内容 |
|---|---|
| 位置 | `resources/AC_Tutorial/ci_tools/` |
| 变更简述 | 新建 CI Tools 完整操作手册与速查卡，含 24 张官方界面截图，网页完全自包含 |
| 来源 | Graphisoft 官方 MyCi 知识库（2026-10 更新）+ 官方教程截图 |

### 目录结构

```
ci_tools/
├── readme.md                    项目说明
├── debug_log_1.md               本文件
├── docs/
│   ├── CI_Tools_用户手册_图文版.html   24 章节 + 24 截图（自包含）
│   ├── CI_Tools_速查卡_网页版.html     一页纸速查（自包含）
│   ├── CI_Tools_用户手册.md            纯文字版
│   ├── CI_Tools_速查卡.md              纯文字版
│   └── manual_master.md               网页版主稿
├── assets/img/                  24 张官方截图 + 图床映射表
└── tools/
    ├── beautify.py              美化管线
    └── localize_images.py       图片本地化
```

### 内容要点

- 16 个工具逐个拆解，每章标明菜单路径
- Annotate 对话框按官方截图逐项核对（Case / Scope / Ignore / Notify 四栏）
- 版本指引覆盖 Archicad 24 ~ 30，含 CI Tools → ProKit 更名对照
- 速查卡按学习优先级排序，非字母序
- 附录含 libpack 加载顺序、安装与补装步骤

### 技术决策

**图片全部本地化**：原网页引用资料库图床外链，搬到这个目录后会成为外部依赖。已用 `tools/localize_images.py` 下载 24 张转相对路径，HTML 完全自包含，可离线打开、随目录迁移。

**字体加本地回退**：标题层 `Noto Serif SC` → `Source Han Serif SC` → `Songti SC` → `SimSun`，等宽字体加 `Microsoft YaHei`。CDN 不可达时排版不塌。

**内容去本机化**：手册原本含作者单机核查结论（AC28 装齐 / AC29 缺 5 个 / AC30 未装），已全部改写为面向全团队的「先自查」指引，路径统一用 `Archicad XX` 占位并补 macOS 路径。

### 验证

| 项目 | 结果 |
|---|---|
| 图片本地化 | 手册 26 处引用、速查卡 2 处引用，全部本地，远程引用 0 |
| 文件完整性 | 相对路径指向的图片文件缺失 0 个 |
| 页面质检 | 两页均 `MINDX_PAGE_QUALITY_OK` |
| 章节结构 | 手册 24 章节、速查卡 6 章节，目录锚点全部命中 |

### 后续

- 资料库云端版本：https://workbuddy.link/p/5fCzXnHhFkUQ2Cb0QS5FyA
- 官网如需挂载，可将 `docs/` 下两个 HTML 部署到静态资源路径

---

## 2026-11-05 10:20 — 升级：全量官方教程站，部署上线

| 项 | 内容 |
|---|---|
| 位置 | `resources/AC_Tutorial/ci_tools/site/` → 线上 `/resources/AC_Tutorial/ci_tools/site/` |
| 变更简述 | 从 16 工具要点版升级为官方教程全量站：357 篇文档、1193 张截图、42.3 万字 |
| 备注 | 已部署至公网（无需登录），并挂到 resources 首页卡片 |

### 内容规模

| 分册 | 篇数 | 分册 | 篇数 | 分册 | 篇数 |
|---|---:|---|---:|---|---:|
| Quantities | 100 | Structural | 16 | Electrical | 9 |
| Cabinets | 49 | Sites | 15 | Transformer | 5 |
| Doors+Windows | 48 | Stairs | 13 | Detail Elements | 5 |
| Coverings | 36 | Electrical | 9 | Fitout | 5 |
| MetaData | 27 | Annotate | 4 | Time Tracker | 1 |
| Keynotes | 24 | | | | |

合计 **357 篇 / 1193 张图 / 42.3 万字**。

### 站点结构（18 个页面）

```
index.html   总览：三步启动 + 16 工具卡片 + 全量目录
guide.html   中文主线速查（我编写的 16 工具操作要点）
all.html     全量文章索引（357 篇，按工具分组）
{16 个工具}.html  工具分册，官方原文 + 全部截图
img/         1193 张本地截图
```

### 技术要点

**数据采集**：MyCi 知识库 Zendesk API（`/api/v2/help_center/en-us/articles/{id}.json` + `/categories/{cid}/articles.json`）批量抓取，正文清洗为 Markdown。

**图片本地化**：1193 张下载压缩（宽 1200px / JPEG q74），全部转相对路径，**零外链依赖**，站点可独立运行。

**失效图处理**：33 张官方源站已 404（多为 blog.cadimageworld.com 老博客关站），页面输出占位说明而非破图。

**图片即链接**：官方正文有 15 处 `<a><img></a>` 形式（图片本身是链接），清洗阶段用 `%%IMGLINK<图片url>|<外链>%%` 占位，生成器渲染为「本地图 + 外链跳转」。

**链接修复**：清洗脚本原用贪婪正则导致 42 处坏链接，改为非贪婪 + 文字为空时用域名兜底。

### 部署

服务器：阿里云 `47.93.210.248`（`47.93.210.248` 在 known_hosts 中，SSH 密钥 `~/.ssh/id_ed25519`）
Web 根：`/www/wwwroot/kbitai.com.cn/`

```bash
tar czf - -C resources AC_Tutorial/ci_tools/site | \
  ssh -i ~/.ssh/id_ed25519 root@47.93.210.248 \
  "cd /www/wwwroot/kbitai.com.cn/resources && tar xzf - && chown -R www:www AC_Tutorial"
```

**认证**：AUtrain 有专门 nginx 认证配置（`extension/www.kbitai.com.cn/autrain.conf`），resources 其他目录默认公开 —— 本教程按堂主要求**完全公开**。

### 验证

| 项目 | 结果 |
|---|---|
| 线上页面 | index / guide / all / 各分册 全部 HTTP 200 |
| 图片 | 抽查 3 张全部 200，尺寸正常 |
| 首页卡片 | resources 首页已插入，含封面图 |
| 远程图片引用 | 0（全部本地化） |
| 页面裸链接 | 0 |
| 浏览器实测 | Chrome 1440×900 线上首页渲染正常 |

### 遗留

- 33 张图官方源站已失效，已用占位说明替代
- 英文原文 357 篇保持原文收录（未逐篇精译），中文主线已覆盖 16 个工具的核心操作

---

## 2026-11-05 10:30 — 修订：主站资源下拉 + 封面优化

| 项 | 内容 |
|---|---|
| 模块 | `index.html`（主站导航）、`resources/AC_Tutorial/ci_tools/cover.jpg` |
| 变更简述 | 主站右上角「资源」改为下拉菜单（5 项）；CI Tools 封面重做为正方形适配卡片裁切 |
| 备注 | 已部署上线并浏览器实测通过 |

### 主站资源下拉

复用既有 `.nav-dropdown` 机制（与「AI工具」下拉同款），新增 `#resDropdown`：

```html
<li class="nav-dropdown" id="resDropdown">
    <a href="./resources/index.html" class="nav-cta resource-cta nav-dropdown-toggle"
       data-i18n="nav-other" onclick="toggleResDropdown(event)">资源</a>
    <ul class="nav-dropdown-menu"> ... 5 项 ... </ul>
</li>
```

菜单项：全部资源 / Archicad CI Tools 完全指南 / 澳洲设计实务资料包 / Vibe Coding 学员实践手册 / 用魔法创建魔法

**配套改动**：
- `toggleResDropdown(e)` —— 移动端（≤768px）点击切换 `.open`，PC 端 CSS `:hover` 展开
- 点击外部自动关闭（复用 AI 下拉的 document 监听，追加 `resDropdown` 判断）
- i18n 中英词典各补 5 个 key（`nav-res-all` / `nav-res-citools` / `nav-res-autrain` / `nav-res-vibe` / `nav-res-magic`）
- 定位修正：`#resDropdown > .nav-dropdown-toggle` 抬 `z-index:103`，避免菜单遮挡触发按钮

### 封面优化

**问题**：`.article-thumb` 是 150×150 正方形 + `object-fit:cover`，原 1200×900 横版封面被裁掉两侧，标题全部丢失。

**解决**：改为 1000×1000 正方形，重新布局：

```
┌─────────────────────┐
│  CI Tools 菜单截图    │  ← 上部 43%，品牌色横线分隔
├─────────────────────┤
│      CI Tools        │  ← 112px 特大字
│      完全指南        │  ← 蓝色
│  16 个效率插件 · …    │  ← 灰色小字
│  357 篇文档 · 1193 图 │  ← 蓝色粗体
└─────────────────────┘
```

截图裁剪自 `site/img/206662343_0.jpg`（CI Tools 完整菜单树），取原图上 74% 保留菜单主体。

实测 150×150 缩略图下「CI Tools 完全指南」清晰可辨。

---

## 2026-11-05 11:40 — 升级：全站中英双语，一键切换

| 项 | 内容 |
|---|---|
| 模块 | `docs/full/build_site.py`、`docs/full/zh_translations.json`、站点全部 18 个页面 |
| 变更简述 | 357 篇官方教程全部译为中文，全站支持中文/EN 一键切换，默认中文 |
| 备注 | 已部署上线并浏览器实测通过 |

### 翻译规模

| 项 | 数值 |
|---|---|
| 翻译篇数 | **357 / 357**（全部） |
| 英文原文 | 422,951 字符 |
| 中文译文 | 约 186,000 字符（压缩率约 44%，符合中英密度差） |
| 图片占位符校验 | 逐篇数量与顺序比对，**不匹配 0** |

**双语呈现方式**（按堂主要求「主线中文 + 原文可对照」）：
- 中文模式：显示完整中文译文
- 每篇文章下方有 **「英文原文对照 / Official English Original」** 折叠区，展开即见官方原文原图
- 英文模式：界面、导航、标题、正文全部切英文

### 切换机制

- 右上角固定 **中文 / EN** 切换按钮
- 默认中文；选择记忆在 `localStorage`（键 `citools-lang`）
- 支持 URL 参数 `?lang=en` / `?lang=zh`，可直接分享特定语言版本
- CSS 用 `html[data-lang]` 属性驱动 `.zh-only` / `.en-only` 两套内容

### 双语覆盖范围

- 侧栏导航（16 工具名 + 分组标题 + 品牌区）
- 页面标题、面包屑、Hero 区、统计数字
- 文章标题与正文（357 篇）
- 首页工具卡片描述、全量目录条目名
- 三步启动说明、页脚

### 修复的三个技术问题

1. **CSS 缺右花括号** —— 批量正则修复时误伤 `html[data-lang="en"] .nav-h.en-only{display:block`，导致后续所有规则被吞，双语切换完全失效（浏览器显示 `zh=block en=block`）。加了 CSS 括号平衡校验定位。
2. **f-string 嵌套字典字面量** —— `{_ZH.get(x["id"], {}).get(...)}` 在 f-string 中 `{}` 需转义为 `{{}}`，且右括号易错。改用辅助函数 `zh_title_of(aid, fallback)` 规避。
3. **display 优先级** —— `.zh-only.block { display:block }` 特异性高于 `html[data-lang="en"] .zh-only { display:none }`。改用 `html:not([data-lang="en"])` 双向规则 + `!important` 兜底。

### 验证

| 项目 | 结果 |
|---|---|
| 翻译完整度 | 357 / 357，缺失 0 |
| 图片占位符 | 不匹配 0 |
| CSS 括号平衡 | 通过（18 页全部） |
| 双语块统计 | zh-only 2738｜en-only 2693｜原文对照 465 |
| 浏览器实测 | 中文模式 `zh=block en=none`；英文模式 `zh=none en=block` |
| 线上验证 | 线上 `?lang=en` 切换正常，页面 200 |

### 新增文件

- `docs/full/zh_translations.json` —— 357 篇中文译文（主数据）
- `docs/full/zh_batch1~6.json` —— 各批次原始产出（可追溯）

---

## 2026-11-05 11:55 — 修订：补齐「来源与说明」页，修复 404

| 项 | 内容 |
|---|---|
| 模块 | `docs/full/build_site.py`、`docs/full/zh_translations.json`、站点 19 个页面 |
| 变更简述 | 新增 `about.html`（来源与说明），修复侧栏入口 404；补译 4 篇遗漏 |
| 备注 | 已部署上线，线上爬取 19 页零断链 |

### 问题

侧栏「来源与说明」入口指向 `about.html`，但**生成器从未产出这个页面** —— 18 个页面都引用了它，全部 404。

### 新增页面

`build_about()` 生成 `about.html`，含五块内容（中英双语）：

| 章节 | 内容 |
|---|---|
| 内容来源 | 官方文档出处、截图数量、译文完整度、整理时间 |
| 翻译处理原则 | 菜单路径保留英文、技术标识符保留英文、原文可对照、统一术语 |
| 已知局限 | 33 张失效截图、Electrical 无国标库、Sites/Bracing 区域限制、AC30 改名 ProKit |
| 免责声明 | 版权归 Central Innovation / Graphisoft，译文非官方 |
| 官方入口 | MyCi 知识库、ProKit 下载、官方论坛 |

### 补译的 4 篇

| 文章 | 原问题 | 处理 |
|---|---|---|
| 8.2 Not | 标题为纯英文 | 改为「8.2 Not（取反运算符）」 |
| Watch: Update overview for AC23 | 正文空（纯视频） | 加提示行 |
| (AC22) Watch: How to create a Cabinet | 正文空 | 加提示行 |
| Watch: Overview webinar recording (27 mins) | 正文空 | 加提示行 |

### 核查方法（修正了误判）

初次用「中文字符占比 < 50%」筛查，得出「66 篇未翻译」—— **误判**。原因是这些文章含大量 Vimeo iframe 编码、英文属性名清单、计算表达式，技术标识符本就应保留英文。

改用精确判定：剥除 iframe 块、占位符、标签、URL 后，检查标题与正文是否含中文 → 实际只有 4 篇存在问题。

### 验证

| 项目 | 结果 |
|---|---|
| 站内链接 | 19 个目标，404 归零 |
| 线上爬取 | 从首页 BFS 遍历，19 页全部 200，**断链 0** |
| 图片引用 | 1175 处，缺失 0 |
| CSS 括号平衡 | 19 页全部通过 |
| about.html 双语 | zh 块 52 / en 块 52 |
| 浏览器实测 | 中文模式表格清晰；英文模式零残留中文 |

---

## 2026-11-05 12:15 — 修订：主站导航下拉统一，AI 工具指向最新区块

| 项 | 内容 |
|---|---|
| 模块 | 主站 `index.html`（导航栏 + Hero 区） |
| 变更简述 | 「资源」下拉与「AI工具」样式完全统一；Hero 区 AI工具 按钮改指向首页最新 AI 区块 |
| 备注 | 已部署上线并浏览器实测通过 |

### 排查过程

初次反馈是「资源键没有箭头」，但实测 `getComputedStyle` 显示两个按钮的 `::after` 都是 `▾` —— 箭头其实早已存在（上一次改动就加了）。真正的问题是**另两处**：

1. Hero 区「AI工具」按钮 `href="./aitools/"` 指向 9 月的旧汇总页。该页只有两张卡片（首席图像架构师、筑元智览），缺 ArchiLinkAI，且无下拉菜单。
2. 导航栏 AI 下拉第一项写死绝对域名 `https://www.kbitai.com.cn/architect/`，本地预览会跳外站。

### 改动

| 位置 | 原内容 | 改为 |
|---|---|---|
| Hero AI 工具 | `./aitools/`（旧汇总页） | `#ai`（首页 AI 工具区，展示最新三个工具） |
| 导航 AI 下拉 1 | `https://www.kbitai.com.cn/architect/` | `./aitools/architect/`（相对路径） |
| 导航 AI 下拉 2 | `https://www.kbitai.com.cn/aitools/archiken/` | `./aitools/archiken/` |
| AI 区块「立即体验」 | `https://www.kbitai.com.cn/aitools/archiken/` | `./aitools/archiken/` |
| 资源下拉 CSS | 独立定位 hack（`top:+12px` + `z-index:103`） | 移除，与 AI 下拉共用同一套机制 |
| 触发按钮层级 | 只给资源加 | 通用化 `.nav-dropdown > .nav-dropdown-toggle` |
| JS | `toggleAiDropdown` / `toggleResDropdown` 两份重复实现 | 合并为 `toggleNavDropdown(e, id)` + 通用关闭逻辑 |

### 验证

| 项目 | 结果 |
|---|---|
| 箭头渲染 | AIarrow=`▾`｜RESarrow=`▾`，实测一致 |
| 悬停展开 | AI 下拉 `op=1 vis=visible`；资源下拉截图确认 |
| 按钮遮挡 | 两个按钮均完整可见，未被菜单盖住 |
| 移动端点击展开 | 700px 视口：`open=true disp=block` |
| 点击外部关闭 | `ai=false ; res=false` |
| Hero AI 工具跳转 | scrollY=3485，AI 区块进入视口，显示三个最新工具 |
| 线上一致性 | 本地与线上同为 80039 字节 |

---

## 2026-11-05 12:27 — 修订：资源页 CI Tools 卡片补齐英文词条

| 项 | 内容 |
|---|---|
| 模块 | `resources/index.html`（I18N 词典） |
| 变更简述 | CI Tools 卡片的 5 个 `data-i18n` 键在中英词典里全缺失，补齐后英文模式可正常切换 |
| 备注 | 已部署上线，线上浏览器实测通过 |

### 问题

卡片 HTML 里写了 `data-i18n="article-citools-tag/title/desc/date/read"`，但 **I18N 词典里这 5 个键一个都没有**。

`setLang()` 的实现是 `if (I18N[lang][key]) { el.innerHTML = ... }` —— 键不存在时静默跳过，所以：

- 中文模式：HTML 里的中文原文直接显示（看起来正常）
- 英文模式：找不到英文词条，卡片保持中文不切换

这就是「CI Tools 指南标题栏没英文」的原因，而其他两张卡片（用魔法创建魔法、Vibe Coding）词条齐全，所以只有这一张有问题。

### 新增词条

| 键 | 中文 | 英文 |
|---|---|---|
| `article-citools-tag` | 插件手册 | Plugin Manual |
| `article-citools-title` | Archicad CI Tools 完全指南 | Archicad CI Tools Complete Handbook |
| `article-citools-desc` | 16 个效率插件的官方教程全量中文版… | The complete bilingual edition of the official Archicad CI Tools documentation… |
| `article-citools-date` | 2026 | 2026 |
| `article-citools-read` | 阅读更多 → | Read More → |

### 验证

新增了词条完整性自检 —— 提取 HTML 中全部 `data-i18n` 键，与 zh / en 两段词典逐一对账：

| 项目 | 结果 |
|---|---|
| HTML 使用的键 | 32 |
| zh 词典覆盖 | 32 / 32，缺 0 |
| en 词典覆盖 | 32 / 32，缺 0 |
| 英文模式实测 | 标题 `Archicad CI Tools Complete Handbook`，描述、Read More → 均英文 |
| 中文模式实测 | 未受影响，正常显示 |
| 视觉对比 | 与下方 Vibe Coding、Magic to Magic 两张卡片样式一致 |
| 线上一致性 | 本地与线上同为 21630 字节 |

**教训**：加 `data-i18n` 属性时必须同步在两段词典里都加键，否则英文模式静默失效。这类问题不会报错，只能靠词条对账发现。

---

## 2026-11-05 12:38 — 修订：资源页补澳洲内训卡片 + AI 工具改下拉

| 项 | 内容 |
|---|---|
| 模块 | 主站 `index.html`（资源下拉）、`resources/index.html`（导航 + 卡片 + 封面） |
| 变更简述 | 修复主站下拉 AUtrain 大小写 404；资源页新增澳洲内训卡片；资源页橙色 AI 工具改为与主页一致的下拉 |
| 备注 | 已部署上线，线上浏览器实测通过 |

### 三个问题

**1. 主站资源下拉的澳洲内训是 404**

服务器上目录名是**小写 `autrain`**，而链接写的是 `./resources/AUtrain/`（大写 U）。Linux 区分大小写，直接 404。

同时确认：`autrain` 有专门的 nginx 认证配置（`extension/www.kbitai.com.cn/autrain.conf`），未登录 302 跳登录页 —— 这是预期行为。

**2. 资源页缺澳洲内训卡片**

页面只有 3 张卡片（CI Tools、Vibe Coding、用魔法创建魔法），澳洲内训只在主站右下角浮动推广位出现。

**3. 资源页橙色 AI 工具按钮是旧代码**

`resources/index.html` 的导航是独立实现的，没有下拉机制。橙色按钮写死指向 `https://www.kbitai.com.cn/architect/`（直接进首席图像架构师），而旁边普通「AI工具」项已指向 `../#ai` —— 同一页里两个 AI 工具入口指向不同地方。

### 改动

| 位置 | 原内容 | 改为 |
|---|---|---|
| 主站资源下拉 | `./resources/AUtrain/` | `./resources/autrain/` |
| 资源页导航 AI 工具 | 裸链接 → architect | 下拉菜单，3 项：首席图像架构师 / 筑审通 ArchiKen / 筑元智联 ArchiLinkAI |
| 资源页 | — | 新增「澳洲设计实务内训」卡片（置顶） |
| 资源页 | — | 新增 `autrain_cover.jpg` 封面（1000×1000 正方形，AU 徽标 + 中英双语） |
| 资源页 i18n | — | 补 10 个词条（AI 下拉 3×2 + 澳洲卡片 5×2） |

资源页新增的 CSS / JS 与主站**完全同款**（`.nav-dropdown` / `::after` 箭头 / `toggleNavDropdown` / 点击外部关闭）。

### 验证

| 项目 | 结果 |
|---|---|
| i18n 词条 | 40 / 40，zh 与 en 均无缺失 |
| 卡片数 | 4 张（澳洲内训置顶） |
| 澳洲内训封面 | HTTP 200，61038 字节 |
| AI 下拉悬停 | 正常展开，3 项清晰，橙色按钮带箭头完整可见 |
| 下拉链接可达性 | aitools/architect/ 200｜aitools/archiken/ 200｜autrain 302（登录跳转，符合预期） |
| 中文模式 | 4 张卡片正常显示 |
| 英文模式 | AU Design Practice Training / Sign in → 正常切换 |
| 线上一致性 | 主站 80039、资源页 26305 字节，与本地一致 |

---

## 2026-11-05 12:47 — 优化：资源页导航改轻量顶栏，消除主页重复

| 项 | 内容 |
|---|---|
| 模块 | `resources/index.html`（导航结构 + CSS + JS + i18n） |
| 变更简述 | 移除与主页重复的完整导航，改用 Portfolio 子页同款轻量顶栏（logo + 返回主站 + 语言切换） |
| 备注 | 已部署上线，桌面/移动/中英四态均浏览器实测通过 |

### 问题

资源页顶部导航是主页 `<nav class="nav">` 的**完整复制**（logo + 6 个文字链接 + 3 个 CTA 按钮 + AI 下拉）。

维护成本：主页改导航要同步改两处。这次就撞上了——为了给资源页加 AI 工具下拉，我不得不把整套下拉 CSS/JS 复制过去一遍；下拉项路径写错大小写（`architect/` vs `aitools/architect/`）也只能靠人工发现。

### 改造方案

参照 `Portfolio/index.html` 的做法——它没有导航栏，只有品牌区 + 语言切换。资源页改为轻量顶栏：

```
┌──────────────────────────────────────────────┐
│ [Logo] KBITAI 匡形无界      ← 返回主站  [CN|EN] │  ← fixed 顶栏
└──────────────────────────────────────────────┘
```

| 项 | 处理 |
|---|---|
| 导航栏 | 整块删除，替换为 `.topbar` |
| logo | 保留，点击返回主站 |
| 返回主站 | 新增，中英双语（返回主站 / Back to Home） |
| 语言切换 | 从页面右上角 fixed 移入顶栏右侧，避免与返回按钮重叠 |
| 旧 CSS | 删除全部 `.nav-*` 规则（约 40 行） |
| 旧 JS | 删除下拉切换 + navbar 滚动监听 |
| 无用 i18n 词条 | 删除 12 个导航相关键 |

### 顺带修的问题

**移动端封面裁切**：移动端 `.article-thumb` 是 `100% × 180px` 横幅 + `object-fit:cover`，正方形封面被裁掉上下（澳洲内训的 AU 徽标和标题都看不见）。

改为给正方形封面加 `.square` 类，用 `object-fit:contain` + 浅底完整显示，不影响其他卡片的图。

### 验证

| 项目 | 结果 |
|---|---|
| 文件体积 | 26305 → 20868 字节（减少 5.4KB 重复代码） |
| 旧导航残留 | 0 处（`nav-links` / `nav-cta` / `nav-dropdown` 全清） |
| i18n 词条 | 29 / 29，zh 与 en 均无缺失、无冗余 |
| 桌面端 | 顶栏排布正常，无重叠 |
| 移动端 390px | logo + 返回主站 + CN/EN 一行放下，无溢出 |
| 中文模式 | 返回主站 / 资源 / 四张卡片全中文 |
| 英文模式 | Back to Home / Resources / AU Design Practice Training 全英文 |
| 封面显示 | 四张卡片封面均完整（桌面 + 移动端） |
| 线上一致性 | 本地与线上同为 20868 字节 |

### 维护收益

以后主页导航怎么改，资源页都不用动 —— 资源页只有 logo 和返回主站两个入口，指向主页的固定地址。

### 关于 autrain 大小写

核查后确认**不需要改名**：本地 Windows 不区分大小写（`AUtrain` 与 `autrain` inode 相同，实为同一目录），服务器上本来就是小写 `autrain`（含 nginx 认证规则全部小写）。之前的 404 纯粹是链接手写成了大写，现已修正。

---

## 2026-11-05 12:55 — 优化：子页顶栏统一，抽出共享样式文件

| 项 | 内容 |
|---|---|
| 模块 | 新增 `public/sub-topbar.css`；`Portfolio/index.html`、`resources/index.html` |
| 变更简述 | 作品集子页接入与资源页一致的顶栏；两页共用同一份样式文件，顶栏代码从两份变一份 |
| 备注 | 已部署上线，两页线上浏览器实测通过 |

### 做法

把顶栏样式抽到 `public/sub-topbar.css`（3183 字节），两个子页各引一行 `<link>`：

```html
<link rel="stylesheet" href="../public/sub-topbar.css">
```

类名统一加 `sub-` 前缀（`.sub-topbar` / `.sub-lang-toggle` / `.sub-zh-only` / `.sub-en-only`），避免与页面自身样式冲突。

中英切换由 `html[data-lang]` 属性驱动，两页的 `setLang()` 同步设置该属性：

```js
document.documentElement.setAttribute('data-lang', lang);
```

### 作品集页的适配

| 项 | 处理 |
|---|---|
| 顶栏 | 原为页面右上角 fixed 语言切换 → 改为标准顶栏 |
| logo | 原来在页头中间（`.brand`）→ 移到顶栏左侧，页头里的重复品牌区删除 |
| 页头留白 | `padding-top` 48px → 108px，避开 fixed 顶栏 |
| 详情页 | `.detail-header` 的 sticky `top:0` → `top:62px`，避免与顶栏重叠 |
| logo 滤镜 | 补 `brightness(1.5) grayscale(0.3)`，与原品牌区一致 |

### 验证

| 项目 | 结果 |
|---|---|
| 共享 CSS | HTTP 200，3183 字节 |
| 两页引用 | Portfolio ✓ / resources ✓ |
| 顶栏视觉 | 两页完全一致（logo 位置、返回主站、CN/EN 位置与样式） |
| Portfolio 中文 | 返回主站 / 建筑设计作品集 |
| Portfolio 英文 | Back to Home / Architectural Portfolio（仅显示一个，不重叠） |
| 移动端 390px | 顶栏无溢出；Back to Home 换行但完整 |
| 资源页 | 4 张卡片、语言切换正常 |
| 线上一致性 | Portfolio 73610 / 资源页 18581 字节，与本地一致 |

### 维护收益

- 顶栏样式只有一份，改一处两页同步生效
- 以后新增子页（如新的 aitools 子页），引一行 CSS 即可获得同样的顶栏
- 子页与主页导航彻底解耦，主页改导航不影响子页

---

## 2026-11-05 13:03 — 优化：子页页脚统一，抽出共享样式文件

| 项 | 内容 |
|---|---|
| 模块 | 新增 `public/sub-footer.css`；`Portfolio/index.html`、`resources/index.html` |
| 变更简述 | 两页页脚统一为主页标准结构（标语 → 链接 → 联系方式 → 备案号 → 版权），共用同一份样式文件 |
| 备注 | 已部署上线，两页线上浏览器实测通过 |

### 改造前的差异

| 页 | 原页脚 |
|---|---|
| 主页 | 标语 + 3 链接 + 备案号 + 版权（最完整） |
| 资源页 | 标语 + 3 链接 + 备案号 + 版权（**缺联系方式**） |
| 作品集页 | 仅「联系方式」标签 + TEL/E-mail + 版权（**缺标语、链接、备案号**，且在 480px 窄容器内） |

### 统一后的结构（两页一致，与主页同款）

```
设计有形 科技无界
FINITE FORM INFINITE TECH
建筑设计作品集 · 首席图像架构师 · 服务协议
TEL：13512848962 刘珂 · E-mail：kbit_ai@126.com
津ICP备2026002055号-1 · 津公网安备12010402002460号
© 2024 天津匡形无界智能科技有限公司（KBITAI）. All rights reserved.
```

### 实现

共享文件 `public/sub-footer.css`（2392 字节），两页各引一行。类名加 `sub-` 前缀避免冲突：

```html
<link rel="stylesheet" href="../public/sub-footer.css">
```

| 位置 | 处理 |
|---|---|
| 作品集页 | 页脚从 480px 的 `.container` 内**移出**（否则宽度受限）；删除本地 `.footer` / `.contact-*` / `.copyright` CSS |
| 资源页 | 补上联系方式一行；删除本地 `.footer-*` CSS |
| 资源页链接 | `architect/` → `aitools/architect/`（与主页一致） |
| 词条 | Portfolio 补 slogan / footer-link×3；资源页补 tel / email |

**版权文案**按公司规范校正：
- 中文：© 2024 天津匡形无界智能科技有限公司（KBITAI）
- 英文：© 2024 Tianjin Kuanform Boundless Intelligent Technology Co., Ltd. (KBITAI)

### 验证

| 项目 | 结果 |
|---|---|
| 共享 CSS | HTTP 200，2392 字节 |
| 两页引用 | Portfolio ✓ / resources ✓ |
| 旧 footer 残留 | 两页均 0 处 |
| 页脚视觉 | 两页完全一致，五段内容齐全 |
| 作品集英文 | Architectural Portfolio / Chief Image Architect / Terms of Service，版权用规范英文名 |
| 页脚链接 | Portfolio 200 / aitools/architect 200 / terms.html 200 / 备案图标 200 |
| 线上一致性 | Portfolio 74416 / 资源页 17676 字节，与本地一致 |

### 踩坑记录

作品集页的滚动容器是 `.viewport`（`overflow-y:auto` + `position:fixed`），不是 window。测试时用 `window.scrollTo` 无效，需 `document.getElementById('viewport').scrollTop`，且因 `scroll-behavior:smooth` 需临时置 `auto` 才能立即生效。

---

## 2026-11-05 13:15 — 优化：主页标语居中、详情页响应式图幅、子页页脚精简

| 项 | 内容 |
|---|---|
| 模块 | 主站 `index.html`、`Portfolio/index.html`、`resources/index.html`、`public/sub-footer.css` |
| 变更简述 | 三处改动：主页标语真正居中；作品集详情页适配大屏图幅；两个子页页脚精简为联系方式+版权 |
| 备注 | 已部署上线，线上浏览器实测通过 |

### 1. 主页标语居中

**问题**：「设计有形 科技无界」视觉偏左，与下方英文不居中。

**原因**：`letter-spacing:4px` 会在末字后额外留 4px 空白，而 `.footer-slogan-cn` 是块级元素、文字默认左对齐 —— 两个 div 的盒子虽然同宽（都是 262px），但中文实际只占了左侧一段。

**解决**：
```css
.footer-slogan { text-align:center; }
.footer-slogan-cn { letter-spacing:4px; margin-right:-4px; }  /* 抵消末字后空白 */
.footer-slogan-en { letter-spacing:3px; margin-right:-3px; }
```

实测中英文中点均为 722px，偏差 0。

### 2. 作品集详情页适配台式显示器

**问题**：详情页所有内容锁在 `max-width:480px` 窄容器内，在 1440px 屏幕上只占三分之一，两侧大片留白。

**解决**：加 `@media (min-width:900px)` 断点，移动端保持原样：

| 元素 | 移动端 | 桌面端 |
|---|---|---|
| 主图 `.hero-image` | 480px | **1080px** |
| 图库 `.gallery-item` | 480px | **1080px** |
| 视频区 `.video-section` | 480px | **1080px** |
| 标题区 `.detail-title-area` | 480px | 1080px，字号 2.1rem |
| 信息卡 `.info-card` | 432px | 1016px，内边距 32/40px |

**图幅选择依据**：1080px 兼顾大屏观感与加载速度——再大则建筑实景图在 1440 屏上会出现明显拉伸感，反而失真。

实测：1440px 视口下主图与图库均 1080px；390px 视口下主图仍为 390px（未受影响）。

### 3. 子页页脚精简

**保留**：联系方式（TEL / E-mail）+ 版权声明
**移除**：标语、快捷链接、ICP 备案号

结构：
```
联系方式
TEL：13512848962 刘珂 · E-mail：kbit_ai@126.com
© 2024 天津匡形无界智能科技有限公司（KBITAI）. All rights reserved.
```

**响应式处理**：桌面端电话与邮箱同行；窄屏（≤640px）自动分行，避免折行错乱。

```css
@media (max-width:640px) {
  .sub-footer-contact .fc-item { display:block; }
  .sub-footer-contact .fc-sep { display:none; }
}
```

共享样式 `sub-footer.css` 保留 `.hidden` 类，需要恢复标语/链接/备案时去掉该类即可。

### 验证

| 项目 | 结果 |
|---|---|
| 主页标语对齐 | cnMid=722 / enMid=722，偏差 0 |
| 详情页桌面端 | 主图 1080px、图库 1080px |
| 详情页移动端 | 主图 390px，未受影响 |
| 子页页脚 | 仅联系方式 + 版权，两页一致 |
| 桌面端页脚 | TEL 与邮箱同行 |
| 移动端页脚 | 各占一行，无折行错乱 |
| i18n 词条 | Portfolio 7/7、资源页 27/27，zh 与 en 均无缺失 |
| 线上一致性 | 主页 80263 / Portfolio 74827 / 资源页 16624 字节 |

---

## 2026-11-05 15:20｜公众号文章配图方案（图文丢失修复）

### 问题

公众号文章 HTML 生成后，粘贴到公众号编辑器时**所有图片丢失**。

**根因**：生成的 HTML 里图片用的是本地相对路径 `images/xxx.jpg`。公众号编辑器粘贴时只会去抓**公网绝对 URL**，相对路径指向本机磁盘，服务器抓不到 → 全部变成裂图。

### 解决方案

图片先同步到服务器，再用公网绝对 URL 引用。

**新增目录**：`site/img/article/`（10 张图，已同步线上）

| 文件 | 内容 | 体积 |
|---|---|---|
| 01_cover.jpg | 封面 | 110 KB |
| 02_annotate.jpg | 文字统一对话框 | 32 KB |
| 03_coverings_columns.jpg | 覆面柱效果 | 13 KB |
| 04_prokit_menu.jpg | ProKit 菜单 | 72 KB |
| 05_cabinet_types.jpg | 橱柜类型面板 | 118 KB |
| 06_cabinets_result.jpg | 橱柜成品效果 | 51 KB |
| 07_tools_menu.jpg | 16 个工具菜单 | 51 KB |
| 08_guide_home.jpg | 教程站首页 | 170 KB |
| 09_index.jpg | 全量文章索引 | 146 KB |
| 10_quickref.jpg | 中文主线速查 | 174 KB |

公网地址：`https://www.kbitai.com.cn/resources/AC_Tutorial/ci_tools/site/img/article/`

**图片处理**：原 PNG 封面 1524 KB → JPEG q88 后 110 KB；三张教程站截图同理压缩，总体积从 2864 KB 降到 1108 KB。公众号单图上限 2 MB，压缩后留足余量。

### 服务器配置验证

| 检查项 | 结果 |
|---|---|
| 无 Referer 访问 | 200 |
| 带 `Referer: mp.weixin.qq.com` | 200 |
| 微信客户端 UA（iOS/Android） | 200 |
| Content-Type | image/jpeg |
| 防盗链 / Referrer-Policy | 无限制 |

结论：微信服务器抓图无任何障碍。

### 构建脚本改造

`build_article.py` 增加三种输出模式：

```bash
python3 build_article.py "文章.md"                    # 本地预览版（相对路径）
python3 build_article.py "文章.md" --online           # 公网版（绝对 URL）
python3 build_article.py "文章.md" --online --copy    # 公网版 + 一键复制按钮
python3 build_article.py "文章.md" --embed            # 单文件内嵌版（base64，离线可用）
```

新增 `IMG_MAP` 映射表（本地文件名 → 服务器文件名），`to_online()` 做路径替换，`to_embedded()` 做 base64 内嵌。公网版生成时自动校验「无残留相对路径 + 映射齐全」。

### 验证

| 项目 | 结果 |
|---|---|
| 公网版图片加载 | 10/10 成功，0 破图 |
| 内嵌版图片加载 | 10/10 成功，0 远程依赖 |
| 文件体积 | 公网版 16 KB｜内嵌版 3.7 MB |
| 破图检查 | 浏览器 DOM 检测 naturalWidth，全部 > 0 |

### 备注

- 发布公众号用 `--online` 版本；图片靠微信自动转存到 CDN
- 其他自媒体平台（知乎/头条等）若不转存外链图，用 `--embed` 单文件版
- 纯文本粘贴（记事本→公众号）必然丢图，这是所有平台通病，不是本项目问题

---

## 2026-11-05 15:50｜公众号「内容插入失败」修复（图床方案）

### 问题

第一版改用公网绝对 URL 后，粘贴到公众号仍报「7 个内容插入失败」。

### 根因（查证结论）

微信编辑器有**两层过滤**，不只是「URL 要能访问」：

1. **只抓公网绝对 URL** —— 相对路径（`images/x.jpg`）必然丢图
2. **过滤第三方域名** —— 自有域名 `www.kbitai.com.cn` 的图在粘贴时也可能被拦

微信官方图床（`mmbiz.qpic.cn`）需 AppID + AppSecret，未认证订阅号无素材管理 API 权限，此路不通。

### 方案：改用 imgurl.org 图床

第三方图床域名是各家编辑器默认信任的，粘贴时微信能正常抓取并转存到自己的 CDN。

- 接口：`POST https://www.imgurl.org/api/v3/upload`
- 鉴权：`Authorization: Bearer sk-xxx`（**注意 Bearer 前缀**）
- 凭据走环境变量 `IMGURL_TOKEN`，不入代码
- 10 张图全部上传成功，实际存储域名 `s3.bmp.ovh`

### 兼容性处理

微信编辑器只认 inline style，class 和外部样式表被整段过滤。正文已做以下替换：

| 原标签 | 改成 | 原因 |
|---|---|---|
| `<code>` | `<span>` + 内联样式 | code 标签容易被丢弃 |
| `<hr>` | `<p>` + border-top | hr 可能整段被吞 |
| `<table>` | 加 `border="1"` + 内联样式 | table 处理不稳定 |
| `<blockquote>` | 加内联样式 | 只认 inline style |
| `<img>` | 图床绝对 URL | 相对路径/自家域名可能被拦 |

最终正文 18 种标签、260 个元素，**风险标签 0 个**。

### 复制逻辑改造

一键复制按钮在复制前会：把 CSS 规则内联成 style 属性 → 清掉 id/class/data-* → 输出图床 URL 的 HTML。

实测剪贴板内容：10 张图全为图床 URL、245 处内联样式、0 个 class、0 个 id。

### 验证

用 Playwright 模拟公众号接收粘贴内容后渲染：

| 项目 | 结果 |
|---|---|
| 剪贴板图片数 | 10 |
| 模拟渲染加载 | 10/10 成功 |
| 破图 | 0 |
| 表格边框/表头底色 | 完整正常 |
| 引用块、行内代码样式 | 正常 |

### 备注

- 公众号上传图床需 AppID + AppSecret，未认证订阅号无权限，故不采用
- 自有服务器那份图保留作备用（`site/img/article/`）
- 本次尝试改 nginx 加 CORS 头时配置嵌套位置有误，已回滚，线上未受影响
