# -*- coding: utf-8 -*-
"""从官方 Zendesk 知识库抓取剩余 4 个分册的 40 篇文章。

分类：Getting Started(27)、Bracing(10)、LaunchPad(2)、Labeller(1)

输出：
  tools/rest_guide/raw/{id}.json   每篇：id、title、cat、html（图片已改写为本地路径）
  site/img/{id}_{n}.png|.jpg       正文图片

重复运行安全：已有文件跳过。
"""
import json
import os
import re
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "rest_guide", "raw")
SITE = os.path.join(HERE, "..", "site")
IMG = os.path.join(SITE, "img")
API = "https://cadimage.zendesk.com/api/v2/help_center/en-us"

CATS = {
    "Getting Started": 360000097455,
    "LaunchPad": 11158360871311,
    "Bracing": 360000027695,
    "Labeller": 16013306289935,
}


def fetch_json(url):
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)


def download(url, path):
    if os.path.exists(path):
        return
    with urllib.request.urlopen(url, timeout=30) as r:
        data = r.read()
    with open(path, "wb") as f:
        f.write(data)


def main():
    os.makedirs(RAW, exist_ok=True)
    os.makedirs(IMG, exist_ok=True)

    official = {}
    for name, cid in CATS.items():
        page = 1
        while True:
            d = fetch_json(f"{API}/categories/{cid}/articles.json?per_page=100&page={page}")
            for a in d.get("articles", []):
                official[str(a["id"])] = name
            if len(d.get("articles", [])) < 100:
                break
            page += 1
            time.sleep(0.2)
    print(f"官方合计 {len(official)} 篇")

    for aid, cat in sorted(official.items(), key=lambda x: (list(CATS).index(x[1]), x[0])):
        out = os.path.join(RAW, f"{aid}.json")
        if os.path.exists(out):
            print(f"  [跳过] {aid}")
            continue
        d = fetch_json(f"{API}/articles/{aid}.json")["article"]
        body = d.get("body") or ""
        imgs = re.findall(r'src="(https://[^"]+)"', body)
        for n, u in enumerate(imgs):
            ext = ".png" if ".png" in u.lower() else ".jpg"
            fn = f"{aid}_{n}{ext}"
            try:
                download(u, os.path.join(IMG, fn))
                body = body.replace(u, f"img/{fn}")
            except Exception as e:
                print(f"  [图片失败] {fn}: {e}")
        rec = {
            "id": aid,
            "title": d.get("title", ""),
            "cat": cat,
            "html": body,
            "created_at": d.get("created_at", ""),
            "updated_at": d.get("updated_at", ""),
            "url": f"https://cadimage.zendesk.com/hc/en-us/articles/{aid}",
        }
        with open(out, "w", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False, indent=1))
        print(f"  [OK] {cat} | {rec['title']}")
        time.sleep(0.2)
    print("完成")


if __name__ == "__main__":
    main()
