"""Full-screen layout: stage fills the viewport, chapters become a slide-out drawer, slim bottom bar, real fullscreen toggle."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
f = os.path.join(HERE, "tour.template.html")
s = open(f, encoding="utf-8").read()

def rep(old, new):
    global s
    assert s.count(old) == 1, (old[:70], s.count(old))
    s = s.replace(old, new)

CSS = """
/* ---- full-screen layout ---- */
:root{--dockh:78px}
.app{display:block;height:100vh;overflow:hidden}
.rail{position:fixed;left:0;top:0;bottom:0;width:320px;z-index:60;transform:translateX(-102%);transition:transform .32s cubic-bezier(.4,0,.2,1);box-shadow:24px 0 60px rgba(0,0,0,.6)}
.rail.open{transform:none}
.scrim{position:fixed;inset:0;background:rgba(0,0,0,.45);z-index:55;opacity:0;pointer-events:none;transition:opacity .3s}
.scrim.on{opacity:1;pointer-events:auto}
.main{height:100vh;padding:0;gap:0;display:flex;flex-direction:column;align-items:stretch}
.stagewrap{flex:1;min-height:0;display:flex;align-items:center;justify-content:center;background:#000}
.window{width:min(100vw, calc((100vh - var(--dockh)) * 1.6));border:0;border-radius:0;box-shadow:none}
.chrome{display:none}
.dock{width:100%;height:var(--dockh);display:grid;grid-template-columns:auto 1fr auto;gap:18px;align-items:center;padding:0 18px;background:#0c0d0e;border-top:1px solid var(--line);position:relative}
.dock .progress{position:absolute;left:0;right:0;top:-1px;height:3px;border-radius:0}
.cap{min-height:0;overflow:hidden}
.cap .meta{font-size:10.5px}
.cap h2{font-size:17px;margin:2px 0 1px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.cap p{font-size:13.5px;line-height:1.38;max-width:none;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.cap .hint{position:absolute;right:18px;top:-30px;margin:0;background:var(--orange);color:#160b02;font-weight:600;padding:4px 10px;border-radius:99px;font-size:12px}
.ctrls{flex-direction:row;align-items:center;gap:10px}
.lbtn{height:40px;padding:0 14px;border-radius:11px;border:1px solid var(--line2);background:rgba(255,255,255,.03);display:inline-flex;align-items:center;gap:8px;font-size:13.5px;font-weight:500;white-space:nowrap}
.lbtn:hover{background:rgba(255,255,255,.08)}
.lbtn svg{width:16px;height:16px}
.lbtn .cn{color:var(--orange);font-weight:600}
@media (max-width: 980px){
  :root{--dockh:120px}
  .dock{grid-template-columns:1fr;grid-template-rows:auto auto;padding:8px 12px;gap:6px;height:var(--dockh)}
  .dock .lbtn.chap-btn{position:absolute;top:8px;right:12px}
  .ctrls{justify-content:flex-start}
  .rail{width:86vw}
  .chapters{display:block}
}
"""
rep("</style>", CSS + "</style>")

# wrap the window in a stage area, add drawer scrim + buttons in the dock
rep('  <main class="main">\n    <div class="window">', '  <div class="scrim" id="scrim"></div>\n  <main class="main">\n    <div class="stagewrap"><div class="window">')
rep('''      </div>
    </div>
    <div class="dock">''', '''      </div>
    </div></div>
    <div class="dock">
      <button class="lbtn chap-btn" id="chapBtn" title="Chapters (C)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 6h16M4 12h16M4 18h10"/></svg>Chapters <span class="cn" id="chapNo"></span></button>''')
rep('''        <div class="row">
          <div class="seg" id="mode">''', '''        <div class="row">
          <button class="lbtn" id="fsBtn" title="Full screen (F)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/></svg>Full screen</button>
          <div class="seg" id="mode">''')

JS = """
/* ---------- drawer + fullscreen ---------- */
const rail = document.querySelector(".rail");
function drawer(open) { rail.classList.toggle("open", open); $("scrim").classList.toggle("on", open); }
$("chapBtn").onclick = () => drawer(!rail.classList.contains("open"));
$("scrim").onclick = () => drawer(false);
document.getElementById("chapters").addEventListener("click", e => { if (e.target.closest(".chap")) drawer(false); });
function toggleFs() {
  if (!document.fullscreenElement) document.documentElement.requestFullscreen && document.documentElement.requestFullscreen();
  else document.exitFullscreen && document.exitFullscreen();
}
$("fsBtn").onclick = toggleFs;
document.addEventListener("fullscreenchange", () => { $("fsBtn").lastChild.textContent = document.fullscreenElement ? "Exit full screen" : "Full screen"; });
document.addEventListener("keydown", e => {
  if (e.key === "c" || e.key === "C") drawer(!rail.classList.contains("open"));
  else if (e.key === "f" || e.key === "F") toggleFs();
  else if (e.key === "Escape") drawer(false);
});
"""
rep("/* ---------- boot ---------- */", JS + "\n/* ---------- boot ---------- */")
# show "n / total" chapter number on the button
rep('  $("chapName").textContent = CH[chIndex].name;', '  $("chapName").textContent = CH[chIndex].name;\n  $("chapNo").textContent = (chIndex + 1) + "/" + CH.length;')
rep('<kbd>T</kbd> switch Watch / Try it', '<kbd>T</kbd> Watch / Try it &nbsp; <kbd>C</kbd> chapters &nbsp; <kbd>F</kbd> full screen')
open(f, "w", encoding="utf-8").write(s)
print("full-screen layout applied")
