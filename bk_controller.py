# Author: Simon Bross
# Date: August 23, 2022
# Python 3.9
# Windows 11

import sys
from src.model.bk_tree import BKTree
from src.view.bk_view import BKView


class BKController:

    def __init__(self, model, view):
        """
        Instantiates a BKController as part of the MVC pattern.
        It serves as a mediator between the model and view, separating
        the user input/output and the data processing.
        @param model: Model component of the MVC architecture, a BKTree
        instance.
        @param view: View component of the MVC architecture, a BKView instance.
        """
        assert isinstance(model, BKTree), \
            "Model must be a BKTree instance"
        self.__model = model
        assert isinstance(view, BKView), \
            "View must be a BKView instance"
        self.__view = view

    @property
    def model(self):
        """
        Returns the controller's model, i.e. a BKTree instance.
        @return: BKTree object.
        """
        return self.__model

    @property
    def view(self):
        """
        Returns the controller's view, i.e. a BKView instance.
        @return: BKView object.
        """
        return self.__view

    def start_view(self, visualize=False):
        """
        Starts the view that presents the model output and
        obtains the user input. It comprises the presentation
        of the tree's specifications and its visualization
        (if visualize is set to True) and sets off the
        interactive mode in the terminal.
        @param visualize: Boolean determining if the view will
        visualize the BKTree.
        """
        # show tree specifications to user (tree depth, root word,
        # and number of words/nodes in the tree)
        depth = self.model.tree_depth
        root = self.model.root
        num_words = self.model.num_of_words
        self.view.get_tree_specs(root, num_words, depth)
        # visualize graph (new window)
        if visualize:
            self.view.visualize(self.model.graph)

        # start interactive mode in terminal
        self.__interactive_mode()

    def __interactive_mode(self):
        """
        Manages the terminal interactive mode in which the user can perform
        word searching in the BKTree, given a query word and maximum distance
        to the target words in the tree. The method obtains both the query word
        and distance from the user input (in view) and passes it to the
        BKTree model. Thereafter, the search result from the model is presented
        to the user. Looping enables multiple search cycles which are stopped
        when a blank line is entered (the entire programm closes).
        """
        # notify user that the interactive mode has started
        self.view.notify_start_of_interactive_mode()

        # main loop for interactive mode logic
        while True:
            # get query word from user, remove leading/trailing whitespaces
            query_word = self.view.get_query_word().strip()
            # if query word is not alphabetic (must not be a numeric string)
            # or not a blank line, loop until user provides a correct input
            # isalpha assures that query word is a single word
            while not query_word.isalpha() and query_word != "":
                error = "Error: Query word must be an alphabetic string" \
                        " without numbers/special characters, " \
                        "i.e. a single word."
                self.view.print_query_word_error(error)
                query_word = self.view.get_query_word().strip()
            # close programm if input is a blank line
            if query_word == "":
                sys.exit("\nThe programm was closed.\n")

            # get distance from user, remove leading/trailing whitespaces
            distance = self.view.get_distance().strip()
            # if distance is not numeric or not a blank line,
            # loop until user provides a correct input
            # isnumeric function assures that distance is an integer >= 0
            while not distance.isnumeric() and distance != "":
                error2 = "Error: Distance must be a single positive integer" \
                         " or 0."
                self.view.print_distance_error(error2)
                distance = self.view.get_distance().strip()
            # close programm if input is a blank line
            if distance == "":
                sys.exit("\nThe programm was closed.\n")
            # convert numeric string to integer
            distance = int(distance)

            # get search results
            result = self.model.search(query_word, distance)
            # print result(s) as joined string rather than a list
            self.view.print_search_results(result)
