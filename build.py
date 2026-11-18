"""Build the interactive guide: embed the screens (assets/screens) and clips (assets/clips) into one
self-contained HTML file -> dist/index.html.   usage: python build.py [out.html]"""
import base64, glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCREENS = os.path.join(HERE, "assets", "screens")
CLIPS = os.path.join(HERE, "assets", "clips")
tpl = open(os.path.join(HERE, "src", "tour.template.html"), encoding="utf-8").read()

names = sorted(set(re.findall(r'img:"([a-z][0-9a-z]*_[a-z0-9_]+)"', tpl)) | {"p1_home"})
imgs = {}
for n in names:
    data = open(os.path.join(SCREENS, n + ".jpg"), "rb").read()
    imgs[n] = "data:image/jpeg;base64," + base64.b64encode(data).decode()

prompt = os.environ.get("ANIM_PROMPT", "Run in place in a steady loop: knees up, arms swinging, a slight forward lean. Keep the shield arm still.")
prompt2 = os.environ.get("ANIM_PROMPT2", "Make it faster with bigger strides, and keep both arms and hands still.")

vids = {}
for vf in sorted(glob.glob(os.path.join(CLIPS, "*.webm"))):
    vids[os.path.splitext(os.path.basename(vf))[0]] = "data:video/webm;base64," + base64.b64encode(open(vf, "rb").read()).decode()

out = (tpl.replace("/*IMAGES*/{}", json.dumps(imgs)).replace("/*VIDS*/{}", json.dumps(vids))
       .replace("/*PROMPT*/", json.dumps(prompt)[1:-1]).replace("/*PROMPT2*/", json.dumps(prompt2)[1:-1]))
dst = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "dist", "index.html")
os.makedirs(os.path.dirname(dst), exist_ok=True)
open(dst, "w", encoding="utf-8").write(out)
print(len(names), "screens,", len(vids), "clips,", round(len(out) / 1e6, 1), "MB ->", dst)
