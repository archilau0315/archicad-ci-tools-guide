#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ProKit 静态站全站校验；失败时输出文件与行号并返回退出码 1。"""
import io
import json
import os
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

from build_search_index import TOOLS as SEARCH_TOOLS
from rebrand_prokit import TOOLS, WHITELIST

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
SITE = os.path.join(ROOT, "site")
CORE = {"annotate", "transformer", "timetracker", "detail"}
ART_RE = re.compile(r'<div class="art" id="(a-[\w.\-]+)">(.*?)'
                    r'(?=<div class="art" id="a-|</article>)', re.S)
H3_ZH = re.compile(r'<h3\b[^>]*class="zh-only block">(.*?)</h3>', re.S)
H3_EN = re.compile(r'<h3\b[^>]*class="en-only block">(.*?)</h3>', re.S)
OLD_PATH = re.compile(r"\b[Cc][Ii] Tools\s*(?:→|>|&gt;)")
STACK_TAGS = {"div", "article", "main", "aside", "details", "script", "style",
              "table", "figure", "ul", "ol"}
COUNT_TAGS = STACK_TAGS | {"tr", "td", "th"}


class StructureParser(HTMLParser):
    def __init__(self, name, errors):
        super().__init__(convert_charrefs=True)
        self.name = name
        self.errors = errors
        self.stack = []
        self.counts = Counter()
        self.ids = []

    def handle_starttag(self, tag, attrs):
        self.ids.extend(v for k, v in attrs if k == "id" and v)
        if tag not in COUNT_TAGS:
            return
        self.counts[tag] += 1
        if tag in STACK_TAGS:
            self.stack.append((tag, self.getpos()[0]))

    def handle_startendtag(self, tag, attrs):
        self.ids.extend(v for k, v in attrs if k == "id" and v)

    def handle_endtag(self, tag):
        if tag not in STACK_TAGS:
            return
        line = self.getpos()[0]
        if not self.stack or tag not in {t for t, _ in self.stack}:
            self.errors.append(f"{self.name}:{line} 多余闭合标签 </{tag}>")
            return
        if self.stack[-1][0] != tag:
            open_tags = ", ".join(f"<{t}>@{n}" for t, n in reversed(self.stack) if t != tag)
            self.errors.append(f"{self.name}:{line} </{tag}> 闭合前仍有未闭合标签：{open_tags}")
        while self.stack:
            open_tag, _ = self.stack.pop()
            if open_tag == tag:
                break

    def finish(self):
        for tag, line in reversed(self.stack):
            self.errors.append(f"{self.name}:{line} <{tag}> 未闭合")
        for value, count in Counter(self.ids).items():
            if count > 1:
                self.errors.append(f"{self.name} id={value} 重复 {count} 次")


