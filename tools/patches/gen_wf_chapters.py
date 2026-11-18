"""Make one tour chapter per workflow template from the real runs (shots/out_wfx + wfx_rects_*.json)."""
import glob, json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
SH = os.path.join(os.path.dirname(HERE), "shots")
slug = lambda t: re.sub(r"[^a-z0-9]+", "_", t.lower()).strip("_")

INFO = {
    "Background Removal": (3, "Cuts every image out of its background: clean transparent cut-outs.", "the knight image"),
    "Character Facial Pose Sheet": (3, "Turns a character image into one sheet of the same face in many expressions.", "the knight as the Character"),
    "Character Turnaround": (3, "Turns a character image into a front, side and back turnaround.", "the knight as the Character"),
    "Color Palette Extraction": (4, "Pulls the main colours out of an image, with hex codes.", "the knight image"),
    "Icon Set": (15, "Makes a matching set of six game icons on transparent backgrounds, in the style of your reference.", "the knight as Style reference, and a Theme: shop currency and rewards"),
    "Image Analysis": (4, "Describes an image's art style, colours, characters and setting in words.", "the knight image"),
    "Parallel Pose Edits": (4, "Redraws your character in several new body poses at once.", "the knight as the Character"),
    "Parallel Image Variations": (4, "Makes several variations of one image, each with its own change.", "the knight as Reference"),
    "Pose Transfer": (4, "Puts your character into the pose from a reference picture.", "the knight as Target character and a walking knight as Pose reference"),
    "Seasonal Re-theme": (7, "Re-themes a batch of game assets for a season or event.", "the knight, and a Theme: winter, snow and frosty light"),
    "Texture 3D Model": (4, "Repaints a 3D model's surface to match a texture reference picture.", "a 3D model (GLB) and the knight as Texture reference"),
    "Tileset": (8, "Makes seamless ground tiles that fit together, in the style of your reference.", "the knight as Style reference, and a Theme: grass, stones and a dirt path"),
    "UI Kit": (21, "Makes a matching game UI kit, from buttons to panels, in your style.", "the knight as Style reference, and a Theme: fantasy RPG menu with PLAY, SHOP and SETTINGS"),
}

rects = {}
for f in glob.glob(os.path.join(SH, "wfx_rects_*.json")):
    rects.update(json.load(open(f)))
have = lambda n: os.path.exists(os.path.join(SH, "out_wfx", n + ".png"))

def cost_line(t):
    if not t:
        return ""
    m = re.search(r"(\d+ steps?[^\n]*?credits)", t.replace("\n", " "))
    return m.group(1) if m else ""

def r(v, d):
    return json.dumps(v if v else d)

chs, steps = [], []
for name, (n, what, gave) in INFO.items():
    s = slug(name); R = rects.get(name)
    if not R or not have(f"y_{s}_card"):
        continue
    cid = "t_" + s
    chs.append(f'  {{id:"{cid}", name:"{name}", sub:"{n} steps · real run", group:"Workflows"}},')
    st = []
    st.append(f' {{ch:"{cid}", img:"y_{s}_card", act:"click", t:{r(R.get("card"), [30,30,13,15])}, z:1.3, title:"Pick {name}", text:"New workflow › From template › {name}. {what}"}},')
    if have(f"y_{s}_editor"):
        st.append(f' {{ch:"{cid}", img:"y_{s}_editor", act:"look", t:{r(R.get("canvas"), [22,20,55,70])}, z:1.05, title:"Its {n} steps", text:"Use template opens the editor with the {n} steps already joined up. You can run it as it is, or change any step first."}},')
        if R.get("run_btn"):
            st.append(f' {{ch:"{cid}", img:"y_{s}_editor", act:"click", t:{r(R.get("run_btn"), [91.6,7.7,3.8,4.8])}, z:1.5, title:"Run", text:"Click Run."}},')
    if have(f"y_{s}_inputs"):
        st.append(f' {{ch:"{cid}", img:"y_{s}_inputs", act:"click", t:{r(R.get("check"), [59,73,9,5])}, ring2:{r(R.get("dialog"), [30,15,40,70])}, z:1.25, title:"Give it the inputs", text:"Here: {gave}. Then Check the cost: nothing is charged yet."}},')
    if have(f"y_{s}_cost"):
        cl = cost_line(R.get("cost_text"))
        cl = f" {cl}." if cl else ""
        st.append(f' {{ch:"{cid}", img:"y_{s}_cost", act:"click", t:{r(R.get("confirm"), [64,69.6,3.6,3.8])}, ring2:{r(R.get("cost_dialog"), [30,23,39,54])}, z:1.3, title:"Check the cost, then Run", text:"The window shows what runs and the credit range before anything is charged.{cl} Click Run."}},')
    if have(f"y_{s}_running"):
        st.append(f' {{ch:"{cid}", img:"y_{s}_running", act:"look", t:[18,8,56,88], z:1.05, title:"It runs step by step", text:"Each step shows Done, Running or Up next, with its results underneath. It is safe to close the tab."}},')
    if have(f"y_{s}_review"):
        st.append(f' {{ch:"{cid}", img:"y_{s}_review", act:"click", t:{r(R.get("keep"), [20,15,12,3])}, z:1.35, title:"Review", text:"Results that the quality check flags wait for you: Keep this result on the ones you want, then Run from here to finish."}},')
    if have(f"y_{s}_result"):
        st.append(f' {{ch:"{cid}", img:"y_{s}_result", act:"look", t:{r(R.get("status"), [18,10,50,4])}, ring2:{r(R.get("downloads"), [74,24,24,10])}, z:1.15, title:"Finished", text:"The run page shows how many steps finished. Downloads on the right lists the files to save."}},')
    if have(f"y_{s}_outputs"):
        st.append(f' {{ch:"{cid}", img:"y_{s}_outputs", act:"look", t:[18,8,56,88], z:1.05, title:"The results", text:"{what}"}},')
    steps += st + [""]

