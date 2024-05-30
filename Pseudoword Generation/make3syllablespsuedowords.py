import random

filename0 = "all_syllables0.txt"
filename1 = "all_syllables1.txt"
filename2 = "all_syllables2.txt"

all_syllables0 = list()
all_syllables1 = list()
all_syllables2 = list()
new_words = set()


with open(filename0) as f:
    for line in f.readlines():
        all_syllables0.append(line.strip())
        
with open(filename1) as f:
    for line in f.readlines():
        all_syllables1.append(line.strip())

with open(filename2) as f:
    for line in f.readlines():
        all_syllables2.append(line.strip())
        
while len(new_words) < 150:
    syllable0 = random.sample(all_syllables0, 1)[0]
    syllable1 = random.sample(all_syllables1, 1)[0]
    syllable2 = random.sample(all_syllables2, 1)[0]

    new_word = syllable0 + syllable1 + syllable2
    new_words.add(new_word)

new_words = sorted(list(new_words))
with open("pseudowords3syllables.txt", "w") as f:
    for word in new_words:
        f.write(str(word) + "\n")
f.close()