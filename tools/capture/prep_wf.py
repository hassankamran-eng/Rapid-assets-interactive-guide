import glob, json, os
from PIL import Image
idx = json.load(open("jpg/index.json"))
for f in sorted(glob.glob("out_wf/w_*.png")):
    n = os.path.splitext(os.path.basename(f))[0]
    im = Image.open(f).convert("RGB"); im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
    im.save(f"jpg/{n}.jpg", quality=82, optimize=True); idx[n] = [im.width, im.height]
json.dump(idx, open("jpg/index.json", "w"), indent=0)
print(len([k for k in idx if k.startswith("w_")]), "workflow shots")
