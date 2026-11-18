"""UI Kit workflow on prod with the Studio home screen as Style reference. Waits for the whole run, keeps flagged
items, re-runs skipped steps, captures every part, saves the parts to the Library and shoots the Gallery.
Shots y_ui_kit_* (+ y_ui_kit_part<N>), rects -> wfx_rects_ui_kit.json."""
import json, os, re, time
from drv import run, HERE

PURL = json.load(open(os.path.join(HERE, "wf_project.json")))["url"].replace("https://rapidassets.ai", "")
HOME = os.path.join(HERE, "wf_inputs", "home_screen.png")
THEME = "Fantasy RPG menu: carved wood and gold frames with blue gems, matching the home screen"
RECTS = os.path.join(HERE, "wfx_rects_ui_kit.json")
NAME = "UI Kit"


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


def got_it(p):
    for b in vis(p.get_by_role("button", name="Got it")):
        try: b.click()
        except Exception: pass


def status(p):
    t = p.inner_text("main") if p.locator("main").count() else p.inner_text("body")
    m = re.search(r"(\d+) of (\d+) finished", t)
    return (int(m.group(1)) if m else -1), ("Running" in t[:3000]), ("waiting for review" in t), t


def wait_run(p, log, limit=900):
    t0, last, same = time.time(), None, 0
    while time.time() - t0 < limit:
        p.wait_for_timeout(15000)
        n, running, review, _ = status(p)
        log(f"{int(time.time()-t0)}s finished={n} running={running} review={review}")
        same = same + 1 if n == last else 0; last = n
        if not running and same >= 2:
            return
        if n == 21:
            return


