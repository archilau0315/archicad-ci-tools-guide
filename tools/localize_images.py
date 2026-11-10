#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片本地化：把 HTML 里指向图床的远程图片下载到本地 assets/img/，
并改写为相对路径，使 HTML 完全自包含（可离线打开、可随目录迁移）。

用法：
    python3 localize_images.py <html文件> [assets/img目录]
"""
import io, os, re, sys, urllib.request, concurrent.futures as cf


def download(url, dest):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=40).read()
        with open(dest, "wb") as f:
            f.write(data)
        return len(data)
    except Exception as e:
        print(f"  ! 下载失败 {url}: {e}")
        return 0


def main():
    html_path = sys.argv[1]
    img_dir = sys.argv[2] if len(sys.argv) > 2 else "assets/img"
    os.makedirs(img_dir, exist_ok=True)

    h = io.open(html_path, encoding="utf-8").read()
    urls = sorted(set(re.findall(r'<img[^>]+src="(https://[^"]+)"', h)))
    if not urls:
        print("无远程图片，无需处理")
        return

    print(f"发现 {len(urls)} 张远程图片")
    mapping = {}
    for u in urls:
        name = u.rsplit("/", 1)[-1]
        if not name.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp")):
            name += ".jpg"
        dest = os.path.join(img_dir, name)
        if not os.path.exists(dest) or os.path.getsize(dest) == 0:
            n = download(u, dest)
            if n == 0:
                continue
        mapping[u] = name

    # 改写为相对路径
    for u, name in mapping.items():
        rel = os.path.relpath(os.path.join(img_dir, name),
                              os.path.dirname(os.path.abspath(html_path)))
        rel = rel.replace(os.sep, "/")   # 浏览器只认正斜杠
        h = h.replace(f'src="{u}"', f'src="{rel}"')

    io.open(html_path, "w", encoding="utf-8").write(h)
    ok = len(re.findall(r'<img[^>]+src="https://', h))
    print(f"本地化 {len(mapping)} 张 → {img_dir}")
    print(f"剩余远程引用: {ok}")


if __name__ == "__main__":
    main()
