"""Workflows (prod): template picker -> Batch Variations -> editor tour (no run)."""
import json, os
from drv import run, HERE

PURL = json.load(open(os.path.join(HERE, "wf_project.json")))["url"].replace("https://rapidassets.ai", "")


def vis(loc):
    return [loc.nth(i) for i in range(loc.count()) if loc.nth(i).is_visible()]


def flow(d):
    p = d.page
    d.go(PURL, wait=6000)
    vis(p.get_by_role("button", name="New workflow", exact=True))[0].click()
    p.wait_for_timeout(2000)
    d.shot("w_new_dialog", hl=vis(p.get_by_text("From template", exact=False))[0])
    vis(p.get_by_text("From template", exact=False))[0].click()
    p.wait_for_timeout(2000)
    card = vis(p.get_by_text("Batch Variations", exact=False))[0]
    card.click(); p.wait_for_timeout(1200)
    d.shot("w_templates", hl=card)
    d.buttons(40)
    use = vis(p.get_by_role("button", name="Use template"))
    use[0].click()
    p.wait_for_timeout(9000)
    print("   url:", p.url)
    json.dump({"url": p.url}, open(os.path.join(HERE, "wf_editor.json"), "w"))
    d.shot("w_editor")
    d.buttons(200)


run([("flow", flow)])
