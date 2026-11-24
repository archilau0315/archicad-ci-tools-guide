#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一键部署 site/ 目录到阿里云 ECS（宝塔面板）。

用法：
    python source/deploy.py              # 部署 site/ 下所有 .html
    python source/deploy.py quantities.html metadata.html
    python source/deploy.py --all        # 同无参数
    python source/deploy.py --dry-run    # 只打印要传什么，不真传
"""
import os, sys, fnmatch, paramiko

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(HERE, "..", "site"))

# ===== 服务器配置 =====
HOST = "47.93.210.248"
PORT = 22
USER = "root"
PASS = "100422lyf"
# 线上站点根（宝塔面板，www 用户运行 nginx/php）
REMOTE_ROOT = "/www/wwwroot/kbitai.com.cn"
# 要部署的本地子目录（相对于 SITE 的内容拼到 REMOTE_ROOT 后面）
REMOTE_SUBDIR = "resources/AC_Tutorial/ci_tools/site"
OWNER = "www:www"


def _ssh():
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(hostname=HOST, port=PORT, username=USER, password=PASS, timeout=15)
    return c


def _run(ssh, cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
    out = stdout.read().decode("utf-8", errors="replace").strip()
    err = stderr.read().decode("utf-8", errors="replace").strip()
    return out, err


def discover_files(explicit=None):
    """返回 (local_path, remote_path) 列表。"""
    files = []
    if explicit:
        for name in explicit:
            p = os.path.join(SITE, name)
            if not os.path.isfile(p):
                print(f"  ✗ 跳过（不存在）：{p}")
                continue
            rem = f"{REMOTE_ROOT}/{REMOTE_SUBDIR}/{name}"
            files.append((p, rem))
    else:
        for n in sorted(os.listdir(SITE)):
            if n.endswith(".html"):
                p = os.path.join(SITE, n)
                rem = f"{REMOTE_ROOT}/{REMOTE_SUBDIR}/{n}"
                files.append((p, rem))
    return files


def main():
    args = sys.argv[1:]
    dry = "--dry-run" in args
    args = [a for a in args if a not in ("--dry-run", "--all")]
    explicit = args or None

    files = discover_files(explicit)
    if not files:
        print("没有要部署的文件")
        sys.exit(0)

    print(f"将部署 {len(files)} 个文件 → {REMOTE_ROOT}/{REMOTE_SUBDIR}/")
    for p, r in files:
        print(f"  {os.path.basename(p)}  ({os.path.getsize(p):,} bytes)")

    if dry:
        print("\n[dry-run] 不真上传")
        return

    print(f"\n连接 {USER}@{HOST}:{PORT} ...")
    ssh = _ssh()
    sftp = ssh.open_sftp()

    uploaded = 0
    for local, remote in files:
        try:
            sftp.put(local, remote)
            uploaded += 1
            print(f"  ✓ {os.path.basename(local)}  →  {remote}")
        except Exception as e:
            print(f"  ✗ {os.path.basename(local)}: {e}")

    sftp.close()

    # 修正 owner（宝塔的网站运行用户是 www）
    if uploaded:
        targets = " ".join(r for _, r in files)
        out, err = _run(ssh, f"chown {OWNER} {targets} 2>&1")
        if err:
            print(f"  chown 提示: {err[:100]}")

        # curl 验证
        base_url = "https://www.kbitai.com.cn"
        for local, remote in files:
            rel = remote.replace(REMOTE_ROOT + "/", "")
            url = f"{base_url}/{rel}"
            out, err = _run(ssh, f"curl -sI '{url}' | head -3")
            status_line = out.split("\n")[0] if out else "(无响应)"
            print(f"  线上 {os.path.basename(local)}: {status_line}")

    ssh.close()
    print(f"\n完成：{uploaded}/{len(files)} 个文件已部署 ✓")


if __name__ == "__main__":
    main()
