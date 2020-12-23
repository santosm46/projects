from common import *
from beauty_print import *
from game import Game
from player import PlayerHandler
from save_manager import *

def start_game(save):
    # print_debug(f"main. {save}")
    save_name = save["save_name"]

    game = Game(save)
    game.setup(PlayerHandler())
    # game.start()

    while(True):
        clear()

        print_header(f"Menu da partida: {save_name} \nJogadores: {game.get_players_list()} \n")
    
        print_normal(f"\t{prim_opt.CONTINUE}) Continuar partida")
        print_normal(f"\t{prim_opt.ADD_PLAYER}) Adicionar jogadores na partida")
        print_normal(f"\t{prim_opt.REM_PLAYER}) Remover jogador da partida")
        print_normal(f"\t{prim_opt.DEL_PLAYER}) Deletar jogador fora da partida")
        print_normal(f"\t{prim_opt.SAVE_EXIT}) Salvar e voltar para menu inicial")

        option = input_question("\nOpção: ").upper()

        if(option == prim_opt.CONTINUE):
            game.start()
        elif(option == prim_opt.ADD_PLAYER):
            game.player_handler.create_players()
        elif(option == prim_opt.REM_PLAYER):
            game.player_handler.remove_players()
        elif(option == prim_opt.DEL_PLAYER):
            game.player_handler.delete_players()
        elif(option == prim_opt.SAVE_EXIT):
            game.save()
            game.stop()
            return
        else:
            print_error(f"Opção ({option}) inválida! pressione ENTER")
            cont = input("")


def run():
    clear()

    while(True):
        clear()
        print_header("Menu inicial\n")
        print_normal(f"\t{prim_opt.CREATE}) Criar novo jogo")
        print_normal(f"\t{prim_opt.LOAD}) Carregar um jogo")
        print_normal(f"\t{prim_opt.DELETE}) Deletar um jogo")

        print_normal(f"\n\t{prim_opt.EXIT}) Fechar jogo")

        option = input_question("Opção: ").upper()

        if(option == prim_opt.CREATE):
            create_new_save()
        elif(option == prim_opt.LOAD):
            save = load_save()
            if save is not None:
                start_game(save)
        elif(option == prim_opt.DELETE):
            delete_save()
        elif(option == prim_opt.EXIT):
            print_sucess("Fechando jogo...")
            break # ou return
        else:
            print_error(f"Opção ({option}) inválida! pressione ENTER")
            cont = input("")




if __name__ == '__main__':
    run()
