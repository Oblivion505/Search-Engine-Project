from gui import Gui
from inverted_index import Inverted_index
from tf_idf import Tf_idf

import utils

docs: dict = utils.get_docs("test_data")

index: Inverted_index = Inverted_index()

# Creates new index structure from documents if saved index not found
if not index.load():

    index.create(docs)
    index.save()

ranking: Tf_idf = Tf_idf(index)

gui: Gui = Gui(ranking)
gui.run()