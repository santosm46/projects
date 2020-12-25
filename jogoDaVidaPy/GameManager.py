#file -- game.py --
from Thing import Thing
from beauty_print import *
from common import *
from SaveManager import SaveManager
from Player import Player
from DataStructure import DataStructure


class GameManager(Thing):
    def __init__(self):
        super().__init__()
        self.teste = "Default"
    
    def setup(self, save):
        # just for not needing to acess ["SaveManager"]["concrete_things"]["1"] every time
        self.meta_data = save["SaveManager"]["concrete_things"]["1"]

        self.state : DataStructure = self.factory.get_instance("DataStructure")
        self.state.setup(save)

        self.player_manager : Player = self.factory.get_instance("Player")
        self.player_manager.setup(self)

        self.save_manager : SaveManager = self.factory.get_instance("SaveManager")
        # self.get_state() = save
        self.save_name = self.get_state()
    


    def start(self):
        clear()

        if(self.has_no_players_in_game()):
            print_error("Não há jogadores na partida, pressione ENTER para voltar e criar alguns no menu de partida.")
            a = input("")
            return
        turn = self.turn_of()
        # self.get_players_id_list() # fix
        # print_debug(f"turn={turn} tipo do turn: {type(turn)}. ids em jogo={self.get_players_id_list()}", fname=__name__, fline=get_linenumber(), pause=True)
        if(turn is None or str(turn) not in self.get_players_id_list()):
            self.turn.set_turn(self.player_manager.get_player_by_idx(0)["id"])

        self.game_ruinning = True

        while self.game_ruinning:
            clear()
            self.player_manager.print_player(self.turn_of())
            self.player_manager.player_move()

    def stop(self):
        self.game_ruinning = False

    def save(self):
        self.save_manager.save_to_file(self.get_state())

    def number_of_players(self) -> int:
        return len(self.get_state()["players"])

    def has_no_players_in_game(self):
        if(self.number_of_players() == 0):
            return True
        return False
    
    def get_players_list(self) -> list:
        players_list = []
        for key in self.get_state()["players"].keys():
            players_list.append(self.get_state()["players"][key]["name"])
        return players_list
    
    # oom = out of match
    def get_players_oom_list(self) -> list:
        players_list = []
        for key in self.get_state()["out_of_match"].keys():
            players_list.append(self.get_state()["out_of_match"][key]["name"])
        return players_list
    
    def get_players_id_list(self) -> list:
        id_list = list(self.get_state()["players"].keys())
        id_list_str = []
        for i in id_list:
            id_list_str.append(str(i))
        return id_list_str

    def get_players_oom_id_list(self) -> list:
        return list(self.get_state()["out_of_match"].keys())

    def current_player(self) -> dict:
        k = self.turn_of()
        return self.get_state()["players"][str(k)]

    
    def generate_id(self) -> str:
        self.meta_data["last_id"] += 1
        return str(self.meta_data["last_id"])
    
    # apenas chama a função da player_manager de mesmo nome
    def get_player_by_idx(self, idx):
        return self.player_manager.get_player_by_idx(idx)

    def get_state(self):
        return self.state.data


    def pass_turn(self):
        num_players = self.number_of_players()
        if(num_players == 0):
            self.meta_data["turn_of"] = None
            self.save()
            return
        player_idx = self.player_manager.get_player_idx()
        next_player_idx = (int(player_idx)+1) % num_players
        next_player = self.player_manager.get_player_by_idx(next_player_idx)

        self.meta_data["turn_of"] = next_player["id"]
    
    def turn_of(self) -> str:
        return self.meta_data["turn_of"]
    
    