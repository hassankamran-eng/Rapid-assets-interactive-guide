"""Re-capture clean result screens from each finished run page (free, no runs)."""
import glob, json, os, re
from drv import run, HERE

slug = lambda t: re.sub(r"[^a-z0-9]+", "_", t.lower()).strip("_")
R = {}
for f in glob.glob(os.path.join(HERE, "wfx_rects_*.json")):
    R.update(json.load(open(f)))


def vis(loc):
    return [loc.nth(i) for i in range(loc.count()) if loc.nth(i).is_visible()]


def one(d, name):
    p = d.page; s = slug(name); url = R[name].get("run_url", "")
    if "/runs/" not in url:
        print("   no run url:", name); return
    d.go(url.replace("https://rapidassets.ai", ""), wait=7000)
    for b in vis(p.get_by_role("button", name="Got it")):
        try: b.click()
        except Exception: pass
    d.esc()
    d.shot(f"y_{s}_result")
    imgs = vis(p.locator("main img"))
    if len(imgs) > 2:
        imgs[-1].scroll_into_view_if_needed(); p.wait_for_timeout(1500)
        d.shot(f"y_{s}_outputs")


names = [n for n in R if "/runs/" in R[n].get("run_url", "")]
print("templates:", len(names), flush=True)
run([(slug(n), (lambda d, n=n: one(d, n))) for n in names])
