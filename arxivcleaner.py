import webapp2
import urllib
from google.appengine.ext.webapp import template


def strip_html(string):
    new_string = ""
    start = 0
    end = 0
    while True:
        try:
            start = string.index("&lt;", end)
            new_string += string[end:start]
            end = string.index("&gt;", start) + 4
        except:
            break
    return new_string


def clean_feed(feed):

    start = 0
    end = 0

    new_feed = ""

    while True:
        try:
            start = feed.index("<dc:creator>", end)
            new_feed += feed[end:start]
            end = feed.index("</dc:creator>", start)
        except:
            new_feed += feed[end:]
            break
        else:
            # 12 is the length of <dc:creator>
            authors = feed[start + 12:end].strip()
            new_feed += "<dc:creator>" + strip_html(authors)

    return new_feed


FEED_URL = {}
FEED_URL['astro-ph'] = "http://localhost/~tom/astro-ph"


class FeedCleaner(webapp2.RequestHandler):

    def get(self, feed):
        feed = clean_feed(urllib.urlopen(FEED_URL[feed]).read())
        self.response.headers['Content-Type'] = 'text/xml'
        self.response.write(feed)


class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.write(template.render('templates/main.html', {}))


app = webapp2.WSGIApplication([
                               ('/', MainPage),
                               ('/(.*)', FeedCleaner)
                               ],
                              debug=True)
