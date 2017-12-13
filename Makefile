all: stats

stats:
	./list-stats free-movies-*.json

listupdate:
	./mklist-archive-org-wikidata
	./mklist-archive-org-search
	./mklist-publicdomaintorrents
	./mklist-vodo
	./mklist-imdb-pd
	./mklist-imdb-pd --dubious-list --output free-movies-imdb-dubious.json
	./mklist-icheckmovies-archive-mochard
	./mklist-publicdomainmovies-net
	./mklist-publicdomainreview
	./mklist-letterboxd-pd
	./mklist-letterboxd-pd --baseurl=https://letterboxd.com/loureviews/list/internet-archive-silent-films --output=free-movies-letterboxd-silent.json
	./mklist-letterboxd-pd --baseurl=https://letterboxd.com/robot2xl/list/looney-tunes-in-the-public-domain/ --output=free-movies-letterboxd-looney-tunes.json
	./mklist-thehillproductions
	./mklist-creative-commons
	./mklist-imdb-c-expired-year --country=us --output=free-movies-imdb-c-expired-us.json
	./mklist-imdb-c-expired-year --country=gb --output=free-movies-imdb-c-expired-gb.json --end=1912

histogram-year.data: histogram-year *.json
	./histogram-year free-movies-*.json > $@
histogram-year.png: histogram-year.data
	./histogram-year-plot

complete-imdb-list.csv: json2csv free-movies-*.json
	./json2csv free-movies-*.json |sort> $@
