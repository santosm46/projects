#file -- beauty_print.py --
import json

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_normal(message, end='\n'):
    print(message, end=end)

def print_warning(message, end='\n'):
    print(f"{bcolors.WARNING}{message}{bcolors.ENDC}", end=end)

def print_debug(message, fname=None, fline=None, enabled=True, pause=False, end='\n'):
    meta=""
    if enabled:
        if fname is not None:
            meta = meta + f" {fname}.py" # file name
        if fline is not None:
            meta = meta + f":{fline}" # file line
        print(f"{bcolors.WARNING}Debug{meta}: {bcolors.ENDC}{message}{bcolors.ENDC}", end=end)
        if pause:
            input("")

def debug_error(message, fname=None, fline=None, enabled=True, pause=False, end='\n'):
    meta=""
    if enabled:
        if fname is not None:
            meta = meta + f" file {fname}.py" # file name
        if fline is not None:
            meta = meta + f":{fline}" # file line
        print(f"{bcolors.WARNING}Debug{meta}: {bcolors.FAIL}{message}{bcolors.ENDC}", end=end)
        if pause:
            input("")

def print_header(message, end='\n'):
    print(f"{bcolors.HEADER}{message}{bcolors.ENDC}", end=end)

def print_error(message, end='\n'):
    print(f"{bcolors.FAIL}{message}{bcolors.ENDC}", end=end)

def print_sucess(message, end='\n'):
    print(f"{bcolors.OKGREEN}{message}{bcolors.ENDC}", end=end)

def input_question(message):
    print(f"{bcolors.OKBLUE}{message}{bcolors.ENDC}", end='')
    value = input("")
    return value

def print_saves(saves):
    print(json.dumps(saves, indent=4))
    # print(json.dumps(saves["saves"]["1"], indent=4))

def print_number_list(values: list, title: str, layed=False):
    print_header(title)
    output = ''
    for i in range(len(values)):
        output = output + f"{bcolors.HEADER}{i+1}) {bcolors.WARNING}{values[i]}{bcolors.ENDC}" + (". " if layed else "\n")
    print_normal(output)

