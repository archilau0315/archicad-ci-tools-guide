# CI Tools（ProKit）完整用户手册

> 适用：Archicad 24 及以上版本（团队通用，各机器安装情况不同，请先看第 1 章自查）
> 编制日期：2026-11-05
> 依据：Graphisoft 官方 MyCi 知识库

---

## 第 0 章 先搞清楚一件事：CI Tools 到底是什么

"CI Tools" 这个名字有 **两个完全不同的含义**，很多人在这里绕弯路。

| 你搜到的 | 真实身份 | 面向谁 |
|---|---|---|
| **CI Tools 插件包**（本文重点） | Central Innovation（新西兰）开发的 16 个 Archicad 加装插件，出图/建模效率工具 | 建筑师、设计师 |
| **Archicad CI（Command Interface）** | Archicad 的 JSON 命令接口 + Python 绑定，写脚本自动化的 | 开发者 |

**本文讲第一个**（插件包）。因为：
- 菜单栏里那个 "CI Tools" 下拉菜单就是它；
- 菜单栏里那个 "CI Tools" 下拉菜单就是它。

**重要变化（2026 起）**：Graphisoft 已把 CI Tools 收进自有产品线，改名 **Archicad ProKit**，分两个包：

- **ProKit Core**：Annotate（文字格式）、Transformer（镜像）、Time Tracker（计时）、Detail Elements（二维详图）
- **ProKit Suite**：Cabinets、Coverings、Doors+Windows、Electrical、Fitout、Keynotes、MetaData、Quantities、Site、Stairs、Structure

你现在用 AC28/29，安装包里仍是 "CI Tools" 名字；AC30 用 "ProKit" 名字。**同一套东西，改了个名**。所以网上搜 "CI Tools" 老教程和搜 "ProKit" 新文档，内容是对得上的。

下载地址（官方）：
- ProKit Core：`https://www.graphisoft.com/downloads/add-ons/prokit/#Archicad-prokitcore`
- ProKit Suite：`https://www.graphisoft.com/downloads/add-ons/prokit/#Archicad-prokitsuite`
- 老版 CI Tools 仍可从 MyCi 知识库下载（`https://myci.centralinnovation.com`）

---

## 第 1 章 先自查：你装了哪些

不同机器、不同 Archicad 版本，CI Tools 的安装情况不一样。开始用之前，先花一分钟确认自己这台机器的状态。

### 查插件装没装

看 Archicad 安装目录下的 Add-Ons 文件夹：

