"""Batch 6b: send the character prompt, approve the plan (8 credits) in the same session, capture the result."""
import json, os
from drv import run, HERE

URL = json.load(open(os.path.join(HERE, "demo.json")))["url"].replace("https://rapidassets.ai", "")
PROMPT = "a cheerful young knight hero with a blue cape and a round shield, full body, front view, T-pose, plain light background"


def vis(loc):
    return [loc.nth(i) for i in range(loc.count()) if loc.nth(i).is_visible()]


def approve(d):
    p = d.page
    d.go(URL, wait=7000)
    p.locator("textarea").first.fill(PROMPT)
    p.wait_for_timeout(600)
    p.get_by_role("button", name="Send message").click()
    yes = []
    for i in range(40):
        p.wait_for_timeout(4000)
        yes = vis(p.get_by_text("Yes, generate", exact=True))
        if yes:
            break
    p.wait_for_timeout(1500)
    d.shot("p2_plan_card", hl=yes[0])
    yes[0].click()
    p.wait_for_timeout(7000)
    d.shot("p2_working")
    for i in range(60):
        p.wait_for_timeout(5000)
        if vis(p.get_by_text("Rate this result")):
            break
    p.wait_for_timeout(5000)
    d.shot("p2_chat_result")
    d.buttons(150)


run([("approve", approve)])
