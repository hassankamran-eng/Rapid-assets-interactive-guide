"""Workflows (prod): Run with 2 files -> Check the cost -> run -> run page -> review -> export."""
import json, os
from drv import run, HERE

EURL = json.load(open(os.path.join(HERE, "wf_editor.json")))["url"].replace("https://rapidassets.ai", "")
FILES = [os.path.join(HERE, "wf_inputs", "knight_front.png"), os.path.join(HERE, "wf_inputs", "knight_walk.png")]


def vis(loc):
    return [loc.nth(i) for i in range(loc.count()) if loc.nth(i).is_visible()]


def click_first(p, names):
    for n in names:
        b = vis(p.get_by_role("button", name=n, exact=False))
        if b:
            b[0].click(); return n
    return None


def flow(d):
    p = d.page
    d.go(EURL, wait=8000)
    vis(p.get_by_role("button", name="Run", exact=True))[0].click()
    p.wait_for_timeout(3000)
    p.get_by_role("dialog").last.locator("input[type=file]").first.set_input_files(FILES)
    p.wait_for_timeout(6000)
    d.shot("w_run_files", hl=vis(p.get_by_role("button", name="Check the cost"))[0])
    vis(p.get_by_role("button", name="Check the cost"))[0].click()
    p.wait_for_timeout(6000)
    d.shot("w_run_cost"); d.buttons(60)
    hit = click_first(p, ["Run whole workflow", "Run 2", "Confirm", "Run now", "Start run", "Run"])
    print("   clicked:", hit, flush=True)
    p.wait_for_timeout(8000)
    print("   url:", p.url, flush=True)
    d.shot("w_run_started"); d.buttons(60)
    for k in range(40):
        p.wait_for_timeout(15000)
        txt = p.inner_text("body")
        if k in (2, 6):
            d.shot(f"w_run_progress{k}")
        if any(s in txt for s in ("Accept batch", "Review", "Approve", "Finished", "Completed", "Done ·")):
            if "Approve" in txt or "Accept batch" in txt:
                break
    p.wait_for_timeout(5000)
    d.shot("w_run_review"); d.buttons(80)
    for b in vis(p.get_by_role("button", name="Approve", exact=True))[:4]:
        try: b.click(); p.wait_for_timeout(700)
        except Exception: pass
    d.shot("w_run_approved"); d.buttons(60)
    if click_first(p, ["Accept batch"]):
        p.wait_for_timeout(4000)
        d.shot("w_run_accepted")
    if click_first(p, ["Export"]):
        p.wait_for_timeout(2000)
        d.shot("w_run_export"); d.buttons(60)
        d.esc()


run([("flow", flow)])
