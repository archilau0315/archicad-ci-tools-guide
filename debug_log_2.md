# 变更日志 · 第 2 册

> 承接 `debug_log_1.md`（已满 934 行）。格式：时间 · 模块 · 变更简述 · 备注。

## 2026-11-10 · 站点顶部全站搜索栏（智能搜索 + 自动补全）

**模块**：`site/search.css`（新增）、`site/search.js`（新增）、`site/search-index.js`（新增，自动生成）、`source/build_search_index.py`（新增）、`source/build_site.py`、`site/*.html`（23 页）、`readme.md`

**背景**：全站 422 篇教程、18 个工具，找一条命令只能翻侧栏或全量索引页，缺一个随手可用的入口。

**变更**：
- 新增吸顶搜索条：注入到 23 个页面的 `<main>` 顶部，滚动时固定在页面顶端；右侧预留 116px 避开固定的「中文 / EN」切换。
- 智能匹配：中文按子串、英文按子串 + 子序列（`qty` → Quantities），支持多关键词（空格分隔，需全部命中）；标题、工具名、命令路径、口语关键词分字段加权，工具命中时同工具的文章一起加权。
- 智能补全：输入即出下拉（防抖 70ms），高亮命中字符，`↑↓` 选择、`Enter` 打开、`Esc` 关闭、`Ctrl/Cmd + K` 或 `/` 聚焦；空输入时显示「最近查看」+「常用命令」，最近 6 条记录存 `localStorage`。
- 双语：占位符、徽标（工具 / 篇章 / 页面）、空态文案跟随 `data-lang`，切换语言时用 MutationObserver 即时重绘。
- 索引：`build_search_index.py` 扫描站点 HTML 抽取每篇中英标题（422 篇）+ 18 个工具（含命令路径与中文口语词）+ 5 个页面，输出 82KB 的 `search-index.js`（`window.CI_SEARCH_INDEX`，`file://` 直接打开也能用）。
- `build_site.py`：`page()` 输出 `search.css` / `search-index.js` / `search.js` 引用；`main()` 末尾调用 `build_search_index(out)`，重新生成站点后搜索索引自动重建。

**验证**：本地 `http.server` 起站，浏览器实测——输入「算量」首条为 Quantities、「镜像」首条为 Transformer、「convert case」首条为 Annotate；下拉展开 / Esc 关闭正常；控制台零报错；滚动 900px 后搜索条仍吸顶且不遮挡标题；1440 宽度下与语言切换无重叠。

**备注**：`search-index.js` 为生成物，勿手改；新增或改文章标题后跑一次 `python source/build_search_index.py`（或重跑 `build_site.py`）即可。索引只收标题与命令，不收录正文，体积可控。工具关键词里补了常用缩写（`qty` / `boq` / `tt` / `md` / `elec`），中文查询不做跳跃高亮，避免散点误标。

**部署**：2026-11-10 已同步到阿里云 `47.93.210.248:/www/wwwroot/kbitai.com.cn/resources/AC_Tutorial/ci_tools/`（scp 走 root 密钥，`chown -R www:www`）。站点内 23 个页面均带上 `search.js` 引用，服务器本地 HTTP / HTTPS 请求 `search.js` 均为 200。
**远程仓库**：当天先推到 GitHub `archilau0315/archicad-ci-tools-guide` 的 `main`，后来发现该仓库已由之前的 resources 子仓库（`cd38920` 那条线）发布过，两条独立历史并存。2026-11-10 14:40 按方案 1 用 `--force-with-lease` 把本地独立仓库 HEAD=`d7da9d7` 覆盖远端 main=`c7d93d2`（forced update），远端 22 个原始 commit 被替换。resources 子仓库里的 `guide` 远端同步删去，避免后续误推把远端又改回去。

---

## 2026-11-23 · ProKit 升级改造计划

**模块**：docs / 全站规划
**变更**：新增 `docs/ProKit_升级改造计划.md`。依据 Graphisoft AC30 帮助（ProKit Core / Suite 工具页）与 ProKit 下载页核实：AC30 起 CI Tools 改名 Archicad ProKit，拆 Core（4 工具，官方手册覆盖）与 Suite（11 工具，官方仍指向 MyCi）；版本 3001-1.2；授权按套餐与国家区分；官方警告不可回存旧版。计划含现状基线（23 页 / 18 工具 / 422 篇 / 392 处旧品牌字样）、差异清单、脚本化迁移方案（rebrand_prokit.py + verify_site.py）、P0–P6 阶段、验收标准与风险（含 3879 张图挂第三方 CDN 的技术债）。
**备注**：本轮只写计划，未改站点代码；待用户确认 4 个决策点后按 P0/P1 开工。

---

## 2026-11-23 · ProKit 计划修订 v1.1（决策落定）

