"""Reorder chapters (CH) and steps (STEPS) in tour.template.html to the owner's order."""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
f = os.path.join(HERE, "tour.template.html")
s = open(f, encoding="utf-8").read()
ORDER = ["start", "first", "controls", "3d", "anim", "view", "rec", "wf", "sprites"]

# chapters
a = s.index("const CH = [") + len("const CH = [")
b = s.index("];", a)
ch_lines = [l for l in s[a:b].split("\n") if l.strip().startswith("{id:")]
by_id = {re.search(r'id:"([^"]+)"', l).group(1): l.rstrip().rstrip(",") + "," for l in ch_lines}
extra = [k for k in by_id if k not in ORDER]
ids = [k for k in ORDER if k in by_id] + extra
s = s[:a] + "\n" + "\n".join("  " + by_id[k].strip() for k in ids) + "\n" + s[b:]

# steps: each step is one line starting with ' {ch:"'
a = s.index("const STEPS = [") + len("const STEPS = [")
b = s.index("];", a)
body = s[a:b]
steps = [l for l in body.split("\n") if l.strip().startswith("{ch:")]
groups = {}
for l in steps:
    c = re.search(r'ch:"([^"]+)"', l).group(1)
    groups.setdefault(c, []).append(" " + l.strip().rstrip(",") + ",")
out = []
for k in ids:
    if k in groups:
        out += groups[k] + [""]
s = s[:a] + "\n" + "\n".join(out) + "\n" + s[b:]
open(f, "w", encoding="utf-8").write(s)
print("chapters:", ids, "| steps:", sum(len(v) for v in groups.values()), "| lost:", len(steps) - sum(len(groups[k]) for k in ids if k in groups))
