# ProKit 事实卡（AC30）

> 用途：站点改写的唯一事实来源。所有页面文案与命令路径以此为准。
> 核实日期：2026-11-23
> 核实方式：Graphisoft 官网下载页 + AC30 官方帮助逐页抓取（14 页全部可访问）

## 1. 产品关系

| 项 | 事实 |
|---|---|
| 现名 | Archicad ProKit |
| 曾用名 | CI Tools（全球）/ Cadimage Tools（澳新） |
| 归属 | Graphisoft 自有产品线（此前为第三方插件） |
| 官网原话 | "builds on the legacy of the former CI Tools previously known to users worldwide as the Cadimage Tools" |
| 官方文档分工 | Core 4 个工具有 AC30 内置帮助；Suite 11 个工具官方仍指向 MyCi 知识库 |

## 2. 两个安装包

### ProKit Core

| 项 | 事实 |
|---|---|
| 工具 | Annotate、Detail Elements、Time Tracker、Transformer |
| 版本 | `3001-1.2`（2026-10-07） |
| 安装包 | Windows `.exe` 81 MB；macOS 76 MB（Apple silicon）/ 67 MB（Intel） |
| 语言包 | INT / FRA / GER |
| 授权 | 仅在指定国家 + 指定计划提供：Studio（AT、BE、DK、FI、FR、DE、NL、NO、SE、CH）、Collaborate（同左 + AU、NZ）、Max（全球所有国家） |
| 市场提示 | 工具页标注 "Not available in all markets" |

### ProKit Suite

| 项 | 事实 |
|---|---|
| 工具 | Cabinets、Coverings、Doors + Windows、Electrical、Fitout、Keynotes、Metadata、Quantities、Site、Stairs、Structure |
| 版本 | `3001-1.2`（2026-10-07） |
| 安装包 | 约 1 GB |
| 授权 | 随 Archicad Collaborate 与 Archicad Max 订阅全球提供 |
| 市场提示 | Site 在 MyCi 分类中标注 NZ Only |

## 3. 不在两个包里的旧工具

| 工具 | 状态 |
|---|---|
| LaunchPad | 在 MyCi 的 ProKit 分区中，下载页未单列 |
| NZ Bracing | MyCi 标注 "NZ Only" |
| Labeller | 免费 CI Tools 工具，两个包与 MyCi ProKit 分区均未收录 |

## 4. 命令路径

| 工具 | 官方路径 |
|---|---|
| Annotate | `ProKit > Annotate > Replace`；另有 Manage Attribute Replacements / Manage Case Standards / Manage Font Replacements |
| Transformer | `ProKit > Transformer`：Mirror / Move / Rotate project、Set Project Origin（不可撤销） |
| Time Tracker | `ProKit > Time Tracker > Timer Palette`；另有 Manage Jobs / Manage Tasks |
| Detail Elements | `ProKit` 菜单；工具本身在**工具箱**里（Detail Element），需 Detail Elements 图库包 |
| Suite 11 个 | `ProKit > <工具名>`（官方未逐条列出，以安装后菜单为准） |

## 5. 兼容性警告（官方原文要点）

- 使用了 ProKit 工具的项目**不建议另存回旧版本**（back-save）。
- 两个 Archicad 版本之间协作时，两边必须使用**版本匹配**的 ProKit 插件，否则出现 ProKit 警告或兼容问题。

## 6. 官方链接清单

| 内容 | URL |
|---|---|
| ProKit 下载页 | https://www.graphisoft.com/en-at/downloads/add-ons/prokit/ |
| Core 工具总览 | https://help.graphisoft.com/AC/30/INT/Topics/960_Prokit/ProKit_Core/prokit_core_tools.html |
| Annotate | https://help.graphisoft.com/AC/30/INT/Topics/960_Prokit/ProKit_Core/Annotate/AnnotateIntro.html |
| Transformer | https://help.graphisoft.com/AC/30/INT/Topics/960_Prokit/ProKit_Core/Transformer/Transformer_Intro.html |
| Time Tracker | https://help.graphisoft.com/AC/30/INT/Topics/960_Prokit/ProKit_Core/TimeTracker/Tracker_HowTo.html |
| Detail Elements | https://help.graphisoft.com/AC/30/INT/Topics/960_Prokit/ProKit_Core/DetailElements/DetailAddTool.html |
| Suite 工具总览 | https://help.graphisoft.com/AC/30/INT/Topics/960_Prokit/ProKit_Suite/prokit_suite_tools.html |
| MyCi 知识库 | https://cadimage.zendesk.com/hc/en-us |

## 7. 官方手册规模（实测）

| 工具 | 官方页数 | 配图 |
|---|---|---|
| Annotate | 5 | 12 |
| Transformer | 2 | 4 |
| Time Tracker | 3 | 5 |
| Detail Elements | 4 | 11 |
| 合计 | **14** | **32** |

图片直链：`https://help.graphisoft.com/AC/30/INT/Graphics/*.png`，均返回 200，单张约 25 KB。

## 8. 未核实项

- `Introducing ProKit for Archicad`（support.graphisoft.com 文章）正文抓取为空，仅记录链接，不引用其中任何说法。
- Work Environment 配置文件在新安装包中的确切名称未核实；页面文案统一写「ProKit 工作环境」，旧版路径括注「Ci Tools Profile」。
