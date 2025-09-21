# file: preprocessing.py
import re
import sys
import subprocess

# ---- setup for nltk ----
try:
    import nltk
    from nltk.stem import PorterStemmer
    from nltk.corpus import stopwords
except ImportError:
    print("nltk not found, installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "nltk"])
    import nltk
    from nltk.stem import PorterStemmer
    from nltk.corpus import stopwords

# ---- download nltk resources if they are missing ----
try:
    stopwords.words('english')
except LookupError:
    print("downloading nltk stopwords...")
    nltk.download('stopwords')
try:
    nltk.word_tokenize('test')
except LookupError:
    print("downloading nltk punkt tokenizer...")
    nltk.download('punkt')

# ---- global tools for preprocessing ----
stemmer = PorterStemmer()
STOPWORDS = set(stopwords.words('english'))

def tokenize(text):
    """simple tokenizer: split on non-word, lowercase, filter empties"""
    tokens = re.split(r'\W+', text.lower())
    return [t for t in tokens if t]

def normalize_and_stem(tokens):
    """remove stopwords and apply stemming"""
    return [stemmer.stem(t) for t in tokens if t not in STOPWORDS]