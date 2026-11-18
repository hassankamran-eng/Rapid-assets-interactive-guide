"""Batch 6: Type picker, a character prompt in Plan mode, plan card, approve (~8 credits), result."""
import json, os
from drv import run, HERE

URL = json.load(open(os.path.join(HERE, "demo.json")))["url"].replace("https://rapidassets.ai", "")
PROMPT = "a cheerful young knight hero with a blue cape and a round shield, full body, front view, T-pose, plain light background"


def vis(loc):
    return [loc.nth(i) for i in range(loc.count()) if loc.nth(i).is_visible()]


def make(d):
    p = d.page
    d.go(URL, wait=6000)
    vis(p.locator("button[aria-label^='Asset type']"))[0].click()
    p.wait_for_timeout(1200)
    d.shot("p2_type_picker")
    vis(p.get_by_text("Character", exact=True))[0].click()
    p.wait_for_timeout(1200)
    box = p.locator("textarea").first
    box.fill(PROMPT)
    p.wait_for_timeout(800)
    d.shot("p2_prompt_typed", hl=p.get_by_role("button", name="Send message"))
    p.get_by_role("button", name="Send message").click()
    for i in range(40):
        p.wait_for_timeout(5000)
        if vis(p.get_by_role("button", name="Yes, generate")):
            break
    p.wait_for_timeout(1500)
    d.shot("p2_plan_card", hl=vis(p.get_by_role("button", name="Yes, generate"))[0])
    vis(p.get_by_role("button", name="Yes, generate"))[0].click()
    p.wait_for_timeout(8000)
    d.shot("p2_working")
    for i in range(60):
        p.wait_for_timeout(5000)
        if vis(p.get_by_text("Rate this result")) or vis(p.get_by_text("further", exact=False)):
            break
    p.wait_for_timeout(4000)
    d.shot("p2_chat_result")
    d.buttons(150)


run([("make", make)])
