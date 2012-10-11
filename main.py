import webapp2
from google.appengine.ext.webapp import template
import os


# Utility functions

def render_template(rel_path, parameters=None, folder="templates"):
    """
    Takes a path relative to the templates/ folder and
    an optional parameter for variables to render to the template.
    """
    parameters = parameters if parameters is not None else {}
    path = os.path.join(os.path.dirname(__file__), folder, rel_path)
    return template.render(path, parameters)


# Request Handlers

class HelloWorld(webapp2.RequestHandler):

    def get(self):
        self.response.write('Hello World!')


# URL Mappings

app = webapp2.WSGIApplication([
    ('/', HelloWorld),
], debug=True)
