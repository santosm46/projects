from common import DEBUG_ENABLED, get_linenumber, replacer
from beauty_print import debug_error, print_beauty_json, print_debug, print_header, print_normal, bcolors, print_warning
from Thing import Thing
from Event import Event
from Category import Category
# from PlayerIM import PlayerIM
import math
from common import MOCK_ID

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
    
    def valid_neighbors(self, coord):
        valids = []
        for (i, j) in [(-1,0), (0,1), (0,-1), (1,0)]: 
            row = coord["row"] + i
            column = coord["column"] + j
            if(row < 0 or column < 0): continue
            if(row >= self.rows() or column >= self.columns()): continue
            if(board_chars[row][column] == spot_type.BUILDING): continue
            # print(f"r,c = {row},{column}")
            valids.append(self.coord_to_alphanum({"row":row, "column":column}))
        return valids

    def wasnt_visited(self, spot):
        return spot not in self.spots_visited
    
    def find_next_valids(self, coord, distance, range_):
        if(distance == range_):
            return
        near_valids = self.valid_neighbors(coord)
        spots_to_look = list(filter(self.wasnt_visited, near_valids))
        self.spots_visited = self.spots_visited + spots_to_look

        for spot in spots_to_look:
            spot_coord = self.alphanum_to_coord(spot)
            # print(f"self.spots_visited -> {self.spots_visited}")
            self.find_next_valids(spot_coord, distance+1, range_)
        

    def get_valid_spots_for_range(self, coord, range_):
        alpha = self.coord_to_alphanum(coord)
        self.spots_visited = [alpha]
        self.find_next_valids(coord, 0, range_)
        return self.spots_visited
      
    def move_entity_to(self, reference, alphanum=None, coord=None):
        try:
            entity : Thing = self.get(reference["category"])
            event : Event = self.get("Event")
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
        categ : Category = self.get("Category")

        a = """
            "Class": [
                {"image":".", "coord":...},
                {"image":".", "coord":...},
            ]
        """

        entities = {}

        self.event.notify("building_board_print", self.reference(MOCK_ID), entities)
        # Players will be the last to be printed
        entities["PlayerIM"] = entities.pop("PlayerIM")
        # Buildings go over players
        for category in entities.keys():
            if(categ.is_category_or_inside(category, "Building")):
                entities[category] = entities.pop(category)


        # print_debug(f"isso foi o que recolhi: ",__name__)
        # print_beauty_json(entities)

        for category, entities in entities.items():
            for entity in entities:
                row = entity["coord"]["row"]
                col = entity["coord"]["column"]
                # print_debug(f"rc={row},{col} out={out}", fname=__name__)
                copy[row] = replacer(copy[row], entity["image"], col)

        print_header("\n       Tabuleiro\n")
        self.print_column_numbers()
        for i in range(len(copy)):
            print_normal(f"  {self.num_to_letter(i)} {copy[i]}")
        print_normal("")

    def print_column_numbers(self):
        # print_normal("            11111111")
        print_normal("🖤   1 2 3 4 5 6 7 8 91011121314151617")

    def print_raw_board(self):
        for row in board_chars:
            print(row)


