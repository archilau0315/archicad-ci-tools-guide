"""重截聚焦版：index_toc（章节分组特写）+ quantities_xref（链接特写）"""
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = "https://www.kbitai.com.cn/resources/AC_Tutorial/ci_tools/site/"
OUT = Path(r"e:\works\Aidev\Kbitai绝对安全\kbitai_com_cn\resources\AC_Tutorial\ci_tools\article_images")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=CHROME, headless=True)
    ctx = browser.new_context(viewport={"width": 1440, "height": 1000},
                              device_scale_factor=2, locale="zh-CN")
    page = ctx.new_page()

    # ---- Quantities 全量目录分组特写 ----
    page.goto(BASE + "index.html", wait_until="networkidle")
    page.wait_for_timeout(500)
    # 滚动到全量文章目录里第一个 chapter divider
    divs = page.locator("li.ch-divider")
    print(f"chapter dividers: {divs.count()}")
    divs.first.scroll_into_view_if_needed()
    page.wait_for_timeout(400)
    # 取第一个 divider 在页面中的位置，向上留一点，截 1440x1000 的窗口
    box = divs.first.bounding_box()
    print("first divider box:", box)
    clip = {"x": 0, "y": box["y"] - 30, "width": 1440, "height": 1000}
    page.screenshot(path=str(OUT / "index_toc.png"), clip=clip)
    print("✓ index_toc.png (focused)")

    # ---- xref 链接特写 ----
    page.goto(BASE + "quantities.html", wait_until="networkidle")
    page.wait_for_timeout(500)
    xref = page.locator("a.xref").first
    xref.scroll_into_view_if_needed()
    page.wait_for_timeout(400)
    box = xref.bounding_box()
    print("first xref box:", box)
    # 截取该 xref 所在段落的上下文：以 xref 为中心，1440x900
    cx = box["x"] + box["width"] / 2
    cy = box["y"] + box["height"] / 2
    clip = {"x": 0, "y": max(0, cy - 400), "width": 1440, "height": 900}
    page.screenshot(path=str(OUT / "quantities_xref.png"), clip=clip)
    print("✓ quantities_xref.png (focused)")

    browser.close()
print("done")
