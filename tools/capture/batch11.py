"""Batch 11: re-shoot the finished sprite key frame (free)."""
import json, os
from drv import run, HERE

URL = json.load(open(os.path.join(HERE, "demo.json")))["url"].replace("https://rapidassets.ai", "")


def vis(loc):
    return [loc.nth(i) for i in range(loc.count()) if loc.nth(i).is_visible()]


def kf(d):
    p = d.page
    d.go(URL, wait=6000)
    vis(p.get_by_role("button", name="Sprites", exact=True))[0].click()
    p.wait_for_timeout(4000)
    d.shot("p2_sprite_list")
    w = vis(p.get_by_text("Walk", exact=False))
    if w:
        w[0].click()
        p.wait_for_timeout(6000)
    d.shot("p2_sprite_keyframe")
    d.buttons(40)


run([("kf", kf)])
