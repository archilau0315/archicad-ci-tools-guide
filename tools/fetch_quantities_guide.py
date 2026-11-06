# -*- coding: utf-8 -*-
"""从官方 Zendesk 知识库抓取 Quantities 分册缺失的 22 篇手册章节。

输出：
  tools/q_guide/raw/{id}.json   每篇：id、title、html（图片已改写为本地路径占位）
  site/img/{id}_{n}.png|.jpg    正文图片

重复运行安全：已有文件跳过。
"""
import io
import json
import os
import re
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "q_guide", "raw")
SITE = os.path.join(HERE, "..", "site")
IMG = os.path.join(SITE, "img")
CAT = 360000115776  # 官方 Quantities 分类
API = "https://cadimage.zendesk.com/api/v2/help_center/en-us"


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

    # 1) 官方全量 vs 站内已有，求缺失集
    qhtml = io.open(os.path.join(SITE, "quantities.html"), encoding="utf-8").read()
    ours = set(re.findall(r'href="https://cadimage\.zendesk\.com/hc/en-us/articles/(\d+)[^"]*"', qhtml))
    official = {}
    for page in (1, 2):
        d = fetch_json(f"{API}/categories/{CAT}/articles.json?per_page=100&page={page}")
        for a in d.get("articles", []):
            official[str(a["id"])] = a["title"]
        time.sleep(0.2)
    miss = {i: t for i, t in official.items() if i not in ours}
    print(f"官方 {len(official)} 篇 / 站内 {len(ours)} 篇 / 待抓 {len(miss)} 篇")

    # 2) 逐篇抓正文 + 图片
    for aid, title in sorted(miss.items(), key=lambda x: x[1]):
        out = os.path.join(RAW, f"{aid}.json")
        if os.path.exists(out):
            print(f"  [跳过] {title}")
            continue
        d = fetch_json(f"{API}/articles/{aid}.json")["article"]
        body = d.get("body") or ""
        # 图片：下载并改写 src
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
            "title": title,
            "html": body,
            "created_at": d.get("created_at", ""),
            "updated_at": d.get("updated_at", ""),
            "url": f"https://cadimage.zendesk.com/hc/en-us/articles/{aid}",
        }
        io.open(out, "w", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False, indent=1))
        print(f"  [OK] {title}")
        time.sleep(0.2)
    print("完成")


if __name__ == "__main__":
    main()
