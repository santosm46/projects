#file -- common.py --
from inspect import currentframe
from datetime import datetime
import os
from utils.beauty_print import print_error
from pathlib import Path

# MAX_HP = 10
DEBUG_ENABLED = True
FILE_NAME = "saves.txt"
TEST_FILE_NAME = "test.txt"
GAME_VERSION = "1.0.0"
DATA_PATH = 'data/'
NAMES_FILE = 'names.txt'
ERRORS_PATH = 'errors/'
ERRORS_FILE = '_errors.txt'
GOVERNMENT = "government"
MOCK_ID = "mock_id"


class prim_opt:
    PASS_TURN = 'P'
    SAVE = 'S'
    EXIT = 'F'
    SAVE_EXIT = '0'
    CONTINUE = 'C'
    ADD_PLAYER = 'A'
    REM_PLAYER = 'R'
    DEL_PLAYER = 'D'
    ROLL_DICE = ''
    RESETE_TEST = 'RT'

    DELETE = 'D'
    LOAD = 'C'
    CREATE = 'N'

class emotions:
    NEUTRAL = "neutral"
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    SCARED = "scared"
    WORRIED = "worried"

class modes:
    ON_BOARD = "on_board"
    ON_BUILDING = "on_building"

class stats:
    QI = 20
    MAX_HP = 5



def line():
    cf = currentframe()
    return cf.f_back.f_lineno

def date_now():
    now = datetime.now()
    return now.strftime("%d/%m/%Y - %H:%M:%S")

def log_error(error, file, line=''):
    date = datetime.today().strftime('%Y-%m-%d')
    time = datetime.today().strftime("%H:%M:%S")
    error_to_save = f"[{time}] Error at: {file}.py:{line} Message: {error}\n"
    file_name = f"{date}{ERRORS_FILE}"
    # file name format: 20/12/30_errors.txt
    path = f"{DATA_PATH}{ERRORS_PATH}"
    Path(path).mkdir(parents=True, exist_ok=True)
    f = open(f"{path}{file_name}", "a")
    f.write(error_to_save)
    f.close()
    


def clear():
    # pass
    os.system("clear -x")

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



def random_name():
    import random

    name = ''

    def rand_char(text):
        # print(text)
        return text[random.randrange(len(text))]

    vogals = "aeiou"
    consonants = "bcdfghjklmnpqrstvxz"

    dobleCon = {'nt': 57, 'tr': 18, 'nh': 58, 'rg': 9, 'rs': 11, 'nd': 19, 'sc': 27, 'cr': 23, 'sp': 10, 'st': 17, 'cn': 22, 'ch': 26, 'pr': 20, 'bj': 6, 'mb': 17, 'lh': 33, 'fl': 1, 'rt': 43, 'mp': 22, 'rp': 1, 'rr': 2, 'rm': 3, 'ss': 13, 'nv': 3, 'lm': 2, 'ns': 7, 'th': 3, 'br': 8, 'lg': 17, 'rd': 3, 'nc': 19, 'sm': 2, 'cl': 1, 'gr': 2, 'xp': 7, 'pl': 4, 'lv': 1, 'fr': 1, 'nq': 1, 'ng': 3, 'nf': 1, 'bs': 1, 'rv': 1, 'lt': 1, 'sf': 1, 'lq': 1, 'vr': 1, 'dr': 1, 'dy': 1, 'yl': 1, 'll': 1}
    dobleVog = {'ia': 7, 'au': 24, 'ea': 24, 'ua': 45, 'ei': 8, 'ai': 7, 'io': 4, 'ui': 8, 'ue': 5, 'ou': 2, 'ie': 6, 'oi': 1, 'ao': 1, 'eu': 1}

    doble_con_list = []
    doble_vog_list = []

    for k, v in dobleCon.items():
        # print(f"{k},{v}")
        for i in range(v):
            doble_con_list.append(str(k))
    

    for k, v in dobleVog.items():
        for i in range(v):
            doble_vog_list.append(str(k))
    

    num_sil = random.randrange(2)+2

    if(random.randrange(100) < 22):
        name = rand_char(vogals)

    
    for i in range(num_sil):
        if(random.randrange(100) < 20 and i != 0):
            name += rand_char(doble_con_list)
        else:
            name += rand_char(consonants)
        if(random.randrange(100) < 20):
            name += rand_char(doble_vog_list)
        else:
            name += rand_char(vogals)

    return name.capitalize()


def prepare_data(fac, file_name):
    save = fac.get_instance("SaveManager")
    data = fac.get_instance("DataStructure")
    lido = save.get_save_by_filename(file_name)
    data.setup(lido)
    event = fac.get_instance("Event")
    event.setup()

def procura():
    tudo = """texto aqui"""


    lista = tudo.split()

    for i in range(len(lista)):
        lista[i] = str_to_file_format(lista[i].lower()).replace(".txt",'')

    def filtrar(palavra: str):
        if(len(palavra) < 4):
            return False
        
        if(not palavra.isalpha()):
            return False
        
        return True

    lista = list(filter(filtrar, lista))

    validos = {}

    vog = "aeiou"
    for i in range(len(lista)):
        for j in range(len(lista[i])-2):
            p = lista[i][j:j+2]
            if(p[0] in vog and p[1] in vog):
                if(p not in validos):
                    validos[p] = 0
                validos[p] += 1

    # a = "asd"

    


    # print(list(validos.keys()))
    print(validos)


def valid_number(value, min_val, max_val):
        if(not is_integer(value)):
            print_error("Digite um número")
            return False
        
        i = int(value)
        if(i < min_val or i > max_val):
            print_error(f"Digite um valor entre 1 e {max_val}")
            return False
        
        return True

# def print_list()

def replacer(s, newstring, index, nofail=False):
    # raise an error if index is outside of the string
    if not nofail and index not in range(len(s)):
        raise ValueError("index outside given string")

    # if not erroring, but the index is still not in the correct range..
    if index < 0:  # add it to the beginning
        return newstring + s
    if index > len(s):  # add it to the end
        return s + newstring

    # insert the new string between "slices" of the original
    return s[:index] + newstring + s[index + 1:]

