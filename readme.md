<div align="center">

# ProKit / CI Tools（旧）完全指南 · Archicad 插件工具包

**ci_tools** — Archicad ProKit 与旧版 CI Tools 的完整中文操作手册与速查卡<br>
*ProKit (AC30) and legacy CI Tools — bilingual handbook and quick-reference*

[![Version](https://img.shields.io/badge/add--on-3001--1.2-35613f?style=flat-square)](https://www.kbitai.com.cn/resources/AC_Tutorial/ci_tools/site/) [![Articles](https://img.shields.io/badge/articles-422-6d9470?style=flat-square)](https://www.kbitai.com.cn/resources/AC_Tutorial/ci_tools/site/all.html) [![Screenshots](https://img.shields.io/badge/screenshots-3800%2B-35613f?style=flat-square)](https://www.kbitai.com.cn/resources/AC_Tutorial/ci_tools/site/) [![CAD](https://img.shields.io/badge/CAD-ArchiCAD%2030-c0392b?style=flat-square)](https://www.kbitai.com.cn/resources/AC_Tutorial/ci_tools/site/)

**[在线访问](https://www.kbitai.com.cn/resources/AC_Tutorial/ci_tools/site/)** · [ProKit 与 CI Tools 差异](https://www.kbitai.com.cn/resources/AC_Tutorial/ci_tools/site/differences.html) · [中文主线速查](https://www.kbitai.com.cn/resources/AC_Tutorial/ci_tools/site/guide.html) · [全量文章索引](https://www.kbitai.com.cn/resources/AC_Tutorial/ci_tools/site/all.html) · [工具目录](#-工具目录) · [工程结构](#-工程结构)

</div>

---

## 这是什么 / What this is

一套**面向团队内部**的 Archicad 插件教程，覆盖 18 个工具、422 篇文章，全站中英双语。

**内容双轨**：AC30 起 CI Tools 更名为 Graphisoft ProKit，拆成 Core 与 Suite 两个安装包。本教程按官方文档的分工整理——

- **Core 4 个工具**（Annotate / Detail Elements / Time Tracker / Transformer）：以 AC30 官方帮助为唯一依据重写，共 14 页官方手册
- **Suite 11 个工具 + 3 个旧版工具**：官方不提供手册，以 MyCi 知识库为基线，全文译为中文
- **旧版入口**：AC29 及更早的 `CI Tools >` 菜单路径集中保留，便于老项目对照

*Dual-track sourcing: the four Core tools follow the official AC30 help; the eleven Suite tools and three legacy tools follow the MyCi knowledge base (no official manual exists for them). Legacy `CI Tools >` menu paths are kept for projects on AC29 and earlier.*

解决的是一个很具体的问题：<b>插件装了，但不知道从哪儿打开，更不知道"为什么打不开"</b>。

同一套工具曾叫 Cadimage Tools（澳新）、CI Tools（全球），AC30 起叫 ProKit —— 搜老教程用 CI Tools，搜新文档用 ProKit，内容对得上。差异细节见 [differences.html](https://www.kbitai.com.cn/resources/AC_Tutorial/ci_tools/site/differences.html)。

<div align="center">
<table>
<tr>
<td width="50%" valign="top">

**📐 手册板块**　<span style="font-size:12px;color:#6d9470">查得全</span>

16 个工具逐个拆解

- **对话框逐项说明** · 不是"点这里"，是每一栏每一项
- **官方界面截图** · 24 张，取自官方教程文档
- **菜单路径** · 每章开头标明入口位置
- **故障排查表** · 10 种常见症状与解法

</td>
<td width="50%" valign="top">

**⚡ 速查卡板块**　<span style="font-size:12px;color:#6d9470">扫得快</span>

一页纸掌握全貌

- **三步启动** · 每个新项目必做，1 分钟
- **16 工具优先级** · 按该学的顺序排，不是按字母
- **三个易踩的坑** · 90% 的问题都在这
- **先自查模块** · 确认自己机器装了什么

</td>
</tr>
</table>
</div>

---

## 快速开始

<div align="center">

| 步骤 | 动作 | 说明 |
|:---:|---|---|
| **1** | 打开速查卡 | 1 分钟扫完，知道整体该干什么 |
| **2** | 做「先自查」 | 确认自己机器的插件与工作环境状态 |
| **3** | 记住三步启动 | 加载工作环境 → 加载图库包 → 加进工具箱 |
| **4** | 按需查手册 | 遇到具体工具再翻对应章节 |

</div>

### 三步启动（每次新项目必做）

```
1. 文件 → 工作环境 → ProKit Profile → 应用        （AC29 及更早：Ci Tools Profile XX）
2. 文件 → 库管理器 → Add → ProKit 图库包          （AC29 及更早：Ci Tools Macros.libpack）
   ★ 必须选单个 .libpack 文件，选文件夹内容会全空
3. 右键工具箱 → 工具箱设置 → 勾选工具 → ★保存工作环境
```

> **第二步是最容易漏的。** 从 Archicad 29 起，图库包不再自动挂载，必须手动加载进项目。这是"装了却用不了"的头号原因。

*Three steps: load the ProKit work environment, add the ProKit library packs manually, then enable the tools in the toolbox and save the environment.*

---

## 工具目录

按**该学的顺序**排列，不是按字母序。AC30 入口统一为 `ProKit >`，括注为 AC29 及更早的旧路径。

| 包 | 优先级 | 工具 | 一句话 | 入口（AC30 / 旧版） |
|:---:|:---:|---|---|---|
| Core | ★★★ | **Annotate** | 全项目文字大小写、字体、属性批量替换 | ProKit → Annotate → Replace / CI Tools → Annotate |
| Core | ★★★ | **Transformer** | 一键镜像、移动、旋转整个项目；重置原点 | ProKit → Transformer / CI Tools → Transformer |
| Core | ★★★ | **Time Tracker** | 记录各任务工时，导出 CSV | ProKit → Time Tracker → Timer Palette |
| Core | ★★ | **Detail Elements** | 拖拽式参数化二维详图库 | 工具箱 → Detail Element |
| Suite | ★★★ | **Metadata** | 属性与分类的批量操作面板 | ProKit → Metadata / CI Tools → MetaData |
| Suite | ★★ | **Quantities** | 从模型出工程量清单 | ProKit → Quantities |
| Suite | ★★ | **Keynotes** | 规范注释数据库，自动挂注释 | ProKit → Keynotes → Keynotes Palette |
| Suite | ★ | **Coverings** | 墙板柱贴 3D 覆面皮 | ProKit → Coverings |
| Suite | ★ | **Fitout** | 房间一键配齐家具 | ProKit → Fitout |
| Suite | ★ | **Site** | 场地边界与退让（澳新） | ProKit → Site / CI Tools → Sites |
| Suite | ★ | **Cabinets** | 一个对象搞定所有橱柜 | ProKit → Cabinets |
| Suite | ★ | **Doors + Windows** | 异形门窗，尺寸捕捉 | ProKit → Doors + Windows |
| Suite | ★ | **Stairs** | 自由楼梯设计 | ProKit → Stairs |
| Suite | ★ | **Structure** | 桁架、框架、连接件 | ProKit → Structure / CI Tools → Structural |
| Suite | ★ | **Electrical** | 电气符号与回路（无国标库） | ProKit → Electrical |
| 旧版 | ★ | **LaunchPad** | 项目与常用命令统一入口 | MyCi 收录，未列入两个包 |
| 旧版 | ★ | **NZ Bracing** | NZ 木结构抗侧力（仅新西兰） | MyCi 收录，NZ Only |
| 旧版 | — | **Labeller** | 表面标注，免费 CI Tools 工具 | ProKit 未收录 |

*18 tools: 4 in ProKit Core, 11 in ProKit Suite, 3 legacy (LaunchPad, NZ Bracing, Labeller).*

---

## 版本与安装

| 版本 | 工具包名称 | 获取方式 | 注意事项 |
|---|---|---|---|
| Archicad 24 ~ 29 | CI Tools（Cadimage） | MyCi Installer | 库包须手动加载 |
| Archicad 30 及以后 | **ProKit Core** `3001-1.2` | Graphisoft 官网，81 MB（Win） | 仅部分国家 + Studio / Collaborate / Max 计划；Max 全球 |
| Archicad 30 及以后 | **ProKit Suite** `3001-1.2` | Graphisoft 官网，约 1 GB | 随 Collaborate / Max 订阅全球提供 |

**兼容性硬规则**：用了 ProKit 工具的项目**不要另存回旧版本**；跨版本协作时两边插件版本必须匹配。

**区域限制**：Electrical 库含欧盟、印度、撒哈拉以南非洲、英国、美国，**无中国国标库**；Site 为澳新专属；NZ Bracing 仅新西兰。

*Core is limited to specific plans and countries; Suite ships with Collaborate and Max worldwide. Never back-save a project that uses ProKit, and keep add-on versions matched across collaborators.*

---

## 工程结构

```
ci_tools/
├── readme.md                          本文件
├── debug_log_1.md                     变更日志（第 1 册，已满）
├── debug_log_2.md                     变更日志（第 2 册）
├── site/                              ★在线站点，24 个页面
│   ├── index.html / all.html …        422 篇文章，18 个工具 + 入门
│   ├── differences.html               ★ProKit 与 CI Tools 版本差异
│   ├── search.css / search.js         顶部全站搜索条（智能匹配 + 自动补全）
│   └── search-index.js                搜索索引，自动生成，勿手改
├── source/                            站点生成器
│   ├── build_site.py                  clean.json → 多页站点
│   ├── build_search_index.py          扫描站点，生成 search-index.js
│   ├── clean_html.py                  官方 Word HTML → Markdown
│   ├── zh_translations.json           中文译文
│   └── handbook_main.md               中文主线速查原稿
├── docs/
│   ├── ProKit_升级改造计划.md          ★AC30 升级改造计划（P0–P6）
│   ├── ProKit_事实卡.md               ★官方事实唯一来源（授权、版本、菜单、链接）
│   ├── CI_Tools_用户手册_图文版.html    ★推荐阅读，24 章节 + 24 张官方截图
│   ├── CI_Tools_速查卡_网页版.html      ★推荐阅读，一页纸速查
│   ├── CI_Tools_用户手册.md            纯文字版，便于检索与二次编辑
│   ├── CI_Tools_速查卡.md              纯文字版，打印用
│   └── manual_master.md               网页版主稿（改内容从这里下手）
├── assets/
│   └── img/                           本地截图（手册用 24 张）
│       └── tool_image_map.json        图床直链映射表
└── tools/
    ├── beautify.py                    美化管线：md → html 全流程
    └── localize_images.py             图片本地化：远程图转本地相对路径
```

**两个 HTML 完全自包含** —— 图片走相对路径指向 `assets/img/`，字体带本地回退。整个目录可直接拷贝、离线打开、随项目迁移。

---

## 维护方式

### 改内容

```bash
# 1. 改主稿
vim docs/manual_master.md

# 2. 重新生成 HTML（自动注入字体、目录、补图片尺寸）
python3 tools/beautify.py docs/manual_master.md docs/CI_Tools_用户手册_图文版.html "Archicad CI Tools 完整用户手册"

# 3. 图片转本地
python3 tools/localize_images.py docs/CI_Tools_用户手册_图文版.html assets/img
```

### 补图

1. 从官方知识库取图：`https://cadimage.zendesk.com/hc/en-us`
2. 压缩后放入 `assets/img/`
3. 在 `manual_master.md` 里用相对路径引用：`![说明](../assets/img/xxx.jpg)`

### 双语切换

右上角 **中文 / EN** 按钮一键切换，选择记忆在浏览器本地（localStorage 键 `citools-lang`）。

也支持 URL 参数：`?lang=en` / `?lang=zh`，可直接分享特定语言版本，例如
`https://www.kbitai.com.cn/resources/AC_Tutorial/ci_tools/site/quantities.html?lang=en`

**中文模式**显示完整中文译文，每篇文章下方有「英文原文对照」折叠区，展开即见官方英文原文与原图。
**英文模式**界面、导航、标题、正文全部切英文。

### 站内搜索

站点顶部有全站搜索条，随手查命令：

| 操作 | 效果 |
|---|---|
| `Ctrl / Cmd + K` 或 `/` | 光标跳到搜索框 |
| 输入「算量」「镜像」「convert case」 | 按中文口语、工具名、命令路径智能匹配 |
| `↑ ↓` | 上下选择结果 |
| `Enter` | 打开对应工具页或文章锚点 |
| `Esc` | 收起下拉 |

结果按「工具 / 篇章 / 页面」分组标注，命中字符高亮；空输入时显示最近查看与 18 个工具的常用命令。

标题或命令有变动后，重建索引即可（`build_site.py` 会自动调用）：

```bash
python3 source/build_search_index.py site
```

`site/search-index.js` 是生成物，不手改。

### 重新生成站点

```bash
cd source/
python3 clean_html.py ../articles.json ../clean.json      # 官方 HTML → Markdown
python3 build_site.py .. ../site                         # 生成双语站点
```

译文改动直接编辑 `zh_translations.json` 后重跑生成器即可。

### 部署到线上

站点已部署至 `https://www.kbitai.com.cn/resources/AC_Tutorial/ci_tools/site/`（公网公开，无需登录）。

服务器：阿里云 `47.93.210.248`，Web 根目录 `/www/wwwroot/kbitai.com.cn/`

```bash
# 从 resources 目录打包上传
tar czf - -C /path/to/resources AC_Tutorial/ci_tools/site | \
  ssh -i ~/.ssh/id_ed25519 root@47.93.210.248 \
  "cd /www/wwwroot/kbitai.com.cn/resources && tar xzf - && chown -R www:www AC_Tutorial"
```

### 同步到资料库

资料库版本供云端协作使用：https://workbuddy.link/p/5fCzXnHhFkUQ2Cb0QS5FyA

---

## 内容来源

- **Core 4 个工具**：Graphisoft AC30 官方帮助 https://help.graphisoft.com/AC/30/INT/Topics/960_Prokit/ProKit_Core/prokit_core_tools.html（14 页，2026-11-23 核实）
- **Suite 11 个 + 旧版工具**：MyCi 知识库 https://cadimage.zendesk.com/hc/en-us（2026-10 更新）
- **下载与授权**：https://www.graphisoft.com/downloads/add-ons/prokit/
- **视频课程**：Graphisoft Learn「Getting Started with ProKit Core」1 小时
- **界面截图**：Core 部分随官方手册重写一并对齐；其余取自 MyCi 教学文档

*Core pages follow the AC30 help; Suite and legacy pages follow MyCi. See `docs/ProKit_事实卡.md` for the verified facts behind every claim.*

---

<div align="center">

**ProKit / CI Tools（旧）完全指南** · AC30 重编 2026-11-23 · 天津匡形无界智能科技有限公司<br>
*ProKit / CI Tools (legacy) handbook · AC30 revision, 2026-11-23 · Kuanform Boundless Intelligent Technology*

</div>
