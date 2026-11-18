"""Real run of each workflow template on prod, with screenshots + element rectangles (% of viewport).
usage: python wfx_run.py "<Template A>" "<Template B>" ..."""
import json, os, re, sys, time
from drv import run, HERE

PURL = json.load(open(os.path.join(HERE, "wf_project.json")))["url"].replace("https://rapidassets.ai", "")
FRONT = os.path.join(HERE, "wf_inputs", "knight_front.png")
WALK = os.path.join(HERE, "wf_inputs", "knight_walk.png")
CAT = r"C:\Users\Hassan\Desktop\3D Models\tripo-cost-test\A-standard\cat.glb"
INPUTS = {
    "Background Removal": ([FRONT], None, None),
    "Character Facial Pose Sheet": ([FRONT], None, None),
    "Character Turnaround": ([FRONT], None, None),
    "Color Palette Extraction": ([FRONT], None, None),
    "Image Analysis": ([FRONT], None, None),
    "Icon Set": ([FRONT], None, "Shop currency and rewards: gold coin, gem, potion, key, treasure chest, shield"),
    "Parallel Pose Edits": ([FRONT], None, None),
    "Parallel Image Variations": ([FRONT], None, None),
    "Pose Transfer": ([FRONT], [WALK], None),
    "Seasonal Re-theme": ([FRONT], None, "Winter: snow on the armour and cape, frosty blue light"),
    "Texture 3D Model": ([CAT], [FRONT], None),
    "Tileset": ([FRONT], None, "Grass with small stones and a dirt path, top-down"),
    "UI Kit": ([FRONT], None, "Fantasy RPG menu with PLAY, SHOP and SETTINGS buttons"),
}
BEFORE_RUN = None
slug = lambda t: re.sub(r"[^a-z0-9]+", "_", t.lower()).strip("_")
RECTS = os.path.join(HERE, "wfx_rects_" + slug(sys.argv[1]) + ".json")


def vis(loc):
    return [loc.nth(i) for i in range(loc.count()) if loc.nth(i).is_visible()]


def btn(p, name, exact=True, scope=None):
    b = vis((scope or p).get_by_role("button", name=name, exact=exact))
    return b[-1] if b else None


def rect(p, loc):
    try:
        bb = loc.bounding_box(); vw, vh = p.viewport_size["width"], p.viewport_size["height"]
        return [round(bb["x"] / vw * 100, 1), round(bb["y"] / vh * 100, 1), round(bb["width"] / vw * 100, 1), round(bb["height"] / vh * 100, 1)]
    except Exception:
        return None


