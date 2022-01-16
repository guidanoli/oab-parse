PDF=oab.pdf
TXT=oab.txt
DB=oab.db

PYTHON=python3
CAT=cat
TR=tr
SED=sed
GREP=grep

default: $(DB)

$(TXT): $(PDF)
	# convert PDF to text
	$(PYTHON) pdf2text.py $(PDF) tmp1
	# remove newlines
	$(CAT) tmp1 | $(TR) -d '\n' > tmp2
	# remove page numbers
	$(CAT) tmp2 | $(SED) 's/[0-9][0-9]*   *//g' > tmp1
	# reinsert important newlines
	$(CAT) tmp1 | $(SED) 's/   */\n/g' > tmp2
	# keep interesting lines only
	$(CAT) tmp2 | $(GREP) -E '^[0-9]+\.([0-9]+\.)?' > tmp1
	# skip line for x.1
	$(CAT) tmp1 | $(SED) -E 's/ ([0-9]+\.1)/\n\1/g' > tmp2
	# keep interesting lines only
	$(CAT) tmp2 | $(GREP) -E '^[0-9]+\.( [^a-z]*$$|[0-9]+)' > $(TXT)
	# clean temporary files
	$(RM) tmp1 tmp2

$(DB): $(TXT)
	# parse file and create database
	$(PYTHON) parse.py $(TXT)

.PHONY: default
