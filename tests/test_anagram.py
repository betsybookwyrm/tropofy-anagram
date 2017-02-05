"""
Tests for basic functions to avoid having to run the whole thing just for this

Written for py.test
"""

from anagram.anagram import hash_word, validate_word


def test_word_hash():
    assert hash_word('Alphabetise') == 'aabeehilpst'
    assert hash_word('live') == hash_word('Evil')
    assert hash_word('TomMarvoloRiddle') == hash_word('IAmLordVoldemort')
    assert hash_word('one') != hash_word('two')


def test_validate_given_word():
    assert not validate_word('Too many words')
    assert validate_word('supercalifragilisticexpialidocious')
    assert not validate_word('can\'t')
    assert not validate_word('no-no')
    assert validate_word('Capitalised')
    assert not validate_word('')
    assert not validate_word(None)
