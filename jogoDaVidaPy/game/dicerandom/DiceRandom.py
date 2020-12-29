
from game.Game import Game

import random

class DiceRandom(Game):

    def __init__(self):
        super().__init__()
    

    def roll_dice(self, num_of_sides=6):

        result = random.randint(1, num_of_sides)

        return result
    
    

