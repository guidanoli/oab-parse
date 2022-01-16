#!/usr/bin/env bash

# constants
pdf=oab.pdf
txt=oab.txt

# convert pdf to text
python3 pdf2text.py "$pdf" "$txt"

# remove newlines
tmp=$(mktemp)
tr -d '\n' < "$txt" > "$tmp"
mv "$tmp" "$txt"

# remove page numbers
sed -i 's/[0-9][0-9]*   *//g' "$txt"

# reinsert important newlines
sed -i 's/   */\n/g' "$txt"

# keep interesting lines only
tmp=$(mktemp)
grep -E '^[0-9]+\.([0-9]+\.)?' "$txt" > "$tmp"
mv "$tmp" "$txt"

# skip line for x.1
sed -Ei 's/ ([0-9]+\.1)/\n\1/g' "$txt"

# keep interesting lines only
tmp=$(mktemp)
grep -E '^[0-9]+\.( [^a-z]*$|[0-9]+)' "$txt" > "$tmp"
mv "$tmp" "$txt"

# parse file and create database
python3 parse.py "$txt"
