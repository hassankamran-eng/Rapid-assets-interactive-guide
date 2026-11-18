"""Free look: find the UI Kit run, print its text + why items were flagged. No runs."""
import json, os, re
from drv import run, HERE


def vis(loc):
    return [loc.nth(i) for i in range(loc.count()) if loc.nth(i).is_visible()]


def probe(d):
    p = d.page
    d.go("/workflows/runs", wait=7000)
    rows = p.evaluate("() => [...document.querySelectorAll('a')].map(a => [a.closest('tr,li,div')?.innerText.trim().replace(/\\s+/g,' ').slice(0,120), a.href]).filter(x => /\\/runs\\//.test(x[1]))")
    ui = [r for r in rows if r[0] and "UI Kit" in r[0]]
    for r in ui[:5]:
        print("RUN", r)
    if not ui:
        print(p.inner_text("body")[:1500]); return
    d.go(ui[0][1].replace("https://rapidassets.ai", ""), wait=7000)
    for b in vis(p.get_by_role("button", name="Got it")):
        try: b.click()
        except Exception: pass
    txt = p.inner_text("body")
    i = txt.find("Part 1")
    print("URL", p.url)
    print(txt[max(0, i - 200): i + 2500].replace("\n", " / "))
    # expand part 1 details
    el = vis(p.get_by_text(re.compile(r"Part 1")))
    if el:
        el[0].scroll_into_view_if_needed(); p.wait_for_timeout(1500)
        d.shot("_probe_ui_part1")


run([("probe", probe)])
