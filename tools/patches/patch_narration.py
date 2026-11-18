"""Narrated subtitle-style caption over the stage (word-by-word reveal, WHAT/WHERE/WHEN/HOW labels, optional voice)."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
f = os.path.join(HERE, "tour.template.html")
s = open(f, encoding="utf-8").read()

def rep(old, new):
    global s
    assert s.count(old) == 1, (old[:70], s.count(old))
    s = s.replace(old, new)

if "/* ---- narration ---- */" in s:
    raise SystemExit("already patched")

CSS = """
/* ---- narration ---- */
.narr{position:absolute;left:50%;transform:translateX(-50%);bottom:3.5%;width:min(76%,1180px);z-index:8;
  background:rgba(9,10,11,.88);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);
  border:1px solid rgba(255,255,255,.09);border-left:5px solid var(--orange);border-radius:16px;
  padding:calc(var(--u)*1.05) calc(var(--u)*1.6) calc(var(--u)*1.2);box-shadow:0 22px 60px rgba(0,0,0,.6);
  opacity:0;transition:opacity .35s ease;pointer-events:none}
.narr.on{opacity:1}
.narr.top{bottom:auto;top:3.5%}
.narr .nk{font-size:calc(var(--u)*.78);letter-spacing:.16em;text-transform:uppercase;color:var(--orange);font-weight:700;margin-bottom:.3em}
.narr .nt{font-family:"Inter Tight",Inter,sans-serif;font-weight:700;color:#fff;font-size:calc(var(--u)*1.6);line-height:1.15;margin-bottom:.4em}
.narr .nl{color:#ececec;font-size:calc(var(--u)*1.22);line-height:1.5;margin:.15em 0}
.narr .nl b{color:var(--orange2);font-weight:800;letter-spacing:.05em;margin-right:.45em;font-size:.86em}
.narr .w{opacity:.08;transition:opacity .22s ease}
.narr .w.on{opacity:1}
.cap p{display:none}
.vbtn.on{background:rgba(249,115,22,.16);border-color:var(--orange)}
"""
rep("</style>", CSS + "</style>")

# caption element inside the stage (not zoomed with the camera)
rep('        <div class="cover" id="intro">', '        <div class="narr" id="narr"><div class="nk" id="nk"></div><div class="nt" id="nt"></div><div id="nb"></div></div>\n        <div class="cover" id="intro">')
# voice toggle next to Full screen
rep('<button class="lbtn" id="fsBtn"', '<button class="lbtn vbtn" id="voiceBtn" title="Read the captions aloud (V)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M11 5 6 9H3v6h3l5 4z"/><path d="M15.5 8.5a5 5 0 0 1 0 7M18.5 5.5a9 9 0 0 1 0 13"/></svg>Voice</button>\n          <button class="lbtn" id="fsBtn"')

JS = r"""
/* ---------- narration ---------- */
let voiceOn = false;
try { voiceOn = localStorage.getItem("ra_voice") === "1"; } catch (e) {}
const LABELS = /(WHAT:|WHERE:|WHEN:|HOW:)/;
function narrLines(text) {
  const parts = text.split(LABELS).filter(x => x && x.trim());
  const lines = []; let cur = null;
  for (const p of parts) {
    if (LABELS.test(p)) { cur = { label: p.replace(":", ""), text: "" }; lines.push(cur); }
    else if (cur && !cur.text) cur.text = p.trim();
    else lines.push({ label: "", text: p.trim() });
  }
  return lines.length ? lines : [{ label: "", text }];
}
function speakText(t) {
  return new Promise(res => {
    if (!voiceOn || !window.speechSynthesis) return res();
    speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(t.replace(/[·›]/g, ",").replace(/×/g, " times"));
    u.rate = Math.min(1.6, 1.02 * speed); u.onend = res; u.onerror = res;
    const v = speechSynthesis.getVoices().find(v => /en-(US|GB)/.test(v.lang) && /Natural|Aria|Jenny|Guy|Google/.test(v.name)) || speechSynthesis.getVoices().find(v => /^en/.test(v.lang));
    if (v) u.voice = v;
    speechSynthesis.speak(u);
  });
}
async function narrate(s, id) {
  const n = $("narr");
  const chName = (CH.find(c => c.id === s.ch) || {}).name || "";
  $("nk").textContent = chName;
  $("nt").textContent = s.title;
  const nb = $("nb"); nb.innerHTML = "";
  const words = [];
  for (const ln of narrLines(s.text)) {
    const d = document.createElement("div"); d.className = "nl";
    if (ln.label) { const b = document.createElement("b"); b.textContent = ln.label; d.appendChild(b); }
    ln.text.split(/\s+/).forEach((w, i) => { const sp = document.createElement("span"); sp.className = "w"; sp.textContent = (i ? " " : "") + w; d.appendChild(sp); words.push(sp); });
    nb.appendChild(d);
  }
  const ty = s.t[1] + s.t[3] / 2;
  n.classList.toggle("top", ty > 56);
  n.classList.add("on");
  const spoken = speakText(s.title + ". " + s.text.replace(/(WHAT|WHERE|WHEN|HOW):/g, "$1,"));
  for (const w of words) { if (!alive(id)) return; w.classList.add("on"); await sleep(voiceOn ? 230 : 70); }
  await spoken;
}
$("voiceBtn").classList.toggle("on", voiceOn);
$("voiceBtn").onclick = () => {
  voiceOn = !voiceOn; $("voiceBtn").classList.toggle("on", voiceOn);
  try { localStorage.setItem("ra_voice", voiceOn ? "1" : "0"); } catch (e) {}
  if (!voiceOn && window.speechSynthesis) speechSynthesis.cancel();
};
document.addEventListener("keydown", e => { if (e.key === "v" || e.key === "V") $("voiceBtn").click(); });
"""
rep("/* ---------- boot ---------- */", JS + "\n/* ---------- boot ---------- */")

# start narration when a step starts; in Watch mode wait for it before moving on
rep('  updateUI(i);\n', '  updateUI(i);\n  if (window.speechSynthesis) speechSynthesis.cancel();\n  $("narr").classList.remove("on");\n')
rep('  await setShot(s.img);                if (!alive(id)) return;',
    '  await setShot(s.img);                if (!alive(id)) return;\n  const narrDone = narrate(s, id);')
rep('  if (!playing) return;\n  await sleep(read);                   if (!alive(id) || !playing) return;',
    '  if (!playing) return;\n  await Promise.all([sleep(read), narrDone]);   if (!alive(id) || !playing) return;\n  await sleep(500);                     if (!alive(id) || !playing) return;')
rep("function finish() {", 'function finish() {\n  $("narr").classList.remove("on"); if (window.speechSynthesis) speechSynthesis.cancel();')
rep('<kbd>T</kbd> Watch / Try it &nbsp; <kbd>F</kbd> full screen', '<kbd>T</kbd> Watch / Try it &nbsp; <kbd>V</kbd> voice &nbsp; <kbd>F</kbd> full screen')
open(f, "w", encoding="utf-8").write(s)
print("narration applied")
