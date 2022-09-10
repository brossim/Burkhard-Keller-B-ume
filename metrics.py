# Author: Simon Bross
# Date: August 15, 2022
# Python 3.9
# Windows 11


import numpy as np
from numba import njit


class MetricError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


# use njit decorator to speed up the functions
# increases the speed considerably for large word lists

@njit(fastmath=True)
def levenshtein(word1, word2):
    """
    Computes the levenshtein distance between two words. The distance reflects
    the total number of single-character edits required to transform one word
    into the other. Each edit has a cost of 1.
    @param word1: First word to be compared as str.
    @param word2: Second word to be compared as str.
    @return: Levenshtein distance as integer.
    """
    n = len(word1)
    m = len(word2)

    # cover two basic cases
    if n < m:
        return levenshtein(word2, word1)
    if m == 0:
        return n

    # create distance matrix
    dist_mtrx = np.zeros((n+1, m+1))

    dist_mtrx[0] = np.arange(m+1)
    dist_mtrx[:, 0] = np.arange(n+1)

    # Recurrence
    for p in np.nditer(np.arange(1, n+1)):
        for q in np.nditer(np.arange(1, m+1)):
            dist_mtrx[p, q] = min(dist_mtrx[p-1, q] + 1,
                                  dist_mtrx[p-1, q-1] +
                                  (1 if word1[p-1] != word2[q-1] else 0),
                                  dist_mtrx[p, q-1] + 1)

    return int(dist_mtrx[n, m])


@njit(fastmath=True)
def lsc_distance(word1, word2):
    """
    Computes the edit distance based on the longest common subsequence.
    Only two operations (insertion and deletion) are allowed.
    @param word1: First word to be compared as str.
    @param word2: Second word to be compared as str.
    @return: LSC distance as int.
    """
    m = len(word1)
    n = len(word2)

    dist_mtrx = np.zeros((m+1, n+1))
    # for i and k, start with 1, D[0][0] is already 0
    for i in np.nditer(np.arange(1, m+1)):
        for k in np.nditer(np.arange(1, n+1)):
            if word1[i-1] == word2[k-1]:
                dist_mtrx[i][k] = dist_mtrx[i-1][k-1] + 1
            else:
                dist_mtrx[i][k] = max(dist_mtrx[i-1][k], dist_mtrx[i][k-1])

    lcs = int(dist_mtrx[m][n])
    return (m-lcs) + (n-lcs)


# get a dict of function name: func (callable) for all available metrics
# allowing the implementation of further metrics without changing any code
# (validity check for metric) in the BkTree class
all_metrics = {
    levenshtein.__name__: levenshtein,
    lsc_distance.__name__: lsc_distance
}
