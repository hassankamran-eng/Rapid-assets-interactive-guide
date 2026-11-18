"""Chapters back as a permanent, compact left rail (small fonts). Stage fills the rest."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
f = os.path.join(HERE, "tour.template.html")
s = open(f, encoding="utf-8").read()
CSS = """
/* ---- compact permanent left rail ---- */
:root{--railw:212px}
.app{display:grid;grid-template-columns:var(--railw) 1fr;height:100vh;overflow:hidden}
.rail{position:static;transform:none!important;width:auto;box-shadow:none;z-index:auto;transition:none}
.scrim{display:none!important}
.chap-btn{display:none!important}
.brand{padding:12px 12px 8px;gap:8px}
.logo{width:22px;height:22px;border-radius:6px;font-size:12px}
.brand b{font-size:12.5px}
.brand span{font-size:10px}
.chapters{padding:2px 6px 10px}
.grp{font-size:9px;padding:9px 8px 2px;letter-spacing:.12em}
.chap{gap:8px;padding:5px 8px;border-radius:8px;margin:1px 0;align-items:center}
.chap .n{width:17px;height:17px;font-size:9.5px}
.chap .t{font-size:11.5px;line-height:1.2}
.chap .s{display:none}
.chap .bar{width:120px;margin-top:3px;height:2px}
.rail-foot{padding:8px 10px;font-size:9.5px;line-height:1.6}
.rail-foot kbd{font-size:9px;padding:0 4px}
.window{width:min(calc(100vw - var(--railw)), calc((100vh - var(--dockh)) * 1.6))}
.dock{grid-template-columns:1fr auto}
.cap h2{font-size:15.5px}
.cap p{font-size:12.5px}
.cap .meta{font-size:9.5px}
.lbtn{height:34px;padding:0 11px;font-size:12px}
.ib{width:34px;height:34px;border-radius:9px}
.ib.play{width:40px}
.ib svg{width:15px;height:15px}
.seg{font-size:11.5px}
.seg button{padding:5px 9px}
:root{--dockh:66px}
@media (max-width: 980px){
  .app{grid-template-columns:1fr;grid-template-rows:auto 1fr}
  .chapters{display:flex;overflow-x:auto}
  .chap{min-width:140px}
  .grp{display:none}
}
"""
if "compact permanent left rail" not in s:
    s = s.replace("</style>", CSS + "</style>", 1)
open(f, "w", encoding="utf-8").write(s)
print("left rail applied")
