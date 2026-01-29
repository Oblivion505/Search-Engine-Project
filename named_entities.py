import spacy as sp
from spacy.language import Language
from spacy.tokens import Doc

import utils

NER: Language = sp.load("en_core_web_sm")

def named_entities_from_doc(html_text: str) -> dict:

    elements: dict = utils.get_document_elements(html_text)

    named_entities: dict = {}

    for element in elements.values():

        for text in element:

            with NER.select_pipes(enable=['ner']): # Only runs the NER pipeline, speeding up processing time

                processed: Doc = NER(text)

                for entity in processed.ents:

                    name: str = entity.text.lower()

                    if name in named_entities.keys():

                        if entity.label_ in named_entities[name].keys():

                            named_entities[name][entity.label_] += 1

                        else:

                            named_entities[name][entity.label_] = 1

                    else:

                        named_entities[name] = {entity.label_ : 1}


    return named_entities

def named_entities_from_query(query: str) -> list:

    entity_pairs: list = []

    with NER.select_pipes(enable=['ner']):

        processed: Doc = NER(query)

    for entity in processed.ents:

        name: str = entity.text.lower()

        entity_pairs.append((name, entity.label_))

    return entity_pairs