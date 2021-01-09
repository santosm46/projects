#file -- player.py --
from entity.object.Food import Food
from game.Logger import Logger
import math
from utils.beauty_print import *
from utils.common import clear, is_integer, line, log_error
from entity.livingbeing.person.Person import Person

player_image = ['😎','🤡','👽','🤠','🧑‍','🤯','🧐','😷','😁','👻','🤑']

events_to_listen = {"building_board_print": "on_building_board_print"}

class Player(Person):

    def __init__(self):
        super().__init__()

    def get_game(self):
        return self.get("GameManager")

    def category_nick(self):
        return "Jogador/a"
    
    def print_player(self, player_id):
        # print_debug(f"\n\nplayer_id={player_id}", fline=get_linenumber(),fname=__name__, pause=True)
        player = self.get_concrete_thing(player_id, "PlayerIM")
        if not player:
            log_error(f"Couldn't find player of id {player_id} to print",__name__, line())
            return
        name = player["name"]
        energy = player[self.attr_energy]
        max_energy = player[self.attr_max_energy]
        money = player[self.attr_money]
        money_dims = "💎" * math.floor(money / 1000)
        money_aux = money % 1000
        money_bags = "💰" * math.floor(money_aux / 100)
        money_aux = money_aux % 100
        money_notes = "💵" * math.ceil(money_aux / 10)
        hp = player["hp"]
        max_hp = player["max_hp"]
        hearts = "💜" * hp + "🖤" * (max_hp - hp)
        coord = player["coord"]
        alphanum = self.get("Board").coord_to_alphanum(coord)
        image = self.get_image(player_id)

        foods_img = ''
        foods_list = None
        food_cls : Food = self.get("Food")
        food_info = food_cls.food_info
        # because player may not have food
        if("Food" in player[self.attr_inventory]):
            foods_list = player[self.attr_inventory]["Food"]
            for food_name, food_qtd in foods_list.items():
                foods_img += food_info[food_name][food_cls.i_image] * food_qtd
            # for k, v in food_cls.food_info.items():
        age = player[self.attr_age]


        print_header(f"Jogador/a: {image} {name}    Posição: {alphanum}  Idade: {age}")

        
        print_normal(f"   vida {hp} [{hearts}]", end='')
        print_normal(f"    Dinheiro {money} {money_notes}{money_bags}{money_dims}")
        print_normal(f"   Energia: {energy}/{max_energy}", end='')
        print_normal(f"                    Comida: {foods_img}")

    def has_food(self):
        pass

        # print_normal("\n")
    
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
        players_oom_id_list = self.get_game().player_oom.get_players_id_list()

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
            clear()
            print_sucess(f"Jogador/a {name} inserido na partida!\n")
        else:
            clear()
            print_error(f"Erro ao adicionar o jogador {name} de idx {idx+1}\n")
        

    # def unsubscribe_funcs(self, _id):
    #     event : Event = self.get("Event")
    #     event.unsubscribe("building_board_print", self.reference(_id, "PlayerIM"))
    
    # remove player from match and put it on OOM list
    def remove_player(self, _id) -> bool:
        try:
            if(_id == self.get_game().turn_of()):
                self.get_game().pass_turn()
            player = self.get_players().pop(_id)
            self.get_players_oom()[_id] = player
            self.get_game().save()
        except:
            log_error(f"player.py: _id:{_id} não é str ou deu outro erro em remove_player()",__name__,line())
            return False
        return True
    
    # put player on match
    def remove_player_oom(self, id) -> bool:
        try:
            player = self.get_players_oom().pop(id)
            self.get_players()[id] = player
            self.get_game().save()
        except:
            print_error(f"player.py: id:{id} não é str ou deu outro erro em remove_player()")
            return False
        return True
    
    
                
                

    def remove_players(self):
        idx = 0
        clear()
        
        while(True):
            players = self.get_game().get_players_list()
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
        players_im = self.get("PlayerIM")
        # players_im.create_player('Anny Beatriz')
        players_im.create_player('Marcelo')
        players_im.create_player('Pedro')
        self.get("GameManager").save()
    
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
        # get idx of player turn_of
        player_id = str(self.get_game().turn_of())
        keys = self.get_players().keys()
        keys_list = list(keys)
        num_players = self.number_of_players()
        for idx in range(num_players):
            if(str(keys_list[idx]) == player_id):
                return idx
        return None
    
    def get_players(self):
        return self.get_dict_list()
    
    # fix
    def get_players_oom(self):
        return self.get_game().player_oom.get_players()
    
    def get_players_id_list(self) -> list:
        id_list = list(self.get_players().keys())
        id_list_str = []
        for i in id_list:
            id_list_str.append(str(i))
        return id_list_str
    
    def get_image(self, _id=None):
        if not _id:
            return '🧑'
        
        size = len(player_image)
        return player_image[int(_id) % size]
    

    

