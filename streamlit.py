import streamlit as st
import nltk
import pickle

# Download NLTK resources if not already downloaded
nltk.download('words')

# Load the pre-processed word list
@st.cache_data
def load_word_list():
    with open('word_list.pkl', 'rb') as f:
        return pickle.load(f)

# Word completion model
class WordCompletionModel:
    def __init__(self, word_list):
        self.word_list = word_list

    def complete_word(self, incomplete_word, excluded_letters):
        possible_words = []
        for word in self.word_list:
            if self.matches_pattern(word, incomplete_word) and not self.contains_excluded_letters(word, excluded_letters):
                possible_words.append(word)
        return possible_words

    def matches_pattern(self, word, pattern):
        if len(word) != len(pattern):
            return False
        for i in range(len(word)):
            if pattern[i] != '_' and pattern[i] != word[i]:
                return False
        return True

    def contains_excluded_letters(self, word, excluded_letters):
        for letter in excluded_letters:
            if letter in word:
                return True
        return False

# Streamlit Interface
st.title("Word Completion App")

# Load the pre-processed word list
all_words = load_word_list()

# User input for the word with missing letters
incomplete_word = st.text_input("Enter a word with missing letters (use '_' for missing letters):")

# User input for excluded letters
excluded_letters = st.text_input("Enter letters that are not in the word:")

if incomplete_word:
    model = WordCompletionModel(all_words)
    possible_words = model.complete_word(incomplete_word.lower(), set(excluded_letters.lower()))

    if possible_words:
        st.write("Possible words:")
        st.write(possible_words)
    else:
        st.write("No possible words found for your input.")
