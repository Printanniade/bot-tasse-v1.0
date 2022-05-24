import json
import numpy as np
import configparser

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')


def computeMessage(message: str):
    # return a list of words contained in the message
    lst_word = json.loads(config['word_sard']['word'])
    return_lst = []
    for index in range(len(lst_word)):
        for word in lst_word[index]:
            if message.find(word) > -1:
                return_lst += [index]
                break

    return return_lst


def advanceState(state: np.ndarray, advancement=None):
    # Advance state of message chat
    shape = state.shape
    if advancement is None:
        advancement = createAdvancement(shape)

    current_state = state[0]
    state = np.matmul(advancement, state)
    return state, current_state


def createAdvancement(shape: int):
    # Create an advancement matrix for state
    advancement = np.zeros((shape,shape))
    for i in range(0, shape - 1):
        advancement[i][i + 1] = 1
    return advancement


def addOccurences(occurence: list, state: np.ndarray):
    # Add occurences to the state matrix

    shape = state.shape
    for i in occurence:
        for j in range(shape[0]):
            state[j][i] += 1

    return state


def createState(message_hold = 15):
    number_word = len(json.loads(config['word_sard']['word']))
    return np.zeros((message_hold, number_word))


def processNewMessage(message: str, state:np.ndarray, advancement: np.ndarray):
    #compute a message, change the state and return the actual state
    lst_index = computeMessage(message)
    state = addOccurences(lst_index, state)
    state, concurrent_state = advanceState(state, advancement)
    return state, concurrent_state



