"""Tour 3D chapter driven from the chat window: prompt T-pose -> prompt remove background -> prompt make it 3D, then Studio steps."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
f = os.path.join(HERE, "tour.template.html")
s = open(f, encoding="utf-8").read()

a = s.index(' {ch:"3d", img:"p1_home", act:"type"')
b = s.index(' {ch:"anim",', a)
CB = "[19,76.4,26.6,4.6]"      # chat composer text area (wrap)
CR = "[18.4,75.4,27.7,6.6]"    # ring around the composer
SEND = "[43.3,82.2,2.5,4.3]"
new = f''' {{ch:"3d", img:"p2_studio_ready", act:"type", wrap:true, t:{CR}, box:{CB}, fs:.9, z:1.45, type:"a knight hero, full body, T-pose with arms straight out, plain background", title:"Step 1 · Prompt a T-pose character", text:"In the Studio chat, ask for the character in a T-pose: full body, arms straight out, plain background. For a biped you want to animate this is a must: without a T-pose, rigging won't work."}},
 {{ch:"3d", img:"p2_studio_ready", act:"click", keep:true, t:{SEND}, z:1.45, title:"Send it", text:"Press Enter or the orange arrow."}},
 {{ch:"3d", img:"p2_plan_card", act:"click", t:[21.8,48.9,23.9,4], z:1.35, title:"Approve the plan", text:"The plan makes one T-pose image (Balanced Image, 1K, 8 credits). Click Yes, generate."}},
 {{ch:"3d", img:"p2_chat_result", act:"look", t:[49.5,13.4,12,19.2], z:1.4, title:"Check the pose", text:"Whole body visible, arms straight out to the sides, legs apart, plain background. If not, ask for a change in the chat."}},
 {{ch:"3d", img:"p2_chat_result", act:"type", wrap:true, t:{CR}, box:{CB}, fs:.9, z:1.45, type:"remove the background", title:"Step 2 · Prompt: remove the background", text:"Type it in the same chat. The agent knows you mean the T-pose image you just made."}},
 {{ch:"3d", img:"p3c_rmbg_typed", act:"click", t:{SEND}, z:1.45, title:"Send it", text:"Press Enter."}},
 {{ch:"3d", img:"p3c_plan_rmbg", act:"click", t:[21.8,52.8,23.9,3.8], z:1.35, title:"Approve: ≈ 3 credits", text:"The plan: Remove background, keep the subject exactly as it is, transparent output. Click Yes, generate."}},
 {{ch:"3d", img:"p3c_rmbg_result", act:"look", t:[49.5,13.4,12,19.2], ring2:[38,44.7,7.2,3.1], z:1.35, title:"The cut-out is ready", text:"The same knight on a transparent background, in the chat and in Media. The check badge says Clean cut-out."}},
 {{ch:"3d", img:"p3c_rmbg_result", act:"type", wrap:true, t:{CR}, box:{CB}, fs:.9, z:1.45, type:"make it 3D", title:"Step 3 · Prompt: make it 3D", text:"Type it in the same chat. The agent builds the model from the cut-out T-pose image."}},
 {{ch:"3d", img:"p3c_rmbg_result", act:"click", keep:true, t:{SEND}, z:1.45, title:"Send it", text:"Press Enter."}},
 {{ch:"3d", img:"p3c_plan_3d", act:"click", t:[21.8,52.7,23.9,3.8], z:1.35, title:"Approve the 3D build", text:"The plan: a 3D model of the knight, background removed, standing in a T-pose. 3D costs about 35 credits and takes a few minutes."}},
 {{ch:"3d", img:"p3_chat_result", act:"look", t:[17.8,13,22.5,31.5], z:1.3, title:"Your 3D model", text:"The model appears in the chat and in Media. Under it: Rig it, Download, More moves. Click it to open the 3D Viewer."}},
 {{ch:"3d", img:"p3_viewer", act:"look", t:[73.2,37.9,25,3.6], z:1.25, title:"Look at it in 3D", text:"Drag to rotate, scroll to zoom, switch Textured, Clay or Wireframe. The stats show the real faces and vertices."}},
 {{ch:"3d", img:"p3_viewer", act:"click", t:[71,21.5,10.3,3.9], ring2:[65.8,25.5,15.4,31.5], z:1.35, title:"Download", text:"Paid plans download the model: GLB as stored, or FBX (Unity, Unreal), OBJ, USDZ, STL, 3MF, GLTF. Next: rig and animate it in the Studio."}},

'''
s = s[:a] + new + s[b:]
s = s.replace('{id:"3d", name:"Make it 3D", sub:"T-pose, cut-out, 3D model"}', '{id:"3d", name:"Make it 3D", sub:"Prompt: T-pose, cut-out, 3D"}')
open(f, "w", encoding="utf-8").write(s)
print("ok", s.count('ch:"3d"'), "3d steps")
