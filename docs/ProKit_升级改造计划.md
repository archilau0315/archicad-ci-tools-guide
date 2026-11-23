# ProKit 升级改造计划 · AC30 版教程

> 版本：v1.2（实施与本地验收完成）
> 日期：2026-11-24
> 范围：`resources/AC_Tutorial/ci_tools` 全站（24 页、18 工具、424 篇：391 篇工具 + 33 篇入门）
> 状态：**P0–P5 已实施并通过本地验收；P6 发布未执行**

**已确认的四个决策**

| 决策 | 结论 |
|---|---|
| 站名 | **ProKit / CI Tools（旧）** |
| Core 四页 | **按 AC30 官方手册重写**，配官方手册图片 |
| 内容口径 | **双轨制**：Core 4 跟官方手册，Suite 11 跟 MyCi |
| 使用场景 | **内部站点**，官方图片与译文版权风险可接受；仍保留来源标注 |

---

## 一、结论先说

这次不是"改个名"，而是**产品归属变了**：CI Tools 从 Central Innovation（Cadimage）的第三方插件，变成 Graphisoft 自有产品线 **Archicad ProKit**，拆成 Core / Suite 两个安装包，授权方式、下载渠道、官方文档位置全部换了。

三条判断：

1. **站点主干不动，改外壳 + 补差异**。422 篇文章的操作逻辑没变（Suite 11 个工具官方仍直接甩回 MyCi 知识库），没必要重写。真正要重写的是**入门安装章**和**4 个 Core 工具页**——它们第一次有了官方手册。
2. **标题保留 "CI Tools" 作为副标**。全网存量搜索、你已发布的 422 个文章锚点都指向 CI Tools。直接抹掉老名字等于自断流量；建议主标题用 ProKit，副标题写"含 CI Tools 旧版"。
3. **新增一页「ProKit vs CI Tools」对照页**。这是当前最大的信息缺口：用户分不清自己装的是哪个包、为什么菜单里没有、能不能买卖。一页讲清，比在 18 个页面里各写一句强。

---

## 二、官方依据（本次核实的原始出处）

