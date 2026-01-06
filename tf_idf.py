# --- Ranks documents on their relevance to a user query using Tf-idf ---

import math

import tokenizor as tok

from inverted_index import Inverted_index

class Tf_idf():

    _index: Inverted_index

    _tag_weights: dict = {

        "title": 10,
        "h1": 5,
        "h2": 3,
        "h3": 2,
        "p": 1,
        "meta": 1

    }

    def __init__(self, index: Inverted_index) -> None:

        self._index = index
    
    def get_index(self) -> Inverted_index:

        return self._index
    
    def get_tag_weights(self) -> dict:

        return self._tag_weights

    def calculate_tf(self, postings_entry: dict) -> int:

        tf: int = 0

        for tag, frequency in postings_entry.items():

            tf += frequency * self._tag_weights[tag]

        return tf
    
    def calculate_tf_idf(self, tf: int, df: int, N: int) -> float:

        return (1 + math.log(tf, 10)) * math.log(N / df, 10)

    def process_query(self, query: str) -> str:

        if query not in self._index.get_vocab().keys():

            return "Query term does not appear in any documents.\n"
        
        document_scores: list = []
        
        query_postings: dict = self._index.get_postings()[self._index.get_vocab()[query]]
        query_docIDs: set = set(query_postings.keys())

        N: int = len(self._index.get_docIDs())
        df: int = len(query_docIDs)

        for docID in query_docIDs:

            tf: int = self.calculate_tf(query_postings[docID])

            tf_idf: float = self.calculate_tf_idf(tf, df, N)

            document_scores.append([docID, tf_idf])
        
        ordered_scores = sorted(document_scores, key = lambda x: x[1], reverse = True) 

        query_result: str = ""

        for score in ordered_scores:

            query_result += self._index.get_docName(score[0]) + " -> " + str(score[1]) + "\n\n"

        return query_result

def test_tf_idf() -> None:

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

    ranking.process_query("Game")

if __name__ == "__main__":

    test_tf_idf()