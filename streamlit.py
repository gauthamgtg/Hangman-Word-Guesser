import streamlit as st
from english_words import get_english_words_set
from PyDictionary import PyDictionary
import streamlit as st
import streamlit.components.v1 as components

# Set page configuration and title
st.set_page_config(page_title="Hangman Word Guesser", layout="centered")

# Inject PostHog analytics script
posthog_script = """
<!-- PostHog Analytics Script -->
<script>
    !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.async=!0,p.src=s.api_host.replace(".i.posthog.com","-assets.i.posthog.com")+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="init push capture register register_once register_for_session unregister unregister_for_session getFeatureFlag getFeatureFlagPayload isFeatureEnabled reloadFeatureFlags updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures on onFeatureFlags onSessionId getSurveys getActiveMatchingSurveys renderSurvey canRenderSurvey getNextSurveyStep identify setPersonProperties group resetGroups setPersonPropertiesForFlags resetPersonPropertiesForFlags setGroupPropertiesForFlags resetGroupPropertiesForFlags reset get_distinct_id getGroups get_session_id get_session_replay_url alias set_config startSessionRecording stopSessionRecording sessionRecordingStarted loadToolbar get_property getSessionProperty createPersonProfile opt_in_capturing opt_out_capturing has_opted_in_capturing has_opted_out_capturing clear_opt_in_out_capturing debug".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);
    posthog.init('phc_Yx0upHWc7VNREvkKArmdSVQ1L8o6llm3nf5FHHVYWyV',{api_host:'https://us.i.posthog.com', person_profiles: 'identified_only' // or 'always' to create profiles for anonymous users as well
        })
</script>
"""

# Display the PostHog script in the Streamlit app
components.html(posthog_script, height=0, width=0)

# Initialize PyDictionary
dictionary = PyDictionary()

# Set page configuration and title
st.markdown("<h1 style='text-align: center; color: #FF5733;'>Hangman Word Guesser</h1>", unsafe_allow_html=True)

with st.sidebar:
    # Title in sidebar
    st.markdown("<h1 style='text-align: center;color: #FF5733;'>Hangman Word Guesser</h1>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/4/46/Circle-icons-typography.svg" 
                 style="width: 50%;">
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # App description
    st.write("This Hangman Word Guesser helps you find possible words based on known and excluded letters, along with word details such as meanings, antonyms, and translations. It's a useful tool for word games and language learning.")
    
    # Tutorial section
    st.markdown("<h4 style='color: #33CFFF;'>How to Use the App:</h4>", unsafe_allow_html=True)
    st.write("""
    1. **Set the Word Length:** Use the slider to choose the number of letters in the word.
    2. **Enter Known Letters:** Fill in the letters you know in the word. Leave empty spaces for unknown letters.
    3. **Exclude Letters:** Input any letters that are definitely not in the word (e.g., letters guessed incorrectly).
    4. **Click 'Check':** The app will generate a list of possible words based on your inputs.
    5. **View Word Details:** Click on any word to see its meaning, antonyms, and translation options.
    6. **Reset the App:** Use the 'Reset' button to clear your inputs and start a new word search.
    """)
    
    # Credits
    st.markdown("<h3 style='color: #FF5733;'>Built by Gautham Mahadevan</h3>", unsafe_allow_html=True)
    
    st.markdown(
            """
            <div style="display: flex; align-items: center;">
                <p style="margin: 0;">GitHub: </p>
                <a href='https://github.com/gauthamgtg' target='_blank' style="margin-left: 5px;">
                    <img src='https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg' width='30' alt='GitHub'>
                </a>
            </div>
            <br>
            """,
            unsafe_allow_html=True
        )
        
    st.markdown(
        """
        <div style="display: flex; align-items: center;">
            <p style="margin: 0;">Portfolio: </p>
            <a href='https://gauthamgtg.github.io/portfolio/' target='_blank' style="margin-left: 5px;">
                <img src='https://upload.wikimedia.org/wikipedia/commons/6/69/Deepin_Icon_Theme_%E2%80%93_dde-file-manager_%284%29.svg' width='30' alt='Projects'>
            </a>
        </div>
        <br>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        """
        <div style="display: flex; align-items: center;">
            <p style="margin: 0;">For feedbacks, hit me up on LinkedIn: </p>
            <a href='https://linkedin.com/in/gautham-mahadevan' target='_blank' style="margin-left: 5px;">
                <img src='https://upload.wikimedia.org/wikipedia/commons/8/81/LinkedIn_icon.svg' width='30' alt='LinkedIn'>
            </a>
        </div>
        <br>
        """,
        unsafe_allow_html=True
    )

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
if 'selected_word' not in st.session_state:
    st.session_state.selected_word = ""

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
            st.session_state.selected_word = ""

with col2:
    if st.button("Reset"):
        st.session_state.letter_inputs = [""] * word_length
        st.session_state.excluded_letters = []
        st.session_state.possible_words = []
        st.session_state.selected_word = ""

# Display possible words as pill boxes side by side
if st.session_state.possible_words:
    st.markdown("<h4 style='color: #28a745;'>Possible words: <span style='color: #FF5733;'>Click the word to see the word details</span></h4>", unsafe_allow_html=True)
    num_words = len(st.session_state.possible_words)
    
    # Create a horizontal layout using columns
    cols = st.columns(min(num_words, 5))  # Adjust the number of columns if needed
    for i, word in enumerate(st.session_state.possible_words):
        with cols[i % len(cols)]:  # Distribute words across the available columns
            if st.button(word, key=f"word_{i}"):
                st.session_state.selected_word = word

# Display word details for the selected word
if st.session_state.selected_word:
    st.markdown(f"### Details for the word '{st.session_state.selected_word}':")
    
    # Get and display meaning
    meaning = dictionary.meaning(st.session_state.selected_word)
    if meaning:
        st.write("**Meaning:**")
        for part_of_speech, definitions in meaning.items():
            st.write(f"**{part_of_speech.capitalize()}:**")
            for definition in definitions:
                st.write(f" - {definition}")
    else:
        st.write("No meaning found.")
    
    # Get and display antonyms
    antonyms = dictionary.antonym(st.session_state.selected_word)
    if antonyms:
        st.write("**Opposites (Antonyms):**")
        st.write(", ".join(antonyms))
    else:
        st.write("No antonyms found.")
    
    # Get and display translation
    st.write("**Translation:**")
    target_language = st.selectbox("Select target language:", [
        'French', 'German', 'Italian', 'Spanish', 'Portuguese', 'Dutch', 'Chinese', 'Japanese', 'Korean', 'Russian', 'Arabic'
    ])
    
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
        translation = dictionary.translate(st.session_state.selected_word, language_codes[target_language])
        if translation:
            st.write(f"**{target_language} Translation:** {translation}")
        else:
            st.write("No translation found.")
