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