def one(d, name):
    p = d.page; s = slug(name); R = {}
    allr = json.load(open(RECTS)) if os.path.exists(RECTS) else {}
    log = lambda *a: print(f"   [{name}]", *a, flush=True)
    d.go(PURL, wait=6000)
    btn(p, "New workflow").click(); p.wait_for_timeout(2000)
    dlg = p.get_by_role("dialog").last
    vis(dlg.get_by_text("From template", exact=False))[0].click(); p.wait_for_timeout(2000)
    sr = vis(dlg.get_by_placeholder("Search templates", exact=False))
    if sr:
        sr[0].fill(name.split()[0]); p.wait_for_timeout(1500)
    card = vis(dlg.get_by_text(name, exact=True)) or vis(dlg.get_by_text(name.split()[0], exact=False))
    card = card[0]
    card.scroll_into_view_if_needed(); card.click(); p.wait_for_timeout(1000)
    R["card"] = rect(p, card); d.shot(f"y_{s}_card", hl=card)
    btn(p, "Use template").click(); p.wait_for_timeout(9000)
    for b in vis(p.get_by_role("button", name="Got it")):
        try: b.click()
        except Exception: pass
    fit = btn(p, "Fit view")
    if fit: fit.click(); p.wait_for_timeout(1500)
    canvas = vis(p.locator(".react-flow__nodes, .react-flow"))
    R["canvas"] = rect(p, canvas[0]) if canvas else None
    R["run_btn"] = rect(p, btn(p, "Run"))
    d.shot(f"y_{s}_editor")
    if BEFORE_RUN: BEFORE_RUN()
    btn(p, "Run").click(); p.wait_for_timeout(3500)
    dlg = p.get_by_role("dialog").last
    R["dialog"] = rect(p, dlg)
    files, second, theme = INPUTS[name]
    fi = dlg.locator("input[type=file]")
    fi.nth(0).set_input_files(files); p.wait_for_timeout(5000)
    if second:
        fi = dlg.locator("input[type=file]")
        fi.nth(fi.count() - 1).set_input_files(second); p.wait_for_timeout(5000)
    if theme:
        ta = vis(dlg.locator("textarea"))
        if ta:
            ta[0].fill(theme); p.wait_for_timeout(500); R["theme"] = rect(p, ta[0])
    cc = btn(p, "Check the cost")
    R["check"] = rect(p, cc)
    d.shot(f"y_{s}_inputs", hl=cc)
    cc.click(); p.wait_for_timeout(6000)
    lc = btn(p, "Lock and continue") or btn(p, "Lock and use")
    if lc:
        log("lock spec"); lc.click(); p.wait_for_timeout(7000)
    dlg = p.get_by_role("dialog").last
    go = btn(p, "Run", scope=dlg) or btn(p, "Run", exact=False, scope=dlg)
    R["cost_dialog"] = rect(p, dlg); R["confirm"] = rect(p, go) if go else None
    try:
        R["cost_text"] = dlg.inner_text()[:400]
    except Exception:
        pass
    d.shot(f"y_{s}_cost", hl=go)
    log("cost:", (R.get("cost_text") or "").replace("\n", " / ")[:220])
    if os.environ.get("RECTS_ONLY"):
        allr[name] = R; json.dump(allr, open(RECTS, "w"), indent=1); log("rects saved (no run)"); return
    go.click(); p.wait_for_timeout(9000)
    for b in vis(p.get_by_role("button", name="Got it")):
        try: b.click()
        except Exception: pass
    R["run_url"] = p.url
    d.shot(f"y_{s}_running")
    t0 = time.time()
    while time.time() - t0 < 480:
        p.wait_for_timeout(10000)
        txt = p.inner_text("body")
        if "Running ·" not in txt and "Running" not in txt.split("\n")[0:40].__str__():
            break
    p.wait_for_timeout(4000)
    for b in vis(p.get_by_role("button", name="Got it")):
        try: b.click()
        except Exception: pass
    st = vis(p.get_by_text(re.compile(r"\d+ of \d+ (finished|steps finished)")))
    R["status"] = rect(p, st[0]) if st else None
    dl = vis(p.get_by_text("Downloads", exact=True))
    R["downloads"] = rect(p, dl[0]) if dl else None
    d.shot(f"y_{s}_result")
    head = p.inner_text("body")[:600].replace("\n", " / ")
    log("after run:", head[:260])
    keeps = vis(p.get_by_role("button", name=re.compile("^Keep this result")))
    if keeps:
        R["keep"] = rect(p, keeps[0])
        d.shot(f"y_{s}_review", hl=keeps[0])
        for k in keeps:
            try: k.click(); p.wait_for_timeout(800)
            except Exception: pass
        p.wait_for_timeout(3000)
        for nm in ("Collect", "Export"):
            ro = vis(p.get_by_role("button", name=f"Run options for {nm}"))
            if ro:
                ro[0].click(); p.wait_for_timeout(1000)
                rf = vis(p.get_by_text("Run from here", exact=True))
                if rf:
                    rf[0].click(); p.wait_for_timeout(3000)
                    cf = btn(p, "Run", scope=p.get_by_role("dialog").last) if vis(p.get_by_role("dialog")) else None
                    if cf: cf.click()
                    break
        t1 = time.time()
        while time.time() - t1 < 240:
            p.wait_for_timeout(10000)
            if "Running" not in p.inner_text("body")[:800]:
                break
        p.wait_for_timeout(4000)
        d.shot(f"y_{s}_result")
    # scroll to the outputs of the main (non-input) step and capture
    imgs = vis(p.locator("main img"))
    if len(imgs) > 2:
        imgs[-1].scroll_into_view_if_needed(); p.wait_for_timeout(1500)
        d.shot(f"y_{s}_outputs")
    allr[name] = R
    json.dump(allr, open(RECTS, "w"), indent=1)


if __name__ == "__main__":
    run([(slug(t), (lambda d, t=t: one(d, t))) for t in sys.argv[1:]])
