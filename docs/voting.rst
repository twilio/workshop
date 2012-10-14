.. _voting:

SMS Polling and Voting
======================

One great use of SMS is to get large groups to vote on something easily. Nearly
everyone in the audience will have a cell phone in their pocket - why not let
them send in their votes over SMS?

We'll create a simple Twilio application to record and report votes via SMS. 

Ballot Format
-------------

For this poll ballots don't need a format. To vote text your choice to your
Twilio number.

For example, to vote for Twilio, you'd text the following::

    twilio

To see all the votes we'll use the `twilio-python
<https://github.com/twilio/twilio-python>`_ helper library to fetch data from
the Twilio REST API. Open ``main.py`` and add the following lines.

.. code-block:: python
   :emphasize-lines: 2,4

   import webapp2
   from twilio.rest import TwilioRestClient

   client = TwilioRestClient("ACCOUNT_SID", "AUTH_TOKEN")

   class HelloWorld(webapp2.RequestHandler):

       def get(self):
           self.response.write('Hello World!')

   app = webapp2.WSGIApplication([
       ('/', HelloWorld),
   ], debug=True)

We're creating a client to talk to the REST API. You'll need to replace the
**ACCOUNT_SID** and **AUTH_TOKEN** with your account credentials. Your
credentials are located at the top of your `account dashboard
<https://www.twilio.com/user/account>`_.

With the client created, we can now query the Twilio REST API for SMS messages.

.. code-block:: python
   :emphasize-lines: 6-10,19

   import webapp2
   from twilio.rest import TwilioRestClient

   client = TwilioRestClient("ACCOUNT_SID", "AUTH_TOKEN")

   class SmsVoting(webapp2.RequestHandler):

       def get(self):
           for msg in client.sms.messages.iter():
                self.response.write(msg.body + "\n")

   class HelloWorld(webapp2.RequestHandler):

       def get(self):
           self.response.write('Hello World!')

   app = webapp2.WSGIApplication([
       ('/', HelloWorld),
       ('/sms', SmsVoting),
   ], debug=True)

To view your votes, open the Google App Engine Launcher. Click the **Run**
button and then **Browse** button. In the URL bar, add ``/sms`` to the URL and
reload.

This page will fail if you have multiple Twilio phone numbers. To fix this
problem, we'll filter messages based on the **To** phone number. Replace
``TWILIO_PHONE_NUMBER`` with one of your Twilio phone numbers. If you can't
remember your number, you'll find them listed in the `Twilio account portal
<https://www.twilio.com/user/account/phone-numbers/incoming>`_.

.. code-block:: python
   :emphasize-lines: 9

   import webapp2
   from twilio.rest import TwilioRestClient

   client = TwilioRestClient("ACCOUNT_SID", "AUTH_TOKEN")

   class SmsVoting(webapp2.RequestHandler):

       def get(self):
           for msg in client.sms.messages.iter(to="TWILIO_PHONE_NUMBER"):
                self.response.write(msg.body + "\n")

   class HelloWorld(webapp2.RequestHandler):

       def get(self):
           self.response.write('Hello World!')

   app = webapp2.WSGIApplication([
       ('/', HelloWorld),
       ('/sms', SmsVoting),
   ], debug=True)

Still, we're only seeing the contents of the messages.

Tallying Votes
--------------

In our election participants can only vote once, therefore each message should
count for a single vote. We'll use a dictionary to keep track of votes.

Instead of just printing the message body we'll print the message body and the
number of votes it received.

.. code-block:: python
   :emphasize-lines: 3,10-16

   import webapp2
   from twilio.rest import TwilioRestClient
   from collections import defaultdict

   client = TwilioRestClient("ACCOUNT_SID", "AUTH_TOKEN")

   class SmsVoting(webapp2.RequestHandler):

       def get(self):
           votes = defaultdict(int)

           for msg in client.sms.messages.iter(to="TWILIO PHONE NUMBER"):
               votes[msg.body] += 1

           for vote, total in votes.items():
                self.response.write("{} {}\n".format(vote, total))

   class HelloWorld(webapp2.RequestHandler):

       def get(self):
           self.response.write('Hello World!')

   app = webapp2.WSGIApplication([
       ('/', HelloWorld),
       ('/sms', SmsVoting),
   ], debug=True)

