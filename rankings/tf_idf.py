# --- Ranks documents on their relevance to a user query using TF-IDF ---

import math

from inverted_index import Inverted_index

import tokenizor as tok

import utils

class Tf_idf():

    _index: Inverted_index

    # Tag Weights should be positive ints
    _tag_weights: dict = {

        "title": 50,
        "h1": 5,
        "h2": 3,
        "h3": 2,
        "h4": 1,
        "h5": 1,
        "h6": 1,
        "li": 1,
        "td": 10, 
        "p": 1,
        "meta": 10 

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
    
    def calculate_unweighted_tf(self, postings_entry: dict) -> int:

        tf: int = 0

        for frequency in postings_entry.values():

            tf += frequency

        return tf
    
    def calculate_tf_idf(self, tf: int, df: int, N: int) -> float:

        return (1 + math.log10(tf)) * math.log10(N / df)

    def process_query(self, query: str) -> str:

        query_terms: set = set(tok.tokenize_query(query))

        if len(set(query_terms) & self._index.get_vocab().keys()) == 0:

            return "Query terms do not appear in any documents.\n"
        
        document_scores: dict = {}

        query_postings: dict
        query_docIDs: set

        N: int = len(self._index.get_docIDs())

        for term in query_terms:

            if term not in self._index.get_vocab().keys():

                continue

            query_postings = self._index.get_postings()[str(self._index.get_vocab()[term])]

            query_docIDs = set(query_postings.keys())

            df: int = len(query_docIDs)

            for docID in query_docIDs:

                tf: int = self.calculate_tf(query_postings[docID])

                tf_idf: float = self.calculate_tf_idf(tf, df, N)

                if docID in document_scores.keys():

                    document_scores[docID].append(tf_idf)
                
                else:

                    document_scores[docID] = [tf_idf]

        summed_scores: list = []
        
        for docID, scores in document_scores.items():

            summed_scores.append([docID, sum(scores)])

        query_results: str = self.produce_results_with_summary(summed_scores, query_terms)

        #self.store_results("saved_data", query, query_results)
        
        return query_results
    
    def produce_results(self, document_scores: list) -> str:

        ordered_scores = sorted(document_scores, key = lambda x: x[1], reverse = True) 

        query_results: str = ""

        score_count: int = 0

        for score in ordered_scores:

            # Return document html title in queries
            doc_name: str = utils.get_document_title("test_data", self._index.get_doc_name(score[0]))

            query_results += doc_name + " -> " + str(score[1]) + "\n\n"

            score_count += 1

            # To get top 10 results only
            if score_count == 10:

                break
        
        return query_results
    
    def produce_results_with_summary(self, document_scores: list, query_terms: set) -> str:

        ordered_scores = sorted(document_scores, key = lambda x: x[1], reverse = True) 

        query_results: str = ""

        score_count: int = 0

        for score in ordered_scores:

            # Return document html title in queries
            doc_name: str = utils.get_document_title("test_data", self._index.get_doc_name(score[0]))

            doc_summary: str = utils.get_document_summary("test_data", self._index.get_doc_name(score[0]), query_terms)

            query_results += "----------------------------------------------------" + "\n\n" 
            query_results += f"<No. {score_count + 1}> : " + doc_name + "\n\n" 
            query_results += "<URL> : " + self._index.get_doc_name(score[0]) + "\n\n" 
            query_results += "<Summary> : \n" + doc_summary + "\n\n"
            query_results += "----------------------------------------------------" + "\n\n" 
                
            score_count += 1

            # To get top 10 results only
            if score_count == 10:

                break
        
        return query_results
    
    def store_results(self, dir_name: str, query: str, query_results: str) -> None:

        saved_data: str = query + "\n\n" + query_results + "\n\n"

        with open(dir_name + "/results.txt", "a", encoding = "utf-8") as f:

            f.write(saved_data)

def test_tf_idf() -> None:

    texts: list = []

    with open("test_data/_ai790XSyjDGrcj7og9LdvGCsBC_SXvb.html", encoding = "utf-8") as f:

        texts.append(f.read())
    
    with open("test_data/_avN5V1KDCAtN5Sh4Tm4YsuNzaHVTx8w.html", encoding = "utf-8") as f:

        texts.append(f.read())

    with open("test_data/_bua93nkRXBBWiJ8ulRPXASuK0xbcL8l.html", encoding = "utf-8") as f:

        texts.append(f.read())

    docs: dict = {"Luxor 3": texts[0], "Final Fantasy Tactics A2": texts[1], "Super Paper Mario": texts[2]}

    index: Inverted_index = Inverted_index()
    index.create(docs)

    ranking: Tf_idf = Tf_idf(index)

    print(ranking.process_query("Game Games Mario Nintendo Final Egypt a b c d e f"))

if __name__ == "__main__":

    test_tf_idf()