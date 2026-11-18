"""Batch 10: rig the knight (40 credits), Bones view, then the full Animation Studio."""
import json, os
from drv import run, HERE

URL = json.load(open(os.path.join(HERE, "demo.json")))["url"].replace("https://rapidassets.ai", "")


def vis(loc):
    return [loc.nth(i) for i in range(loc.count()) if loc.nth(i).is_visible()]


def rig(d):
    p = d.page
    d.go(URL, wait=6000)
    vis(p.locator("button[aria-label^='Open 3D model']"))[0].click()
    p.wait_for_timeout(8000)
    g = vis(p.get_by_role("button", name="Got it"))
    if g:
        g[0].click(); p.wait_for_timeout(800)
    vis(p.get_by_role("button", name="Rig it (recommended)"))[0].click()
    p.wait_for_timeout(7000)
    d.buttons(80)
    rc = vis(p.get_by_role("button", name="Rig character"))
    d.shot("p4_rig_view", hl=rc[0])
    rc[0].click()
    p.wait_for_timeout(5000)
    d.shot("p4_rigging")
    for i in range(70):
        p.wait_for_timeout(6000)
        if vis(p.get_by_text("Rigged ✓", exact=False)) or vis(p.get_by_text("Rigging finished", exact=False)):
            break
    p.wait_for_timeout(6000)
    b = vis(p.get_by_role("button", name="Bones", exact=False)) or vis(p.get_by_text("Bones", exact=True))
    if b:
        b[0].click()
        p.wait_for_timeout(3000)
    d.shot("p4_rigged")
    d.buttons(80)


def anim(d):
    p = d.page
    d.go(URL, wait=6000)
    vis(p.locator("button[aria-label^='Open 3D model']"))[0].click()
    p.wait_for_timeout(8000)
    vis(p.get_by_role("button", name="Animate", exact=True))[0].click()
    p.wait_for_timeout(15000)
    d.shot("p4_anim_studio")
    d.buttons(120)


run([("rig", rig), ("anim", anim)])
