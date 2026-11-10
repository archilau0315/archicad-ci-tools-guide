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
