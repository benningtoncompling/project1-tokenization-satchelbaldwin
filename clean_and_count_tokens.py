#!/usr/bin/env python3

# satchel baldwin
# 3-8-2019
# worked with five and kelsey

import sys, re

if len(sys.argv) != 3:
    print("usage: ./clean_and_count_tokens.py <infile> <outfile>")
    exit()

infile_name = sys.argv[1]
outfile_name = sys.argv[2]

infile = open(infile_name, 'r')
outfile = open(outfile_name, 'w')

xml = infile.read()

# attempts to match '< {anything} >'
tag_match = r'<\/?(\w|\s|\=|\"|\'|\-|\:|\.|\/)*\/?>'
no_tags = re.sub(tag_match, ' ', xml) 

# &gt; and &lt; are > and <, not a word. 
no_html_escapes = r'\b(gt|lt)\b'
no_html = re.sub(no_html_escapes, ' ', no_tags) 

# no spaces so [[word | plural]]s work
no_double_brackets = r'(\[\[|\]\])'
no_brackets = re.sub(no_double_brackets, '', no_html)

# matches words well, except catches ones that end in -
# however this gets filtered out an easier way than changing the regex below
words_match = r'\b[a-zA-Z](?:[a-zA-Z]|\'|\.)*[a-zA-Z]?\b'
words = re.findall(words_match, no_brackets)

count = {}
for w in words:
    if len(w) != 0:
        w = w.lower()
        # aformentioned fix
        if w[-1] != '-':
            if w in count:
                count[w] = count[w] + 1
            else:
                count[w] = 1

# sort 1..x then flip for highest...lowest
items = [item for item in count.items()]
items.sort(key = lambda x: x[1])
items.reverse()

# take all output numbers, alphabetize each one and write
numbers = []
for i in items:
    if not i[1] in numbers:
        numbers.append(i[1])

for n in numbers:
    words = []
    for i in items:
        if i[1] == n:
            words.append(i[0])
    words.sort()
    for i in range(0, len(words)):
        outfile.write("{}\t{}\n".format(words[i], n))

infile.close()
outfile.close()
