__AUTHOR__ = 'Petter Reinholdtsen <pere@hungry.com>'

import re
import time
import urllib2

def http_get_read(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', 'public-domain-movie-locator/0.0')]
    # Try several times in case the first one fail
    for tries in xrange(0,3):
        try:
            f = opener.open(url)
            return f.read()
        except:
            print("Retrying %s in 20 seconds" % url)
            time.sleep(20)

def wikipedia_lookup(wpurl):
    m = re.search('^(.*wikipedia.org)/wiki/(.+)', wpurl, re.IGNORECASE)
    url = "%s/w/index.php?title=%s&action=raw" % (m.group(1),m.group(2))
    #print(url)
    text = http_get_read(url)
    for line in text.split("\n"):
        #print line
        if -1 != line.lower().find('{{imdb title'):
            m = re.search("\* ?{{IMDb title *\| *(id=)?(tt)?(\d+) *(\|?.+}})?",
                          line, re.IGNORECASE)
            if m:
                # Normalize URLs to 7 digit numbers, as some wikipedia
                # pages have more or less digits.
                imdburl = 'http://www.imdb.com/title/tt%07d/' % int(m.group(3))
                return imdburl
            else:
                print("info: '%s' ignored in %s" % (line, wpurl))
    return None

