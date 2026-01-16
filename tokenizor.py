# --- Tokenizes the user's input query ---

import bs4 as bs
import regex as re

import nltk.downloader
nltk.download("stopwords")
nltk.download("punkt_tab")

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

PS: PorterStemmer = PorterStemmer()
STOPWORDS: list = stopwords.words("english")
SPECIAL_CHARS: str = r'[^\w\s]' # Regex pattern : matches any character that is not alphanumeric or a whitespace

def create_tokens(text: str) -> list:

    alphanumeric_text: str = re.sub(SPECIAL_CHARS, "", text) 
    tokens: list = word_tokenize(alphanumeric_text, "english")

    return [PS.stem(tok) for tok in tokens if tok not in STOPWORDS]

def tokenize_document(html_text: str) -> dict: 

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
    
    # Tokenize elements and clean the tokens 
    tokens: dict = {}

    for key, element in elements.items():

        tokens[key] = []

        for text in element:

            tokens[key] += create_tokens(text)

    # Counts token frequencies
    frequency_pairs: dict = {}

    for key, element in tokens.items():

        for token in element:

            if token in frequency_pairs.keys():

                if key in frequency_pairs[token]:

                    frequency_pairs[token][key] += 1

                else:

                    frequency_pairs[token][key] = 1
            
            else:

                frequency_pairs[token] = {key: 1}

    return frequency_pairs

# --- Testing ---

def test_tokenizor() -> None:

    with open("test_data/_ai790XSyjDGrcj7og9LdvGCsBC_SXvb.html", encoding = "utf-8") as f:

        text: str = f.read()

        print(tokenize_document(text))

if __name__ == "__main__":

    test_tokenizor()