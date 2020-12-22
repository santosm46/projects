from typing import Optional
from common import *
from beauty_print import *
from game import Game
from player import PlayerHandler

import json
import os
    

def create_new_game():
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
        "last_open": current_datetime,
        "creation_date": current_datetime
    }

    save_game_to_file(save, game_id)

    print_sucess(f"Partida \"{game_name}\" criado! Aperte ENTER para começar.\n")
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
    choice_name = choice["save_name"]
    choice_id = choice["save_id"]
    print_normal(f"Você escolheu \"{choice_name}\", pressione ENTER para começar")
    save_loaded = data["saves"][str(choice_id)].copy()
    cont = input("")
    return save_loaded

def start_game(save):
    save_name = save["save_name"]

    game = Game(save)
    game.setup(PlayerHandler())
    game.start()

    while(True):
        clear()

        print_header(f"Menu da partida: {save_name}\n")
    
        print_normal(f"\t{prim_opt.CONTINUE}) Continuar partida")
        print_normal(f"\t{prim_opt.ADD_PLAYER}) Adicionar jogadores na partida")
        print_normal(f"\t{prim_opt.REM_PLAYER}) Remover jogadores da partida")
        print_normal(f"\t{prim_opt.SAVE_EXIT}) Salvar e voltar para menu inicial")

        option = input_question("\nOpção: ").upper()

        if(option == prim_opt.CONTINUE):
            game.start()
        elif(option == prim_opt.ADD_PLAYER):
            game.player_handler.create_players()
        elif(option == prim_opt.REM_PLAYER):
            input("main.py fazer remover player")
        elif(option == prim_opt.SAVE_EXIT):
            game.save()
            game.stop()
            return
        else:
            print_error(f"Opção ({option}) inválida! pressione ENTER")
            cont = input("")




    


def run():
    os.system("clear")


    while(True):
        clear()
        print_header("Menu inicial\n")
        print_normal(f"\t{prim_opt.CREATE}) Criar novo jogo")
        print_normal(f"\t{prim_opt.LOAD}) Carregar um jogo")
        print_normal(f"\t{prim_opt.DELETE}) Deletar um jogo")

        print_normal(f"\n\t{prim_opt.EXIT}) Fechar jogo")

        option = input_question("Opção: ").upper()

        if(option == prim_opt.CREATE):
            create_new_game()
        elif(option == prim_opt.LOAD):
            save = load_save()
            start_game(save)
        elif(option == prim_opt.DELETE):
            input("main.py fazer deletar jogo")
        elif(option == prim_opt.EXIT):
            print_sucess("Fechando jogo...")
            break # ou return
        else:
            print_error(f"Opção ({option}) inválida! pressione ENTER")
            cont = input("")


    





def change_turn():
    pass



def is_turn_of(player_id):
    return 






# def debug_state():
#     print("Players:")
#     for j in game["players"]:
#         print(j)

if __name__ == '__main__':
    run()