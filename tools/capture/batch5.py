"""Batch 5: skip the Style Spec, then the chat composer menus (no credits)."""
import json, os
from drv import run, HERE

URL = json.load(open(os.path.join(HERE, "demo.json")))["url"].replace("https://rapidassets.ai", "")


def vis(loc):
    return [loc.nth(i) for i in range(loc.count()) if loc.nth(i).is_visible()]


def skip(d):
    p = d.page
    d.go(URL, wait=6000)
    s = vis(p.get_by_text("Skip for now", exact=True))
    if not s:
        b = vis(p.get_by_role("button", name="Back to the setup choices"))
        if b:
            b[0].click(); p.wait_for_timeout(1500)
        s = vis(p.get_by_text("Skip for now", exact=True))
    if s:
        s[0].click()
        p.wait_for_timeout(3000)
    d.shot("p2_studio_ready", hl=p.locator("textarea").first)
    d.buttons()


def plus(d):
    p = d.page
    p.get_by_role("button", name="Add", exact=True).first.click()
    p.wait_for_timeout(1200)
    d.shot("p2_plus_menu")
    d.buttons(120)
    d.esc()


def type_picker(d):
    p = d.page
    p.get_by_role("button", name="Asset type: Any").first.click()
    p.wait_for_timeout(1000)
    d.shot("p2_type_picker")
    d.esc()


def mode(d):
    p = d.page
    p.get_by_role("button", name="Generation mode: Plan").first.click()
    p.wait_for_timeout(1000)
    d.shot("p1_mode_pill")
    d.buttons(120)
    d.esc()


def recipes(d):
    p = d.page
    p.get_by_role("button", name="Recipes").first.click()
    p.wait_for_timeout(2500)
    d.shot("p2_recipes")
    d.esc()


run([("skip", skip), ("plus", plus), ("type_picker", type_picker), ("mode", mode), ("recipes", recipes)])
