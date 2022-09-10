# Author: Simon Bross
# Date: August 23, 2022
# Python 3.9
# Windows 11

from metrics import levenshtein, lsc_distance
# results for levenshtein from https://planetcalc.com/1721/


class TestMetrics:

    def test_equality_levenshtein(self):
        assert levenshtein("hallo", "hallo") == 0

    def test_equality_lsc(self):
        assert lsc_distance("hallo", "hallo") == 0

    def test_missing_word_levenshtein(self):
        assert levenshtein("", "hallo") == 5

    def test_missing_word_lsc(self):
        assert lsc_distance("", "hallo") == 5

    def test_missing_words_levenshtein(self):
        assert levenshtein("", "") == 0

    def test_missing_words_lsc(self):
        assert lsc_distance("", "") == 0

    def test_case_levenshtein(self):
        assert levenshtein("Test", "test") == 1

    def test_case_lsc(self):
        # only insertion and deletion allowed
        assert lsc_distance("Test", "test") == 2

    def test_reversed_levenshtein(self):
        assert levenshtein("Hallo", "ollaH") == 4

    def test_reversed_lsc(self):
        # 'ollaH' delete o,a,H (3) -> 'll' (longest subsequence)
        # insert H, a before 'll' and 'o' after (3) --> 6
        assert lsc_distance("Hallo", "ollah") == 6

    def test_spelling_mistake_levenshtein(self):
        assert levenshtein("absantse", "absence") == 3

    def test_spelling_mistake_lsc(self):
        # delete 'a', 't', 's" --> absne (3)
        # insert 'e', 'c' --> (5)
        assert lsc_distance("absantse", "absence") == 5

    def test_word_family_levenshtein(self):
        assert levenshtein("unfamiliar", "familiarization") == 9

    def test_word_family_lsc(self):
        assert lsc_distance("unfamiliar", "familiarization") == 9

    def test_mixed_levenshtein(self):
        assert levenshtein("paper", "scissors") == 7

    def test_mixed_lsc(self):
        # delete all but 'r' in paper --> (4)
        # insert s,c,i,s,s, o,s --> (11)
        assert lsc_distance("paper", "scissors") == 11
