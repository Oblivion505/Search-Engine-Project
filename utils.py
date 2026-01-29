# --- Supplies utility functions that can be used throughout the program ---

import os

import bs4 as bs

import tokenizor as tok

def get_document_title(dir_name: str, file_name: str) -> str:

    with open(dir_name + "/" + file_name, "r", encoding = "utf-8") as f:

        doc_text: str = f.read()

    soup: bs.BeautifulSoup = bs.BeautifulSoup(doc_text, "html.parser")

    if soup.title:

        return soup.title.get_text()

    return ""

def get_document_summary(dir_name: str, file_name: str, query_terms: set) -> str:

    with open(dir_name + "/" + file_name, "r", encoding = "utf-8") as f:

        doc_text: str = f.read()

    soup: bs.BeautifulSoup = bs.BeautifulSoup(doc_text, "html.parser")

    paragraphs: list = [p.get_text() for p in soup.find_all('p')]

    paragraph_tokens: list = []

    for p in paragraphs:

        paragraph_tokens.append(set(tok.create_tokens(p)))

    for i in range(0, len(paragraph_tokens)):

        if len(query_terms & paragraph_tokens[i]) != 0:

            return paragraphs[i][:200] + " ..." # Only take first 200 characters

    return "Summary not found."

def get_document_length(html_text: str) -> int:

    soup: bs.BeautifulSoup = bs.BeautifulSoup(html_text, "html.parser")

    return len(soup.get_text())

def get_docs(dir_name: str) -> dict:

    docs: dict = {}

    for file_name in os.listdir(dir_name):

        with open(dir_name + "/" + file_name, "r", encoding = "utf-8") as f:

            doc_text: str = f.read()

            docs[file_name] = doc_text
    
    return docs