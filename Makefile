all: stats

stats:
	for f in free-movies-*.json; do python list-stats --input $$f; done

listupdate:
	./mklist-wikidata-archive-org
	./mklist-publicdomaintorrents
	./mklist-vodo
	./mklist-imdb-pd
	./mklist-archive-org-butter
	./mklist-icheckmovies-archive-mochard

# See http://countwordsworth.com/blog/dale-chall-easy-word-list-text-file/
DaleChallEasyWordList.txt:
	curl -q -o $@ http://countwordsworth.com/download/DaleChallEasyWordList.txt

histogram-year.data: histogram-year *.json
	./histogram-year > $@
histogram-year.png: histogram-year.data
	./histogram-year-plot
