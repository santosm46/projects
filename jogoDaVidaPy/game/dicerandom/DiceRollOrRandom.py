
from game.dicerandom.DiceRandom import DiceRandom
from utils.beauty_print import input_question
from utils.common import valid_number

class DiceRollOrRandom(DiceRandom):


    def __init__(self):
        super().__init__()

    
    def roll_dice(self, num_of_sides=6):
        # if(num_of_sides is not None):
        #     return 
        while True:
            result = input_question("Jogue o dado e digite o resultado (ENTER para valor aleatório): ")
            if(len(result) == 0):
                return super().roll_dice(num_of_sides)
            if(valid_number(result, 1, num_of_sides)):
                break
        
        result = int(result)

        return result
        


        