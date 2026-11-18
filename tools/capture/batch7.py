"""Batch 7: free screens around the knight image."""
import json, os
from drv import run, HERE

URL = json.load(open(os.path.join(HERE, "demo.json")))["url"].replace("https://rapidassets.ai", "")


def vis(loc):
    return [loc.nth(i) for i in range(loc.count()) if loc.nth(i).is_visible()]


def open_chat(d):
    p = d.page
    d.go(URL, wait=7000)
    if not vis(p.get_by_text("Rate this result")):
        p.locator("button[aria-label^='Chat history']").first.click()
        p.wait_for_timeout(1500)
        d.shot("p1_chat_history")
        vis(p.get_by_text("Cheerful Young Knight", exact=False))[-1].click()
        p.wait_for_timeout(7000)


def more_moves(d):
    p = d.page
    open_chat(d)
    vis(p.get_by_role("button", name="More moves"))[0].click()
    p.wait_for_timeout(1000)
    d.shot("p2_more_moves")
    d.esc()


def redo(d):
    p = d.page
    vis(p.get_by_role("button", name="Redo, about 8 credits"))[0].click()
    for i in range(15):
        p.wait_for_timeout(2000)
        if vis(p.get_by_text("Improved from your original prompt", exact=False)):
            break
    d.shot("p2_redo_dialog")
    vis(p.get_by_role("button", name="Cancel"))[0].click()
    p.wait_for_timeout(800)


def tile_hover(d):
    p = d.page
    t = vis(p.locator("button[aria-label^='Open Image']"))[0]
    t.hover()
    p.wait_for_timeout(800)
    d.shot("p2_media_hover")


def viewer(d):
    p = d.page
    vis(p.locator("button[aria-label^='Open Image']"))[0].click()
    p.wait_for_timeout(3000)
    d.shot("p2_viewer")
    dl = vis(p.get_by_role("dialog").get_by_role("button", name="Download"))
    if dl:
        dl[0].click()
        p.wait_for_timeout(1000)
        d.shot("p2_viewer_download")
        d.esc()
    d.esc()


def edit_view(d):
    p = d.page
    vis(p.locator("button[aria-label^='Edit image']"))[0].click()
    p.wait_for_timeout(5000)
    d.shot("p2_edit_view")
    d.buttons(150)


def sprites(d):
    p = d.page
    d.go(URL, wait=6000)
    vis(p.locator("button[aria-label^='Open Image']"))[0].hover()
    p.wait_for_timeout(800)
    p.locator("button[aria-label^='Make a sprite sheet from']").first.click(force=True)
    p.wait_for_timeout(5000)
    d.shot("p2_sprite_setup")
    d.buttons(150)


run([("more_moves", more_moves), ("redo", redo), ("sprites", sprites)])
