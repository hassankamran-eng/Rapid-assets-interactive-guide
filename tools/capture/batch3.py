"""Batch 3: create the demo project, Studio first screen + Style Spec setup."""
import json, os
from drv import run, HERE


def create(d):
    d.go("/studio?newProject=1", wait=4000)
    d.page.locator("input").first.fill("Guide Book Demo")
    d.page.wait_for_timeout(400)
    d.shot("p1_new_project", hl=d.page.get_by_role("button", name="Create and open"))
    d.page.get_by_role("button", name="Create and open").click()
    d.page.wait_for_timeout(9000)
    print("   url:", d.page.url)
    json.dump({"url": d.page.url}, open(os.path.join(HERE, "demo.json"), "w"))
    d.shot("p2_studio_first")
    d.buttons()


run([("create", create)])
