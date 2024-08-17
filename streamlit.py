import streamlit as st
import nltk
from english_words import get_english_words_set

# Download NLTK resources if not already downloaded
nltk.download('words')

# Load the word list from NLTK and the english_words library
web2lowerset = get_english_words_set(['web2'], lower=True)
nltk_words = set(nltk.corpus.words.words())
all_words = list(web2lowerset.union(nltk_words))

# Word completion model
class WordCompletionModel:
    def __init__(self, all_words):
        self.word_list = list(set(all_words))

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
st.title("Hangman Word Guesser")

# Reset session state
if st.button("Reset"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun()  # New way to rerun after clearing session state

# Slider to choose the number of characters (2 to 28)
num_characters = st.slider("Select the number of characters in the word:", min_value=2, max_value=28)

# Display input boxes based on the number of characters
placeholders = []
for i in range(num_characters):
    placeholders.append(st.text_input(f"Character {i + 1}", key=f"char_{i}"))

# User input for excluded letters
excluded_letters = st.text_input("Enter letters that are not in the word:")

# Validate if any excluded letters are already used in the word
if st.button("Check Word"):
    entered_word = "".join([char if char != "" else "_" for char in placeholders]).lower()
    excluded_set = set(excluded_letters.lower())
    duplicate_error = False
    for char in entered_word:
        if char in excluded_set:
            duplicate_error = True
            break

    if duplicate_error:
        st.error("Error: You have entered a letter in the excluded list that is already used in the word!")
    else:
        # Run the model to find possible completions
        model = WordCompletionModel(all_words)
        possible_words = model.complete_word(entered_word, excluded_set)

        if possible_words:
            st.write("Possible words:")
            st.write(possible_words)
        else:
            st.write("No possible words found for your input.")
