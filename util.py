import os
from twilio.util import TwilioCapability
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template
import xml.etree.ElementTree as ET


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


def current_weather(zipcode):
    """
    Return the current weather for a zip code
    """
    url = "http://xml.weather.yahoo.com/forecastrss?p=" + str(zipcode)
    resp = urlfetch.fetch(url)
    feed = ET.fromstring(resp.content)

    description = feed.find(".//{http://xml.weather.yahoo.com/ns/rss/1.0}condition")

    if description is None:
        return "unknown"

    return "{}, {} degrees".format(description.attrib.get('text', 'Sunny'),
                                   description.attrib.get('temp', '85'))
