// Part 5 · Workflows: Recipes (in chat), the Workflow Builder (Workflows page), and every template.
function part5(L) {
  const { p, h1, h2, bullet, small, callout, levelBanner, flow, table, shot, W } = L;
  return [
    h1("Part 5 · Workflows"),
    p("A workflow is a job that's already set up for you. There are two kinds:"),
    table([2400, 3620, 3620], ["", "Recipes", "Workflow Builder"], [
      ["What it is", "Ready-made jobs, one click in the chat", "Your own chain of steps on a canvas"],
      ["Runs on", "One image or one set at a time", "A whole batch: up to 20 images per run"],
      ["Where", "Studio chat › `Recipes`", "Sidebar › Create › `Workflows`"],
      ["Best for", "Turnarounds, expressions, poses, icon sets, UI kits, tilesets", "The same job on many assets: 10 enemies, a whole season re-theme"],
    ], { firstCol: true, firstColBold: true }),
    callout("Lock a Style Spec first (2D-15). Every recipe and every workflow run in the project follows it, so whole sets come out looking like one game."),

    levelBanner("Recipes", "One-click jobs in the chat", "Each recipe below follows the same pattern: pick it, give it an image or a short list, check the cost, send."),
    flow({ id: "W-1", title: "How every recipe works",
      img: [["p2_recipes", "Studio chat › Recipes: tabs All, Character, Image, Analyze, My workflows."], ["p2_chat_result", "Shortcuts: the buttons under a result (Turnaround, Expressions, Poses, Variations…) open the matching recipe with the image already attached."]],
      when: "You want a standard job done without writing a long prompt.",
      where: "Studio chat › `Recipes` (next to the message box). Or a button under a result: `Turnaround`, `Expressions`, `Poses`, `Variations`, `Icon set in this style`, `UI kit in this style`.",
      cost: "Shown before you send. The Icon Set, UI Kit and Tileset forms show the full total.",
      steps: [
        "Make or open the image you want to work from (for example your character).",
        "Click `Recipes`, or the matching button under the result.",
        "Click a card. It becomes a chip in the message box (`Clear selected workflow` removes it).",
        "Fill the image slot (the dashed `+`) and any short form.",
        "Add a few words if the box asks (style, outfit, how many), then press Enter.",
        "Approve the plan if you're in Plan mode. Results land in the chat and in Media.",
      ] }),

    table([2300, 3300, 4040], ["Recipe", "You give it", "Steps and tips"], [
      ["Character Turnaround", "1 character image (full body)", "Under the character: `Turnaround`. Add outfit or style notes. You get front, side and back in one sheet: use it for Make it 3D and sprite sheets."],
      ["Expression Sheet", "1 character image + how many (1–9)", "Under the character: `Expressions`. Say how many and which (\"happy, angry, surprised\")."],
      ["Pose Variations", "1 character image + up to 4 pose names", "Under the character: `Poses`. Name the poses: \"T-pose, standing, running, jumping\"."],
      ["Pose Transfer", "`Pose Reference` image + `Target Character` image", "Recipes › Pose Transfer. Put the pose picture in the first slot and your character in the second."],
      ["Image Variations", "1 image + how many (1–4), optional Keep / Change", "Under the result: `Variations`. Keep: \"face, outfit\". Change: \"cloak colour, weather\"."],
      ["Background Removal", "1 image", "Recipes › Background Removal, or `Remove background` under a result (3 credits)."],
      ["Color Palette", "1 image", "Recipes › Color Palette. Pulls out the main colours, handy for a Style Spec."],
      ["Image Analysis", "1 image", "Recipes › Image Analysis. Describes the art style and content in words."],
      ["Icon Set", "Item names (up to 12) + a theme", "Recipes › Icon Set, or `Icon set in this style`. Add a theme (\"shop currency and rewards\") so they read as a set. Each icon is cut out (~11 each)."],
      ["UI Kit", "The parts you want + exact text", "Recipes › UI Kit: primary/secondary button, panel, progress bar, toggle, slider, tab, close, currency badge. `Text on parts`: \"PLAY\", \"SHOP\" is spelled exactly (~11 per part)."],
      ["Tileset", "How many tiles (2–9) + the ground", "Recipes › Tileset, or `Type` › `Tileset (2–9)`. Matching seamless tiles that fit in any order (~8 per tile + 8)."],
    ], { firstCol: true, firstColBold: true }),
    small("Chain sets: under any icon, `UI kit in this style` or `Icon set in this style` starts the next set from it."),

    levelBanner("Workflow Builder", "Build once, run on a whole batch", "A real run on rapidassets.ai: the Batch Variations template on two knight images."),
    flow({ id: "W-2", title: "Open Workflows and pick a project",
      img: [["w_dash", "Sidebar › Workflows: your projects and recent workflows."], ["w_which_project", "New workflow › Which project? Every workflow lives in a project and follows its Style Spec."]],
      when: "You want to run the same steps on several assets.",
      where: "Sidebar › Create › `Workflows`",
      steps: [
        "Click `Workflows` in the sidebar. The page lists your projects and recent workflows.",
        "Click `New workflow` (the arrow next to it has more ways to start).",
        "Pick the project in \"Which project?\", then `Continue`.",
        "No Style Spec yet? You can set one up or `Skip for now` (\"Run asks for a spec later, right here\").",
      ] }),

    flow({ id: "W-3", title: "Start from a template",
      img: [["w_new_dialog", "New workflow: Blank, From template, or Import JSON."], ["w_templates", "Templates: filter All, 2D or 3D. Each shows its number of steps."]],
      where: "Project › `New workflow`",
      steps: [
        "Choose `From template` (\"Start from a proven recipe\"). `Blank` gives an empty canvas; `Import JSON` loads a workflow someone exported.",
        "Pick a template, for example `Batch Variations` (5 steps: make several variations of every image).",
        "Click `Use template`. The editor opens.",
      ] }),

    flow({ id: "W-4", title: "Understand the editor",
      img: [["w_editor", "The editor: steps palette on the left, the canvas in the middle, the outline on the right."], ["w_palette_image", "Add step › Image: Generate image, Edit image, Region edit, Remove background, Segment, Upscale…"]],
      steps: [
        "The **canvas** shows the steps left to right, joined by lines: Assets → For each → Variations → Collect → Export.",
        "**Assets** holds the starting images; each one becomes its own item. **For each** runs the next steps once per image. **Collect** gathers the results back into one list. **Export** hands them over.",
        "The **left rail** adds steps: Inputs, Image, 3D, Video, Utility, Flow, Output, Your workflows. Click one, or drag it onto the canvas.",
        "The **right panel** shows the outline of every step, or the settings of the step you clicked.",
        "Top bar: the name and version (v1), the project, the Style Spec, then `Save`, `Run` and ⋯ (Duplicate, Export JSON, Version history, Lock).",
      ] }),

    flow({ id: "W-5", title: "Change a step's settings",
      img: [["w_assets_settings", "Assets: \"Several starting images. Each one becomes its own item.\""], ["w_variations_set", "Variations: Variations per item set to 2; What should differ: pose and expression."]],
      steps: [
        "Click the settings icon on a step (or the step in the outline).",
        "Change what you need. Here: `Variations per item` = 2, and \"What should differ\" = pose and expression. Everything else stays the same.",
        "`Save`. Unsaved changes show \"Unsaved changes · kept on this device\" until you save.",
      ] }),

    flow({ id: "W-6", title: "Run it on your images",
      img: [["w_run_dialog", "Run: add up to 20 images: Choose files, From Library, or From a previous run."], ["w_run_files", "Two knight images added: 2 images ready · 2 of 20."], ["w_run_spec_gate", "No locked Style Spec yet? The run stops here until you set one up. Nothing has been charged."], ["w_spec_ready", "Draft ready: palette, rendering and Always / Never rules. `Lock and use` locks it and goes back to the run; `Preview sample` shows one asset first (~5 credits)."], ["w_spec_lock_continue", "Already drafted a spec? The run asks: Lock Spec v1 to run? › Lock and continue."], ["w_run_cost", "Run Batch Variations? Inputs, what runs (1 step · 2 items · 32–96 credits) and your balance after. Then Run."]],
      cost: "Shown in the run window. Nothing is charged until you confirm the run.",
      steps: [
        "Click `Run`.",
        "Add the images to run (up to 20): `Choose files`, `From Library`, or `From a previous run`. Or drop files in. Each image shows as ready, with `Remove` to take it out.",
        "Click `Check the cost`.",
        "**The project needs a locked Style Spec.** If it has none, you'll see \"Set up your project's Style Spec first: Runs follow a locked Style Spec so every result in the batch matches.\" Click `Set up Style Spec`, pick a starting point (a style, describe it, or reference images), then `Lock and use` (or `Edit first`). You stay on the same page.",
        "The window now shows what the run will cost. Confirm to start it.",
      ],
      callout: "Workflows always run with a locked Style Spec, so a batch of 20 comes out in one consistent style. Lock it once per project (2D-15) and every run after that goes straight to the cost." }),

    flow({ id: "W-7", title: "Watch it run, review and export",
      img: [["w_run_started", "Run #1 · Batch Variations: every step with its status (Done, Running, Up next). Safe to close the tab."], ["w_run_review", "Finished with 2 waiting for review: the quality check flagged both variations."], ["w_run_export", "Keep this result on the ones you want, then Run from here to finish Collect and Export."]],
      steps: [
        "After `Run`, the run page opens: \"Run #1 · Batch Variations\". Each step shows Done, Running or Up next, with its results underneath. It is safe to close the tab; the run keeps going.",
        "On the right: \"Accepted so far\" (how many items passed the quality checks) and \"Downloads\" (files appear here as results finish).",
        "Results that don't pass the automatic quality check wait for you: the run says \"2 waiting for review\". Press `Keep this result` on the ones you want, or `Retry failed items` to try again.",
        "Then open the ⋯ on the next step (Collect or Export) and choose `Run from here` (or `Run this step`) to finish.",
        "Download the finished results from \"Downloads\". `Open in editor` takes you back to change the workflow.",
      ],
      tips: ["The confirm window shows the range: \"1 step · 2 items · 32–96 credits\". You're only charged for what actually runs; quality checks are free.", "Each run records which Style Spec version it used, so past runs keep their look even if you change the spec later."] }),

    h2("All workflow templates"),
    table([2700, 900, W - 3600], ["Template", "Steps", "What it does"], [
      ["Batch Variations", "5", "Several variations of every image in a batch."],
      ["Background Removal", "3", "Cuts each image out of its background."],
      ["Character Facial Pose Sheet", "3", "Turns a character image into a sheet of faces and expressions."],
      ["Character Turnaround", "3", "Turns a character image into a front, side and back turnaround."],
      ["Color Palette Extraction", "4", "Pulls the main colours out of an image."],
      ["Icon Set", "15", "Makes a matching set of six game icons."],
      ["Image Analysis", "4", "Describes an image's art style and content."],
      ["Parallel Pose Edits", "4", "Redraws your character in several poses at once."],
      ["Parallel Image Variations", "4", "Several variations of one image at once."],
      ["Pose Transfer", "4", "Puts your character into the pose from another image."],
      ["Seasonal Re-theme", "7", "Re-themes a batch of game assets (for example for winter or Halloween)."],
      ["Texture 3D Model", "4", "Repaints a 3D model's surface."],
      ["Tileset", "8", "Makes seamless ground tiles that fit together."],
      ["UI Kit", "21", "Makes a matching game UI kit, from buttons to panels."],
    ], { firstCol: true, firstColBold: true }),
    ...require("./guide_wf_templates").sections(L),
  ];
}
module.exports = { part5 };
