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
