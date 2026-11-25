# ProKit / CI Tools 完全指南 · 一次让阅读体验升级的更新

> 一天，19 次提交，4 项核心优化。这不只是"改了几行代码"，而是一次让整份指南从"能看"变成"好读"的升级。

![ProKit / CI Tools 完全指南](https://www.kbitai.com.cn/resources/AC_Tutorial/ci_tools/article_images/index_home.jpg)

## 这份指南是什么

如果你用 ArchiCAD 配合 ProKit 或 CI Tools 做工程量算量、清单管理、属性映射，那么 ProKit / CI Tools 完全指南就是一份可以常驻浏览器书签的参考手册——18 个工具、424 篇文章、中英双语，覆盖从入门到精通的全部场景。

之前它有一个老毛病：**像一份长文档，不像一份指南。**

今天，我们把它修好了。

## 01 章节引用：从"看一眼"到"一键跳"

> "见 2.3.8"、"详见第 4 章"、"refer to sections 4 to 4.4"……这些引用以前就是一行字，你得自己滚动去找。

现在，**全部变成了可点击的链接**。

![正文里的"1.3 节"已是可点击链接](https://www.kbitai.com.cn/resources/AC_Tutorial/ci_tools/article_images/quantities_xref.jpg)

鼠标悬停有下划线提示，点击直接跳到对应章节。跨章节引用、范围引用（"4 至 4.4 节"）、英文复数（"sections 4.6 and 4.5"）——全部都识别并转化。

仅"工程量算量"这一篇，就新增了 **297 个可点击跳转**。

## 02 章节结构：从"一锅粥"到"分得清"

之前总览页里，工程量算量的 122 条目录全堆在一起，根本分不清"3.1 背景"属于第 3 章还是第 2 章的尾巴。

![目录被 9 个章分隔条清楚分组](https://www.kbitai.com.cn/resources/AC_Tutorial/ci_tools/article_images/index_toc.jpg)

现在，9 个章节分隔条把它切成了 9 组：

- **第 1 章 引言** → 1.1 / 1.2 / 1.3
- **第 2 章 项目数据管理** → 2.1 / 2.2 / 2.3 ……
- **第 3 章 工程量清单** → 3.1 / 3.2 / 3.3 ……
- **第 9 章 计算运算符** → 9.1 …… 9.6

正文里，每一章也补上了独立的"第 X 章"标题——渐变背景、左侧蓝色竖条、上下留白，让"章"和"节"在视觉上彻底分开。

## 03 侧边栏：项目名终于写全了

> "ProKit / CI Tools（旧）" + "完全指南"，分成两行，字号统一、字重统一，一眼就知道这是什么。

![侧边栏品牌区：两行布局](https://www.kbitai.com.cn/resources/AC_Tutorial/ci_tools/article_images/sidebar_brand.jpg)

切换英文模式，品牌区自动变成 "ProKit / CI Tools (legacy)" + "Complete Guide"。整站 24 页全部同步。

## 04 中英切换：EN 模式不再"中英混杂"

之前切换到英文，页面级的"开始使用"、"全量文章目录"这些标题还是中文。

现在全部包好了双语标签——切到 EN 就显示 "Get Started" / "Full Article Index"，干净利落。

## 一个小插曲

最后一步去掉副标题的灰色时，PowerShell 的正则把 CSS 闭合的 `}` 一起吞掉了，整个侧边栏瞬间乱成一锅粥。

解决方式：回滚 + 换 Python 精准替换。

教训是——**做批量文本替换时，正则要永远保住结构完整性，不能只顾着匹配目标字符串。**

## 现在就去看看

访问 **www.kbitai.com.cn** ，进入 AC Tutorial → CI Tools，或直接搜索"ProKit 完全指南"。

按 **Ctrl + Shift + R** 强刷一下，感受新版本。

有建议欢迎后台留言。
