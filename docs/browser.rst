.. _browser:

Into the Browser
================

Using Twilio Client
-------------------

Using Twilio Client, we can be hooked into the full power of the Twilio API
from your Web Browser. This includes the ability to make and receive phone
calls, opening up the world of telephony to your dynamic web applications.

Let's try writing a web app that is capable of answering phone calls in a
Twilio <Queue>. This way, our Radio DJ customer won't be required to use their
personal phone when answering queues.

Creating an Application
-----------------------

The first thing 
Go to the `Create App page <https://www.twilio.com/user/account/apps/add>`_
(For reference, if you didn't have a link, you can find it from your Account
Portal, click on "Dev Tools" > "TwiML Apps" and click the button for "Add.")

We'll name our new application "Client DJ Call-In" and set the Voice Request
URL to a new endpoint for the TwiML we want to be executed when the DJ's
browser connects (this should be the same URL as the DJ's dial-in number).

Generating a Token
------------------

Since Twilio Client applications are being run on the browser, we need a
technique to grant the end user temporary privileges on our Twilio Account.
This is the job of `Capability Tokens
<https://www.twilio.com/docs/client/capability-tokens>`_.  Capability Tokens
allow us to lock down access to what we want the end user's session to be able
to do. For our needs we only need to add access to making an outgoing
connection to our new Application.

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
new AppEngine RequestHandler into ``main.py``.

.. code-block:: python

    class IndexPage(webapp2.RequestHandler):

        def get(self):
            params = {
                "token": gen_token(ACCOUNT_SID, AUTH_TOKEN, APP_SID)
            }
            self.response.out.write(render_template("index.html", params))


We're rending the ``token`` variable to this ``index.py`` file, and there are
two important lines in the Javascript that make this work:

.. code-block:: javascript

    Twilio.Device.setup("{{ token }}");

The above line of code calls ``Twilio.Device.setup`` and uses our templating
engine to pass in a valid Capability Token. When ``setup`` finishes, the
callback passed into ``Twilio.Device.ready`` will be called to let us know that
we've initialized our access to the microphone, speakers, and we've started
listening for incoming calls (if applicable).

.. code-block:: javascript

    function call() {
      Twilio.Device.connect();
    }

This code defines a new function called ``call`` that just wraps
``Twilio.Device.connect`` which initiates an outgoing call to our Application
we created earlier. In this case, calling ``call()`` will execute the TwiML

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Dial>
            <Queue>radio-callin-queue</Queue>
        </Dial>
    </Response>

assuming that we correctly configured the Application to the URL that returns
this TwiML

Getting the Next Caller From the <Queue>
-----------------------------------------
With <Queue>s, we can hangup on the current caller and move to the next one by
pressing the "#" key on the phone. Luckily, Twilio Client has a feature for
sending DTMF tones programmatically.

First, we need to hold on to the response of ``Twilio.Device.connect()`` so
let's add a global variable called ``connection`` and have every ``call()``
command set it. Replace the existing ``call`` function with something like this:

.. code-block:: javascript

    var connection = null;
    function call() {
        connection = Twilio.Device.connect();
    }

Now, we can add a new function, called ``next()``:

.. code-block:: javascript

    function next() {
        if(connection) {
            connection.sendDTMF("#");
        }
    }

Now we just need to add another button that let's us bring in the next caller.

.. code-block:: html

    <button class="next" onclick="next();">
        Next Caller
    </button>

Adding UI To Display the Queue
------------------------------

Let's add a feature where we can see a visualization of the queue

.. code-block:: python

    import json
    from twilio import TwilioRestClient

    class QueueStatusPage(webapp2.RequestHandler):

        def get(self):
            client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
            q_data = {"queues": client.queues.get(QUEUE_SID)}
            self.response.out.write(json.dumps(q_data))


Add this QueueStatusPage into the WSIApplication's routing map as ``/queue-status``.
Now we need some Javascript to poll the state of the queue and update the UI.

.. code-block:: javascript

    $.get("/queue-status", function(result) {
        // update your UI here
    });
