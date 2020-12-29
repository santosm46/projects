from Player import Player
from common import *
from beauty_print import *

from Instanciator import Instanciator
from SaveManager import SaveManager
from GameManager import GameManager


def start_game(save):
    factory : Instanciator = Instanciator()

    game : GameManager = factory.get_instance("GameManager")
    
    game.setup(save)
    game.start()
    # fix tal dar setup() em DataStructure e Category

    while(True):
        clear()
        players_names = ", ".join(game.get_players_list())
        print_header(f"Menu da partida: {game.get_save_name()} \nJogadores: {players_names} \n")
    
        print_normal(f"\t{prim_opt.CONTINUE}) Continuar partida")
        print_normal(f"\t{prim_opt.ADD_PLAYER}) Adicionar jogadores na partida")
        print_normal(f"\t{prim_opt.REM_PLAYER}) Remover jogador da partida")
        print_normal(f"\t{prim_opt.DEL_PLAYER}) Deletar jogador fora da partida")
        print_normal(f"\t{prim_opt.SAVE_EXIT}) Salvar e voltar para menu inicial")

        option = input_question("\nOpção: ").upper()

        if(option == prim_opt.CONTINUE):
            game.start()
        elif(option == prim_opt.ADD_PLAYER):
            game.player_im.create_players()
        elif(option == prim_opt.REM_PLAYER):
            game.player_im.remove_players()
        elif(option == prim_opt.DEL_PLAYER):
            game.player_oom.delete_players()
        elif(option == prim_opt.SAVE_EXIT):
            game.save()
            game.stop()
            return
        else:
            print_error(f"Opção ({option}) inválida! pressione ENTER")
            cont = input("")


def create_new_game():
    factory : Instanciator = Instanciator()
    save_manager : SaveManager = factory.get_instance("SaveManager")
    save_manager.create_new_save()

def continue_game():
    factory : Instanciator = Instanciator()
    save_manager : SaveManager = factory.get_instance("SaveManager")
    save = save_manager.load_save()
    if save is not None:
        start_game(save)

def resete_test():
    factory : Instanciator = Instanciator()
    save_manager : SaveManager = factory.get_instance("SaveManager")
    save_manager.delete_save(TEST_FILE_NAME)
    save_manager.create_new_save(TEST_FILE_NAME)
    prepare_data(factory, TEST_FILE_NAME)
    player : Player = save_manager.get("Player")
    player.create_players_mock()

def delete_game():
    # factory : Instanciator = Instanciator()
    save_manager : SaveManager = SaveManager()
    save_manager.delete_save()

def exit_game():
    print_sucess("Fechando jogo...")

def run():

    clear()

    while(True):
        clear()
        print_header("Menu inicial\n")
        print_normal(f"\t{prim_opt.CREATE}) Novo jogo")
        print_normal(f"\t{prim_opt.LOAD}) Continuar um jogo")
        print_normal(f"\t{prim_opt.DELETE}) Deletar um jogo")

        print_normal(f"\n\t{prim_opt.EXIT}) Fechar jogo")


        option = input_question("Opção: ").upper()

        if(option == prim_opt.CREATE): 
            create_new_game()
        elif(option == prim_opt.LOAD):
            continue_game()
        elif(option == prim_opt.DELETE): 
            delete_game()
        elif(option == prim_opt.RESETE_TEST):
            resete_test()
        elif(option == prim_opt.EXIT):
            exit_game()
            break
        else:
            print_error(f"Opção ({option}) inválida! pressione ENTER")
            input("")
        




if __name__ == '__main__':
    run()
