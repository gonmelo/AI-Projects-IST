from solver import *
from search import *

from collections import Counter
import linecache
import os
import tracemalloc

import timeit

def display_top(snapshot, key_type='lineno', limit=10):
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(key_type)

    print("Top %s lines" % limit)
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        # replace "/path/to/module/file.py" with "module/file.py"
        filename = os.sep.join(frame.filename.split(os.sep)[-2:])
        print("#%s: %s:%s: %.1f KiB"
              % (index, filename, frame.lineno, stat.size / 1024))
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            print('    %s' % line)

    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        print("%s other: %.1f KiB" % (len(other), size / 1024))
    total = sum(stat.size for stat in top_stats)
    print("Total allocated size: %.1f KiB" % (total / 1024))


tracemalloc.start()


b1 = [["_", "O", "O", "O", "_"],
          ["O", "_", "O", "_", "O"],
          ["_", "O", "_", "O", "_"],
          ["O", "_", "O", "_", "_"],
          ["_", "O", "_", "_", "_"]]

b2 = [["O", "O", "O", "X"],
          ["O", "O", "O", "O"],
          ["O", "_", "O", "O"],
          ["O", "O", "O", "O"]]


b3 = [["O", "O", "O", "X", "X"],
          ["O", "O", "O", "O", "O"],
          ["O", "_", "O", "_", "O"],
          ["O", "O", "O", "O", "O"]]

b4 = [["O", "O", "O", "X", "X", "X"],
          ["O", "_", "O", "O", "O", "O"],
          ["O", "O", "O", "O", "O", "O"],
          ["O", "O", "O", "O", "O", "O"]]

board = [["X", "X", "O", "O", "O", "O", "O", "X", "X"],
         ["X", "X", "O", "O", "O", "O", "O", "X", "X"],
         ["O", "O", "O", "O", "O", "O", "O", "O", "O"],
         ["O", "O", "O", "O", "O", "O", "O", "O", "O"],
         ["O", "O", "O", "O", "_", "O", "O", "O", "O"],
         ["O", "O", "O", "O", "O", "O", "O", "O", "O"],
         ["O", "O", "O", "O", "O", "O", "O", "O", "O"],
         ["X", "X", "O", "O", "O", "O", "O", "X", "X"],
         ["X", "X", "O", "O", "O", "O", "O", "X", "X"]]

# compare_searchers([solitaire(b2),solitaire(board4),solitaire(b1)],["Algoritms","Board","B2"],searchers=[
#     # breadth_first_tree_search,
#     #                              breadth_first_search,
#                                 # depth_first_graph_search,
#     #                              iterative_deepening_search,
#     #                              depth_limited_search,
#     #                              recursive_best_first_search,
#     #                             greedy_best_first_graph_search,
#                                  astar_search])

def greedy_search(solitaire):
    greedy_best_first_graph_search(solitaire, solitaire.h)

for s in [
    # breadth_first_tree_search,
    #                              breadth_first_search,
                                depth_first_graph_search,
                                 # iterative_deepening_search,
                                 # depth_limited_search,
                                 recursive_best_first_search,
                                # greedy_best_first_graph_search,
                                #  astar_search
          ]:

    start_time = timeit.default_timer()
    compare_searchers([solitaire(b1)], ["B1", "Branches/Test Solution/Nodes"], [s])
    time = round(timeit.default_timer() - start_time, 3)
    print("Executing time:{}\n".format(time))
    start_time = timeit.default_timer()
    compare_searchers([solitaire(b2)], ["B2", "Branches/Test Solution/Nodes"], [s])
    time = round(timeit.default_timer() - start_time, 3)
    print("Executing time:{}\n".format(time))

    compare_searchers([solitaire(b3)], ["B3", "Branches/Test Solution/Nodes"], [s])
    time = round(timeit.default_timer() - start_time, 3)
    print("Executing time:{}\n".format(time))
    start_time = timeit.default_timer()
    if(s!=depth_first_graph_search):
        compare_searchers([solitaire(b4)], ["B4", "Branches/Test Solution/Nodes"], [s])
        time = round(timeit.default_timer() - start_time, 3)
        print("Executing time:{}\n".format(time))




for s in [greedy_search,
                                 astar_search]:
    start_time = timeit.default_timer()
    compare_searchers([solitaire(b1)], ["B1", "Branches/Test Solution/Nodes"], [s])
    time = round(timeit.default_timer() - start_time, 3)
    print("Executing time:{}\n".format(time))
    start_time = timeit.default_timer()
    compare_searchers([solitaire(b2)], ["B2", "Branches/Test Solution/Nodes"], [s])
    time = round(timeit.default_timer() - start_time, 3)
    print("Executing time:{}\n".format(time))
    start_time = timeit.default_timer()
    compare_searchers([solitaire(b3)], ["B3", "Branches/Test Solution/Nodes"], [s])
    time = round(timeit.default_timer() - start_time, 3)
    print("Executing time:{}\n".format(time))
    start_time = timeit.default_timer()
    compare_searchers([solitaire(b4)], ["B4", "Branches/Test Solution/Nodes"], [s])
    time = round(timeit.default_timer() - start_time, 3)
    print("Executing time:{}\n".format(time))

# start_time = timeit.default_timer()
# compare_searchers([solitaire(board)], ["B4", "Branches/Test Solution/Nodes"], [astar_search])
# time = round(timeit.default_timer() - start_time, 3)
# print("Executing time:{}\n".format(time))


# print("\nMemory use:\n")
# snapshot = tracemalloc.take_snapshot()
# display_top(snapshot)
