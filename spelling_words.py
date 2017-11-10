# coding=utf-8
import random
import os
import time
import sqlite3
import sys
import argparse
import json
from os.path import join, dirname
from watson_developer_cloud import TextToSpeechV1
import subprocess
import requests
# from playsound import playsound
from pygame import mixer

base_words = ['fish', 'wish', 'shop', 'ship', 'rush', 'made', 'name', 'cake', 'late', 'safe']
used = []

sqlite_file = 'database/words.db'

def initiate(sql_file,base_words):
    conn = sqlite3.connect(sql_file)
    c = conn.cursor()
    c.execute("""CREATE TABLE
                 IF NOT EXISTS words (
                    id integer PRIMARY KEY,
                    name text NOT NULL
                )""")
    conn.commit()

    for word in base_words:
        c.execute("insert into words (name) values ('%s')" % word )
        conn.commit()
    conn.close();

def execute_sql(sql_statement):
    sqlite_file = 'database/words.db'

    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute(sql_statement)
    rows  = c.fetchall()
    conn.commit()

    return rows

def say_word(word):

    # exec('Say ' + word)
    subprocess.call('Say ' + word, shell=True)


    # headers = {
    #     'Content-Type': 'application/json',
    #     'Accept': 'audio/wav',
    # }
    #
    # params = (
    #     ('voice', 'en-US_AllisonVoice'),
    # )
    #
    # data = '{"text":"%s"}' % (word)
    #
    #
    # with open('resources/'+word+'.wav', mode='wb+') as audio_file:
    #     response = requests.post('https://stream.watsonplatform.net/text-to-speech/api/v1/synthesize', stream=True, headers=headers, params=params, data=data, auth=('4ef7923c-a9b1-43d6-b466-95f4bb32708c', 'q4BjDwfaeCOj'))
    #     audio_file.write(response.content)



    # mixer.init() #you must initialize the mixer
    # alert=mixer.Sound('resources/'+word+'.wav')
    # alert.play()
    # playsound('resources/'+word+'.wav')
    # subprocess.call(["afplay", 'resources/'+word+'.wav'])

def add_word(word):
    sql = "insert into words (name) values ('%s')" % (word)
    execute_sql(sql)
    return True

def the_game():

    words = execute_sql("select name from words")
    random_word = random.choice(words)[0]
    used = []
    while len(words) != len(used):
        os.system('clear')


        if random_word not in used:
            print(random_word)
            used.append(random_word)
            say_word(random_word)
            time.sleep(3)
            os.system('clear')

            for letters in random_word:
                print(letters)
                time.sleep(1)
            print(random_word)

        random_word = random.choice(words)[0]



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This is a spelling game.')
    parser.add_argument('-a', '--add', action="store", dest='add_word', default=False)
    parser.add_argument('-i', '--initiate', action="store_true", default=False)
    parser.add_argument('-p', '--play', action="store_true", default=True)
    args = parser.parse_args()


    if args.add_word:
        print("going to add a word %s") % (args.add_word)
        if add_word(args.add_word):
            print('word has been added')

            sys.exit()
        else:
            print('there was a small problem')
            sys.exit()
    if args.initiate:
        print('creating the db')
        #    initiate(sqlite_file, base_words)
        sys.exit()
    else:
        the_game()
