// Part 2 levels 3-4 (Style Spec, Recipes, sets, sprites, flow, workflows, gallery) and Part 5 journeys.
function levels(L) {
  const { p, bullet, gap, table, levelBanner, flow, W } = L;
  return [
    levelBanner("Level 3 · Consistent sets", "One style, many matching assets", "Lock a style once, then make whole sets that belong together."),

    flow({ img: [["p2_spec_setup", "Three ways to start a Style Spec."], ["p2_spec_continue", "Pick a look, then `Continue with` it."], ["p2_spec_questions", "A few questions pin the style down."]], id: "2D-15", title: "Lock your art style (Style Spec)",
      when: "Every asset in a project should share one look: palette, line, proportions.",
      where: "Studio chat bar › `No style locked · Lock style` (or the `Style Spec vN` chip). Home › Spec chip. Media ⋯ › `Style Spec`. Learn › `Create a Style Spec`. New projects ask you first.",
      cost: "Free: \"drafting doesn't use credits.\"",
      result: "A locked Style Spec (v1, v2…) that every new image, 3D model and workflow run in the project follows.",
      steps: [
        "Open the setup: \"Set up your project's Style Spec\".",
        "Pick a starting point: `Start from a style` (choose a preset, then `Continue with {name}`), `Describe it` (write the style, then `Continue`), or `Use reference images` (upload at least 3, then `Draft spec`).",
        "Answer the short questions (\"A few questions to pin the style down\"), then `Draft spec`.",
        "Wait for \"Drafting your Style Spec…\". The draft shows how many sections, colours and references it has.",
        "Check it with `Preview sample`, change it with `Edit spec`, then click `Lock it`.",
        "You'll see \"Style Spec v1 locked: Every new asset in this project follows it.\"",
      ],
      tips: [
        "Not ready? `Skip for now` lets you work without a spec. You can set one up later.",
        "Every asset remembers which spec version it used.",
        "The Free plan can save 3 styles; Starter 25; Pro 100; Studio no limit.",
      ] }),

    flow({ id: "2D-16", title: "Change or refine your Style Spec",
      when: "The style needs a tweak: warmer shadows, thinner outlines, a new colour.",
      where: "Media ⋯ › `Style Spec`, or the `Style Spec vN` chip",
      cost: "Free",
      steps: [
        "Open the Style Spec panel. It has sections: Overview, Palette, Rendering & line, Proportions & shapes, Characters, Environments, Props & items, UI & text, Output defaults, Always / Never, References.",
        "Edit a section directly, or click `Refine with AI…`, pick a section (or `Whole spec`), type the change (for example \"warmer shadows, thinner outlines\") and click `Refine`.",
        "Click `Save v{n+1}`. On a locked spec it asks \"Save as v{n+1}?\": new runs use the new version, runs already started keep theirs.",
        "Add style images under References (up to 100): `Add from Media` or `Add images`, or drop files.",
        "`History` lists every version; restoring one saves it as a new version.",
      ],
      tips: ["`Unlock` lets you change the spec freely; `Lock` fixes it again.", "If you change the spec while a plan is waiting, the plan offers `Re-plan` or `Use plan as is`."] }),

    flow({ img: [["p2_recipes", "The Recipes window."]], id: "2D-17", title: "Recipes: ready-made jobs in one click",
      when: "A common job (turnaround, expressions, icon set…) without writing a long prompt.",
      where: "Studio chat › `Recipes` (next to the message box). Home › `Recipes`. Home \"Continue where you left off\" shows starter recipes when you're new.",
      cost: "Shown before you send. The Icon Set, UI Kit and Tileset forms show the full price.",
      steps: [
        "Click `Recipes`. The \"Workflows\" window opens with tabs `All`, `Character`, `Image`, `Analyze` (and `My workflows`).",
        "Click a card. It becomes a chip in the message box (`Clear selected workflow` removes it).",
        "Fill the image slots (the dashed `+` buttons) and any form.",
        "Add a short description if the placeholder asks for one, then press Enter.",
      ],
      table: { widths: [2300, 4540, 2800], head: ["Recipe", "What it makes", "What you give it"], o: { firstCol: true, firstColBold: true }, rows: [
        ["Character Turnaround", "A 360° turnaround sheet of a character", "1 image, plus style or outfit notes"],
        ["Expression Sheet", "A sheet of facial expressions", "1 image; how many (1–9)"],
        ["Pose Variations", "Front-view body poses (T-pose, standing, running…)", "1 image; name up to 4 poses"],
        ["Pose Transfer", "Puts the pose from one image onto another character", "`Pose Reference` and `Target Character` images"],
        ["Image Variations", "Several takes on one image", "1 image; how many (1–4); optional Keep and Change"],
        ["Background Removal", "A clean cut-out", "1 image"],
        ["Color Palette", "The colour palette of an image", "1 image"],
        ["Image Analysis", "A description of what's in an image", "1 image"],
        ["Icon Set", "Matching game icons, each on a transparent background", "Icon names (optional) and a count (2–12)"],
        ["UI Kit", "Buttons, bars, panels and badges in one style", "The parts you want (at least 2) and their text"],
        ["Tileset", "Matching seamless ground tiles that fit in any order", "How many tiles (2–9)"],
      ] },
      tips: ["While a recipe is picked, Tools, Web search, size and Exact text are off (\"Clear the workflow to use Tools or Web search\").", "With the Workflow Builder you can open any recipe with `Open in builder` and change its steps (see 2D-22)."] }),

    flow({ id: "2D-18", title: "Character sheets: turnaround, expressions, poses",
      when: "You need the same character from every side, with different faces, or in different poses: for 3D, sprites or animation.",
      where: "The `Turnaround`, `Expressions` and `Poses` buttons under a character result, or `Recipes` › Character tab",
      cost: "Shown before you send.",
      steps: [
        "Make the character first, with `Type` set to `Character` (2D-8).",
        "Under the result, click `Turnaround` (or `Expressions` or `Poses`). The recipe is picked and the image attached.",
        "Add notes if you like (\"armour stays gold\", \"6 expressions\") and press Enter.",
        "To copy a pose from another picture, use `Recipes` › `Pose Transfer`: put the pose picture in `Pose Reference` and your character in `Target Character`.",
      ],
      tips: ["A turnaround is a good source for Make it 3D and for sprite sheets: it keeps the character the same from every side."] }),

    flow({ id: "2D-19", title: "Icon sets, UI kits and tilesets",
      when: "A whole matching set at once, for a game's interface or level.",
      where: "`Recipes` › `Icon Set`, `UI Kit` or `Tileset`. Also `Icon set in this style` and `UI kit in this style` under a result. Chat `Type` › `Tileset (2–9)`.",
      cost: "Icon or UI part: about 11 each (image + cut-out). Tileset: about 8 per tile + 8. The form shows the total, for example \"≈ 6 × 11 = 66 credits\".",
      steps: [
        "**Icon Set:** type the icon names (\"sword, shield, potion…\") or leave it empty, set the count (2–12, default 6), press Enter.",
        "**UI Kit:** keep or untick parts: primary button, secondary button, panel/window frame, progress bar, toggle, slider, tab, close button, currency badge (at least 2). `Text on parts` lets you write labels like \"PLAY\". Press Enter.",
        "**Tileset:** choose how many tiles (2–9, default 4), describe the ground (\"grass with stones\"), press Enter.",
        "Each piece arrives as its own image in Media. Icons and UI parts are cut out on transparency.",
      ],
      tips: ["Lock a Style Spec first so the set matches the rest of your game.", "Use `Tiled preview` and the \"Seamless\" badge to check tiles."] }),

    levelBanner("Level 4 · Advanced", "Animate in 2D, see the whole session, automate, share", null),

    flow({ img: [["p2_sprite_setup", "Sprite setup: reference, action, frames, view and the cost."], ["p2_sprite_keyframe", "Approve the key frame before the other frames are made."]], id: "2D-20", title: "Sprite sheets: animate a character frame by frame",
      when: "A 2D character needs an idle, walk, run, attack, jump or hurt cycle for your game.",
      where: "Media toolbar › `Sprites`. The `Sprite` button on an image tile. Viewer › `Sprite sheet`. The `Sprite sheet` button under a result. Edit view › `Use in sprite sheet`.",
      cost: "11 credits per frame. The setup shows the total (\"8 frames × 11 = 88 credits\") and your balance. Failed frames aren't charged.",
      result: "A sprite sheet with a loop preview, exported as a sheet + JSON atlas, a frames ZIP, a GIF or an animated WebP.",
      steps: [
        "Open Sprites and click `New sprite sheet`. Pick the reference character: `Pick from Media` or `Upload`.",
        "Choose the **Action**: Idle, Walk, Run, Attack, Jump, Hurt or Custom (`Describe the action`, for example \"casting a fireball\").",
        "Choose the **Frames** (4–12; Walk and Run start at 8) and the **View**: Side, Front, Three-quarter or Top-down.",
        "Click `Make key frame · 11 credits`. Frame 1 is made first so you can check it.",
        "In \"Approve the key frame\": `Approve · 7 more frames · 80 credits` (the key frame's background removal is included), `Regenerate · 11`, or `Edit in editor` to fix it first.",
        "Watch \"3 of 8 frames ready\" until \"All 8 frames are ready\". Any single frame can be redone (`Regenerate · 11`) or edited (`Edit`).",
        "Check the loop preview: Play/Pause, step frame by frame, `Speed` (4–24 fps), `Mirror` (Side view) and `Onion skin`.",
        "Click `Export`, pick `Grid` or `One row`, then `Sheet + JSON atlas`, `Frames ZIP`, `GIF` or `Animated WebP`.",
      ],
      tips: [
        "Use a clean, full-body character with a plain background as the reference. A turnaround (2D-18) works well.",
        "Run out of credits mid-way? Top up, then `Resume · N frames`.",
        "The sheet + JSON atlas works with common 2D engines and TexturePacker-style importers.",
      ] }),

    flow({ id: "2D-21", title: "See how everything connects: Session flow",
      when: "You've made many versions and want to see what came from what.",
      where: "Media ⋯ › `Session flow`, or `Flow` in the 3D Viewer",
      cost: "Free",
      steps: [
        "Open Session flow. Each output is a node, with lines showing which result fed the next.",
        "Drag nodes to rearrange. Click an image or video node to open it; click a 3D node to open the 3D Viewer.",
        "On a node: `Add / edit a note`, `Tag for further editing`, or `Remove from canvas` (removes it from the graph only).",
      ] }),

    flow({ img: [["p1_workflows", "The Workflows page."]], id: "2D-22", title: "The Workflow Builder: build once, run on a whole set",
      when: "You repeat the same chain of steps on many items.",
      where: "Sidebar › Create › `Workflows`",
      intro: "Full step-by-step tutorial with screenshots: Part 5 · Workflows (W-2 to W-7), plus every template." }),

    flow({ img: [["p1_gallery", "The Gallery."]], id: "2D-23", title: "Share to the Gallery, and remix other people's work",
      when: "Show off your work and earn credits, or start from something in the community.",
      where: "Viewer › `Share to gallery +5`, or a Media tile ⋯ › `Share to gallery`. Sidebar › Library › `Gallery` for the community.",
      cost: "Sharing earns credits: +50 for your first approved item, then +5 per image (+10 per 3D model), up to 150 a month, plus bonuses at 10 and 50 likes.",
      steps: [
        "**Share:** click `Share to gallery`. The first time, set up your public profile (avatar and handle), then `Continue`.",
        "Read \"Before you share\", tick I agree, and click `Share to gallery`.",
        "It is checked (\"Checking your asset…\"), then `Published` with `View in gallery`, or `Couldn't publish`.",
        "**Remix:** in the Gallery, search or filter (`All`, `2D`, `3D`; Trending, New, Most liked; categories like Characters, Props, Icons). Open an item and click `Remix`.",
        "Pick or create a project. The Studio opens with the prompt and image filled in. Change it if you like, then press Send.",
      ] }),
  ];
}

