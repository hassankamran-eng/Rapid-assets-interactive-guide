"""PNG screenshots (out/) -> 1600-px JPEGs (jpg/) + index.json {name: [w, h]} for the guide generator."""
import glob, json, os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC, DST = os.path.join(HERE, "out"), os.path.join(HERE, "jpg")
os.makedirs(DST, exist_ok=True)
index = {}
for f in sorted(glob.glob(os.path.join(SRC, "p*.png"))):
    name = os.path.splitext(os.path.basename(f))[0]
    im = Image.open(f).convert("RGB")
    if im.width > 1600:
        im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
    im.save(os.path.join(DST, name + ".jpg"), quality=82, optimize=True)
    index[name] = [im.width, im.height]
json.dump(index, open(os.path.join(DST, "index.json"), "w"), indent=0)
print(len(index), "shots ->", DST)
