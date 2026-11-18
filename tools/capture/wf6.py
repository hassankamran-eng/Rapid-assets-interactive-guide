"""Workflows (prod): set variations = 2, Save, open Run window (do not confirm)."""
import json, os
from drv import run, HERE

EURL = json.load(open(os.path.join(HERE, "wf_editor.json")))["url"].replace("https://rapidassets.ai", "")


def vis(loc):
    return [loc.nth(i) for i in range(loc.count()) if loc.nth(i).is_visible()]


def flow(d):
    p = d.page
    d.go(EURL, wait=8000)
    vis(p.get_by_role("button", name="Settings for Variations"))[0].click()
    p.wait_for_timeout(1500)
    inp = p.locator("input").filter(has=p.locator("xpath=.")).all()
    box = None
    for lab in vis(p.get_by_text("Variations per item", exact=False)):
        cand = lab.locator("xpath=following::input[1]")
        if cand.count():
            box = cand.first; break
    if box:
        box.fill("2"); p.wait_for_timeout(800)
        d.shot("w_variations_set", hl=box)
    sv = vis(p.get_by_role("button", name="Save", exact=True))
    if sv:
        sv[0].click(); p.wait_for_timeout(2500)
        d.shot("w_saved")
    vis(p.get_by_role("button", name="Run", exact=True))[0].click()
    p.wait_for_timeout(4000)
    d.shot("w_run_dialog"); d.buttons(120)


run([("flow", flow)])
