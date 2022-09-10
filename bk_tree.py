# Author: Simon Bross
# Date: August 15, 2022
# Python 3.9
# Windows 11

import pickle
import random
import os
import networkx as nx
from networkx.drawing.nx_pydot import write_dot
from src.model.metrics.metrics import all_metrics, MetricError
from datetime import datetime


class SearchWordError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class SearchDistanceError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class ListIntegrityError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class BKTree:
    """
    Burkhard Keller Tree is a tree-based data structure that provides an
    efficient search method looking up words in a given string metric distance
    to a query word. It is mainly used for spell checking or providing
    word suggestions. In the tree, words are represented by labeled nodes
    that are linked to other words (child nodes) via distance-labeled edges.
    The distance between two words is computed using a string metric that
    has to satisfy the axioms of non-negativity, implication, symmetry,
    and triangle inequality (e.g. levenshtein distance).
    """

    def __init__(self, word_list, dist_func):
        """
        Instantiates a BKTree object from the provided word list and
        distance function.
        @param word_list: List of single words (str), i.e. one word per list
        element.
        @param dist_func: String of distance function used to compute the
        distance between two words. The string is searched for in the
        all_metrics dict (defined in metrics.py) that contains the function
        name (key) and callable function (value) of every metric.
        """
        assert isinstance(word_list, list), \
            "Attribute 'word_list' must be a list."
        # assure that every element in the word list is a single word/string
        # and raise error if not
        self.__check_list_integrity(word_list)
        # make sure that every word is unique
        self.__word_list = list(set(word_list))
        # check if dist_func is valid
        # all_metrics dict structure = function_name : function (callable)
        if dist_func not in all_metrics:
            raise MetricError(f"Invalid metric function. "
                              f"Available functions: "
                              f"{', '.join(all_metrics.keys())}.")
        # store attribute as a callable function
        self.__dist_func = all_metrics[dist_func]

        # get randon number to determine root word
        n = random.randint(0, self.num_of_words - 1)
        self.__root_word = self.__word_list[n]

        # recursive tuple representation (word-labeled node, child dict)
        # dict keys represent the levenshtein/lsc distance mapping
        # to other subtrees that in turn are recursive 2-tuples, too
        self.__tree = (self.__root_word, dict())

        # lay basis for graph/graphical visualization
        self.__graph = nx.DiGraph()

        # iterate over word list without root word (already in self.__tree)
        # to insert all words into the tree
        # add_word also adds the edges to the graph object
        # using the word-labeled nodes and distance-labelled edges
        # from the recursive tuple representation
        for word in [word for word in self.__word_list
                     if word != self.__root_word]:
            self.__add_word(self.__tree, word)

        # get tree depth using recursive traversal
        # node_depths stores the depth of every node
        # max of node_depths values is the max tree depth
        # start by adding the root_word with depth zero
        self.__node_depths = {self.__root_word: 0}
        self.__get_tree_depth(self.tree)
        self.__tree_depth = max(self.__node_depths.values())

        # save graph as .dot in output folder
        # create output folder if it is nonexistent
        if not os.path.isdir("src/model/output"):
            os.mkdir("src/model/output")

        # create unique filename for every tree
        date_suffix = datetime.now().strftime("%H:%M").replace(":", "_")
        file_name = f"{self.__root_word}_{self.__dist_func.__name__}_" \
                    f"{date_suffix}"

        write_dot(self.graph, f"src/model/output/{file_name}.dot")

        # save BKTree object as .pkl in output folder to recreate it for
        # interactive mode and graphical visualization
        self.__save_as_pkl(f"src/model/output/{file_name}.pkl")

    def __add_word(self, tree, word):
        """
        Recursively adds the words (= labeled node) and distances
        (= labeled edges) to the tuple representation of the BKTree.
        The distance between parent word and child word is computed
        using one of the metrics defined in metrics.py.
        The function for the metric is stored in the dist_func attribute.
        The labeled edges are added to the DiGraph object used to graphically
        visualize the tree (in view component).
        @param tree: Tuple representation of the BKTree.
        @param word: New word (labeled node) to be added to the BKTree, as str.
        """
        # compute the distance between parent word and child word
        parent_word = tree[0]
        distance = self.__dist_func(parent_word, word)
        # if the current node already has a child with distance d
        # recursively proceed with this child tree
        if distance in tree[1]:
            self.__add_word(tree[1][distance], word)
        else:
            tree[1][distance] = (word, dict())
            # build up graph here to save computation time
            # i.e. no second for loop/recursive function necessary
            # parent_word and word are recognized as nodes by networkx
            self.graph.add_edge(f"{parent_word}", f"{word}",
                                weight=distance)

    @property
    def root(self):
        """
        Returns the root word of the BKTree.
        @return: Root word as str.
        """
        return self.__root_word

    @property
    def graph(self):
        """
        Returns the DiGraph object of the tree that was built up
        using the tree's tuple representation.
        @return: DiGraph object of the tree.
        """
        return self.__graph

    @property
    def num_of_words(self):
        """
        Returns the number of words in the BKTree/word_list the tree
        was built up from.
        @return: Number of words as int.
        """
        return len(self.__word_list)

    @property
    def tree(self):
        """
        Returns the BKTree as a recursive tuple consisting of two elements:
        Root (labeled node) and the child dict containing the distance-labeled
        edges and child nodes.
        The child nodes are recursive tree tuples themselves.
        @return: Tuple representation of BKTree object.
        """
        return self.__tree

    @property
    def tree_depth(self):
        """
        Returns the maximum depth of the tree, i.e. the longest path found
        from the root to a leaf.
        @return: Maximum tree depth as int.
        """
        return self.__tree_depth

    def __get_tree_depth(self, tree):
        """
        Recursively traverse the tree and get the depth of every node
        to determine the maximum tree depth. Individual node depths are
        stored in the object attribute node_depths (dict) which
        presupposes that an individual word only occurs once in the
        tree, otherwise the node depth would be overridden to the
        depth of the latest occurrence.
        @param tree: Tuple representation of the tree/subtree.
        """
        # access child dict of current node
        for ele in tree[1]:
            # Termination condition:
            # if child has no subtree(s), stop here and set
            # depth(child) to depth(parent) + 1
            if not tree[1][ele][1]:
                self.__node_depths[tree[1][ele][0]] \
                    = self.__node_depths[tree[0]] + 1
            # if child has subtree(s)
            else:
                # depth(child) = depth(parent) + 1
                self.__node_depths[tree[1][ele][0]] \
                    = self.__node_depths[tree[0]] + 1
                # recursively proceed
                self.__get_tree_depth(tree[1][ele])

    def search(self, search_word, d):
        """
        Recursively searches for words in the BKTree exhibiting a maximum
        distance (d, distance in levenshtein/lsc units, etc.) to the search
        word. Returns the search results as a list of words.
        @param search_word: Query string of at least one character.
        @param d: Maximum distance (levenshtein, etc.) from search word to
        any target word to be included in the results. d must be an integer
        equal to or greater than 0.
        @return: Query results (words) as a list of strings.
        """
        # raise errors for invalid parameters
        if not isinstance(search_word, str) or len(search_word) == 0:
            raise SearchWordError("Search word must be a string equal to or"
                                  "longer than 1 character")
        if not isinstance(d, int) or d < 0:
            raise SearchDistanceError("Distance d must be an integer"
                                      " equal to or greater than 0")

        # determine distance between search word and root word
        d_root = self.__dist_func(search_word, self.__root_word)
        # if distance too big, return empty list
        if d_root > d:
            return []
        # if root within distance but no child(s), return root only
        elif not self.tree[1]:
            return [self.__root_word]
        else:
            # store results, root word has already been checked
            results = [self.__root_word]
            # define queue as list of tuples from child_dict of root node
            node_queue = [(node, child_dict)
                          for node, child_dict in self.tree[1].values()]
            # traverse all possible child nodes, i.e. in range d-dr <= d+dr
            while node_queue:
                # get first element from queue and divide it out
                node, child_dict = node_queue.pop(0)
                # get dr, i.e. dist(wq, wr)
                dr = self.__dist_func(search_word, node)
                if dr <= d:
                    results.append(node)
                # get all possible child nodes (only in range dr-d to dr+d)
                # from current node and proceed
                node_queue.extend(node for dist, node in child_dict.items()
                                  if dist in range(dr - d, dr + d + 1))

        return results

    @staticmethod
    def __check_list_integrity(word_list2):
        """
        Assures that every element in the list is a single word
        as str, especially when the word list was read in from a
        .txt file. Raises an error if this is not the case.
        @param word_list2: List of words (str).
        """
        for ele in word_list2:
            if not isinstance(ele, str) or len(ele.split()) > 1 \
                    or ele.isnumeric():
                raise ListIntegrityError("Every element in the word"
                                         " list must be a single word")

    def __save_as_pkl(self, path):
        """
        Serializes and stores the BKTree object as a pickle object
        in the given path.
        @param path: Valid file path ending in .pkl, as str.
        """
        assert isinstance(path, str) and path.endswith(".pkl"), \
            "Invalid path to .pkl file"
        with open(path, "wb") as f:
            pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)


def read_from_pkl(path):
    """
    Recreates a BKTree instance from a pickle file.
    @param path: Valid path to .pkl file, as str.
    """
    assert os.path.exists(path) and path.endswith(".pkl"), \
        "Invalid path to .pkl file"
    with open(path, "rb") as f:
        bk_tree = pickle.load(f)
        # return the original BKTree object
        return bk_tree
