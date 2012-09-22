import webapp2
import urllib
from google.appengine.ext.webapp import template

from BeautifulSoup import BeautifulSoup


def strip_html(string):
    string = string.replace('&lt;', '<')
    string = string.replace('&gt;', '>')
    return "".join(BeautifulSoup(string).findAll(text=True))


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
FEED_URL['astro-ph'] = "http://arxiv.org/rss/astro-ph"
FEED_URL['astro-ph.CO'] = "http://arxiv.org/rss/astro-ph.CO"
FEED_URL['astro-ph.EP'] = "http://arxiv.org/rss/astro-ph.EP"
FEED_URL['astro-ph.GA'] = "http://arxiv.org/rss/astro-ph.GA"
FEED_URL['astro-ph.HE'] = "http://arxiv.org/rss/astro-ph.HE"
FEED_URL['astro-ph.IM'] = "http://arxiv.org/rss/astro-ph.IM"
FEED_URL['astro-ph.SR'] = "http://arxiv.org/rss/astro-ph.SR"


class FeedCleaner(webapp2.RequestHandler):

    def get(self, feed):

        if feed not in FEED_URL:
            self.response.write(template.render('templates/404.html', {'feed':feed}))
            return

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
