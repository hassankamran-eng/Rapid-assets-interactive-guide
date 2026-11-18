"""Workflows (prod): Run -> files -> Check the cost -> Lock and continue -> cost -> confirm -> run -> review -> export."""
import json, os
from drv import run, HERE

EURL = json.load(open(os.path.join(HERE, "wf_editor.json")))["url"].replace("https://rapidassets.ai", "")
FILES = [os.path.join(HERE, "wf_inputs", "knight_front.png"), os.path.join(HERE, "wf_inputs", "knight_walk.png")]


def vis(loc):
    return [loc.nth(i) for i in range(loc.count()) if loc.nth(i).is_visible()]


def btn(p, name, exact=True):
    b = vis(p.get_by_role("button", name=name, exact=exact))
    return b[-1] if b else None


def flow(d):
    p = d.page
    d.go(EURL, wait=8000)
    btn(p, "Run").click(); p.wait_for_timeout(3000)
    p.get_by_role("dialog").last.locator("input[type=file]").first.set_input_files(FILES)
    p.wait_for_timeout(6000)
    btn(p, "Check the cost").click(); p.wait_for_timeout(5000)
    lc = btn(p, "Lock and continue") or btn(p, "Lock and use")
    if lc:
        d.shot("w_spec_lock_continue", hl=lc); lc.click(); p.wait_for_timeout(8000)
    d.shot("w_run_cost"); d.buttons(50)
    for name in ("Run whole workflow", "Preview on 2 items first", "Run 2 items", "Run now", "Confirm and run", "Start run", "Run"):
        b = btn(p, name, exact=False)
        if b:
            print("   confirm:", name, flush=True); b.click(); break
    p.wait_for_timeout(8000)
    print("   url:", p.url, flush=True)
    d.shot("w_run_started"); d.buttons(50)
    for k in range(22):
        p.wait_for_timeout(12000)
        if k == 2:
            d.shot("w_run_progress")
        if btn(p, "Accept batch", exact=False) or vis(p.get_by_role("button", name="Approve")):
            break
    p.wait_for_timeout(4000)
    d.shot("w_run_review"); d.buttons(60)
    for b in vis(p.get_by_role("button", name="Approve", exact=True))[:4]:
        try: b.click(); p.wait_for_timeout(600)
        except Exception: pass
    a = btn(p, "Accept batch", exact=False)
    if a:
        a.click(); p.wait_for_timeout(4000); d.shot("w_run_accepted")
    e = btn(p, "Export", exact=False)
    if e:
        e.click(); p.wait_for_timeout(2000); d.shot("w_run_export"); d.buttons(40)


run([("flow", flow)])
