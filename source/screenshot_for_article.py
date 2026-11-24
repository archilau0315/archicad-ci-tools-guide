"""
为公众号文章截图：
1. index_home.png       — 主页首屏（banner 感）
2. index_toc.png        — index.html 里 Quantities 全量目录的章节分组
3. quantities_xref.png  — quantities.html 里的可点击 xref 链接特写
4. sidebar_brand.png    — 左侧 sidebar 顶部 brand 区特写
"""
import os, sys
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except Exception as e:
    print(f"playwright 不可用: {e}", file=sys.stderr)
    sys.exit(1)

BASE = "https://www.kbitai.com.cn/resources/AC_Tutorial/ci_tools/site/"
OUT = Path(r"e:\works\Aidev\Kbitai绝对安全\kbitai_com_cn\resources\AC_Tutorial\ci_tools\article_images")
OUT.mkdir(parents=True, exist_ok=True)

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME, headless=True)
        ctx = browser.new_context(
            viewport={"width": 1440, "height": 900},
            device_scale_factor=2,
            locale="zh-CN",
        )

        # ---- 1. 主页首屏 ----
        page = ctx.new_page()
        page.goto(BASE + "index.html", wait_until="networkidle")
        page.wait_for_timeout(800)
        page.screenshot(path=str(OUT / "index_home.png"))
        print("✓ index_home.png")

        # ---- 2. Quantities 全量目录（章节分组）----
        # 找到 Quantities 区块的全量目录 ul，滚到它并截图整个目录卡片
        page.goto(BASE + "index.html", wait_until="networkidle")
        page.wait_for_timeout(500)
        # 定位到 "全量文章目录 / Full Article Index" 下 Quantities 那一段
        # 直接滚动到包含 chapter divider 的容器
        target = page.locator("li.ch-divider").first
        target.scroll_into_view_if_needed()
        page.wait_for_timeout(400)
        # 截整个 main 内容区域（含分组条）
        page.locator("main").screenshot(path=str(OUT / "index_toc.png"))
        print("✓ index_toc.png")

        # ---- 3. quantities.html 的 xref 链接特写 ----
        page.goto(BASE + "quantities.html", wait_until="networkidle")
        page.wait_for_timeout(500)
        # 滚到第一个 xref 链接，截取其所在段落所在的 article 卡片
        xref = page.locator("a.xref").first
        xref.scroll_into_view_if_needed()
        page.wait_for_timeout(400)
        # 截取包含该 xref 的最近 .art 卡片
        card = xref.locator("xpath=ancestor::div[contains(@class,'art')][1]")
        if card.count() == 0:
            card = page.locator("article").first
        card.screenshot(path=str(OUT / "quantities_xref.png"))
        print("✓ quantities_xref.png")

        # ---- 4. 左侧 sidebar brand 区特写 ----
        page.goto(BASE + "index.html", wait_until="networkidle")
        page.wait_for_timeout(500)
        sb = page.locator(".brand").first
        sb.scroll_into_view_if_needed()
        page.wait_for_timeout(300)
        sb.screenshot(path=str(OUT / "sidebar_brand.png"))
        print("✓ sidebar_brand.png")

        browser.close()
    print(f"\n全部完成 → {OUT}")

if __name__ == "__main__":
    run()
