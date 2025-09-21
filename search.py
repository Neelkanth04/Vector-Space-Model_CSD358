import re
import math
from collections import defaultdict, Counter
from preprocessing import split_text_into_words, clean_my_words
from soundex import get_soundex_code
from indexer import word_locations, word_counts_in_doc, doc_lengths, soundex_codes

def find_exact_phrase(words_in_phrase):
    """finds documents where the words in a phrase appear one after another"""
    if not words_in_phrase or words_in_phrase[0] not in word_locations:
        return set()

    # start with a set of documents that contain the first word
    possible_docs = set(word_locations[words_in_phrase[0]].keys())
    
    # narrow down the set of documents to only those containing all words in the phrase
    for word in words_in_phrase[1:]:
        possible_docs &= set(word_locations.get(word, {}).keys())

    found_in_docs = set()
    for doc_name in possible_docs:
        position_lists = [word_locations[word][doc_name] for word in words_in_phrase]
        
        # now, check if the positions are consecutive (e.g., position 5, 6, 7)
        for first_word_pos in position_lists[0]:
            is_a_match = True
            for i, next_word_positions in enumerate(position_lists[1:], 1):
                if (first_word_pos + i) not in next_word_positions: # checks if the next word is in the correct spot
                    is_a_match = False
                    break
            if is_a_match:
                found_in_docs.add(doc_name)
                break # we found a match in this doc, no need to check other positions
    return found_in_docs

def calculate_query_weights(query_words, total_docs):
    """calculates the tf-idf weight for each word in the user's query"""
    query_word_counts = Counter(query_words)
    query_vector = {}
    
    for word, count in query_word_counts.items():
        doc_freq = len(word_locations.get(word, {}))
        
        # if the word isn't found, try to find a similar-sounding word
        if doc_freq == 0:
            code = get_soundex_code(word)
            similar_words = soundex_codes.get(code, set())
            if similar_words:
                best_match = max(similar_words, key=lambda w: len(word_locations.get(w, {})))
                doc_freq = len(word_locations.get(best_match, {}))
                word = best_match # use the similar word instead

        if doc_freq > 0:
            weight = (1.0 + math.log10(count)) * math.log10(total_docs / doc_freq) # this is the ltc formula from the assignment
            query_vector[word] = query_vector.get(word, 0.0) + weight

    # normalize the query vector by its length
    length = math.sqrt(sum(w*w for w in query_vector.values()))
    if length > 0:
        for word in query_vector:
            query_vector[word] /= length
    return query_vector

def find_scores_for_docs(query_vector, docs_with_phrase=None):
    """calculates the final score for each relevant document"""
    scores = defaultdict(float)
    possible_docs = set()
    for word in query_vector:
        possible_docs.update(word_locations.get(word, {}).keys())

    # if this was a phrase search, only consider documents that had the phrase
    if docs_with_phrase is not None:
        possible_docs &= docs_with_phrase

    for doc_name in possible_docs:
        dot_product = 0.0
        doc_length = doc_lengths.get(doc_name, 1.0)
        
        for word, query_word_weight in query_vector.items():
            if word in word_counts_in_doc[doc_name]:
                doc_word_count = word_counts_in_doc[doc_name][word]
                doc_word_weight = 1.0 + math.log10(doc_word_count) # this is the lnc formula for doc weights
                dot_product += query_word_weight * (doc_word_weight / doc_length)
        
        if dot_product > 0:
            scores[doc_name] = dot_product

    return sorted(scores.items(), key=lambda item: (-item[1], item[0])) # sorts results by score (high to low)

def search(user_query):
    """the main search function that handles the user's query string"""
    # this finds any text inside of "quotes"
    phrase_pattern = r'"([^"]+)"'
    phrases_found = re.findall(phrase_pattern, user_query)
    normal_query_text = re.sub(phrase_pattern, ' ', user_query)
    
    normal_words = clean_my_words(split_text_into_words(normal_query_text))
    
    docs_that_match_phrase = None
    all_words_in_query = normal_words[:]
    
    if phrases_found:
        for phrase in phrases_found:
            words_in_phrase = clean_my_words(split_text_into_words(phrase))
            all_words_in_query.extend(words_in_phrase)
            
            # find the documents that contain this exact phrase
            matched_for_this_phrase = find_exact_phrase(words_in_phrase)
            if docs_that_match_phrase is None:
                docs_that_match_phrase = matched_for_this_phrase
            else:
                docs_that_match_phrase &= matched_for_this_phrase

    total_docs = len(word_counts_in_doc)
    final_query_vector = calculate_query_weights(all_words_in_query, total_docs)
    results = find_scores_for_docs(final_query_vector, docs_with_phrase=docs_that_match_phrase)
    return results