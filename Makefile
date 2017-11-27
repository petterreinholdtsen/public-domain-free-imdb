all: stats

stats:
	./list-stats free-movies-*.json

listupdate:
	./mklist-wikidata-archive-org
	./mklist-publicdomaintorrents
	./mklist-vodo
	./mklist-imdb-pd
	./mklist-imdb-pd --dubious-list --output free-movies-imdb-dubious.json
	./mklist-archive-org-butter
	./mklist-icheckmovies-archive-mochard
	./mklist-publicdomainmovies-net
	./mklist-publicdomainreview
	./mklist-letterboxd-pd
	./mklist-letterboxd-pd --baseurl=https://letterboxd.com/loureviews/list/internet-archive-silent-films --output=free-movies-letterboxd-silent.json
	./mklist-letterboxd-pd --baseurl=https://letterboxd.com/robot2xl/list/looney-tunes-in-the-public-domain/ --output=free-movies-letterboxd-looney-tunes.json

# See http://countwordsworth.com/blog/dale-chall-easy-word-list-text-file/
DaleChallEasyWordList.txt:
	curl -q -o $@ http://countwordsworth.com/download/DaleChallEasyWordList.txt

histogram-year.data: histogram-year *.json
	./histogram-year free-movies-*.json > $@
histogram-year.png: histogram-year.data
	./histogram-year-plot

complete-imdb-list.csv: json2csv free-movies-*.json
	./json2csv free-movies-*.json |sort> $@
