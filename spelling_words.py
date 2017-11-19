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
import speech_recognition as sr

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

def text_to_speech(word):
    subprocess.call('Say -v Victoria ' + word, shell=True)

def say_word(word):

    text_to_speech(word)

    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)

    # Speech recognition using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("You said: " + r.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    if r.recognize_google(audio).lower().replace(" ", "") == word.lower():
        text_to_speech('Great Job')
    else:
        # we had an error, with either the spellign or something, lets try it again
        say_word(word)



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
                # print(letters)
                time.sleep(1)
            # print(random_word)

        sys.exit()
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
