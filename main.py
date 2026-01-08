from gui import run_gui

from inverted_index import Inverted_index
from tf_idf import Tf_idf

import utils

docs: dict = utils.get_docs("test_data")

index: Inverted_index = Inverted_index()

# Creates new index structure from documents if saved index not found
if not index.load_index():

    index.new_index(docs)
    index.save_index()

ranking: Tf_idf = Tf_idf(index)

run_gui(ranking)