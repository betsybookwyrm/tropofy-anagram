"""
Anagram solving app for Tropofy, heavily based on Tropofy example apps
"""

import pkg_resources

from tropofy.app import AppWithDataSets, StepGroup, Step, Parameter
from tropofy.database.tropofy_orm import DataSetMixin
from tropofy.widgets import ParameterForm, ExecuteFunction, SimpleGrid

from sqlalchemy.schema import Column
from sqlalchemy.types import Text


def hash_word(word):
    """
    Creates a hash of a word by converting it to lowercase and sorting the letters alphabetically

    :param word: The word to be hashed
    :type word: str
    :return: A hash of a word
    :rtype: str
    """
    return ''.join(sorted(word.lower()))


def validate_word(word):
    """
    Ensure the word given to find anagrams for is a single word with no punctuation.

    :param word: The input word
    :type word: str
    :return: True if word is valid
    :rtype: bool
    """
    if word is not None and len(word) > 0:
        return word.isalpha()
    return False


class DictionaryWord(DataSetMixin):
    word = Column(Text, nullable=False)
    sorted = Column(Text, nullable=False)

    def __init__(self, word=None, sorted=None):
        """
        The sorted parameter is ignored - it's only here to make entering data through SimpleGrid work. The column
        should always be hidden.
        """
        self.word = word
        self.sorted = hash_word(word)

    def __str__(self):
        return '<DictionaryWord {} (letters: {})>'.format(self.word, self.sorted)


class SolutionWord(DataSetMixin):
    word = Column(Text, nullable=False)


class ExecuteSolverFunction(ExecuteFunction):

    def get_button_text(self, app_session):
        return "Solve Anagrams"

    def execute_function(self, app_session):
        find_anagrams(app_session)


class AnagramApp(AppWithDataSets):

    def get_name(self):
        return 'Anagram Solver'

    def get_examples(self):
        return {"SOWPODS Scrabble dictionary": load_sowpods}

    def get_gui(self):
        # Dictionaries are not generally editable, but here it is just in case
        step_group1 = StepGroup(name='View your dictionary')
        step_group1.add_step(Step(
            name='Dictionary of available words',
            widgets=[SimpleGrid(DictionaryWord, hidden_column_names=['sorted'])],
            help_text="View and edit all possible potential anagram words"
        ))

        step_group2 = StepGroup(name='Pick a word')
        step_group2.add_step(Step(
            name='Word to rearrange',
            widgets=[{"widget": ParameterForm(), "cols": 6}],
        ))

        step_group3 = StepGroup(name='Solve')
        step_group3.add_step(
            Step(name='Solve Anagrams', widgets=[ExecuteSolverFunction()]))

        step_group4 = StepGroup(name='View the Solutions')
        step_group4.add_step(Step(
            name='View Anagrams',
            widgets=[
                {"widget": SimpleGrid(SolutionWord), "cols": 6}
            ],
            help_text="These words are all anagrams of your original word (excluding your original word itself)."
        ))

        return [step_group1, step_group2, step_group3, step_group4]

    def get_parameters(self):
        return [Parameter(name='original_word', label='Original word', default='live', allowed_type=str,
                          validator=validate_word)]


def find_anagrams(app_session):
    """
    Find and store all anagrams of the original word

    This process is slightly awkwardly stretched out to fit the Tropofy app pattern, as an excercise in Tropofy rather
    than an exercise in finding anagrams.
    """
    # Clear previous solutions
    app_session.data_set.query(SolutionWord).delete()

    # What do we have here today
    dictionary_size = app_session.data_set.query(DictionaryWord).count()
    app_session.task_manager.send_progress_message('There are {} words in your dictionary'.format(dictionary_size))

    original_word = app_session.data_set.get_param('original_word')
    app_session.task_manager.send_progress_message('Finding anagrams for {}'.format(original_word))

    # Find anagrams
    anagrams = app_session.data_set.query(DictionaryWord)\
                                   .filter(DictionaryWord.sorted == hash_word(original_word))\
                                   .all()

    # Save solutions
    for word in anagrams:
        # Exclude original word if present in the list
        # All words are anagrams of themselves but we don't need the original word in the solutions.
        if word.word != original_word:
            app_session.data_set.add(SolutionWord(word=word.word))

    anagram_count = app_session.data_set.query(SolutionWord).count()
    app_session.task_manager.send_progress_message('{} anagrams found'.format(anagram_count))


def load_dictionary(app_session, file_path):
    """
    Load words from provided dictionary text file.

    Words are expected to be one per line.

    Omits words that are not valid by anagram app definition

    :param file_path: Full location & name of dictionary file
    :type file_path: str
    """
    with open(file_path, 'r') as dictionary:
        for word in dictionary.readlines():
            clean_word = word.strip()
            if validate_word(clean_word):
                app_session.data_set.add(DictionaryWord(word=clean_word))


def load_sowpods(app_session):
    load_dictionary(app_session, pkg_resources.resource_filename('anagram', 'sowpods.txt'))
