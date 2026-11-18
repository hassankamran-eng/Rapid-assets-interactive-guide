"""Batch 2: Home fixes, create the Guide Book Demo project, first Studio screens (no credits)."""
from drv import run


def home(d):
    d.go("/home")
    box = d.page.locator("textarea").first
    d.shot("p1_home", hl=box)


def home_pick(d):
    d.go("/home")
    d.page.get_by_text("Pick a tool", exact=True).first.click()
    d.page.wait_for_timeout(1000)
    d.shot("p1_home_pick_tool")


def projects(d):
    d.go("/projects")
    d.shot("p1_projects", hl=d.page.get_by_text("Create New").first)


def new_project(d):
    d.go("/studio?newProject=1", wait=5000)
    d.shot("p1_new_project")
    d.buttons()
    inp = d.page.locator("input").first
    inp.fill("Guide Book Demo")
    d.page.wait_for_timeout(500)
    d.buttons()


run([("home", home), ("home_pick", home_pick), ("projects", projects), ("new_project", new_project)])
