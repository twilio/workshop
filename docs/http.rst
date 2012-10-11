.. _http:

Introduction to HTTP
====================

When a web browser requests a web page it needs to talk to a web server.
Browsers talk to servers using a language known as HTTP, or Hypertext Transfer
Protocol. The language is simple and easy to understand and this
request/response model of communication is referred to as REST, or
`REpresentational State Transfer`. 

A simple HTTP request might look like:

.. code-block:: text

	GET / HTTP/1.1
	Host: www.example.com
	
And the server response would be:

.. code-block:: text

	HTTP/1.1 200 OK
	Content Type: text/html
	 
	Response body appears here…

The response is comprised of a header block and a content block. The ``Content
Type`` header tells the browser how to interpret the response. If it had been
``image/png`` the browser would have known to expect PNG data, or in the case
of ``application/json`` it would have expected a JSON formatted data response.

HTTP Headers
^^^^^^^^^^^^

Clients and servers need to pass information about the requests and response
and do so by setting what are called headers. These headers can describe many
things, among them the request type, the response type, and the server state.

While not required, it is up to the client to tell the server what kind of
information it can accept.

A browser request for a web page should include an ``Accept`` header that tells
the server what kind of information it can understand. Browsers can understand
a wide range of information so their requests often look like:

.. code-block:: text

	GET / HTTP/1.1
	Host: www.example.com
	Accept: text/html,application/xhtml+xml,application/xml
	Accept-Language: en-US,en
	
This request tells the server how it can respond to the request in a way that
the client will understand as well as how it can compress the response to
reduce the size of the response content.

It is server's responsibility to tell the client how to interpret the response.
As we saw above the ``Content Type`` header tells the browser what to expect in
the content block of the response.

In the case of a server that requires authentication the response would also
include an extra header that identifies the type of authentication required,
for example:

.. code-block:: text

	HTTP/1.1 401 Unauthorized
	Content Type: text/html
	WWW-Authenticate: Basic Realm="Protected Resource"
	
In this case an authorization response must be returned to access the resource.
The response has to signify what kind of authentication scheme it is using and
provide the proper credentials. HTTP authorization response a Base64 encoded
string of the user's credentials in ``username:password`` format. So a response
to an authentication response would include:

.. code-block:: text

	Authorization: Basic dHdpbGlvOnR3aWxpbyByb2Nrcw==

HTTP Headers in Action
^^^^^^^^^^^^^^^^^^^^^^

Lets try this out on `Hurl.it <http://hurl.it/?url=http://www.twilio.com>`_ to
see how we can change the way a server responds.

By just loading the server's response we see a content body of HTML that we can
read. Now click on `add header`, enter ``Accept-Encoding`` and ``gzip,deflate``
and submit the request.

The response now includes a header ``Content-Encoding: gzip`` and the content
body is compressed with gzip compression and is unreadable by mortal man.

HTTP Verbs/Methods
^^^^^^^^^^^^^^^^^^

HTTP defines methods, also known as Verbs, that allow the request specify the
action to perform on the resource. While there are many methods defined by
HTTP, we only really need 4 of them to maintain a RESTful application
structure.

**GET**
	The request is for a representation of the requested resource that is
        identified by the request URI.

**POST**
	The request is to submit data to be processed for the specified 
        resource. This may create a new resource or update an existing resource.

**PUT**
	The request is to upload a representation of the specified resource 
        that should be stored at the request URI.

**DELETE**
	The request is to delete the specified resource.

HTTP Cookies
^^^^^^^^^^^^

An HTTP Cookie is a small piece of information that is sent in a server's
response and stored by the client. When returning to the site the client will
send that cookie data back to the server each time it requests a resource.

Cookies have many uses but are generally used to help the server identify
returning users so that the server can maintain the state of your session. For
example, after logging in to a website you are given a cookie that allows the
server to identify you and verify that you are logged in during your browser
session.

WebHooks
^^^^^^^^

Webhooks are a pattern of enabling user-defined callbacks in web applications.
A webhook is simply an HTTP callback to a specific URI that is triggered by an
event.

In Twilio the Request URLs you define for Voice and SMS are webhooks. When
Twilio receives a call to your number it will make a request to the URL you
defined to notify your application of the event and to get TwiML to use in
response to the event.

Twilio Account Portal
---------------------

When you log into your Twilio Account, the first page you will come across is
your Account Dashboard. This is where your Account Sid and Auth Token are
displayed.

Twilio uses your Account Sid and Auth Toekn to authenticate the API requests
your Twilio application sends, these are your account credentials. The Account
SID acts as a username and the Auth Token acts as a password.

Analytics about your Voice and SMS application are also shown here, we'll go
over these after we've made some calls and sent some SMS messages.

At the bottom of your Account Dashboard is the API Explorer and the Debugger. 


Hello World - SMS
-----------------

Let's send a text message using Python and the Twilio REST API. Open the
``send_sms.py`` file in your text editor. First, replace the dummy account
credentials with those of your own. Locate your Account Sid and Auth Token,
which can be found `at the top of your Twilio account dashboard
<https://www.twilio.com/user/account>`_.

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
