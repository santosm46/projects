#file -- common.py --
from inspect import currentframe
from datetime import datetime
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
    DEL_PLAYER = 'D'

    DELETE = 'D'
    LOAD = 'L'
    CREATE = 'C'

def get_linenumber():
    cf = currentframe()
    return cf.f_back.f_lineno

def date_now():
    now = datetime.now()
    return now.strftime("%d/%m/%Y - %H:%M:%S")

def clear():
    os.system("clear")

def is_integer(n):
    try:
        int(n)
    except ValueError:
        return False
    
    return float(n).is_integer()