We can now see tallies. However, this code is very brittle. Votes for ``foo``
and ``Foo`` won't count for the same thing. Let's normalize the message bodies
so that similar votes count for the same option.

.. code-block:: python
   :emphasize-lines: 13

   import webapp2
   from twilio.rest import TwilioRestClient
   from collections import defaultdict

   client = TwilioRestClient("ACCOUNT_SID", "AUTH_TOKEN")

   class SmsVoting(webapp2.RequestHandler):

       def get(self):
           votes = defaultdict(int)

           for msg in client.sms.messages.iter(to="TWILIO PHONE NUMBER"):
               votes[msg.body.upper().strip()] += 1

           for vote, total in votes.items():
                self.response.write("{} {}\n".format(vote, total))

   class HelloWorld(webapp2.RequestHandler):

       def get(self):
           self.response.write('Hello World!')

   app = webapp2.WSGIApplication([
       ('/', HelloWorld),
       ('/sms', SmsVoting),
   ], debug=True)


Preventing Cheaters
-------------------

Cheaters never prosper. And currently they don't get caught either. Any person
can vote any number of times. We'll keep track of every number that's already voted,
only allowing them a single vote. To do this phone numbers will be added to a
set and checked before each vote is tallied.

.. code-block:: python
   :emphasize-lines: 11,14-15,18

   import webapp2
   from twilio.rest import TwilioRestClient
   from collections import defaultdict

   client = TwilioRestClient("ACCOUNT_SID", "AUTH_TOKEN")

   class SmsVoting(webapp2.RequestHandler):

       def get(self):
           votes = defaultdict(int)
           voted = set()

           for msg in client.sms.messages.iter(to="TWILIO PHONE NUMBER"):
               if msg.from_ in voted:
                   continue

               votes[msg.body.upper().strip()] += 1
               voted.add(msg.from_)

           for vote, total in votes.items():
                self.response.write("{} {}\n".format(vote, total))

   class HelloWorld(webapp2.RequestHandler):

       def get(self):
           self.response.write('Hello World!')

   app = webapp2.WSGIApplication([
       ('/', HelloWorld),
       ('/sms', SmsVoting),
   ], debug=True)

Graphing the Results
--------------------

No election is complete without graphs. Let's take the results from the
previous section and make some pretty graphs. We'll use the `Google Graph API
<https://developers.google.com/chart/image/docs/making_charts>`_ due to its
simplicity and price (free).

.. code-block:: python
   :emphasize-lines: 1,21-31

   import urllib
   import webapp2
   from twilio.rest import TwilioRestClient
   from collections import defaultdict

   client = TwilioRestClient("ACCOUNT_SID", "AUTH_TOKEN")

   class SmsVoting(webapp2.RequestHandler):

       def get(self):
           votes = defaultdict(int)
           voted = set()

           for msg in client.sms.messages.iter(to="TWILIO PHONE NUMBER"):
               if msg.from_ in voted:
                   continue

               votes[msg.body.upper().strip()] += 1
               voted.add(msg.from_)

           url = "https://chart.googleapis.com/chart"

           options = {
               "cht": "pc",
               "chs": "500x500",
               "chd": "t:" + ",".join(map(str, votes.values())),
               "chl": "|".join(votes.keys()),
           }

           image = '<img src="{}?{}">'.format(self.url, urllib.urlencode(options))
           self.response.write(image)

   class HelloWorld(webapp2.RequestHandler):

       def get(self):
           self.response.write('Hello World!')

   app = webapp2.WSGIApplication([
       ('/', HelloWorld),
       ('/sms', SmsVoting),
   ], debug=True)


Existing Solutions
------------------

`Wedgies <http://wedgies.com/>`_ is a very similar concept built on top of
Twilio, but questions are limited to two answers. Great for simple surveys, but
not for elections.
