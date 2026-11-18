// Rapid Assets Studio guide book (2D, 3D, rigging, animation). node guide.js <out.docx>
const fs = require("fs");
const L = require("./guidelib");
const { p, small, h1, h1keep, h2, bullet, sub, gap, steps, table, callout, levelBanner, flow, build, shot, Paragraph, TextRun, W, INK, GREY, ORANGE, FONT, runs } = L;
const advanced = require("./guide_2d_advanced");

const out = process.argv[2] || "guide.docx";
const C = [];
const add = (...x) => C.push(...x.flat(Infinity));

// ---------------------------------------------------------------- cover
add(
  new Paragraph({ spacing: { before: 1800, after: 120 }, children: [new TextRun({ text: "RAPID ASSETS", bold: true, color: ORANGE, size: 22, font: FONT, characterSpacing: 60 })] }),
  new Paragraph({ spacing: { after: 160 }, children: [new TextRun({ text: "Studio Guide Book", bold: true, size: 64, font: FONT, color: INK })] }),
  new Paragraph({ spacing: { after: 480 }, children: [new TextRun({ text: "2D images, 3D models and animation: every path, from your first image to an animated, game-ready character.", size: 28, font: FONT, color: GREY })] }),
  table([2300, W - 2300], null, [
    ["Matches", "The live site, rapidassets.ai, on 17 November 2026"],
    ["Prices", "From the live price list on the same day. The exact price always shows on the button before you spend."],
    ["Who it's for", "Anyone using the Studio: new users, the support team, and anyone showing the product."],
  ], { firstCol: true, firstColBold: true }),
  gap(),
  L.h2("How to read this guide"),
  table([2300, W - 2300], null, [
    ["`Bold words`", "The exact words on the screen: a button, tab, menu item or message."],
    ["›", "Then open or click. Example: Sidebar › Create › `Studio`."],
    ["≈ 8", "About 8 credits. The real price shows before anything runs."],
    ["Levels", "Each part starts simple and gets more advanced. Level 1 is your first day; Level 4 is for power users."],
    ["Flow boxes", "Every flow starts with a box: when to use it, where to find it, what it costs, and what you get. Numbered steps follow."],
  ], { firstCol: true, firstColBold: true }),
  gap(),
  L.h2("Contents"),
  ...[
    "Part 1 · Getting around: the screen, the main places, projects, the Studio, the agent or the tools, chat modes",
    "Part 2 · 2D images: Level 1 first steps → Level 2 control → Level 3 consistent sets → Level 4 advanced",
    "Part 3 · 3D models: T-pose image, remove background, Make it 3D, full settings, download and convert, your own models, parts",
    "Part 4 · Rigging and animation: rig, motion prompt, tune speed and intensity, lock body parts, check and fix, save",
    "Part 5 · Workflows: every Recipe, the Workflow Builder step by step, all templates",
    "Part 6 · Complete journeys: start-to-finish recipes for common game assets",
    "Part 7 · Credits and plans: every price, plan limits, where to see your balance",
    "Part 8 · Problems and answers",
  ].map(bullet),
);

