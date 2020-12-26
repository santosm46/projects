
from Thing import Thing
from Board import Board

class Entity(Thing):

    def __init__(self):
        super().__init__()
    

    def new_concrete_thing(self):
        board : Board = self.factory.get_instance("Board")
        concrete = super().new_concrete_thing()
        concrete["coord"] = board.alphanum_to_coord("A1")
        return concrete
    
    