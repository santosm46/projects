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

def str_to_file_format(text: str) -> str:
    import unicodedata 

    text = text.strip()
    text = " ".join(text.split()).replace(" ","_")
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore').decode("utf-8")
    text = f"{text}.txt"

    return text

def get_saves_list() -> list:

    def valid_file(name):
        return ".txt" in name and len(name) > 4 and name[-4:] == ".txt"

    saves_names : list = os.listdir("./saves")
    saves_names = list(filter(valid_file, saves_names))
    
    return(saves_names)

