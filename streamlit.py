import streamlit as st
from english_words import get_english_words_set
from PyDictionary import PyDictionary

# Initialize PyDictionary
dictionary = PyDictionary()

# Set page configuration and title
st.set_page_config(page_title="Hangman Word Guesser", layout="centered")
st.markdown("<h1 style='text-align: center; color: #FF5733;'>Hangman Word Guesser</h1>", unsafe_allow_html=True)

# Sidebar content
with st.sidebar:
    st.markdown("<h2 style='color: #FF5733;'>Hangman Word Guesser</h2>", unsafe_allow_html=True)
    st.image("https://upload.wikimedia.org/wikipedia/commons/4/46/Circle-icons-typography.svg", caption="AI-Powered Word Guesser", use_column_width=True)
    st.write("This Hangman Word Guesser helps you find possible words based on known and excluded letters, along with word details such as meanings, antonyms, and translations.")
    st.markdown("<h3 style='color: #FF5733;'>Built by Gautham Mahadevan</h3>", unsafe_allow_html=True)
    st.write("[GitHub](https://github.com/gauthamgtg)")
    st.write("[Portfolio](https://gauthamgtg.github.io/portfolio/)")
    st.write("[Follow on LinkedIn](https://linkedin.com/in/gautham-mahadevan)")

# Main content
web2lowerset = get_english_words_set(['web2'], lower=True)

# Function to validate excluded letters
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
if 'possible_words' not in st.session_state:
    st.session_state.possible_words = []
if 'show_details' not in st.session_state:
    st.session_state.show_details = False

# Update session state if word length changes
if len(st.session_state.letter_inputs) != word_length:
    st.session_state.letter_inputs = [""] * word_length

# Display input boxes side by side
st.markdown("<h4 style='color: #33CFFF;'>Enter the known letters below:</h4>", unsafe_allow_html=True)
cols = st.columns(word_length)
for i in range(word_length):
    st.session_state.letter_inputs[i] = cols[i].text_input(f"Letter {i+1}", st.session_state.letter_inputs[i], max_chars=1, key=f"letter_{i}").lower()

# User input for excluded letters
st.markdown("<h4 style='color: #33CFFF;'>Enter letters that are not in the word:</h4>", unsafe_allow_html=True)
excluded_letters_input = st.text_input("Excluded letters (separated by commas):", value=", ".join(st.session_state.excluded_letters)).lower()
st.session_state.excluded_letters = [letter for letter in excluded_letters_input if letter.isalpha()]

# Check function to find possible words
col1, col2 = st.columns([4, 1])
with col1:
    if st.button("Check"):
        if validate_excluded_letters(st.session_state.letter_inputs, st.session_state.excluded_letters):
            pattern = "".join([letter if letter else "_" for letter in st.session_state.letter_inputs])
            st.session_state.possible_words = [
                word for word in web2lowerset if len(word) == word_length and all(
                    (c1 == c2 or c2 == "_") and c1 not in st.session_state.excluded_letters for c1, c2 in zip(word, pattern)
                )
            ]
            st.session_state.show_details = False

with col2:
    if st.button("Reset"):
        st.session_state.letter_inputs = [""] * word_length
        st.session_state.excluded_letters = []
        st.session_state.possible_words = []
        st.session_state.show_details = False

# Display possible words
if st.session_state.possible_words:
    st.markdown("<h4 style='color: #28a745;'>Possible words:</h4>", unsafe_allow_html=True)
    st.write(", ".join(st.session_state.possible_words))

    # Button to show word details
    if st.button("Show Word Details"):
        st.session_state.show_details = True

# Display word details in a popup-like section
if st.session_state.show_details:
    st.markdown("<h4 style='color: #FF5733;'>Word Details:</h4>", unsafe_allow_html=True)
    
    for word in st.session_state.possible_words:
        st.markdown(f"#### Details for '{word}':")
        
        # Get and display meaning
        meaning = dictionary.meaning(word)
        if meaning:
            st.write("**Meaning:**")
            for part_of_speech, definitions in meaning.items():
                st.write(f"**{part_of_speech.capitalize()}:**")
                for definition in definitions:
                    st.write(f" - {definition}")
        else:
            st.write("No meaning found.")
        
        # Get and display antonyms
        antonyms = dictionary.antonym(word)
        if antonyms:
            st.write("**Opposites (Antonyms):**")
            st.write(", ".join(antonyms))
        else:
            st.write("No antonyms found.")
        
        # Get and display translation
        st.write("**Translation:**")
        target_language = st.selectbox(f"Select target language for '{word}':", [
            'French', 'German', 'Italian', 'Spanish', 'Portuguese', 'Dutch', 'Chinese', 'Japanese', 'Korean', 'Russian', 'Arabic'
        ], key=f"lang_{word}")
        
        language_codes = {
            'French': 'fr',
            'German': 'de',
            'Italian': 'it',
            'Spanish': 'es',
            'Portuguese': 'pt',
            'Dutch': 'nl',
            'Chinese': 'zh',
            'Japanese': 'ja',
            'Korean': 'ko',
            'Russian': 'ru',
            'Arabic': 'ar'
        }
        
        if target_language:
            translation = dictionary.translate(word, language_codes[target_language])
            if translation:
                st.write(f"**{target_language} Translation:** {translation}")
            else:
                st.write("No translation found.")
