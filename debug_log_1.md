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
