from utils.common import MOCK_ID
from entity.object.building.commerce.Commerce import Commerce


class GunShop(Commerce):


    def __init__(self) -> None:
        # self.interactions['buy_food'] = 'comprar comida'
        super().__init__()

        self.sell_item_class = 'Weapon'
        self.sell_nick = 'arma'

    def choose_quantity(self, building_ref, person_ref):
        return 1
    

    def new_concrete_thing(self):
        gunshop = super().new_concrete_thing()
        self.update_concrete(gunshop)
        board : Board = self.get("Board")
        gunshop["id"] = MOCK_ID
        gunshop[self.attr_name] = "Loja de armas"
        gunshop[self.attr_money] = 1000000
        # gunshop[self.attr_owner] = 10000000
        gunshop[self.attr_coord] = board.alphanum_to_coord("B3")
        self.update_subscriber(self.reference(gunshop["id"]))

        return gunshop