def one(d):
    p = d.page; R = {}
    log = lambda *a: print("   [ui]", *a, flush=True)
    d.go(PURL, wait=6000)
    btn(p, "New workflow").click(); p.wait_for_timeout(2000)
    dlg = p.get_by_role("dialog").last
    vis(dlg.get_by_text("From template", exact=False))[0].click(); p.wait_for_timeout(2000)
    sr = vis(dlg.get_by_placeholder("Search templates", exact=False))
    if sr:
        sr[0].fill("UI"); p.wait_for_timeout(1500)
    card = vis(dlg.get_by_text(NAME, exact=True))[0]
    card.scroll_into_view_if_needed(); card.click(); p.wait_for_timeout(1000)
    R["card"] = rect(p, card); d.shot("y_ui_kit_card", hl=card)
    btn(p, "Use template").click(); p.wait_for_timeout(9000); got_it(p)
    fit = btn(p, "Fit view")
    if fit: fit.click(); p.wait_for_timeout(1500)
    canvas = vis(p.locator(".react-flow__nodes, .react-flow"))
    R["canvas"] = rect(p, canvas[0]) if canvas else None
    R["run_btn"] = rect(p, btn(p, "Run"))
    d.shot("y_ui_kit_editor")
    btn(p, "Run").click(); p.wait_for_timeout(3500)
    dlg = p.get_by_role("dialog").last
    R["dialog"] = rect(p, dlg)
    dlg.locator("input[type=file]").nth(0).set_input_files([HOME]); p.wait_for_timeout(6000)
    ta = vis(dlg.locator("textarea"))
    if ta:
        ta[0].fill(THEME); p.wait_for_timeout(500); R["theme"] = rect(p, ta[0])
    cc = btn(p, "Check the cost"); R["check"] = rect(p, cc)
    d.shot("y_ui_kit_inputs", hl=cc)
    cc.click(); p.wait_for_timeout(6000)
    lc = btn(p, "Lock and continue") or btn(p, "Lock and use")
    if lc:
        log("lock spec"); lc.click(); p.wait_for_timeout(7000)
    dlg = p.get_by_role("dialog").last
    go = btn(p, "Run", scope=dlg) or btn(p, "Run", exact=False, scope=dlg)
    R["cost_dialog"] = rect(p, dlg); R["confirm"] = rect(p, go) if go else None
    R["cost_text"] = dlg.inner_text()[:400]
    d.shot("y_ui_kit_cost", hl=go)
    log("cost:", R["cost_text"].replace("\n", " / ")[:220])
    go.click(); p.wait_for_timeout(12000); got_it(p)
    R["run_url"] = p.url
    json.dump({NAME: R}, open(RECTS, "w"), indent=1)
    d.shot("y_ui_kit_running")
    wait_run(p, log)
    got_it(p)
    keeps = vis(p.get_by_role("button", name=re.compile("^Keep this result")))
    if keeps:
        R["keep"] = rect(p, keeps[0]); keeps[0].scroll_into_view_if_needed(); p.wait_for_timeout(800)
        R["keep"] = rect(p, keeps[0])
        d.shot("y_ui_kit_review", hl=keeps[0])
        for k in keeps:
            try: k.click(); p.wait_for_timeout(1200)
            except Exception: pass
        p.wait_for_timeout(3000)
        # re-run whatever was skipped after a flagged part, then Export
        for _ in range(4):
            heads = p.evaluate("""() => [...document.querySelectorAll('button[aria-label^="Run options for"]')]
               .map(b => [b.getAttribute('aria-label'), (b.closest('section,li,article,div[class*=card]')||b.parentElement).innerText.includes('Skipped')])""")
            todo = [h[0] for h in heads if h[1]]
            log("skipped steps:", todo)
            if not todo:
                break
            ro = vis(p.get_by_role("button", name=todo[0]))
            if not ro: break
            ro[0].click(); p.wait_for_timeout(1000)
            rf = vis(p.get_by_text("Run from here", exact=True))
            if not rf: d.esc(); break
            rf[0].click(); p.wait_for_timeout(3000)
            if vis(p.get_by_role("dialog")):
                cf = btn(p, "Run", scope=p.get_by_role("dialog").last)
                if cf: cf.click()
            p.wait_for_timeout(5000)
            wait_run(p, log, 420)
    p.evaluate("() => window.scrollTo(0, 0)"); p.wait_for_timeout(1500)
    n, _, _, txt = status(p)
    log("final:", txt[:400].replace("\n", " / "))
    st = vis(p.get_by_text(re.compile(r"\d+ of \d+ finished")))
    R["status"] = rect(p, st[0]) if st else None
    dl = vis(p.get_by_text("Downloads", exact=True))
    R["downloads"] = rect(p, dl[0]) if dl else None
    d.shot("y_ui_kit_result")
    # every part, one screen each (card rect recorded for the camera)
    R["parts"] = {}
    for k in range(1, 10):
        h = vis(p.get_by_text(re.compile(rf"^Part {k}:")))
        if not h: continue
        h[0].scroll_into_view_if_needed(); p.evaluate("() => window.scrollBy(0, -160)"); p.wait_for_timeout(1500)
        lab = h[0].inner_text().strip()
        card = h[0].locator("xpath=ancestor::*[.//img][1]")
        R["parts"][k] = {"label": lab, "rect": rect(p, card.first) if card.count() else None}
        d.shot(f"y_ui_kit_part{k}")
    # Save to Library, then the Gallery shows the whole kit together
    p.evaluate("() => window.scrollTo(0, 0)"); p.wait_for_timeout(1000)
    sv = btn(p, "Save") or btn(p, "Save", exact=False)
    if sv:
        sv.scroll_into_view_if_needed(); p.wait_for_timeout(600)
        R["save"] = rect(p, sv); d.shot("y_ui_kit_save", hl=sv)
        sv.click(); p.wait_for_timeout(6000); got_it(p)
        d.shot("y_ui_kit_saved")
    json.dump({NAME: R}, open(RECTS, "w"), indent=1)


def gallery(d):
    p = d.page
    d.go("/gallery", wait=8000); got_it(p)
    d.shot("y_ui_kit_gallery")
    d.buttons(60)


run([("ui_kit", one), ("gallery", gallery)])
