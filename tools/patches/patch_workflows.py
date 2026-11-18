"""Add 'Recipes' and 'Workflows' chapters to the original-UI tour (tour.template.html). RUN_STEPS appended from run screens."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
f = os.path.join(HERE, "tour.template.html")
s = open(f, encoding="utf-8").read()
RUN_STEPS = open(os.path.join(HERE, "run_steps.js"), encoding="utf-8").read() if os.path.exists(os.path.join(HERE, "run_steps.js")) else ""

if '{id:"wf"' not in s:
    s = s.replace('  {id:"anim", name:"Rig & animate",', '  {id:"rec", name:"Recipes", sub:"One-click jobs in the chat"},\n  {id:"wf", name:"Workflows", sub:"Build once, run on a batch"},\n  {id:"anim", name:"Rig & animate",', 1)
    # move the two new chapters to the end of the chapter list order
    a = s.index('  {id:"rec", name:"Recipes"')
    b = s.index('  {id:"anim", name:"Rig & animate"')
    block = s[a:b]
    s = s[:a] + s[b:]
    end = s.index('];', s.index('const CH = ['))
    s = s[:end] + block + s[end:]

new_steps = r''' {ch:"rec", img:"p2_chat_result", act:"look", t:[17.6,30.6,29,21.6], z:1.3, title:"Recipes from a result", text:"Under every result, the buttons Turnaround, Expressions, Poses and Variations open the matching recipe with your image already attached."},
 {ch:"rec", img:"p2_more_moves", act:"click", t:[17.8,47,28.8,2.9], ring2:[17.8,51,11,32], z:1.3, title:"More recipes under More moves", text:"Icon set in this style, UI kit in this style, Turnaround, Expressions, Poses, Remove background, Upscale and Sprite sheet."},
 {ch:"rec", img:"p2_recipes", act:"look", t:[28.6,28.6,42.8,55], z:1.1, title:"Or open Recipes", text:"Click Recipes next to the message box: Character Turnaround, Background Removal, Color Palette, Image Analysis, Pose Transfer, Image Variations, Pose Variations, Expression Sheet, Icon Set, UI Kit, Tileset."},
 {ch:"rec", img:"p2_recipes", act:"click", t:[28.9,31.5,10.4,16], z:1.35, title:"Pick a card", text:"It becomes a chip in the message box. Fill the image slot or the short form (icon names, UI parts with exact text, number of tiles), check the cost, press Enter."},

 {ch:"wf", img:"w_dash", act:"click", t:[1.6,25,12.8,5.1], z:1.3, title:"Open Workflows", text:"Sidebar › Workflows. A workflow is a chain of steps you build once and run on a whole batch of images."},
 {ch:"wf", img:"w_dash", act:"click", t:[85.3,9.6,12.4,4], z:1.35, title:"New workflow", text:"Click New workflow. The arrow next to it has more ways to start."},
 {ch:"wf", img:"w_which_project", act:"click", t:[33.4,38.4,33.2,6.7], ring2:[58.8,76.5,8,5.3], z:1.25, title:"Pick the project", text:"Every workflow lives in a project and follows its Style Spec. Pick it, then Continue."},
 {ch:"wf", img:"w_new_dialog", act:"click", t:[43.6,12.2,12.9,10], z:1.35, title:"From template", text:"Blank gives an empty canvas, Import JSON loads an exported workflow. From template starts from a proven recipe."},
 {ch:"wf", img:"w_templates", act:"click", t:[30,29.4,12.8,15.6], z:1.3, title:"Pick a template", text:"14 templates: Batch Variations, Background Removal, Turnaround, Icon Set, Tileset, UI Kit, Seasonal Re-theme and more. Here: Batch Variations, then Use template."},
 {ch:"wf", img:"w_editor", act:"look", t:[25.4,53,49.2,8], z:1.25, title:"The steps, left to right", text:"Assets (your images) › For each (runs the next steps once per image) › Variations › Collect (gathers the results) › Export."},
 {ch:"wf", img:"w_palette_image", act:"click", t:[16.6,26.9,3.4,4], ring2:[20.6,26.9,22.2,42.4], z:1.3, title:"Add any step", text:"The left rail adds steps: Inputs, Image, 3D, Video, Utility, Flow, Output. Image has Generate, Edit, Region edit, Remove background, Segment, Upscale."},
 {ch:"wf", img:"w_variations_set", act:"click", t:[46.3,53.4,7.2,9.5], ring2:[80,42.2,19.2,5.2], z:1.25, title:"Change a step", text:"Click a step to open its settings. Here: 2 variations per item, differing in pose and expression. Then Save."},
 {ch:"wf", img:"w_editor", act:"click", t:[91.6,7.7,3.8,4.8], z:1.5, title:"Run", text:"Click Run when it's ready."},
 {ch:"wf", img:"w_run_dialog", act:"click", t:[33.4,44.3,9.6,5.1], ring2:[30.5,29.3,38.9,41.3], z:1.25, title:"Add the images", text:"Up to 20 images: Choose files, From Library, or From a previous run. Nothing is charged until you confirm."},
'''
if '{ch:"wf"' not in s:
    end = s.index('];', s.index('const STEPS = ['))
    s = s[:end] + new_steps + RUN_STEPS + s[end:]
open(f, "w", encoding="utf-8").write(s)
print("ok", s.count('ch:"wf"'), "wf steps,", s.count('ch:"rec"'), "recipe steps")
