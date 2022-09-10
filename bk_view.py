# Author: Simon Bross
# Date: August 23, 2022
# Python 3.9
# Windows 11

import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout


class BKView:
    """
    Represents the view component of the MVC architecture.
    It presents the model's (BKTree) data to the user and obtains
    the user input that is passed via the controller to the model.
    """

    @staticmethod
    def notify_start_of_interactive_mode():
        """
        Notifies the user about the start of the interactive mode.
        """
        notification = "Interactive Mode has started." \
                       "\nExit by entering a blank line " \
                       "(Press Enter without input)\n"
        print(notification)

    @staticmethod
    def get_tree_specs(root, num_words, depth):
        """
        Presents the following tree specifications to the user:
        root word of the BKTree, the number of its nodes/words, and
        its maximum tree depth, i.e. the longest path found from the root
        to a leaf.
        @param root: Root word of the BKTree instance as str.
        @param num_words: Number of words contained in the BKTree instance,
        as int.
        @param depth: Tree depth of the BKTree instance, as int.
        """
        s1 = "Root Word"
        s2 = "Number of Words"
        s3 = "Maximum Tree Depth"
        # store all output strings in a list in order to join them
        out_list = [
            "\n", "-" * 35, "Burkhard Keller Tree Specifications",
            "-" * 35, f"{s1:20}: {root}",
            f"{s2:20}: {num_words}", f"{s3:20}: {depth}",
            "\n"
        ]
        # join all strings together for output in terminal
        # strings are evenly aligned
        print("\n".join(out_list))

    @staticmethod
    def visualize(graph):
        """
        Graphically visualizes the BkTree in a new window after
        determining its layout. The graph's edges were built up
        during the model's instantiation. Note that networkx can
        only visualize the tree up to a few thousand nodes. However,
        the visualization of a tree this size is acutely indistinct
        and should be refrained from.
        @param graph: Graph of BKTree (networkx.Digraph)
        """
        # notify user that the visualization is being prepared
        print("The BKTree is being plotted. Depending on the tree size, "
              "this may take a few moments.\n")
        # get tree (dot) layout
        pos = graphviz_layout(graph, prog="dot")
        # draw nodes invisibly, only show the words
        nx.draw_networkx_nodes(graph, pos, node_size=200, alpha=0)
        # draw edges
        nx.draw_networkx_edges(graph, pos, edgelist=graph.edges,
                               width=0.5)
        # draw words/node labels, put black box around them
        nx.draw_networkx_labels(graph, pos, font_size=5,
                                font_family="monospace", font_color="white",
                                bbox=dict(facecolor="black"))

        # determine edge labels
        edge_labels = nx.get_edge_attributes(graph, "weight")
        # draw edge labels
        nx.draw_networkx_edge_labels(graph, pos, edge_labels,
                                     font_size=4)
        # plot settings
        ax = plt.gca()
        ax.margins(0)
        plt.axis("off")
        plt.tight_layout(pad=0.1)
        plt.gcf().set_dpi(200)
        plt.show(block=False)

    @staticmethod
    def get_query_word():
        """
        Obtains the query word from the user which is used in the
        tree lookup to find target words with a given maximum
        distance to it.
        @return: Query word as str.
        """
        query_word = input("Enter query word: ")
        return query_word

    @staticmethod
    def get_distance():
        """
        Obtains the distance from the user which is used in the
        tree search determining the maximum distance allowed between
        the query word and target word. The controller converts it to
        an integer, if possible.
        @return: Distance as str.
        """
        distance = input("Enter distance as integer: ")
        return distance

    @staticmethod
    def print_search_results(results):
        """
        Presents the search results from the model.
        @param results: Search results as a list of strings.
        """
        print(f"Search Result(s): {', '.join(results)}\n")

    @staticmethod
    def print_distance_error(error):
        """
        Notifies the user if the input for distance used in the
        tree search is invalid.
        @param error: Error message as str.
        """
        print(error)

    @staticmethod
    def print_query_word_error(error):
        """
        Notifies the user if the query word input used in the
        tree search is invalid.
        @param error: Error message as str.
        """
        print(error)