| 平台 | 路径 |
|---|---|
| Windows | `C://Program Files\Graphisoft\Archicad XX\Add-Ons\CI Tools\` |
| macOS | `/Applications/Graphisoft/ARCHICAD XX/Add-Ons/CI Tools/` |

里面是 `CI Tools XXX.apx` 格式的插件文件，每个 `.apx` 对应一个工具。

### 查工作环境有没有

Archicad 菜单 **文件 → 工作环境**，列表里找 **Ci Tools Profile** 开头的条目。有这一项说明工作环境文件已就位。

### 三种常见状态

| 状态 | 判断依据 | 怎么办 |
|---|---|---|
| **全新安装** | Add-Ons 里没有 CI Tools 文件夹 | 装 CI Tools 或 ProKit 安装包 |
| **插件在但没加载** | 有 `.apx` 文件，但菜单栏和工具箱看不到入口 | 走第 2 章三步启动，八成是缺工作环境或图库包 |
| **一切就绪** | 菜单栏有 CI Tools 菜单，工具箱有对应工具 | 直接用，遇到问题查第 5 章故障排查 |

### 版本差异提示

- **Archicad 24 及以上**支持 CI Tools
- **Archicad 29 起**，库包（libpack）不再自动挂载，**必须手动加载**，这是"装了却用不了"的头号原因
- **Archicad 30** 起工具包改名为 **ProKit**，安装包从 Graphisoft 官网下载，不再走 MyCi
- 各版本包含的工具数量不同，缺失的工具需单独补装

### 区域限制

- **Electrical**：库含欧盟、印度、撒哈拉以南非洲、英国、美国，**无中国国标库**，国内项目需自建符号
- **Sites**：澳新专属
- **Bracing**：新西兰专属

---

## 第 2 章 三步启动（5 分钟）

### 第 1 步：加载 CI Tools 工作环境

Archicad 启动后：
1. 菜单 **文件 → 工作环境**
2. 列表里找 **"Ci Tools Profile 28"**（中文版可能显示为 `Ci Tools Profile 28`）
3. 选中 → **设置/应用**

> 如果列表里找不到：点 **浏览**，路径
> Windows: `%APPDATA%\Graphisoft\Archicad XX.0.0 CHI R1\工作环境\配置文件\Ci Tools Profile XX.xml`  
> macOS: `~/Library/Preferences/Graphisoft/Archicad XX.0.0 CHI R1/工作环境/配置文件/Ci Tools Profile XX.xml`

加载后，左侧工具箱（Toolbox）会出现 CI Tools 的专属工具条。

### 第 2 步：把插件工具加进工具箱（如果没显示）

有些插件装上了但工具箱里没有图标：

1. 在左侧工具箱**空白处右键**
2. 选 **工具箱设置 / Toolbox Settings**
3. 找到对应的插件名（如 "ProKit Detail Elements"、"ProKit Electrical"）
4. 勾选 → 确认

> 官方特别提醒：**加完记得保存工作环境**，否则下次开 Archicad 又没了。

### 第 3 步：加载图库包（关键！AC29 起变成必做）

**这是 90% "装了却用不了" 的原因。**

从 Archicad 29 开始，CI Tools 的库包**不再自动挂载**，必须手动加载进项目。

操作：
1. 菜单 **文件 → 库管理器（Library Manager）**
2. 点 **"添加 / Add"**
3. 定位到：
   ```
   C://Program Files\Graphisoft\Archicad XX\Archicad 图库包\Ci Tools Library Packages\
   ```
4. **选中具体的 .libpack 文件**（如 `Ci Tools Detail Elements.libpack`）
   - ⚠️ **不要选文件夹层级**——选文件夹只会挂载一层，导致内容找不到。这是官方明确警告的坑
5. 加载后关联的宏（Macros）也会一并进来

> **哪些插件需要手动加载 libpack？**（官方 Start-here 文档明确点名）
> - Detail Elements（详图元素）
> - Electrical（电气）
> - Keynotes（注释键）
>
> 其余插件在 AC28 里通常靠工作环境自动挂载；AC29/30 建议全部手动加载一遍最保险。
>
> **Macros 主包很关键**：`Ci Tools Macros.libpack` 承载各工具的自动化宏，很多功能依赖它。优先加载它。

---

## 第 3 章 16 个工具逐个拆解

> 菜单路径统一为 **CI Tools → XXX**（AC30 上是 **ProKit → XXX**）

### 3.1 Annotate — 文字大小写批量转换

**用途**：全项目文字格式统一。这是出图前最省时间的一个工具——CAD 里从别处粘来的文字大小写乱成一片，手改能改到下班。

**入口**：**CI Tools → Annotate → Convert Case…**

**操作步骤**：
1. 打开 **Case Conversion Options** 对话框
2. **Case（格式）** 区：
   - `Sentence case` — 句首大写
   - `UPPER CASE` — 全大写
   - `lower case` — 全小写
   - `Title Case` — 标题式大写
   - 勾 **Observe case exceptions**（观察例外）→ 出现 **编辑** 按钮，可把某些词/缩写锁定为固定格式（如 "iPhone"、"m²"、"BIM"）
3. **Scope（范围）** 区 —— 这栏决定改多少，是防手滑的关键：

   | 选项 | 作用范围 |
   |---|---|
   | Selected items only | 只改当前选中项（没选中时该项变灰不可用） |
   | Text in the current drawing | 只改当前视图；平面图激活时=当前楼层 |
   | Text in floor plan (all storeys) | 平面图全部楼层 |
   | Text in all drawings | 全部图纸，含剖面、详图、图表 |

   - 勾 **String properties** → 同时转换字符串型属性值
     - ⚠️ 不影响下拉预设菜单里选出来的值，那种要用属性管理器改
   - 勾 **String parameters** → 同时转换参数文字
     - 锁定或隐藏的参数**不会**被改
     - 选 "If displayed"（若为显示值）时，只转换与 2D 显示完全一致的参数值 —— **更安全，推荐**
4. **Ignore（忽略）** 区：勾选要跳过的项
   - Hidden items（隐藏图层上的全部）
   - Locked items（被锁定的构件）
   - Locked layers（锁定的图层）
5. 点 **OK** 执行

**进阶用法**：
- **替换字体**：CI Tools → Annotate → Replace Fonts
- **批量替换属性值**：CI Tools → Annotate → Attribute Replacement
- **合并文本框**：把多个独立文本框合并成一个可编辑文本框（CAD 里手改最烦的场景）

> **实战建议**：跑 Annotate 前先 `Ctrl+Z` 备份，或用"只改选中项"试手。勾 "If displayed" 是最保险的选项。

---

### 3.2 Transformer — 一键镜像整个项目

**用途**：整个项目（含模型、标记、标签、2D 文字）沿轴线镜像。适合对称建筑、重复户型、批量复制改朝向。

**为什么需要它**：手动旋转 3D 模型后，剖面、立面、标注、房间标签全得跟着改，极易漏。

**入口**：**CI Tools → Transformer → Mirror Project…**

**操作步骤**：
1. 点击**镜像轴线的起点**
2. 屏幕上出现镜像预览线，随鼠标在**水平 / 垂直**之间自动切换
   - ⚠️ **目前只支持水平或垂直轴**，其他角度不支持
3. 轴线方向满意 → **单击确认**
4. 想取消 → **按 ESC**

**配套文章**：`1.3 Mirroring Notes` 讲注释、标记的镜像细节。

> **注意**：这是"破坏性"操作，镜像后元素 ID 会变、原位置对象被替换。建议先另存一份再试。

---

### 3.3 Time Tracker — 项目工时记录

**用途**：记录你在各任务上花的时间，和报价/预期工时对比。**接活报价场景直接相关**——你手上澳洲项目、滨海项目都能用。

**入口**：**CI Tools → Time Tracker → Open Time Tracker**

**操作步骤**：
1. 点 **文件夹图标**，选择存档位置（时间数据存在你指定的文件里）
2. 指定 **Job（项目）** 和 **Task（任务）**
3. **启动计时**

就这三步。数据存在你自己选的文件中，可导出做对比分析。

---

### 3.4 Detail Elements — 智能二维详图构件库

**用途**：拖拽式的参数化 2D 详图对象库，大幅加速详图绘制（平面/剖面/立面/详图视图都能用）。

**10 个分类**：
```
General Objects        通用构件
Floor Objects          地面构件
Wall Objects           墙体构件
Roof Objects           屋面构件
Ceiling Objects        顶棚构件
Door and Window Objects 门窗构件
Interior Trim Objects  室内收边构件
Fastening Objects      连接件
Reinforcing Objects    加固件
2D Symbols             二维符号
```

**前置条件（必做）**：手动加载 `Ci Tools Detail Elements.libpack`（见 2.3 节）

**操作**：
1. 在工具箱选中 **ProKit Detail Elements** 工具
2. 在设置面板里挑构件 → 在图纸上放置
3. 对象是参数化的，双击可参数化编辑

**工具箱没有这个工具？** → 右键工具箱 → 工具箱设置 → 勾选 → **保存工作环境**

---

### 3.5 Keynotes — 规范注释自动化

**用途**：建立注释数据库，按构件属性**自动**挂注释到构件上，避免手工逐个标注的枯燥和错误。

**入口**：**ProKit/CI Tools → Keynotes → Keynotes Palette**

**前置**：手动加载 `Ci Tools Keynotes.libpack`

**操作**：
1. 打开 **Keynotes Palette**
2. 点 **A+** 添加 Keynote、编辑内容
3. **放置** Keynote：用 Archicad 的**标签工具（Label Tool）**，但要选 **ProKit Label**
4. **双击** Palette 里的注释 → 在图纸上定位放置
5. 也能把 Keynote 关联到 Archicad 的**属性（Attributes）**，自动标注

**两种用法**：
- 直接在图纸上放**完整注释**
- 只放**参考键（reference key）**，然后由 Keynotes 自动**汇总成注释明细表**

**进阶**：
- 属性关联 Keynote：`Working with Attribute linked Keynotes`
- 主控明细表同步：`Using Master Schedules to define and sync Keynote Schedule Settings`
- 多页 Keynotes 明细表：`Creating Multiple Page Keynote Schedules`
- **从其他项目导入已有数据库**（关键——公司内部复用注释库）

> 数据文件在 `C:\Program Files\Graphisoft\Archicad 29\CI Tools Extras\`：
> `CI Tools Keynotes.csv`、`CI Tools Keynotes.keynotes`
> 也可 `Import a Sample Database` 先拿样例试手。

---

### 3.6 Metadata — 属性与分类的批量操作面板

**用途**：在一个面板里直接改构件的属性和分类，不用在各种对话框里来回跳。**做 BIM 数据管理的主力工具**。

**入口**：**CI Tools → MetaData**（打开 MetaData 面板）

**核心能力**：
| 功能 | 说明 |
|---|---|
| 属性视图 | 在模型视图里直接看/改属性，不用开属性管理器 |
| **批量改属性** | 一次改多个选中构件的属性 |
| **筛选与选择** | 按条件过滤出目标构件（改属性前先精准定位） |
| **属性传递** | 在构件之间复制/传递属性 |
| **Traits 管理** | 给构件添加/移除/迁移自定义标记 |

**实战路径**：
1. **筛选定位** → 用属性/分类条件筛出目标构件
2. **批量编辑** → 在面板里统一赋值
3. **审计检查** → 查哪些构件漏设了

---

### 3.7 Quantities — 工程量清单与算量

**用途**：从实时模型出工程量清单，分配单价与数量，可导出 CSV 喂给其他造价软件。

**入口**：**CI Tools → Quantities**

**工作流（官方 9 章结构）**：

```
1. Overview          总览与术语
2. Project Data      构件数据管理（数量 Traits）
3. Bill of Quantities 工程量清单结构（Bill Structure）
4. Defining Measurements 测量配方（Recipe）
5. Generating Quantities  生成工程量
6. Auditing          审计核查
7. Element Calculation Expressions  构件计算表达式
8. Calculation Functions  计算函数
9. Calculation Operators 计算运算符
```

**核心概念**：
- **Recipe（配方）** —— 用规则自动给构件分配数量/成本。避免手工一个个填
- **Bill Structure（清单结构）** —— 分级目录（分类 → 条目），可嵌套
- **Traits** —— 挂在构件上的数量/成本标记

**关键操作**：
- 创建 Recipe：`4.2.1 How to create a recipe`
- 排清单：`5.2.1 How to schedule the bill of quantities`
- 限定计算范围（只算选中的构件）：`5.2.2`
- 按条目/分类过滤：`5.2.3`、`5.2.4`
- **审计**（强烈推荐，交付前必做）：
  - 审计构件数据 `6.2`
  - 审计 Recipe 完成度 `6.3`
  - **审计漏算构件** `6.4`
  - 审计工程量清单 `6.5`
- 导出：`CI Tools → Quantities → Export` → CSV

> **实战建议**：Quantities 是最容易"看着对其实错"的工具。交付前至少跑一遍 6.4 漏算审计 + 6.5 清单审计。

---

### 3.8 Cabinets — 高度可配置的橱柜对象

**用途**：**一个**高度可配置的对象搞定所有橱柜类型，不用为每种柜体单独建对象。

**能力**：
- 平面和曲面柜门、抽屉面板库
- 可编辑面板样式、把手类型
- 自定义门、顶板、酒架、隔板、分隔件
- 橱柜隔板支持**三维直接编辑**

**入口**：工具箱中的 ProKit Cabinets 工具 + `Ci Tools Cabinets.lcf` 图库

> 室内、装配式、异形柜体场景价值最大。

---

### 3.9 Doors+Windows — 门窗样式扩展

**用途**：突破 Archicad 原生门窗样式限制，多面板、多开启方式、多收边/窗台组合。

**能力**：
- 多种面板、开启方式、装饰线、窗台组合
- **门窗尺寸捕捉**（Snap）—— 画图时直接吸尺寸
- 自定义门窗样式可**在项目之间共享**（团队标准化）

**入口**：工具箱 ProKit Doors+Windows 工具 + `Ci Tools Doors+Windows.lcf`

> 官方新文档：`ProKit Doors and Windows - Start here`

---

### 3.10 Coverings — 3D 覆面层

**用途**：给墙、板、柱、屋顶贴 3D 建模的"皮"，2D/3D 视图都能显示，模型立刻有真实感。

**关键机制**：
- 覆面**保持正确比例**，**自动链接到主体构件**，主体改了覆面跟着更新（参数化关系，不易不一致）
- 预置覆面样式 + 支持自定义样式
- 屋顶覆面可**自动生成排水管**

**入口**：工具箱 ProKit Coverings 工具 + `Ci Tools Coverings.lcf`

> 出效果图和汇报模型时性价比很高——比单纯改材质真实得多。

---

### 3.11 Electrical — 智能电气符号与回路

**用途**：智能放置电气符号，自动创建回路、明细表。

**库覆盖区域**：欧盟 / 印度 / 撒哈拉以南非洲 / 英国 / 美国（**没有中国国标库**——国内项目需自建符号）

**前置**：手动加载 `Ci Tools Electrical.libpack`（官方明确要求）

**操作**：
1. 工具箱选中 ProKit Electrical 工具
2. 设置里挑符号（插座、开关、插孔、其他面板）
   - 设置**标高（Elevation）** → 符号自动旋转并贴靠墙体
   - 符号既可显示为整个面板，也可拆成面板内的单个组件
3. **自动布电线**：选中 Archicad 构件或电气构件 → 工具可自动加走线
4. 设 Wire Style（走线样式）→ 自动生成关联走线
5. 建回路：`Creating Circuits`
6. 明细表模板在 `C:\Program Files\Graphisoft\Archicad 29\CI Tools Extras\`：
   - `Electrical Legend 29.xml`（图例）
   - `Electrical Schedule 29.xml`（明细表）

---

### 3.12 Stairs — 灵活楼梯设计

**用途**：直接在模型上自由设计楼梯。

**能力**：
- 各类独立构件，住宅商业都能配
- **栏杆可关联楼梯、板，甚至独立放置**，能在不同宽度和高度处转折、接平台
- 楼梯组合可**当作单一对象**编辑、标注、出图

**入口**：工具箱 ProKit Stairs 工具 + `Ci Tools Stairs.lcf`

> 注：另有 "CI Polystair" 变体，用单个组件做高度定制楼梯。

---

### 3.13 Structural — 结构构件库

**用途**：创建 3D 结构构件——桁架、框架、连接件。

**入口**：工具箱 ProKit Structural 工具 + `Ci Tools Structural.lcf`
**官方文档**：`ProKit Structural – Start here`

---

### 3.14 Sites — 场地与景观（仅澳新 / ANZ）

**用途**：可视评估模型与边界、退让高度的关系关系（**澳洲项目直接相关**）。

**能力**：
- 边界（boundaries）与**高度退让平面（height recession planes）**
- 大型剪影式植物对象库（billboard style）
- 面积图章（area stamps）
- 边界绘制辅助工具
- 建筑包络（building envelope）工具
- **早期方案阶段**评价场地关系最有用

**入口**：工具箱 ProKit Sites 工具 + `Ci Tools Sites.lcf`
> 官方标注 "Sites (NZ Only)"，但澳新区（ANZ）订阅可用。

---

### 3.15 Fitout — 一键布置房间

**用途**：把空房间一键变成配齐家具的房间。**酒店客房、公寓户型快速布置神器**。

**前置**：
- 加载 **Ci Tools Profile 28/29** 工作环境（工具箱里才有 Fitout 工具）
- `Ci Tools Fitout.lcf` 图库 + `Ci Tools Fitout.libpack`

**操作**：
1. 编译 **Sets（套组）** 和 **Fitouts（布置）**
   - 样例存在 CI Tools Library → Fitout 文件夹
2. 在 **Fitout 工具**里选一个 Example Fitout（如 Bathroom 布置，含浴缸、淋浴、马桶、洗手盆）
3. **在 Zone（房间）里点击**放置
   - ⚠️ **工具对光标位置敏感**——会优先把重点构件放在离点击点最近处
   - **可能要试放几次**才能满意
   - 若 Zone 里没有窗扇净空（Window Clearance），工具会自动补一个
4. 放置后是**成组**的 → `Alt+G` / `Cmd+G` 切换挂起分组，可单独移动某个物件
   - 移动洗手盆时会**自动吸附到靠着的墙**

**延伸**：`Fitout - Window Treatments and Door Circulation`（窗饰与门扇通行）

---

### 3.16 Bracing — NZ 木结构支撑（仅新西兰）

**用途**：新西兰木结构住宅的抗侧力构件计算与布置（符合 NZS 规范）。

**入口**：`Ci Tools Bracing.lcf` + `CI Tools Bracing.apx`
> 仅 NZ 订阅可用。国内和澳洲项目用不上。

---

### 3.17 Ci Tools Update — 自动更新

**作用**：检查并下载 CI Tools 的更新。装完新版本 Archicad 后，用它拉最新插件。

---

### 3.18 Launchpad — 新功能试验场（AC29+）

**作用**：Central Innovation 的新功能原型区，可试用概念验证功能并反馈。
> 在 AC28 里没有独立插件（功能在别的插件里），AC29 起拆为独立 `Ci Tools Launchpad.apx` + libpack。所有订阅包都免费包含。

---

### 3.19 Masterspec MasterKey — 规范联动（附加）

`Masterspec MasterKey.apx` —— 与 Masterspec 规范库联动，国内项目用不上，可忽略。

---

## 第 4 章 场景化速查：按任务找工具

| 你要做的事 | 用这个工具 | 入口 |
|---|---|---|
| 全项目文字大小写统一 | **Annotate** | CI Tools → Annotate → Convert Case… |
| 换字体 / 批量改属性文字 | **Annotate** | CI Tools → Annotate → Replace Fonts / Attribute Replacement |
| 项目对称镜像 | **Transformer** | CI Tools → Transformer → Mirror Project… |
| 记录工时对报价 | **Time Tracker** | CI Tools → Time Tracker → Open Time Tracker |
| 快速出详图 | **Detail Elements** | 工具箱 → ProKit Detail Elements |
| 规范注释自动化 | **Keynotes** | CI Tools → Keynotes → Keynotes Palette |
| 批量改属性/分类 | **MetaData** | CI Tools → MetaData |
| 算量出清单 | **Quantities** | CI Tools → Quantities |
| 定制橱柜/木作 | **Cabinets** | 工具箱 → ProKit Cabinets |
| 异形门窗 | **Doors+Windows** | 工具箱 → ProKit Doors+Windows |
| 模型贴皮提真实感 | **Coverings** | 工具箱 → ProKit Coverings |
| 电气点位与回路 | **Electrical** | 工具箱 → ProKit Electrical |
| 自由设计楼梯 | **Stairs** | 工具箱 → ProKit Stairs |
| 结构构件/桁架/框架 | **Structural** | 工具箱 → ProKit Structural |
| 场地边界与退让（澳洲） | **Sites** | 工具箱 → ProKit Sites |
| 房间一键配家具 | **Fitout** | 工具箱 → ProKit Fitout |

---

## 第 5 章 故障排查

| 症状 | 原因 | 解决 |
|---|---|---|
| 菜单里没有 "CI Tools" | 工作环境没加载 | 文件 → 工作环境 → 选 Ci Tools Profile 28 → 应用 |
| 工具箱里没有某个工具 | 插件已装但工具箱没加 | 右键工具箱 → 工具箱设置 → 勾选 → **保存工作环境** |
| 工具能开但没内容 | **libpack 没加载** | 文件 → 库管理器 → Add → 选**具体 .libpack 文件**（不要选文件夹） |
| AC29/30 上内容为空 | AC29 起必须手动加载库包 | 同上 |
| 安装器里看不到 Archicad 版本 | 安装器检测不到 | 关闭 Archicad；点安装器右上角 **Find** 手动指到安装目录；确认 Archicad 和安装器是**同一个系统用户**装的；macOS 别手动拷 Applications |
| 图库加载了但对象不出现 | 选了文件夹层级 | 回到库管理器，选单个 .libpack 文件重新加载 |
| 插件菜单全变英文/找不到某菜单 | 版本不一致 | AC28 用 "CI Tools"，AC30 用 "ProKit"；老版 CI Tools 从 MyCi 下载 |
| Detail Elements 拖不出对象 | Macros 没加载 | 优先加载 `Ci Tools Macros.libpack` |
| Annotate 改错了想回退 | 不可逆风险 | 执行前 Ctrl+Z 备份；优先用 "Selected items only" 试手 |
| Transformer 镜像后元素丢失 | 破坏性操作 | 提前另存副本 |

---

## 第 6 章 上手建议（按优先级）

**别一次学 16 个。** 按你这个阶段（澳洲项目 + 旧建筑改造 + BIM 出图）：

**第一优先（立刻见效）**
1. **Annotate** — 出图前文字统一，10 分钟上手，省几小时
2. **MetaData** — 属性批量管理，做 BIM 交付必用
3. **Time Tracker** — 你接项目要算工时和报价，直接对钱

**第二优先（项目需要时再学）**
4. **Quantities** — 出算量清单
5. **Keynotes** — 规范注释系统（要配数据库，前期投入大）
6. **Transformer** — 偶尔镜像时用

**第三优先（特定场景）**
7. **Coverings**（汇报模型提质感）、**Fitout**（客房批量布置）、**Sites**（澳洲场地）、**Detail Elements**（详图库）

**不建议现在碰**：Cabinets、Doors+Windows、Electrical（无国标库）、Structural、Bracing（NZ 专用）

---

## 第 7 章 官方资源

| 资源 | 地址 |
|---|---|
| **MyCi 知识库（最全，有中文外全部图解）** | `https://cadimage.zendesk.com/hc/en-us` |
| ProKit 官方下载 | `https://www.graphisoft.com/en-gs/downloads/prokit` |
| ProKit Core 介绍 | Graphisoft Support → "Introducing Archicad ProKit" |
| 免费试用申请 | `https://myci.centralinnovation.com/freetrial` |
| Graphisoft Learn 视频课（ProKit Core） | `https://learn.graphisoft.com/visitor_catalog_class/show/131995` |
| 旧版 CI Tools 安装器 | MyCi 知识库 → "Get CI Tools"（需 MyCi 账号，非 Graphisoft ID） |
| CI Tools 官方社区 | `https://centralinnovation.com/software/ci-tools` |
| 开发者社区（JSON/Python 方向） | `https://community.graphisoft.com/t5/Developer-Hub/ct-p/developer` |

