# Author: Simon Bross
# Date: August 27, 2022
# Python 3.9
# Windows 11

import click
from src.view.bk_view import BKView
from src.model.bk_tree import BKTree, read_from_pkl
from src.controller.bk_controller import BKController


class PickleError(Exception):
    def __init__(self, msg):
        super().__init__(self, msg)


def notify_tree_instantiation(word_list_length):
    """
    Notifies the user that the BKTree instance is being instantiated.
    @param word_list_length: Length of word list as int.
    @return: Notification as str.
    """
    return f"\nThe BKTree is being instantiated with a word list" \
           f" of {word_list_length} words. \nIt may take a few moments" \
           f" if a large (~200k) word list was provided."


@click.command()
# option for reading BKTree from .pkl file
@click.option("-pkl", "--pickle")
# path option for reading in word list
@click.option("-p", "--path", type=click.File('r', encoding="utf-8"))
# metric option
@click.option("-m", "--metric", default='levenshtein', )
# boolean option for visualization in new window
@click.option('--vis/--no-vis', default=True)
def main(pickle, path, metric, vis):
    """
    Provides a terminal interface and interactive mode for
    the (re)-construction, graphical visualization, and near-matches
    search to a string query of a Burkhard Keller Tree.
    @param pickle: Valid path to .pkl file storing a BKTree object.
    Function read_from_pkl checks if .pkl file exists.
    @param path: Valid path to a .txt file in which
    every line should be a single word assuring that a conforming
    word list can be created for the BkTree object.
    @param metric: Valid string metric. If none is provided,
    the levenshtein distance is selected by default.
    Available metrics are defined in src/model/metrics/metrics.py.
    The option expects the distance function's name as str.
    @param vis: Boolean flag that determines if a graphical visualization
    is being presented to the user.
    By default, the boolean is true (= --vis) and can be omitted if a
    visualization is desired.
    """
    # Case 1: recreate BKTree object from .pkl
    if pickle:
        if pickle.endswith(".pkl"):
            print("\nTrying to recreate BKTree from pickle file.")
            model = read_from_pkl(pickle)
        else:
            msg = "You must provide a file path leading to a .pkl file."
            raise PickleError(msg)

    # Case 2: create new BKTree from word list
    else:
        # file in path should be composed of one word per line
        # model throws an error if word_list is nonconforming
        word_list = path.read().splitlines()
        # notify user of BKTree instantiation
        print(notify_tree_instantiation(len(word_list)))
        # instantiate model
        model = BKTree(word_list, dist_func=metric)
        # do not visualize in new plotting window if more than 5000 words
        if len(word_list) > 5000:
            vis = False
    view = BKView()
    # create controller by combining MVC components
    controller = BKController(model, view)
    # start terminal programm/interactive mode with/without visualization
    controller.start_view(visualize=vis)


if __name__ == '__main__':
    main()
