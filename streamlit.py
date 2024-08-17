import streamlit as st
from english_words import get_english_words_set
from PIL import Image

# Set page configuration and title
st.set_page_config(page_title="Hangman Word Guesser", layout="centered")
st.markdown("<h1 style='text-align: center; color: #FF5733;'>Hangman Word Guesser</h1>", unsafe_allow_html=True)

# Display social links with icons
st.markdown("""
<div style='text-align: center;'>
    <a href='https://github.com/gauthamgtg' target='_blank'>
        <img src='https://image.flaticon.com/icons/png/512/25/25231.png' width='40' style='margin: 0 15px;'>
    </a>
    <a href='https://gauthamgtg.github.io/portfolio/' target='_blank'>
        <img src='https://image.flaticon.com/icons/png/512/1006/1006771.png' width='40' style='margin: 0 15px;'>
    </a>
    <a href='https://linkedin.com/in/gautham-mahadevan' target='_blank'>
        <img src='https://image.flaticon.com/icons/png/512/174/174857.png' width='40' style='margin: 0 15px;'>
    </a>
</div>
""", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center; color: #FF5733;'>This app was built by Gautham Mahadevan</h3>", unsafe_allow_html=True)

# Initialize word set
web2lowerset = get_english_words_set(['web2'], lower=True)

# Function to display error if excluded letter is in the word
def validate_excluded_letters(included_letters, excluded_letters):
    for letter in excluded_letters:
        if letter in included_letters:
            st.error(f"The letter '{letter}' is already used in the word. Please remove it from the excluded letters.")
            return False
    return True

# Slider to choose word length
word_length = st.slider("How many characters does the word have?", 2, 28, 5)

# Display input boxes side by side
st.markdown("<h4 style='color: #33CFFF;'>Enter the known letters below:</h4>", unsafe_allow_html=True)
cols = st.columns(word_length)
letter_inputs = [cols[i].text_input(f"Letter {i+1}", "", max_chars=1, key=f"letter_{i}") for i in range(word_length)]

# User input for excluded letters
st.markdown("<h4 style='color: #33CFFF;'>Enter letters that are not in the word:</h4>", unsafe_allow_html=True)
excluded_letters = st.text_input("Excluded letters (separated by commas):").replace(" ", "").lower().split(",")

# Check function
if st.button("Check"):
    if validate_excluded_letters(letter_inputs, excluded_letters):
        pattern = "".join([letter if letter else "_" for letter in letter_inputs])
        # Word guessing logic
        possible_words = [word for word in web2lowerset if len(word) == word_length and all(
            (c1 == c2 or c2 == "_") and c1 not in excluded_letters for c1, c2 in zip(word, pattern)
        )]

        if possible_words:
            st.markdown("<h4 style='color: #28a745;'>Possible words:</h4>", unsafe_allow_html=True)
            st.write(possible_words)
        else:
            st.markdown("<h4 style='color: #dc3545;'>No possible words found for your input.</h4>", unsafe_allow_html=True)

# Reset button to clear inputs
if st.button("Reset"):
    st.experimental_rerun()
