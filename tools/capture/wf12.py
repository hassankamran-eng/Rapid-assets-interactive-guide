"""Workflows (prod): Run -> files -> Check the cost -> Set up Style Spec in place (Describe it) -> lock -> run -> review -> export."""
import json, os
from drv import run, HERE

EURL = json.load(open(os.path.join(HERE, "wf_editor.json")))["url"].replace("https://rapidassets.ai", "")
FILES = [os.path.join(HERE, "wf_inputs", "knight_front.png"), os.path.join(HERE, "wf_inputs", "knight_walk.png")]


def vis(loc):
    return [loc.nth(i) for i in range(loc.count()) if loc.nth(i).is_visible()]


def btn(p, name, exact=True):
    b = vis(p.get_by_role("button", name=name, exact=exact))
    return b[0] if b else None


def flow(d):
    p = d.page
    d.go(EURL, wait=8000)
    btn(p, "Run").click(); p.wait_for_timeout(3000)
    p.get_by_role("dialog").last.locator("input[type=file]").first.set_input_files(FILES)
    p.wait_for_timeout(6000)
    d.shot("w_run_files", hl=btn(p, "Check the cost"))
    btn(p, "Check the cost").click(); p.wait_for_timeout(5000)
    sp = vis(p.get_by_text("Describe it", exact=True))
    if not sp:
        b = btn(p, "Set up Style Spec")
        if b:
            d.shot("w_run_spec_gate", hl=b); b.click(); p.wait_for_timeout(3000)
        sp = vis(p.get_by_text("Describe it", exact=True))
    print("   spec setup visible:", bool(sp), flush=True)
    sp[-1].click(); p.wait_for_timeout(1500)
    ta = vis(p.locator("textarea"))[-1]
    ta.fill("Bright hand-painted fantasy game art: chunky shapes, clean dark outlines, soft cel shading, warm palette, plain light background.")
    p.wait_for_timeout(500)
    d.shot("w_spec_describe")
    c = btn(p, "Continue") or btn(p, "Draft spec")
    c.click()
    for _ in range(45):
        p.wait_for_timeout(4000)
        if (btn(p, "Lock and use") or btn(p, "Lock it")):
            break
        sq = btn(p, "Skip questions")
        if sq:
            d.shot("w_spec_questions"); sq.click(); p.wait_for_timeout(2000); continue
        dr = btn(p, "Draft spec")
        if dr:
            dr.click()
    d.shot("w_spec_ready", hl=(btn(p, "Lock and use") or btn(p, "Lock it"))); d.buttons(40)
    (btn(p, "Lock and use") or btn(p, "Lock it")).click(); p.wait_for_timeout(6000)
    d.shot("w_spec_locked"); d.buttons(40)
    cc = btn(p, "Check the cost")
    if not cc:
        r = btn(p, "Run")
        if r:
            r.click(); p.wait_for_timeout(3000)
            p.get_by_role("dialog").last.locator("input[type=file]").first.set_input_files(FILES); p.wait_for_timeout(6000)
        cc = btn(p, "Check the cost")
    cc.click(); p.wait_for_timeout(6000)
    d.shot("w_run_cost"); d.buttons(40)
    for name in ("Run whole workflow", "Preview on 2 items first", "Run 2 items", "Run now", "Confirm and run", "Start run"):
        b = btn(p, name, exact=False)
        if b:
            print("   confirm:", name, flush=True); b.click(); break
    p.wait_for_timeout(8000)
    d.shot("w_run_started"); d.buttons(40)
    for k in range(30):
        p.wait_for_timeout(12000)
        if k == 3:
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
