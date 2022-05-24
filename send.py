import json
import random
import time

import numpy as np
import configparser
from chat import createState

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')


def question():
    lst_question = json.loads(config['question_sard']['question'])
    question = random.choice(lst_question)
    return question


def random_emote():
    lst_emote = json.loads(config['emote_sard']['emote'])
    emote = random.choice(lst_emote)
    return emote


def emoji(coefficient: list[int], message):
    k = 0
    for i in range(len(coefficient)):
        control = random.randint(0, 100)
        if control < coefficient[i]:
            message += " " + random_emote()
            k += 1
        else:
            break
    k += 1

    if k == len(coefficient):
        control = random.randint(0, 100)
        while control < coefficient[-1]:
            message += " " + random_emote()
            control = random.randint(0, 100)
    return message


def word_to_message(word):
    lst_phrase = json.loads(config['phrase_sard'][word])
    phrase = random.choice(lst_phrase)
    return phrase


def send(state, current_state, global_timer: float, threshold: int, timer_message: int, timer_question: int, coefficient):
    lst_word = json.loads(config['word_sard']['word'])
    words = []
    for i in range(len(current_state)):
        if current_state[i] >= threshold:
            words += [lst_word[i][0]]

    trigger_word = None
    if len(words) > 0:
        trigger_word = random.choice(words)

    actual_time = time.time()
    elapsed_time = actual_time - global_timer

    if elapsed_time > timer_message and trigger_word is not None:
        state = createState(state.shape[0])
        global_timer = time.time()
        mess = emoji(coefficient, word_to_message(trigger_word) )
        return mess, state, global_timer

    elif elapsed_time > timer_question:
        global_timer = time.time()
        message = question()
        question_emojized = emoji(coefficient, message)
        return question_emojized, state, global_timer

    else:
        return None, state, global_timer
