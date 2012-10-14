.. _hello_world:

Hello World
===========

The first thing we'll do today is explore Twilio's REST API calls. Soon, you'll
see how SMS and phone calls can be originated from your web browser with Twilio.

Twilio Account Portal
---------------------

When you log into your Twilio Account, the first page you will come across is
your Account Dashboard. This is where your Account SID and Auth Token are
displayed.

.. image:: _static/bar.png
	:class: screenshot

These are your account credentials. The Account SID acts as a username and the 
Auth Token acts as a password. Twilio uses your Account SID and Auth Token to 
authenticate the API requests made by your application. 

Analytics about your Voice and SMS application are also shown here. We'll go
over these after we've made some calls and sent some SMS messages.

At the bottom of your Account Dashboard is the API Explorer and the Debugger. 

Twilio API Explorer
-------------------

The `API Explorer`_ is a helpful application built into the Account Portal that allows you to easily try out the API without getting into the details of scripting and :ref:`HTTP <http>` calls.

Let's use the `API Explorer`_ to get to know the Twilio API.

Hello World: Sending an SMS
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's send a text message using the `API Explorer`_. Go to your Twilio `Account Portal`_, click on `Dev Tools`, then click on `SMS Messages`, then on `Send SMS`.

Here we can try out the Twilio API for sending SMS Messages. All the fields required to send an SMS are visible.

============ ==========
Parameter    Definition
============ ==========
`Format`     The `Format` field tells the API in what format we want the API to respond with. For our purposes right now this doesn't matter, but you can request the response in either `XML`_ or `JSON`_ format.
`AccountSid` The `AccountSid` field tells the API which Account we want to use to send the SMS. This is pre-populated with your account.
`From`       The `From` field tells the API which phone number to use to send the Message. This can only be one of the phone numbers you've purchased or ported into Twilio.
`To`         The `To` field tells the API where to send the message. The phone number should be in `E.164`_ format. Phone numbers that do not include a "+" with country code will be assumed to be from the same country as the `From` phone number.
`Body`       The body is a freeform field to enter your message. You can enter a message up to 160 characters long.
============ ==========

Enter your cell phone number in the `To` field along with a text message `Body`, and click the `Make Request` button at the bottom of the page. This will send an SMS. You may be prompted to confirm the use of funds from your account. Aren't you glad you got the Promo credit?

Your phone should receive a text message shortly.

Hello World: Making a Phone Call
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now let's make a phone call using the `API Explorer`_. Go to your Twilio `Account Portal`_, click on `Dev Tools`, then click on `Phone Calls`, then on `Make call`.

============ ==========
Parameter    Definition
============ ==========
`Format`     The `Format` field tells the API in what format we want the API to respond with. For our purposes right now this doesn't matter, but you can request the response in either `XML`_ or `JSON`_ format.
`AccountSid` The `AccountSid` field tells the API which Account we want to use to make the call. This is prepopulated with your account.
`From`       The `From` field tells the API which phone number to use to make the call. This can be a number that you've purchased from Twilio or any phone number that you've validated on your account.
`To`         The `To` field tells the API where to send the call. The phone number should be in `E.164`_ format or be a valid Twilio Client ID. Phone numbers that do not include a "+" with country code will be assumed to be from the same country as the `From` phone number.
`Url`        The `Url` field tells the API where to load TwiML instructions for handling the call. `TwiML`_ is a set of instructions that tells Twilio what to do. Don't worry, we'll get more into TwiML later. 
============ ==========

Enter your cell phone number in the `To` field. To make things easy, we're going to use a `Twimlet`_ for the `Url`. We'll get into the details of building TwiML later on. Copy the url below into the `Url` field.

.. code-block:: bash

	http://twimlets.com/message?Message=Hello+World

Click on the `Make Request` button at the bottom of the page. Your phone should start ringing momentarily.

Additional Information
----------------------
- `TwiML: the Twilio Markup Language <http://www.twilio.com/docs/api/twiml>`_
- `Twilio REST API - Calls Resource <http://www.twilio.com/docs/api/rest/call>`_
- `Twilio REST API - SMS/Messages Resource <http://www.twilio.com/docs/api/rest/sms>`_

.. _API Explorer: https://www.twilio.com/user/account/developer-tools/api-explorer
.. _Account Portal: https://www.twilio.com/user/account 
.. _XML: http://en.wikipedia.org/wiki/XML
.. _JSON: http://en.wikipedia.org/wiki/JSON
.. _E.164: http://en.wikipedia.org/wiki/E.164
.. _TwiML: http://www.twilio.com/docs/api/twiml
.. _Twimlet: https://www.twilio.com/labs/twimlets
