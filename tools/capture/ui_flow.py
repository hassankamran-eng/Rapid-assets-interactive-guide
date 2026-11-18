"""Game UI in Studio (prod, original UI): home screen -> UI kit in this style -> Shop screen -> Settings screen.
Screens pu_*; saves the home screen as wf_inputs/home_screen.png for the UI Kit workflow."""
import json, os, sys
from drv import run, HERE

URL = json.load(open(os.path.join(HERE, "demo.json")))["url"].replace("https://rapidassets.ai", "")
HOME = ("Home screen for my fantasy RPG game, full screen, landscape: the title KNIGHT QUEST at the top, "
        "a big PLAY button in the middle with SHOP and SETTINGS buttons under it, coin and gem counters in a top bar, "
        "a player panel with a knight avatar and LEVEL 12 on the left. Carved wood and gold frames with blue gems, "
        "castle in the background")
SHOP = ("Now the Shop screen in the same style: a SHOP title banner, a grid of item panels (sword, shield, potion, "
        "gem pack) each with a price and a BUY button, the coin counter at the top and a close button")
SETTINGS = ("Now the Settings screen in the same style: a SETTINGS panel with Music and Sound sliders, "
            "Vibration and Notifications on/off toggles, a language tab, and a BACK button")
ONLY = sys.argv[1:]


def vis(loc):
    return [loc.nth(i) for i in range(loc.count()) if loc.nth(i).is_visible()]


def dismiss(p):
    for lab in ("Maybe later", "Not now", "Got it", "Skip for now"):
        for b in vis(p.get_by_text(lab, exact=True)):
            try: b.click(); p.wait_for_timeout(500)
            except Exception: pass


def wait_result(d, tag, before, secs=300):
    p = d.page
    yes = []
    for _ in range(45):
        p.wait_for_timeout(4000)
        yes = vis(p.get_by_text("Yes, generate", exact=True))
        if yes or p.get_by_text("Rate this result").count() > before:
            break
    if yes:
        p.wait_for_timeout(1500); d.shot(f"pu_{tag}_plan", hl=yes[-1]); yes[-1].click()
        p.wait_for_timeout(8000); d.shot(f"pu_{tag}_working")
    for _ in range(secs // 5):
        if p.get_by_text("Rate this result").count() > before:
            break
        p.wait_for_timeout(5000)
    p.wait_for_timeout(7000); dismiss(p)
    d.shot(f"pu_{tag}_result")


def last_image(p):
    """src of the newest big image in the chat column."""
    return p.evaluate("""() => { const im = [...document.querySelectorAll('img')].filter(i => i.offsetParent && i.naturalWidth >= 400
        && i.getBoundingClientRect().left < innerWidth * 0.5); return im.length ? im[im.length - 1].src : null; }""")


def save_src(p, src, path):
    if not src: print("   no image src"); return
    if src.startswith("blob:") or src.startswith("data:"):
        b64 = p.evaluate("async s => { const r = await fetch(s); const b = await r.blob(); return await new Promise(ok => { const f = new FileReader(); f.onload = () => ok(f.result.split(',')[1]); f.readAsDataURL(b); }); }", src)
        import base64; data = base64.b64decode(b64)
    else:
        data = p.request.get(src).body()
    open(path, "wb").write(data); print("   saved", path, len(data), flush=True)


def send(d, text, tag, secs=300):
    p = d.page
    box = vis(p.locator("textarea"))[-1]
    box.fill(text); p.wait_for_timeout(800)
    d.shot(f"pu_{tag}_typed", hl=p.get_by_role("button", name="Send message"))
    before = p.get_by_text("Rate this result").count()
    box.press("Enter")
    wait_result(d, tag, before, secs)


def flow(d):
    p = d.page
    d.go(URL, wait=7000); dismiss(p)
    nc = vis(p.locator("button[aria-label*='New chat' i], button[aria-label*='New conversation' i], button[title*='New chat' i]"))
    if nc:
        nc[0].click(); p.wait_for_timeout(3000); dismiss(p)
    else:
        print("   no New chat button"); d.buttons(60)
    d.shot("pu_new_chat")
    # asset type stays Any for whole screens (UI type would cut the screen out)
    t = vis(p.locator("button[aria-label^='Asset type']"))
    if t:
        t[-1].click(); p.wait_for_timeout(1200)
        d.shot("pu_type_open")
        d.esc()
    send(d, HOME, "home")
    os.makedirs(os.path.join(HERE, "wf_inputs"), exist_ok=True)
    save_src(p, last_image(p), os.path.join(HERE, "wf_inputs", "home_screen.png"))
    json.dump({"chat_url": p.url}, open(os.path.join(HERE, "ui_chat.json"), "w"))
    d.buttons(120)

    # recipe: UI kit in this style, from the home-screen result
    pill = vis(p.get_by_role("button", name="UI kit in this style", exact=False))
    if not pill:
        mm = vis(p.get_by_role("button", name="More moves"))
        if mm:
            mm[-1].click(); p.wait_for_timeout(1000)
            d.shot("pu_more_moves")
        pill = vis(p.get_by_text("UI kit in this style", exact=True))
    if pill:
        pill[-1].click(); p.wait_for_timeout(2500)
        box = vis(p.locator("textarea"))[-1]
        if not box.input_value().strip():
            box.fill("PLAY, SHOP and SETTINGS buttons, a panel frame, a health bar, a coin badge, a close button")
            p.wait_for_timeout(600)
        d.shot("pu_kit_typed", hl=p.get_by_role("button", name="Send message"))
        before = p.get_by_text("Rate this result").count()
        box.press("Enter")
        wait_result(d, "kit", before)
        save_src(p, last_image(p), os.path.join(HERE, "wf_inputs", "ui_kit_sheet.png"))
    else:
        print("   UI kit recipe not found"); d.buttons(120)

    send(d, SHOP, "shop")
    save_src(p, last_image(p), os.path.join(HERE, "wf_inputs", "shop_screen.png"))
    send(d, SETTINGS, "settings")
    save_src(p, last_image(p), os.path.join(HERE, "wf_inputs", "settings_screen.png"))
    # gallery view of everything made
    d.shot("pu_gallery")


run([("flow", flow)])
