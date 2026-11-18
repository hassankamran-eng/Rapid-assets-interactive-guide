"""Rebuild the animate half of 'Rig & animate': prompt -> Animate -> plan -> watch -> Tune (Speed, Intensity,
Arm swing, Forward lean) -> quick buttons -> Locks -> fine-tune -> Check -> Save. Each step says what/where/when/how
and plays the real clip of that control being changed (owner's recording)."""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
f = os.path.join(HERE, "tour.template.html")
s = open(f, encoding="utf-8").read()

# 1) engine: hide the fake cursor on video steps (the clip has the real one), hold the step for the clip length
def rep(old, new):
    global s
    assert s.count(old) == 1, (old[:70], s.count(old))
    s = s.replace(old, new)
if "s.vid ? 0" not in s:
    rep('  cursor.style.opacity = mode === "try" ? 0 : 1;', '  cursor.style.opacity = (mode === "try" || s.vid) ? 0 : 1;')
if "s.dur" not in s:
    rep("  if (s.vid) read = Math.max(read, 8500);", "  if (s.vid) read = Math.max(read, (s.dur || 8.5) * 1000 + 600);")

# 2) replace every anim step after "Step 5 · Animate"
lines = s.split("\n")
keep, out, seen5 = [], [], False
for l in lines:
    if l.strip().startswith('{ch:"anim"'):
        if seen5:
            continue
        if 'title:"Step 5 · Animate"' in l:
            seen5 = True
    out.append(l)
s = "\n".join(out)

TUNE = [83.1, 53.6, 14.8, 16.2]          # whole Tune block
ROW = lambda y: [83.1, y, 14.8, 1.7]      # one slider row
LABEL = [69.8, 22.3, 12, 2.1]             # clip label above the character
NEW = [
 ('vc_play', None, "type", dict(t=[83.2, 29.4, 14.3, 6.2], box=[83.7, 30.1, 13.3, 1.9], fs=.62, z=1.8, type="make the character run"),
  "1 · Describe the move", "WHAT: say what the character should do, in plain words. WHERE: the Motion box, top right. WHEN: first, as soon as the Animation Studio opens. Or tap an example: Run, Jump, 3 punches, Wave, Idle."),
 ('vc_play', None, "click", dict(t=[83.4, 36.1, 13.9, 3.1], z=1.8, keep=True),
  "2 · Animate", "Click Animate. Leave Auto-check ticked so the result is checked for you."),
 ('vc_play', None, "look", dict(t=[83.2, 41.6, 14.2, 9], z=1.75),
  "3 · Read the plan", "The plan lists what will move (hips, torso, head, legs, arms, hands) and what stays still (hair, ears, face), worked out from your words."),
 ('vc_play', 'c_play', "look", dict(t=[24, 13, 46, 74], ring2=LABEL, z=1, dur=8),
  "4 · Watch the move", "The character runs in a loop. The label above it shows the clip: run · 0.80 s per loop · loops. This is the starting point you'll tune next."),
 ('vc_open', 'c_open', "click", dict(t=[83.2, 53.7, 14.6, 1.9], ring2=TUNE, z=1.6, dur=3.2),
  "5 · Open Tune", "WHERE: the Tune section, right under the plan. WHEN: the move is right but needs adjusting. Tuning is instant and uses no credits, no new prompt needed."),
 ('vc_speed', 'c_speed', "look", dict(t=ROW(56.1), ring2=LABEL, z=1.35, dur=9),
  "6 · Speed: faster or slower", "HOW: drag the Speed slider right to speed up, left to slow down (1.00× is normal). Here 1.65× makes each loop 0.48 s; 0.45× makes it 1.78 s. The label above the character shows the new speed. WHEN: the move feels too slow or too fast."),
 ('vc_intensity', 'c_intensity', "look", dict(t=ROW(57.4), z=1.7, dur=6),
  "7 · Intensity: bigger or smaller", "HOW: drag Intensity right for a bigger, more energetic movement (1.50), left for a smaller, calmer one (0.60). WHEN: the move is too stiff or too wild."),
 ('vc_arm', 'c_arm', "look", dict(t=ROW(58.7), z=1.7, dur=3.5),
  "8 · Arm swing", "HOW: drag Arm swing right for arms that swing more (1.35), left for less. WHEN: the arms look too stiff or too loose."),
 ('vc_lean', 'c_lean', "look", dict(t=ROW(60), z=1.7, dur=5),
  "9 · Forward lean", "HOW: drag Forward lean right to lean the body forward (1.90 gives a sprint), left to stand up straighter. WHEN: you want the run to feel faster or more relaxed."),
 ('vc_tuneall', None, "look", dict(t=[83.3, 64.2, 11.6, 4.6], ring2=[83.6, 61.7, 3, 1.6], z=1.7),
  "10 · Quick buttons and Reset", "Faster, Slower, Bigger motion and Loop it make the common changes in one click. Reset puts every slider back to 1.00."),
 ('vc_locks', 'c_locks', "look", dict(t=[11.8, 33.8, 12.6, 26.4], ring2=[16.8, 31.3, 3, 1.9], z=1.3, dur=12.5),
  "11 · Keep parts still (Locks)", "WHERE: Parts on the left › Locks. HOW: click a body part to switch it from Moves to Kept still; it turns grey. Here the right arm, right hand, left arm and left hand are locked, so the legs, hips and head run while the arms hold the shield. WHEN: a part must not move."),
 ('vc_speed2', 'c_speed2', "look", dict(t=ROW(56.1), ring2=LABEL, z=1.35, dur=4),
  "12 · Fine-tune again", "You can tune at any time, also after locking parts. Here Speed is set to 1.05× for the final take."),
 ('vc_check', 'c_check', "look", dict(t=[83.2, 35, 14.3, 30.5], ring2=[84.6, 68.4, 12.4, 10], z=1.35, dur=9),
  "13 · Check the result", "Check shows how far each part moved: the locked arms only 4°, the right leg 60°. \"The script moved Right arm 40°: the lock held it still.\" If a locked part still moves a little, click Fix (make right arm follow its own bones)."),
 ('vc_save', None, "look", dict(t=[83.4, 85.4, 14.2, 3.4], z=1.7),
  "14 · Save the clip", "Happy with it? Save to project · 150 credits adds the clip to this character, or Download GLB."),
]
def js(v):
    if isinstance(v, str): return '"' + v.replace('"', '\\"') + '"'
    if isinstance(v, bool): return "true" if v else "false"
    if isinstance(v, list): return "[" + ",".join(str(x) for x in v) + "]"
    return str(v)
steps = []
for img, vid, act, o, title, text in NEW:
    parts = [f'ch:"anim"', f'img:"{img}"'] + ([f'vid:"{vid}"'] if vid else []) + [f'act:"{act}"']
    for k in ("t", "ring2", "box", "fs", "z", "type", "keep", "dur"):
        if k in o: parts.append(f"{k}:{js(o[k])}")
    parts += [f"title:{js(title)}", f"text:{js(text)}"]
    steps.append(" {" + ", ".join(parts) + "},")
lines = s.split("\n")
i = max(k for k, l in enumerate(lines) if 'title:"Step 5 · Animate"' in l)
lines = lines[:i + 1] + steps + lines[i + 1:]
s = "\n".join(lines)
s = s.replace('{id:"anim", name:"Rig & animate", sub:"Rig, then animate by prompting"}', '{id:"anim", name:"Rig & animate", sub:"Rig, prompt, tune, lock, check"}')
open(f, "w", encoding="utf-8").write(s)
print("anim steps now:", s.count('{ch:"anim"'))
