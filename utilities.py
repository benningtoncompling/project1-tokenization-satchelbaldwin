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

def condition_d(word):
    if word[-1] == word[-2]:
        return (True, word[-1])
    else:
        return (False, '')

def condition_o(word):
    if len(word) < 3:
        return False
    s = word[-3:]
    if consonant(s[0]) and not consonant(s[1]) and consonant(s[2]):
        if s[2] != 'w' and s[2] != 'x' and s[2] != 'y':
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
    (word, changed) = r_suffix(word, "eed", "ee") if m > 0 else (word, False)
    if changed:
        return word
    if (
            (condition_v(word, 'ed') or condition_v(word, 'ing')) 
            and (word.endswith("ed") or word.endswith("ing"))
        ):
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
        new_word = r_suffix_d(word, d)
        if (word == new_word):
            (r, v) = condition_d(word)
            if r and not (v == 'l' or v =='s' or v == 'z'):
                word = word[:-1]
            elif m == 1 and condition_o(word):
                word = word + 'e'
    return word

def step_1c(word):
    if condition_v(word, 'i') and word.endswith('y'):
        (word, changed) = r_suffix(word, 'y', 'i')
    return word

def step_2(word):
    m = measure(word)
    d = {
            "ational": "ate",
            "tional": "tion",
            "enci": "ence",
            "anci": "ance",
            "izer": "ize",
            "abli": "able",
            "alli": "al",
            "entli": "ent",
            "eli": "e",
            "ousli": "ous",
            "ization": "ize",
            "ation": "ate",
            "ator": "ate",
            "alism": "al",
            "iveness": "ive",
            "fulness": "ful",
            "ousness": "ous",
            "aliti": "al",
            "iviti": "ive",
            "biliti": "ble"
        }
    if m > 0:
        word = r_suffix_d(word, d)
    return word

def step_3(word):
    m = measure(word)
    d = {
            "icate": "ic",
            "ative": "",
            "alize": "al",
            "iciti": "ic",
            "ical": "ic",
            "ful": "",
            "ness": ""
        }
    if m > 0:
        word = r_suffix_d(word, d)
    return word

def step_4(word):
    m = measure(word)
    def r_suffix_blank(word, l):
        d = {}
        for s in l:
            d[s] = ''
        return r_suffix_d(word, d)
    l = ["al", "ance", "ence", "er", "ic", "able", "ible", "ant", "ement", 
            "ment", "ent", "ou", "ism", "ate", "iti", "ous", "ive", "ize"]
    if m > 1:
        if word.endswith("tion") or word.endswith("sion"):
            (word, changed) = r_suffix(word, 'tion', '')
            (word, changed) = r_suffix(word, 'sion', '')
            return word
        word = r_suffix_blank(word, l)
    return word

def step_5a(word):
    m = measure(word)
    if m > 1:
        (word, changed) = r_suffix(word, "e", "")
    if m == 0 and not condition_o(word):
        (word, changed) = r_suffix(word, "e", "")
    return word

def step_5b(word):
    m = measure(word)
    if m > 1 and condition_d(word) and word.endswith("l"):
        (word, changed) = r_suffix(word, "ll", "l")
    return word

def porter_stemmer(w):
    words = []
    for word in w:
        word = word.lower()
        if word[-1] != '-' and len(word) > 1:
            w1a = step_1a(word)
            w1b = step_1b(w1a)
            w1c = step_1c(w1b)
            w2 = step_2(w1c)
            w3 = step_3(w2)
            w4 = step_4(w3)
            w5a = step_5a(w4)
            w5b = step_5b(w5a)
            words.append(w5b)
    return words

