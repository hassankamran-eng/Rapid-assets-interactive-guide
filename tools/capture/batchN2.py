"""New UI (localhost:7071, dev): T-pose -> remove background -> make it 3D, all by prompting the Agent chat on the right."""
import json, os
from drv import run, HERE

URL = json.load(open(os.path.join(HERE, "demo_dev.json")))["url"].split("7071", 1)[1]
TPOSE = "a knight hero, full body, front view, T-pose with arms straight out, plain light background"


def vis(loc):
    return [loc.nth(i) for i in range(loc.count()) if loc.nth(i).is_visible()]


def send_and_approve(d, text, tag, wait_done_s, done_check):
    p = d.page
    box = vis(p.locator("textarea"))[-1]
    box.fill(text)
    p.wait_for_timeout(700)
    d.shot(f"n_{tag}_typed", hl=p.get_by_role("button", name="Send message"))
    box.press("Enter")
    yes = []
    for _ in range(45):
        p.wait_for_timeout(4000)
        yes = vis(p.get_by_text("Yes, generate", exact=True))
        if yes:
            break
    p.wait_for_timeout(1500)
    if not yes:
        d.shot(f"n_{tag}_noplan"); d.buttons(80)
        return False
    d.shot(f"n_{tag}_plan", hl=yes[0])
    yes[0].click()
    p.wait_for_timeout(9000)
    d.shot(f"n_{tag}_working")
    for _ in range(wait_done_s // 6):
        p.wait_for_timeout(6000)
        if done_check(p):
            break
    p.wait_for_timeout(7000)
    d.shot(f"n_{tag}_result")
    d.buttons(100)
    return True


def flow(d):
    p = d.page
    d.go(URL, wait=7000)
    s = vis(p.get_by_text("Skip for now", exact=True))
    if s:
        s[-1].click()
        p.wait_for_timeout(3500)
    t = vis(p.locator("button[aria-label^='Asset type']"))
    if t:
        t[-1].click(); p.wait_for_timeout(1000)
        c = vis(p.get_by_text("Character", exact=True))
        if c:
            c[-1].click(); p.wait_for_timeout(1000)
    d.shot("n_ready", hl=vis(p.locator("textarea"))[-1])

    rated = lambda: p.get_by_text("Rate this result").count()
    r0 = rated()
    if not send_and_approve(d, TPOSE, "tpose", 240, lambda pg: pg.get_by_text("Rate this result").count() > r0):
        return
    r1 = rated()
    if not send_and_approve(d, "remove the background", "rmbg", 180, lambda pg: pg.get_by_text("Rate this result").count() > r1):
        return
    send_and_approve(d, "make it 3D", "3d", 600,
                     lambda pg: bool(vis(pg.get_by_text("Rig it", exact=False))) or pg.locator("button[aria-label^='Open 3D']").count() > 0)


if __name__ == "__main__":
    run([("flow", flow)])
