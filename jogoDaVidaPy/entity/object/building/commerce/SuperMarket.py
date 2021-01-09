from entity.object.building.commerce.Bank import Bank
from math import trunc
from utils.common import MOCK_ID
from entity.object.Food import Food
from game.Board import Board
from entity.object.building.commerce.Commerce import Commerce




class SuperMarket(Commerce):


    def __init__(self) -> None:
        # self.interactions['buy_food'] = 'comprar comida'
        super().__init__()

        self.sell_item_class = 'Food'
        self.sell_nick = 'comida'

        self.work_nick = 'Caixa de supermercado'

        self.wage_multipl = 30
    
    # def get_interactions_for(self, me_ref):
    #     return self.interactions
    def can_work_here(self, person_ref):
        return self.get('School').person_has_highest_level(person_ref)

    def new_concrete_thing(self):
        market = super().new_concrete_thing()
        self.update_concrete(market)
        board : Board = self.get("Board")
        market["id"] = MOCK_ID
        market[self.attr_name] = "Super Mercado"
        market[self.attr_money] = 1000000
        # market[self.attr_owner] = 10000000
        market[self.attr_coord] = board.alphanum_to_coord("C2")
        self.update_subscriber(self.reference(market["id"]))

        return market

    

    



    
    


