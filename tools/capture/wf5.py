"""Workflows (prod): open Assets step settings + Variations settings + Add step palette (no run)."""
import json, os
from drv import run, HERE

EURL = json.load(open(os.path.join(HERE, "wf_editor.json")))["url"].replace("https://rapidassets.ai", "")


def vis(loc):
    return [loc.nth(i) for i in range(loc.count()) if loc.nth(i).is_visible()]


def flow(d):
    p = d.page
    d.go(EURL, wait=8000)
    vis(p.get_by_role("button", name="Image", exact=True))[0].click()
    p.wait_for_timeout(1500)
    d.shot("w_palette_image"); d.buttons(60)
    d.esc()
    vis(p.get_by_role("button", name="Settings for Assets"))[0].click()
    p.wait_for_timeout(2000)
    d.shot("w_assets_settings"); d.buttons(80)
    vis(p.get_by_role("button", name="Settings for Variations"))[0].click()
    p.wait_for_timeout(2000)
    d.shot("w_variations_settings"); d.buttons(80)


run([("flow", flow)])
