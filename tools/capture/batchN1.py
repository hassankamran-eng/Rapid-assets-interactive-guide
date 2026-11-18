"""New UI (localhost:7071, dev): create the demo project and look at the Studio layout."""
import json, os
from drv import run, HERE

def create(d):
    p = d.page
    d.go("/studio?newProject=1", wait=5000)
    d.shot("n_new_project")
    d.buttons(60)
    inp = p.locator("input").first
    inp.fill("Guide Book Demo")
    p.wait_for_timeout(500)
    btn = [b for b in [p.get_by_role("button", name="Create and open")] if b.count()]
    if btn:
        btn[0].first.click()
    else:
        inp.press("Enter")
    p.wait_for_timeout(9000)
    print("   url:", p.url)
    json.dump({"url": p.url}, open(os.path.join(HERE, "demo_dev.json"), "w"))
    d.shot("n_studio_first")
    d.buttons(120)

run([("create", create)])
