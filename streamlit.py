import streamlit as st
from english_words import get_english_words_set

# Set page configuration and title
st.set_page_config(page_title="Hangman Word Guesser", layout="centered")
st.markdown("<h1 style='text-align: center; color: #FF5733;'>Hangman Word Guesser</h1>", unsafe_allow_html=True)

# Display social links with updated icons
st.markdown("""
<div style='text-align: center;'>
    <a href='https://github.com/gauthamgtg' target='_blank'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg' width='40' style='margin: 0 15px;' alt='GitHub'>
    </a>
    <a href='https://gauthamgtg.github.io/portfolio/' target='_blank'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/6/69/Deepin_Icon_Theme_%E2%80%93_dde-file-manager_%284%29.svg' width='40' style='margin: 0 15px;' alt='Projects'>
    </a>
    <a href='https://linkedin.com/in/gautham-mahadevan' target='_blank'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/8/81/LinkedIn_icon.svg' width='40' style='margin: 0 15px;' alt='LinkedIn'>
    </a>
</div>
""", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center; color: #FF5733;'>This app was built by Gautham Mahadevan</h3>", unsafe_allow_html=True)

# Initialize word set
web2lowerset = get_english_words_set(['web2'], lower=True)

# Function to display error if excluded letter is in the word
def validate_excluded_letters(included_letters, excluded_letters):
    if not excluded_letters:
        return True
    for letter in excluded_letters:
        if letter in included_letters:
            st.error(f"The letter '{letter}' is already used in the word. Please remove it from the excluded letters.")
            return False
    return True

# Slider to choose word length
word_length = st.slider("How many characters does the word have?", 2, 28, 5)

# Initialize session state
if 'letter_inputs' not in st.session_state:
    st.session_state.letter_inputs = [""] * word_length
if 'excluded_letters' not in st.session_state:
    st.session_state.excluded_letters = []

# Update session state if word length changes
if len(st.session_state.letter_inputs) != word_length:
    st.session_state.letter_inputs = [""] * word_length

# Display input boxes side by side
st.markdown("<h4 style='color: #33CFFF;'>Enter the known letters below:</h4>", unsafe_allow_html=True)
cols = st.columns(word_length)
for i in range(word_length):
    st.session_state.letter_inputs[i] = cols[i].text_input(
        f"Letter {i+1}", st.session_state.letter_inputs[i], max_chars=1, key=f"letter_{i}"
    ).lower()  # Convert input to lowercase

# User input for excluded letters
st.markdown("<h4 style='color: #33CFFF;'>Enter letters that are not in the word:</h4>", unsafe_allow_html=True)
excluded_letters_input = st.text_input("Excluded letters (separated by commas):", value=", ".join(st.session_state.excluded_letters)).lower()
st.session_state.excluded_letters = [letter for letter in excluded_letters_input if letter.isalpha()]

# Check function
col1, col2 = st.columns([4, 1])
with col1:
    if st.button("Check"):
        if validate_excluded_letters(st.session_state.letter_inputs, st.session_state.excluded_letters):
            pattern = "".join([letter if letter else "_" for letter in st.session_state.letter_inputs])
            # Word guessing logic
            possible_words = [word for word in web2lowerset if len(word) == word_length and all(
                (c1 == c2 or c2 == "_") and c1 not in st.session_state.excluded_letters for c1, c2 in zip(word, pattern)
            )]

            if possible_words:
                st.markdown("<h4 style='color: #28a745;'>Possible words:</h4>", unsafe_allow_html=True)
                st.write(possible_words)
            else:
                st.markdown("<h4 style='color: #dc3545;'>No possible words found for your input.</h4>", unsafe_allow_html=True)

with col2:
    if st.button("Reset"):
        st.session_state.letter_inputs = [""] * word_length
        st.session_state.excluded_letters = []
        st.session_state.word_length = word_length
        # Clear all inputs manually
        st.experimental_set_query_params()  # Reset query parameters
