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

You can retrieve users responses from the Twilio API. Add a server side
endpoint to fetch your 50 most recent inbound text messages.

.. code-block:: python

    import json
    from twilio import TwilioRestClient

    class RetrieveSMSEndpoint(webapp2.RequestHandler):

        def get(self):
            client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
            # Note direction=inbound filter, or you will show all of your
            # outbound messages in this list as well.
            msgs = client.sms.messages.list(direction='inbound')
            msgs_json = {"messages": [msg.__dict__ for msg in msgs]}
            self.response.out.write(json.dumps(msgs_json))

Add this RetrieveSMSEndpoint into the WSGIApplication's routing map as
``/inbound-sms``. Now we need some HTML for the status, and Javascript to poll
the state of the queue and update the UI.

Add this HTML:

.. code-block:: html

    <div style="width: 500px; font-family: sans-serif; text-align: left; margin: 0 auto;">
        <h2>SMS Feedback</h2>
        <ul id="messages">
            
        </ul>
    </div>

And this Javascript function to hit our new server-side endpoint, and retrieve
our SMS messages.

.. code-block:: javascript

    var constructMessageHTML = function(from, message) {
      return '<li style="padding-bottom: 10px;"><b>' + from + '</b><br />' + message + '<br />';
    }

    var getSMSMessages = function() {
        $.getJSON('messages.json', function(result) {
            var msgs = result.messages;
            for (var i = 0; i < msgs.length; i++) {
                var msg = msgs[i];
                $("#messages").append(constructMessageHTML(msg.from, msg.body));
            }
        });
    };

    // run the queue fetcher once on page load
    $(function() {
      getSMSMessages();
    });

Now, you'll be able to see when customers send you feedback on your call-in
line.

Advanced Features
------------------

That is the end of the content for this tutorial. If you still have some time,
try implementing some of these advanced features:

- Add a server-side endpoint to reply to users directly from your dashboard.
- Send yourself an email whenever someone new writes in.
- Add paging to your SMS list - eg a "More" button which will fetch the next 50
  SMS messages from your list.
- Add a way to hide SMS messages you've seen/replied to already.

