"""Workflows (prod): More-ways menu, New workflow dialog, templates, then open a Blank workflow editor (no credits)."""
from drv import run


def vis(loc):
    return [loc.nth(i) for i in range(loc.count()) if loc.nth(i).is_visible()]


def dismiss(p):
    for lab in ("Maybe later", "Not now", "Got it"):
        for b in vis(p.get_by_text(lab, exact=True)):
            try: b.click(); p.wait_for_timeout(600)
            except Exception: pass


def flow(d):
    p = d.page
    d.go("/workflows", wait=6000); dismiss(p)
    vis(p.get_by_role("button", name="More ways to create a workflow"))[0].click()
    p.wait_for_timeout(1200)
    d.shot("w_more_menu"); d.buttons(30)
    d.esc()
    vis(p.get_by_role("button", name="New workflow", exact=True))[0].click()
    p.wait_for_timeout(1500)
    vis(p.get_by_text("Guide Book Demo", exact=True))[-1].click()
    p.wait_for_timeout(600)
    d.shot("w_which_project", hl=vis(p.get_by_role("button", name="Continue"))[0])
    vis(p.get_by_role("button", name="Continue"))[0].click()
    p.wait_for_timeout(2500)
    d.shot("w_new_dialog"); d.buttons(80)
    t = vis(p.get_by_text("From template", exact=False))
    if t:
        t[0].click(); p.wait_for_timeout(2000)
        d.shot("w_templates"); d.buttons(120)


run([("flow", flow)])