// ---------------------------------------------------------------- part 1
add(
  h1("Part 1 · Getting around"),
  p("Rapid Assets runs in the browser at rapidassets.ai. After you sign in you land on **Home**. Everything you make is saved inside a **project**, and you can always find it again in that project's Media."),
  h2("1.1  The screen"),
  table([2200, W - 2200], ["Area", "What's there"], [
    ["Left sidebar", "Logo and plan, the project switcher, `Home`. Under **Create**: `Studio`, `Workflows`, `Tools` (Image, Edit, 3D, Video). Under **Library**: `Projects`, `Shared with me`, `Gallery`. At the bottom: `Integrations` and `Learn`. The collapse button shrinks it to icons."],
    ["Top bar", "Where you are on the left (for example \"Project · Agent · Chat\"). On the right: the gift (`Earn credits`), the bell (notifications: All, Updates, Activity, Credits), the credits pill, `Upgrade` (Free plan only) and your avatar."],
    ["Avatar menu", "Profile, Show tips again, Credits & usage, Billing, Settings, AI agents, Logout."],
    ["On a phone", "A top bar (menu, logo, credits, bell, avatar) and tabs at the bottom: Home, Studio, Workflows, Library, Learn."],
  ], { firstCol: true, firstColBold: true }),
  shot("p1_home", "Home: the sidebar on the left, the prompt box in the middle, credits and your avatar top-right."),
  h2("1.2  The main places and how to reach them"),
  table([1700, 3300, W - 5000], ["Place", "How to get there", "What it's for"], [
    ["Home", "Sidebar › `Home`", "Start anything: type an idea or pick a tool. Also shows \"Continue where you left off\", \"New & featured\" and \"Inspirations\"."],
    ["Studio", "Sidebar › Create › `Studio`, or send a prompt from Home", "Chat with the agent on the left, the project's Media on the right. The agent plans and makes assets for you."],
    ["Workflows", "Sidebar › Create › `Workflows`", "Build a chain of steps once and run it on a whole batch (see Part 5)."],
    ["Tools", "Sidebar › Create › `Tools` › Image, Edit, 3D or Video. Or Home › `Pick a tool`", "Choose the model and every setting yourself. One job at a time, no chat."],
    ["Projects", "Sidebar › Library › `Projects`", "All your projects. Search, filter My, Shared or All, create, rename, share, delete."],
    ["Shared with me", "Sidebar › Library › `Shared with me`", "Projects other people shared with you."],
    ["Gallery", "Sidebar › Library › `Gallery`", "Community images and 3D models. Search, filter 2D or 3D, and Remix one into your own project."],
    ["Learn", "Sidebar › `Learn`", "A \"Get set up\" checklist, tours, video tutorials and articles."],
    ["Integrations", "Sidebar › `Integrations`, or avatar › `AI agents`", "Use Rapid Assets from coding agents (Claude Code, Cursor, Codex and more) and from engine plugins (Unity, Unreal, Godot, Blender)."],
    ["Credits", "The credits pill in the top bar", "Your balance and history. Buy credits or upgrade."],
  ], { firstCol: true, firstColBold: true }),
  shot("p1_sidebar_tools", "Sidebar › Create › Tools opens Image, Edit, 3D and Video."),
  shot("p1_projects", "Library › Projects: every project as a card. `Create New` is top-right."),
  h2("1.3  Projects"),
  bullet("Every image, edit, model and animation is saved to the project that is open."),
  bullet("The **project switcher** sits at the top of the sidebar. It has a name search, `My projects` and `Shared` tabs, `See all →`, and `New Project`."),
  bullet("When you send a prompt from Home, it goes to the project picked in the switcher, or else your most recent project. A new project is only made when you have none."),
  bullet("The Free plan allows 2 projects. Starter allows 10. Pro and Studio have no limit."),
  ...steps([
    "**New project:** project switcher › `New Project` (or Library › Projects › `Create New`). The Studio opens on \"Start a new project\".",
    "**Rename, share or delete:** Library › `Projects` › the ⋯ on a project › `Members`, `Rename`, `Share` or `Delete`. Only the owner can rename, share or delete.",
    "**Share:** `Share project` › type the person's email (\"user@example.com\") › they get an email (\"Project shared\"). They find it under `Shared with me`. `Members` lists who has access; the owner can remove them.",
    "**Delete:** `Delete \"{name}\"?` cannot be undone. Everything in the project goes with it.",
  ]),
  shot("p1_project_switcher", "The project switcher: search, My projects or Shared, and `New Project`."),
  shot("p1_new_project", "Naming a new project, then `Create and open`."),
  h2("1.4  Inside the Studio"),
  table([2000, W - 2000], ["Part", "What it does"], [
    ["Left: the chat", "Talk to the agent. At the top, `New chat ▾` lists your chats (Rename, Delete) next to a New chat button. At the bottom: the message box (\"Describe your asset idea...\"), the `+` menu, `Type: Any ▾`, the mode pill and Send."],
    ["Chat | Tools switch", "Under the left panel. Swaps the chat for the Tools forms without leaving the project."],
    ["Right: Media", "Everything in this project, newest first. `All`, `Image`, `3D`, `Video` filters, `Search prompts`, `Edit`, `Sprites`, and the ⋯ menu (`Refresh`, `Grid size`, `Style Spec`, `Session flow`)."],
    ["Right: views", "The right side also opens the Edit view, Sprites, Style Spec, Rig, the Animation Studio and Flow. Each has a way back to Media."],
  ], { firstCol: true, firstColBold: true }),
  shot("p2_studio_ready", "The Studio: chat on the left (with idea chips when it's empty), Media on the right, the Chat | Tools switch at the bottom."),
  shot("p1_chat_history", "`New chat ▾` lists the chats in this project."),
  h2("1.5  Two ways to work: the agent or the tools"),
  table([2000, 3820, 3820], ["", "Agent (Studio chat)", "Tools"], [
    ["You give it", "What you want, in your own words", "The exact model and settings"],
    ["Good for", "Ideas, several steps in a row, sets of assets, \"make it like this one\"", "Repeatable single jobs with fixed settings"],
    ["Cost shown", "On the plan card (\"Total ≈ N credits\") and on next-step buttons", "On the `Generate ≈ N` button"],
    ["Where", "Sidebar › Create › `Studio`", "Sidebar › Create › `Tools`, or the `Chat | Tools` switch"],
  ], { firstCol: true, firstColBold: true }),
  h2("1.6  Chat modes"),
  p("The **mode pill** next to Send sets how much the agent checks with you first. Click it, or press Shift+Tab in the message box, to change it. Each chat remembers its own mode."),
  table([2000, 4840, 2800], ["Mode", "What happens", "Best for"], [
    ["`Ask, then plan`", "Up to 4 quick questions (pick an answer or \"Type your own…\"), then a plan to approve. Buttons: `Make the plan`, `Skip questions`.", "New ideas when you're unsure of the details"],
    ["`Plan` (default)", "A plan card comes first. Nothing is made until you approve it.", "Most work: you see the steps and cost first"],
    ["`Just make it`", "Goes straight to the finished result.", "Small, quick jobs you trust"],
  ], { firstCol: true }),
  shot("p1_mode_pill", "The mode pill: `Ask, then plan`, `Plan`, `Just make it`."),
  small("Guests (not signed in) can only use Just make it. The mode is locked while the Style Spec setup is on screen."),
  h2("1.7  Trying it without an account"),
  bullet("Visitors who aren't signed in get **one free try**: one asset, made in the chat (\"Your free try is ready — describe your asset in the chat\")."),
  bullet("Recipes, the Style Spec, Sprites, references, sets, downloads and remixing are locked for guests. Locked items show `Sign up to use`."),
  bullet("Signing up gives a free account with 100 credits and no credit card (\"Sign up — 100 free credits\"). The guest's try is moved into the new account."),
  h2("1.8  Help inside the app"),
  bullet("Sidebar › `Learn`: the \"Get set up\" checklist (first asset, Style Spec, a workflow, a coding agent, a plugin), plus tours (`What moved`, `Make your first asset`, `Your first workflow`), videos and articles."),
  bullet("Avatar › `Show tips again` brings back the hints in the Studio."),
  shot("p1_learn", "Learn: the Get set up checklist, tours and articles."),
);

