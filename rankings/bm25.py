# --- Improves on TF-IDF by taking document length into account in TF calculation ---

from inverted_index import Inverted_index
from rankings.tf_idf import Tf_idf

import tokenizor as tok

import math

class BM25(Tf_idf):

    def __init__(self, index: Inverted_index) -> None:
        super().__init__(index)

    def calculate_bm25_tf(self, postings_entry: dict, doc_length: int, avg_dl: int) -> float:

        # Constants that control scaling
        K1: float = 1.2
        B: float = 0.75

        freq_td: int = self.calculate_tf(postings_entry)

        return freq_td / (freq_td + K1 * (1 - B + B * doc_length / avg_dl))
    
    def calculate_bm25_tf_idf(self, tf: float, df: int, N: int) -> float:
        
        return tf * math.log10(1 + (N - df + 0.5) / (df + 0.5))

    def process_query(self, query: str) -> str:

        query_terms: set = set(tok.tokenize_query(query))

        if len(set(query_terms) & self._index.get_vocab().keys()) == 0:

            return "Query terms do not appear in any documents.\n"
        
        document_scores: dict = {}

        query_postings: dict
        query_docIDs: set

        N: int = len(self._index.get_docIDs())

        AVG_DL: int = self._index.get_average_doc_length()

        for term in query_terms:

            if term not in self._index.get_vocab().keys():

                continue

            query_postings = self._index.get_postings()[str(self._index.get_vocab()[term])]

            query_docIDs = set(query_postings.keys())

            df: int = len(query_docIDs)

            for docID in query_docIDs:

                doc_length: int = self._index.get_doc_length(docID)

                tf: float = self.calculate_bm25_tf(query_postings[docID], doc_length, AVG_DL)

                tf_idf: float = self.calculate_bm25_tf_idf(tf, df, N)

                if docID in document_scores.keys():

                    document_scores[docID].append(tf_idf)
                
                else:

                    document_scores[docID] = [tf_idf]

        summed_scores: list = []
        
        for docID, scores in document_scores.items():

            summed_scores.append([docID, sum(scores)])

        query_results: str = self.produce_results_with_summary(summed_scores, query_terms)

        return query_results