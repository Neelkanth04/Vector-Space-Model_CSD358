import re
import sys
import subprocess

# this part just makes sure you have the nltk library installed
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

# ---- download nltk data if it's missing ----
try:
    stopwords.words('english')
except LookupError:
    print("downloading nltk stopwords...")
    nltk.download('stopwords')
try:
    # this uses word_tokenize to check if 'punkt' is downloaded
    nltk.word_tokenize('test')
except LookupError:
    print("downloading nltk punkt tokenizer...")
    nltk.download('punkt')

my_stemmer = PorterStemmer() # creates the tool that finds the root of words (e.g., 'running' -> 'run')
common_words = set(stopwords.words('english')) # gets a list of common english words to ignore

def split_text_into_words(sentence): #tokenizing 
    """splits a sentence into a list of words and makes them lowercase"""
    words = re.split(r'\W+', sentence.lower()) # splits text by anything that isn't a letter or number
    return [word for word in words if word] # returns the list of words and removes any empty strings

def clean_my_words(word_list):           #normalising and stemming 
    """removes common words and finds the root form of the rest"""
    cleaned_list = [my_stemmer.stem(word) for word in word_list if word not in common_words]      # processes each word in the list
    return cleaned_list                # returns the final list of useful, stemmed words
