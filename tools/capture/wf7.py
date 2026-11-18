"""Workflows (prod): Run -> From Library -> pick 2 images -> Check the cost (stop there)."""
import json, os
from drv import run, HERE

EURL = json.load(open(os.path.join(HERE, "wf_editor.json")))["url"].replace("https://rapidassets.ai", "")


def vis(loc):
    return [loc.nth(i) for i in range(loc.count()) if loc.nth(i).is_visible()]


def flow(d):
    p = d.page
    d.go(EURL, wait=8000)
    vis(p.get_by_role("button", name="Run", exact=True))[0].click()
    p.wait_for_timeout(3000)
    d.shot("w_run_dialog", hl=vis(p.get_by_role("button", name="From Library"))[0])
    vis(p.get_by_role("button", name="From Library"))[0].click()
    p.wait_for_timeout(4000)
    d.shot("w_library"); d.buttons(60)
    dlg = p.get_by_role("dialog").last
    tiles = [t for t in vis(dlg.locator("button:has(img), [role=checkbox]:has(img), [role=option]:has(img)"))]
    print("   tiles:", len(tiles), flush=True)
    for t in tiles[:2]:
        t.click(); p.wait_for_timeout(700)
    d.shot("w_library_picked"); d.buttons(60)


run([("flow", flow)])
