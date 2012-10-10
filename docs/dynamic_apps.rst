.. _dynamic_apps:

Building Dynamic Applications
=============================

We've built awesome Twilio applications in the last two sections, but we've
been limited to static TwiML. The true power of Twilio can only be unlocked by
using a web application.

This section assumes you've completed :ref:`setup` and have the Google App Engine
SDK running locally on your computer.

Your first web application
--------------------------

The first part of the guide walked you through running a sample application.
Before continuing, make sure that example is running and you have "Hello World"
displayed in your browser. If you can't remember how to run the sample app,
refer back to :ref:`setup`


Before we can write our web application, we need to understand the Hello World
example. Let's go through the example line-by-line and how it works.

.. literalinclude:: ../main.py
   :language: python
   :lines: 1 


This line is first part of our application. We use the `webapp2
<http://webapp-improved.appspot.com/>`_ module to create our web application,
so we must import before we can use it in our code.

.. literalinclude:: ../main.py
   :language: python
   :lines: 3-6

This class handles incoming requests to our application at a specific URL.
Whenever a user makes a request to our application, a method on this class will
be envoked. The method will usually write out a response for display in a
browser. 

Here, we only define a single method on the class called `get`. If you remember
your HTTP verbs from the first section, this method name corresponds to an HTTP
GET. We'll show later how to handle different HTTP verbs, such as POST or
DELETE.

.. literalinclude:: ../main.py
   :language: python
   :lines: 8-

Here we actually create our application. In the `webapp2` framework, web
applications are a mapping of URLs to request handler classes. The above
mapping says "Whenever someone vists the front page of my application, process
that requests using the HelloWorld request handler class".

Your first task will be to change the message displayed in your browser. Open
up `main.py` in your text editor and change the "Hello World" message on line 6
to "Hello TwilioCon". Refresh the page to see your new message.

Congratulations, you've just created your first web application!

Responding with TwiML
---------------------

A simple message is great, but we want to use our applicatin to serve TwiML?
How do we respond with TwiML instead of plain text?  First, let's change the
message we responsd with to valid TwiML.

.. code-block:: python
   :emphasize-lines: 6

   import webapp2
    
   class HelloWorld(webapp2.RequestHandler):
    
       def get(self):
           self.response.write('<Response><Say>Hello TwilioCon</Say></Response>')
    
    
   app = webapp2.WSGIApplication([
       ('/', HelloWorld),
   ], debug=True)

When someone requests the frontpage of our application, they will now get TwiML
instead of HTML. However, if you refresh your page, nothing seems to have
changed. The problem is that while we're sending back TwiML, the browser still
thinks we're sending it HTML. To fix this problem, we'll include additional
metadata to tell the browser we're sending valid TwiML.

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

When you refresh the page, you should now see the entire TwiML response (and
maybe it's even highlighted and formatted).


Using the Twilio Helper Library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Manually writing TwiML soon becomes very painful. If you miss a single ending
tag, your entire application can break. Instead, we'll use the `twilio-python`
helper library to generate TwiML for us. This way, we won't have to worry about
messing up the syntax.

.. code-block:: python
   :emphasize-lines: 2, 9-11

   import webapp2
   from twilio import twiml
    
   class HelloWorld(webapp2.RequestHandler):
    
       def get(self):
           self.response.headers['Content-Type'] = "application/xml"

           response = twiml.Response()
           respone.say("Hello TwilioCon")
           self.response.write(str(response))

   app = webapp2.WSGIApplication([
       ('/', HelloWorld),
   ], debug=True)


When you refresh your page, nothing should look different. The helper library
code we just wrote is equivalent to the static TwiML we had before. Let's
explain what the added code is actually doing.

.. code-block:: python

   response = twiml.Response()

Here we create a new Response object. We'll add additional TwiML verbs using
methods on this object. We also use this object to output our TwiML into a
string.

.. code-block:: python

   respone.say("Hello TwilioCon")

This methods adds a Say verb to the response. There are similar methods on the
resonse object for Play, Gather, Record, and Dial. We've already covered these
verbs in the previous sections.

.. code-block:: python

   self.response.write(str(response))

Here we turn our response object into a string using Python's built in string
function. We then write this string to the response object.

Personalized Greetings
----------------------

So far, all our responses look the same. We're just returning static TwiML, and
we did that the last two sessions. Now we're about to show you why building a
dyanmic application is so powerful. First, a simple example.

.. code-block:: python
   :emphasize-lines: 10

   import webapp2
   from twilio import twiml
    
   class HelloWorld(webapp2.RequestHandler):
    
       def get(self):
           self.response.headers['Content-Type'] = "application/xml"

           response = twiml.Response()
           respone.say("Hello " + self.request.params('FromNumber'))
           self.response.write(str(response))

   app = webapp2.WSGIApplication([
       ('/', HelloWorld),
   ], debug=True)


Now visit your page. You'll see the message "Hello " without a name. To add a
name to your message, add a parameter to your URL. 

.. code-block:: bash

    http://localhost:8080/?From=+5005550000

Whenever an HTTP request is sent to your application, it includes data in query
string and body of the request. The line we added

.. code-block:: python

   self.request.params('FromNumber')

Incoming Twilio Data
~~~~~~~~~~~~~~~~~~~~

Adding this parameter to your URL mimics the request that Twilio will send to
your server. All TwiML requests made by Twilio include additional information
about the caller. Here is short list of some of the data that Twilio will send your way.

Introduce query string and form data. Talk about parameters

=========== ===========
Parameter   Description
=========== ===========
From        The phone number or client identifier of the party that initiated the call. Phone numbers are formatted with a '+' and country code, e.g. +1617555121
To          The phone number or client identifier of the called party. Phone numbers are formatted with a '+' and country code, e.g. +16175551212
CallStatus  A descriptive status for the call. The value is one of queued, ringing, in-progress, completed, busy, failed or no-answer
Body        The text body of the SMS message. Up to 160 characters long.
=========== ===========

Deploy your Twilio application
------------------------------

We're now ready to hook up your brand new application to a Twilio number. Open
the Google App Engine Launcher application, highlight your application, and hit
the 'Deploy' button. A window will pop up and show you the status of your
deployemnt. It should take less than a minute to deploy. Once it's deployed,
get the url for your application and set it as the voice number for your Twilio
phone number. Now give it a call. You should hear a custom message. Hooray.
