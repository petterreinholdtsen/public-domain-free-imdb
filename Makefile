all:

listupdate:
	./mklist-wikidata-archive-org
	./mklist-publicdomaintorrents
	./mklist-vodo
	./mklist-imdb-pd
	./mklist-archive-org-butter

# See http://countwordsworth.com/blog/dale-chall-easy-word-list-text-file/
DaleChallEasyWordList.txt:
	curl -q -o $@ http://countwordsworth.com/download/DaleChallEasyWordList.txt
