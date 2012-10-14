.. _hello_world:

Hello World
===========

The first thing we'll do today is get to know the `Twilio API`.

Twilio Account Portal
---------------------

When you log into your Twilio Account, the first page you will come across is
your Account Dashboard. This is where your Account Sid and Auth Token are
displayed.

.. image:: _static/bar.png
	:class: screenshot

These are your account credentials. The Account SID acts as a username and the 
Auth Token acts as a password. Twilio uses your Account Sid and Auth Token to 
authenticate the API requests made by your application. 

Analytics about your Voice and SMS application are also shown here, we'll go
over these after we've made some calls and sent some SMS messages.

At the bottom of your Account Dashboard is the API Explorer and the Debugger. 

Twilio API Explorer
-------------------

The `API Explorer`_ is a helpful application built in to the Account Portal that allows you to easily try out the API without getting in to the details of scripting and :ref:`HTTP <http>` calls.

Let's use the `API Explorer` to get to know the `Twilio API`.

Getting Account Information
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's start of with a basic request for your account information. Go to your Twilio Account Portal, click on `Dev Tools`, then click on `Accounts` (on the right near the bottom), then click on `View Account`.

Go ahead and click on the `Make Request` button. A response with your Account information should appear at the end of the page. 

**Ok, so what did we just do?**

Let's take a look at the key parts of the request we just made:

.. code-block:: bash

	GET /2010-04-01/Accounts/AC000.xml

This command is specially formatted to function on the command line. Lets break that down a bit:

- **GET**: this line tells curl to make a ``GET`` request, meaning that the intent of this call is to retrieve information from the server.
- **/2010-04-01/Accounts/AC000.xml**: this is the endpoint for retrieving Account data from the Twilio API. Lets break it down further:
	- **/2010-04-01/** is the version of the API that we want to request. The version of the API we want to talk to is important because we want to make sure that the way we talk to the API doesn't change. If Twilio makes a major change to how to talk to the API the version will change, but the old version will continue to work the same way so that your application doesn't break.
	- **Accounts/AC000.xml** means that we want to retrieve an Account resource for the account "AC000" and that we want the response in XML format.
	
Now lets look at the response. The server responded with an XML formatted representation of your account information.

Sending an SMS
^^^^^^^^^^^^^^

Let's send a text message using the `API Explorer`_. Go to your Twilio Account Portal, click on `Dev Tools`, then click on `SMS Messages`, then on `Send SMS`.

Here we can try out the Twilio API for sending SMS Messages. All the fields required to send an SMS are visible.

============ ==========
Parameter    Definition
============ ==========
`Format`     The `Format` field tells the API in what format we want the API to respond with. For our purposes right now this doesn't matter, but you can request the response in either `XML`_ or `JSON`_ format.
`AccountSid` The `AccountSid` field tells the API which Account we want to use to send the SMS. This is pre-populated with your account.
`From`       The `From` field tells the API which phone number to use to send the Message. This can only be one of the phone numbers you've purchased or ported in to Twilio.
`To`         The `To` field tells the API where to send the message. The phone number should be in `E.164`_ format. Phone numbers that do not include a "+" with country code will be assumed to be from the same country as the `From` phone number.
`Body`       The body is a freeform field to enter your message. You can enter a message up to 160 characters long.
============ ==========

Enter your cell phone number in the `To` field and a `Body` and click the `Make Request` button at the bottom of the page. This will send an SMS. You may be prompted to confirm the use of funds from your account. Aren't you glad you got the Promo credit?

Your phone should receive a text message shortly.

**So how was that different from our Accounts information request?**

Lets take a look at the key parts of this request:

.. code-block:: bash

	POST /2010-04-01/Accounts/AC000/SMS/Messages.xml
	
There are a few key differences to note:

- **POST** tells curl to make a ``POST`` request, meaning that the purpose of this request is to pass data in to the API for the purposes of modifying the ``SMS Messages`` resource.
- **Parameters**: if you **-d 'From=xxx'*** et al... tell curl what data to pass to the API. You can see each entry you modified in the form is represented here. You'll also notice that each entry contains special characters (ie: ``%2B`` instead of ``+``). This is called `Url Encoding`_ and is required to make sure that special characters are properly transmitted to the API.

Making a Phone Call
^^^^^^^^^^^^^^^^^^^

Now let's make a phone call using the `API Explorer`_. Go to your Twilio Account Portal, click on `Dev Tools`, then click on `Phone Calls`, then on `Make call`.

============ ==========
Parameter    Definition
============ ==========
`Format`     The `Format` field tells the API in what format we want the API to respond with. For our purposes right now this doesn't matter, but you can request the response in either `XML`_ or `JSON`_ format.
`AccountSid` The `AccountSid` field tells the API which Account we want to use to make the call. This is pre-populated with your account.
`From`       The `From` field tells the API which phone number to use to make the call. This can be a number that you've purchased from Twilio or any phone number that you've validated on your account.
`To`         The `To` field tells the API where to send the call. The phone number should be in `E.164`_ format or be a valid Twilio Client ID. Phone numbers that do not include a "+" with country code will be assumed to be from the same country as the `From` phone number.
`Url`        The `Url` field tells the API where to load TwiML instructions for handling the call. `TwiML`_ is a set of instructions that tells Twilio what to do. Don't worry, we'll get more in to TwiML later. 
============ ==========

Enter your cell phone number in the `To` field. To make things easy up we're gonna use a `Twimlet`_ for the `Url`. We'll get in to the details of building TwiML later on. Copy the url below in to the `Url` field.

.. code-block:: bash

	http://twimlets.com/message?Message=Hello+World

Click on the `Make Request` button at the bottom of the page. Your phone should start ringing momentarily.

Additional Information
----------------------
- `TwiML: the TWilio Markup Language <http://www.twilio.com/docs/api/twiml>`_
- `Twilio REST API - Calls Resource <http://www.twilio.com/docs/api/rest/call>`_
- `Twilio REST API - SMS/Messages Resource <http://www.twilio.com/docs/api/rest/sms>`_

.. _API Explorer: https://www.twilio.com/user/account/developer-tools/api-explorer
.. _XML: http://en.wikipedia.org/wiki/XML
.. _JSON: http://en.wikipedia.org/wiki/JSON
.. _E.164: http://en.wikipedia.org/wiki/E.164
.. _TwiML: http://www.twilio.com/docs/api/twiml
.. _Twimlet: https://www.twilio.com/labs/twimlets
.. _Url Encoding: http://en.wikipedia.org/wiki/Percent-encoding