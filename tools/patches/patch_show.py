"""Show the second prompt (already typed) in the motion box on the 'arms stay still' screen."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
f = os.path.join(HERE, "tour.template.html")
s = open(f, encoding="utf-8").read()

def rep(old, new_):
    global s
    assert s.count(old) == 1, (old[:70], s.count(old))
    s = s.replace(old, new_)

rep('{ch:"anim", img:"v_lock_arms", act:"look", t:[83.3,42.6,14.9,8.4],',
    '{ch:"anim", img:"v_lock_arms", act:"look", show:{box:[83.6,30.2,14.3,4.9], fs:.62, text:"/*PROMPT2*/"}, t:[83.3,42.6,14.9,8.4],')
rep('  await setShot(s.img);                if (!alive(id)) return;',
    '  await setShot(s.img);                if (!alive(id)) return;\n'
    '  if (s.show) { pct(typer, s.show.box); typer.style.fontSize = `calc(var(--u) * ${s.show.fs || 1})`; typer.classList.add("wrap"); typed.textContent = s.show.text; typer.classList.add("on"); }')
open(f, "w", encoding="utf-8").write(s)
print("ok")
