"""Batch 4: Style Spec setup in the demo project (free)."""
import json, os
from drv import run, HERE

URL = json.load(open(os.path.join(HERE, "demo.json")))["url"].replace("https://rapidassets.ai", "")


def spec(d):
    p = d.page
    d.go(URL, wait=6000)
    p.get_by_text("Start from a style", exact=True).first.click()
    p.wait_for_timeout(2000)
    d.shot("p2_spec_presets")
    p.get_by_text("Hand-Painted", exact=True).first.click()
    p.wait_for_timeout(1500)
    d.buttons()
    cont = p.get_by_text("Continue with").first
    cont.scroll_into_view_if_needed()
    d.shot("p2_spec_continue", hl=cont)
    cont.click()
    for i in range(12):
        p.wait_for_timeout(5000)
        if p.get_by_role("button", name="Draft spec").count():
            break
    d.shot("p2_spec_questions")
    def vis(loc):
        return [loc.nth(i) for i in range(loc.count()) if loc.nth(i).is_visible()]
    for i in range(10):
        nxt = vis(p.get_by_role("button", name="Next", exact=True))
        if not nxt:
            break
        nxt[0].click()
        p.wait_for_timeout(1500)
    d.shot("p2_spec_after_questions")
    d.buttons()
    draft = vis(p.get_by_role("button", name="Draft spec"))[0]
    d.shot("p2_spec_draft_button", hl=draft)
    draft.click()
    for i in range(30):
        p.wait_for_timeout(5000)
        if p.get_by_role("button", name="Lock it").count():
            break
    d.shot("p2_spec_draft_ready", hl=p.get_by_role("button", name="Lock it").first)
    p.get_by_role("button", name="Lock it").first.click()
    p.wait_for_timeout(5000)
    d.shot("p2_spec_locked")
    d.buttons()


run([("spec", spec)])
