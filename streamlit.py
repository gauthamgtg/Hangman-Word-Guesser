import streamlit as st
import nltk
from english_words import get_english_words_set

# Download NLTK resources if not already downloaded
nltk.download('words')

# Load the word list using `english_words` package
web2lowerset = get_english_words_set(['web2'], lower=True)

# Word completion model
class WordCompletionModel:
    def __init__(self):
        # Load the NLTK word list and merge with words from `english_words` package
        self.word_list = nltk.corpus.words.words() + list(web2lowerset)
        # Remove duplicates
        self.word_list = list(set(self.word_list))

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

# Ask how many characters the word has
word_length = st.number_input("How many characters does the word have?", min_value=1, step=1)

if word_length:
    # Display input boxes for the user to enter characters
    incomplete_word = ""
    cols = st.columns(word_length)
    for i in range(word_length):
        char = cols[i].text_input(f"Letter {i+1}:", max_chars=1)
        incomplete_word += char if char else "_"

    # User input for excluded letters
    excluded_letters = st.text_input("Enter letters that are not in the word:")

    # Check if any excluded letter is present in the incomplete word
    if any(letter in incomplete_word for letter in excluded_letters):
        st.error("You cannot exclude letters that are already part of the word!")

    if st.button("Find Possible Words"):
        model = WordCompletionModel()
        possible_words = model.complete_word(incomplete_word.lower(), set(excluded_letters.lower()))

        if possible_words:
            st.write("Possible words:")
            st.write(possible_words)
        else:
            st.write("No possible words found for your input.")
