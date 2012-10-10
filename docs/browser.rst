.. _browser:

Into the Browser
================

Using Twilio Client
-------------------
Using Twilio Client, we can be hooked into the full power of the Twilio
API from your Web Browser. This includes the ability to make and receive phone
calls, opening up the world of telephony to your dynamic web applications.

Let's try writing a web app that is capable of answering phone calls in a
Twilio <Queue>. This way, our Radio DJ customer won't be required to use their
personal phone when answering queues.

Creating an Application
-----------------------
The first thing we'll need to do is create an `Application <http://www.twilio.com/docs/api/rest/applications>`_ for the browser to call into.
Go to the `Create App page <https://www.twilio.com/user/account/apps/add>`_
(For reference, if you didn't have a link, you can find it from your Account Portal,
click on "Dev Tools" > "TwiML Apps" and click the button for "Add.")

We'll name our new application "Client DJ Call-In" and set the Voice Request
URL to a new endpoint for the TwiML we want to be executed when the DJ's
browser connects (this should be the same URL as the DJ's dial-in number).

Generating a Token
------------------
Since Twilio Client applications are being run on the browser, we need a
technique to grant the end user temporary privileges on our Twilio Account.
This is the job of `Capability Tokens <https://www.twilio.com/docs/client/capability-tokens>`_.
Capability Tokens allow us to lock down access what we want the end
user's session to be able to do. For our needs, we only need to add access to
making an outgoing connection to our new Application.

Here is the function we'll use for generating the Capability Token.

.. code-block:: python

    from twilio.util import TwilioCapability

    def gen_token(account_sid, auth_token, application_sid):
        capability = TwilioCapability(account_sid, auth_token)
        # Allow access to the Call-in ApplicationSid we created
        capability.allow_client_outgoing(application_sid)
        return capability.generate()


Answering Queues in the Browser
-------------------------------
The first thing we'll need to build is a web interface. Let's start by adding a
new AppEngine RequestHandler into `main.py`.

.. code-block:: python

    import os
    from google.appengine.ext.webapp import template

    class HelloWorld(webapp2.RequestHandler):

        def get(self):
            self.response.write('Hello World!')


Dequeuing Calls From One Queue To Another
-----------------------------------------




