"""Let a step play a looping video clip over its screenshot (step.vid = clip name in VIDS)."""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
f = os.path.join(HERE, "tour.template.html")
s = open(f, encoding="utf-8").read()

def rep(old, new):
    global s
    assert s.count(old) == 1, (old[:70], s.count(old))
    s = s.replace(old, new)

if 'id="clip"' not in s:
    rep('<img class="shot" id="shotB" alt="">', '<img class="shot" id="shotB" alt="">\n          <video class="shot" id="clip" muted loop playsinline preload="auto"></video>')
    rep("const IMG = /*IMAGES*/{};", "const IMG = /*IMAGES*/{};\nconst VIDS = /*VIDS*/{};")
    rep('  await setShot(s.img);                if (!alive(id)) return;',
        '  await setShot(s.img);                if (!alive(id)) return;\n'
        '  { const v = $("clip");\n'
        '    if (s.vid && VIDS[s.vid]) { if (v.dataset.k !== s.vid) { v.src = VIDS[s.vid]; v.dataset.k = s.vid; } v.currentTime = 0; v.play().catch(() => {}); v.classList.add("on"); }\n'
        '    else { v.classList.remove("on"); v.pause(); } }')
    rep("function finish() {", 'function finish() {\n  $("clip").classList.remove("on"); $("clip").pause();')

# attach clips to the animation steps
def add_vid(title, clip):
    global s
    m = re.search(r'( \{ch:"anim", img:"[^"]+", )([^\n]*title:"' + re.escape(title) + '")', s)
    if m and 'vid:' not in m.group(0):
        s = s.replace(m.group(0), m.group(1) + f'vid:"{clip}", ' + m.group(2), 1)
        return True
    return bool(m)

print("Play it:", add_vid("Play it", "clip_run"))
print("Arms still:", add_vid("The arms stay still", "clip_arms"))
open(f, "w", encoding="utf-8").write(s)
