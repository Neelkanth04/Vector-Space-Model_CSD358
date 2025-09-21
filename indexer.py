import os
import math
from collections import defaultdict, Counter
from preprocessing import split_text_into_words, clean_my_words #functions from preprocessing
from soundex import get_soundex_code 

# ---- data holders for our search index ----
word_locations = defaultdict(lambda: defaultdict(list)) # tracks where each word is located in each file
word_counts_in_doc = defaultdict(Counter) # counts how many times each word appears in a file
doc_lengths = {} # stores the calculated length for each document
all_words = set() # a set of every unique word we find
soundex_codes = defaultdict(set) # stores soundex codes to find similar-sounding words
corpus_folder = "corpus"

def calculate_doc_lengths():
    """calculates the vector length for each document"""
    for doc_name, term_counts in word_counts_in_doc.items():
        sum_of_squares = 0.0
        for word, count in term_counts.items():
            weight = 1.0 + math.log10(count)       # calculates the log-frequency weight for a word
            sum_of_squares += weight * weight
        doc_lengths[doc_name] = math.sqrt(sum_of_squares)

def create_search_index():
    """reads all text files and builds all parts of the search index"""
    print("building index...")
    if not os.path.isdir(corpus_folder):
        print(f"error: corpus folder '{corpus_folder}' not found.")
        return False

    all_files = sorted([f for f in os.listdir(corpus_folder) if f.lower().endswith('.txt')])
    
    for file_name in all_files:
        file_path = os.path.join(corpus_folder, file_name)
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file_handle: # opens and reads each text file
            text_content = file_handle.read()
        
        words = split_text_into_words(text_content)
        clean_words = clean_my_words(words)
        
        for position, word in enumerate(clean_words):
            word_locations[word][file_name].append(position) # stores the exact position of the word in the file
            word_counts_in_doc[file_name][word] += 1
            all_words.add(word)
    
    for word in all_words:
        code = get_soundex_code(word)
        soundex_codes[code].add(word) # creates a soundex code for each unique word
        
    calculate_doc_lengths() # calculates the lengths after all documents are processed
    print(f"indexed {len(all_files)} documents, vocab size {len(all_words)}")
    return True