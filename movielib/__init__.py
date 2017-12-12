__AUTHOR__ = 'Petter Reinholdtsen <pere@hungry.com>'

import json
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
            print("Retrying %s in 2 seconds" % url)
            time.sleep(2)
    # Fake exception to keep callers happy
    raise urllib2.HTTPError(url, None, "failure after 3 tries", {}, None)

def savelist(l, name = None):
    with open(name, 'wt') as out:
        json.dump(l,
                  out,
                  sort_keys=True,
                  indent=4,
                  separators=(',', ': '))

def test_wikipedia_lookup():
    for line in [
            '* {{IMDb title|0005339|A Fool There Was}}',
            '*{{IMDb title|id=0013704|title=The Trap}}',
            '*{{IMDb title|id=0036697|title=Captain America}}',
            '* {{IMDb title|id=0052646}}',
            '* {{IMDb title|id =0175627|title =La fuga degli amanti  }}'
    ]:
        m = re.search("\* ?{{IMDb title *\| *(id *=)?(tt)?(\d+) *(\|?.+}})?",
                      line, re.IGNORECASE)
        if m is not None:
            imdburl = 'http://www.imdb.com/title/tt%s/' % m.group(3)
            print imdburl
        else:
            print("Error %s" % line)

def wikipedia_lookup(wpurl):
    m = re.search('^(.*wikipedia.org)/wiki/(.+)', wpurl, re.IGNORECASE)
    url = "%s/w/index.php?title=%s&action=raw" % (m.group(1),m.group(2))
    #print(url)
    text = http_get_read(url)
    for line in text.split("\n"):
        #print line
        if -1 != line.lower().find('{{imdb title'):
            m = re.search("\* ?{{IMDb title *\| *(id *=)?(tt)?(\d+) *(\|?.+}})?",
                          line, re.IGNORECASE)
            if m:
                # Normalize URLs to 7 digit numbers, as some wikipedia
                # pages have more or less digits.
                imdburl = 'http://www.imdb.com/title/tt%07d/' % int(m.group(3))
                return imdburl
            else:
                print("info: '%s' ignored in %s" % (line, wpurl))
    return None

if __name__ == '__main__':
    test_wikipedia_lookup()
