"""Batch 12: from the chat, prompt 'remove the background' (3 credits) and 'make it 3D' (plan card only, not approved)."""
import json, os
from drv import run, HERE

URL = json.load(open(os.path.join(HERE, "demo.json")))["url"].replace("https://rapidassets.ai", "")


def vis(loc):
    return [loc.nth(i) for i in range(loc.count()) if loc.nth(i).is_visible()]


def chat(d):
    p = d.page
    d.go(URL, wait=6000)
    p.locator("button[aria-label^='Chat history']").first.click()
    p.wait_for_timeout(1500)
    vis(p.get_by_text("Cheerful Young Knight", exact=False))[-1].click()
    p.wait_for_timeout(8000)
    d.shot("p3c_chat_before")
    rated = p.get_by_text("Rate this result").count()

    box = p.locator("textarea").first
    box.fill("remove the background")
    p.wait_for_timeout(600)
    d.shot("p3c_rmbg_typed", hl=p.get_by_role("button", name="Send message"))
    box.press("Enter")
    yes = []
    for i in range(40):
        p.wait_for_timeout(4000)
        yes = vis(p.get_by_text("Yes, generate", exact=True))
        if yes:
            break
    p.wait_for_timeout(1500)
    if yes:
        d.shot("p3c_plan_rmbg", hl=yes[0])
        yes[0].click()
    else:
        d.shot("p3c_after_rmbg_send")
    for i in range(50):
        p.wait_for_timeout(5000)
        if p.get_by_text("Rate this result").count() > rated:
            break
    p.wait_for_timeout(6000)
    d.shot("p3c_rmbg_result")
    d.buttons(60)

    box = p.locator("textarea").first
    box.fill("make it 3D")
    p.wait_for_timeout(600)
    d.shot("p3c_3d_typed", hl=p.get_by_role("button", name="Send message"))
    box.press("Enter")
    for i in range(40):
        p.wait_for_timeout(4000)
        if vis(p.get_by_text("Yes, generate", exact=True)) or vis(p.get_by_text("Would you like", exact=False)):
            break
    p.wait_for_timeout(2500)
    d.shot("p3c_plan_3d")
    d.buttons(60)


run([("chat", chat)])
