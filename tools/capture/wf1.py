"""Workflows (prod): dashboard, New workflow menu and dialog (no credits)."""
from drv import run


def vis(loc):
    return [loc.nth(i) for i in range(loc.count()) if loc.nth(i).is_visible()]


def dash(d):
    p = d.page
    d.go("/workflows", wait=6000)
    for lab in ("Maybe later", "Not now", "Got it"):
        for b in vis(p.get_by_text(lab, exact=True)):
            try: b.click(); p.wait_for_timeout(600)
            except Exception: pass
    d.shot("w_dash")
    d.buttons(120)
    nb = vis(p.get_by_role("button", name="New workflow", exact=False))
    if nb:
        # the split button: open its menu (chevron is usually the last part)
        nb[-1].click(); p.wait_for_timeout(1500)
        d.shot("w_new_menu")
        d.buttons(140)
        d.esc()


run([("dash", dash)])
