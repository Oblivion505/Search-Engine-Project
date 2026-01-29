import sys

from gui import Gui
from inverted_index import Inverted_index
from rankings.tf_idf import Tf_idf

import utils

# Command Line Arguments
args: list = sys.argv

# { filename : text } pairs
docs: dict = utils.get_docs("test_data")

index: Inverted_index = Inverted_index()

# New index created if saved index doesn't exist or user enters 'new' as an argument
if not index.load() or (len(args) > 1 and args[1] == "new"):

    index.create(docs)
    index.save()

    print("New Index Saved")

else:

    ranking: Tf_idf = Tf_idf(index)

    gui: Gui = Gui(ranking)
    gui.run()