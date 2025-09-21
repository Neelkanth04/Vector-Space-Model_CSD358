from indexer import create_search_index
from search import search

def display_results(search_results, num_to_show=10):
    """prints the top search results in a clean format."""
    if not search_results:
        print("no results found.")
        return
    for i, (doc_name, score) in enumerate(search_results[:num_to_show], 1):
        print(f"{i}. ('{doc_name}', {score})")

def start_program():
    """this function builds the index, runs the tests, and starts the search loop."""
    if not create_search_index():    # this calls the function from indexer.py to build the index first
        return
    
    # ---- run the two test cases from the assignment pdf ----
    print("\n" + "="*20 + " Test Queries " + "="*20)
    query1 = "Developing your Zomato business account and profile is a great way to boost your restaurant's online reputation" # this is the first test query
    print(f"\nQ1: {query1}")
    results1 = search(query1)
    display_results(results1)

    query2 = "Warwickshire, came from an ancient family and was the heiress to some land"
    print(f"\nQ2: {query2}")
    results2 = search(query2)
    display_results(results2)

    # ---- start the interactive search loop for the user ----
    print("\n" + "="*20 + " Interactive Search " + "="*20)
    print("type a query, use \"phrases in quotes\", or type 'exit' to quit.")
    
    while True:
        try:
            user_input = input("\nquery> ").strip()   # asks the user to type a query and waits
            if not user_input:
                continue
            if user_input.lower() in ('exit', 'quit'):
                print("exiting.")
                break
            
            results = search(user_input)   # calls the main search function from search.py with the user's input
            display_results(results)
            
        except (EOFError, KeyboardInterrupt):
            print("\nexiting.")
            break

if __name__ == "__main__":
    start_program()