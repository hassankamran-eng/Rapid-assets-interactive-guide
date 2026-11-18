"""Batch 8 (credits): sprite key frame (11) + Make it 3D on the knight (35), viewer + download menu."""
import json, os
from drv import run, HERE

URL = json.load(open(os.path.join(HERE, "demo.json")))["url"].replace("https://rapidassets.ai", "")


def vis(loc):
    return [loc.nth(i) for i in range(loc.count()) if loc.nth(i).is_visible()]


def key_frame(d):
    p = d.page
    d.go(URL, wait=6000)
    vis(p.locator("button[aria-label^='Open Image']"))[0].hover()
    p.wait_for_timeout(800)
    p.locator("button[aria-label^='Make a sprite sheet from']").first.click(force=True)
    p.wait_for_timeout(4000)
    mk = vis(p.get_by_text("Make key frame", exact=False))[-1]
    d.shot("p2_sprite_setup", hl=mk)
    mk.click()
    for i in range(40):
        p.wait_for_timeout(5000)
        if vis(p.get_by_text("Approve the key frame", exact=False)):
            break
    p.wait_for_timeout(3000)
    d.shot("p2_sprite_keyframe")
    d.buttons(60)


def make_3d(d):
    p = d.page
    d.go(URL, wait=6000)
    if not vis(p.get_by_text("Rate this result")):
        p.locator("button[aria-label^='Chat history']").first.click()
        p.wait_for_timeout(1500)
        vis(p.get_by_text("Cheerful Young Knight", exact=False))[-1].click()
        p.wait_for_timeout(7000)
    m3 = vis(p.get_by_role("button", name="Make it 3D, about 35 credits"))[0]
    d.shot("p3_make_it_3d_pill", hl=m3)
    m3.click()
    p.wait_for_timeout(2000)
    box = p.locator("textarea").first
    box.fill("Make it 3D")
    p.wait_for_timeout(600)
    d.shot("p3_make_it_3d_armed", hl=p.get_by_role("button", name="Send message"))
    box.press("Enter")
    p.wait_for_timeout(8000)
    yes = vis(p.get_by_text("Yes, generate", exact=True))
    if yes:
        d.shot("p3_plan_card_3d", hl=yes[0])
        yes[0].click()
    p.wait_for_timeout(15000)
    d.shot("p3_building")
    for i in range(80):
        p.wait_for_timeout(6000)
        if vis(p.locator("button[aria-label^='Open 3D']")) or vis(p.get_by_text("Rig it", exact=False)):
            break
    p.wait_for_timeout(6000)
    d.shot("p3_chat_result")
    d.buttons(80)


run([("key_frame", key_frame), ("make_3d", make_3d)])
