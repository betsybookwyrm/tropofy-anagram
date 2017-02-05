# Anagram solver

This is an anagram solving app using Tropofy. Code is heavily based on the Tropofy example apps.

## Dictionaries

This anagram app requires a dictionary of valid words to find anagrams from.

The included dictionary is the SOWPODS list from https://www.wordgamedictionary.com/sowpods/ . This is a Scrabble 
dictionary, not a full English word list.

Dictionaries may take a couple of minutes to load initially, as there is some pre-processing done.

Other dictionary files may be substituted, but note that current functionality can't handle hyphens, apostrophes, or 
other word-internal punctuation. Dictionary substitution currently requires code changes.

## For future

### Improvement

Make dictionary loading properly Tropofyable for ease of loading other dictionaries. The easiest solution is to 
convert the dictionary itself to CSV, but that might require changing how the DictionaryWord object pre-processes each 
word. It depends on exactly how the Tropofy CSV loading works.

### Expansion

Features for word games:
* Include Scrabble scoring calculator

Use WordNet instead of dictionary files, this doesn't follow the data processing nature of Tropofy as much, but allows 
for the possibility of:
* Multi-lingual anagram solving
* Restricting to certain parts of speech (e.g. nouns only)
* Expanding from single-word anagrams to phrases and sentences (filtering for grammatically plausible answers) - this 
requires considerable additional complexity but would be *awesome*
