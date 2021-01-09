
from entity.object.Object import Object


class Weapon(Object):

    def __init__(self):
        super().__init__()

        self.i_attack = 'attack'
        self.i_nick = 'nick'
    

    items_info = {
        # "Bow": {
        #     "attack": 5,
        #     "image": '🏹',
        # }
        "Knife": {
            "nick": "Faca",
            "attack": 1,
            "image": '🔪',
            "price": 400,
        },
        "Pistol": {
            "nick": "Pistola",
            "attack": 2,
            "image": '🔫',
            "price": 500
        },
        "MachineGun": {
            "nick": "Metralhadora",
            "attack": 3,
            "image": '🔫',
            "price": 650,
        },
        "Shotgun": {
            "nick": "Escopeta",
            "attack": 4,
            "image": '🔫',
            "price": 800,
        }
    }


    def item_info(self, item):
        return self.items_info[item]
    # def get_image(self, reference):
    #     return self.item_info(reference)["image"]

    def item_attack(self, item):
        return self.item_info(item)["attack"]

    def get_gui_item(self, name, show_price=True, item_qtd=None):
        info = self.items_info[name]

        image = info[self.i_image]
        price = info[self.i_price]
        nick = info[self.i_nick]
        attack = info[self.i_attack]
        price_info = f"{price:<4}💲 " if show_price else ''
        nick_image = f"{nick} {image}:"
        # if qtd == 0: return None
        # qtd_out = f"{qtd}" if qtd else ''
        # qtd_out = f"{qtd}"
        gui_out = f"{nick_image:<16} {price_info}atk: {attack:<2}💜"

        return gui_out




