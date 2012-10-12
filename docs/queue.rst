.. _queue:

Queue Dispatch
==============

Now that we've had a taste of queues and how they work, let's add some
complexity.  When we were building our radio call-in application, we
just had a single DJ pulling people off of a single queue of callers.

Let's think about a customer service call center.  In its simplest
terms, the problem is similar: the only real difference is that you
have multiple customer service reps answering calls from the queue
of customers.  You could actually reuse the radio call-in app without
much modification.

But let's add a requirement: customers can pay for a premium level of
support to ensure that their calls are answered faster.  Now we can
have two queues: one for premium customers, and one for everyone else.

We'll use a simple algorithm: as long as there are customers in the
premium support queue, we answer those calls, and we don't handle the
regular customers until the premium queue is empty.

Enqueue Calls into multiple queues
----------------------------------

We'll use two queues:

* ``premium-customers``
* ``customers``

The customer end is simple.  Our fictitious company will publish a
special phone number for premium customers, and the TwiML served for this
number will push customers into the ``premium-customers`` queue:

.. code-block:: xml

    <?xml version='1.0' encoding='utf-8'?>
    <Response>
        <Enqueue>premium-customers</Enqueue>
    </Response>

... and the TwiML for regular customers just puts them in the ``customers``
queue:

.. code-block:: xml

    <?xml version='1.0' encoding='utf-8'?>
    <Response>
        <Enqueue>customers</Enqueue>
    </Response>

For the customer service reps, it's a little different.  The first bit
of TwiML should try to dial into the premium customer's queue:

.. code-block:: xml

    <?xml version='1.0' encoding='utf-8'?>
    <Response>
        <Dial timeout="1" action="/rep-call-complete" method="GET">
            <Queue>premium-customers</Queue>
        </Dial>
    </Response>

The ``timeout`` parameter in the ``<Dial>`` verb tells Twilio to only wait
for 1 second for a call in the queue to become available.  If that fails
Twilio will request the ``/rep-call-complete`` URL from your webserver
almost immediately.  From there, we can see if the call failed (that is,
the timeout was reached).  If the call failed we then try the regular
``customers`` queue.  If the call succeeded we know that the rep just
finished talking to a customer, and since our rule is that premium
customers get handled first, we have that rep go back to the premium
queue.  Here's what it might look like in the Python code powering our
web server:

.. code-block:: python

    from twilio import twiml

    PREMIUM_QUEUE_SID = 'QU123...'

    class RepCallComplete(webapp2.RequestHandler):
        def get(self):
            response = twiml.Response()
            dial = response.dial(timeout=1, action="/rep-call-complete", method="GET")

            if self.request.params['DequeueResult'] == 'bridged':
                # The rep successfully talked to someone and is now
                # finished with the call, so send them back to the
                # premium queue.
                dial.queue('premium-customers')
            else:
                # The rep failed to dequeue someone.  Based on which
                # queue was tried, we'll have them try another queue.
                if self.request.params['QueueSid'] == PREMIUM_QUEUE_SID:
                    # Failed to get a premium call, try a regular call
                    dial.queue('customers')
                else:
                    # Failed to get a regular call, try for premium
                    dial.queue('premium-customers')

            self.response.out.write(str(response))

So here we've implemented a rudimentary priority queue with two
sub-queues.  We always try to fetch a customer from the
``premium-customers`` queue, but if that fails, we go to the ``customers``
queue.

You might also note that we don't even need the separate TwiML file for
customer support reps when they initially call in.  If we set the
VoiceUrl for the support reps' call-in number to our
``rep-call-complete`` script, we note that the default behavior for when
the ``DequeueResult`` and ``QueueSid`` fields are absent is to connect the
rep to the ``premium-customers`` queue, so our python script also
suffices as the initial entry point for our app.

Testing Twilio Applications
---------------------------

Installing and using local tunnel

https://showoff.io/
local tunnel
pagekite

Local tunnel sometimes doesn't work. Many of these services suffer from the
same problems tthat networks can't be awesome.

So, how do we test if we can't connect to Twilio

Mocking out Twilio
~~~~~~~~~~~~~~~~~~

A simple example showing how, using cUrl, you can actually duplicate many of
Twilio's behaviors


Adding a Feedback Loop
----------------------

- SMS stuff
- Increasing Engagement
