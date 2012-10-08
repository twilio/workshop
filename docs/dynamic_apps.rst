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

Here we actually create our web application objects. In the `webapp2` framework, 
web applications are just a mapping of URLs to request handlers. The above mapping
says "Whenever someone vists the front page of my application, process that
requests using this handler class".

Your first task will be to change the message displayed in your browser. Open up `main.py` in your text editor and change

Personalized SMS messages
-------------------------

Deploy your Twilio application
------------------------------
