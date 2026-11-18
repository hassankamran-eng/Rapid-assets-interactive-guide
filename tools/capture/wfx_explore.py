"""Open every workflow template (prod), screenshot card + editor + Run inputs. No runs, no credits.
usage: python wfx_explore.py <start> <end>   (template index range)"""
import json, os, re, sys
from drv import run, HERE

PURL = json.load(open(os.path.join(HERE, "wf_project.json")))["url"].replace("https://rapidassets.ai", "")
TEMPLATES = ["Batch Variations", "Background Removal", "Character Facial Pose Sheet", "Character Turnaround",
             "Color Palette Extraction", "Icon Set", "Image Analysis", "Parallel Pose Edits",
             "Parallel Image Variations", "Pose Transfer", "Seasonal Re-theme", "Texture 3D Model", "Tileset", "UI Kit"]
slug = lambda t: re.sub(r"[^a-z0-9]+", "_", t.lower()).strip("_")
MAP = os.path.join(HERE, "wfx_map_" + sys.argv[1] + ".json")


def vis(loc):
    return [loc.nth(i) for i in range(loc.count()) if loc.nth(i).is_visible()]


def one(d, name):
    p = d.page; s = slug(name)
    d.go(PURL, wait=6000)
    vis(p.get_by_role("button", name="New workflow", exact=True))[0].click(); p.wait_for_timeout(2000)
    vis(p.get_by_text("From template", exact=False))[0].click(); p.wait_for_timeout(2000)
    card = vis(p.get_by_text(name, exact=True))[0]
    card.scroll_into_view_if_needed(); card.click(); p.wait_for_timeout(1000)
    d.shot(f"x_{s}_card", hl=card)
    vis(p.get_by_role("button", name="Use template"))[0].click(); p.wait_for_timeout(9000)
    for lab in ("Got it",):
        for b in vis(p.get_by_role("button", name=lab)):
            try: b.click()
            except Exception: pass
    fit = vis(p.get_by_role("button", name="Fit view"))
    if fit: fit[0].click(); p.wait_for_timeout(1200)
    d.shot(f"x_{s}_editor")
    m = json.load(open(MAP)) if os.path.exists(MAP) else {}
    m[name] = {"editor": p.url}
    vis(p.get_by_role("button", name="Run", exact=True))[0].click(); p.wait_for_timeout(3500)
    d.shot(f"x_{s}_inputs")
    dlg = p.get_by_role("dialog").last
    info = {"text": dlg.inner_text()[:900], "files": dlg.locator("input[type=file]").count(),
            "textareas": dlg.locator("textarea").count(), "inputs": dlg.locator("input:not([type=file])").count()}
    m[name]["run"] = info
    json.dump(m, open(MAP, "w"), indent=1)
    print("   ", name, "| files", info["files"], "| textareas", info["textareas"], "| inputs", info["inputs"], "|", info["text"][:300].replace("\n", " / "), flush=True)
    d.esc()


a, b = int(sys.argv[1]), int(sys.argv[2])
run([(slug(t), (lambda d, t=t: one(d, t))) for t in TEMPLATES[a:b]])
