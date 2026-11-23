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
