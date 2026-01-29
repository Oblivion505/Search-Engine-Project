# --- Extends TF-IDF by converting documents into vectors with TF-IDF scores for each term --- 

import math

from inverted_index import Inverted_index
from rankings.tf_idf import Tf_idf

import tokenizor as tok

class Vector_space(Tf_idf):

    def __init__(self, index: Inverted_index) -> None:
        super().__init__(index)

    def get_relevant_docIDs(self, query_terms: list) -> list:

        relevant_docIDs: list = []

        for term in query_terms:

            if term not in self._index.get_vocab().keys():

                continue

            query_postings = self._index.get_postings()[str(self._index.get_vocab()[term])]

            query_docIDs = set(query_postings.keys())

            for docID in query_docIDs:

                if docID not in relevant_docIDs:

                    relevant_docIDs.append(docID)
            
        return relevant_docIDs
    
    def normalize_vector(self, vector: list) -> None:

        sum_of_squares: float = 0

        for num in vector:

            sum_of_squares += num ** 2

        magnitude: float = math.sqrt(sum_of_squares)

        # Avoids division by zero
        if magnitude == 0:

            magnitude = 1

        for i in range(0, len(vector)):

            vector[i] = vector[i] / magnitude
    
    def cosine_similarity(self, vector_1: list, vector_2: list) -> float:

        cosine_score: float = 0

        for i in range(0, len(vector_1)):

            cosine_score += vector_1[i] * vector_2[i]

        return cosine_score

    def process_query(self, query: str) -> str:

        query_terms: list = tok.tokenize_query(query)

        if len(set(query_terms) & self._index.get_vocab().keys()) == 0:

            return "Query terms do not appear in any documents.\n"
        
        query_vector = []
        document_vectors = {}

        for docID in self.get_relevant_docIDs(query_terms):

            document_vectors[docID] = []

        query_postings: dict
        query_docIDs: set

        N: int = len(self._index.get_docIDs()) + 1

        for term in query_terms:

            df: int

            if term not in self._index.get_vocab().keys():

                df = 1

                for docID in document_vectors.keys():

                    document_vectors[docID].append(0)

            else: 

                query_postings = self._index.get_postings()[str(self._index.get_vocab()[term])]

                query_docIDs = set(query_postings.keys())

                df = len(query_docIDs) + 1

                for docID in document_vectors.keys():

                    if docID in query_docIDs:

                        tf: int = self.calculate_tf(query_postings[docID])

                        tf_idf: float = self.calculate_tf_idf(tf, df, N)

                        document_vectors[docID].append(tf_idf)

                    else:

                        document_vectors[docID].append(0)

            query_tf: int = query_terms.count(term)

            query_tf_idf: float = self.calculate_tf_idf(query_tf, df, N)

            query_vector.append(query_tf_idf)

        self.normalize_vector(query_vector)

        for vector in document_vectors.values():

            self.normalize_vector(vector)
        
        document_scores = []

        for docID, vector in document_vectors.items():

            cosine_score: float = self.cosine_similarity(query_vector, vector)

            document_scores.append([docID, cosine_score])

        query_results: str = self.produce_results_with_summary(document_scores, set(query_terms))

        return query_results