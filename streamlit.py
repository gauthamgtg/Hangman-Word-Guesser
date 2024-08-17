

# Import necessary libraries
import pdfplumber
import nltk
from nltk.tokenize import word_tokenize
import tkinter as tk
from tkinter import messagebox

# Download NLTK resources if not already downloaded
nltk.download('punkt')
nltk.download('words')

# Path to your uploaded PDF file
file_name = 'dictionary.pdf'  # Replace with the path to your PDF file

# Initialize an empty list to store all words
all_words = []

# Process the PDF in chunks (e.g., 100 pages at a time)
chunk_size = 100

with pdfplumber.open(file_name) as pdf:
    for chunk_start in range(0, len(pdf.pages), chunk_size):
        text_chunk = ""
        for page in pdf.pages[chunk_start:chunk_start + chunk_size]:
            page_text = page.extract_text()
            if page_text:
                text_chunk += page_text
        
        # Tokenize and filter words
        words_list = word_tokenize(text_chunk)
        words_list = [word for word in words_list if word.isalpha()]
        
        # Add the words to the main list
        all_words.extend(words_list)

        # Optional: Save progress after each chunk
        with open('extracted_words.txt', 'a') as f:
            f.write("\n".join(words_list) + "\n")

        print(f"Processed pages {chunk_start} to {chunk_start + chunk_size}")

# Final word count
print(f"Total words extracted: {len(all_words)}")

# Optionally, print a sample of the words
print(all_words[:50])  # Print only the first 50 words for inspection

# Define the word completion model
class WordCompletionModel:
    def __init__(self):
        # Load the NLTK word list and merge with words extracted from the PDF
        self.word_list = nltk.corpus.words.words() + all_words
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

# GUI using tkinter
class WordCompletionApp:
    def __init__(self, root):
        self.model = WordCompletionModel()

        # Set up the main window
        root.title("Word Completion App")

        # Initial input for the word with missing letters
        self.label = tk.Label(root, text="Enter a word with missing letters (use '_' for missing letters):")
        self.label.pack(pady=10)
        
        self.entry = tk.Entry(root, width=30)
        self.entry.pack(pady=10)

        # "Submit" button to display the word in boxes
        self.submit_button = tk.Button(root, text="Submit", command=self.display_word_boxes)
        self.submit_button.pack(pady=10)

        # Frame to hold the letter boxes
        self.box_frame = tk.Frame(root)
        self.box_frame.pack(pady=10)

        # Entry box for letters that should be excluded
        self.excluded_label = tk.Label(root, text="Enter letters that are not in the word:")
        self.excluded_label.pack(pady=10)
        
        self.excluded_entry = tk.Entry(root, width=30)
        self.excluded_entry.pack(pady=10)

        # "Guess" button to show guesses
        self.guess_button = tk.Button(root, text="Guess", command=self.guess_word, state=tk.DISABLED)
        self.guess_button.pack(pady=10)

        # Create a listbox to show the possible completions
        self.result_listbox = tk.Listbox(root, width=50, height=10)
        self.result_listbox.pack(pady=10)

        # "Found" button to stop the process
        self.found_button = tk.Button(root, text="Found", command=self.word_found, state=tk.DISABLED)
        self.found_button.pack(pady=10)

        self.letter_boxes = []
        self.current_word = ""

    def display_word_boxes(self):
        # Clear any previous boxes
        for box in self.letter_boxes:
            box.destroy()

        # Get the word with missing letters from the entry
        incomplete_word = self.entry.get().strip()

        # Ensure valid input
        if not incomplete_word:
            messagebox.showwarning("Input Error", "Please enter a word.")
            return

        # Store the current word
        self.current_word = incomplete_word

        # Create letter boxes
        self.letter_boxes = []
        for i, char in enumerate(incomplete_word):
            if char == '_':
                entry_box = tk.Entry(self.box_frame, width=2, justify='center')
                entry_box.bind("<FocusOut>", self.update_letter_boxes)
            else:
                entry_box = tk.Entry(self.box_frame, width=2, justify='center')
                entry_box.insert(0, char)
                entry_box.config(state='readonly')
            entry_box.grid(row=0, column=i, padx=5)
            self.letter_boxes.append(entry_box)

        # Enable the guess button
        self.guess_button.config(state=tk.NORMAL)

    def update_letter_boxes(self, event=None):
        # Update the word based on the current contents of the boxes
        updated_word = "".join([box.get() if box.get() else "_" for box in self.letter_boxes])
        self.current_word = updated_word

    def guess_word(self):
        # Clear previous results
        self.result_listbox.delete(0, tk.END)

        # Get the excluded letters from the entry box
        excluded_letters = set(self.excluded_entry.get().strip().lower())

        # Get possible word completions
        self.update_letter_boxes()
        possible_words = self.model.complete_word(self.current_word, excluded_letters)

        if possible_words:
            # Display the possible completions in the listbox
            for word in possible_words:
                self.result_listbox.insert(tk.END, word)
        else:
            messagebox.showinfo("No Matches", "No possible words found for your input.")

        # Enable the found button after guessing
        self.found_button.config(state=tk.NORMAL)

    def word_found(self):
        # Ask the user if the word was found
        is_found = messagebox.askyesno("Word Found", "Have you found the word?")
        if not is_found:
            # Ask for another letter if not found
            messagebox.showinfo("Keep Going", "You can enter more letters and guess again.")
        else:
            # Reset everything for a new word
            self.reset_app()

    def reset_app(self):
        self.entry.delete(0, tk.END)
        for box in self.letter_boxes:
            box.destroy()
        self.result_listbox.delete(0, tk.END)
        self.excluded_entry.delete(0, tk.END)
        self.guess_button.config(state=tk.DISABLED)
        self.found_button.config(state=tk.DISABLED)
        self.current_word = ""
        self.letter_boxes = []

if __name__ == "__main__":
    root = tk.Tk()
    app = WordCompletionApp(root)
    root.mainloop()
