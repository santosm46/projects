
from Thing import Thing

import random

class DiceRandom(Thing):

    def __init__(self):
        super().__init__()
    

    def roll_dice(self, num_of_sides=6):

        result = random.randint(1, num_of_sides)

        return result
    
    

