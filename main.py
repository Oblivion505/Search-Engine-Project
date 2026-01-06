from gui import run_gui

from inverted_index import Inverted_index
from tf_idf import Tf_idf

texts: list = []

with open("test_data/_ai790XSyjDGrcj7og9LdvGCsBC_SXvb.html", encoding = "utf-8") as f:

    texts.append(f.read())
    
with open("test_data/_avN5V1KDCAtN5Sh4Tm4YsuNzaHVTx8w.html", encoding = "utf-8") as f:

    texts.append(f.read())

with open("test_data/_bua93nkRXBBWiJ8ulRPXASuK0xbcL8l.html", encoding = "utf-8") as f:

    texts.append(f.read())

docs: dict = {"Luxor 3": texts[0], "Final Fantasy Tactics A2": texts[1], "Super Paper Mario": texts[2]}

index: Inverted_index = Inverted_index(docs)

ranking: Tf_idf = Tf_idf(index)

run_gui(ranking)