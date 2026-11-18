# Rapid Assets — Studio Guide

Interactive, self-playing guide to Rapid Assets Studio (2D, 3D, rig & animate, recipes, all 14 workflows,
sprite sheets), plus the Word handbook.

## Open it
`dist/index.html` — one self-contained file (screens and clips embedded). Open it in a browser, no server needed.
Keys: ← → step · Space play/pause · T Watch / Try it · V voice · F full screen.

## Build
```
python build.py            # -> dist/index.html
```

## Layout
| Path | What |
|---|---|
| `src/tour.template.html` | The guide: chapters (`CH`), steps (`STEPS`), player engine, narration captions |
| `assets/screens/` | Real prod screenshots (JPG, 1440 or 1754 wide) + `index.json` sizes |
| `assets/clips/` | Animation-studio clips (VP9 WebM) played on the Tune / Locks steps |
| `dist/index.html` | Built guide (what gets hosted) |
| `handbook/` | Word handbook generator (docx-js: `node guide.js out.docx`) and the latest `.docx` |
| `tools/capture/` | Playwright scripts that captured the screens on prod (headless, anonymised) |
| `tools/patches/` | History of the edit scripts applied to the template (reference only) |

## Step format
`{ch, img, vid?, act: look|click|type|drag, t: [x,y,w,h] %, ring2?, box?, type?, z, keep?, dur?, title, text}`
— `t` is the highlighted target in % of the screen, `z` the camera zoom, `vid` a clip from `assets/clips`.
