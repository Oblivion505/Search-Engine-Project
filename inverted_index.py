# --- Inverted Index Structure for document tokens ---

import json

import tokenizor as tok
import named_entities as ner

import utils

class Inverted_index():

    _docIDs: dict # Maps docIDs to doc names
    _vocab: dict # Maps vocab names to vocabIDs
    _postings: dict # Maps vocabIDs to docIDs of appearances
    _doc_lengths: dict # Maps docIDs to doc lengths (for BM25 ranking) 
    _entities: dict # Maps entity names to entityIDs
    _entity_postings: dict # Maps entityIDs to docIDs of named entity appearances

    def __init__(self) -> None:

        self._docIDs = {}
        self._vocab = {}
        self._postings = {}
        self._doc_lengths = {}
        self._entities = {}
        self._entity_postings = {}
    
    def create(self, docs: dict) -> None:

        # Reset instance variables if data has already been loaded to them
        self.__init__()

        self._add_docIDs(set(docs.keys()))

        doc_tokens: dict = {}
        token_keys: list= []

        doc_named_entities: dict = {}
        entity_keys: list = []

        for doc_name, doc in docs.items():

            self._doc_lengths[self.get_docID(doc_name)] = utils.get_document_length(docs[doc_name])

            token_dict: dict = tok.tokenize_document(doc)

            doc_tokens[doc_name] = token_dict
            token_keys += token_dict.keys()

            ner_dict: dict = ner.named_entities_from_doc(doc)

            doc_named_entities[doc_name] = ner_dict
            entity_keys += ner_dict.keys()

        for key in token_keys:

            self._add_vocab(key)

        for key in entity_keys:

            self._add_entity(key)

        for vocab, vocabID in self._vocab.items():

            appearances: dict = {}

            for doc_name, token_dict in doc_tokens.items():

                for token, frequencies in token_dict.items():

                    if vocab == token:

                        appearances[self.get_docID(doc_name)] = frequencies
            
            self._add_postings(vocabID, appearances)

        for entity, entityID in self._entities.items():

            appearances: dict = {}

            for doc_name, ner_dict in doc_named_entities.items():

                for entity_text, frequencies in ner_dict.items():

                    if entity == entity_text:

                        appearances[self.get_docID(doc_name)] = frequencies
            
            self._add_entity_postings(entityID, appearances)
    
    def save(self) -> None:

        save_data: dict = {

            "docIDs": self._docIDs,

            "vocab": self._vocab,

            "postings": self._postings,

            "doc_lengths": self._doc_lengths,

            "entities": self._entities,

            "entity_postings": self._entity_postings
        }

        json_string: str = json.dumps(save_data, indent = 4)

        with open("saved_data/index.json", "w", encoding = "utf-8") as f:

            f.write(json_string)
    
    def load(self) -> bool:

        with open("saved_data/index.json", "a+", encoding = "utf-8") as f:

            file_data: dict = {}

            if not f.read(1) == None:

                f.seek(0)
                file_data = json.load(f)
    
        if not len(file_data) == 0:

            if "docIDs" in file_data.keys():

                self._docIDs = file_data["docIDs"]
            
            if "vocab" in file_data.keys():

                self._vocab = file_data["vocab"]
            
            if "postings" in file_data.keys():

                self._postings = file_data["postings"]
            
            if "doc_lengths" in file_data.keys():

                self._doc_lengths = file_data["doc_lengths"]

            if "entities" in file_data.keys():

                self._entities = file_data["entities"]

            if "entity_postings" in file_data.keys():

                self._entity_postings = file_data["entity_postings"]
            
            return True
        
        return False

    def _add_docIDs(self, doc_names: set) -> None:

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

    def _add_entity(self, named_entity: str) -> None:

        if named_entity not in self._entities.keys():

            self._entities[named_entity] = len(self._entities)

    def _add_entity_postings(self, key: int, appearances: dict) -> None:

        if key not in self._entity_postings.keys():

            self._entity_postings[key] = appearances
    
    def get_doc_name(self, docID: int) -> str:

        return self._docIDs[docID] 
    
    def get_docID(self, doc_name: str) -> int | None:

        for key, value in self._docIDs.items():

            if value == doc_name:

                return key
        
        return None
    
    def get_doc_length(self, docID: int) -> int:

        return self._doc_lengths[docID]
    
    def get_average_doc_length(self) -> int:

        num_docs: int = len(self._doc_lengths)

        if num_docs == 0:

            return 0

        total_length: int = 0

        for doc_length in self._doc_lengths.values():

            total_length += doc_length

        return total_length

    def get_docIDs(self) -> dict:

        return self._docIDs

    def get_vocab(self) -> dict:

        return self._vocab
    
    def get_postings(self) -> dict:

        return self._postings
    
    def get_doc_lengths(self) -> dict:

        return self._doc_lengths
    
    def get_entities(self) -> dict:

        return self._entities
    
    def get_entities_postings(self) -> dict:

        return self._entity_postings

def test_inverted_index():

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

    print("Doc IDs: " + str(index.get_docIDs()) + "\n")
    print("Vocab: " + str(index.get_vocab()) + "\n")
    print("Postings: " + str(index.get_postings()) + "\n")

if __name__ == "__main__":

    test_inverted_index()