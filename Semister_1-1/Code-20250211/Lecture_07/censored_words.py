# Original text with sensitive words
text = "This is a bad example of a text with offensive language."

# Words to be censored
censored_words = ["bad", "offensive"]

# Replace each censored word with asterisks
for word in censored_words:
    text = text.replace(word, "*" * len(word))

print("Censored text:", text)
