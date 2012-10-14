.. _dynamic_apps:

Building Dynamic Applications
=============================

We've built awesome Twilio applications in the last two sections, but we've
been limited to static TwiML. The true power of Twilio can only be unlocked by
using a web application.

This section assumes you've completed the :ref:`setup` and have the Google App Engine
SDK running locally on your computer.

Your first web application
--------------------------

The first part of the guide walked you through running a sample application.
Before continuing, make sure that app is running and you have "Hello World"
displayed in your browser. If you can't remember how to run the sample app,
refer back to :ref:`setup`.


Before we can write our web application, we need to understand the Hello World
example. Let's go through the example line-by-line and how it works. Inside our
``main.py`` file:

.. literalinclude:: ../main.py
   :language: python
   :lines: 1


This line is the first part of our application. We use the `webapp2
<http://webapp-improved.appspot.com/>`_ Python module to create our web application,
so we must do an import before we can use it in our code.

.. literalinclude:: ../main.py
   :language: python
   :lines: 3-6

This code handles incoming requests to our application at the specified URL.
Whenever a user makes a request to our application, this is the code that
will be run. The output of the code gets displayed to the web browser.

Here we only define a single method on the class called ``get``. If you
remember your HTTP verbs from the :ref:`http` section, this method name
corresponds to an HTTP GET. We'll show later how to handle different HTTP
verbs, such as POST or DELETE.

.. literalinclude:: ../main.py
   :language: python
   :lines: 8-

Here we actually create our application. In the `webapp2` framework web
applications are a mapping of URLs to request handler classes. The above
mapping says "Whenever someone visits the front page of my application
(the ``/`` url), process that request using the HelloWorld request handler class".

Your first task will be to change the message displayed in your browser. Open
up ``main.py`` in your text editor and change the "Hello World" message on line
6 to "Hello TwilioCon". Refresh the page to see your new message.

Congratulations! You've just created your first web application.

Responding with TwiML
---------------------

A simple message is great, but we want to use our application to serve TwiML.
How do we respond with TwiML instead of plain text?  First, let's change the
message we respond with to valid TwiML.

.. code-block:: python
   :emphasize-lines: 6

   import webapp2
    
   class HelloWorld(webapp2.RequestHandler):
    
       def get(self):
           self.response.write('<Response><Say>Hello TwilioCon</Say></Response>')
    
    
   app = webapp2.WSGIApplication([
       ('/', HelloWorld),
   ], debug=True)

When someone requests the front page of our application, they will now get TwiML
instead of HTML. However, if you refresh your page, nothing seems to have
changed. 

The problem is that while we're sending back TwiML, the browser still
thinks we're sending it HTML. To fix this problem we'll include additional
metadata via an HTTP header to tell the browser we're sending valid TwiML.

.. code-block:: python
   :emphasize-lines: 6

   import webapp2
    
   class HelloWorld(webapp2.RequestHandler):
    
       def get(self):
           self.response.headers['Content-Type'] = "application/xml"
           self.response.write('<Response><Say>Hello TwilioCon</Say></Response>')

   app = webapp2.WSGIApplication([
       ('/', HelloWorld),
   ], debug=True)

When you refresh the page, you should now see the entire TwiML response (and it
may even be highlighted and formatted).


Using the Twilio Helper Library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Manually writing TwiML soon becomes very tiresome. If you miss a single ending
tag, your entire application can break. Instead, we'll use the ``twilio-python``
helper library to generate TwiML for us. This way we won't have to worry about
messing up the syntax.

.. code-block:: python
   :emphasize-lines: 2, 9-11

   import webapp2
   from twilio import twiml
    
   class HelloWorld(webapp2.RequestHandler):
    
       def get(self):
           self.response.headers['Content-Type'] = "application/xml"

           response = twiml.Response()
           response.say("Hello TwilioCon")
           self.response.write(str(response))

   app = webapp2.WSGIApplication([
       ('/', HelloWorld),
   ], debug=True)


When you refresh your page nothing should look different. The helper library
code we just wrote is equivalent to the static TwiML we had before. Let's
explain what the added code is actually doing.

