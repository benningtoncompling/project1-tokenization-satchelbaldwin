#!/usr/bin/env python3

# satchel baldwin
# 3-8-2019
# worked with five and kelsey

import sys, re
from utilities import *

(infile, outfile) = get_files()
text = clean_text(infile.read())
words = get_words(text)
output = sort_and_count_words(count_words(words))
outfile.write(output)

infile.close()
outfile.close()