// ---------------------------------------------------------------- part 2, levels 1-2
add(
  h1("Part 2 · 2D images"),
  p("From your first picture to sprite sheets and full asset sets. Each level builds on the one before."),
  levelBanner("Level 1 · First steps", "Make, find and download images", "Start here. Everything in this level takes a minute or less."),

  flow({ img: [["p1_home", "Home: type your idea, then Send."], ["p2_spec_setup", "A new project first offers a Style Spec: set one up, or `Skip for now`."], ["p2_working", "While it works, the chat shows progress."], ["p2_chat_result", "The result, with \"Take this character further\" next steps. It also appears in Media."]], id: "2D-1", title: "Make your first image from Home",
    when: "You have an idea and want a picture fast.",
    where: "Home › prompt box › Send (the orange ↑)",
    cost: "Shown on the plan card before anything is made. A Balanced image at 1K is 8 credits.",
    result: "An image in the chat and in the project's Media.",
    steps: [
      "Go to `Home`. Under \"What are you making today?\", keep `Ask the agent` selected.",
      "Type what you want, for example \"a wooden treasure chest, game prop, hand-painted style\".",
      "Optional: `+ Reference` adds an image to work from. Pick a past image with `Use image`, or `Upload new image`.",
      "Press Enter or the orange ↑. The Studio opens a new chat and sends your prompt.",
      "If this project has no Style Spec yet, the Studio first asks you to set one up (\"Set up your Style Spec to start…\"). Choose `Lock it` or `Skip for now` (see 2D-15).",
      "A plan card appears. Check the steps and \"Total ≈ N credits\", then click `Yes, generate`.",
      "The working line shows progress (\"Thinking…\", then each step). The image appears in the chat and in Media on the right.",
    ],
    tips: [
      "With 0 credits, Send opens the upgrade window instead.",
      "Home always starts in Plan mode. To stop seeing plans in this chat, click `Yes, and skip plans for this chat` on the first plan card.",
      "You can type the next prompt while one is still being made. It waits as a dimmed bubble; the x removes it.",
    ] }),

  flow({ img: [["p2_tools_image", "Tools › Image."]], id: "2D-2", title: "Make an image with Tools (you pick the model)",
    when: "You want full control over the model, size and settings.",
    where: "Sidebar › Create › Tools › `Image`, or Home › `Pick a tool` › `Create Image`",
    cost: "5 to 16 credits, shown on the `Generate` button.",
    result: "The image, saved to the open project (\"Saved to project\").",
    steps: [
      "Open Tools › Image. If no project is open, pick one under \"Choose a project\" (or `New project`). The panel says \"Image generation\".",
      "Pick a `Model` (see the table below).",
      "Optional: pick an `Asset type`, and add reference images in the `Add` tiles.",
      "Write the prompt (up to 2,000 characters).",
      "Set the `Output`: aspect ratio, size, and for some models background, format, negative prompt or seed.",
      "Optional: `Use library` adds your library's closest images as references. The `Style Spec` switch applies your locked style.",
      "Click `Generate ≈ N`. The status shows Starting…, Queued…, Generating… (\"Usually under a minute.\").",
      "On the result card, click `Open` or `Download`.",
    ],
    table: { widths: [2100, 3940, 1700, 1900], head: ["Model", "Best for", "Reference images", "Credits"], o: { firstCol: true, firstColBold: true }, rows: [
      ["High Quality", "Detailed images in a given style", "1", "5"],
      ["Balanced Image", "Following the prompt closely; sizes 1K, 2K, 4K", "up to 4", "8 / 12 / 16"],
      ["Text & Lettering", "Exact words in the image (logos, buttons, signs); transparent background option", "up to 4", "5"],
      ["Fast Image", "Quick drafts; negative prompt and seed", "none", "5"],
    ] },
    tips: [
      "With Fast Image, the same seed and prompt give you the same picture again.",
      "The asset types `Prop`, `UI` and `Icon` start with a transparent background.",
    ] }),

  flow({ img: [["p2_media_hover", "Hover a Media tile for Edit and Sprite."], ["p2_viewer", "The viewer: prompt, details, check badges and actions."], ["p2_viewer_download", "`Download ▾`: PNG, JPG or WebP."]], id: "2D-3", title: "Find, view and download your images",
    when: "You want to look at, compare or save what you made.",
    where: "Studio › Media (right side) › click a tile",
    cost: "Free. Image downloads are included on every plan, Free too.",
    steps: [
      "In the Studio, look at Media on the right. Click `Image` to see only images, or type in `Search prompts`.",
      "Click a tile. The viewer opens: the image on the left (arrows go through the others), details on the right.",
      "The details show the prompt (`Copy`), size, ratio, when it was made, credits used, and check badges.",
      "Click `Download ▾` and pick `PNG` (lossless, keeps transparency), `JPG` (smallest, white background) or `WebP` (small, keeps transparency).",
      "To change tile size: Media ⋯ › `Grid size` › Small, Medium or Large.",
    ],
    tips: [
      "Check badges tell you whether the result matches what you asked: \"Size matches\", \"Clean cut-out\" or \"Edges may need cleanup\", \"Seamless\" or \"Visible seams\", \"Text ✓ 'PLAY'\" or \"Text may differ\".",
      "Rate results with the stars under each chat result. At 3 stars or fewer it asks what went wrong; this helps the team fix it.",
    ] }),

  flow({ img: [["p2_more_moves", "`More moves` holds Sprite sheet, Remove background, Icon set, UI kit, Upscale and more."]], id: "2D-4", title: "Remove the background",
    when: "You need a cut-out on a transparent background: a sprite, icon or prop.",
    where: "Chat: the `Remove background` button under a result. Tools › Edit › `Remove background`. Or the `Remove background +3 credits` switch when you pick an asset type.",
    cost: "3 credits",
    steps: [
      "Under an image result, click `Remove background` (≈ 3). The image is attached and the tool is picked; nothing runs yet.",
      "Press Enter (or Send).",
      "The cut-out appears in the chat and Media. Download it as PNG or WebP to keep the transparency.",
    ],
    tips: ["In Tools: Edit › Model `Remove background` › add the image › `Generate ≈ 3`.", "Check the badge: \"Clean cut-out\" or \"Edges may need cleanup\"."] }),

  flow({ id: "2D-5", title: "Make an image bigger and sharper (Upscale)",
    when: "You need a larger, sharper version.",
    where: "Chat: the `Upscale` button under a result. Tools › Edit › `Upscale`.",
    cost: "3 credits",
    steps: ["Click `Upscale` under the result (or attach an image, then `+` › `Tools` › `Upscale`).", "Press Enter.", "The larger image is saved to Media."] }),

  flow({ img: [["p2_redo_dialog", "Redo writes a better prompt that you can change before it runs."]], id: "2D-6", title: "Get other versions: Variations and Redo",
    when: "You like the idea but want other takes (Variations), or the result missed and you want a better prompt (Redo).",
    where: "The `Variations` and `Redo` buttons under a chat result. `Variations` is also in the viewer.",
    cost: "Redo: 8, 12 or 16 credits (same size as the original). Variations: shown before you send.",
    steps: [
      "**Variations:** click `Variations`. The Image Variations recipe opens with your image attached and a short form for what to keep and what to change. Fill it in and press Enter.",
      "**Redo:** click `Redo`. The \"Redo this image\" window writes a better prompt (\"Writing a better prompt…\").",
      "Change the prompt if you like, or click `Use the original prompt`.",
      "Click `Redo · N credits`. Redo skips the plan and makes the image straight away.",
    ] }),
);

