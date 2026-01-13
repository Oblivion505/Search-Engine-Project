# --- Supplies utility functions that can be used throughout the program ---

import os

import bs4 as bs

def get_document_title(html_text: str) -> str:

    soup: bs.BeautifulSoup = bs.BeautifulSoup(html_text, "html.parser")

    if soup.title:

        return soup.title.get_text()

    return ""

def get_docs(dir_name: str) -> dict:

    docs: dict = {}

    for file_name in os.listdir(dir_name):

        with open(dir_name + "/" + file_name, encoding = "utf-8") as f:

            doc_text: str = f.read()

            doc_title: str = get_document_title(doc_text)

            docs[doc_title] = doc_text
    
    return docs