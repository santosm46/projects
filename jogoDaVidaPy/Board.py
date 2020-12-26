from common import DEBUG_ENABLED, get_linenumber, replacer
from beauty_print import debug_error, print_debug, print_header, print_normal, bcolors
from Thing import Thing
from Event import Event
# from PlayerIM import PlayerIM
import math


class spot_type:
    FREE = '⬜'
    BUILDING = '⬛'


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
                if(row >= self.rows() or column >= self.columns()):
                    continue
                distance = abs(i) + abs(j)
                if(distance > range_):
                    continue
                # if(self.coord_to_alphanum(coord) == "E10"):
                #     print_debug(f"board[{i}][{j}] = {board_chars[i][j]}",__name__)
                if(board_chars[row][column] != spot_type.FREE):
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
    
    def board_copy(self):
        copy = []
        for i in board_chars:
            copy.append(i)
        return copy

    def print_board(self):
        # print_normal("Board.py: finge que o tabuleiro foi imprimido")
        copy = self.board_copy()

        a = """
            {
                "image":".",
                "coord":...
            }
        """

        entities = {}
        entities["list"] = []

        self.event.notify("building_board_print", self.reference("id_mock"), entities)

        for entity in entities["list"]:
            row = entity["coord"]["row"]
            col = entity["coord"]["column"]
            # print_debug(f"rc={row},{col} out={out}", fname=__name__)
            copy[row] = replacer(copy[row], entity["image"], col)

        print_header("\n       Tabuleiro\n")
        for i in range(len(copy)):
            print_normal(f"  {self.num_to_letter(i)} {copy[i]}")
        print_normal("")


    def print_raw_board(self):
        for row in board_chars:
            print(row)