function journeys(L) {
  const { h2, p, steps, small, gap, table, W } = L;
  const j = (title, cost, list, note) => [h2(title), small(`Typical cost: ${cost}`), ...steps(list), ...(note ? [p(note)] : []), gap()];
  return [
    ...j("J1 · A game prop, from idea to engine", "≈ 8 + 35 = 43 credits, plus 10 for a converted format", [
      "Home › type \"a wooden treasure chest, stylised, game prop\" › Send.",
      "On the plan card, `Yes, generate`. (Set `Type` to `Prop` in the Studio for a transparent background.)",
      "Under the result, `Make it 3D` › Enter.",
      "Open the model, check it in Clay and Wireframe.",
      "`Download` › FBX for Unity or Unreal, GLB for Godot (paid plans).",
    ]),
    ...j("J2 · A 2D platformer hero with animations", "≈ 8 for the hero, then 11 per frame (an 8-frame walk is 88)", [
      "Lock a Style Spec: `Start from a style` › a pixel-art or cartoon preset › `Lock it` (2D-15).",
      "In the chat, `Type` › `Character`, and ask for \"a knight hero, full body, side view, plain background\".",
      "Optional: `Turnaround` to keep the hero consistent.",
      "Sprites › `New sprite sheet` › pick the hero › Action `Walk`, Frames 8, View `Side` › `Make key frame`.",
      "`Approve` the key frame, wait for all frames, check the loop (`Mirror` for the other direction).",
      "`Export` › `Sheet + JSON atlas`. Repeat for Idle, Attack and Jump.",
    ]),
    ...j("J3 · An animated 3D character", "≈ 8 + 3 + 35 + 40 = 86 credits; saving an Animation Studio clip adds 150", [
      "In the chat, `Type` › `Character`: \"a knight hero, full body, front view, T-pose with arms straight out, plain light background\". Approve.",
      "Under the result: `More moves` › `Remove background` › Enter.",
      "Under the cut-out: `Make it 3D` › Enter.",
      "`Rig it` › biped › `Rig character`. Turn on `Bones` to check.",
      "`Animate` › write the motion prompt › `Animate`.",
      "Tune: drag `Speed` and `Intensity`, or use `Faster`, `Slower`, `Bigger motion`, `Loop it`.",
      "Lock what should stay still: Parts › `Locks` › click a region (\"Kept still\"), then `Animate` again.",
      "Open \"Check\" and use any fix button it offers.",
      "`Save to project · 150 credits`, then `Download` › FBX (paid plans).",
    ]),
    ...j("J4 · A UI pack in one style", "≈ 99 for a 9-part UI kit, ≈ 66 for 6 icons", [
      "Lock a Style Spec for the game.",
      "`Recipes` › `UI Kit` › keep the parts you need › `Text on parts`: \"PLAY\", \"SETTINGS\" › Enter.",
      "`Recipes` › `Icon Set` › \"sword, shield, potion, coin, heart, key\" › Enter.",
      "Download the pieces as PNG (transparent).",
    ]),
    ...j("J5 · Ground tiles and textures for a level", "≈ 40 for 4 tiles, 16 per texture", [
      "`Recipes` › `Tileset` › 4 tiles › \"grass with small stones\" › Enter.",
      "Open each tile: `Tiled preview` and the \"Seamless\" badge.",
      "For walls: `Type` › `Texture` › \"mossy castle wall\" (made tileable).",
    ]),
    ...j("J6 · The same job on a whole batch", "Shown in the run window before anything runs", [
      "Do the job once in the chat (for example: make an enemy → remove background → sprite sheet).",
      "Media ⋯ › `Save chat as workflow` › `Open in builder`.",
      "Add a `For each` step so the chain runs once for every item in your list (for example, each enemy).",
      "`Run` › `Preview on 2 items first` › check › `Run the remaining N`.",
      "Review: `Approve` / `Reject`, `Accept batch`, then export.",
    ]),
  ];
}

module.exports = { levels, journeys };
