import sys, re

def get_files():
    if len(sys.argv) != 3:
        print("usage: ./clean_and_count_tokens.py <infile> <outfile>")
        exit()
    infile_name = sys.argv[1]
    outfile_name = sys.argv[2]
    infile = open(infile_name, 'r')
    outfile = open(outfile_name, 'w')
    return (infile, outfile)

def clean_text(text):
    # remove text by regex
    def remove(pattern, text, spaces = True):
        return re.sub(pattern, ' ' if spaces else '', text)
    # attempts to match '< {anything} >'
    tags = r'<\/?(\w|\s|\=|\"|\'|\-|\:|\.|\/)*\/?>'
    text = remove(tags, text)
    # &gt; and &lt; are > and <, not a word. 
    html_escapes = r'\b(gt|lt)\b'
    text = remove(html_escapes, text) 
    # no spaces so [[word | plural]]s work
    double_brackets = r'(\[\[|\]\])'
    text = remove(double_brackets, text, False)
    return text

# matches words fairly well
# NOTE: catches ones that end in -
def get_words(text):
    words_match = r'\b[a-zA-Z](?:[a-zA-Z]|\'|\.)*[a-zA-Z]?\b'
    return(re.findall(words_match, text))

def count_words(words):
    count = {}
    for w in words:
        if len(w) != 0:
            w = w.lower()
            if w[-1] != '-':
                if w in count:
                    count[w] = count[w] + 1
                else:
                    count[w] = 1
    return count

def sort_and_count_words(count):
    items = [item for item in count.items()]
    items.sort(key = lambda x: x[1])
    items.reverse()
    numbers = []
    output = ""
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
            output = output + "{}\t{}\n".format(words[i], n)
    return(output)

# porter stemmer

vowels = ['a', 'e', 'i', 'o', 'u']
consonant = lambda c: (c not in vowels)
yv = lambda w, y_index: (consonant(w[y_index - 1]))

def measure(word):
    word = word.lower()
    c = 0
    i = 0
    state = "c"
    for letter in word:
        if letter != "y":
            if not consonant(letter) and state == "c":
                c = c + 1 
                state = "v"
            if consonant(letter) and state == "v":
                state = "c"
        else:
            if i != 0:
                if yv(word, i) and state == "c": 
                    c = c + 1
                    state = "v"
                if not yv(word, i) and state == "v":
                    state = "c"
        i = i + 1
    if state == "v":
        c = c - 1
    return c

def r_suffix(word, suffix, replacement):
    matched = word.endswith(suffix)
    return (word[:-len(suffix)] + replacement if matched else word, matched)

def r_suffix_d(word, d):
    for k in sorted(d, key=len, reverse = True):
        (word, changed) = r_suffix(word, k, d[k])
        if changed:
            break
    return word

def condition_v(word, suffix):
    possible_stem = word[:-len(suffix)]
    for letter in possible_stem:
        if letter in vowels:
            return True
    return False

def step_1a(word):
    d = {
            "sses": "ss"
        ,   "ies" : "i" 
        ,   "ss"  : "ss"
        ,   "s"   : ""
        }
    word = r_suffix_d(word, d)
    return word
def step_1b(word):
    m = measure(word)
    (word, m) = r_suffix(word, "eed", "ee") if m > 0 else word
    if m:
        break
    if (condition_v(word) and (word.endswith("ed") or word.endswith("ing"))):
        d = {
                "ed" : ""
            ,   "ing": ""
            }
        word = r_suffix_d(word, d)
        d = {
                "at": "ate"
            ,   "bl": "ble"
            ,   "iz": "ize"
            }



def step_1c(word):
    pass
def step_2(word):
    pass
def step_3(word):
    pass
def step_4(word):
    pass
def step_5a(word):
    pass
def step_5b(word):
    pass

def porter_stemmer(w):
    words = []
    for word in w:
        word = word.lower()
        if w[-1] != '-':
            words.append(word)
    # stemming steps
    
