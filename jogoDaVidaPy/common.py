#file -- common.py --
from inspect import currentframe
from datetime import datetime
import json
import os

MAX_HP = 10
DEBUG_ENABLED = True
FILE_NAME = "saves.txt"

class prim_opt:
    PASS_TURN = 'P'
    SAVE = 'S'
    EXIT = 'E'
    SAVE_EXIT = '0'
    CONTINUE = 'C'
    ADD_PLAYER = 'A'
    REM_PLAYER = 'R'

    DELETE = 'D'
    LOAD = 'L'
    CREATE = 'C'

def get_linenumber():
    cf = currentframe()
    return cf.f_back.f_lineno

def get_saves():
    try:
        with open(FILE_NAME, 'r+') as json_file:
            data = json.load(json_file)
    except:
        data = {
            "last_save_id": 0,
            "saves": {}
        }
        with open(FILE_NAME, 'w') as outfile:
            json.dump(data, outfile)

    return data

def save_game_to_file(save, new_save_id=None):
    data = get_saves()

    if(new_save_id is not None):
        data["last_save_id"] = new_save_id

    save_id = save["save_id"]
    data["saves"][save_id] = save

    with open(FILE_NAME, 'w') as outfile:
        json.dump(data, outfile)


def date_now():
    now = datetime.now()
    return now.strftime("%d/%m/%Y - %H:%M:%S")

def clear():
    os.system("clear")

def is_integer(n):
    try:
        int(n)
        # return True
    except ValueError:
        return False
    
    return float(n).is_integer()

