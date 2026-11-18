"""Workflows (prod): project workflows page -> New workflow dialog -> templates (no credits)."""
import json, os
from drv import run, HERE


def vis(loc):
    return [loc.nth(i) for i in range(loc.count()) if loc.nth(i).is_visible()]


def flow(d):
    p = d.page
    d.go("/workflows", wait=6000)
    vis(p.get_by_role("button", name="New workflow", exact=True))[0].click()
    p.wait_for_timeout(1500)
    vis(p.get_by_text("Guide Book Demo", exact=True))[-1].click()
    p.wait_for_timeout(500)
    vis(p.get_by_role("button", name="Continue"))[0].click()
    p.wait_for_timeout(3000)
    d.shot("w_spec_prompt", hl=vis(p.get_by_text("Skip for now", exact=True))[-1])
    vis(p.get_by_text("Skip for now", exact=True))[-1].click()
    p.wait_for_timeout(2500)
    print("   url:", p.url)
    json.dump({"url": p.url}, open(os.path.join(HERE, "wf_project.json"), "w"))
    d.shot("w_project_page"); d.buttons(60)
    nb = vis(p.get_by_role("button", name="New workflow", exact=True))
    if nb:
        nb[0].click(); p.wait_for_timeout(2000)
        d.shot("w_new_dialog"); d.buttons(80)
        t = vis(p.get_by_text("From template", exact=False))
        if t:
            t[0].click(); p.wait_for_timeout(2000)
            d.shot("w_templates"); d.buttons(140)


run([("flow", flow)])
