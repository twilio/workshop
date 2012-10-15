.. _gather_voicemail:

Routing Calls to Voicemail
==========================

Phone numbers are available all of the time, but your agents might not be. We
don't want to put people on hold if there's no human available.

Instead, if our call-in hotline is closed, let's ask people to leave
a voicemail. We'll use a simple time-of-day heuristic to determine whether to
place users in a queue, or to direct them to voicemail. 

We may also want to give people the option to leave a voicemail if there are
currently long hold times for a real agent.

Let's take a look at what that logic would look like.

.. code-block:: python

   import webapp2
   from twilio import twiml
   from datetime import datetime

   UNACCEPTABLE_WAIT_TIME = 5

   class EnqueueHandler(webapp2.RequestHandler):

       def queue_closed(opening_hour=9, closing_hour=17):
           now = datetime.now()
           # Check if current time is before opening or after closing
           return now.hour < opening_hour or now.hour > closing_hour

       def get(self):
           self.response.headers['Content-Type'] = 'application/xml'

           resp = twiml.Response()
           queue_sid = 'QU123'
           client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
           queue = client.queues.get(queue_sid)
           if queue.average_wait_time > UNACCEPTABLE_WAIT_TIME:
                with resp.gather(num_digits=1, timeout=10, action="/voicemail") as r:
                    r.say("The wait time is currently {} minutes. Press 1 to
                        leave a voicemail, or stay on the line for 
                        an agent.".format(queue.average_wait_time))

           elif self.queue_closed():
               # Redirect straight to voicemail, no need to press a button.
               resp.say("The queue is currently closed. Please stay on the line
                   to leave a voicemail.")
               resp.redirect('/voicemail')
               self.response.write(str(resp))

           resp.enqueue("radio-callin-queue",
               waitUrl="/twiml/wait", waitMethod="GET")
           self.response.write(str(resp))

   class WaitHandler(webapp2.RequestHandler):
       # Rest of the file is the same as the previous pages...

If the average queue wait time is higher than some threshold, we listen for
a key input, and redirect people to voicemail if they press a key. If the user
does not press a key, they'll just fall through to the <Enqueue> verb at the
bottom of the handler. If the queue is closed, we redirect straight to
voicemail.

Otherwise, the queue is open and wait times are short, so we place people in
the call queue.

We need to add a new handler for our voicemail endpoint. Set up the following
route to listen at ``/voicemail``.

.. code-block:: python

   import webapp2
   from twilio import twiml
   from datetime import datetime

   UNACCEPTABLE_WAIT_TIME = 5

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

Advanced Features
------------------

That's the end of the content for this tutorial. If you still have some time,
try implementing some of these advanced features:

- Send an email to yourself when someone leaves a new recording.
- Write a unit test to check the logic in your controller.

.. _Twilio Dashboard: https://www.twilio.com/user/account/log/recordings
