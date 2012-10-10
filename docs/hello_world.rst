.. _hello_world:

Hello World
===========

HTTP and Webhooks
-----------------

Twilio Account Dashboard
---------------------

When you log into your Twilio Account, the first page you will come across is your Account Dashboard. This is where your Account Sid and Auth Token are displayed.

Twilio uses your Account Sid and Auth Toekn to authenticate the API requests your Twilio application sends, these are your account credentials. The Account SID acts as a username and the Auth Token acts as a password.

Analytics about your Voice and SMS application are also shown here, we'll go over these after we've made some calls and sent some SMS messages.

At the bottom of your Account Dashboard is the API Explorer and the Debugger. 


Hello World - SMS
-----------------

Let's send a text message using Python and the Twilio REST API. Open the
``send_sms.py`` file in your text editor. First, replace the dummy account
credentials with those of your own. Locate your Account Sid and Auth Token, which can be found `at
the top of your Twilio account dashboard <https://www.twilio.com/user/account>`_.

.. literalinclude:: ../send_sms.py
   :lines: 1-4

On the next line, set `TO_NUMBER` to the number you used to sign up
with Twilio. During your free trial, you're only allowed to make calls and send
messages to phone numbers you have verified.

set `FROM_NUMBER` to your new Twilio number. if you
can't remember it, check the `Numbers
<https://www.twilio.com/user/account/phone-numbers/incoming>`_ section of your
account dashboard.

Pick any message less than 140 characters to serve as the body.

.. literalinclude:: ../send_sms.py
   :lines: 6-8

With the above information, we constructed a Twilio REST API client. We'll use
this to create and send a new text message.

.. literalinclude:: ../send_sms.py
   :lines: 10-

We're now ready to send a SMS message.

.. code-block:: bash

    $ python send_sms.py

Your phone should be getting a message in a few seconds.

Hello World - Voice
-------------------

It's time to make a call to your phone using the REST API. 
Open ``make_call.py`` in your text editor and, just like the last section,
fill in your account credentials and phone numbers details.

With the above information, we construct a Twilio REST API client and create a
new call.

.. literalinclude:: ../make_call.py
   :lines: 8-

Run the script to start the call.

.. code-block:: bash

    $ python make_call.py

Your phone should start ringing momentarily.


Additional Information
----------------------
- `Twilio REST API - Calls Resource <https://www.twilio.com/docs/api/rest/call>`_
- `Twilio REST API - SMS/Messages Resource <https://www.twilio.com/docs/api/rest/sms>`_

.. _Dial: https://www.twilio.com/docs/api/twiml/dial
.. _Say: https://www.twilio.com/docs/api/twiml/say
.. _Play: https://www.twilio.com/docs/api/twiml/play
.. _Record: https://www.twilio.com/docs/api/twiml/record
.. _Gather: https://www.twilio.com/docs/api/twiml/gather
