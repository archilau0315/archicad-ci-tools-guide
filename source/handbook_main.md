# CI Tools 中文主线 · 16 个工具操作要点

> 本文是**主线速查** —— 每个工具"干什么、入口在哪、关键步骤、坑在哪"。
> 完整细节看右侧分册（含官方原文与全部截图）。
> 适用 Archicad 24 及以上版本。

---

## 通用前提

### 这套工具是什么

Central Innovation（新西兰）为 Archicad 开发的效率插件包，2026 年起被 Graphisoft 收进自有产品线并改名 **ProKit**。同一套东西两个名字，搜老教程用 CI Tools，搜新文档用 ProKit。

| | ProKit Core | ProKit Suite |
|---|---|---|
| 包含 | Annotate、Transformer、Time Tracker、Detail Elements | Cabinets、Coverings、Doors+Windows、Electrical、Fitout、Keynotes、MetaData、Quantities、Site、Stairs、Structure |
| 解决什么 | 出图提速、改图安全、计工时 | 建模提速、数据管理、算量出图 |

### 三步启动（每次新项目必做）

```
1. 文件 → 工作环境 → Ci Tools Profile XX → 应用
2. 文件 → 库管理器 → Add → Ci Tools Macros.libpack（先加这个）
   ★ 必须选单个 .libpack 文件，选文件夹内容会全空
3. 右键工具箱 → 工具箱设置 → 勾选工具 → ★保存工作环境
```

**第二步是"装了却用不了"的头号原因** —— 从 Archicad 29 起，CI Tools 的库包不再自动挂载，必须手动加载进项目。

### 先自查

不同机器安装情况不同，用之前先确认：

