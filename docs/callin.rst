.. _callin:

Radio Call In
=============

In this workshop we'll be designing a radio call in application 
using Twilio's new <Queue> functionality.

Using the Twilio Helper Libraries
---------------------------------

Though this workshop will assume use of Python and the twilio-python helper
library, Twilio offers helper libraries for a large set of languages. If you
aren't using Python, download the `helper library`_ for your language of
choice. You'll need the library in the next section.

For the twilio-python helper library, you may find the `Queue API
Reference`_ helpful for this workshop.

.. _here: http://www.twilio.com/docs/libraries
.. _Queue API Reference: https://twilio-python.readthedocs.org/en/latest/api/rest/resources.html#queues

Using Queue (TwiML)
-------------------
We'll need two Twilio phone numbers to work with Queue - one for the DJ to
dequeue calls from, and one for the queue that the listener will call into.

First, we'll enqueue some calls via TwiML. In the example below, we enqueue
to a queue named ``radio-callin-queue``. Note that queues are created on
<Enqueue> if they do not already exist.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Say>You are being enqueued now.</Say>
        <Enqueue>radio-callin-queue</Enqueue>
    </Response>

Bind this TwiML to your listener queue number.

We can spice it up by adding some wait music, using the ``waitUrl`` parameter.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Enqueue waitUrl="/wait-loop">radio-callin-queue</Enqueue>
    </Response>

The ``/wait-loop`` endpoint goes to some TwiML that plays music. The ``waitUrl``
TwiML document supports a `subset of TwiML verbs`_.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Say>Please hold.</Say>
        <Play>http://com.twilio.sounds.music.s3.amazonaws.com/MARKOVICHAMP-Borghestral.mp3</Play>
    </Response>



For the DJ dequeuing number, we use some TwiML that bridges the current call
to the queue. Note that <Dial>ing into a queue represents dequeuing a caller
on the queue, while the only way to get onto a queue is to be <Enqueue>d.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Dial>
            <Queue>radio-callin-queue</Queue>
        </Dial>
    </Response>

Now, the DJ can call the DJ dequeuing number, and will automatically be routed
to the first member on the queue.

.. _subset of TwiML verbs: http://www.twilio.com/docs/api/twiml/enqueue#attributes-waitUrl

Dynamic Queue Information
-------------------------
Twilio's Queue exposes dynamic inforrmation about the queue state that
you can use to build rich applications. In this section, we'll move past
static TwiML applications and start using the data Queue gives you to
create dynamic TwiML through a web application.

We'll start by working on our hold music. Wouldn't it be cool if we could
tell users where they were in the queue, how long they've been there, or
even the average wait time for their queue? Twilio exposes `all these
parameters`_ when invoking your application's waiting logic via HTTP so that
you can pass it along in your dynamic TwiML!

.. code-block:: python

    class WaitLoop(webapp2.RequestHandler):
        def post(self):
            response = twiml.Response()
            response.say("You are number %s in line." % self.request.get('QueuePosition'))
            response.say("You've been in line for %s seconds." % self.request.get('QueueTime'))
            response.say("The average wait time is currently %s seconds." % self.request.get('AverageQueueTime'))
            response.play("http://com.twilio.music.rock.s3.amazonaws.com/nickleus_-_original_guitar_song_200907251723.mp3")
            self.response.out.write(str(response))

You can also take advantage of similar information when a call is dequeued
through the ``action`` parameter when enqueuing.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Say>You are being enqueued now.</Say>
        <Enqueue action="/dequeue-logic">radio-callin-queue</Enqueue>
    </Response>

.. code-block:: python

    class DequeueLogic(webapp2.RequestHandler):
        def post(self):
            res = self.request.get('QueueResult')
            if res == 'bridged':
                # save to db, ping analytics, whatever you want!


.. _all these parameters: http://www.twilio.com/docs/api/twiml/enqueue#attributes-waiturl-parameters

Queue Times Are Too Long! - A Call to Action
--------------------------------------------
We can use the ``action`` parameter to collect all sorts of useful metrics
on the backend, or even issue hasty apologies for long queue wait times.

Let's try to implement some small features on our dequeue action call to
let our users know we care. Using the `action URL parameters`_, we can
send an SMS apology if the wait time exceeded 30 seconds, or if their
call was rejected from a full queue.

You may find the `helper library documentation`_ for your `language of choice`_
helpful in sending SMS.

Here is some stub code that may help, if you are taking the Python / Google
App Engine route...

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Say>You are being enqueued now.</Say>
        <Enqueue action="/dequeue-logic">radio-callin-queue</Enqueue>
    </Response>

.. code-block:: python

    import webapp2
    class DequeueLogic(webapp2.RequestHandler):
        def post(self):
            
            # ... FILL ME IN ...
            # res = self.request.get('QueueResult')

    app = webapp2.WSGIApplication([('/dequeue-logic', DequeueLogic)], debug=True)

.. _action URL parameters: http://www.twilio.com/docs/api/twiml/enqueue#attributes-action-parameters
.. _helper library documentation: https://twilio-python.readthedocs.org/en/latest/api/rest/resources.html#sms-messages
.. _language of choice: http://www.twilio.com/docs/libraries


See You Next Time - Closing Out the Queue
-----------------------------------------
Unfortunately, all good things must come to an end. It's time for our
radio show to close down until next time - but what about the people
still on the waiting queue?

We can use `Queue`_ and `Member`_ REST API resources to programmatically
look at all of our account's queues and active members on those queues.

Let's write a quick script that will find our queue, loop through its
members, and dequeue each of them with a thank you message. 

.. code-block:: python

    from twilio.rest import TwilioRestClient
    client = TwilioRestClient("ACCOUNT_SID", "AUTH_TOKEN")
    my_queue_name = "radio-callin-queue"

First, we need to `find our queue`_.

.. code-block:: python

    my_queue = None
    for queue in client.queues.list():
        if queue.friendly_name == my_queue_name:
            my_queue = queue


Then, we can iterate over its members and dequeue with some static thank
you TwiML. Try it yourself! Hint: issuing `an HTTP POST to a Member instance`_
will dequeue that member.
    
As a bonus, try allowing the callers being dequeued to record a message 
for the DJs to listen to at the beginning of the next show.

Finally, we can delete the queue using a REST API call.

.. code-block:: python

    my_queue.delete()

.. _Queue: http://www.twilio.com/docs/api/rest/queue
.. _Member: http://www.twilio.com/docs/api/rest/member
.. _find our queue: https://twilio-python.readthedocs.org/en/latest/usage/queues.html
.. _an HTTP POST to a Member instance: http://www.twilio.com/docs/api/rest/member#instance-post
