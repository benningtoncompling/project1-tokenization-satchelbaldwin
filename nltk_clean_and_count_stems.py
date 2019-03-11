#!/usr/bin/env python3

# satchel baldwin
# 3-8-2019

import sys, re
import nltk
from nltk import word_tokenize
from nltk.stem import *
from utilities import *

(infile, outfile) = get_files()
text = clean_text(infile.read())

# additional cleaning for nltk -- instead of using regex to pull valid words
# from the xml, clean out tags and let the nltk tokenizer do the work
symbols = r'(ref|\&|\;|\"|\:|\/\/|\/|\#|\!|\=\=|\=|\{\{|\}\}|\[|\]|\(|\)|\||\{|\}|\*|\-|\')'
cleaned = re.sub(symbols, ' ', text)

stemmer = PorterStemmer()
tokens = word_tokenize(cleaned)
stems = [stemmer.stem(w) for w in tokens]

output = sort_and_count_words(count_words(stems))
outfile.write(output)

infile.close()
outfile.close()
