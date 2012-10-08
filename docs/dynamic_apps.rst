.. _dynamic_apps:

Building Dynamic Applications
=============================

So far we've built some awesome Twilio applications, but we've been limited to
static TwiML. The true power of Twilio is unlocked with the full power of a web
application.

This section assumes you've completed :ref:`setup` and have the Google App Engine
SDK running locally on your computer.

Your first web application
--------------------------

The first part of the guide just showed you how to run a sample application.
You should have made it far enough to open a webpage in your browser that shows
'Hello World'. We didn't actually explain how that example work, so let's do
that now.

.. literalinclude:: ../main.py
   :language: python
   :lines: 1 


We need to use the `webapp2` module for creating our web application, so we
import it into our own main module.

.. literalinclude:: ../main.py
   :language: python
   :lines: 3-6

This class handles requests to out application. Whenever an HTTP request is
made to our app, a method on this class in envoked. The method will usuually
write some contents out to the response for display in a browser.

Here, we only define a single method on the class called `get`. If you remember
your HTTP versb from the first section, this method name corresponds to that
method. We'll show later how to handle different types of requests.

.. literalinclude:: ../main.py
   :language: python
   :lines: 8-

Here we actually create our web application objects. In the `webapp2`
framework, web applications are just a mapping of URLs to request handlers. The
above mapping says "Whenever someone vists the front page of my application,
process that requests using this handler class".

Your first task will be to change the message displayed in your browser. Open
up `main.py` in your text editor and change the "Hello World" message on line 6
to "Hello TwilioCon". Refresh the page to see your new message.

Responding with TwiML
---------------------

A simple message is great, but how do we respond with TwiML instead of plain text?
First, let's change the message we responsd with to valid TwiML.

.. code-block:: python
   :emphasize-lines: 6

   import webapp2
    
   class HelloWorld(webapp2.RequestHandler):
    
       def get(self):
           self.response.write('<Response><Say>Hello TwilioCon</Say></Response>')
    
    
   app = webapp2.WSGIApplication([
       ('/', HelloWorld),
   ], debug=True)

If you refresh your page, nothing seems to have changed. This is strange. To
see our changes, we'll need tell the broswer that the content we are returning
is XML, not HTML.


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


Personalized Greetings
----------------------

So far, this all seems like a big waste of time. We're just returning static
TwiML, and we did that the last two sessions. Now we're about to show you why
building a dyanmic application is so much better.


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
name to your message, add a parameter to your URL. Introduce query string
arguments. Talk about all the data that Twilio sends your way.

.. code-block:: bash

    http://localhost:8080/?FromNumebr=+5005550000


Deploy your Twilio application
------------------------------

We're now ready to hook up your brand new application to a Twilio number. Open
the Google App Engine Launcher application, highlight your application, and hit
the 'Deploy' button. A window will pop up and show you the status of your
deployemnt. It should take less than a minute to deploy. Once it's deployed,
get the url for your application and set it as the voice number for your Twilio
phone number. Now give it a call. You should hear a custom message. Hooray.
