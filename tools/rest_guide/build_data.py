# -*- coding: utf-8 -*-
"""合并剩余 4 分册的译文与原文为 articles.json。

输入：tools/rest_guide/{raw,en_clean,zh}/{id}.{json|html}
输出：tools/rest_guide/articles.json
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

# 分册定义：显示顺序 + 中文标题
BOOKS = {
    "Getting Started": {
        "page": "gettingstarted.html",
        "title_zh": "入门与安装",
        "kicker": "入门指南 / Getting Started",
    },
    "LaunchPad": {
        "page": "launchpad.html",
        "title_zh": "启动台",
        "kicker": "工具分册 / Reference Chapter",
    },
    "Bracing": {
        "page": "bracing.html",
        "title_zh": "支撑（NZ 专用）",
        "kicker": "工具分册 / Reference Chapter",
    },
    "Labeller": {
        "page": "labeller.html",
        "title_zh": "表面标注",
        "kicker": "工具分册 / Reference Chapter",
    },
}

# 各篇中文标题与排序（按 id）
TITLES = {
    # Getting Started
    "360001013796": "第 1 步：下载并安装 Ci Installer",
    "360001004595": "认识 Ci Tools 安装器",
    "212058666": "第 2 步：安装 CI Tools",
    "360000565575": "第 3 步：应用 Ci Tools 工作环境配置",
    "6670736377615": "第 4 步：激活工具或开始试用",
    "203711800": "如何获取 30 天试用版",
    "205332530": "电脑上已有 Cadimage 安装器时如何安装工具",
    "205069694": "重置工具安装设置",
    "205332500": "创建离线安装文件",
    "360000586095": "Ci Tools 托管部署指南（多机批量安装）",
    "205332550": "在 Archicad 内检查更新",
    "360001004575": "通过安装器更新工具",
    "205332560": "设置「每日贴士」偏好",
    "217200806": "手动把工具加进工具箱",
    "218103543": "在工具箱中显示 Cadimage / Ci Tools 图标",
    "15337912093583": "手动卸载 Ci Tools",
    "8157247435407": "Ci Tools 订阅套餐说明",
    "10608799688079": "变更订阅套餐或支付方式",
    "208082996": "把 Ci Tools 部署到 BIMcloud / BIM Server",
    "9329825787663": "更新 BIMcloud 上的 Ci Tools 库",
    "10886875093391": "Archicad 28/29 的库加载新机制（Libpack）",
    "13957207499279": "在 Archicad 29 中打开旧版项目的库加载",
    "13496226496143": "Archicad 29 技术预览版 Ci Tools 安装",
    "360003865516": "疑难：Ci Tools 库版本不匹配警告",
    "9365919766159": "各工具入门视频合集",
    "4405269195919": "Q&A 研讨会实操视频索引",
    "14581623162639": "Ci Tools 实用链接",
    # LaunchPad
    "11169235181967": "把项目库从 27 迁移到 Global Libraries",
    "11352953618319": "Launchpad 发布网络研讨会（2024 年 11 月）",
    # Bracing
    "360000546816": "工具概览：NZS 3604 木框架支撑设计",
    "360000548435": "安装 Cadimage Bracing 工具",
    "360000549475": "设置风区与地震区",
    "360000547096": "单层建筑支撑布置",
    "360000547376": "两层建筑支撑布置",
    "360003640276": "创建自定义支撑类型",
    "360000548835": "团队协作项目中使用 Bracing",
    "360000548875": "疑难：找不到内/外墙（INT/EXT）",
    "8297046906383": "Archicad 27 版更新：自动尺寸与支撑重新编号",
    "8620440038159": "发布说明 - Bracing 6.16",
    # Labeller
    "15938882269583": "表面标注的放置与更新",
}

# 分册内文章顺序（id 列表）
ORDER = {
    "Getting Started": [
        "360001013796", "360001004595", "212058666", "360000565575",
        "6670736377615", "203711800", "205332530", "205069694",
        "205332500", "360000586095", "205332550", "360001004575",
        "205332560", "217200806", "218103543", "15337912093583",
        "8157247435407", "10608799688079", "208082996", "9329825787663",
        "10886875093391", "13957207499279", "13496226496143",
        "360003865516", "9365919766159", "4405269195919", "14581623162639",
    ],
    "LaunchPad": ["11169235181967", "11352953618319"],
    "Bracing": [
        "360000546816", "360000548435", "360000549475", "360000547096",
        "360000547376", "360003640276", "360000548835", "360000548875",
        "8297046906383", "8620440038159",
    ],
    "Labeller": ["15938882269583"],
}


def strip_tags(html):
    return re.sub(r"<[^>]+>", "", html)


def main():
    out = {"books": BOOKS, "articles": []}
    for cat, ids in ORDER.items():
        for aid in ids:
            raw = json.load(open(os.path.join(HERE, "raw", f"{aid}.json"), encoding="utf-8"))
            zh = open(os.path.join(HERE, "zh", f"{aid}.html"), encoding="utf-8").read().strip()
            en = open(os.path.join(HERE, "en_clean", f"{aid}.html"), encoding="utf-8").read().strip()
            out["articles"].append({
                "id": aid,
                "cat": cat,
                "title_en": raw["title"].strip(),
                "title_zh": TITLES[aid],
                "zh": zh,
                "en": en,
                "url": raw["url"],
                "updated_at": raw.get("updated_at", ""),
                "n_imgs": len(re.findall(r'src="img/', zh)),
                "n_chars": len(strip_tags(zh)),
            })
    with open(os.path.join(HERE, "articles.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    # 汇总
    from collections import defaultdict
    stats = defaultdict(lambda: [0, 0, 0])
    for a in out["articles"]:
        s = stats[a["cat"]]
        s[0] += 1
        s[1] += a["n_imgs"]
        s[2] += a["n_chars"]
    for cat, (n, img, ch) in stats.items():
        print(f"{cat:15s} {n:3d} 篇  {img:3d} 图  {ch:6d} 字")
    print("合计", sum(v[0] for v in stats.values()), "篇",
          sum(v[1] for v in stats.values()), "图",
          sum(v[2] for v in stats.values()), "字")


if __name__ == "__main__":
    main()
