
from Thing import Thing
from Board import Board
from common import GOVERNMENT


class Building(Thing):

    def __init__(self) -> None:
        super().__init__()
    
    def new_concrete_thing(self):
        building = super().new_concrete_thing()

        board : Board = self.get("Board")

        building["coord"] = board.alphanum_to_coord("A1")
        building["selling_price"] = 1000
        building["money"] = 0
        building["owner"] = GOVERNMENT
        building["name"] = "Nome da construção"


        return building
    

