#file -- game.py --
import random
from game.Logger import Logger
from entity.object.building.commerce.Bank import Bank, MoneyBag
from entity.livingbeing.person.player.PlayerIM import PlayerIM
from entity.livingbeing.person.player.PlayerOOM import PlayerOOM
from game.Game import Game
from utils import beauty_print
from utils.beauty_print import *
from utils.common import *
from game.SaveManager import SaveManager
from game.DataStructure import DataStructure
from game.Board import Board
from game.Event import Event
from game.Category import Category



class GameManager(Game):
    def __init__(self):
        super().__init__()
        self.player_idx = None
        self.valid_spots_buffer = []
    
    def setup(self, save):
        # just for not needing to acess ["SaveManager"]["concrete_things"]["1"] every time
        # self.meta_data() = save
        
        self.state.setup(save)
        
        # # Just to work with the category system used at the time
        # self.get("Category").setup(save)

        self.get("Event").setup()

        self.player_im : PlayerIM = self.get("PlayerIM")
        self.player_oom : PlayerOOM = self.get("PlayerOOM")
        self.update_subscribers()
        # self.get_state() = save

    def update_subscribers(self):
        event : Event = self.get("Event")
        # to show valid paths
        event.subscribe("building_board_print", self.reference(MOCK_ID), "on_building_board_print")
        event.subscribe("entity_choosing_spot", self.reference(MOCK_ID), "save_valid_spots_on_buffer")
        event.subscribe("new_round", self.reference(MOCK_ID), "on_new_round")
    
    def get_save_name(self):
        try:
            return self.meta_data()["save_name"]
        except:
            return "Game of life py"
    
    def meta_data(self):
        data : DataStructure = self.get("DataStructure")
        try:
            # print_debug(data.data["SaveManager"]["concrete_things"], __name__)
            return data.data["SaveManager"]["concrete_things"][MOCK_ID]
        except:
            log_error(f"Can't get meta data (SaveManager)",__name__,line())
            return None
            # It gives exception when testing because data strucure wasn't assigned
            # to game manager, so for testing porposes it creates a temporary data
            # print_debug(f"deu expeption",__name__)
            # concrete = self.new_concrete_thing("game_mock_for_test")
            # print_debug(concrete, __name__)
            # data.data["SaveManager"]["concrete_things"]["1"] = concrete
            # data.keep_concrete_thing("1", concrete, self.get_category())
            # return data.data["SaveManager"]["concrete_things"]["1"]

    def set_factory(self, factory):
        super().set_factory(factory)
        self.state : DataStructure = self.get("DataStructure")
        self.board : Board = self.get("Board")
        
        self.save_manager : SaveManager = self.get("SaveManager")

        

    def on_building_board_print(self, interested, event_causer, additional):
        if(len(self.valid_spots_buffer) == 0):
            return
        category = self.get_category()
        if(category not in additional):
            additional[category] = []
        for i in self.valid_spots_buffer:
            additional[category].append({
                "image": '📗',
                "coord": self.board.alphanum_to_coord(i)
            })
        self.valid_spots_buffer = []

    def save_valid_spots_on_buffer(self, interested, player_ref, additional):
        player_categ = player_ref["category"]
        if(not self.is_player(player_categ)):
            return
        self.valid_spots_buffer = additional["valid_spots"]
        # player_class : Player = self.factory.gi(player_categ)
        # player_id = player_ref["id"]
        # player_concr = player_class.get_concrete_thing(player_id)

    def is_player(self, category):
        categ_mg : Category = self.factory.gi("Category")
        return categ_mg.is_category_or_inside(category, "Player")

    def start(self):
        clear()

        if(self.has_no_players_in_game()):
            print_error("Não há jogadores na partida, pressione ENTER para voltar e criar alguns no menu de partida.")
            a = input("")
            return
        
        turn = self.turn_of()

        # self.player_idx = self.get("PlayerIM").get_player_idx()

        # self.get_players_id_list() # fix
        # print_debug(f"turn={turn} tipo do turn: {type(turn)}. ids em jogo={self.get_players_id_list()}", fname=__name__, fline=get_linenumber(), pause=True)
        if(turn is None or str(turn) not in self.player_im.get_players_id_list()):
            self.set_turn(self.player_im.get_player_by_idx(0)["id"])

        self.game_ruinning = True

        self.get("Event").notify("game_is_starting")

        while self.game_ruinning:
            if(self.has_no_players_in_game()):
                # log_error(f"No players in game",__name__,line())
                self.get('Logger').dump()
                print_error("Todos os jogadores morreram")
                a = input("ENTER para voltar")
                break

            self.print_game()
            turn_of = self.turn_of()
            # print_debug(f"turn_of = {turn_of}",__name__,line())
            self.player_im.player_move(turn_of)
            if not self.pass_turn():
                continue
            if(self.turn_of() == self.player_im.get_players_id_list()[0]):
                self.get("Event").notify("new_round")


    def on_new_round(self, interested, event_causer):
        save_mg = self.get_concrete_thing_by_ref(self.reference(MOCK_ID, "SaveManager"))
        save_mg['year'] += 1

        ubi = 50
        bank : Bank = self.get("Bank")
        data : DataStructure = self.get("DataStructure")
        bank_k = list(bank.get_dict_list().keys())[0]
        # print_debug(bank_k)
        bank_crt = bank.get_concrete_thing(bank_k)
        for player in self.player_im.get_players_id_list():
            bank.transfer_money_from_to(bank.reference(MOCK_ID), self.player_im.reference(player), ubi)
        log : Logger = self.get("Logger")
        players_list = ", ".join(self.player_im.get_players_list())
        log.add(f"Jogadores {players_list} receberam auxílio de R$ {ubi}")

        # add money on the board
        money : MoneyBag = self.get("MoneyBag")
        if len(money.get_dict_list()) < 4:
            m = money.new_concrete_thing()
            m["money"] = random.randrange(10, 75, 5)
            data.keep_concrete_thing(m["id"], m, "MoneyBag")
        
        self.save()
        # print_debug(bank_crt)

    def get_year(self):
        try:
            save_mg = self.get_concrete_thing_by_ref(self.reference(MOCK_ID, "SaveManager"))
            return save_mg['year']
        except:
            return STARTING_YEAR
        
    def stop(self):
        self.game_ruinning = False
    
    def print_game(self):
        clear()
        self.get("Logger").dump()
        self.board.print_board()
        self.player_im.print_player(self.turn_of())

    def save(self):
        self.save_manager.save_to_file(self.get_state())

    def number_of_players(self) -> int:
        return self.player_im.number_of_players()

    def has_no_players_in_game(self):
        if(self.number_of_players() == 0):
            return True
        return False
    
    def set_turn(self, new_turn: str):
        id_list : list = self.player_im.get_players_id_list()
        idx = id_list.index(new_turn)
        self.meta_data()["turn_of_idx"] = idx
    
    def get_players_list(self) -> list:
        return self.player_im.get_players_list()
    
    # def get_players_id_list(self) -> list:
    #     return self.player_im.get_players_id_list()

    # def get_players_oom_id_list(self) -> list:
    #     return self.player_oom.get_players_id_list()

    def current_player(self) -> dict:
        k = self.turn_of()
        return self.player_im.get_players()[str(k)]

    
    def generate_id(self) -> str:
        self.meta_data()["last_id"] += 1
        return str(self.meta_data()["last_id"])
    
    def get_state(self):
        return self.state.data


    
    def empty(self, lista):
        if len(lista)==0: 
            self.save()
            return True
        return False

    def pass_turn(self):
        data = self.meta_data()
        turns : list = data['turns']
        players_id = self.get("PlayerIM").get_players_id_list()

        if self.empty(players_id): return False
        if self.empty(turns): return False
        
        current = turns.pop(0)
        if(current in players_id):
            turns.append(current)
        
        data['turns'] = turns
        if self.empty(turns): return False

        # new_p_idx = self.player_im.get_player_idx()
        # if new_p_idx is None, player died, so the last idx is the id of the next player
        # and doesn't need to update
        e : Event = self.get("Event")
        e.notify("new_turn", additional=turns[0])

        return True


    
    def turn_of(self) -> str:
        data = self.meta_data()
        turns = data['turns']
        
        player_mg : PlayerIM = self.get("PlayerIM")
        players_id = player_mg.get_players_id_list()

        if self.empty(players_id): 
            # print_debug(f"get_players_id_list vazio -> {players_id}",__name__,line())
            return None
        
        # update players turn
        for _id in players_id:
            if _id not in turns:
                turns.append(_id)
        
        # if self.empty(turns): return None 
        
        if turns[0] not in players_id:
            # player id is not in match, so delete it
            del turns[0]
        
        data['turns'] = turns
        if self.empty(turns): return None
        
        # turn_id = turns[0]

        return turns[0]
        # idx = self.meta_data()["turn_of"]
        # if idx is None:
        #     self.meta_data()["turn_of"] = 0
        #     idx = 0
        # return [idx]
        # return self.meta_data()["turn_of"]
    
    # def update_concrete(self, concrete: dict):
    #     self.add_attr_if_not_exists(concrete, 'year', STARTING_YEAR)

    
    

    # def pass_turn1(self):
    #     num_players = self.number_of_players()
    #     if(num_players == 0):
    #         self.meta_data()["turn_of_idx"] = None
    #         self.save()
    #         return
    #     new_p_idx = self.player_im.get_player_idx()
    #     # if new_p_idx is None, player died, so the last idx is the id of the next player
    #     # and doesn't need to update

    #     next_player_idx = (int(self.player_idx)+1) % num_players
    #     next_player = self.player_im.get_player_by_idx(next_player_idx)

    #     self.set_turn(next_player["id"])
    #     e : Event = self.get("Event")
    #     e.notify("new_turn", additional=self.turn_of())
    