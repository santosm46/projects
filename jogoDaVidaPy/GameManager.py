#file -- game.py --
from Player import Player
from PlayerOOM import PlayerOOM
from PlayerIM import PlayerIM
from Thing import Thing
from beauty_print import *
from common import *
from SaveManager import SaveManager
from DataStructure import DataStructure
from Board import Board
from Event import Event
from Category import Category


class GameManager(Thing):
    def __init__(self):
        super().__init__()
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
        event.subscribe("building_board_print", self.reference("1"), "on_building_board_print")
        event.subscribe("entity_choosing_spot", self.reference("1"), "save_valid_spots_on_buffer")
    
    def get_save_name(self):
        try:
            return self.meta_data()["save_name"]
        except:
            return "Save name not loaded"
    
    def meta_data(self):
        data : DataStructure = self.get("DataStructure")
        try:
            # print_debug(data.data["SaveManager"]["concrete_things"], __name__)
            return data.data["SaveManager"]["concrete_things"]["1"]
        except:
            # It gives exception when testing because data strucure wasn't assigned
            # to game manager, so for testing porposes it creates a temporary data
            # print_debug(f"deu expeption",__name__)
            concrete = self.new_concrete_thing("game_mock_for_test")
            # print_debug(concrete, __name__)
            data.data["SaveManager"]["concrete_things"]["1"] = concrete
            # data.keep_concrete_thing("1", concrete, self.get_category())
            return data.data["SaveManager"]["concrete_things"]["1"]

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
                # "image": '🔲',
                "coord": self.board.alphanum_to_coord(i)
            })
        self.valid_spots_buffer = []

    def save_valid_spots_on_buffer(self, interested, player_ref, additional):
        player_categ = player_ref["category"]
        if(not self.is_player(player_categ)):
            return
        self.valid_spots_buffer = additional["spots"]
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
        # self.get_players_id_list() # fix
        # print_debug(f"turn={turn} tipo do turn: {type(turn)}. ids em jogo={self.get_players_id_list()}", fname=__name__, fline=get_linenumber(), pause=True)
        if(turn is None or str(turn) not in self.player_im.get_players_id_list()):
            self.set_turn(self.player_im.get_player_by_idx(0)["id"])

        self.game_ruinning = True

        self.get("Event").notify("game_is_starting")

        while self.game_ruinning:
            self.print_game()
            self.player_im.print_player(self.turn_of())
            self.player_im.player_move(self.turn_of())
            self.pass_turn()


    def stop(self):
        self.game_ruinning = False
    
    def print_game(self):
        clear()
        self.board.print_board()

    def save(self):
        self.save_manager.save_to_file(self.get_state())

    def number_of_players(self) -> int:
        return self.player_im.number_of_players()

    def has_no_players_in_game(self):
        if(self.number_of_players() == 0):
            return True
        return False
    
    def set_turn(self, new_turn: str):
        self.meta_data()["turn_of"] = new_turn
    
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


    def pass_turn(self):
        num_players = self.number_of_players()
        if(num_players == 0):
            self.meta_data()["turn_of"] = None
            self.save()
            return
        player_idx = self.player_im.get_player_idx()
        next_player_idx = (int(player_idx)+1) % num_players
        next_player = self.player_im.get_player_by_idx(next_player_idx)

        self.meta_data()["turn_of"] = next_player["id"]
    
    def turn_of(self) -> str:
        return self.meta_data()["turn_of"]
    
    def new_concrete_thing(self, game_name):
        current_datetime = date_now()

        return {
            "save_name": game_name,
            "save_filename": str_to_file_format(game_name),
            "last_id": 1,
            "turn_of": None,
            "last_save_date": current_datetime,
            "creation_date": current_datetime,
            "game_version": GAME_VERSION,
        }

