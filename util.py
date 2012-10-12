import os
from twilio.util import TwilioCapability
from google.appengine.ext.webapp import template


def render_template(rel_path, parameters=None, folder="templates"):
    """
    Takes a path relative to the templates/ folder and
    an optional parameter for variables to render to the template.
    """
    parameters = parameters if parameters is not None else {}
    path = os.path.join(os.path.dirname(__file__), folder, rel_path)
    return template.render(path, parameters)


def generate_token(account_sid, auth_token, application_sid):
    """
    Create a capability token given Twilio account credentials
    and an application sid.
    """
    capability = TwilioCapability(account_sid, auth_token)
    # Allow access to the Call-in ApplicationSid we created
    capability.allow_client_outgoing(application_sid)
    return capability.generate()