.. code-block:: python

   response = twiml.Response()

Here we create a new Response object. We'll add additional TwiML verbs using
methods on this object. We also use this object to output our TwiML into a
string.

.. code-block:: python

   response.say("Hello TwilioCon")

This methods adds a Say verb to the response. There are similar methods on the
response object for Play, Gather, Record, and Dial. We've already covered these
verbs in the previous sections.

.. code-block:: python

   self.response.write(str(response))

Here we turn our response object into a string using Python's built in string
function. We then write this string to the response object.

The Weather Channel
-------------------

So far all our responses look the same. We're just returning static TwiML as we
did that the last two sessions. Now we're about to show you why building a
dynamic application is so powerful. Instead of simply reading a message, we'll
inform the caller of the current weather in his or her zipcode.

.. note::

    The zipcode information Twilio passes to our application is the zipcode of
    the caller's phone number, not to be confused with the zipcode of live
    location of the caller themselves.

.. code-block:: python
   :emphasize-lines: 2,10,11,14,15

   import webapp2
   from util import current_weather
   from twilio import twiml
    
   class HelloWorld(webapp2.RequestHandler):
    
       def get(self):
           self.response.headers['Content-Type'] = "application/xml"

           weather = current_weather(self.request.get("FromZip", "94117"))
           city = self.request.get("FromCity", "San Francisco")

           response = twiml.Response()
           response.say("Hello from " + city)
           response.say("The current weather is " + weather)
           self.response.write(str(response))

   app = webapp2.WSGIApplication([
       ('/', HelloWorld),
   ], debug=True)


Now visit your page. You'll see the following message.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <Response>
      <Say>Hello from San Francisco</Say>
      <Say>The current weather is Partly Cloudy, 65 degrees</Say>
    </Response>


Our city defaults to San Francisco in case we can't find your zipcode or city.
To test out the greeting, add the ``FromZip`` and ``FromCity`` parameter to your URL.

.. code-block:: bash

    http://localhost:8080/?FromZip=15601&FromCity=Greensburg

You should now see the weather for Greensburg, PA show up in your TwiML response.

.. code-block:: xml

   <?xml version="1.0" encoding="UTF-8"?>
   <Response>
     <Say>Hello from Greensburg</Say>
     <Say>The current weather is Cloudy, 59 degrees</Say>
   </Response>

Whenever an HTTP request is sent to your application from Twilio, it includes
data in query string and body of the request. The code we added when
constructing the Say verb pulls that data from the HTTP request parameter.

.. code-block:: python

   self.request.get('FromZip')

Incoming Twilio Data
~~~~~~~~~~~~~~~~~~~~

Adding this parameter to your URL mimics the request that Twilio will send to
your server. All TwiML requests made by Twilio include additional information
about the caller. Here is short list of some of the data that Twilio will send
your way.

=============== ===========
Parameter       Description
=============== ===========
``From``        The phone number or client identifier of the party that initiated the call. 
``To``          The phone number or client identifier of the called party.
``CallStatus``  A descriptive status for the call. The value is one of queued, ringing, in-progress, completed, busy, failed or no-answer
``FromCity``    The city of the caller.
``FromState``   The state or province of the caller.
``FromZip``     The postal code of the caller.
``FromCountry`` The country of the caller.
=============== ===========

Phone numbers are formatted in E164 format (with a '+' and country code, e.g.
`+1617555121`).

For a complete list, check out `Twilio request parameters  
<http://www.twilio.com/docs/api/twiml/twilio_request#synchronous-request-parameters>`_ 
on the Twilio Docs.

Gathering Digits From the Caller
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Since not everyone's phone number is from the location they currently live,
it may be helpful to add a feature to our app for checking the weather of
any zipcode. To achieve this, we're going to use a TwiML verb called ``<Gather>``.

Let's update our file to look like this:

