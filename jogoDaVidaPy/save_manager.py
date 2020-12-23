#file -- save_manager.py --
import json
from common import *
from beauty_print import *

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

def save_to_file(save, new_save_id=None):
    data = get_saves()

    if(new_save_id is not None):
        data["last_save_id"] = new_save_id

    current_datetime = date_now()

    save_id = save["save_id"]
    save["last_save_date"] = current_datetime
    data["saves"][save_id] = save
    data["saves"][save_id] = save

    with open(FILE_NAME, 'w') as outfile:
        json.dump(data, outfile)

def save_all(saves):
    with open(FILE_NAME, 'w') as outfile:
        json.dump(saves, outfile)

def create_new_save():
    data = get_saves()
    
    clear()

    game_name = input_question("Nome da nova partida: (ENTER para cancelar)\n")

    if(len(game_name) == 0):
        return
    
    data["last_save_id"] += 1

    game_id = data["last_save_id"]

    current_datetime = date_now()

    save = {
        "save_id": game_id,
        "save_name": game_name,
        "players": {},
        "last_id": 0,
        "turn_of": None,
        "out_of_match":{},
        "last_save_date": current_datetime,
        "creation_date": current_datetime
    }

    save_to_file(save, game_id)

    print_sucess(f"Partida \"{game_name}\" criado! Aperte ENTER para continuar.\n")
    cont = input("")

def load_save(save_id=None):

    def valid_save_value(value, size):
        if(not is_integer(value)):
            print_error("Digite um número")
            return False
        
        i = int(value)
        if(i < 1 or i > size):
            print_error(f"Digite um valor entre 1 e {size}")
            return False
        
        return True

    data = get_saves()
    if(save_id is not None):
        save_loaded = data["saves"][save_id].copy()
        return save_loaded
    
    if(len(data["saves"]) == 0):
        print_warning("Não há partidas! Aperte ENTER para voltar e crie uma.")
        input("")
        return None

    saves_id = list(data["saves"].keys())

    clear()
    idx = 0
    print_header("Partidas")
    for key in data["saves"].keys():
        save_name = data["saves"][key]["save_name"]
        print_normal(f"    {idx+1}) {save_name}")

        idx += 1

    while True:
        option = input_question("Digite o número da partida: (ENTER p/ cancelar)\n")
        if(len(option) == 0):
            return None
        if(valid_save_value(option, len(saves_id))):
            break

    choice = data["saves"][saves_id[int(option)-1]]
    choice_id = choice["save_id"]
    # print_normal(f"Você escolheu \"{choice_name}\", pressione ENTER para começar")
    save_loaded = data["saves"][str(choice_id)].copy()
    # cont = input("")
    return save_loaded


def delete_save():
    data = get_saves()
    
    clear()

    while True:
        if(len(data["saves"]) == 0):
            print_warning("Não há partidas salvas! Aperte ENTER para voltar.")
            input("")
            return
        
        print_header("Partidas")
        for key in data["saves"].keys():
            save_name = data["saves"][key]["save_name"]
            save_id = data["saves"][key]["save_id"]
            print_normal(f"    {save_id}) {save_name}")


        game_id = input_question(f"\nCódigo da partida que quer {bcolors.FAIL}Deletar{bcolors.OKBLUE} (ENTER para cancelar): ")

        if(len(game_id) == 0):
            return
        
        try:
            save = data["saves"][game_id]
        except:
            clear()
            print_error(f"Id {game_id} inválido, digite um valor válido.\n")
            continue

        save_name = save["save_name"]
        save_id = str(save["save_id"])

        sure = input_question(f"\nTem certeza que quer deletar a partida \"{save_name}\"? (S/N): ").upper()
        
        clear()
        if(sure == 'S'):
            data["saves"].pop(save_id)
            save_all(data)
            print_sucess(f"Partida \"{save_name}\" deletada!\n")

        else:
            print_normal("Deleção cancelada!\n")
