# -*- coding: utf-8 -*-
"""合并 raw / en_clean / zh 三处数据为注入用 articles.json。

每条：id、no（手册编号）、zh（中文标题）、en（官方标题）、src（官方链接）、
      zh_body（中文译文 HTML）、en_body（清洗后官方 HTML）
"""
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

ZH_TITLES = {
    "1.1": "1.1 工具定位：为什么在模型上直接算量",
    "1.2": "1.2 核心功能：与 ARCHICAD 原生明细表的七点差异",
    "1.3": "1.3 术语定义（BoQ / 清单条目 / 类别 / 编号 / 特征标记）",
    "2.1": "2.1 总览：属性、分类与配方的管理背景",
    "2.2": "2.2 查看构件数据：Quantities Info 面板详解",
    "2.3": "2.3 管理特征标记（配方 / 属性 / 分类）",
    "2.3.1": "2.3.1 如何给构件添加特征标记",
    "2.3.2": "2.3.2 如何从构件移除特征标记",
    "2.3.3": "2.3.3 如何把选定的特征标记设置或转移到构件",
    "2.3.4": "2.3.4 如何让新建构件自动带上特征标记",
    "2.3.5": "2.3.5 如何选中匹配所选特征标记的构件",
    "2.3.6": "2.3.6 如何把选择集筛选为匹配特征标记的构件",
    "2.3.7": "2.3.7 如何快速发现选择集中的异常与问题",
    "2.3.8": "2.3.8 如何在 ARCHICAD 设置对话框中编辑配方",
    "2.3.9": "2.3.9 如何让构件不参与成本度量",
    "2.4": "2.4 管理被度量的属性",
    "2.4.1": "2.4.1 如何编辑属性值",
    "2.4.2": "2.4.2 如何查看同一属性的不同取值",
    "2.4.3": "2.4.3 如何同时编辑多个属性值",
    "2.4.4": "2.4.4 如何给构件添加属性",
    "2.4.5": "2.4.5 如何从构件删除属性",
    "2.4.6": "2.4.6 如何按属性值选中构件",
}


def sort_key(no):
    return tuple(int(x) for x in no.split("."))


def main():
    out = []
    for fn in sorted(os.listdir(os.path.join(HERE, "raw"))):
        if not fn.endswith(".json"):
            continue
        d = json.load(io.open(os.path.join(HERE, "raw", fn), encoding="utf-8"))
        no = d["title"].split(" ")[0]
        if no not in ZH_TITLES:
            raise SystemExit(f"缺中文标题映射: {d['title']}")
        aid = d["id"]
        zh_body = io.open(os.path.join(HERE, "zh", f"{aid}.html"), encoding="utf-8").read().strip()
        en_body = io.open(os.path.join(HERE, "en_clean", f"{aid}.html"), encoding="utf-8").read().strip()
        out.append({
            "id": aid, "no": no, "zh": ZH_TITLES[no], "en": d["title"],
            "src": d["url"], "zh_body": zh_body, "en_body": en_body,
        })
    out.sort(key=lambda a: sort_key(a["no"]))
    path = os.path.join(HERE, "articles.json")
    io.open(path, "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1))
    print("生成", path, len(out), "篇")


if __name__ == "__main__":
    main()
