.. _callin:

Radio Call In
=============

In this workshop, we'll be designing a radio call in application 
using Twilio's new <Queue> functionality.

Using the Twilio Helper Libraries
---------------------------------

Though this workshop will assume use of Python and the twilio-python
helper library, Twilio offers helper libraries for a large set of
languages. Check them out `here`_.

For the twilio-python helper library, you may find the `Queue API
Reference`_ helpful for this workshop.

.. _here: http://www.twilio.com/docs/libraries
.. _Queue API Reference: https://twilio-python.readthedocs.org/en/latest/api/rest/resources.html#queues

Using Queue (TwiML)
-------------------
We'll need two Twilio phone numbers to work with Queue - one for the DJ to
dequeue calls from, and one for the queue that the listener will call into.

First, we'll enqueue some calls via TwiML. In the example below, we enqueue
to a queue named `my-new-twilio-queue`. Note that queues are created on
<Enqueue> if they do not already exist.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Say>You are being enqueued now.</Say>
        <Enqueue>my-new-twilio-queue</Enqueue>
    </Response>

Bind this TwiML to your listener queue number.

We can spice it up by adding some wait music, using the `waitUrl` parameter.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Enqueue waitUrl="my_wait_twiml.xml">my-new-twilio-queue</Enqueue>
    </Response>

The `my_wait_twiml.xml` points to some TwiML that plays music. Like any other
TwiML, we could also <Say> stuff here as well.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Play>http://com.twilio.sounds.music.s3.amazonaws.com/MARKOVICHAMP-Borghestral.mp3</Play>
    </Response>



For the DJ dequeuing number, we use some TwiML that bridges the current call
to the queue.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Dial>
            <Queue>my-new-twilio-queue</Queue>
        </Dial>
    </Response>

Now, the DJ can call the DJ dequeuing number, and will automatically be routed
to the first member on the queue.

Dynamic Queue Information (REST API)
------------------------------------
Twilio's Queue exposes dynamic inforrmation about the queue state that
you can use to build rich applications. In this section, we'll move past
static TwiML applications and start using the data Queue gives you to
create dynamic TwiML through a web application.

We'll start by working on our hold music. Wouldn't it be cool if we could
tell users where they were in the queue, how long they've been there, or
even the average wait time for their queue? Twilio exposes `all these
parameters`_ when invoking your application's waiting logic via HTTP, so
you can pass it along in your dynamic TwiML!

.. _all these parameters: http://www.twilio.com/docs/api/twiml/enqueue#attributes-waiturl-parameters

.. code-block:: python

    class WaitingLoop(webapp2.RequestHandler):
        def post(self):
            response = twiml.Response()
            response.say("You are number %s in line." % self.request.get('QueuePosition'))
            response.say("You've been in line for %s seconds." % self.request.get('QueueTime'))
            response.say("The average wait time is currently %s seconds." % self.request.get('AverageQueueTime'))
            response.play("http://com.twilio.music.rock.s3.amazonaws.com/nickleus_-_original_guitar_song_200907251723.mp3")
            self.response.out.write(str(response))

You can also take advantage of similar information when a call is dequeued,
through the `action` parameter when enqueuing.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Say>You are being enqueued now.</Say>
        <Enqueue action="/dequeue-logic">my-new-twilio-queue</Enqueue>
    </Response>

.. code-block:: python

    class DequeueLogic(webapp2.RequestHandler):
        def post(self):
            res = self.request.get('QueueResult')
            if res == 'bridged':
                # save to db, ping analytics, whatever you want!



Play a Specific Message for the Nth Caller
------------------------------------------

* HEY! I'm going to figure out another app for this, since we don't want persistence.
* and we want to showcase queue, and Nth caller is something we can do without queue, duh.

* Dequeue via REST API: http://www.twilio.com/docs/api/rest/member#instance-post


HTTP -> TwiML
Stub out a flask app, users can fill this in, or webapp2

* TwiML for enqueuing calls.
* Using the twilio.twiml.Response class to generate TwiML

* Action on dequeue (specified at enqueue time) [ this is the key for keeping track of the nth caller ]

* waitUrl parameters passed in - 
* action parameters passed in - time call spent in queue
* Intro to the twilio.client.queues resource
    * List and confirm that our queue exists
    * See the amount of calls on it.
