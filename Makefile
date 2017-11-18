all: stats

stats:
	./list-stats free-movies-*.json

listupdate:
	./mklist-wikidata-archive-org
	./mklist-publicdomaintorrents
	./mklist-vodo
	./mklist-imdb-pd
	./mklist-archive-org-butter
	./mklist-icheckmovies-archive-mochard
	./mklist-publicdomainmovies
	./mklist-publicdomainreview

# See http://countwordsworth.com/blog/dale-chall-easy-word-list-text-file/
DaleChallEasyWordList.txt:
	curl -q -o $@ http://countwordsworth.com/download/DaleChallEasyWordList.txt

histogram-year.data: histogram-year *.json
	./histogram-year free-movies-*.json > $@
histogram-year.png: histogram-year.data
	./histogram-year-plot
