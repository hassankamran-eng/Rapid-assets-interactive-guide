"""Tour: animation chapter done only by prompting (no sliders, quick buttons or lock toggles)."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
f = os.path.join(HERE, "tour.template.html")
s = open(f, encoding="utf-8").read()

a = s.index(' {ch:"anim", img:"p3_viewer", act:"click", t:[59.4')
b = s.index('];', a)
new = r''' {ch:"anim", img:"p3_viewer", act:"click", t:[59.4,21.5,10.8,3.9], z:1.35, title:"Step 4 · Rig it", text:"A model needs a skeleton before it can move."},
 {ch:"anim", img:"p4_rig_view", act:"look", t:[71.6,88.6,20.2,4.7], z:1.35, title:"Body and skeleton", text:"biped for a T-pose person or humanoid; quadruped for four legs, and more."},
 {ch:"anim", img:"p4_rig_view", act:"click", t:[88.3,93.3,10.4,4.3], z:1.35, title:"Rig character", text:"40 credits. It takes a minute or two."},
 {ch:"anim", img:"p4_rigged", act:"click", t:[71.3,14.4,7,3.7], z:1.35, title:"Rigged ✓", text:"Turn on Bones and check the arms and legs have bones."},
 {ch:"anim", img:"p3_viewer", act:"click", t:[81.8,21.5,7.5,3.9], z:1.35, title:"Step 5 · Animate", text:"Click Animate. The Animation Studio opens and the chat folds away."},
 {ch:"anim", img:"v_motion", act:"type", wrap:true, t:[83.3,29.8,14.9,5.6], box:[83.6,30.2,14.3,4.9], fs:.62, z:1.9, type:"/*PROMPT*/", title:"Describe the whole move in one prompt", text:"Say what the character does, how fast and how big, and which parts stay still. The AI plans the body parts from your words."},
 {ch:"anim", img:"v_motion", act:"click", keep:true, t:[83.3,36.2,14.9,2.8], z:1.9, title:"Animate", text:"Click Animate. Leave Auto-check on so the result is checked for you."},
 {ch:"anim", img:"v_motion", act:"look", keep:true, t:[83.3,42,14.9,9], z:1.9, title:"It plans from your prompt", text:"The plan shows what will move and what stays still, worked out from what you wrote: Moving: Hips, Torso, Head, legs… Keeping still: Hair / ears / face."},
 {ch:"anim", img:"v_running", act:"look", t:[26.6,87.3,42,2.8], z:1.3, title:"Play it", text:"Play the move with the timeline. The label above shows the clip, its length and that it loops."},
 {ch:"anim", img:"v_motion", act:"type", wrap:true, t:[83.3,29.8,14.9,5.6], box:[83.6,30.2,14.3,4.9], fs:.62, z:1.9, type:"/*PROMPT2*/", title:"Change it by prompting", text:"Not quite right? Write what to change in plain words: faster, bigger, calmer, or keep a part still."},
 {ch:"anim", img:"v_motion", act:"click", keep:true, t:[83.3,36.2,14.9,2.8], z:1.9, title:"Animate again", text:"Click Animate. A new take is made from your words; the old one is replaced in the preview."},
 {ch:"anim", img:"v_lock_arms", act:"look", t:[83.3,42.6,14.9,8.4], ring2:[48.3,36.5,12,17.5], z:1.35, title:"The arms stay still", text:"The plan now keeps the arms and hands still, and the character's arms stay put while the legs and hips move."},
 {ch:"anim", img:"v_check", act:"look", t:[83.2,21.6,15,56.5], z:1.35, title:"Step 6 · Check", text:"Auto-check tests the move: feet on the ground, knees bend the right way, parts kept still. If something is off, say what to fix in a new prompt, or click the Fix button it offers."},
 {ch:"anim", img:"v_motion", act:"look", t:[83.3,85.6,14.9,2.8], z:1.8, title:"Save the clip", text:"Happy with it? Save to project · 150 credits, or Download GLB."},
'''
s = s[:a] + new + s[b:]

def rep(old, new_):
    global s
    assert s.count(old) == 1, (old[:70], s.count(old))
    s = s.replace(old, new_)

rep('{id:"anim", name:"Rig & animate", sub:"Rig, prompt, tune, lock, check"}', '{id:"anim", name:"Rig & animate", sub:"Rig, then animate by prompting"}')
rep('.typer.on{opacity:1}', '.typer.on{opacity:1}\n.typer.wrap{white-space:pre-wrap;align-items:flex-start;line-height:1.35;padding:.25em .35em;overflow:hidden}')
rep('  typer.style.fontSize = `calc(var(--u) * ${s.fs || 1})`;', '  typer.style.fontSize = `calc(var(--u) * ${s.fs || 1})`;\n  typer.classList.toggle("wrap", !!s.wrap);')
open(f, "w", encoding="utf-8").write(s)

bf = os.path.join(HERE, "build.py")
b_ = open(bf, encoding="utf-8").read()
if "PROMPT2" not in b_:
    b_ = b_.replace('prompt = os.environ.get("ANIM_PROMPT", "make the character run")',
                    'prompt = os.environ.get("ANIM_PROMPT", "Run in place in a steady loop: knees up, arms swinging, a slight forward lean. Keep the shield arm still.")\n'
                    'prompt2 = os.environ.get("ANIM_PROMPT2", "Make it faster with bigger strides, and keep both arms and hands still.")')
    b_ = b_.replace('.replace("/*PROMPT*/", json.dumps(prompt)[1:-1])',
                    '.replace("/*PROMPT*/", json.dumps(prompt)[1:-1]).replace("/*PROMPT2*/", json.dumps(prompt2)[1:-1])')
open(bf, "w", encoding="utf-8").write(b_)
print("patched: drag steps left =", s.count('act:"drag"'), "| prompt slots =", s.count("/*PROMPT"), "| wrap css =", ".typer.wrap" in s)
