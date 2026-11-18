"""Batch 9: 3D viewer + download menu, rig (40 credits), Animation Studio, Tools pages with the demo project open."""
import json, os
from drv import run, HERE

URL = json.load(open(os.path.join(HERE, "demo.json")))["url"].replace("https://rapidassets.ai", "")


def vis(loc):
    return [loc.nth(i) for i in range(loc.count()) if loc.nth(i).is_visible()]


def viewer3d(d):
    p = d.page
    d.go(URL, wait=6000)
    vis(p.locator("button[aria-label^='Open 3D model']"))[0].click()
    p.wait_for_timeout(9000)
    d.shot("p3_viewer")
    d.buttons(80)
    dl = vis(p.get_by_role("button", name="Download", exact=False))
    if dl:
        dl[-1].click()
        p.wait_for_timeout(1500)
        d.shot("p3_download_menu")
        d.esc()


def rig(d):
    p = d.page
    r = vis(p.get_by_text("Rig it", exact=False))
    r[0].click()
    p.wait_for_timeout(6000)
    rc = vis(p.get_by_text("Rig character", exact=True))
    d.shot("p4_rig_view", hl=rc[0] if rc else None)
    d.buttons(80)
    rc[0].click()
    for i in range(60):
        p.wait_for_timeout(6000)
        if vis(p.get_by_text("Rigged", exact=False)) and not vis(p.get_by_text("Rigging…", exact=False)):
            break
    p.wait_for_timeout(5000)
    b = vis(p.get_by_text("Bones", exact=True))
    if b:
        b[0].click()
        p.wait_for_timeout(2500)
    d.shot("p4_rigged")


def anim(d):
    p = d.page
    a = vis(p.get_by_role("button", name="Animate", exact=False)) or vis(p.get_by_text("Animate", exact=True))
    a[0].click()
    p.wait_for_timeout(12000)
    d.shot("p4_anim_studio")
    d.buttons(100)


def tools(d):
    p = d.page
    for path, name in (("/manual/image-generation", "p2_tools_image"), ("/manual/image-editing", "p2_tools_edit"), ("/manual/3d-generator", "p3_tools_3d")):
        d.go(path, wait=5000)
        g = vis(p.get_by_text("Guide Book Demo", exact=True))
        if g and vis(p.get_by_text("Choose a project", exact=False)):
            g[-1].click()
            p.wait_for_timeout(4000)
        d.shot(name)


run([("viewer3d", viewer3d), ("rig", rig), ("anim", anim), ("tools", tools)])
