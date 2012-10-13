.. _bestpractices:

Best Practices for Developing On Twilio
=======================================

Here's a summary of a number of best practices we've found that work well in the
development of your Twilio applications.

Using TwiML
-----------

This section covers pro tips related to handling inbound Twilio requests and
responding to them with `TwiML`_.

* Use a `helper library`_ to generate your TwiML and avoid simple typo errors.
* Make use of `Fallback URLs`_ for phone numbers and TwiML apps to prevent your
  users from hearing the dreaded "We're sorry - an application error has
  occured."
* If you're looking to maintain any state around calls, be sure to leverage 
  `Status Callback URLs`_ to get asynchronous notifications of completed calls.

.. _TwiML: http://www.twilio.com/docs/api/twiml
.. _helper library: http://www.twilio.com/docs/libraries
.. _Fallback URLs: https://www.twilio.com/docs/availability-reliability#fallback-urls
.. _Status Callback URLs: https://www.twilio.com/docs/api/twiml/twilio_request#asynchronous


Using the REST API
------------------

Here we cover a few helpful tips for using the `REST API`_ for outbound Twilio
requests like placing calls or sending text messages.

* Make use of the exceptions available in your helper library to prevent
  malformed phone numbers or missing permissions from causing fatal errors.
  Try/catching all outbound REST requests against these exceptions give you an
  easy way to handle errors gracefully and log for debugging later.
* If making a large number of requests - like when sending text messages to a
  group of contacts - make use of a task queue like `Celery`_ to send
  asynchronously.
* Use the new `Usage API`_ to reduce API calls for summary statistics on Twilio
  usage.

.. _REST API: https://www.twilio.com/docs/api/rest
.. _Celery: http://celeryproject.org/
.. _Usage API: http://www.twilio.com/docs/api/rest/usage


Using Twilio Client
-------------------

`Twilio Client`_ for JavaScript, iOS and Android are excellent ways to stay in
touch with your users.

* Be sure to include a visual cue for first time users to click "Allow" in the
  popup permissions dialog.
* Set your `token expiration`_ to a value that makes sense for your use case.  By
  default, this is an hour.
* Use the `parameters`_ property to surface important details to your users like
  who is calling and what is dialed.


.. _Twilio Client: http://www.twilio.com/client
.. _token expiration: https://www.twilio.com/docs/client/capability-tokens#token-expiration
.. _parameters: https://www.twilio.com/docs/client/connection#parameters


Security
--------

Security is critical to telephony applications - here's some tips on using
Twilio safely.

* Never bundle your AccountSid and AuthToken in a client-side application, even
  if it is compiled.
* Always generate Twilio Client capability tokens server-side.
* Use `Digest Authentication`_ and SSL in concert for your TwiML URLs to make
  Twilio authenticate with your webserver.
* Use `Request Validation`_ to further confirm that requests are legitimately
  coming from Twilio.

.. _Digest Authentication: https://www.twilio.com/docs/security#http-authentication
.. _Request Validation: https://www.twilio.com/docs/security#validating-requests


Testing
-------

Testing your apps before you go into production is always wise.  Be sure to
avail yourself of our new `Testing Credentials`_.  Here are a few tips to make
sure your tests work well.

* If mocking the Twilio REST Client, be sure mock the *resource* instead of the
  client itself for best effect.
* Simulate Twilio in your test web client by matching the parameters found in a
  `Twilio request`_.
* Test early, test often.  It's good for you!

.. _Testing Credentials: https://www.twilio.com/docs/howto
.. _Twilio request: https://www.twilio.com/docs/api/twiml/twilio_request#synchronous-request-parameters
