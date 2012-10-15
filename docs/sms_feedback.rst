.. _sms_feedback:

SMS Feedback
============

We've set up a basic call in line. Let's say we want to keep the dialogue going
with our callers a little more. We are going to send an SMS to callers after
they get off the line.

Sending an SMS From a Call
--------------------------

We want to send an SMS after the DJ call is complete. Let's modify our customer
call in TwiML slightly to request a new endpoint after the call connects.

.. code-block:: xml
   :emphasize-lines: 3

    <?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Enqueue action="/sms" waitUrl="/wait-loop">radio-callin-queue</Enqueue>
    </Response>

After the DJ disconnects from the call, Twilio will make a POST request to the
"/sms" endpoint. Let's set up that endpoint to send an SMS to the caller.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Sms>Thanks for calling the DJ hotline! Do you have any feedback for us?</Sms>
    </Response>

This will send a text asking for feedback after the call completes.

You can retrieve users responses from the Twilio API. Here's some Javascript to
do so:

.. code-block:: javascript

    var account_sid = 'AC123';
    var auth_token  = '456bef';
    var getSMSMessages = function() {
        $.getJSON('https://api.twilio.com');
    };