| 查什么 | 怎么看 |
|---|---|
| 插件装没装 | `C:\Program Files\Graphisoft\Archicad XX\Add-Ons\CI Tools\` 下有 `CI Tools XXX.apx` |
| 工作环境在不在 | 文件 → 工作环境，列表有 `Ci Tools Profile` |
| 库包装没装 | 库管理器里能选到 `Ci Tools Macros.libpack` |

---

## 一、Annotate · 文字格式

**干什么**：全项目文字大小写、字体批量统一。CAD 里从别处粘来的文字格式乱成一片，手改能改到下班 —— 出图前最省时间的工具。

**入口**：CI Tools → Annotate → Convert Case…

**关键步骤**：

1. 打开 **Case Conversion Options** 对话框
2. **Case** 栏选目标格式：`Sentence case` / `UPPER CASE` / `lower case` / `Title Case`
   - 勾 `Observe case exceptions` → 出现「编辑」按钮，可把 iPhone、BIM、m² 锁定不变
3. **Scope** 栏决定改多少（**防手滑的关键**）：
   - `Selected items only` — 只改选中项（没选中时变灰）
   - `Text in the current drawing` — 当前视图；平面图激活时=当前楼层
   - `Text in floor plan (all storeys)` — 平面图全部楼层
   - `Text in all drawings` — 全部图纸，含剖面、详图
   - 勾 `String properties` 同时转字符串属性值
   - 勾 `String parameters` 同时转参数文字，选 `If displayed` **最安全**
4. **Ignore** 栏勾选跳过的：隐藏图层、锁定构件、锁定图层、可能引起关联标签变化的内容
5. 点 OK

**其他功能**：
- 替换字体 — CI Tools → Annotate → Replace Fonts
- 批量替换属性值 — CI Tools → Annotate → Attribute Replacement
- 合并文本框 — 把多个独立文本框合并成一个可编辑文本框

> **坑**：批量改错撤不回来。执行前先 Ctrl+Z 备份，或先用「Selected items only」试手。

---

## 二、Transformer · 项目镜像

**干什么**：整个项目（含模型、标记、标签、2D 文字）沿轴线镜像。适合对称建筑、重复户型、批量复制改朝向。

手动旋转 3D 模型后，剖面、立面、标注、房间标签全得跟着改，极易漏 —— 这就是它的价值。

**入口**：CI Tools → Transformer → Mirror Project…

**关键步骤**：

1. 点击镜像轴线的起点
2. 预览线随鼠标在**水平 / 垂直**之间自动切换（目前只支持这两种角度）
3. 方向满意 → 单击确认；取消 → 按 ESC

> **坑**：破坏性操作，镜像后元素 ID 会变、原位置对象被替换。先另存副本。

---

## 三、Time Tracker · 工时统计

**干什么**：记录各任务工时，和报价、预期工时对比。**接活报价场景直接相关。**

**入口**：CI Tools → Time Tracker → Open Time Tracker

**关键步骤**（就三步）：

1. 点文件夹图标，选择存档位置（时间数据存在你指定的文件里）
2. 指定 **Job（项目）** 和 **Task（任务）**
3. 启动计时

---

## 四、Detail Elements · 二维详图

**干什么**：拖拽式参数化 2D 详图对象库，大幅加速详图绘制。

**10 个分类**：General / Floor / Wall / Roof / Ceiling / Door and Window / Interior Trim / Fastening / Reinforcing / 2D Symbols

**前置**：手动加载 `Ci Tools Detail Elements.libpack`

**关键步骤**：工具箱选中 ProKit Detail Elements → 设置面板挑构件 → 图纸上放置。对象是参数化的，双击可编辑。

**工具箱没有这个工具**：右键工具箱 → 工具箱设置 → 勾选 → **保存工作环境**

---

## 五、Keynotes · 规范注释

**干什么**：建立注释数据库，按构件属性**自动**挂注释，避免手工逐个标注的枯燥和错误。

**入口**：CI Tools → Keynotes → Keynotes Palette

**前置**：手动加载 `Ci Tools Keynotes.libpack`

**关键步骤**：

1. 打开 Keynotes Palette，点 **A+** 添加 Keynote、编辑内容
2. **放置** Keynote：用 Archicad 标签工具，但要选 **ProKit Label**
3. **双击** Palette 里的注释 → 在图纸上定位放置
4. 也可把 Keynote 关联到 Archicad 属性，自动标注

**两种用法**：直接放完整注释；或只放参考键，由 Keynotes 自动汇总成明细表。

---

## 六、MetaData · 属性管理

**干什么**：在一个面板里改属性和分类，不用在各种对话框里跳。**BIM 数据管理的主力工具。**

**入口**：CI Tools → MetaData

**核心能力**：

| 能力 | 说明 |
|---|---|
| 属性视图 | 在模型视图里直接看改属性 |
| 批量改属性 | 一次改多个选中构件 |
| 筛选与选择 | 按条件过滤出目标构件 |
| 属性传递 | 在构件之间复制、传递属性 |
| Traits 管理 | 添加、移除、迁移自定义标记 |

**实战路径**：筛选定位 → 批量编辑 → 审计检查。

---

## 七、Quantities · 工程量算量

**干什么**：从实时模型出工程量清单，分配单价与数量，可导出 CSV 喂给其他造价软件。

**入口**：CI Tools → Quantities

**三个核心概念**：

- **Recipe（配方）** — 用规则自动给构件分配数量成本，避免手工一个个填
- **Bill Structure（清单结构）** — 分级目录（分类 → 条目），可嵌套
- **Traits** — 挂在构件上的数量成本标记

**九个模块**：概览 → 构件数据 → 清单结构 → 测量配方 → 生成工程量 → 审计 → 构件计算表达式 → 计算函数 → 计算运算符

**审计是交付前必做**：

| 审计项 | 查什么 |
|---|---|
| 6.2 审计构件数据 | 数据填全没有 |
| 6.3 审计 Recipe 完成度 | 配方有没有漏 |
| **6.4 审计漏算构件** | 哪些构件根本没进清单 |
| 6.5 审计工程量清单 | 清单本身对不对 |

> Quantities 是最容易「看着对其实错」的工具。交付前至少跑 6.4 和 6.5。

---

## 八、Cabinets · 橱柜木作

**干什么**：**一个**高度可配置的对象搞定所有橱柜类型，不用为每种柜体单独建对象。

**能力**：平面和曲面柜门、抽屉面板库；可编辑面板样式与把手类型；自定义门、顶板、酒架、隔板、分隔件；隔板支持三维直接编辑。

---

## 九、Doors+Windows · 门窗

**干什么**：突破原生门窗样式限制，多面板、多开启方式、多收边/窗台组合。

**能力**：面板与开启方式组合；**门窗尺寸捕捉**；自定义样式可**跨项目共享**（团队标准化关键）。

---

## 十、Coverings · 覆面层

**干什么**：给墙、板、柱、屋顶贴 3D 建模的"皮"，2D/3D 视图都显示，模型立刻有真实感。

**关键机制**：

- 覆面**保持正确比例**，**自动链接主体构件**，主体改了覆面跟着更新
- 预置覆面样式 + 支持自定义
- 屋顶覆面可**自动生成排水管**

> 出效果图和汇报模型时性价比很高 —— 比单纯改材质真实得多。

---

## 十一、Electrical · 电气

**干什么**：智能放置电气符号，自动创建回路、明细表。

**库覆盖**：欧盟、印度、撒哈拉以南非洲、英国、美国。**没有中国国标库**，国内项目需自建符号。

**前置**：手动加载 `Ci Tools Electrical.libpack`

**关键步骤**：

1. 工具箱选中 ProKit Electrical → 设置里挑符号（插座、开关、插孔、其他面板）
   - 设**标高 Elevation** → 符号自动旋转并贴靠墙体
   - 符号可显示为整个面板，或拆成面板内的单个组件
2. **自动布电线**：选中构件 → 工具自动加走线
3. 设 Wire Style 走线样式 → 生成关联走线
4. 建回路、明细表

---

## 十二、Stairs · 楼梯

**干什么**：直接在模型上自由设计楼梯。

**能力**：各类独立构件，住宅商业都能配；**栏杆可关联楼梯、板甚至独立放置**，能在不同宽度和高度处转折接平台；楼梯组合可当作单一对象编辑、标注、出图。

---

## 十三、Structural · 结构构件

**干什么**：创建 3D 结构构件 —— 桁架、框架、连接件。

---

## 十四、Sites · 场地景观

**干什么**：可视评估模型与边界、退让高度的关系。**澳洲项目直接相关。**

**能力**：边界与高度退让平面；大型剪影式植物对象库；面积图章；边界绘制辅助；建筑包络工具。**早期方案阶段**评价场地关系最有用。

> 澳新专属。

---

## 十五、Fitout · 室内布置

**干什么**：把空房间一键变成配齐家具的房间。**酒店客房、公寓户型快速布置神器。**

**前置**：加载 Ci Tools Profile 工作环境 + `Ci Tools Fitout.lcf` 图库

**关键步骤**：

1. 编译 Sets（套组）和 Fitouts（布置），样例在 CI Tools Library → Fitout 文件夹
2. 在 Fitout 工具里选一个 Example Fitout（如 Bathroom 含浴缸、淋浴、马桶、洗手盆）
3. **在 Zone 里点击**放置
   - 工具对光标位置敏感，会优先把重点构件放在离点击点最近处
   - **可能要试放几次**才满意
   - 若 Zone 里没有窗扇净空，工具会自动补一个
4. 放置后是**成组**的 → `Alt+G` / `Cmd+G` 切换挂起分组，可单独移动，移动时自动吸附到靠着的墙

---

## 十六、Bracing · NZ 木结构支撑

**干什么**：新西兰木结构住宅的抗侧力构件计算与布置，符合 NZS 规范。

> 新西兰专属，国内和澳洲项目用不上。

---

## 学习路径建议

**别一次学 16 个。** 按你手上的活选：

**第一优先 · 立刻见效**

1. **Annotate** — 出图前文字统一，10 分钟上手，省几小时
2. **MetaData** — 属性批量管理，BIM 交付必用
3. **Time Tracker** — 算工时对报价，直接对钱

**第二优先 · 项目需要时**

4. **Quantities** — 出算量清单
5. **Keynotes** — 规范注释系统（配数据库前期投入大）
6. **Transformer** — 偶尔镜像时用

**第三优先 · 特定场景**

7. **Coverings**（汇报模型提质感）、**Fitout**（客房批量布置）、**Sites**（澳洲场地）、**Detail Elements**（详图库）

**暂不建议碰**：Cabinets、Doors+Windows、Electrical（无中国国标库）、Structural、Bracing（NZ 专用）

---

## 三个最常踩的坑

**① libpack 选成文件夹 → 内容全空**
库管理器里必须选**单个 `.libpack` 文件**，选文件夹层级只会挂载一层，工具打开是空的。官方明确警告。

**② 加了工具箱图标没保存工作环境**
下次开 Archicad 又没了，每次都要重加。勾选后务必点**保存工作环境**。

**③ Annotate 批量改错 → 撤不回来**
执行前先 Ctrl+Z 备份。优先用「Selected items only」试手，参数勾「If displayed」最保险。
