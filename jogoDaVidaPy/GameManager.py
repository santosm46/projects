#file -- game.py --
from PlayerOOM import PlayerOOM
from PlayerIM import PlayerIM
from Thing import Thing
from beauty_print import *
from common import *
from SaveManager import SaveManager
from DataStructure import DataStructure
from Board import Board

class GameManager(Thing):
    def __init__(self):
        super().__init__()
        self.teste = "Default"
    
    def setup(self, save):
        # just for not needing to acess ["SaveManager"]["concrete_things"]["1"] every time
        self.meta_data = save["SaveManager"]["concrete_things"]["1"]

        self.board : Board = self.factory.get_instance("Board")
        self.state : DataStructure = self.factory.get_instance("DataStructure")
        self.state.setup(save)

        self.player_im : PlayerIM = self.factory.get_instance("PlayerIM")
        self.player_im.setup(self)
        self.player_oom : PlayerOOM = self.factory.get_instance("PlayerOOM")
        self.player_oom.setup(self)

        self.save_manager : SaveManager = self.factory.get_instance("SaveManager")
        # fix talvez tirar isso
        self.factory.get_instance("Category").setup(save)
        # self.get_state() = save
        self.save_name = self.meta_data["save_name"]
    


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

        while self.game_ruinning:
            clear()
            self.board.print_board()
            self.player_im.print_player(self.turn_of())
            self.player_im.player_move()

    def stop(self):
        self.game_ruinning = False

    def save(self):
        self.save_manager.save_to_file(self.get_state())

    def number_of_players(self) -> int:
        return self.player_im.number_of_players()

    def has_no_players_in_game(self):
        if(self.number_of_players() == 0):
            return True
        return False
    
    def set_turn(self, new_turn: str):
        self.meta_data["turn_of"] = new_turn
    
    def get_players_list(self) -> list:
        return self.player_im.get_players_list()
    
    # def get_players_id_list(self) -> list:
    #     return self.player_im.get_players_id_list()

    # def get_players_oom_id_list(self) -> list:
    #     return self.player_im.oom.get_players_id_list()

    def current_player(self) -> dict:
        k = self.turn_of()
        return self.player_im.get_players()[str(k)]

    
    def generate_id(self) -> str:
        self.meta_data["last_id"] += 1
        return str(self.meta_data["last_id"])
    
    def get_state(self):
        return self.state.data


    def pass_turn(self):
        num_players = self.number_of_players()
        if(num_players == 0):
            self.meta_data["turn_of"] = None
            self.save()
            return
        player_idx = self.player_im.get_player_idx()
        next_player_idx = (int(player_idx)+1) % num_players
        next_player = self.player_im.get_player_by_idx(next_player_idx)

        self.meta_data["turn_of"] = next_player["id"]
    
    def turn_of(self) -> str:
        return self.meta_data["turn_of"]
    
    