**免费视频课程**：Graphisoft Learn 上的 "Getting Started with ProKit Core"，覆盖 Annotate / Detail Elements / Time Tracker / Transformer 四个工具，1 小时，英文，有字幕。**这是最快的入门路径。**

---

## 附录 A：安装与补装

### 首次安装 CI Tools（Archicad 24 ~ 29）

1. 前往 MyCi 知识库下载 CI Tools Installer → https://cadimage.zendesk.com/hc/en-us
2. 关闭 Archicad，运行安装器，用 **MyCi 账号**登录（注意：不是 Graphisoft ID）
3. 选择 **Install Ci Tools**，指定目标 Archicad 版本
4. 列表里勾选需要的工具 → Install
5. 重启 Archicad，**加载工作环境 + 加载图库包**

> 若安装器里看不到你的 Archicad 版本：关闭 Archicad，点安装器右上角 **Find** 手动指到安装目录；确认 Archicad 和安装器是同一个系统用户装的。

### 安装 ProKit（Archicad 30）

2026 起 CI Tools 更名为 ProKit，改为 Graphisoft 官方产品，**无需 MyCi 账号**：

- ProKit Core（Annotate、Transformer、Time Tracker、Detail Elements）→ https://www.graphisoft.com/downloads/add-ons/prokit/#Archicad-prokitcore
- ProKit Suite（Cabinets、Coverings、Doors+Windows、Electrical、Fitout、Keynotes、MetaData、Quantities、Site、Stairs、Structure）→ https://www.graphisoft.com/downloads/add-ons/prokit/#Archicad-prokitsuite

