__AUTHOR__ = 'Petter Reinholdtsen <pere@hungry.com>'

import json
import lxml.html
import re
import time
import urllib
import urllib2
import urlparse

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
        out.write("\n")

def test_imdb_lookup():
    # This one return several entries
    print imdb_find_one("What Becomes of the Children?",1936)

def imdb_find_one(title, year, feature_only=False):

    """
Look up title and year in IMDB, and return the IMDB title ID if only
one title was found in the search result.
"""
    if not year:
        return None
    url = "http://www.imdb.com/find?ref_=nv_sr_fn&q=%s+%d&s=all" % \
          (urllib.quote_plus(title), year)
    if feature_only:
        url += "&ttype=ft"
    #print(url)
    try:
        root = lxml.html.fromstring(http_get_read(url))
    except urllib2.HTTPError as e:
        return None
    res = []
    for a in root.cssselect("td.primary_photo a[href]"):
        info = {}
        movie = a.getparent().getparent()
        info['imdb'] = urlparse.urljoin(url, a.attrib['href']).split("?")[0]
        info['title'] = movie.cssselect("td.result_text a[href]")[0].text_content()

        m = re.search("\((\d{4})\)", movie.text_content())
        if m:
            info['year'] = int(m.group(1))
        else:
            # Drop IMDB entries without year
            continue

        #print info['imdb'], info['year'], info['title']
        # Verify the years are the same +-2.  Not verifying title, as the
        # shown title might not be in the same language as the search
        # term.
        if int(year)-2 <= info['year'] \
           and info['year'] <= int(year)+2:
            res.append(info)
        else:
            print("warning: Ignoring %s (%s) for %s (%d)" % (info['imdb'],
                                                             info['year'],
                                                             title, year))
    #print(len(res))
    if 1 == len(res):
        return res[0]['imdb']
    else:
        return None

def test_wikipedia_lookup():
    for line in [
            '* {{IMDb title|0005339|A Fool There Was}}',
            '*{{IMDb title|id=0013704|title=The Trap}}',
            '*{{IMDb title|id=0036697|title=Captain America}}',
            '* {{IMDb title|id=0052646}}',
            '* {{IMDb title|id =0175627|title =La fuga degli amanti  }}'
    ]:
        m = re.search("\* ?{{ *IMDb title *\| *(id *=)?(tt)?(\d+) *(\|?.+}})?",
                      line, re.IGNORECASE)
        if m is not None:
            imdburl = 'http://www.imdb.com/title/tt%s/' % m.group(3)
            print(imdburl)
        else:
            print("Error %s" % line)
    urls = [
        "https://en.wikipedia.org/wiki/D.O.A._%281950_film%29",
        "https://en.wikipedia.org/wiki/Lonely_Wives_%28film%29",
        "https://en.wikipedia.org/wiki/The_Brain_that_Wouldn%27t_Die",
    ]
    for url in urls:
        print(wikipedia_lookup(url))

def imdb_url_clean(url):
    url = url.replace('/us.imdb.com/', '/www.imdb.com/')
    url = url.split('?')[0]
    url = url.split('#')[0]
    return url

def wikipedia_lookup(wpurl):
    m = re.search('^(https?://[^/]+)/wiki/(.+)', wpurl, re.IGNORECASE)
    #print m.group(1)
    if -1 != m.group(1).find('wikipedia.org'):
        url = "%s/w/index.php?title=%s&action=raw" % (m.group(1),m.group(2))
    else:
        url = wpurl + '?action=raw'
    #print(url)
    text = http_get_read(url)
    info = {}
    for line in text.split("\n"):
        #print line
        m = re.search('#REDIRECT \[\[(.+)\]\]', line)
        if m:
            #print m.group(1)
            newurl = urlparse.urljoin(wpurl, m.group(1).replace(" ", "_"))
            return wikipedia_lookup(newurl)
        if -1 != line.lower().find('{{imdb title'):
            m = re.search("\* ?{{ *IMDb title *\| *(id *=)?(tt)?(\d+) *(\|?.+}})?",
                          line, re.IGNORECASE)
            if m:
                # Normalize URLs to 7 digit numbers, as some wikipedia
                # pages have more or less digits.
                imdburl = 'http://www.imdb.com/title/tt%07d/' % int(m.group(3))
                info['imdb'] = imdburl
            else:
                print("info: '%s' ignored in %s" % (line, wpurl))
        # Used on wiki.creativecommons.org
        m = re.search("^ *\| *imdburl *= *(.+)", line, re.IGNORECASE)
        if m:
            info['imdb'] = imdb_url_clean(m.group(1))
        m = re.search("^ *\| *name *= *(.+)", line, re.IGNORECASE)
        if m:
            info['title'] = m.group(1)
        m = re.search("^ *\| *(released|releasedate) *= *.*(\d{4}).*", line,
                      re.IGNORECASE)
        if m:
            info['year'] = m.group(2)
    return info

if __name__ == '__main__':
    test_imdb_lookup()
    #test_wikipedia_lookup()
