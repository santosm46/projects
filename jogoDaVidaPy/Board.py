from common import DEBUG_ENABLED, get_linenumber
from beauty_print import debug_error, print_normal, bcolors
from Thing import Thing
from Event import Event
# from PlayerIM import PlayerIM
import math


class spot_type:
    FREE = '⬜'
    BUILDING = '⬛'
    PLAYERS_MANY = ['👨‍👦','👨‍👩‍👦','👨‍👩‍👧‍👦']
    PLAYERS = ['😎','🤡','👽','👨‍🦰','🧑‍','🤯','🥶','😷','😁','👻']

board_chars = [
    "⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜",
    "⬜⬛⬛⬛⬛⬜⬛⬛⬛⬛⬜⬛⬛⬜⬛⬛⬜",
    "⬜⬛⬛⬛⬛⬜⬛⬛⬛⬛⬜⬛⬛⬜⬛⬛⬜",
    "⬜⬛⬛⬛⬛⬜⬛⬛⬛⬛⬜⬛⬛⬜⬛⬛⬜",
    "⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜",
    "⬜⬛⬛⬛⬜⬛⬛⬛⬛⬜⬛⬛⬜⬛⬛⬛⬜",
    "⬜⬛⬛⬛⬜⬛⬛⬛⬛⬜⬛⬛⬜⬛⬛⬛⬜",
    "⬜⬛⬛⬛⬜⬛⬛⬛⬛⬜⬛⬛⬜⬛⬛⬛⬜",
    "⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜",
    "⬜⬛⬛⬛⬜⬛⬛⬛⬜⬛⬛⬛⬜⬛⬛⬛⬜",
    "⬜⬛⬛⬛⬜⬛⬛⬛⬜⬛⬛⬛⬜⬛⬛⬛⬜",
    "⬜⬛⬛⬛⬜⬛⬛⬛⬜⬛⬛⬛⬜⬛⬛⬛⬜",
    "⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜",
]



class Board(Thing):

    def __init__(self):
        super().__init__()
    
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def num_to_letter(self, num: int) -> str:
        size = len(self.alphabet)
        letter = ''
        while True:
            letter = (self.alphabet[num % size]) + letter
            if(num < size):
                break
            num = math.floor(num / size)
        
        return letter
    
    def letter_to_num(self, letter: str) -> int: 
        size = len(self.alphabet)
        num = 0

        for i in range(len(letter)):
            num += math.pow(size, i) + self.alphabet.index(letter[i])
        return int(num)-1

    def alphanum_to_coord(self, alphanum):
        def is_num(val):
            return val.isdigit()
        def is_alpha(val):
            return val.isalpha()
        

        row = "".join(list(filter(is_alpha, alphanum)))
        column = int("".join(list(filter(is_num, alphanum))))-1

        "".isalpha

        return {
            "row": self.letter_to_num(row),
            "column": column
        }

    def coord_to_alphanum(self, coord) -> str:
        row = int(coord["row"])
        column = coord["column"]+1
        alpha = self.num_to_letter(row)
        return f"{alpha}{column}"
    

    def get_valid_spots_for_range(self, coord, range_):
        # range_ += 1
        valid_spots = []

        for i in range(-range_, range_+1):
            for j in range(-range_, range_+1):
                row = coord["row"] + i
                column = coord["column"] + j
                if(row < 0 or column < 0):
                    continue
                if(row > self.rows() or column > self.columns()):
                    continue
                distance = i + j
                if(distance > range_):
                    continue
                if(board_chars[i][j] != spot_type.FREE):
                    continue
                valid_spots.append(self.coord_to_alphanum({"row":row, "column":column}))

        return valid_spots
                # print(f"({row},{column})")

    def move_entity_to(self, reference, alphanum=None, coord=None):
        try:
            entity : Thing = self.factory.get_instance(reference["category"])
            event : Event = self.factory.get_instance("Event")
            concrete = entity.get_concrete_thing(reference["id"])
            if coord is None:
                coord = self.alphanum_to_coord(alphanum)
            concrete["coord"] = coord
            event.notify("entity_moved_to_coord", reference, coord)
        except:
            debug_error(f"Error trying to move entity {reference} to coord {coord}", fname=__name__, enabled=DEBUG_ENABLED, fline=get_linenumber())
    # def get_free_spots(self, coord: dict ) -> dict [str, str]:

    def rows(self):
        return len(board_chars)

    def columns(self):
        return len(board_chars[0])

    def print_board(self):
        print_normal("Board.py: finge que o tabuleiro foi imprimido")
        players = self.factory.get_instance("PlayerIM")
        players_concr = players.get_dict_list()
        pl_spots = {}
        for key, player in players_concr.items():
            if key not in pl_spots:
                pl_spots[key] = 0
            # pl_spots[key] += 1
            # a = "oi"
            # a.


    def print_raw_board(self):
        for row in board_chars:
            print(row)

