# --- Tokenizes html documents and queries ---

import bs4 as bs
import regex as re

import nltk.downloader
nltk.download("stopwords")
nltk.download("punkt_tab")
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger_eng')

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk import pos_tag

STEMMER: PorterStemmer = PorterStemmer()
LEMMATIZER: WordNetLemmatizer = WordNetLemmatizer()
STOPWORDS: list = stopwords.words("english")
SPECIAL_CHARS: str = r'[^\w\s]' # Regex pattern : matches any character that is not alphanumeric or a whitespace

# Removes special chars from text and sets it to lowercase, then tokenizes it
def create_tokens(text: str) -> list:

    text = text.lower()
    alphanumeric_text: str = re.sub(SPECIAL_CHARS, "", text) 
    tokens: list = word_tokenize(alphanumeric_text, "english")

    return tokens

# Removes stopwords from tokens
def clean_tokens(tokens: list) -> list:

    return [tok for tok in tokens if tok not in STOPWORDS]

# Applies basic stemming to tokens
def stem_tokens(tokens: list) -> list:

    return [STEMMER.stem(tok) for tok in tokens]

# Applies lemmatization to tokens using parts of speech
def lemmatize_tokens(tokens: list) -> list:

    token_pos_pairs: list = pos_tag(tokens)

    # Parts of speech must be converted to be recognised by lemmatizer
    converted_pairs: list = []

    for pair in token_pos_pairs:

        pos: str = pair[1]

        if pos.startswith('V'):

            converted_pairs.append((pair[0], wordnet.VERB))

        elif pos.startswith('J'):

            converted_pairs.append((pair[0], wordnet.ADJ))

        elif pos.startswith('R'):

            converted_pairs.append((pair[0], wordnet.ADV))

        # Default POS is noun
        else:

            converted_pairs.append((pair[0], wordnet.NOUN))

    lemmatized_tokens: list = []

    for pair in converted_pairs:

        lemmatized_tokens.append(LEMMATIZER.lemmatize(pair[0], pair[1]))

    return lemmatized_tokens

# Adds related terms to query tokens to improve recall
def expand_query(query_tokens: list) -> list:

    expanded_tokens = []

    for token in query_tokens:

        expanded_tokens.append(token)

        for synset in wordnet.synsets(token):

            for lemma in synset.lemmas():

                expanded_tokens.append(lemma.name())

    return expanded_tokens

def tokenize_query(query: str) -> list:

    tokens: list = create_tokens(query)
    tokens = clean_tokens(tokens)
    tokens = expand_query(tokens)
    tokens = lemmatize_tokens(tokens)

    return tokens

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
    all_tokens: dict = {}

    for key, element in elements.items():

        all_tokens[key] = []

        for text in element:

            tokens: list = create_tokens(text)
            tokens = clean_tokens(tokens)
            tokens = lemmatize_tokens(tokens)

            all_tokens[key] += tokens

    # Counts token frequencies
    frequency_pairs: dict = {}

    for key, element in all_tokens.items():

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