### 补装缺失的单个工具

- **Archicad 24~29**：在 CI Tools Installer 里勾选该工具单独安装，装完重新加载工作环境与图库包
- **Archicad 30**：ProKit Core 与 Suite 是两个独立安装包，缺哪个装哪个

### 版本与功能对照

| 版本 | 工具包名称 | 获取方式 | 注意 |
|---|---|---|---|
| 24 ~ 29 | CI Tools | MyCi Installer | 库包需手动加载 |
| 30 及以后 | ProKit Core / Suite | Graphisoft 官网 | 菜单名改为 ProKit |

---

## 附录 B：libpack 全量加载清单（AC28 路径）

```
C:\Program Files\Graphisoft\Archicad XX\Archicad 图库包\Ci Tools Library Packages\
```
建议按此顺序加载（Macros 优先，它承载其他工具的宏）：
```
1. Ci Tools Macros.libpack          ← 先加载这个
2. Ci Tools Detail Elements.libpack
3. Ci Tools Electrical.libpack
4. Ci Tools Keynotes.libpack
5. Ci Tools Cabinets.libpack
6. Ci Tools Coverings.libpack
7. Ci Tools Doors+Windows.libpack
8. Ci Tools Fitout.libpack
9. Ci Tools Stairs.libpack
10. Ci Tools Structural.libpack
11. Ci Tools Sites.libpack
12. Ci Tools Bracing.libpack
13. Ci Tools Time Tracker.libpack
```

---

*本手册基于官方 MyCi 知识库（2026-10 更新）编写，界面截图取自官方教程文档，适用于 Archicad 24 及以上版本。各机器安装情况不同，请先按第 1 章自查。*
