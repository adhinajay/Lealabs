# Open the file
f1 = open('adhin','r')

# Read and convert to lowercase
text = f1.read().lower()

# Close the file
f1.close()

# Remove basic punctuation
for ch in ['.', ',', '!', '?', ';', ':', '-', '"', "'"]:
    text = text.replace(ch, '')

# Split into words
words = text.split()

# Count word frequency manually
word_counts ={}

for word in words:
    if word in word_counts:
        word_counts[word] += 1
    else:
        word_counts[word] = 1

# Print word frequencies
for word, count in word_counts.items():
    print(word,':',count)