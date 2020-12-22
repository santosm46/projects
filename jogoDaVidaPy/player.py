#file -- player.py --
from beauty_print import *
from common import *

class PlayerHandler:

    def __init__(self):
        pass

    def setup(self, game):
        self.game = game

    def player_move(self):
        player_id = self.game.current_player()["id"]
        
        while(player_id == self.game.state["turn_of"]):
            print_normal(f"\nEscolha uma opção")
            print_normal(f"\t{prim_opt.PASS_TURN}) Passar vez")
            print_normal(f"\n")
            # print_normal(f"\t{prim_opt.SAVE}) Salvar")
            # print_normal(f"\t{prim_opt.EXIT}) Sair")
            print_normal(f"\t{prim_opt.SAVE_EXIT}) Salvar e sair para menu da partida")
            option = input_question("\nOpção: ").upper()

            if(option == prim_opt.PASS_TURN):
                print_normal("Passando vez...  ENTER para confirmar ou outra coisa para cancelar\n")
                if len(input("")) == 0:
                    break
            elif(option == prim_opt.SAVE_EXIT):
                print_sucess("Salvando e saindo...")
                self.game.stop()
                self.game.save()
                return
            else:
                print_error(f"Opção ({option}) inválida! pressione ENTER")
                cont = input("")
        self.game.pass_turn()


    def create_player(self, name):
        new_id = self.game.generate_id()
        
        self.game.state["players"][new_id] = {
            "id": new_id,
            "name": name,
            "hp": MAX_HP,
            "max_hp": MAX_HP
        }
    
    def print_player(self, player_id):
        player = self.game.state["players"][str(player_id)]
        name = player["name"]
        hp = player["hp"]
        max_hp = player["max_hp"]
        hearts = "💜" * hp + "🖤" * (max_hp - hp)
        
        print_header(f"Jogador/a: {name}")

        
        print_normal(f"   vida {hp} [{hearts}]", end='')
        print_normal("\n")

    def create_players(self):
        clear()
        created_players = 0
        print_header("\tCriação de jogadores\n")
        print_warning("\t\tobs: Aperte ENTER para sair\n")
        while(True):
            name = input_question("Nome do jogador: ")
            if(len(name) == 0):
                break
            self.create_player(name)
            created_players += 1
            print_sucess(f"Jogador {name} criado!\n")
        print_sucess(f"Foram criados {created_players} jogadores")
        
    def create_players_mock(self):
        self.create_player('Anny Beatriz')
        self.create_player('Marcelo')
        self.create_player('Andréia')

    def get_player_by_idx(self, idx):
        keys = self.game.state["players"].keys()
        key = list(keys)[idx]
        return self.game.state["players"][str(key)]
    
    def get_player_idx(self) -> int:
        player_id = str(self.game.current_player()["id"])
        keys = self.game.state["players"].keys()
        keys_list = list(keys)
        num_players = self.game.number_of_players()
        for idx in range(num_players):
            if(str(keys_list[idx]) == player_id):
                return idx
        return None
        