**模块**：docs / 全站规划
**变更**：按用户确认更新 `docs/ProKit_升级改造计划.md`：站名定为「ProKit / CI Tools（旧）」；Core 四页改为按 AC30 官方手册重写并配官方图；明确双轨制（Core 跟官方手册、Suite 跟 MyCi）；站点内部使用，版权放开但仍保留来源角标。新增 5.6 官方手册采集小节（14 页 / 32 图，实测直链 200，落 `assets/img/prokit/` + manifest.json），P3 拆成 P3a 采集 / P3b 重写，校验项扩到 9 条。
**备注**：仍未改站点代码；剩余 2 项不阻塞开工（授权说明写不写、MyCi 3879 张 CDN 图是否镜像）。

---

## 2026-11-23 · P0 事实卡 + P1 框架改造

**模块**：docs / site（index、about、differences）/ readme
**变更**：
1. **P0** 新增 `docs/ProKit_事实卡.md`：产品关系、Core/Suite 两包与授权国家、版本 `3001-1.2`、命令路径、另存警告、官方链接、手册规模（14 页 / 32 图）、2 项未核实记录。
2. **P1** 新增 `site/differences.html`（28.6 KB）：六问结构（包里有什么、我装的是哪个、菜单路径变了、版本与兼容、官方文档在哪、FAQ），中英双语，四张对照表，官方链接与来源脚注。
3. **index.html**：站名改 `ProKit / CI Tools（旧）`；工具区拆为 Core 4 / Suite 11 / 旧版 3 三组，各带 `.pkg` 徽标；补 LaunchPad / NZ Bracing / Labeller 三张卡片；三步启动路径改 `ProKit Profile` / `ProKit 图库包`（括注旧路径）；hero 增加双轨依据说明；meta 描述校正为 422 篇 / 3800+ 图；footer 改 AC30 重编。
4. **about.html**：来源改双轨（AC30 官方帮助 14 页 + MyCi 基线），删除「1208 张已本地化」「33 张失效」两处失实描述，改述第三方 CDN 现状；官方入口补 AC30 ProKit Core 帮助；页脚与品牌同步。
5. **readme.md**：标题、徽章（add-on 3001-1.2 / 3800+ 图）、双轨说明、三步启动、18 工具目录（按 Core/Suite/旧版 + AC30 与旧路径对照）、版本授权表、工程结构（24 页，新增两篇 docs）、内容来源与页脚全部双语化。
**备注**：站点共 24 页。验证：HTML 结构配对（div/main/article）全通过、11 项静态断言全过、Edge 无头截图核对首页与差异页；修复一次 CSS 误注入 `</style>` 外导致页面顶部露出样式文本的问题。18 个工具页外壳与搜索索引重建留待 P4/P5。

---

## 2026-11-23 · P4 工具页外壳批量改造

**模块**：site（18 工具页 + guide + all + search-index.js）/ source/rebrand_prokit.py / source/build_search_index.py
**变更**：
1. 新增 `source/rebrand_prokit.py`（约 370 行，含 `--dry-run`）：品牌块、`<title>`、页脚统一为 ProKit / CI Tools（旧）；侧栏改为「开始 / ProKit Core·4 / ProKit Suite·11 / 其他·旧版·3」四段；工具页 hero 插入包徽标与官方入口（Core → Graphisoft AC30 帮助，Suite/LaunchPad/Bracing → MyCi，Labeller → Central Innovation）；`CI Tools > X`、`Ci Tools > X` 统一为 `ProKit > X`。
2. 历史语境行（含 AC28/AC29/旧版/老版/MyCi/Cadimage/legacy/Profile）跳过替换；正文其余内容不动。
3. 工具更名：Structural→Structure、Sites→Site、MetaData→Metadata、Doors+Windows→Doors + Windows、Launchpad→LaunchPad（导航、面包屑、h1、索引同步；URL 与锚点不变）。
4. guide：16→18 工具，补 LaunchPad / Labeller 两节，更新顶部改名说明与旧版流程提示、表格与「暂不建议碰」名单；all：补 LaunchPad / Bracing / Labeller 三个分组（18 组），标题统一官方名。
5. `build_search_index.py`：TOOLS 改名与路径改 `ProKit > ...`，关键词补 `prokit cadimage ac30 core suite`，PAGES 增 differences，重生成 `search-index.js`（18 工具 / 6 页 / 422 篇 / 83 KB）。
**备注**：静态校验通过（徽标 18/18、无白名单外旧命令路径、站内链接全在、索引可解析）；Edge 截图核对首页、Cabinets、Structure、guide、Bracing 正常。差异页对照表保留旧路径 `CI Tools >` 属预期。遗留：`bracing.html`、`sites.html` 存在改造前已有的 div/script 标签计数不平衡（改造前后差值一致，未由本次改动引入），留待 P5 统一修复；`gettingstarted.html` 标题与安装内容仍为旧版，属 P2 重写范围。

---

## 2026-11-24 · P3a/P3b 官方手册采集与 Core 四页重写

