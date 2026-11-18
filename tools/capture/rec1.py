"""Recipes (prod): from the knight result, run Turnaround, Expressions, Poses, Icon set, UI kit; capture armed + plan + result."""
import json, os
from drv import run, HERE

URL = json.load(open(os.path.join(HERE, "demo.json")))["url"].replace("https://rapidassets.ai", "")
RECIPES = [("Turnaround", "r_turnaround", None), ("Expressions", "r_expressions", "4 expressions: happy, angry, surprised, sad"),
           ("Poses", "r_poses", "standing, running, jumping, attacking"),
           ("Icon set in this style", "r_iconset", None), ("UI kit in this style", "r_uikit", None)]


def vis(loc):
    return [loc.nth(i) for i in range(loc.count()) if loc.nth(i).is_visible()]


def dismiss(p):
    for lab in ("Maybe later", "Not now", "Got it"):
        for b in vis(p.get_by_text(lab, exact=True)):
            try: b.click(); p.wait_for_timeout(500)
            except Exception: pass


def open_knight(d):
    p = d.page
    d.go(URL, wait=7000); dismiss(p)
    p.locator("button[aria-label^='Chat history']").first.click(); p.wait_for_timeout(1500)
    vis(p.get_by_text("Cheerful Young Knight", exact=False))[-1].click(); p.wait_for_timeout(8000); dismiss(p)


def one(d, label, tag, extra):
    p = d.page
    open_knight(d)
    # first knight result's pill (scroll to top result)
    pills = vis(p.get_by_role("button", name=label, exact=False))
    if not pills:
        mm = vis(p.get_by_role("button", name="More moves"))
        if mm: mm[0].click(); p.wait_for_timeout(800)
        pills = vis(p.get_by_text(label, exact=True))
    pills[0].click(); p.wait_for_timeout(2500)
    box = p.locator("textarea").first
    if extra:
        box.fill(extra); p.wait_for_timeout(500)
    d.shot(f"{tag}_armed", hl=p.get_by_role("button", name="Send message"))
    d.buttons(40)
    rated = p.get_by_text("Rate this result").count()
    box.press("Enter")
    yes = []
    for _ in range(40):
        p.wait_for_timeout(4000)
        yes = vis(p.get_by_text("Yes, generate", exact=True))
        if yes: break
    if yes:
        p.wait_for_timeout(1500); d.shot(f"{tag}_plan", hl=yes[0]); yes[0].click()
    for _ in range(60):
        p.wait_for_timeout(5000)
        if p.get_by_text("Rate this result").count() > rated: break
    p.wait_for_timeout(7000); dismiss(p)
    d.shot(f"{tag}_result")


steps = [(tag, (lambda d, l=label, t=tag, e=extra: one(d, l, t, e))) for label, tag, extra in RECIPES]
run(steps)
