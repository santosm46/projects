
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
            "price": 300,
        },
        "Pistol": {
            "nick": "Pistola",
            "attack": 2,
            "image": '🔫',
            "price": 400
        },
        "MachineGun": {
            "nick": "Metralhadora",
            "attack": 3,
            "image": '🔫',
            "price": 550,
        },
        "Shotgun": {
            "nick": "Escopeta",
            "attack": 4,
            "image": '🔫',
            "price": 700,
        }
    }


    def item_info(self, item):
        return self.items_info[item]
    
    def get_image(self, a=None):
        return self.item_info(self.get_category())["image"]

    def item_attack(self, item):
        return self.item_info(item)["attack"]
    def item_nick(self, item):
        return self.item_info(item)["nick"]
    

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

    def new_concrete_thing(self):
        weapon = super().new_concrete_thing()
        self.update_concrete(weapon)
        self.update_subscriber(self.reference(weapon["id"]))
        # weapon[self.mon]
        # print_debug(f"esse foi o saco de $ criado...",__name__,line())
        # print_beauty_json(weapon)
        return weapon

    # def new_concrete_thing(self):
    #     weapon = super().new_concrete_thing()


    def entity_entered_my_spot(self, myself_ref, entity_ref):
        self.entity_stepped_on_weapon(myself_ref, entity_ref)

    def entity_stepped_on_weapon(self, interested, event_causer, additional=None):
        # print_debug(f"{event_causer} pisou no dinheiro {interested} ",__name__,line())
        log : Logger = self.get("Logger")
        # moneybag = self.get_concrete_thing_by_ref(interested)
        self.add_to_inventory(event_causer, interested['category'], 1)
        name = self.get(event_causer['category']).person_name(event_causer)
        log.add(f"{name} achou uma arma {self.item_nick(interested['category'])}")

        self.delete_myself(interested)


    def put_all_weapons_on_board(self, entity_ref):
        person = self.get_concrete_thing_by_ref(entity_ref)
        
        # print_debug(f"\n\t-> p={person}\n\t-> m={weapon}",__name__,line())

        weapons : dict = self.get_item_inventory_of(entity_ref)
        data : DataStructure = self.get("DataStructure")

        for weap_categ, qtd in weapons.items():
            if qtd == 0: continue
            weapon = self.get(weap_categ).new_concrete_thing()
            weapon['coord'] = person['coord']
            data.keep_concrete_thing(weapon["id"], weapon, weap_categ)
    

class Knife(Weapon):
    def __init__(self):
        super().__init__()
class Pistol(Weapon):
    def __init__(self):
        super().__init__()
class MachineGun(Weapon):
    def __init__(self):
        super().__init__()
class Shotgun(Weapon):
    def __init__(self):
        super().__init__()

