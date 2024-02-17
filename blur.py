# Load the bad words list
with open("bad.txt", "r") as f:
    bad_words = [line.strip() for line in f.readlines()]


def replace_bad_words(text):
    # Make the text lower case for comparison
    lower_text = text.lower()
    # Replace bad words
    for bad_word in bad_words:
        if bad_word in lower_text:
            text = text.replace(bad_word, '*' * len(bad_word))
    return text


