#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""上传文章配图到公网站点，返回可外链的 URL 列表。

用法：python source/upload_article_images.py
输出：article_images/urls.txt（每行 name<TAB>url）
"""
import os, sys, paramiko

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
LOCAL_DIR = os.path.join(ROOT, "article_images")

HOST, PORT, USER, PASS = "47.93.210.248", 22, "root", "100422lyf"
REMOTE_DIR = "/www/wwwroot/kbitai.com.cn/resources/AC_Tutorial/ci_tools/article_images"
BASE_URL = "https://www.kbitai.com.cn/resources/AC_Tutorial/ci_tools/article_images"


def main():
    names = sorted(n for n in os.listdir(LOCAL_DIR) if n.lower().endswith((".jpg", ".png")))
    if not names:
        print("没有图片")
        sys.exit(1)
    # 优先上传 jpg（压缩版），跳过同名 png 以减少体积
    jpg_stems = {os.path.splitext(n)[0] for n in names if n.endswith(".jpg")}
    upload = [n for n in names if not (n.endswith(".png") and os.path.splitext(n)[0] in jpg_stems)]

    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(hostname=HOST, port=PORT, username=USER, password=PASS, timeout=15)
    c.exec_command(f"mkdir -p {REMOTE_DIR}", timeout=20)[1].read()

    sftp = c.open_sftp()
    lines = []
    for n in upload:
        lp = os.path.join(LOCAL_DIR, n)
        rp = f"{REMOTE_DIR}/{n}"
        sftp.put(lp, rp)
        url = f"{BASE_URL}/{n}"
        lines.append(f"{n}\t{url}")
        print(f"  ✓ {n} ({os.path.getsize(lp):,}B) -> {url}")
    sftp.close()

    c.exec_command(f"chown -R www:www {REMOTE_DIR}", timeout=20)[1].read()

    # 公网可达性检查
    print("\n线上验证：")
    for n in upload:
        url = f"{BASE_URL}/{n}"
        code = c.exec_command(f"curl -s -o /dev/null -w '%{{http_code}}' '{url}'", timeout=25)[1].read().decode().strip()
        print(f"  {code}  {n}")
    c.close()

    out = os.path.join(LOCAL_DIR, "urls.txt")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"\nURL 清单 -> {out}")


if __name__ == "__main__":
    main()
