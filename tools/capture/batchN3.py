"""New UI (dev): reopen the T-pose chat, dismiss pop-ups, then prompt 'remove the background' and 'make it 3D'."""
import json, os
from drv import run, HERE
from batchN2 import vis, send_and_approve, URL


def dismiss(p):
    for label in ("Maybe later", "Not now", "Got it"):
        for b in vis(p.get_by_text(label, exact=True)):
            try:
                b.click(); p.wait_for_timeout(800)
            except Exception:
                pass


def flow(d):
    p = d.page
    d.go(URL, wait=7000)
    dismiss(p)
    if not vis(p.get_by_text("Rate this result")):
        p.locator("button[aria-label^='Chat history']").last.click()
        p.wait_for_timeout(1500)
        vis(p.get_by_text("knight hero", exact=False))[-1].click()
        p.wait_for_timeout(8000)
        dismiss(p)
    d.shot("n_tpose_result")
    r1 = p.get_by_text("Rate this result").count()
    if not send_and_approve(d, "remove the background", "rmbg", 180, lambda pg: pg.get_by_text("Rate this result").count() > r1):
        return
    dismiss(p); d.shot("n_rmbg_result")
    send_and_approve(d, "make it 3D", "3d", 600,
                     lambda pg: pg.locator("button[aria-label^='Open 3D']").count() > 0 or bool(vis(pg.get_by_text("Rig it", exact=False))))
    dismiss(p); d.shot("n_3d_result")


if __name__ == "__main__":
    run([("flow", flow)])
