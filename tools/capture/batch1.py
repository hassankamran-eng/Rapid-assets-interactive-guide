"""Batch 1: free navigation screens."""
from drv import run


def home(d):
    d.go("/home")
    d.shot("p1_home", hl=d.page.get_by_role("button", name="Ask the agent"))


def home_pick(d):
    d.go("/home")
    d.page.get_by_role("button", name="Pick a tool").first.click()
    d.page.wait_for_timeout(800)
    d.shot("p1_home_pick_tool")


def sidebar_tools(d):
    d.go("/home")
    d.page.get_by_text("Tools", exact=True).first.click()
    d.page.wait_for_timeout(800)
    d.shot("p1_sidebar_tools")
    d.esc()


def project_switcher(d):
    d.go("/home")
    d.page.get_by_text("No project selected").first.click()
    d.page.wait_for_timeout(1000)
    d.shot("p1_project_switcher")
    d.esc()


def projects(d):
    d.go("/projects")
    d.shot("p1_projects")


def gallery(d):
    d.go("/gallery", wait=5000)
    d.shot("p1_gallery")


def learn(d):
    d.go("/learn")
    d.shot("p1_learn")


def integrations(d):
    d.go("/integrations")
    d.shot("p1_integrations")


def workflows(d):
    d.go("/workflows")
    d.shot("p1_workflows")


def credits(d):
    d.go("/home")
    d.page.get_by_text("166").first.click()
    d.page.wait_for_timeout(1500)
    d.shot("p6_credits_modal")
    d.esc()


def tools_image(d):
    d.go("/manual/image-generation", wait=5000)
    d.shot("p2_tools_image")


def tools_edit(d):
    d.go("/manual/image-editing", wait=5000)
    d.shot("p2_tools_edit")


def tools_3d(d):
    d.go("/manual/3d-generator", wait=5000)
    d.shot("p3_tools_3d")


run([("home", home), ("home_pick", home_pick), ("sidebar_tools", sidebar_tools), ("project_switcher", project_switcher),
     ("projects", projects), ("gallery", gallery), ("learn", learn), ("integrations", integrations),
     ("workflows", workflows), ("credits", credits), ("tools_image", tools_image), ("tools_edit", tools_edit),
     ("tools_3d", tools_3d)])