add(
  levelBanner("Level 2 · Control", "Steer the result: references, type, size, text, plans and edits", "Use these when the first result is close but not right."),

  flow({ img: [["p2_plus_menu", "The `+` menu."]], id: "2D-7", title: "Give the AI reference images",
    when: "The result should look like an image you have: a style, a character, a layout.",
    where: "Chat `+` › `Upload or reuse an image`. Drag images onto the chat. Home › `+ Reference`. Viewer › `Remix`.",
    cost: "Free to attach.",
    steps: [
      "In the Studio chat, click `+` › `Upload or reuse an image`.",
      "In \"Recent Images\", click `Use image` on a past image, or `Upload new image`. You'll see \"Image added\".",
      "Or drag files onto the chat (\"Drop images here · up to 4 files\").",
      "Say how to use it, for example \"same character, now holding a bow\". Send.",
    ],
    tips: [
      "`+` › `Use library` adds your project's closest images as references automatically. A chip shows \"Using: …\"; click it to turn it off (\"Library off\").",
      "`+` › `Web search` searches the web. Click a result to attach it (\"Reference added\").",
      "`+` › `Game search` opens \"Find a game's art style\". Type a game name or link to match its look.",
      "In the viewer, `Remix` puts that image into the chat as a reference.",
    ] }),

  flow({ img: [["p2_type_picker", "The Type picker."]], id: "2D-8", title: "Say what kind of asset it is",
    when: "You want the right framing and background for the job.",
    where: "Chat › `Type: Any ▾`. Tools › Image › `Asset type (optional)`.",
    cost: "Free to choose. Optional extras: `Remove background +3 credits`, texture `Made tileable +8 credits`.",
    table: { widths: [2000, W - 2000], head: ["Type", "What changes"], o: { firstCol: true, firstColBold: true }, rows: [
      ["Character", "Portrait 3:4, background kept. Next steps suggest Turnaround, Expressions and Poses."],
      ["Prop", "Transparent background. Next steps suggest Make it 3D and Icon set."],
      ["Building", "A single building, ready for Make it 3D."],
      ["Environment", "A full scene. Make it 3D, Remove background and Sprite sheet are hidden for scenes."],
      ["UI, Icon", "Transparent background, made for game interfaces."],
      ["Texture", "Made tileable (+8) so the edges repeat without seams."],
      ["Tileset (2–9)", "Opens the Tileset recipe instead (see Level 3)."],
    ] },
    tips: ["The type applies to normal chat prompts. When a tool or recipe is picked, the chat says \"Asset type applies to chat generations\"."] }),

  flow({ id: "2D-9", title: "Set the size, the shape and exact text",
    when: "You need a set size (a banner, a phone screen) or real words in the image.",
    where: "Chat `+` › `Aspect ratio & size`. Chat `+` › `Exact text`.",
    cost: "Size changes the price for Balanced Image only (8, 12 or 16). Exact text: 5 credits per image.",
    steps: [
      "`+` › `Aspect ratio & size`: pick Auto, 1:1, 4:3, 3:4, 16:9, 9:16, 3:2 or 2:3, and 1K, 2K or 4K. Anything other than Auto · 1K shows as a chip you can remove.",
      "`+` › `Exact text`: type the words (up to 80 characters), for example \"PLAY\" or \"GAME OVER\", then `Done`.",
      "Send your prompt. The words are drawn letter for letter and read back to check them.",
    ],
    tips: ["Exact text applies to your next message and only to new images, not edits or recipes.", "Look for the \"Text ✓\" badge on the result."] }),

  flow({ img: [["p2_plan_card", "A plan card: the step, its model and size, the cost, and four choices."]], id: "2D-10", title: "Plan, approve or change the plan",
    when: "You're in Plan or Ask, then plan mode (Plan is the default).",
    where: "Studio chat",
    cost: "The card shows each step's cost and \"Total ≈ N credits\".",
    steps: [
      "Send your request. The plan card shows \"Plan · follows Style Spec vN\", the goal, numbered steps (each with its Prompt and Refs) and the total.",
      "To change one step's prompt, click its pencil. `+` next to Refs adds up to 4 references.",
      "Pick one: `Yes, generate`, `Yes, and skip plans for this chat`, `Edit plan` (then `Approve edited plan` or `Cancel edits`), or `No, tell the AI what to change` (type it, then `Send`).",
      "The card folds to a line like \"Approved · 2 steps · 16 credits\" and the steps run in order.",
    ],
    tips: [
      "If the plan wants to save a new rule to your Style Spec, choose `Add` or `Just this time`.",
      "If your Style Spec changed since the plan was made: `Re-plan` or `Use plan as is`.",
      "In `Ask, then plan` mode the questions come first; answer them, then `Make the plan` (or `Skip questions`).",
    ] }),

  flow({ id: "2D-11", title: "Quick edits in the chat",
    when: "Small changes: \"make it night\", \"give him a red cape\", \"remove the hat\".",
    where: "Studio chat",
    cost: "An edit is 8 credits at 1K; the plan card shows it.",
    steps: [
      "Refer to the last result, or attach the image you want to change (viewer › `Remix`, or `+` › `Upload or reuse an image`).",
      "Optional, to change only one part: click the brush on the attached image (\"Highlight an area to edit\"). Paint with `Brush` (size 6–140) or `Eraser`, use `Undo` or `Clear`, then `Use this area`.",
      "Write what should change and send.",
    ],
    tips: ["Highlighting keeps the rest of the image exactly as it was.", "The pen on an attached image (\"Open in editor\") opens the full Edit view instead."] }),

  flow({ img: [["p2_edit_view", "The Edit view: tools on the left, the image in the middle, versions on the right, the prompt bar at the bottom."]], id: "2D-12", title: "The Edit view: a precise image editor",
    when: "Careful local edits, making the canvas bigger, moving things, comparing versions.",
    where: "Media tile › `Edit`. Viewer › `Edit`. The `Edit precisely` button under a chat result. Media toolbar › `Edit`. The pen on an attached image.",
    cost: "8 credits per edit. Some moves show \"Free\" or \"may be free\". If an edit fails: \"You weren't charged.\"",
    steps: [
      "Open an image in Edit. With nothing open, use `Browse Media` or `Upload image`.",
      "Pick a tool on the left rail (table below).",
      "Select the area: Brush, Lasso or Rectangle. `Add to selection` and `Subtract from selection` refine it.",
      "Describe the change in the bar: \"Describe what should change in the selected area…\".",
      "Optional: `Add reference` (up to 2, each marked Subject or Reference). The `Style:` chip keeps your Style Spec.",
      "Click `Generate` (or `Expand`, or `Blend into place`). The new version appears (\"Generating v2…\").",
      "`Compare` slides between before and after. The Versions panel lists every version; click an older one to go back. Editing an older one starts a new branch.",
      "`Export` › PNG, JPG or WebP. Or `Use in sprite sheet`.",
    ],
    table: { widths: [2300, 900, W - 3200], head: ["Tool", "Key", "What it does"], o: { firstCol: true, firstColBold: true }, rows: [
      ["Brush", "B", "Paint the area to change (size 4–240 px)"],
      ["Eraser", "E", "Take away from the painted area"],
      ["Lasso", "L", "Draw a free-hand selection"],
      ["Rectangle", "R", "Draw a box selection"],
      ["Expand canvas", "X", "Make the picture bigger (1:1, 4:3, 3:4, 16:9, 9:16, 21:9 or Custom), choose \"Where the image sits\"; the AI fills the new space"],
      ["Move & resize", "V", "Move or scale a selected part, then `Blend into place`"],
      ["Hand", "H", "Move around the picture"],
    ] },
    tips: ["Undo Ctrl+Z, Redo Ctrl+Shift+Z (Cmd on a Mac). `Focus` hides everything but the image.", "`Cancel` only stops waiting. The edit may still finish, appear in Media and use its credits."] }),

  flow({ img: [["p2_tools_edit", "Tools › Edit."]], id: "2D-13", title: "Edit with Tools (you pick the edit model)",
    when: "You want a specific edit model with fixed settings.",
    where: "Sidebar › Create › Tools › `Edit`, or Home › `Pick a tool` › `Edit Image`",
    cost: "3 to 16 credits, shown on the `Generate` button.",
    steps: ["Pick the `Model`.", "Add the image or images under \"Images to edit\".", "Write the \"Edit instruction\".", "Click `Generate ≈ N`.", "`Open` or `Download` the result."],
    table: { widths: [2300, 3940, 1400, 2000], head: ["Model", "Best for", "Images", "Credits"], o: { firstCol: true, firstColBold: true }, rows: [
      ["Smart Edit", "Most edits; follows instructions closely", "1–4", "8 / 12 / 16"],
      ["High Quality Edit", "Detailed results", "1–4", "5"],
      ["Quick Edit", "Fast, simple changes", "1–4", "5"],
      ["Multi-Image Edit", "Combine things from several images", "1–3", "5"],
      ["Precision Edit", "Change one thing, keep the rest; seed", "1", "5"],
      ["Remove background", "A clean cut-out", "1", "3"],
      ["Upscale", "Bigger and sharper", "1", "3"],
    ] } }),

  flow({ id: "2D-14", title: "Seamless textures",
    when: "Floors, walls and materials that repeat without visible seams.",
    where: "Chat `Type` › `Texture`. Viewer › `Make tileable · 8`. Edit view › `Make tileable · 8`.",
    cost: "8 credits to make an image tileable, plus the image itself.",
    steps: [
      "In the chat, set `Type` to `Texture` (the \"Made tileable +8 credits\" switch is on) and describe the material, for example \"mossy stone floor\".",
      "Open the result. `Tiled preview` shows it repeated so you can spot seams.",
      "Already have an image? Viewer › `Make tileable · 8` › confirm. It runs in the Edit view.",
      "Check the badge: \"Seamless ✓\" or \"Visible seams\".",
    ] }),
);

