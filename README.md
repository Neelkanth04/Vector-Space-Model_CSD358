# Vector Space Model Search Engine 🔍

This project is a ranked retrieval search engine built from scratch in Python for the **CSD358 Information Retrieval** assignment. The system uses the Vector Space Model with an `lnc.ltc` weighting scheme to rank text documents from a corpus against user queries.

---

### ✨ Features

- **Vector Space Model:** Implements the `lnc.ltc` cosine similarity ranking scheme for accurate document ranking.
- **Positional Index:** Builds a positional index to store the exact location of every word, enabling advanced search features.
- **Phrase Search (Novelty Feature):** Allows users to search for exact phrases by wrapping their query in double quotes (e.g., `"information retrieval"`).
- **Soundex Algorithm:** Includes a phonetic matching algorithm to find terms that sound alike, which is great for handling spelling variations in names.
- **Full Text Preprocessing:** A complete pipeline for text normalization, including tokenization, stop-word removal, and Porter Stemming.
- **Modular Codebase:** The project is organized into five distinct modules for clarity and maintainability.

---

### 📂 Project Structure

The code is split into five logical Python files:

- **`main.py`**: The main entry point that runs the program.
- **`preprocessing.py`**: Contains all functions for cleaning and normalizing text.
- **`soundex.py`**: Contains the implementation of the Soundex algorithm.
- **`indexer.py`**: Responsible for reading the corpus and building the search index.
- **`search.py`**: Contains all logic for query processing, ranking, and scoring documents.

---

### 🚀 How to Run

Follow these steps to get the search engine running on your local machine.

#### **1. Prerequisites**

- Python 3.x
- pip (Python package installer)

#### **2. Setup**

1.  **Clone the repository.**

2.  **Set up the Corpus:**
    - Place all your `.txt` document files inside the **`corpus`** folder. If the folder doesn't exist, please create it.

3.  **Install Dependencies:**
    - The script will attempt to install `nltk` automatically. To install it manually, run:
    ```bash
    pip install nltk
    ```

#### **3. Execution**

- Run the `main.py` script from your terminal:
    ```bash
    python main.py
    ```
- The program will first build the index, run the test cases, and then start an interactive search loop.

---

### 💡 Usage

Once the program is running, you can type your queries directly into the terminal.

- **Free-Text Query:** Simply type your search terms and press Enter.
    ```
    query> zomato business account
    ```

- **Phrase Search:** To search for an exact phrase, enclose your query in double quotes.
    ```
    query> "ancient family"
    ```

- **To Exit:** Type `exit` or `quit` and press Enter.

---

### 👥 Team Members

- **Nilaansh Mathur** - 2310110537
- **Manasvi Vedanta** - 2210110385
- **Shivam Doriya** - 2310110598

---

### 📝 License

This project is for educational purposes. Please feel free to use it for learning and reference.
