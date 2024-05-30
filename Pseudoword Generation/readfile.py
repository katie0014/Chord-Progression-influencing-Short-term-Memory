from tqdm import tqdm
current_word = ""
words = set()
weirdwords = set()
semic2syllablewords = set()
words_syllables0 = set()
words_syllables1 = set()
words_syllables2 = set()
gutenbergfile = "C:\\Users\\katie\\Downloads\\Katie\\School\\TJHSST\\Senior2023-2024\\NeuroResLocklear\\projectstuff\\actualcode\\dataset_and_code_v2\\gutenbergdictionary.txt"

# with open(gutenbergfile) as f:
with open("gutenbergdictionary.txt") as f:
    for line in tqdm(f.readlines()):
        split = line.strip().split(",")
        saying = split[0]
        if ("*" in saying) and (saying.count("*") + saying.count("\"") + saying.count("\'") + saying.count(" ") + saying.count("`") == 1) and current_word.isupper():
            if (";" in current_word):
                lsplit = current_word.split("; ")
                if (lsplit[0].isupper()):
                    newsaying = saying.strip().replace("*", "?").replace("\"", "?").replace("\'", "?").replace(" ", "?").replace("`", "?")
                    anothersplit = newsaying.split("?")
                    if (len(anothersplit[-1]) != 0):
                        semic2syllablewords.add((current_word.strip(), tuple(split)))
        if ("*" in saying) and (saying.count("*") + saying.count("\"") + saying.count("\'") + saying.count(" ") + saying.count("`") == 2) and current_word.isupper():
            if (";" in current_word):
                lsplit = current_word.split("; ")
                if (lsplit[0].isupper()):
                    newsaying = saying.strip().replace("*", "?").replace("\"", "?").replace("\'", "?").replace(" ", "?").replace("`", "?")
                    anothersplit = newsaying.split("?")
                    if (len(anothersplit[-1]) != 0):
                        weirdwords.add((current_word.strip(), tuple(split)))
            else:
                newsaying = saying.strip().replace("*", "?").replace("\"", "?").replace("\'", "?").replace(" ", "?").replace("`", "?").replace(".", "?")
                anothersplit = newsaying.split("?")
                if (len(anothersplit[-1]) != 0):
                    words.add(current_word.strip())
                    if "(" not in anothersplit[0] and len(anothersplit[0]) != 0:
                        words_syllables0.add(anothersplit[0].upper());
                    if "(" not in anothersplit[1] and len(anothersplit[1]) != 0:
                        words_syllables1.add(anothersplit[1].upper());
                    if "(" not in anothersplit[2] and len(anothersplit[2]) != 0:
                        words_syllables2.add(anothersplit[2].upper());                    
        current_word = line
f.close();

print(len(words))
print(len(weirdwords))
print(len(semic2syllablewords))

words = sorted(list(words))
with open("words3syllable.txt", "w") as f:
    for word in words:
        f.write(word + "\n")
f.close()

weirdwords = sorted(list(weirdwords))
with open("weirdwords.txt", "w") as f:
    for wword in weirdwords:
        f.write(str(wword) + "\n")
f.close()

semic2syllablewords = sorted(list(semic2syllablewords))
with open("semicwords2.txt", "w") as f:
    for wword in semic2syllablewords:
        f.write(str(wword) + "\n")
f.close()


#----------------------------------------------------------------------------

words_syllables0 = sorted(list(words_syllables0))
with open("syllables3words0.txt", "w") as f:
    for wword in words_syllables0:
        f.write(str(wword) + "\n")
f.close()

words_syllables1 = sorted(list(words_syllables1))
with open("syllables3words1.txt", "w") as f:
    for wword in words_syllables1:
        f.write(str(wword) + "\n")
f.close()

words_syllables2 = sorted(list(words_syllables2))
with open("syllables3words2.txt", "w") as f:
    for wword in words_syllables2:
        f.write(str(wword) + "\n")
f.close()