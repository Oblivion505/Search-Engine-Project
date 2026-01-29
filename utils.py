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

def get_document_elements(html_text: str) -> dict:

    soup: bs.BeautifulSoup = bs.BeautifulSoup(html_text, "html.parser")

    # Get elements of interest from document
    elements: dict = {}

    if soup.title:

        elements["title"] = [soup.title.get_text()]

    elements["h1"] = [h1.get_text() for h1 in soup.find_all('h1')]
    elements["h2"] = [h2.get_text() for h2 in soup.find_all('h2')]
    elements["h3"] = [h3.get_text() for h3 in soup.find_all('h3')]
    elements["h4"] = [h4.get_text() for h4 in soup.find_all('h4')]
    elements["h5"] = [h5.get_text() for h5 in soup.find_all('h5')]
    elements["h6"] = [h6.get_text() for h6 in soup.find_all('h6')]
    elements["li"] = [li.get_text() for li in soup.find_all('li')]
    elements["td"] = [td.get_text() for td in soup.find_all('td')]
    elements["p"] = [p.get_text() for p in soup.find_all('p')]

    keywords_tag: bs.Tag | None = soup.find('meta', attrs={"name": "keywords"})

    if keywords_tag:

        elements["meta"] = [keywords_tag.get("content", "")]
    
    return elements