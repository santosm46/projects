
from entity.object.Object import Object


class Food(Object):


    def __init__(self):
        super().__init__()
        
        self.i_energy = "energy"
        self.i_health = "health"


    items_info = {
        "Hamburger": {
            "image": '🍔',
            "energy": 20,
            "price": 50,
            "health": -3
            
        },
        "Pizza": {
            "image": '🍕',
            "energy": 10,
            "price": 45,
            "health": -2
        },
        "Chicken": {
            "image": '🍗',
            "energy": 7,
            "price": 40,
            "health": -1
        },
        "Apple": {
            "image": '🍎',
            "energy": 10,
            "price": 75,
            "health": 1
        },
        "Mango": {
            "image": '🥭 ',
            "energy": 3,
            "price": 25,
            "health": 1
        },
        # "Bone": {
        #     "image": '🦴',
        #     "energy": 0,
        #     "price": 10,
        #     "health": 0
        # },
        "Avocado": {
            "image": '🥑',
            "energy": 3,
            "price": 75,
            "health": 3
        },
        "Cake": {
            "image": '🍰',
            "energy": 4,
            "price": 40,
            "health": -1
        },
    }

    def get_gui_item(self, name, show_price=True, item_qtd=None):
        info = self.items_info[name]

        imgage = info[self.i_image]
        energy = info[self.i_energy]
        health = info[self.i_health]
        price = info[self.i_price]
        price_info = f"{price}💲 " if show_price else ''
        qtd = item_qtd[name] if item_qtd else ''
        qtd = f"{qtd:>2}" if qtd !='' else ''
        # if qtd == 0: return None
        # qtd_out = f"{qtd}" if qtd else ''
        # qtd_out = f"{qtd}"
        gui_out = f"{qtd}{imgage}: {energy:>2}⚡ {price_info:>3}{health:>2}💜"

        return gui_out


    

    def apply_item_properties_to(self, being_ref, food, qtd=1):
        # from entity.livingbeing.LivingBeing import LivingBeing
        # being = self.get_concrete_thing_by_ref(being_ref)

        info = self.items_info[food]
        energy = info[self.i_energy]
        image = info[self.i_image]
        health = info[self.i_health]

        being_class : LivingBeing = self.get(being_ref["category"])

        if(not being_class.reduce_energy(being_ref, -energy * qtd)):
            return False
        cause = {'type':'ate_junk_food', 'info':f'comendo porcaria: {image}'}
        if(not being_class.reduce_hp(being_ref, -health * qtd, cause)):
            return False
        
        return self.remove_from_inventory(being_ref, food, qtd)

    



