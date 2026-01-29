# --- TF-IDF ranking that also uses NER (Named Entity Recognition) for improved search ---

from inverted_index import Inverted_index
from rankings.tf_idf import Tf_idf

import tokenizor as tok
import named_entities as ner

class Ner(Tf_idf):

    _ner_weight: int = 50 

    def __init__(self, index: Inverted_index) -> None:
        super().__init__(index)

    def calculate_ner_tf(self, postings_entry: dict, entity_type: str) -> int:

        tf: int = 0

        for type, frequency in postings_entry.items():

            if type == entity_type:

                tf += frequency * self._ner_weight

        return tf

    def process_query(self, query: str) -> str:

        query_terms: set = set(tok.tokenize_query(query))

        entity_pairs: list = ner.named_entities_from_query(query)

        if len(set(query_terms) & self._index.get_vocab().keys()) == 0:

            return "Query terms do not appear in any documents.\n"
        
        document_scores: dict = {}

        query_postings: dict
        query_docIDs: set

        N: int = len(self._index.get_docIDs())

        for term in query_terms:

            if term not in self._index.get_vocab().keys():

                continue

            query_postings: dict = self._index.get_postings()[str(self._index.get_vocab()[term])]

            query_docIDs: set = set(query_postings.keys())

            df: int = len(query_docIDs)

            for docID in query_docIDs:

                tf: int = self.calculate_tf(query_postings[docID])

                tf_idf: float = self.calculate_tf_idf(tf, df, N)

                if docID in document_scores.keys():

                    document_scores[docID].append(tf_idf)
                
                else:

                    document_scores[docID] = [tf_idf]

        for pair in entity_pairs:

            # Check if any documents contain the query entity
            if pair[0] not in self._index.get_entities().keys():

                continue

            entity_postings: dict = self._index.get_entities_postings()[str(self._index.get_entities()[pair[0]])]

            entity_docIDs: set = set(entity_postings.keys())

            df: int = len(entity_docIDs)

            for docID in entity_docIDs:

                # Check if document entity has same entity type as query
                if pair[1] not in entity_postings[docID].keys():

                    continue

                tf: int = self.calculate_ner_tf(entity_postings[docID], pair[1])

                tf_idf: float = self.calculate_tf_idf(tf, df, N)

                if docID in document_scores.keys():

                    document_scores[docID].append(tf_idf)
                
                else:

                    document_scores[docID] = [tf_idf]

        summed_scores: list = []
        
        for docID, scores in document_scores.items():

            summed_scores.append([docID, sum(scores)])

        query_results: str = self.produce_results_with_summary(summed_scores, query_terms)
        
        return query_results