class Verifier:
    def __init__(self):
        self.errors = []
        self.html = {}
        self.ids = {}
        self.articles = {}

    def fail(self, message):
        self.errors.append(message)

    def load(self):
        names = sorted(n for n in os.listdir(SITE) if n.endswith(".html"))
        if len(names) != 24:
            self.fail(f"页面数应为 24，实际 {len(names)}")
        for name in names:
            text = io.open(os.path.join(SITE, name), encoding="utf-8").read()
            self.html[name] = text
            parser = StructureParser(name, self.errors)
            parser.feed(text)
            parser.close()
            parser.finish()
            self.ids[name] = set(parser.ids)
            found = list(ART_RE.finditer(text))
            self.articles[name] = found
            for match in found:
                aid, block = match.group(1), match.group(2)
                if not H3_ZH.search(block) or not H3_EN.search(block):
                    self.fail(f"{name}#{aid} 缺少中英文章标题")
                if 'class="zh-only' not in block or 'class="en-only' not in block:
                    self.fail(f"{name}#{aid} 缺少双语正文")
            title = re.search(r"<title>(.*?)</title>", text, re.S)
            if not title or "ProKit / CI Tools（旧）" not in title.group(1):
                self.fail(f"{name} 标题缺少 ProKit / CI Tools（旧）品牌")
            if 'class="lang-switch"' not in text or 'data-lang="zh"' not in text:
                self.fail(f"{name} 缺少双语切换")
            sidebar = text.split('<aside class="sidebar"', 1)[-1].split("</aside>", 1)[0]
            for group in ("ProKit Core · 4", "ProKit Suite · 11", "其他 / 旧版 · 3"):
                if group not in sidebar:
                    self.fail(f"{name} 侧栏缺少分组 {group}")
            for tool, en, zh, icon, package, source in TOOLS:
                label = (f'<span class="zh-only">{en} · {zh}</span>'
                         f'<span class="en-only">{en}</span>')
                if label not in sidebar:
                    self.fail(f"{name} 侧栏工具名未统一：{en}")

    def verify_articles(self):
        tool_total = 0
        for tool, en, zh, icon, package, source in TOOLS:
            name = tool + ".html"
            text = self.html.get(name, "")
            matches = self.articles.get(name, [])
            tool_total += len(matches)
            if f"pkg pkg-{package}" not in text:
                self.fail(f"{name} 缺少 {package} 包徽标")
            if not matches:
                self.fail(f"{name} 没有工具文章")
        getting = self.articles.get("gettingstarted.html", [])
        total = tool_total + len(getting)
        if (tool_total, len(getting), total) != (391, 33, 424):
            self.fail(f"文章计数错误：工具 {tool_total} / 入门 {len(getting)} / 全站 {total}")
        new_ids = {m.group(1) for m in getting if m.group(1).startswith("a-prokit-")}
        if len(new_ids) != 6:
            self.fail(f"入门页 AC30 主线应为 6 篇，实际 {len(new_ids)}")
        text = self.html.get("gettingstarted.html", "")
        if 'class="legacy-install"' not in text or "AC24–AC29" not in text:
            self.fail("入门页缺少 AC24–AC29 旧版折叠归档")

    def verify_links(self):
        for name, text in self.html.items():
            for attr, href in re.findall(r'\b(href|src)="([^"]+)"', text):
                if not href or href.startswith(("data:", "javascript:", "mailto:", "tel:")):
                    continue
                parsed = urlsplit(href)
                if parsed.scheme or parsed.netloc:
                    continue
                path = unquote(parsed.path)
                target_name = os.path.normpath(os.path.join(os.path.dirname(name), path)) if path else name
                target_path = os.path.normpath(os.path.join(SITE, path)) if path else os.path.join(SITE, name)
                if path and not os.path.exists(target_path):
                    self.fail(f"{name} 死链 {attr}={href}")
                    continue
                if parsed.fragment and target_name in self.ids:
                    anchor = unquote(parsed.fragment)
                    if anchor not in self.ids[target_name]:
                        self.fail(f"{name} 死锚点 {href}")

    def verify_search(self):
        path = os.path.join(SITE, "search-index.js")
        raw = io.open(path, encoding="utf-8").read()
        try:
            payload = raw.split("window.CI_SEARCH_INDEX = ", 1)[1].strip().removesuffix(";")
            data = json.loads(payload)
        except (IndexError, json.JSONDecodeError) as exc:
            self.fail(f"search-index.js 无法解析：{exc}")
            return
        if len(data.get("tools", [])) != 18 or len(data.get("pages", [])) != 6:
            self.fail("搜索索引应为 18 个工具 / 6 个页面")
        records = data.get("articles", [])
        if len(records) != 424:
            self.fail(f"搜索索引应有 424 篇，实际 {len(records)}")
        indexed = {(r.get("f"), r.get("a")) for r in records}
        actual = {(name, m.group(1)) for name, matches in self.articles.items()
                  for m in matches if name != "index.html"}
        if indexed != actual:
            missing = sorted(actual - indexed)[:8]
            stale = sorted(indexed - actual)[:8]
            self.fail(f"搜索索引与正文不一致，缺少 {missing}，多余 {stale}")
        if len(indexed) != len(records):
            self.fail("搜索索引存在重复文章锚点")
        for record in records:
            if not record.get("zh") or not record.get("en"):
                self.fail(f"搜索索引缺双语标题：{record.get('f')}#{record.get('a')}")
            elif record["a"] not in self.ids.get(record["f"], set()):
                self.fail(f"搜索索引死锚点：{record['f']}#{record['a']}")

    def verify_catalogs_and_images(self):
        for catalog in ("index.html", "all.html"):
            text = self.html.get(catalog, "")
            for name, matches in self.articles.items():
                if name in {"gettingstarted.html", "index.html"} or not matches:
                    continue
                for match in matches:
                    link = f"{name}#{match.group(1)}"
                    if link not in text:
                        self.fail(f"{catalog} 缺少目录项 {link}")
        for phrase in ("18 个工具、424 篇教程", "共 391 篇"):
            if phrase not in self.html.get("index.html", ""):
                self.fail(f"index.html 缺少计数文案：{phrase}")
        if "共 391 篇工具教程" not in self.html.get("all.html", ""):
            self.fail("all.html 工具篇数不是 391")
        for name in CORE:
            text = self.html.get(name + ".html", "")
            for src in re.findall(r'<img[^>]+src="([^"]+)"', text):
                if not src.startswith(f"img/prokit/{name}/"):
                    self.fail(f"{name}.html 图片未走本工具本地目录：{src}")
                elif not os.path.exists(os.path.join(SITE, src.replace("/", os.sep))):
                    self.fail(f"{name}.html 缺图：{src}")
        for name, text in self.html.items():
            if re.search(r'<img[^>]+src="https://help\.graphisoft\.com/', text):
                self.fail(f"{name} 仍引用 Graphisoft 官方图片直链")

    def verify_old_paths(self):
        for name, text in self.html.items():
            # 差异页专门逐项对照 AC29 旧路径与 AC30 新路径。
            if name == "differences.html":
                continue
            if name == "gettingstarted.html" and "<!-- legacy-ci-tools:start -->" in text:
                before, rest = text.split("<!-- legacy-ci-tools:start -->", 1)
                text = before + rest.split("<!-- legacy-ci-tools:end -->", 1)[1]
            for number, line in enumerate(text.splitlines(), 1):
                if OLD_PATH.search(line) and not any(word in line for word in WHITELIST):
                    self.fail(f"{name}:{number} 白名单外旧命令路径：{OLD_PATH.search(line).group(0)}")

    def run(self):
        self.load()
        self.verify_articles()
        self.verify_links()
        self.verify_search()
        self.verify_catalogs_and_images()
        self.verify_old_paths()
        if self.errors:
            print(f"校验失败：{len(self.errors)} 项")
            for error in self.errors:
                print("  -", error)
            return 1
        print("全站校验通过：24 页 / 18 工具 / 424 篇；链接、锚点、双语、索引、图片、徽标与标签结构均正常")
        return 0


if __name__ == "__main__":
    sys.exit(Verifier().run())