// ---------------------------------------------------------------- part 2, levels 3-4 (separate module)
add(advanced.levels(L));

// ---------------------------------------------------------------- parts 3 and 4 (separate module)
const G3 = require("./guide_3d");
add(G3.part3(L), G3.part4(L));

// ---------------------------------------------------------------- part 5
add(require("./guide_workflows").part5(L));
add(h1("Part 6 · Complete journeys"), p("Start-to-finish recipes for common game assets. Costs are typical, at 1K."), advanced.journeys(L));

// ---------------------------------------------------------------- part 6
add(
  h1("Part 7 · Credits and plans"),
  p("Every job costs credits. The price always shows before you spend: on the plan card, on a next-step button (≈ N) or on the `Generate` button. Prices below are from the live price list on 17 November 2026."),
  h2("6.1  Plans"),
  table([1500, 1500, 1700, 1500, W - 6200], ["Plan", "Price / month", "Credits / month", "Projects", "Notes"], [
    ["Free", "$0", "100", "2", "Up to 20 images and 10 image edits a month, one 3D model in total. Image downloads included; 3D downloads locked. No commercial use."],
    ["Starter", "$12", "600", "10", "Commercial use, downloads."],
    ["Pro", "$29", "1,800", "No limit", "Commercial use, downloads."],
    ["Studio", "$79", "6,000", "No limit", "Commercial use, downloads."],
  ], { firstCol: true, firstColBold: true }),
  small("Paying yearly takes 30% off. Credit packs: the first top-up is 500 credits for $5 (once per account), then 500 for $10, 1,200 for $20 or 3,500 for $50."),
  h2("6.2  What things cost"),
  table([5200, 1700, W - 6900], ["Job", "Credits", "Note"], [
    ["Balanced Image (1K / 2K / 4K)", "8 / 12 / 16", "The agent's usual image model"],
    ["High Quality, Text & Lettering, Fast Image", "5", ""],
    ["Smart Edit (1K / 2K / 4K)", "8 / 12 / 16", "Edit view edits and Redo use this price"],
    ["High Quality, Quick, Multi-Image, Precision Edit", "5", ""],
    ["Make tileable", "8", ""],
    ["Remove background, Upscale, Segment", "3", ""],
    ["Sprite sheet, per frame", "11", "One edit plus one background removal; +8 when there's no source picture"],
    ["Image to 3D, Text to 3D", "35", "HD texture +10, 8K +20, detailed geometry +20, quads +5, parts +10"],
    ["Texture a model or part", "20", "+10 for HD"],
    ["Rig a character", "40", ""],
    ["Standard animation moves", "20", "+15 per extra move, up to 5"],
    ["Save an Animation Studio clip", "150", ""],
    ["3D format conversion", "10", "Paid plans or after a credit pack"],
    ["Optimise a model", "5", ""],
    ["Video", "5 per second", "A 5-second clip is 25"],
    ["Rig check, importing a model, palette snap", "Free", ""],
  ], { firstCol: true }),
  h2("6.3  Your balance"),
  shot("p6_credits_modal", "Credits & plan: your plan, credits left and `Top up`."),
  bullet("The credits pill in the top bar shows your balance. Click it for `Overview` and `History`."),
  bullet("Avatar › `Credits & usage` shows the same."),
  bullet("Running low? The chat warns: \"You have X; this needs ≈ Y.\" At 0, you'll see a window with `Go Pro — $29/month` and `Buy credits from $10`."),
  bullet("Earn credits: share to the Gallery (+50 for your first approved item, then +5 per image or +10 per 3D model, up to 150 a month, plus bonuses at 10 and 50 likes), or the gift icon (`Earn credits`)."),
);

