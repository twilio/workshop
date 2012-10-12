import os
from google.appengine.ext.webapp import template

def render_template(rel_path, parameters=None, folder="templates"):
    """
    Takes a path relative to the templates/ folder and
    an optional parameter for variables to render to the template.
    """
    parameters = parameters if parameters is not None else {}
    path = os.path.join(os.path.dirname(__file__), folder, rel_path)
    return template.render(path, parameters)
