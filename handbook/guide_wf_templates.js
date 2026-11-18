// One handbook section per workflow template, from the real runs (shots in GUIDE_SHOTS as y_<slug>_*.jpg, rects/costs in WFX_DIR).
const fs = require("fs");
const path = require("path");

const INFO = [
  ["Background Removal", 3, "Cuts every image out of its background: clean transparent cut-outs.", "Image: the images to cut out (up to 20)."],
  ["Character Facial Pose Sheet", 3, "Turns a character image into one sheet of the same face in many expressions.", "Character: one or more character images."],
  ["Character Turnaround", 3, "Turns a character image into a front, side and back turnaround.", "Character: one or more character images (full body works best)."],
  ["Color Palette Extraction", 4, "Pulls the main colours out of an image, with hex codes.", "Image: the images to read colours from."],
  ["Icon Set", 15, "Makes a matching set of six game icons on transparent backgrounds, in the style of your reference.", "Style reference image(s) + Theme (for example: shop currency and rewards)."],
  ["Image Analysis", 4, "Describes an image's art style, colours, characters and setting in words.", "Image: the images to describe."],
  ["Parallel Pose Edits", 4, "Redraws your character in several new body poses at once.", "Character: the character image(s)."],
  ["Parallel Image Variations", 4, "Makes several variations of one image, each with its own change.", "Reference: the image(s) to vary."],
  ["Pose Transfer", 4, "Puts your character into the pose from a reference picture.", "Target character image(s) + one Pose reference picture for the whole run."],
  ["Seasonal Re-theme", 7, "Re-themes a batch of game assets for a season or event.", "The images to re-theme + Theme (for example: winter)."],
  ["Texture 3D Model", 4, "Repaints a 3D model's surface to match a texture reference picture.", "Model: 3D files (GLB, FBX, OBJ or STL, up to 30 MB) + one Texture reference picture."],
  ["Tileset", 8, "Makes seamless ground tiles that fit together, in the style of your reference.", "Style reference image(s) + Theme (for example: grass, stones and a dirt path)."],
  ["UI Kit", 21, "Makes a matching game UI kit, from buttons to panels, in your style.", "Style reference image(s) + Theme (for example: fantasy RPG menu with PLAY, SHOP, SETTINGS)."],
];
const slug = (t) => t.toLowerCase().replace(/[^a-z0-9]+/g, "_").replace(/^_|_$/g, "");

function sections(L) {
  const { flow, levelBanner, small } = L;
  const dir = process.env.WFX_DIR || "";
  let rects = {};
  if (dir && fs.existsSync(dir)) for (const f of fs.readdirSync(dir)) if (/^wfx_rects_.*\.json$/.test(f)) Object.assign(rects, JSON.parse(fs.readFileSync(path.join(dir, f), "utf8")));
  const out = [levelBanner("Every workflow, one by one", "A real run of each template", "Each template below was run for real on rapidassets.ai with the knight images. Batch Variations is the example in W-2 to W-7.")];
  let n = 8;
  for (const [name, steps, what, inputs] of INFO) {
    const s = slug(name), R = rects[name] || {};
    const m = (R.cost_text || "").replace(/\n/g, " ").match(/(\d+ steps?[^.]*?credits)/);
    out.push(...flow({ id: `W-${n++}`, title: name,
      img: [[`y_${s}_card`, `New workflow › From template › ${name} (${steps} steps).`], [`y_${s}_editor`, "The template's steps in the editor."],
            [`y_${s}_inputs`, "The inputs it asks for."], [`y_${s}_cost`, "The cost before anything runs."],
            [`y_${s}_result`, "The finished run."], [`y_${s}_outputs`, "The results."]],
      when: what,
      where: "Sidebar › Workflows › New workflow › From template",
      cost: m ? `In this run: ${m[1]}. The window always shows the range before you run.` : "Shown in the run window before anything is charged.",
      result: inputs,
      steps: [
        `\`New workflow\` › pick the project › \`From template\` › **${name}** › \`Use template\`.`,
        "Check the steps in the editor; change any setting if you like, then `Save`.",
        "`Run` › add the inputs" + (/Theme/.test(inputs) ? " and type the Theme" : "") + " › `Check the cost`.",
        "Click `Run`. Follow it on the run page; `Keep this result` on anything waiting for review.",
        "Save the files from Downloads on the run page.",
      ] }));
  }
  out.push(small("Prices are what these runs showed on 18 November 2026; the run window always shows the current range."));
  return out;
}
module.exports = { sections };