// ---------------------------------------------------------------- part 7
add(
  h1("Part 8 · Problems and answers"),
  table([3800, W - 3800], ["You see", "What to do"], [
    ["\"Set up your Style Spec to start…\"", "Choose `Lock it` to set a style for the project, or `Skip for now`. Your prompt sends right after."],
    ["\"Generation failed\" with `Try again`", "Read the reason under it. Click `Try again`, or change the prompt or image."],
    ["\"Not enough credits for this generation.\"", "Buy a credit pack or upgrade from the credits pill."],
    ["\"This image was rejected under the content policy.\"", "Try another image or change the wording."],
    ["\"That edit didn't go through — You weren't charged.\"", "Click `Retry`."],
    ["\"Still working… (busy, retrying)\"", "Wait a little. `Cancel` stops waiting, but the job may still finish, show up in Media and use its credits."],
    ["Your prompt shows as a dimmed bubble", "It's queued and starts when the current job has started. The x removes it."],
    ["The result ignores your style", "Turn on the Style Spec, add references, or turn on `Use library`."],
    ["Words in the image are wrong", "Use `+` › `Exact text`, then check the \"Text ✓\" badge."],
    ["\"You've made your free 3D model\"", "The Free plan includes one 3D model. Upgrade or buy credits for more."],
    ["The 3D Download button has a lock", "3D downloads need a paid plan or a credit pack. You can still preview, rig and animate."],
    ["`Create New` project shows \"Included with Starter\"", "Free allows 2 projects. Upgrade, or delete one you no longer need."],
    ["\"Rigging failed\", or limbs move strangely", "Make the character image again in a T-pose (full body, arms straight out, plain background), remove the background, Make it 3D, then rig again."],
    ["\"{name} has no skeleton yet\"", "Click `Rig it`, then `Animate` again."],
    ["Can't find something you made", "Check the open project (project switcher), then Media › `All` and `Search prompts`."],
  ], { firstCol: true }),
  gap(),
  p("More help: Sidebar › `Learn` (tours, videos, articles), avatar › `Show tips again`, and the Discord link on the Integrations page."),
  small("Prices and plan limits change from time to time. The app always shows the current price before anything runs."),
);

fs.writeFileSync(out, "");
L.Packer.toBuffer(build(C, "Rapid Assets · Studio Guide Book")).then((b) => {
  fs.writeFileSync(out, b);
  console.log("wrote", out, b.length);
  if (L.missing.length) console.log("missing shots:", [...new Set(L.missing)].join(", "));
});
