all: stats

stats:
	./list-stats free-movies-*.json

listupdate:
	./mklist-archive-org-wikidata
	./mklist-archive-org-search
	./mklist-publicdomaintorrents
	./mklist-vodo
	./mklist-imdb-pd
	./mklist-icheckmovies-archive-mochard
	./mklist-publicdomainmovies-net --imdblookup
	./mklist-publicdomainreview --imdblookup
	./mklist-publicdomainmovies-info
	./mklist-letterboxd-pd
	./mklist-letterboxd-pd --baseurl=https://letterboxd.com/loureviews/list/internet-archive-silent-films --output=free-movies-letterboxd-silent.json
	./mklist-letterboxd-pd --baseurl=https://letterboxd.com/robot2xl/list/looney-tunes-in-the-public-domain/ --output=free-movies-letterboxd-looney-tunes.json
	./mklist-thehillproductions
	./mklist-creative-commons
	./mklist-imdb-c-expired-year --country=us --output=free-movies-imdb-c-expired-us.json
	./mklist-imdb-c-expired-year --country=gb --output=free-movies-imdb-c-expired-gb.json --end=1912
	./mklist-retrofilmvault --imdblookup
	./mklist-openflix --imdblookup
	./mklist-horrortheque-com
	./mklist-filmchest-com --imdblookup
	./mklist-infodigi-pd --imdblookup
	./mklist-fesfilm --imdblookup
	./mklist-fesfilm-xls
	./mklist-profilms-pd --imdblookup
	./mklist-cinemovies --imdblookup
	./mklist-two-movies-net --imdblookup
	./mklist-mubi --imdblookup

free-complete.json: title.basics.tsv.gz free-movies-*.json
	./list-stats --create-complete free-movies-*.json

histogram-year.data: histogram-year *.json
	./histogram-year free-movies-*.json > $@
histogram-year.png: histogram-year-plot histogram-year.data
	./histogram-year-plot

complete-imdb-list.csv: json2csv free-movies-*.json
	./json2csv free-movies-*.json |sort> $@

# This step require ~100 MiB on disk
title.basics.tsv.gz:
	curl --silent https://datasets.imdbws.com/title.basics.tsv.gz > $@.new && mv $@.new $@
histogram-title.basics.csv: title.basics.tsv.gz
	gunzip < title.basics.tsv.gz | awk --field-separator "\t" \
          '("short" == $$2 || "movie" == $$2) && 2019 > $$6  { hist[$$6]++} END { for (y in hist) print y, hist[y] }' \
        > $@.new && mv $@.new $@
