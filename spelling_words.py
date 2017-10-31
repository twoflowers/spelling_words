import random
import os
import time

words = ['fish', 'wish', 'shop', 'ship', 'rush', 'made', 'name', 'cake', 'late', 'safe']
used = []

random_word = random.choice(words)
while len(words) != len(used):
    os.system('clear')


    if random_word not in used:
        print(random_word)
        used.append(random_word)

        time.sleep(6)
        os.system('clear')
    
        for letters in random_word:
            print(letters)
            time.sleep(1)
        print(random_word)
    
    random_word = random.choice(words)


