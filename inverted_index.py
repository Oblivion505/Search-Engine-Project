# --- Inverted Index Structure for document tokens ---

import tokenizor as tok

class Inverted_index():

    _docIDs: dict
    _vocab: dict
    _postings: dict

    def __init__(self, docs: dict) -> None:

        self._docIDs = {}
        self._vocab = {}
        self._postings = {}

        self._set_docIDs(set(docs.keys()))

        doc_tokens: dict = {}
        token_keys: list= []

        for doc_name, doc in docs.items():

            token_dict: dict = tok.tokenize_document(doc)

            doc_tokens[doc_name] = token_dict
            token_keys += token_dict.keys()

        for key in token_keys:

            self._add_vocab(key)

        for vocab, vocabID in self._vocab.items():

            appearances: dict = {}

            for doc_name, token_dict in doc_tokens.items():

                for token, frequencies in token_dict.items():

                    if vocab == token:

                        appearances[self.get_docID(doc_name)] = frequencies
            
            self._add_postings(vocabID, appearances)

    def _set_docIDs(self, doc_names: set) -> None:

        id: int = 0

        for name in doc_names:

            self._docIDs[id] = name

            id += 1
    
    def _add_vocab(self, vocab: str) -> None:

        if vocab not in self._vocab.keys():

            self._vocab[vocab] = len(self._vocab)

    def _add_postings(self, key: int, appearances: dict) -> None:

        if key not in self._postings.keys():

            self._postings[key] = appearances
    
    def get_docName(self, docID: int) -> str:

        return self._docIDs[docID] 
    
    def get_docID(self, doc_name: str) -> int | None:

        for key, value in self._docIDs.items():

            if value == doc_name:

                return key
        
        return None

    def get_docIDs(self) -> dict:

        return self._docIDs

    def get_vocab(self) -> dict:

        return self._vocab
    
    def get_postings(self) -> dict:

        return self._postings

def test_inverted_index():

    texts: list = []

    with open("test_data/_ai790XSyjDGrcj7og9LdvGCsBC_SXvb.html", encoding = "utf-8") as f:

        texts.append(f.read())
    
    with open("test_data/_avN5V1KDCAtN5Sh4Tm4YsuNzaHVTx8w.html", encoding = "utf-8") as f:

        texts.append(f.read())

    with open("test_data/_bua93nkRXBBWiJ8ulRPXASuK0xbcL8l.html", encoding = "utf-8") as f:

        texts.append(f.read())

    docs: dict = {"Luxor 3": texts[0], "Final Fantasy Tactics A2": texts[1], "Super Paper Mario": texts[2]}

    index: Inverted_index = Inverted_index(docs)

    print("Doc IDs: " + str(index.get_docIDs()) + "\n")
    print("Vocab: " + str(index.get_vocab()) + "\n")
    print("Postings: " + str(index.get_postings()) + "\n")

if __name__ == "__main__":

    test_inverted_index()