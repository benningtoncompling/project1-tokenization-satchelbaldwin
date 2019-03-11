#!/usr/bin/env python3

# satchel baldwin
# 3-8-2019

import sys, re
from utilities import *

(infile, outfile) = get_files()
text = clean_text(infile.read())
words = get_words(text)
stems = porter_stemmer(words)
output = sort_and_count_words(count_words(stems))
outfile.write(output)

infile.close()
outfile.close()