**模块**：source/fetch_prokit_manual.py、source/core_content.py、source/build_core_pages.py、site/img/prokit、site 四页、docs/prokit_manual
**变更**：
1. P3a：抓取 AC30 官方 ProKit Core 帮助 14 页 → `docs/prokit_manual/<tool>/`，31 张配图 → `site/img/prokit/<tool>/`，生成 `manifest.json`（本地路径 / 原 URL / MD5 / 页面归属）；增量抓取，单页失败不中断（本次 0 失败）。
2. P3b：按官方手册重写 Annotate（5 篇 / 9 图）、Transformer（2 篇 / 3 图）、Time Tracker（3 篇 / 5 图）、Detail Elements（4 篇 / 7 图），保留页面外壳与双语结构；每张图用 `<figure>` + 本地路径 + 双语图注，文末标注官方来源与原文链接。
3. 内容含官方关键事实：Annotate 五类替换与四种大小写、三种作用范围、`.conversion`；Transformer 四命令且不可撤销；Time Tracker Job/Task 与 `.csv`；Detail Elements 工具箱 + 图库包双前提、69 个对象分 10 个文件夹。
4. 同步 hero 统计、`all.html` / `index.html` Core 目录与锚点、全站篇数 422 → 418（404 篇 MyCi + 14 篇官方编译）、搜索索引重建（18 工具 / 6 页 / 418 篇）。
**备注**：锚点校验 0 死链、Core 页 div/figure/table/ul 全部配对、无官方图片直链；Edge 截图核对 Annotate 与 Detail 正常。图片放在 `site/img/prokit/` 以保证站点目录可独立部署。

---

## 2026-11-24 · P2 入门重写与 P5 全站验收

**模块**：site（入门、目录、侧栏、Bracing、Sites、旧文链接）/ source（4 个新脚本与搜索索引）/ readme / docs

**变更**：
1. 新增 `build_gettingstarted.py`：入门页重写为 6 篇 AC30 主线，覆盖两包授权与市场、版本下载、安装、工作环境与图库、自检、团队协作和兼容警告；27 篇 AC24–AC29 文档原样保留为折叠归档，旧锚点与配图不动。当前总数为工具 391 + 入门 33 = 全站 424。
2. 新增 `sync_catalogs.py`：按工具页实际文章重建 `index.html` / `all.html` 目录，补齐 LaunchPad、Bracing、Labeller，Quantities 修正为实际 122 篇，同步首页、About、README 计数。
3. 新增 `repair_legacy_links.py`：129 个目标已丢失的旧文 `href="#fragment"` 回链至对应 MyCi 官方原文小节；Cabinets 9、Doors 60、Keynotes 12、Quantities 39、Sites 9。
4. 新增 `verify_site.py`：校验 24 页、真实标签嵌套、重复 id、双语文章、站内链接与锚点、18 工具目录、424 篇索引、本地 Core 图片、包徽标及白名单外旧路径；修复 Bracing 中文层少一个 `</div>`，Sites 三处损坏 Vimeo 嵌入改为官方播放器直接链接。
5. 统一首页、差异页等侧栏的 18 个工具名称与分组；更新入门搜索描述和 `ci tools` 差异页关键词，避免旧文章抢占首条。
6. README 补新脚本与维护命令；升级计划更新为 v1.2，标明 P0–P5 本地验收完成、P6 发布未执行。

**验证**：入门、目录和搜索生成器幂等复跑后 5 个目标文件 SHA-256 不变；20 个 Python 脚本语法检查通过；`verify_site.py` 通过。Edge 实测「算量 / 镜像 / convert case / prokit quantities / ci tools」首条分别进入 Quantities / Transformer / Annotate / Quantities / differences；中英切换、27 篇归档展开及 Bracing / Sites 结构断言通过，7 张截图排版正常，无 JavaScript 错误或本地资源 404。

**备注**：本次只验证站内静态结构与本地浏览器交互，未承诺外部 URL 均可访问；未部署、未 push。

---

## 2026-11-24 · P6 发布：ProKit 资源卡封面与主站入口同步

**模块**：cover.jpg、docs/ProKit_升级改造计划.md、主站 index.html、resources/index.html

**变更**：
1. `cover.jpg` 重制为 1000×1000 正方形：顶部改用 AC30 官方 ProKit Annotate 菜单截图，主体为 ProKit / CI Tools（旧）、中英双语与「18 工具 · 424 篇 · 3800+ 图」，清除旧 CI Tools 菜单和 16 / 357 / 1193 旧口径。
2. 主站资源下拉与资源展示卡同步 ProKit 名称、双轨来源和当前统计，中英 HTML 初始文案及语言字典一并更新；所有教程 URL 与锚点保持不变。
3. P6 执行三个已有仓库的既定边界：主站根仓库提交首页入口，ci_tools 独立仓库提交封面与发布记录；`resources/index.html` 按 resources 仓库既有忽略规则不入库。

**验证**：`source/verify_site.py` 通过（24 页 / 18 工具 / 424 篇）；Edge 验证首页桌面下拉、资源卡中英切换、桌面与移动排版、封面完整显示和教程跳转，目标资源无 404、无 JavaScript 错误。

**备注**：发布至 `/www/wwwroot/kbitai.com.cn/` 后，以线上首页、资源页、封面和教程入口复核结果为准。
