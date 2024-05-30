from tqdm import tqdm
import re
new_weirdwords = set()
new_ww_syllables0 = set()
new_ww_syllables1 = set()
new_ww_syllables2 = set()


with open("weirdwords.txt") as f:
    for line in tqdm(f.readlines()):
        match = re.match(r"\('(.*?)', \((.*?)\)\)", line)
        if match:
            words = match.group(1).split('; ')
            pronunciations = [pron.strip().strip('\'\"') for pron in match.group(2).split(', ')]
                      
            for i in range(len(words)):
                try:
                    current_word = words[i]
                    current_pronounciation = pronunciations[i]
                    if (current_pronounciation[0] == " "):
                        current_pronounciation = current_pronounciation[1:]
                    
                    p_replaced = current_pronounciation.replace("*", "?").replace("\"", "?").replace("\'", "?").replace(" ", "?").replace("`", "?").replace(".", "?")
                    p_to_w = p_replaced.replace("?", "").upper()
                    if (current_word == p_to_w):
                        p_splitted = p_replaced.split("?")
                        if (len(p_splitted) == 3):
                            new_weirdwords.add(current_word) 
                        if "(" not in p_splitted[0] and len(p_splitted[0]) != 0:
                            new_ww_syllables0.add(p_splitted[0].upper());
                        if "(" not in p_splitted[1] and len(p_splitted[1]) != 0:
                            new_ww_syllables1.add(p_splitted[1].upper());
                        if "(" not in p_splitted[2] and len(p_splitted[2]) != 0:
                            new_ww_syllables2.add(p_splitted[2].upper());    
                except:
                    continue

print(len(new_weirdwords))

new_weirdwords = sorted(list(new_weirdwords))
with open("cleaned_weirdwords.txt", "w") as f:
    for word in new_weirdwords:
        f.write(str(word) + "\n")
f.close()
        
new_ww_syllables0 = sorted(list(new_ww_syllables0))
with open("syllablesww0.txt", "w") as f:
    for wword in new_ww_syllables0:
        f.write(str(wword) + "\n")
f.close()

new_ww_syllables1 = sorted(list(new_ww_syllables1))
with open("syllablesww1.txt", "w") as f:
    for wword in new_ww_syllables1:
        f.write(str(wword) + "\n")
f.close()

new_ww_syllables2 = sorted(list(new_ww_syllables2))
with open("syllablesww2.txt", "w") as f:
    for wword in new_ww_syllables2:
        f.write(str(wword) + "\n")
f.close()