| 来源 | 关键事实 |
|---|---|
| [Graphisoft ProKit 下载页](https://www.graphisoft.com/en-at/downloads/add-ons/prokit/) | 官方明说 ProKit「builds on the legacy of the former CI Tools / Cadimage Tools」。两个安装包；Core 含 4 个工具、Suite 含 11 个；Core 版本 `3001-1.2`（2026-10-07），Suite 同版本、安装包约 1 GB |
| 同上 | **授权差异**：Suite 只随 Archicad Collaborate / Archicad Max 全球提供；Core 只在部分国家 + 部分计划（Studio / Collaborate / Max）提供 |
| [AC30 帮助 · ProKit Core Tools](https://help.graphisoft.com/AC/30/INT/Topics/960_Prokit/ProKit_Core/prokit_core_tools.html) | 4 个工具：Annotate、Detail Elements、Time Tracker、Transformer，各有独立官方页；标明「Not available in all markets」；**警告：用了 ProKit 的项目不建议另存回旧版本** |
| [AC30 帮助 · ProKit Suite Tools](https://help.graphisoft.com/AC/30/INT/Topics/960_Prokit/ProKit_Suite/prokit_suite_tools.html) | 11 个工具（Cabinets / Coverings / Doors and Windows / Electrical / Fitout / Keynotes / Metadata / Quantities / Sites / Stairs / Structure），**官方不写手册，逐个链接回 MyCi 知识库**；同样的另存警告 |
| [AC30 帮助 · Annotate](https://help.graphisoft.com/AC/30/INT/Topics/960_Prokit/ProKit_Core/Annotate/AnnotateIntro.html) | AC30 把大小写 / 字体 / 属性替换合并成 **ProKit > Annotate > Replace** 一个对话框，下设三个规则管理器；旧版是分散菜单项 |
| [AC30 帮助 · Transformer](https://help.graphisoft.com/AC/30/INT/Topics/960_Prokit/ProKit_Core/Transformer/Transformer_Intro.html) | 命令在 **ProKit > Transformer** 菜单：镜像 / 移动 / 旋转整个项目 + Set Project Origin；**不可撤销** |
| [AC30 帮助 · Time Tracker](https://help.graphisoft.com/AC/30/INT/Topics/960_Prokit/ProKit_Core/TimeTracker/Tracker_HowTo.html) | 入口 **ProKit > Time Tracker > Timer Palette**；Job / Task 两级；工时写 `.csv`，可连续追加 |
| [AC30 帮助 · Detail Elements](https://help.graphisoft.com/AC/30/INT/Topics/960_Prokit/ProKit_Core/DetailElements/DetailAddTool.html) | 需要**工具箱里的 Detail Element 工具** + **Detail Elements 图库包**；菜单命令同挂 ProKit 菜单；工具箱缺失时可手工添加 |
| [MyCi 知识库首页](https://cadimage.zendesk.com/hc/en-us) | 已整版改成 ProKit 分区：Getting Started、LaunchPad、Annotate…NZ Bracing（仅新西兰）；文章标题统一前缀「ProKit … – Start here」——**Suite 的官方内容仍在这里** |
| [Labeller 介绍（Central Innovation）](https://centralinnovation.com/resources/use-the-new-ci-tools-labeller-to-label-surfaces-with-ease) | Labeller 是免费 CI Tools 工具，**不在 ProKit 两个包的清单里**，MyCi 的 ProKit 分区也没收录 |

> 未能取到正文的一条：[Introducing ProKit for Archicad（Graphisoft 支持站）](https://support.graphisoft.com/hc/en-us/articles/51633416621073-Introducing-ProKit-for-Archicad)，页面抓取为空，列为待人工核验项。

---

## 三、现状盘点（改造前的基线）

| 项 | 现状 |
|---|---|
| 页面数 | 23：18 个工具页（含 Launchpad、Bracing、Labeller）+ 5 个通用页（index / gettingstarted / all / guide / about） |
| 文章数 | 422 篇（`class="art"` 锚点统计） |
| 品牌字样 | 全站 "CI Tools" 出现 **392 处 / 26 个文件**；已有 15 个文件提到 ProKit（部分内容改过一半） |
| 双语 | 同页双份 DOM：`.zh-only` / `.en-only`，`html[data-lang]` 切换，`localStorage` 记忆 |
| 搜索 | `search.js` + `search-index.js`（84 KB），索引 18 工具 + 5 页 + 422 篇；工具表硬编码在 `source/build_search_index.py` 的 `TOOLS` |
| 图片 | 正文图片 **3879 个 `<img>`，几乎全部指向第三方 CDN（`aka.doubaocdn.com`）**；本地 `assets/img` 仅 25 张 |
| 构建 | `build_site.py`（38 KB，依赖已不存在的 `clean.json`，实际是"一次性生成器"）；`build_search_index.py` 可重跑；`tools/*.py` 是文章导入脚本 |
| 命令路径 | 混乱：Annotate / Transformer / Time Tracker / Keynotes / MetaData / Quantities / Launchpad 写 `CI Tools →`；其余 11 个写 `工具箱 → ProKit X`——**两种都不符合官方 `ProKit > X` 菜单** |
| 描述文案 | index 的 meta 写「419 篇官方文档、1330 张截图」，实际 422 篇；截图数无法核对 |

---

## 四、差异清单（官方 vs 教程）

### 4.1 命名

| 教程现名 | 官方名称 | 处理 |
|---|---|---|
| CI Tools（全站） | Archicad ProKit | 主品牌替换，旧名降为副标 + 保留搜索别名 |
| Structural | **Structure**（下载页）/ Structural（KB 文章标题） | 页面保留 structural.html；正文用 "ProKit Structure"，首次出现括注 Structural |
| Sites | **Site**（下载页）/ Sites（KB） | 同上，正文统一 "ProKit Site" |
| MetaData | **Metadata**（下载页）/ MetaData（KB） | 正文用 Metadata，保留 MetaData 作为搜索别名 |
| Doors+Windows | **Doors + Windows** | 仅统一写法与菜单路径 |
| Labeller | 无 ProKit 名 | 标注「CI Tools 免费工具，未纳入 ProKit 包」，页面保留 |
| Bracing | NZ Bracing（仅新西兰） | 标注市场限制 |
| Launchpad | LaunchPad | 统一大小写 |

### 4.2 结构性缺口

1. **没有 ProKit 授权 / 获取路径说明**：Core 与 Suite 的套餐包含关系、按国家差异、安装包版本与大小，教程完全没写，`gettingstarted.html` 仍以 MyCi 老安装流程为主（该页 "CI Tools" 出现 92 次）。
2. **没有版本兼容警告**：官方两句硬话——「用了 ProKit 的项目不要另存回旧版」「两版之间要用匹配的插件版本」，教程未收录。
3. **没有「我到底装了哪个包」的判断法**：ProKit Core / ProKit Suite / 老 CI Tools 三者装完后菜单、工具箱、图库包表现不同。
4. **详情页缺官方出处**：4 个 Core 工具现在有权威 AC30 帮助页，教程页未链过去，用户无法自助核对。
5. **搜索不认 ProKit**：索引关键词里没有 `prokit`、`cadimage`、`3001`，搜 "prokit" 命中率靠标题里的零星出现。

---

## 五、改造方案

### 5.1 站点定位与信息架构

- 站点名：**ProKit / CI Tools（旧）**；`<h1>` 写 `Archicad ProKit 完全指南`，其下一行小字 `CI Tools（旧）· AC30 版`
- 导航分三组，替代现在的"工具卡片平铺"：
  - **ProKit Core（4）**：Annotate / Detail Elements / Time Tracker / Transformer — 标"官方手册已覆盖"
  - **ProKit Suite（11）**：Cabinets / Coverings / Doors + Windows / Electrical / Fitout / Keynotes / Metadata / Quantities / Site / Stairs / Structure — 标"随 Collaborate / Max 提供"
  - **其他 / 旧版（3）**：LaunchPad、NZ Bracing（仅 NZ）、Labeller（免费，未入包）
- 新增页面：**`differences.html`「ProKit 与 CI Tools 有什么不同」**（包构成、授权、市场、菜单、迁移注意事项、另存警告）
- URL 全部保持不变（`site/*.html`），避免已发布锚点与外链失效。

### 5.2 页面级改造清单

| 页面 | 改动 | 类型 |
|---|---|---|
| `index.html` | 标题/副标/工具卡片分组/版本徽标/新增 differences 入口；meta 描述数字校正 | 结构 |
| `gettingstarted.html` | **重写**：ProKit 两包下载与版本号 → 套餐与市场判断 → 安装三步骤 → 工作环境与图库包 → 装完自检 → 另存兼容警告；保留 AC24–29 的 CI Tools 安装折叠区 | 重写 |
| `differences.html` | 新建 | 新建 |
| `annotate.html` | **按 AC30 官方结构重写**（5 个官方子页：Replace 对话框、属性替换、字体替换、大小写例外、注释替换）；配官方 12 张图；补官方链接 | 重写 |
| `transformer.html` | **重写**：ProKit > Transformer 四项 + "不可撤销"警示；配官方 4 张图；官方链接 | 重写 |
| `timetracker.html` | **重写**：Timer Palette、Job/Task 两级、CSV 工时文件；配官方 5 张图；官方链接 | 重写 |
| `detail.html` | **重写**：工具箱 Detail Element + 图库包双前提、手工添加工具箱步骤；配官方 11 张图；官方链接 | 重写 |
| `cabinets.html` … `structural.html`（11 篇） | 只换外壳：品牌、菜单路径、页面徽标、官方入口链接（MyCi 分类），正文不动 | 批量 |
| `bracing.html` | 标注「NZ Only」+ ProKit 包不含 | 微调 |
| `labeller.html` | 标注「免费独立工具，ProKit 未收录」 | 微调 |
| `launchpad.html` | 大小写统一 LaunchPad + 菜单路径 | 微调 |
| `guide.html` | 16 工具速查 → 18 工具，命令路径统一 | 改写 |
| `about.html` | 来源改为「Graphisoft AC30 帮助 + MyCi 知识库」，写清两套文档分工 | 改写 |
| `all.html` | 分组标题随工具改名 | 批量 |
| `search-index.js` | 重新生成（脚本内 TOOLS 表同步改名 + 加别名） | 生成物 |

### 5.3 术语与命令路径规则（脚本化执行的基础）

统一替换表（按顺序，避免二次替换）：

1. 品牌：`CI Tools` → `ProKit`（**例外**：涉及 AC28/29 旧入口、旧安装包、MyCi 旧链接时保留 CI Tools，见下条）
2. 旧入口写法：`CI Tools → <Tool> → <命令>` → `ProKit > <Tool> > <命令>（AC28 及更早：CI Tools > <Tool>）`
3. 菜单符号：`→` 统一为 `>`；`工具箱 → ProKit X` 不成立，改为 `ProKit > X`（Detail Elements 除外，它是工具箱工具）
4. 工具名：Structural→Structure、Sites→Site、MetaData→Metadata、Doors+Windows→Doors + Windows、Launchpad→LaunchPad（**仅在英文正文与命令路径中替换，中文名不变**）
5. 每条工具页顶部加徽标：`ProKit Core` / `ProKit Suite` / `旧版工具`，以及 `AC30 官方手册` 链接或 `MyCi 知识库` 链接

**不做全局无脑替换**：392 处里约 1/3 属于历史语境（"AC28 及更早没有这个对话框""老版 CI Tools 从 MyCi 下载"），这些必须保留原名。执行方式见 5.4。

### 5.4 实施方式：一个脚本 + 人工复核，不做手工 392 处修改

新建 `source/rebrand_prokit.py`（预计 200–300 行，符合 ≤500 行约束）：

```
输入：site/*.html
规则：
  1. 上下文白名单段落（含 AC28/AC29/旧版/MyCi/Cadimage 的句子）跳过替换
  2. 命令路径正则统一：CI Tools\s*(→|>)\s* → ProKit >
  3. 工具箱误写修正："工具箱 → ProKit X" → "ProKit > X"（Detail Elements 白名单）
  4. 双语文档同步：.zh-only 与 .en-only 两段分别替换，替换后校验两段命中数一致
  5. 干跑模式 --dry-run 输出逐文件 diff 摘要（文件、替换次数、跳过次数）
  6. 不改 <title> 里的中文名，只改品牌前缀
输出：改写后的 html + 迁移报告 rebrand_report.md
```

配套调整：

- `build_search_index.py`：TOOLS 表改名 + 命令路径 + 关键词补 `prokit` `cadimage` `ac30` `core` `suite`；`PAGES` 增加 `differences.html`；重新生成索引
- `build_site.py`：BOOKS 与 ORDER 同步分组（Core / Suite / 其他），供后续重新生成时不再回退
- `readme.md`：标题、简介、模块清单、搜索说明同步；中英文双份
- `debug_log_3.md`：按规则记录（`debug_log_2.md` 已超 300 行，接近阈值时新开）

### 5.6 官方手册采集（Core 4 专用，实测可行）

实测：AC30 帮助 ProKit Core 共 **14 页、32 张图**，图片为相对路径 `../../../../Graphics/*.png`，直链全部返回 200，单张约 25 KB。

新建 `source/fetch_prokit_manual.py`（150–200 行）：

```
输入：官方 14 个页面 URL（写死在脚本里的清单）
输出：
  docs/prokit_manual/            14 页 HTML 快照（作为重写时的对照底本）
  site/img/prokit/<tool>/        官方配图按页面归属分目录（实际采用 31 张）
  docs/prokit_manual/manifest.json
      每张图记录：本地路径、原始 URL、抓取日期、MD5
规则：
  1. 跳过已存在且 MD5 一致的图，支持增量更新
  2. 单页抓取失败不中断，最后汇总失败清单
  3. 中文文件名一律用工具 id + 序号，避免空格与大小写问题
```

页面引用规范：

- 图片走站点内相对路径 `img/prokit/annotate/01.png`，**禁止直链官方 URL**
- 每张图用 `<figure>` + `<figcaption>`，图下加一行来源角标：`来源：Graphisoft AC30 帮助 · ProKit Annotate`
- 只配操作关键界面（打开方式、对话框、结果对比），装饰性图不搬
- `<img>` 统一 `max-width:100%`，alt 中英各一份（`.zh-only` / `.en-only` 分别给 alt 不现实，改为 `alt` 写英文、图注写双语）

### 5.7 质量校验（不依赖人工逐页看）

新增 `source/verify_site.py`（100–150 行）：

1. 页面数 = 24（新增 differences）
2. 每页 `<title>` 含 ProKit；`about/differences` 允许显式提及 CI Tools
3. 双语配对：每页 `.zh-only` 与 `.en-only` 块数量差 ≤ 2
4. 命令路径：不得出现 `CI Tools →` / `CI Tools >`（白名单段落除外）、不得出现 `工具箱 → ProKit`
5. 链接：站内链接全部存在；每页对外官方链接数 ≥ 1
6. 索引：JSON 可解析；工具数 = 18；文章数 = 424；搜 "prokit" 命中 ≥ 15
7. 搜索回归：`算量` / `镜像` / `convert case` / `prokit quantities` / `ci tools` 五组查询，首条正确
8. 图片：Core 4 页的 `<img>` 全部指向 `img/prokit/`，本地文件存在；全站无 `help.graphisoft.com` 直链图片
9. 徽标：每页恰有一个包包徽标（Core / Suite / 旧版工具），且与工具归属表一致

---

## 六、分阶段实施

| 阶段 | 内容 | 前置 |
|---|---|---|
| **P0 事实定稿** | 把第二节的官方事实落成 `docs/ProKit_事实卡.md`（一页表格，含版本号、套餐、市场、警告原文链接）；人工核验 1 条抓取失败的官方文章 | 无 |
| **P1 框架与导航** | index 改名与分组、differences 新建、about 改写、readme 双语更新；先不动 18 个工具页 | P0 |
| **P2 入门章重写** | gettingstarted 全量重写（ProKit 安装 + 授权判断 + 自检 + 兼容警告） | P1 |
| **P3a 手册采集** | `fetch_prokit_manual.py` 抓 14 页 + 32 图，生成 manifest；人工核对图与页面归属 | P0 |
| **P3b Core 四页重写** | Annotate / Transformer / Time Tracker / Detail Elements 按官方结构重写，内嵌本地图，补官方链接 | P3a、P1 |
| **P4 Suite 十一页 + 3 个旧版工具** | 跑 rebrand 脚本 → 人工复核 18 页徽标与命令路径 → 微调 Bracing / Labeller / LaunchPad | P1、P3b（复用规则） |
| **P5 搜索与全站 QA** | 重建索引、跑 verify_site、五组查询回归、双语抽查 10 页 | P4 |
| **P6 发布** | 本地起站全站抽查 → 同步阿里云 → git 提交（ci_tools 独立仓库 + resources 子仓库） → 记录 debug_log | P5 |

顺序原则：**先封面后内容**（P1 先行，站点随时可发布一版"改名完成"的状态），**先官方有据的 4 页，再批量 11 页**，避免在事实没定稿时批量改 422 篇。

---

## 七、验收标准

- [x] 全站主标题为 ProKit，副标保留 CI Tools；搜索 "ci tools" 与 "prokit" 都能命中相关页面
- [x] index 的工具分组为 Core 4 / Suite 11 / 其他 3，每组标注授权与市场限制
- [x] `differences.html` 能回答四个问题：装的是哪个包、为什么菜单没有、能不能买、能不能另存回旧版
- [x] gettingstarted 给出 Core / Suite 两包下载入口、版本号、套餐判断表、装完自检清单
- [x] 4 个 Core 工具页每条命令都与 AC30 官方帮助一致，配官方截图（本地镜像），并链到官方页
- [x] 11 个 Suite 工具页命令路径统一为 `ProKit > X`，页面顶部链到对应 MyCi 分类
- [x] Bracing 标 NZ Only、Labeller 标"未纳入 ProKit 包"
- [x] 双语文章标题与正文配对，入门页中英切换及旧版折叠归档通过 Edge 实测
- [x] verify_site 全过；五组搜索查询首条正确
- [x] 当前 424 篇文章的站内链接与锚点校验通过（不代表外部 URL 可用性保证）

---

## 八、风险与对策

| 风险 | 影响 | 对策 |
|---|---|---|
| **正文图片 3879 张全在第三方 CDN** | 对方改版或限流，教程变"文字版" | 本次不处理，但列入技术债；P6 后单独做一次"图片镜像到本站 assets"的任务，脚本按 URL 去重下载并改写 src。官方 32 张图（Core 4）本次就落地到本地，不依赖 CDN |
| Suite 11 个工具官方无 AC30 手册 | 无法核对命令是否变化 | 以 MyCi「ProKit X – Start here」为基线，逐页标注"依据 MyCi（日期）"；菜单名以实际安装截图为准，拿不到就写"以 ProKit 菜单为准" |
| Core 工具"Not available in all markets" | 国内用户可能装不上 | 安装章明确写清市场限制与获取途径，避免用户下完发现无授权 |
| 另存回旧版本导致项目损坏 | 用户数据风险 | differences + 每个 Core 页面顶部统一警示条 |
| 全局替换误伤历史语义 | 教程自相矛盾 | 脚本白名单 + `--dry-run` 报告 + 人工复核 18 页 |
| 双语不同步 | 英文页残留 "CI Tools"，中文页残留 "ProKit" | verify_site 校验 + 脚本内双段计数比对 |
| 存量外链与 SEO | 422 个锚点、已发布链接失效 | URL 与锚点 ID 一律不动，只改标题与正文 |
| Labeller 归属未定 | 可能后续被并入 ProKit | 页面加"截至 2026-11 官方未收录"，并留脚注便于更新 |

---

## 九、决策记录与剩余事项

**已定（2026-11-23）**

1. 站名「ProKit / CI Tools（旧）」——采用。
2. Core 四页按 AC30 官方结构重写，结构变化处保留原锚点（新增内容挂旧锚点后，不删旧 id）。
3. 内容双轨：Core 跟官方手册、Suite 跟 MyCi，页头分别标注依据。
4. 站点为内部使用，官方图片可下载转载；仍保留「来源：Graphisoft AC30 帮助」角标，便于日后版本对照。

**剩余 2 项（不阻塞 P0/P1）**

- **授权说明**：是否写"国内怎么拿到 ProKit"（套餐与购买途径属实操建议，非官方原文），建议放进 `differences.html` 的折叠段。
- **MyCi 图片镜像**：现有 3879 张第三方 CDN 图本次不动，P6 之后单独立项。

开工顺序：P0（事实卡）→ P1（框架与导航），每步先给 diff 摘要再提交。

---

## 十、English Summary

The AC30 release rebrands CI Tools as **Archicad ProKit**, split into **ProKit Core** (Annotate, Detail Elements, Time Tracker, Transformer — now documented in the official AC30 help) and **ProKit Suite** (11 tools — official help still defers to the MyCi knowledge base). Licensing and market availability differ per package, and Graphisoft warns against back-saving projects that use ProKit.

Implementation: preserved all tool-page URLs and legacy anchors, rebranded the shell (title, navigation grouped by Core / Suite / legacy, per-page badges), added `differences.html`, rewrote Getting Started and the four Core tool pages against official docs, and retained 27 legacy setup articles in a collapsed archive. The current site contains 424 articles: 391 tool articles plus 33 Getting Started articles. P0–P5 passed local static and Edge browser checks; P6 deployment has not been performed.

Confirmed decisions: site title **ProKit / CI Tools (legacy)**; Core pages rewritten from the official AC30 manual; dual-track sourcing (Core = official help, Suite = MyCi); internal-only site. Fourteen official pages were captured, with 31 selected screenshots mirrored under `site/img/prokit/` and source captions retained.
