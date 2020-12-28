
from Thing import Thing
from Board import Board

class Entity(Thing):

    def __init__(self):
        super().__init__()
    

    def new_concrete_thing(self):
        board : Board = self.get("Board")
        concrete = super().new_concrete_thing()
        concrete["coord"] = board.alphanum_to_coord("A1")
        concrete["dice_method"] = "DiceRandom"

        return concrete
    
    def roll_dice(self, _id, max_val=6):
        entity = self.get_concrete_thing(_id)
        dice = self.get(entity["dice_method"])
        return dice.roll_dice(max_val)

        

