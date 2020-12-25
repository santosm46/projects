#file -- player.py --
from beauty_print import *
from common import *
from Thing import Thing

class Player(Thing):

    def __init__(self):
        super().__init__()

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
        
        self.get_players()[new_id] = {
            "id": new_id,
            "name": name,
            "hp": MAX_HP,
            "max_hp": MAX_HP
        }
    
    def print_player(self, player_id):
        # print_debug(f"\n\nplayer_id={player_id}", fline=get_linenumber(),fname=__name__, pause=True)
        player = self.get_players()[str(player_id)]
        name = player["name"]
        hp = player["hp"]
        max_hp = player["max_hp"]
        hearts = "💜" * hp + "🖤" * (max_hp - hp)
        
        print_header(f"Jogador/a: {name}")

        
        print_normal(f"   vida {hp} [{hearts}]", end='')
        print_normal("\n")
    
    def print_players_list(self, players):
        for i in range(len(players)):
            print_normal(f"\t{i+1}) {players[i]}")

    def add_player_on_match(self, idx):
        players_oom_id_list = self.game.get_players_oom_id_list()

        if(len(players_oom_id_list) == 0):
            clear()
            return
        
        if(not self.valid_player_idx(idx, len(players_oom_id_list))):
            return

        idx = int(idx) - 1
        # player = self.get_player_oom_by_idx(idx)
        id_oom = str(players_oom_id_list[idx])
        player_oom = self.get_players_oom()[str(id_oom)]
        name = player_oom["name"]
        
        if self.remove_player_oom(id_oom):
            clear()
            print_sucess(f"Jogador/a {name} inserido na partida!\n")
        else:
            clear()
            print_error(f"Erro ao adicionar o jogador de idx {idx+1}\n")
        
        

    def create_players(self):
        clear()
        created_players = 0
        
        while(True):
            print_header("\tCriação ou adicionar jogadores fora da partida\n")
            print_warning("\t\tobs: Aperte ENTER para sair\n")
            players_oom = self.game.get_players_oom_list()
            print_header("Fora da partida: ")
            self.print_players_list(players_oom)


            print_normal("\nNome do jogador para criá-lo")
            name = input_question("  ou o N° de alguém para adicionar na partida: ")
            if(len(name) == 0):
                break
            if(is_integer(name)):
                self.add_player_on_match(name)
            else:
                clear()
                self.create_player(name)
                created_players += 1
                print_sucess(f"Jogador {name} criado!\n")
        
        self.game.save()
        print_sucess(f"Foram criados {created_players} jogadores")
    
    def remove_player(self, id) -> bool:
        try:
            turn_of = self.game.turn_of()
            if(id == turn_of):
                self.game.pass_turn()
            player = self.get_players().pop(id)
            self.get_players_oom()[id] = player
            self.game.save()
        except:
            print_error(f"player.py: id:{id} não é str ou deu outro erro em remove_player()")
            return False
        return True
        
    def remove_player_oom(self, id) -> bool:
        try:
            player = self.get_players_oom().pop(id)
            self.get_players()[id] = player
            self.game.save()
        except:
            print_error(f"player.py: id:{id} não é str ou deu outro erro em remove_player()")
            return False
        return True
    
    def delete_players(self):
        clear()

        while(True):
            players_oom = self.game.get_players_oom_list()
            print_header("Deletar jogadores [Só é possível deletar jogadores fora da partida]")
            if(len(players_oom) == 0):
                print_error("Não há jogadores fora da partida! Pressione ENTER")
                input("")
                return
            
            print_warning("\t\tobs: Aperte ENTER para sair\n")
            print_header("Fora da partida: ")
            self.print_players_list(players_oom)

            players_oom_id_list = self.game.get_players_oom_id_list()

            while True:
                idx = input_question("\nN° do jogador para remover: ")
                if(len(idx) == 0):
                    return
                
                if(self.valid_player_idx(idx, len(players_oom_id_list))):
                    break
            idx = int(idx)-1

            id_oom = str(players_oom_id_list[idx])
            player_oom = self.get_players_oom()[id_oom]
            name = player_oom["name"]

            resp = input_question(f"Tem certeza que quer deletar o jogador \"{name}\"? (S/N): ").upper()
            if(resp == "S"):
                self.get_players_oom().pop(id_oom)
                self.game.save()
                print_sucess(f"Jogador {name} deletado!\n")
            clear()
                
                

    def remove_players(self):
        idx = 0
        clear()
        
        while(True):
            players = self.game.get_players_list()
            if(len(players) == 0):
                print_warning("Não há jogadores para remover da partida! \nAperte ENTER para voltar e insira jogadores na partida.")
                input("")
                return
            
            print_header("Remoção de jogadores da partida")
            print_warning("\tobs: Aperte ENTER para sair\n")
            self.print_players_list(players)
            
            while(True):
                idx = input_question("N° do jogador: ")
                if(len(idx) == 0):
                    return
                if(self.valid_player_idx(idx)):
                    break

            idx = int(idx) - 1
            player = self.get_player_by_idx(idx)
            name = player["name"]
            
            if self.remove_player(str(player["id"])):
                clear()
                print_sucess(f"Jogador/a \"{name}\" fora da partida!\n")
            else:
                clear()
                print_error("Erro ao remover o jogador de idx " + str(idx+1))
            

    def create_players_mock(self):
        self.create_player('Anny Beatriz')
        self.create_player('Marcelo')
        self.create_player('Andréia')
    
    def valid_player_idx(self, idx, num_players=None):
        if(not is_integer(idx)):
            print_error("Número inválido! Digite um número!")
            return False
        idx = int(idx)
        if(num_players is None):
            num_players = self.game.number_of_players()
        if(idx < 1 or idx > num_players):
            print_error(f"Digite um número entre 1 e {num_players}")
            return False
        return True

    def get_player_by_idx(self, idx):
        keys = self.get_players().keys()
        key = list(keys)[idx]
        return self.get_players()[str(key)]
    
    def get_player_idx(self) -> int:
        player_id = str(self.game.current_player()["id"])
        keys = self.get_players().keys()
        keys_list = list(keys)
        num_players = self.game.number_of_players()
        for idx in range(num_players):
            if(str(keys_list[idx]) == player_id):
                return idx
        return None
    
    def get_players(self):
        return self.game.state["players"]
    
    def get_players_oom(self):
        return self.game.state["out_of_match"]
    