from Thing import Thing
import math

class spot_type:
    FREE = '⬜'
    BUILDING = '⬛'
    PLAYERS = "🧑👨‍👦👨‍👩‍👦👨‍👩‍👧‍👦"

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

"""
0  = A
25 = Z
26 = AA 0,0     (26 % 26), (26 % 26)
27 = AB 0,1     (26 % 26), (27 % 26)
28 = AC 0,2     (26 % 26), (28 % 26)
29 = AD 0,3     (26 % 26), (29 % 26)

26^0 + u   +   26^1 + d   +   

0,1
27 = 

"""


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
        row = alphanum[0]
        column = int(alphanum[1])-1

        return {
            "row": self.letter_to_num(row),
            "column": column
        }

    def coord_to_alphanum(self, coord) -> str:
        row = int(coord["row"])
        column = coord["column"]+1
        alpha = self.num_to_letter(row)
        return f"{alpha}{column}"
    
    # def 

    # def get_free_spots(self, coord: dict ) -> dict [str, str]:


    def print_raw_board(self):
        for row in board_chars:
            print(row)

