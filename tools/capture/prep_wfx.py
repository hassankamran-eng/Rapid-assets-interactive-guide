import glob, json, os
from PIL import Image
idx = json.load(open("jpg/index.json"))
n = 0
for f in sorted(glob.glob("out_wfx/y_*.png")):
    k = os.path.splitext(os.path.basename(f))[0]
    im = Image.open(f).convert("RGB"); im = im.resize((1440, round(im.height * 1440 / im.width)), Image.LANCZOS)
    im.save(f"jpg/{k}.jpg", quality=78, optimize=True); idx[k] = [im.width, im.height]; n += 1
json.dump(idx, open("jpg/index.json", "w"), indent=0)
print(n, "template shots")
