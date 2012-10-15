.. _recording:

Call Recording
==============

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
------------------

That's the end of the content for this tutorial. If you still have some time,
try implementing some of these advanced features:

- Listen to your recordings straight from your Dashboard.
- Export your recordings to a private S3 folder, and delete the Twilio copies
  of the recording.
- Set up monitoring of your application, so that you receive notifications if
  your application becomes unreachable.
- Set up HTTP Authentication so that Twilio must authenticate before reading
  TwiML from your server, and other browsers will receive a 401 Forbidden
  message.

