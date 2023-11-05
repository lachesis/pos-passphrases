import collections
import functools
import re
import secrets
import random
import json

VALID_POS_CODES = 'anrsv'

CODE_PHRASE = 'anvan'
NUM_PASSWORDS = 10
MAX_LEN = 8

def get_wordlist_iter(part_of_speech):
    from nltk.corpus import wordnet
    for synset in wordnet.all_synsets(pos=part_of_speech):  # 'n' denotes nouns
        for lemma in synset.lemmas():
            yield lemma.name()

def wordlists_unique(wordlists):
    word_ctr = collections.Counter()
    for code, wl in wordlists.items():
        for word in set(wl):
            word_ctr[word] += 1

    bad_words = set()
    for word, cnt in word_ctr.most_common():
        if cnt <= 1:
            break
        bad_words.add(word)
    del word_ctr

    return {
        code: [ w for w in wl if w not in bad_words ]
        for code, wl in wordlists.items()
    }

def get_password(wordlists, code_phrase):
    if any(x not in VALID_POS_CODES for x in code_phrase):
        raise ValueError("Invalid part of speech: use [anrsv]")

    return ''.join(
        secrets.choice(wordlists[pos_code]).capitalize()
        for pos_code in code_phrase
    )

def save_wordlists(wordlists):
    with open('wordlists.json', 'w') as out:
        json.dump({
            code: list(wl)
            for code, wl in wordlists.items()
        }, out, indent=0)

def load_wordlists():
    with open('wordlists.json', 'r') as inp:
        return json.load(inp)

def build_wordlists():
    # get the wordlists for all valid parts of speech
    wordlists = {
        pos: set(
            w
            for w in get_wordlist_iter(pos)
            if re.match('^[a-z]*$', w)
        )
        for pos in VALID_POS_CODES
    }

    # replace the wordlists with only words that are unique to their own part of speech
    wordlists = wordlists_unique(wordlists)

    return wordlists

def get_wordlists():
    try:
        return load_wordlists()
    except Exception:
        wordlists = build_wordlists()
        save_wordlists(wordlists)
        return wordlists

def main():
    # should be argparse
    code_phrase = CODE_PHRASE
    num_passwords = NUM_PASSWORDS
    max_len = MAX_LEN

    wordlists = get_wordlists()

    # filter to max length
    wordlists = {
        code: [w for w in wl if len(w) < max_len]
        for code, wl in wordlists.items()
    }

    for i in range(num_passwords):
        print(get_password(wordlists, code_phrase))

if __name__ == "__main__":
    main()
