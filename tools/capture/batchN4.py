"""New UI (dev): Rig it from the chat, rig, Bones; then Animate by prompting (two prompts)."""
from drv import run
from batchN2 import vis, URL
from batchN3 import dismiss

P1 = "Run in place in a steady loop: knees up, arms swinging, a slight forward lean. Keep the shield arm still."
P2 = "Make it faster with bigger strides, and keep both arms and hands still."


def open_chat(d):
    p = d.page
    d.go(URL, wait=7000)
    dismiss(p)
    if not vis(p.get_by_role("button", name="Rig it (recommended)")):
        p.locator("button[aria-label^='Chat history']").last.click()
        p.wait_for_timeout(1500)
        vis(p.get_by_text("Knight Hero", exact=False))[-1].click()
        p.wait_for_timeout(8000)
        dismiss(p)


def rig(d):
    p = d.page
    open_chat(d)
    r = vis(p.get_by_role("button", name="Rig it (recommended)"))
    d.shot("n_rigit_chat", hl=r[-1])
    r[-1].click()
    p.wait_for_timeout(7000)
    dismiss(p)
    rc = vis(p.get_by_role("button", name="Rig character"))
    d.shot("n_rig_view", hl=rc[0] if rc else None)
    d.buttons(80)
    rc[0].click()
    p.wait_for_timeout(6000)
    d.shot("n_rigging")
    for _ in range(70):
        p.wait_for_timeout(6000)
        if vis(p.get_by_text("Rigged ✓", exact=False)) or vis(p.get_by_text("Rigging finished", exact=False)):
            break
    p.wait_for_timeout(5000)
    b = vis(p.get_by_role("button", name="Bones", exact=False))
    if b:
        b[0].click(); p.wait_for_timeout(2500)
    dismiss(p)
    d.shot("n_rigged")
    d.buttons(80)


def animate(d):
    p = d.page
    a = vis(p.get_by_role("button", name="Animate", exact=True)) or vis(p.get_by_text("Animate", exact=True))
    if not a:
        open_chat(d)
        a = vis(p.get_by_role("button", name="Animate", exact=True))
    a[0].click()
    p.wait_for_timeout(14000)
    dismiss(p)
    d.shot("n_anim_open")
    d.buttons(120)
    box = [t for t in vis(p.locator("textarea")) if "motion" in (t.get_attribute("placeholder") or "").lower()]
    box = box[0] if box else vis(p.locator("textarea"))[0]
    for k, prompt in ((1, P1), (2, P2)):
        box.fill(prompt)
        p.wait_for_timeout(700)
        go = vis(p.get_by_role("button", name="Animate", exact=True))
        d.shot(f"n_anim_prompt{k}", hl=go[-1] if go else None)
        go[-1].click()
        p.wait_for_timeout(5000)
        d.shot(f"n_anim_working{k}")
        for _ in range(40):
            p.wait_for_timeout(5000)
            if vis(p.get_by_text("Moving:", exact=False)) and not vis(p.get_by_text("Animating", exact=False)):
                break
        p.wait_for_timeout(8000)
        dismiss(p)
        d.shot(f"n_anim_result{k}")
    d.buttons(120)


run([("rig", rig), ("animate", animate)])