tpl = os.path.join(HERE, "tour.template.html")
s = open(tpl, encoding="utf-8").read()
s = re.sub(r"\n  \{id:\"t_[^\n]*", "", s)
s = re.sub(r"\n \{ch:\"t_[^\n]*", "", s)
a = s.index('  {id:"sprites"')
s = s[:a] + "\n".join(chs) + "\n" + s[a:]
s = s.replace('{id:"wf", name:"Workflows", sub:"Build once, run on a batch"}', '{id:"wf", name:"How workflows work", sub:"Batch Variations · real run", group:"Workflows"}')
if 'group:"2D animation"' not in s:
    s = re.sub(r'(\{id:"sprites"[^}]*)\}', r'\1, group:"2D animation"}', s, count=1)
st_a = s.index('\n {ch:"sprites"')
s = s[:st_a] + "\n" + "\n".join(steps) + s[st_a:]
open(tpl, "w", encoding="utf-8").write(s)
print(len(chs), "template chapters,", sum(1 for x in steps if x), "steps")

# SEASONAL_MANUAL: no real run possible (prod keeps "Pick a theme first" after a theme is chosen)
if have("y_seasonal_re_theme_editor") and not any('t_seasonal' in c for c in chs):
    cid = "t_seasonal_re_theme"
    chs.append('  {id:"t_seasonal_re_theme", name:"Seasonal Re-theme", sub:"7 steps · set the theme", group:"Workflows"},')
    steps += [
     ' {ch:"t_seasonal_re_theme", img:"y_seasonal_re_theme_card", act:"look", t:[15,8,70,84], z:1, title:"Pick Seasonal Re-theme", text:"New workflow › From template › Seasonal Re-theme (7 steps): re-themes a batch of game assets for a season or event, keeping each subject the same."},',
     ' {ch:"t_seasonal_re_theme", img:"y_seasonal_re_theme_editor", act:"look", t:[25,50,50,13], z:1.15, title:"Its 7 steps", text:"Assets › For each › Re-theme › Cut out › Review › Collect › Export. The Re-theme step needs a theme before it can run."},',
     ' {ch:"t_seasonal_re_theme", img:"y_seasonal_re_theme_settings", act:"click", t:[40,52.8,5,8], ring2:[80,36,19.5,25], z:1.3, title:"Open the Re-theme step", text:"Click the Re-theme step. Its settings open on the right: Season or event, Describe the theme, Theme references."},',
     ' {ch:"t_seasonal_re_theme", img:"y_seasonal_re_theme_theme", act:"click", t:[86.5,48,9.3,3.6], ring2:[80,63.6,19.5,10], z:1.45, title:"Pick a season and describe it", text:"Pick Halloween, Winter Holidays, Lunar New Year, Summer, Valentine’s or Custom, and optionally describe it (snow on the armour, frosty blue light). Then Save and Run."},',
    ]
    steps.append("")
    tpl2 = os.path.join(HERE, "tour.template.html")
    s2 = open(tpl2, encoding="utf-8").read()
    NL = chr(10)
    a2 = s2.index('  {id:"sprites"'); s2 = s2[:a2] + chs[-1] + NL + s2[a2:]
    st2 = s2.index(NL + ' {ch:"sprites"'); s2 = s2[:st2] + NL + NL.join(steps[-5:]) + s2[st2:]
    open(tpl2, 'w', encoding='utf-8').write(s2)
    print('seasonal chapter added')
