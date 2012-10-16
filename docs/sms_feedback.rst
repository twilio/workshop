.. _sms_feedback:

Extending Radio Call In
=======================

Let's add some additional features to our current application. Any of these
additions are also suitable for call centers.

SMS Feedback
------------

We've set up a basic call-in line. Let's say we want to keep the dialogue going
with our callers a little more. We are going to send an SMS to callers after
they get off the line.

Sending an SMS From a Call
~~~~~~~~~~~~~~~~~~~~~~~~~~

We want to send an SMS after the DJ call is complete. Let's modify our customer
call in TwiML slightly to request a new endpoint after the call connects.

.. code-block:: xml
   :emphasize-lines: 3

    <?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Enqueue action="/sms" waitUrl="/wait-loop">radio-callin-queue</Enqueue>
    </Response>

After the DJ disconnects from the call, Twilio will make a POST request to the
``/sms`` endpoint. Let's set up that endpoint to send an SMS to the caller.

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
            
            params = {
                'msgs': client.sms.messages.list(direction='inbound'),
            }
            self.response.out.write(render_template('messages.html', params))

Add this RetrieveSMSEndpoint into the WSGIApplication's routing map as
``/inbound-sms``. The ``messages.html`` template prints out the feedback you've
received.

.. literalinclude:: ../templates/messages.html
   :language: html

Now, you'll be able to see when customers send you feedback on your call-in
line.

Advanced Features
~~~~~~~~~~~~~~~~~~

Try implementing some of these advanced features:

- Add a server-side endpoint to reply to users directly from your dashboard.
- Send yourself an email whenever someone new writes in.
- Add paging to your SMS list - eg a "More" button which will fetch the next 50
  SMS messages from your list.
- Add a way to hide SMS messages you've seen/replied to already.


Call Recording
--------------

To help our DJ improve his manners on the phone, let's record all of the
incoming calls to our Queue.

Many states have laws about letting the party know that they are being
recorded. So let's add a short message before the call, letting the calling
party know that we are recording the call.

We need to alter the TwiML that plays on the DJ's side to `add a url attribute`_.
This URL will hold TwiML telling the caller they are about to be recorded.
We're also going to add ``record="True"`` to the Dial verb, to record the call.

.. code-block:: xml
   :emphasize-lines: 3,4

    <?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Dial record="true" hangupOnStar="true">
            <Queue url="/record-message">radio-callin-queue</Queue>
        </Dial>
        <Redirect></Redirect>
    </Response>

Then at the ``/record-message`` route, place the following TwiML:

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Say>This call is being recorded.</Say>
    </Response>

.. _add a url attribute: http://www.twilio.com/docs/api/twiml/queue#attributes-url

That's it! Now all of your incoming calls will be recorded. To listen to the
recorded calls, go to the `Recordings page of your Twilio Dashboard`_.

.. _Recordings page of your Twilio Dashboard: https://www.twilio.com/user/account/log/recordings

Advanced Features
~~~~~~~~~~~~~~~~~~

Try implementing some of these advanced features:

- Listen to your recordings straight from your Dashboard.
- Export your recordings to a private S3 folder, and delete the Twilio copies
  of the recording.
- Set up monitoring of your application, so that you receive notifications if
  your application becomes unreachable.
- Set up HTTP Authentication so that Twilio must authenticate before reading
  TwiML from your server, and other browsers will receive a 401 Forbidden
  message.



Routing Calls to Voicemail
--------------------------

Phone numbers are available all of the time, but your agents might not be. We
don't want to put people on hold if there's no human available.

Instead, if our call-in hotline is overwhelmed, we'll give people the option to
leave a voicemail if there are currently long hold times for a real agent.

Let's take a look at what that logic would look like.

.. code-block:: python

   import webapp2
   from twilio import twiml
   from twilio.rest import TwilioRestClient

   class EnqueueHandler(webapp2.RequestHandler):

       def get(self):
           self.response.headers['Content-Type'] = 'application/xml'

           client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

           resp = twiml.Response()

           for queue in client.queues.list():
               if queue.friendly_name == 'radio-callin-queue':

                   if queue.average_wait_time < 5: # Wait is less than five minutes
                       continue

                   g = resp.gather(num_digits=1, timeout=10, action="/voicemail")
                   g.say("The wait is {} minutes.".format(queue.average_wait_time))
                   g.say("Press 1 to leave a voicemail, "
                         "or stay on the line for an agent")

           resp.enqueue("radio-callin-queue",
               waitUrl="/twiml/wait", waitMethod="GET")
           self.response.write(str(resp))

   class WaitHandler(webapp2.RequestHandler):
       # Rest of the file is the same as the previous pages...

If the average queue wait time is higher than some threshold, we listen for a
key input, and redirect people to voicemail if they press a key. If the user
does not press a key, they'll just fall through to the <Enqueue> verb at the
bottom of the handler. 

Otherwise, the queue wait times are short, so we place people in the call
queue.

We need to add a new handler for our voicemail endpoint. Set up the following
route to listen at ``/voicemail``.

.. code-block:: python

   import webapp2
   from twilio import twiml


   class EnqueueHandler(webapp2.RequestHandler):
       # Same as above..


   class VoicemailHandler(webapp2.RequestHandler):

       def get(self):
           """ GET /voicemail """
           self.response.headers['Content-Type'] = 'application/xml'

           resp = twiml.Response()
           resp.say("Please leave a message after the tone.")
           resp.record()
           self.response.write(str(resp))


    class WaitHandler(webapp2.RequestHandler):
        # Rest of the file is the same as the previous pages...

Try it out! You should be able to retrieve these recordings from your `Twilio
Dashboard`_.

It's Closing Time
~~~~~~~~~~~~~~~~~

If the queue is closed, we redirect straight to voicemail.

.. code-block:: python
   :emphasize-lines: 4-9,30-35 

   import webapp2
   from twilio import twiml
   from twilio.rest import TwilioRestClient
   from datetime import datetime

   def queue_closed(opening_hour=9, closing_hour=17):
       now = datetime.now()
       # Check if current time is before opening or after closing
       return now.hour < opening_hour or now.hour > closing_hour

   class EnqueueHandler(webapp2.RequestHandler):

       def get(self):
           self.response.headers['Content-Type'] = 'application/xml'

           client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

           resp = twiml.Response()

           for queue in client.queues.list():
               if queue.friendly_name == 'radio-callin-queue':

                   if queue.average_wait_time < 5: # Wait is less than five minutes
                       continue

                   g = resp.gather(num_digits=1, timeout=10, action="/voicemail")
                   g.say("The wait is {} minutes.".format(queue.average_wait_time))
                   g.say("Press 1 to leave a voicemail, "
                         "or stay on the line for an agent")

           if queue_closed():
               resp.say("The queue is currently closed. Please stay "
                        "on the line to leave a voicemail.")
               resp.redirect('/voicemail')
           else:
               resp.enqueue("radio-callin-queue",
                   waitUrl="/twiml/wait", waitMethod="GET")

           self.response.write(str(resp))

   class WaitHandler(webapp2.RequestHandler):
       # Rest of the file is the same as the previous pages...


Our users will now hear a helpful message when the queue is closed, instead of
waiting around for an agent that will never pick up



Advanced Features
~~~~~~~~~~~~~~~~~~

That's the end of the content for this tutorial. If you still have some time,
try implementing some of these advanced features:

- Send an email to yourself when someone leaves a new recording.
- Write a unit test to check the logic in your controller.

.. _Twilio Dashboard: https://www.twilio.com/user/account/log/recordings
