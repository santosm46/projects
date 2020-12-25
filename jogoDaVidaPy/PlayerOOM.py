from beauty_print import *
from common import *

from Player import Player



class PlayerOOM(Player):

    def __init__(self):
        super().__init__()
    
    
    def delete_players(self):
        clear()

        while(True):
            players_oom = self.game.player_oom.get_players()
            print_header("Deletar jogadores [Só é possível deletar jogadores fora da partida]")
            if(len(players_oom) == 0):
                print_error("Não há jogadores fora da partida! Pressione ENTER")
                input("")
                return
            
            print_warning("\t\tobs: Aperte ENTER para sair\n")
            print_header("Fora da partida: ")
            self.print_players_list(players_oom)

            players_oom_id_list = self.game.player_oom.get_players_id_list()

            while True:
                idx = input_question("\nN° do jogador para remover: ")
                if(len(idx) == 0):
                    return
                
                if(self.valid_player_idx(idx, len(players_oom_id_list))):
                    break
            idx = int(idx)-1

            id_oom = str(players_oom_id_list[idx])
            player_oom = self.game.player_oom.get_players()[id_oom]
            name = player_oom["name"]

            resp = input_question(f"Tem certeza que quer deletar o jogador \"{name}\"? (S/N): ").upper()
            if(resp == "S"):
                self.game.player_oom.get_players().pop(id_oom)
                self.game.save()
                print_sucess(f"Jogador {name} deletado!\n")
            clear()
    







