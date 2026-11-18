// Part 3 (3D models) and Part 4 (rigging and animation), in the owner's order:
// T-pose image -> remove background -> Make it 3D -> rig -> animate with a prompt -> tune -> lock parts -> check -> save.
const ANIM_PROMPT = process.env.ANIM_PROMPT || "make the character run";

function part3(L) {
  const { p, h1, h2, bullet, callout, levelBanner, flow, steps, table, W } = L;
  return [
    h1("Part 3 · 3D models"),
    p("Every 3D model starts from an image. For a character you want to animate, the order matters:"),
    ...steps([
      "**Make the character image in a T-pose** (for a biped: a person or humanoid). Full body, arms straight out to the sides, plain background.",
      "**Remove the background** from that T-pose image.",
      "**Make it 3D** from the cut-out image.",
      "**Rig it, then animate it** (Part 4).",
    ]),
    callout("Biped characters must be in a T-pose. If the image isn't a T-pose, the rigging step won't work and the character can't be animated. Props and buildings don't need a T-pose: one clean subject on a plain background is enough."),
    levelBanner("Level 1 · First steps", "Get the image right, then make the model", null),

    flow({ id: "3D-1", title: "Start with a T-pose image (characters you will animate)",
      img: [["p2_chat_result", "A T-pose character: full body, arms straight out to the sides, plain background."]],
      when: "You want a 3D character that will walk, run, fight or move in any way.",
      where: "Studio chat, with `Type` set to `Character`",
      cost: "8 credits for the image (Balanced Image at 1K).",
      result: "A full-body T-pose image, ready for the next step.",
      steps: [
        "In the Studio chat, set `Type` to `Character`.",
        "Ask for the pose and background in words, for example: \"a knight hero, full body, front view, T-pose with arms straight out to the sides, plain light background\".",
        "Approve the plan (`Yes, generate`).",
        "Check the result before going on: the whole body is visible, the arms are straight out to the sides, the legs are apart, and the background is plain. If not, use `Redo` or ask for a change.",
      ],
      tips: ["Four-legged animals, birds and other bodies don't use a T-pose; show the whole body side-on on a plain background."] }),

    flow({ id: "3D-2", title: "Remove the background from the T-pose image",
      img: [["p2_more_moves", "Under the result: `More moves` › `Remove background`."]],
      when: "Always, before Make it 3D. A clean cut-out gives a cleaner model.",
      where: "Under the image result: `More moves` › `Remove background`. Or turn on `Remove background +3 credits` before you send the prompt.",
      cost: "3 credits",
      result: "The same character on a transparent background.",
      steps: [
        "Under the T-pose image, click `More moves ▾`.",
        "Click `Remove background`. The image is attached and the tool is picked.",
        "Press Enter. The cut-out appears in the chat and in Media.",
        "Check the badge: \"Clean cut-out\" means it's ready; \"Edges may need cleanup\" means look closely before going on.",
      ] }),

    flow({ id: "3D-3", title: "Make it 3D from the cut-out image",
      img: [["p3_make_it_3d_pill", "`Make it 3D` under the image result."], ["p3_viewer", "The finished model in the 3D Viewer."]],
      when: "The cut-out T-pose image looks right.",
      where: "The `Make it 3D` button under the cut-out result. Viewer › `Make it 3D`. `+` › `Tools` › `Image to 3D`.",
      cost: "35 credits",
      result: "A textured 3D model, shown in the chat and in Media under 3D.",
      steps: [
        "Under the **cut-out** image, click `Make it 3D` (≈ 35). The image is attached and the Image to 3D tool is picked.",
        "Press Enter.",
        "Wait a few minutes. You can keep working; the chat shows progress.",
        "Click the finished model to open the 3D Viewer.",
      ] }),

    flow({ id: "3D-4", title: "Look at your model: the 3D Viewer",
      when: "To check a model before you rig, animate or download it.",
      where: "Click a 3D tile in Media, or the model in the chat.",
      table: { widths: [2300, W - 2300], head: ["What", "How"], o: { firstCol: true, firstColBold: true }, rows: [
        ["Move around", "Drag to rotate, scroll or pinch to zoom. Zoom and rotate buttons, auto-rotate."],
        ["View modes", "Textured, Clay, Normals, Wireframe."],
        ["Scene", "Light angle, brightness, camera height and background colour."],
        ["Stats", "Real faces and vertices, plus \"asked …\" when you set a polygon budget."],
        ["Actions", "`Rig it` (Recommended), `Download`, `Animate`, `World` (Soon), `Flow`, `Remix`, `Share to gallery`."],
      ] } }),

    levelBanner("Level 2 · Control", "Choose every setting, then download", null),

    flow({ id: "3D-5", title: "Full control: Tools › 3D generation",
      img: [["p3_tools_3d", "Tools › 3D generation."]],
      when: "You know the polygon budget and quality you need.",
      where: "Sidebar › Create › Tools › `3D`, or Home › `Pick a tool` › `Create 3D Model`",
      cost: "35, plus the options you turn on (up to +45).",
      steps: [
        "Choose `Image to 3D` and add your cut-out T-pose image as the \"Source image\" (\"One subject on a clean background works best.\"), or `Text to 3D`.",
        "Set the Output (table below).",
        "Click `Generate ≈ N`. \"This can take a few minutes. You can leave — it will be saved to this project.\"",
      ],
      table: { widths: [2300, 4840, 2500], head: ["Setting", "Choices", "Extra credits"], o: { firstCol: true, firstColBold: true }, rows: [
        ["Polygon budget", "Automatic, Low poly (~4k faces), Mid poly (~18k), High poly (~50k)", "none"],
        ["Texture, PBR materials", "On or off", "none"],
        ["Texture quality", "standard, detailed (HD), extreme (8K)", "+10 / +20"],
        ["Geometry quality", "standard, detailed", "+20 (not on v2.5)"],
        ["Quad topology", "Quads instead of triangles", "+5"],
        ["Model version", "v3.1 (latest), v3.0, v2.5", "none"],
      ] } }),

    flow({ id: "3D-6", title: "Download and convert",
      img: [["p3_download_menu", "Download formats."]],
      when: "The model is ready for your engine.",
      where: "3D Viewer › `Download` (also top-right in the Rig view)",
      cost: "The stored GLB file: no credits. Other formats: 10 credits per conversion. 3D downloads need a paid plan or a credit pack.",
      steps: [
        "Click `Download`. The first item is the stored file (\"stored file · instant\").",
        "For another format, pick FBX, OBJ, USDZ, STL, 3MF or GLTF. The download starts by itself, usually in under a minute.",
      ],
      table: { widths: [4000, W - 4000], head: ["For", "Pick"], o: { firstCol: true }, rows: [
        ["Unity, Unreal", "FBX"], ["Godot", "GLB"], ["Blender", "GLB or FBX"], ["3D printing", "STL or 3MF"], ["iPhone and AR", "USDZ"],
      ] },
      callout: "On the Free plan the button shows a lock (\"Download · Paid\"): \"Preview, rig and animate your models on Free. To download the 3D file, pick a plan or buy a credit pack.\"" }),

    levelBanner("Level 3 · Advanced", "Your own models and models in parts", null),

    flow({ id: "3D-7", title: "Bring your own model",
      when: "You already have a model and want to optimise, reduce or retexture it.",
      where: "Chat `+` › `Upload a 3D model` (GLB · FBX · OBJ · STL, up to 30 MB)",
      cost: "Each job you ask for shows its cost before it runs.",
      steps: [
        "`+` › `Upload a 3D model` and pick the file. You'll see \"Uploading the 3D model…\", then \"Model added\".",
        "Tap a suggestion or type your own: \"Optimize this model for a game engine\", \"Reduce the poly count to 5,000 faces\", \"Retexture it as weathered bronze with a green patina\".",
        "Send.",
      ] }),

    flow({ id: "3D-8", title: "Models in parts: texture each part",
      when: "The model was built as separate parts.",
      where: "3D Viewer › the badge \"{n} separate parts · Texture parts\"",
      cost: "Building in parts: +10. Each texture job: 20 (+10 for HD).",
      steps: [
        "Click the parts badge. The \"Texture parts\" view opens.",
        "Click a part on the model, or pick it in the \"Parts · n\" list.",
        "Under \"Textures for Part n\", choose \"Plain (no texture)\", a texture you made before, or type a prompt and click `Texture Part n · 20 credits`.",
        "`Whole model` › `Texture all parts · 20 credits` does them all. `Reset` starts over; `Download this mix` saves the combination (paid plans).",
      ] }),
  ];
}

