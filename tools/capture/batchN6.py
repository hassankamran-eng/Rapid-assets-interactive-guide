"""New UI (dev): Animation Studio — wait for prompt 1 to finish, then prompt 2, wait, then Check."""
from drv import run
from batchN2 import vis
from batchN3 import dismiss
from batchN4 import open_chat, P2


def wait_written(p, limit_s=420):
    for _ in range(limit_s // 5):
        p.wait_for_timeout(5000)
        if not vis(p.get_by_text("Writing the motion", exact=False)):
            return True
    return False


def anim(d):
    p = d.page
    open_chat(d)
    vis(p.locator("button[aria-label^='Open 3D model']"))[0].click()
    p.wait_for_timeout(9000); dismiss(p)
    vis(p.get_by_role("button", name="Animate", exact=True))[0].click()
    p.wait_for_timeout(15000); dismiss(p)
    print("   writing?", bool(vis(p.get_by_text("Writing the motion", exact=False))), flush=True)
    wait_written(p)
    p.wait_for_timeout(4000)
    d.shot("n_anim_result1")
    box = [t for t in vis(p.locator("textarea")) if "motion" in (t.get_attribute("placeholder") or "").lower()] or vis(p.locator("textarea"))
    box = box[0]
    box.fill(P2)
    p.wait_for_timeout(700)
    go = vis(p.get_by_role("button", name="Animate", exact=True))
    d.shot("n_anim_prompt2", hl=go[-1])
    go[-1].click()
    p.wait_for_timeout(6000)
    d.shot("n_anim_working2")
    wait_written(p)
    p.wait_for_timeout(5000)
    d.shot("n_anim_result2")
    c = vis(p.get_by_text("Check", exact=True))
    if c:
        c[-1].click(); p.wait_for_timeout(2500)
        d.shot("n_anim_check")
    d.buttons(80)


run([("anim", anim)])
