"""Seasonal Re-theme: open template, pick a theme in the Re-theme step, then run like the others."""
import json, os, re, sys
sys.argv = [sys.argv[0], "Seasonal Re-theme"]
import wfx_run as W
from drv import run


def vis(loc):
    return [loc.nth(i) for i in range(loc.count()) if loc.nth(i).is_visible()]


orig_one = W.one


def one(d, name):
    p = d.page
    real_click = None
    # monkey-patch: after editor shot, before Run, set the theme
    def before_run():
        st = vis(p.get_by_role("button", name="Settings for Re-theme"))
        if st:
            st[0].click(); p.wait_for_timeout(1800)
            d.shot("y_seasonal_re_theme_settings"); d.buttons(80)
            chip = vis(p.get_by_role("button", name="Winter Holidays")) or vis(p.get_by_text("Winter Holidays", exact=True))
            if chip: chip[0].click(); p.wait_for_timeout(1000)
            ta = vis(p.get_by_placeholder("For example: pumpkins", exact=False))
            if ta: ta[0].fill("snow on the armour and cape, frosty blue light, keep the gold trim"); p.wait_for_timeout(500)
            d.shot("y_seasonal_re_theme_theme")
            sv = vis(p.get_by_role("button", name="Save", exact=True))
            if sv: sv[0].click(); p.wait_for_timeout(2500)
    W.BEFORE_RUN = before_run
    orig_one(d, name)


run([("seasonal_re_theme", lambda d: one(d, "Seasonal Re-theme"))])
