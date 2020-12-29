
import builtins
from Object import Object
from Board import Board
from common import GOVERNMENT


class Building(Object):


    def __init__(self) -> None:
        super().__init__()
        self.attr_money = 'money'
        self.attr_name = 'name'
    
    images = {
        "College": '🎓',
        "House": ['🏠', '🏡'],
        "Hospital": '🏥',
        "Church": '⛪',
        "Bank": '🏦',
        "TownHall": '🏛️',
        "GasStation": '⛽',
        "Castle": '🏰',
        "SuperMarket": '🛒',
        "Casino": '🎰',
    }
    
    

    def new_concrete_thing(self):
        building = super().new_concrete_thing()

        self.update_concrete(building)        

        return building
    
    
    def update_concrete(self, building: dict):
        super().update_concrete(building)

        board : Board = self.get("Board")
        
        self.add_attr_if_not_exists(building, self.attr_coord, board.alphanum_to_coord("A1"))
        self.add_attr_if_not_exists(building, self.attr_price, 1000)
        self.add_attr_if_not_exists(building, self.attr_money, 0)
        self.add_attr_if_not_exists(building, self.attr_owner, GOVERNMENT)
        self.add_attr_if_not_exists(building, self.attr_name  ,"Nome da construção")



