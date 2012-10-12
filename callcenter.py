import webapp2
import util
from twilio import twiml
from twilio import rest

NUMBER = ""

# Change this to a sub account
ACCOUNT_SID = ""
AUTH_TOKEN = ""
APP_SID = ""

client = rest.TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

class BossHandler(webapp2.RequestHandler):

    def get(self):
        """Enqueue a caller into the entry queue"""
        self.response.headers['Content-Type'] = 'application/xml'

        resp = twiml.Response()
        d = resp.dial()
        d.conference("boss")

        self.response.write(str(resp))


class WaitHandler(webapp2.RequestHandler):

    def get(self):
        """Tell a caller information about how long they have waited"""
        self.response.headers['Content-Type'] = 'application/xml'

        resp = twiml.Response()

        messages = [
            "You are number %s in line." % self.request.get('QueuePosition'),
            "You've been in line for %s seconds." % self.request.get('QueueTime'),
            "Average wait time is %s seconds." % self.request.get('AverageQueueTime'),
        ]

        for message in messages:
            resp.say(message)

        resp.play("http://com.twilio.music.rock.s3.amazonaws.com/nickleus_-_"
                  "original_guitar_song_200907251723.mp3")

        self.response.out.write(str(resp))


class EnqueueHandler(webapp2.RequestHandler):

    def get(self):
        """Enqueue a caller into the entry queue"""
        self.response.headers['Content-Type'] = 'application/xml'

        resp = twiml.Response()
        resp.say("You are being enqueued now.")
        resp.enqueue(self.request.params.get('queue', 'support'),
                waitUrl='/twiml/wait', waitMethod='GET')
        resp.sms("Thanks for calling into today. How was your call?")
        self.response.write(str(resp))


class DequeueHandler(webapp2.RequestHandler):

    def get(self):
        """Enqueue a caller into the entry queue"""
        self.response.headers['Content-Type'] = 'application/xml'

        resp = twiml.Response()
        resp.say("Looking for a caller")
        d = resp.dial(record=True)
        d.queue(self.request.params.get('queue', 'support'),
            url="/twiml/record-consent")
        resp.pause(length=10)
        resp.redirect()
        self.response.write(str(resp))


class ConsentHandler(webapp2.RequestHandler):

    def get(self):
        """Inform the caller that the call may be recorded"""
        self.response.headers['Content-Type'] = 'application/xml'

        resp = twiml.Response()
        resp.say("This call may be recorded for quality purposes")

        self.response.write(str(resp))


class MenuHandler(webapp2.RequestHandler):

    def post(self):
        choice = self.request.params('Digits')

        if choice == '1':
            self.redirect('/twiml/enqueue?queue=support')
        elif choice == '2':
            self.redirect('/twiml/enqueue?queue=sales')
        elif choice == '3':
            self.redirect('/twiml/enqueue?queue=marketing')
        else:
            self.redirect('/twiml/menu')

    def get(self):
        """Let the caller choose what department to queue into"""
        self.response.headers['Content-Type'] = 'application/xml'

        resp = twiml.Response()
        gather = resp.gather()
        gather.say("For support, press 1")
        gather.say("For sales, press 2")
        gather.say("For marketing, press 3")
        resp.redirect()

        self.response.write(str(resp))


class SupportHandler(webapp2.RequestHandler):

    def get(self):
        params = {
            "token": util.generate_token(ACCOUNT_SID, AUTH_TOKEN, APP_SID)
        }
        self.response.out.write(render_template("index.html", params))


class CallHandler(webapp2.RequestHandler):

    def get(self):
        """Show a list of all the current calls"""
        params = {
            "calls": client.calls.iter(status="in-progress"),
        }

        self.response.out.write(render_template("calls.html", params))

    def post(self):
        sid = self.request.params.get('sid')

        if sid == '':
            return 

        call = client.calls.get(sid)
        call.redirect('/twiml/boss')


class FeedbackHandler(webapp2.RequestHandler):

    def get(self):
        """Show a list of all the text messages to this number"""
        params = {
            "messages": client.sms.messages.iter(),
        }

        self.response.out.write(render_template("messages.html", params))


app = webapp2.WSGIApplication([
    ('/twiml/boss', BossHandler),
    ('/twiml/wait', WaitHandler),
    ('/twiml/menu', MenuHandler),
    ('/twiml/dequeue', DequeueHandler),
    ('/twiml/enqueue', EnqueueHandler),
    ('/twiml/record-consent', ConsentHandler),
    ('/web/support', SupportHandler),
    ('/web/calls', SupportHandler),
    ('/web/feedback', FeedbackHandler),
], debug=True)