function part4(L) {
  const { p, h1, bullet, callout, levelBanner, flow, table, W } = L;
  return [
    h1("Part 4 · Rigging and animation"),
    p("A model needs a **rig** (a skeleton) before it can move. Rig it once, then make as many animations as you like."),
    callout("Rigging a biped only works on a model made from a **T-pose** image with the background removed (3D-1 to 3D-3). If rigging fails or the limbs move strangely, go back to the T-pose image."),
    levelBanner("Level 1 · Rig", "Give the model a skeleton", null),

    flow({ id: "A-1", title: "Rig the character",
      img: [["p4_rig_view", "The Rig view: body type, skeleton, file type, then `Rig character`."], ["p4_rigged", "Rigged ✓, with Bones turned on."]],
      when: "Before a character or creature can move.",
      where: "3D Viewer › `Rig it`. The `Rig it` button under a 3D result. `Rig it` in the Animation tab.",
      cost: "40 credits (the button doesn't show the price)",
      steps: [
        "Click `Rig it` on the model. The Rig view opens with it selected under \"Characters\" (\"Not rigged\").",
        "Choose the body type: `biped` for a T-pose person or humanoid (table below).",
        "Choose the skeleton: `Standard skeleton`, or `Mixamo-compatible skeleton` if you'll use Mixamo animations. Choose the file type: glb or fbx.",
        "Click `Rig character`. It takes a minute or two (\"Rigging…\"); the card then says \"Rigged\".",
        "Turn on `Bones` to see the skeleton and check that the arms and legs have bones.",
      ],
      table: { widths: [5000, W - 5000], head: ["Body", "Rig type"], o: { firstCol: true }, rows: [
        ["People and humanoids (T-pose)", "biped"], ["Four legs (dog, horse)", "quadruped"], ["Insects", "hexapod"], ["Spiders, octopus-like", "octopod"],
        ["Birds", "avian"], ["Snakes", "serpentine"], ["Fish", "aquatic"],
      ] } }),

    levelBanner("Level 2 · Animate", "Describe the move, then make it right", null),

    flow({ id: "A-2", title: "Animate it with a motion prompt",
      img: [["v_motion", "The Animation Studio: Parts on the left, the character in the middle, Motion, Tune and Check on the right."]],
      when: "The character is rigged.",
      where: "3D Viewer › `Animate`, or the `Animate` button under a rigged result. The chat folds away while the Animation Studio is open.",
      cost: "Trying moves shows no price. Saving a clip: `Save to project · 150 credits`.",
      steps: [
        "Click `Animate`. The Animation Studio opens with your character (\"Character\" picker at the top).",
        `Under "Motion", write the motion prompt: what the character should do, in your own words. Example: "${ANIM_PROMPT}". Or tap an example: Run, Jump, 3 punches, Uppercut, Lift something, Wave, Idle.`,
        "Click `Animate`. Leave `Auto-check` on.",
        "Read the plan under the button: \"Moving: Hips, Torso, Head, Right leg, Right arm…\" and \"Keeping still: Hair / ears / face\". This is what will move.",
        "Play it with the play button and the timeline. The label above the character shows the clip, its length and whether it loops (\"run · 0.80 s · loops\").",
      ],
      tips: ["`Plan parts` lets the AI decide which parts move before animating. `Test locks` checks your locked parts (A-4)."] }),

    flow({ id: "A-3", title: "Tune the animation: speed, intensity and more",
      img: [["v_tune_speed", "Tune: Speed dragged to 1.65×. The label now reads \"speed 1.65×\"."]],
      when: "The move is right but too slow, too fast, too small or too big.",
      where: "Animation Studio › \"Tune\"",
      cost: "No credits to tune.",
      steps: [
        "Open \"Tune\". Each slider starts at 1.00 (normal).",
        "Drag a slider right to increase it, or left to decrease it: `Speed`, `Intensity` (how big the move is), `Arm swing`, `Forward lean`.",
        "The preview updates straight away; the label shows the new values (for example \"speed 1.65×\").",
        "Quick buttons do common changes in one click: `Faster`, `Slower`, `Bigger motion`, `Loop it`.",
        "`Reset` puts every slider back to 1.00.",
      ] }),

    flow({ id: "A-4", title: "Keep parts still: lock a body region",
      img: [["v_lock_leg", "Locks: Right leg switched to \"Kept still\"; the locked region changes colour on the model."], ["v_lock_arms", "Arms and hands locked; the legs, hips and head still move."]],
      when: "One part of the body should not move: a hand holding a shield, the legs during an upper-body move, the hair or face.",
      where: "Animation Studio › \"Parts\" › `Locks`",
      cost: "No credits.",
      steps: [
        "In \"Parts\", click `Locks`. Every body region is listed with its bones: Hips, Torso, Head, Right leg, Right arm, Right hand, Left arm, Left hand, Hair / ears / face.",
        "Click a region to switch it from \"Moves\" to \"Kept still\". Click again to let it move.",
        "Locked regions change colour on the character, so you can see what will stay still. You can also click a part on the character itself (\"Click a part to lock or unlock it\").",
        "`All move` and `All still` switch every region at once.",
        "Click `Animate` again. The plan now lists the locked parts under \"Keeping still\".",
        "`Test locks` checks that the locked parts really stay still.",
      ],
      tips: ["`Model`, `Parts` and `Locks` change how the character is coloured: the whole model, each part in its own colour, or moving vs. locked.", "\"Pose locked parts\": pick a locked part, `Start posing`, drag the rings to set its fixed pose."] }),

    flow({ id: "A-5", title: "Check and fix",
      img: [["v_check", "Check: what passed, how far each part moved, and one-click fixes."]],
      when: "After every Animate; the check runs by itself when `Auto-check` is on.",
      where: "Animation Studio › \"Check\" and \"Fix a problem\"",
      steps: [
        "Open \"Check\". It shows how many things need fixing (\"1 to fix\") and a list with ✓ or ✗: script runs on every frame, stays on the ground, knees bend the right way, planted feet stay put, hands stay outside the body, joints stay in natural ranges, moves smoothly, loops cleanly, the planned parts move, mesh keeps its shape.",
        "Below the list, each part shows how far it moved. Locked parts show messages such as \"The script moved Right arm 40° — the lock held it still.\"",
        "When something is off, a fix button appears, for example `Fix: make right arm follow its own bones`. Click it.",
        "For a bad moment in the move: \"Fix a problem\" › pause on the frame, `Paint` over the wrong area, write \"What's wrong here?\", then `Send to the AI to fix`.",
      ] }),

    flow({ id: "A-6", title: "Save the clip and use it",
      when: "You're happy with the move.",
      where: "Animation Studio › bottom right",
      cost: "`Save to project · 150 credits`",
      steps: [
        "Click `Save to project · 150 credits`. The clip is added to this character (\"Clip saved\") and listed under \"Clips\".",
        "Or `Download GLB` (paid plans).",
        "For your engine: FBX for Unity and Unreal, GLB for Godot, GLB or FBX for Blender. Or use the Rapid Assets plugins (Sidebar › `Integrations`).",
      ],
      tips: ["Standard moves can also be asked for in the chat: \"animate it: idle, walk and run\" (20 credits for the first, +15 for each extra, up to 5)."] }),
  ];
}

module.exports = { part3, part4, ANIM_PROMPT };