.. code-block:: python
    :emphasize-lines: 12,13,14,17-43,46

    import webapp2
    from util import current_weather
    from twilio import twiml
    
    class HelloWorld(webapp2.RequestHandler):
    
        def get(self):
            self.response.headers['Content-Type'] = "application/xml"
            city = self.request.get("FromCity", "San Francisco")

            response = twiml.Response()
            gather = response.gather(method="POST", numDigits=1)
            gather.say("Press one for the weather in " + city)
            gather.say("Press two to get the weather for another zip code.")
            self.response.write(str(response))

        def post(self):
            response = twiml.Response()

            weather = current_weather(self.request.get("FromZip", "94117"))

            digit_pressed = self.request.get("Digits")
            if digit_pressed == "1":
                response.say("The current weather is " + weather)
                response.redirect("/", method="GET")
            else:
                gather = response.gather(action="/weather_for_zip", method="POST", numDigits=5)
                gather.say("Please enter a 5 digit zip code.")
            self.response.write(str(response))

    class GetWeather(webapp2.RequestHandler):
        
        def post(self):
            response = twiml.Response()

            zipcode = self.request.get("Digits")
            weather = current_weather(zipcode)

            response.say("The current weather is " + weather)
            response.redirect("/", method="GET")
            
            self.response.write(str(response))

    app = webapp2.WSGIApplication([
        ('/', HelloWorld),
        ('/weather_for_zip', GetWeather),
    ], debug=True)


A few things of note in this example. The code

.. code-block:: python

    response.gather(action="/weather_for_zip", method="POST", numDigits=5)

generates the TwiML for

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Gather method="POST" action="/weather_for_zip" numDigits="5" />
    </Response>

The ``method`` and ``action`` of the ``<Gather>`` verb tell Twilio what to do when the caller
finishes entering digits. In this example, we use the ``numDigits`` attribute to
know when the caller is done pressing digits. This works because we know how many
digits are in a valid zipcode. If we didn't know this, we could use another attribute called
``finishOnKey``.

When the caller has entered 5 digits, Twilio will do a ``POST`` request to
``/weather_for_zip`` with the digits pressed passed as the ``Digits`` argument
through HTTP. We use these digits to lookup the weather, just as we did for the original
app with the zipcode passed in by Twilio.

We've added a second ``webapp2.RequestHandler`` class. We also configure this handler
to respond to the URL ``/weather_for_zip`` which is what we're POSTing the second
gather to.

Another new addition is the ``post`` function on the original ``HelloWorld`` handler.
This code is triggered when an HTTP client sends a ``POST`` to the ``/`` URL instead of a
``GET``. Because our first ``<Gather>`` specifies a ``POST`` method and no ``action``, the default
``action`` is the current URL (In this case, "/"). So, this code is what will get run
after the first ``<Gather>`` is ``POST``ed.


Handling Server Errors
--------------------------------------------

Sometimes, errors happen on the web application side of the code.

.. image:: _static/app_error.png

Don't panic if you see this. The stack trace will usually give you
hints as to what error the application encountered, and where it occurred.

Some errors may also appear on the AppEngine logs. If the errors on the browser
aren't too informative, try clicking on the Logs button on the AppEngine
Launcher.

.. TODO: maybe we should include a screen capture of where the Logs button is on the AppEngine launcher. I wanna make the 
.. red circles but I probably can't make it the same as what we have on the Initial Setup guide

Deploy your Twilio application
------------------------------

We're now ready to hook up your brand new application to a Twilio number. To do this,
we'll need to host your application live on the Internet, so that Twilio can find it!

Open the Google App Engine Launcher application, highlight your application, and hit
the "Deploy" button. A window will pop up and show you the status of your
deployment. It should take less than a minute to deploy.

.. image:: _static/deployapp.png

Once it's deployed, take the URL for your application,
``http://<your-application-name>.appspot.com`` and set it as the voice number
for your Twilio phone number. Configuring Twilio numbers is covered in more
detail in :ref:`configure-number`.

.. note:: 

   Since we have only implemented the GET endpoint, be sure to configure your
   number to use the GET method instead of the default POST*

Now give it a call. You should hear your custom message. Hooray!
