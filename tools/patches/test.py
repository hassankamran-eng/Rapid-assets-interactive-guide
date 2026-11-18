import os, sys
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
f = "file:///" + os.path.join(HERE, "Rapid_Assets_Interactive_Guide.html").replace("\\", "/")
os.makedirs(os.path.join(HERE, "t"), exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.goto(f); pg.wait_for_timeout(1500)
    pg.screenshot(path=os.path.join(HERE, "t", "0_intro.png"))
    pg.click("#startWatch")
    for k, ms in enumerate([2200, 4000, 5200, 6000]):
        pg.wait_for_timeout(ms)
        pg.screenshot(path=os.path.join(HERE, "t", f"{k+1}_watch.png"))
    # jump to the anim chapter, typing step
    pg.click("#speed button[data-s='2']")
    pg.locator(".chap").nth(6).click(); pg.wait_for_timeout(9000)
    pg.screenshot(path=os.path.join(HERE, "t", "5_anim.png"))
    # try mode
    pg.click("#mode button[data-m='try']"); pg.wait_for_timeout(2500)
    pg.screenshot(path=os.path.join(HERE, "t", "6_try.png"))
    pg.click("#ring"); pg.wait_for_timeout(3000)
    pg.screenshot(path=os.path.join(HERE, "t", "7_try_after.png"))
    print("errors:", errs[:5])
    b.close()
