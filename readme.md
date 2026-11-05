<div align="center">

# CI Tools 完全指南 · Archicad 插件工具包

**ci_tools** — Central Innovation CI Tools / Graphisoft ProKit 的完整中文操作手册与速查卡

[![Version](https://img.shields.io/badge/version-v2.0-35613f?style=flat-square)](https://www.kbitai.com.cn/resources/AC_Tutorial/ci_tools/site/) [![Articles](https://img.shields.io/badge/articles-357-6d9470?style=flat-square)](https://www.kbitai.com.cn/resources/AC_Tutorial/ci_tools/site/all.html) [![Screenshots](https://img.shields.io/badge/screenshots-1193-35613f?style=flat-square)](https://www.kbitai.com.cn/resources/AC_Tutorial/ci_tools/site/) [![CAD](https://img.shields.io/badge/CAD-ArchiCAD-c0392b?style=flat-square)](https://www.kbitai.com.cn/resources/AC_Tutorial/ci_tools/site/)

**[在线访问](https://www.kbitai.com.cn/resources/AC_Tutorial/ci_tools/site/)** · [中文主线速查](https://www.kbitai.com.cn/resources/AC_Tutorial/ci_tools/site/guide.html) · [全量文章索引](https://www.kbitai.com.cn/resources/AC_Tutorial/ci_tools/site/all.html) · [工具目录](#-工具目录) · [工程结构](#-工程结构)

</div>

---

## 这是什么

一套**面向全团队**的 Archicad CI Tools 官方教程全量中文版。

内容来自 Central Innovation / Graphisoft 官方 MyCi 知识库，<b>357 篇官方文档全部译为中文、1193 张界面截图</b>，按 16 个工具分册整理。

**全站中英双语，右上角一键切换，默认中文。** 每篇文章下方可展开「英文原文对照」，随时对照官方原图。

解决的是一个很具体的问题：<b>插件装了，但不知道从哪儿打开，更不知道"为什么打不开"</b>。

CI Tools 是 Central Innovation（新西兰）为 Archicad 开发的效率插件包，2026 年起被 Graphisoft 收进自有产品线并改名 **ProKit**。同一套东西，两个名字 —— 搜老教程用 CI Tools，搜新文档用 ProKit，内容对得上。

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
1. 文件 → 工作环境 → Ci Tools Profile XX → 应用
2. 文件 → 库管理器 → Add → Ci Tools Macros.libpack（先加这个）
   ★ 必须选单个 .libpack 文件，选文件夹内容会全空
3. 右键工具箱 → 工具箱设置 → 勾选工具 → ★保存工作环境
```

> **第二步是最容易漏的。** 从 Archicad 29 起，CI Tools 的库包不再自动挂载，必须手动加载进项目。这是"装了却用不了"的头号原因。

---

## 工具目录

按**该学的顺序**排列，不是按字母序。

| 优先级 | 工具 | 一句话 | 入口 |
|:---:|---|---|---|
| ★★★ | **Annotate** | 全项目文字大小写、字体批量改 | CI Tools → Annotate → Convert Case… |
| ★★★ | **MetaData** | 属性与分类的批量操作面板 | CI Tools → MetaData |
| ★★★ | **Time Tracker** | 记录各任务工时，和报价对比 | CI Tools → Time Tracker → Open Time Tracker |
| ★★ | **Quantities** | 从模型出工程量清单 | CI Tools → Quantities |
| ★★ | **Keynotes** | 规范注释数据库，自动挂注释 | CI Tools → Keynotes → Keynotes Palette |
| ★★ | **Transformer** | 一键镜像整个项目 | CI Tools → Transformer → Mirror Project… |
| ★ | **Detail Elements** | 拖拽式参数化二维详图库 | 工具箱 → ProKit Detail Elements |
| ★ | **Coverings** | 墙板柱贴 3D 覆面皮 | 工具箱 → ProKit Coverings |
| ★ | **Fitout** | 房间一键配齐家具 | 工具箱 → ProKit Fitout |
| ★ | **Sites** | 场地边界与退让（澳新） | 工具箱 → ProKit Sites |
| ★ | **Cabinets** | 一个对象搞定所有橱柜 | 工具箱 → ProKit Cabinets |
| ★ | **Doors+Windows** | 异形门窗，尺寸捕捉 | 工具箱 → ProKit Doors+Windows |
| ★ | **Stairs** | 自由楼梯设计 | 工具箱 → ProKit Stairs |
| ★ | **Structural** | 桁架、框架、连接件 | 工具箱 → ProKit Structural |
| ★ | **Electrical** | 电气符号与回路（无国标库） | 工具箱 → ProKit Electrical |
| ★ | **Bracing** | NZ 木结构抗侧力（NZ 专属） | 工具箱 → ProKit Bracing |

---

## 版本与安装

| 版本 | 工具包名称 | 获取方式 | 注意事项 |
|---|---|---|---|
| Archicad 24 ~ 29 | CI Tools | MyCi Installer | 库包须手动加载 |
| Archicad 30 及以后 | ProKit Core / Suite | Graphisoft 官网 | 菜单名改为 ProKit |

**区域限制**：Electrical 库含欧盟、印度、撒哈拉以南非洲、英国、美国，**无中国国标库**；Sites 为澳新专属，Bracing 为新西兰专属。

---

## 工程结构

```
ci_tools/
├── readme.md                          本文件
├── debug_log_1.md                     变更日志
├── docs/
│   ├── CI_Tools_用户手册_图文版.html    ★推荐阅读，24 章节 + 24 张官方截图
│   ├── CI_Tools_速查卡_网页版.html      ★推荐阅读，一页纸速查
│   ├── CI_Tools_用户手册.md            纯文字版，便于检索与二次编辑
│   ├── CI_Tools_速查卡.md              纯文字版，打印用
│   └── manual_master.md               网页版主稿（改内容从这里下手）
├── assets/
│   └── img/                           24 张官方截图（本地化，无外链依赖）
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

- **官方文档**：MyCi 知识库 https://cadimage.zendesk.com/hc/en-us（2026-10 更新）
- **官方下载**：https://www.graphisoft.com/en-gs/downloads/prokit
- **视频课程**：Graphisoft Learn「Getting Started with ProKit Core」1 小时
- **界面截图**：取自官方教程文档，用于教学对照

---

<div align="center">

**CI Tools 完全指南** · 2026-11-05 · 天津匡形无界智能科技有限公司

</div>
