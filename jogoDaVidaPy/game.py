#file -- game.py --
from beauty_print import *
from common import *
from save_manager import save_to_file

class Game:

    def __init__(self, save):
        self.state = save
    
    def set_player_handler(self, ph):
        self.player_handler = ph

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
            self.state["turn_of"] = self.player_handler.get_player_by_idx(0)["id"]

        self.game_ruinning = True

        while self.game_ruinning:
            clear()
            self.player_handler.print_player(self.turn_of())
            self.player_handler.player_move()

    def setup(self, player_handler):
        self.set_player_handler(player_handler)
        self.player_handler.setup(self)
    
    def turn_of(self) -> str:
        return str(self.state["turn_of"])

    def pass_turn(self):
        num_players = self.number_of_players()
        if(num_players == 0):
            self.state["turn_of"] = None
            self.save()
            return
        player_idx = self.player_handler.get_player_idx()
        next_player_idx = (int(player_idx)+1) % num_players
        next_player = self.player_handler.get_player_by_idx(next_player_idx)

        self.state["turn_of"] = next_player["id"]

    def stop(self):
        self.game_ruinning = False

    def save(self):
        save_to_file(self.state)

    def number_of_players(self) -> int:
        return len(self.state["players"])

    def has_no_players_in_game(self):
        if(self.number_of_players() == 0):
            return True
        return False
    
    def get_players_list(self) -> list:
        players_list = []
        for key in self.state["players"].keys():
            players_list.append(self.state["players"][key]["name"])
        return players_list
    
    # oom = out of match
    def get_players_oom_list(self) -> list:
        players_list = []
        for key in self.state["out_of_match"].keys():
            players_list.append(self.state["out_of_match"][key]["name"])
        return players_list
    
    def get_players_id_list(self) -> list:
        id_list = list(self.state["players"].keys())
        id_list_str = []
        for i in id_list:
            id_list_str.append(str(i))
        return id_list_str

    def get_players_oom_id_list(self) -> list:
        return list(self.state["out_of_match"].keys())

    def current_player(self) -> dict:
        k = self.turn_of()
        return self.state["players"][str(k)]

    
    def generate_id(self) -> str:
        self.state["last_id"] += 1
        return str(self.state["last_id"])
    
    # apenas chama a função da player_handler de mesmo nome
    def get_player_by_idx(self, idx):
        return self.player_handler.get_player_by_idx(idx)






