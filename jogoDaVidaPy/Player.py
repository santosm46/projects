#file -- player.py --
from Event import Event
from DataStructure import DataStructure
from beauty_print import *
from common import *
from Person import Person
# from GameManager import GameManager
from Board import Board

player_image = ['😎','🤡','👽','🤠','🧑‍','🤯','🥶','😷','😁','👻']

class Player(Person):

    def __init__(self):
        super().__init__()

    def setup(self, game):
        self.game  = game
        # self.im : Player = self.factory.get_instance("PlayerIM")
        # self.oom : Player = self.factory.get_instance("PlayerOOM")

        # self.im.setup(game)

    def new_concrete_thing(self):
        return super().new_concrete_thing()

    
    def print_player(self, player_id):
        # print_debug(f"\n\nplayer_id={player_id}", fline=get_linenumber(),fname=__name__, pause=True)
        player = self.get_players()[str(player_id)]
        name = player["name"]
        hp = player["hp"]
        max_hp = player["max_hp"]
        hearts = "💜" * hp + "🖤" * (max_hp - hp)
        coord = player["coord"]
        board : Board = self.factory.get_instance("Board")
        alphanum = board.coord_to_alphanum(coord)
        image = self.get_image(player_id)

        print_header(f"Jogador/a: {image} {name}    Posição: {alphanum}")

        
        print_normal(f"   vida {hp} [{hearts}]", end='')
        print_normal("\n")
    
    def print_players_list(self, players=None):
        if players is None:
            players = self.get_players_list()
        # print_debug(f"tipo players = {type(players)}")
        for i in range(len(players)):
            print_normal(f"\t{i+1}) {players[i]}")
        # try:
        # except:
        #     debug_error(f"players must be a list, it is {type(players)}", fname=__name__, fline=get_linenumber())

    def get_players_list(self) -> list:
        players_list = []
        for key in self.get_players().keys():
            # print_warning(f"key {key}")
            # print_warning(self.get_players())
            aa = self.get_players()[key]["name"]
            # print(aa)
            players_list.append(aa)
        return players_list

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
        print_debug(f"id_oom={id_oom}",__name__)
        if self.remove_player_oom(id_oom):
            self.subscrive_funcs(id_oom)
            clear()
            print_sucess(f"Jogador/a {name} inserido na partida!\n")
        else:
            clear()
            print_error(f"Erro ao adicionar o jogador {name} de idx {idx+1}\n")
        
    def subscrive_funcs(self, _id):
        event : Event = self.factory.get_instance("Event")
        event.subscribe(
            "building_board_print", 
            self.reference(_id, "PlayerIM"),
            "on_building_board_print")        

    def unsubscribe_funcs(self, _id):
        event : Event = self.factory.get_instance("Event")
        event.unsubscribe("building_board_print", self.reference(_id, "PlayerIM"))
    
    # remove player from match and put it on OOM list
    def remove_player(self, _id) -> bool:
        try:
            if(_id == self.game.turn_of()):
                self.game.pass_turn()
            player = self.get_players().pop(_id)
            self.get_players_oom()[_id] = player
            self.unsubscribe_funcs(_id)
            self.game.save()
        except:
            print_error(f"player.py: _id:{_id} não é str ou deu outro erro em remove_player()")
            return False
        return True
    
    # put player on match
    def remove_player_oom(self, id) -> bool:
        try:
            player = self.get_players_oom().pop(id)
            self.get_players()[id] = player
            self.game.save()
        except:
            print_error(f"player.py: id:{id} não é str ou deu outro erro em remove_player()")
            return False
        return True
    
    
                
                

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
    
    def number_of_players(self) -> int:
        return len(self.get_players())

    def valid_player_idx(self, idx, num_players=None):
        if(not is_integer(idx)):
            print_error("Número inválido! Digite um número!")
            return False
        idx = int(idx)
        if(num_players is None):
            num_players = self.number_of_players()
        if(idx < 1 or idx > num_players):
            print_error(f"Digite um número entre 1 e {num_players}")
            return False
        return True

    def get_player_by_idx(self, idx):
        keys = self.get_players().keys()
        key = list(keys)[idx]
        return self.get_players()[str(key)]
    
    def get_player_idx(self) -> int:
        player_id = str(self.game.turn_of())
        keys = self.get_players().keys()
        keys_list = list(keys)
        num_players = self.number_of_players()
        for idx in range(num_players):
            if(str(keys_list[idx]) == player_id):
                return idx
        return None
    
    def get_players(self):
        return self.get_dict_list()["concrete_things"]
    
    # fix
    def get_players_oom(self):
        return self.game.player_oom.get_players()
    
    def get_players_id_list(self) -> list:
        id_list = list(self.get_players().keys())
        id_list_str = []
        for i in id_list:
            id_list_str.append(str(i))
        return id_list_str
    
    def get_image(self, _id):
        size = len(player_image)
        return player_image[int(_id) % size]
    
