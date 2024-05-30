from tqdm import tqdm

file1 = "syllables3words0.txt"
file2 = "syllables3words1.txt"
file3 = "syllables3words2.txt"
file4 = "semicwords.txt"
file5 = "syllablesww0.txt"
file6 = "syllablesww1.txt"
file7 = "syllablesww2.txt"

syllables3words0 = set()
syllables3words1 = set()
syllables3words2 = set()
semicwords = list()
syllablesww0 = set()
syllablesww1 = set()
syllablesww2 = set()

with open(file1) as f:
    for line in tqdm(f.readlines()):
        syllables3words0.add(line.strip())

with open(file2) as f:
    for line in tqdm(f.readlines()):
        syllables3words1.add(line.strip())

with open(file3) as f:
    for line in tqdm(f.readlines()):
        syllables3words2.add(line.strip())
        
with open(file4) as f:
    for line in tqdm(f.readlines()):
        semicwords.append(line.strip())
        
with open(file5) as f:
    for line in tqdm(f.readlines()):
        syllablesww0.add(line.strip())

with open(file6) as f:
    for line in tqdm(f.readlines()):
        syllablesww1.add(line.strip())

with open(file7) as f:
    for line in tqdm(f.readlines()):
        syllablesww2.add(line.strip())

print(len(syllables3words0) + len(syllables3words1) + len(syllables3words2) + len(semicwords) + len(syllablesww0) + len(syllablesww1) + len(syllablesww2))

all_syllables0 = syllables3words0.union(syllablesww0)
all_syllables0.add(semicwords[0])

all_syllables1 = syllables3words1.union(syllablesww1)
all_syllables1.add(semicwords[1])

all_syllables2 = syllables3words2.union(syllablesww2)
all_syllables2.add(semicwords[2])


all_syllables0 = sorted(list(all_syllables0))
with open("all_syllables0.txt", "w") as f:
    for word in all_syllables0:
        f.write(str(word) + "\n")
f.close()

all_syllables1 = sorted(list(all_syllables1))
with open("all_syllables1.txt", "w") as f:
    for word in all_syllables1:
        f.write(str(word) + "\n")
f.close()

all_syllables2 = sorted(list(all_syllables2))
with open("all_syllables2.txt", "w") as f:
    for word in all_syllables2:
        f.write(str(word) + "\n")
f.close()