from utils.common import line, log_error, replacer, MOCK_ID
from utils.beauty_print import print_header, print_normal
from game.Event import Event
from game.Category import Category
from game.Game import Game
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



class Board(Game):

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
            log_error(f"Error trying to move entity {reference} to coord {coord}", __name__, line())
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

        self.get("Event").notify("building_board_print", self.reference(MOCK_ID), entities)
        # Players will be the last to be printed
        try:
            entities["PlayerIM"] = entities.pop("PlayerIM")
        except:
            log_error(f"entities doen't have key 'PlayerIM'",__name__,line())
        # Buildings go over players

        categ_debug = ''
        try:
            for category in entities.keys():
                categ_debug = category
                if(categ.is_category_or_inside(category, "Building")):
                    entities[category] = entities.pop(category)
        except:
            log_error(f"entities doen't have key '{categ_debug}'",__name__,line())
            

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


