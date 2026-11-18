"""Tiny driver for guide-book screenshots on prod (hidden browser, logged-in profile from login.py)."""
import os, sys, time, traceback
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
PROFILE = os.path.join(HERE, os.environ.get("RA_PROFILE", "profile"))
OUT = os.path.join(HERE, os.environ.get("RA_OUT", "out"))
SITE = os.environ.get("RA_SITE", "https://rapidassets.ai")
os.makedirs(OUT, exist_ok=True)

HL_CSS = "outline: 3px solid #ff7a1a !important; outline-offset: 3px !important; border-radius: 10px;"


class D:
    def __enter__(self):
        self.pw = sync_playwright().start()
        self.ctx = self.pw.chromium.launch_persistent_context(
            PROFILE, headless=True, viewport={"width": 1440, "height": 900}, device_scale_factor=1.5)
        self.page = self.ctx.pages[0] if self.ctx.pages else self.ctx.new_page()
        self.page.set_default_timeout(15000)
        return self

    def __exit__(self, *a):
        self.ctx.close()
        self.pw.stop()

    def go(self, path, wait=3500):
        self.page.goto(SITE + path, wait_until="domcontentloaded", timeout=90000)
        try:
            self.page.wait_for_load_state("networkidle", timeout=20000)
        except Exception:
            pass
        self.page.wait_for_timeout(wait)

    def esc(self):
        self.page.keyboard.press("Escape")
        self.page.wait_for_timeout(500)

    def hl(self, loc):
        loc.first.evaluate("(el, css) => { el.dataset.guideHl = '1'; el.style.cssText += css; }", HL_CSS)

    def unhl(self):
        self.page.evaluate("() => document.querySelectorAll('[data-guide-hl]').forEach(e => { e.style.outline=''; e.style.outlineOffset=''; delete e.dataset.guideHl; })")

    def anon(self):
        """Swap the owner's name/email for neutral text in the visible page (screenshots only). Hide the local Design switch."""
        self.page.evaluate(r"""() => {
          document.querySelectorAll('button').forEach(b => { if ((b.innerText||'').trim() === 'Design' && getComputedStyle(b).position === 'fixed') b.style.display = 'none'; });
          document.querySelectorAll('button,div').forEach(b => { if ((b.innerText||'').trim() === 'Design' && b.getBoundingClientRect().left < 200 && b.getBoundingClientRect().top > 700) b.style.display = 'none'; });
          const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
          let n; while ((n = w.nextNode())) {
            if (/Hassan|Kamran|@imaginationai|@gmail/i.test(n.nodeValue))
              n.nodeValue = n.nodeValue.replace(/Hassan Kamran/gi, 'Your Name').replace(/Hassan/gi, 'You')
                .replace(/[\w.+-]+@[\w.-]+/g, 'you@example.com');
          }
        }""")

    def buttons(self, limit=80):
        """Print the visible buttons/links/tabs (to learn labels)."""
        names = self.page.evaluate("""() => [...document.querySelectorAll('button,[role=button],[role=tab],[role=menuitem],a,[role=option],[role=radio]')]
          .filter(e => e.offsetParent !== null).map(e => (e.getAttribute('aria-label') || e.innerText || '').trim().replace(/\\s+/g,' ').slice(0,60))
          .filter(Boolean)""")
        seen = []
        for x in names:
            if x not in seen:
                seen.append(x)
        print("   buttons:", " | ".join(seen[:limit]), flush=True)

    def shot(self, name, hl=None, clip=None):
        self.anon()
        if hl is not None:
            self.hl(hl)
        self.page.wait_for_timeout(400)
        self.page.screenshot(path=os.path.join(OUT, name + ".png"), clip=clip)
        self.unhl()
        print("OK  ", name, flush=True)


def run(steps):
    """steps: list of (name, fn(d)). Each runs on its own; a failure is reported and the next one goes on."""
    with D() as d:
        for name, fn in steps:
            try:
                fn(d)
            except Exception as e:
                print("FAIL", name, type(e).__name__, str(e).splitlines()[0][:200], flush=True)
                try:
                    d.page.screenshot(path=os.path.join(OUT, "_fail_" + name + ".png"))
                    d.esc()
                except Exception:
                    pass
