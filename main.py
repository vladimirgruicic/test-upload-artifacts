from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import os

def find_similar_words(word_to_search, text):
    """
        Find similar words to the given word within the text.

        Args:
            word_to_search (str): The word to search for.
            text (str): The text to search within.

        Returns:
            list: A list of tuples containing similar words and their similarity scores.
        """
    # Tokenize the text
    words = text.split()

    # Find similar words using fuzzy matching
    similar_words = process.extract(word_to_search, words, scorer=fuzz.partial_ratio, limit=100)

    return similar_words

def extract_text_from_txt(txt_path):
    """
    Extract text from a .txt file.

    Args:
        txt_path (str): Path to the .txt file.

    Returns:
        str: Extracted text from the .txt file.
    """
    with open(txt_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text


def search_word_in_text_files(word_to_search, text_files_folder):
    """
    Search for a word in text files within a folder.

    Args:
        word_to_search (str): The word to search for.
        text_files_folder (str): Path to the folder containing text files.

    Returns:
        bool: True if the word is found in any text file, False otherwise.
    """
     # Handle cases where the specified folder doesn't exist
    if not os.path.exists(text_files_folder):
        print(f"Error: Folder '{text_files_folder}' does not exist.")
        return False


    # Iterate over text files in the folder
    for filename in os.listdir(text_files_folder):
        if filename.endswith(".txt"):
            txt_path = os.path.join(text_files_folder, filename)
            extracted_text = extract_text_from_txt(txt_path)
            if search_word(extracted_text, word_to_search):
                return True
    return False


def search_word(text, word):
    """
    Perform a case-insensitive search for a word within the text.

    Args:
        text (str): The text to search within.
        word (str): The word to search for.

    Returns:
        bool: True if the word is found, False otherwise.
    """
    return word.lower() in text.lower()


# Set the folder path containing the text files dynamically from the artifact folder name
artifact_folder = os.environ['GITHUB_WORKSPACE'] + "/pdf-to-txt"
text_files_folder = ""
for folder_name in os.listdir(artifact_folder):
    if os.path.isdir(os.path.join(artifact_folder, folder_name)):
        text_files_folder = os.path.join(artifact_folder, folder_name)
        break

if text_files_folder:
    # Set the word you want to search for
    word_to_search = "Pola"

    # Perform search in the extracted text
    found = search_word_in_text_files(word_to_search, text_files_folder)

    # Print the search result
    if found:
        print(f"The word '{word_to_search}' was found in the text.")
    else:
        print(f"The word '{word_to_search}' was not found in the text.")

    # Optional: Find similar words in the text files
    if found:
        similar_words = find_similar_words(word_to_search, extracted_text)
        print(f"Similar words to '{word_to_search}':")
        for word, score in similar_words:
            print(f"- {word} (Similarity: {score})")
else:
    print("Error: No text files folder found.")