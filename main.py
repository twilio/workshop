import webapp2

class HelloWorld(webapp2.RequestHandler):

    def get(self):
        self.response.write('Hello World!')


app = webapp2.WSGIApplication([
    ('/', HelloWorld),
], debug=True)
