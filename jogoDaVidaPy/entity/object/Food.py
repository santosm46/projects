
from entity.object.Object import Object


class Food(Object):


    def __init__(self):
        super().__init__()
        self.i_image = "image"
        self.i_energy = "energy"
        self.i_price = "price"
        self.i_health = "health"


    food_info = {
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

    def food_categs_to_options(self, food_categ_list, show_price=True, food_qtd=None):
        options = []
        food_dict = []
        food_names = []


        for name in food_categ_list:
            food_names.append(name)
            info = self.food_info[name]
            imgage = info[self.i_image]
            energy = info[self.i_energy]
            price = info[self.i_price]
            health = info[self.i_health]
            price_info = f"{price}💲 " if show_price else ''
            qtd = food_qtd[name] if food_qtd else None
            if qtd == 0: continue
            qtd_out = f"Qtd: {qtd} " if qtd else ''
            opt = f"{imgage}: {qtd_out}{energy}⚡ {price_info}{health}💜"
            food_dict.append(info)
            options.append(opt)
        
        return options, food_dict, food_names

    def apply_food_properties_to(self, being_ref, food, qtd=1):
        from entity.livingbeing.LivingBeing import LivingBeing

        being = self.get_concrete_thing_by_ref(being_ref)

        info = self.food_info[food]
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

    def get_food_inventory_of(self, being_ref):
        being = self.get_concrete_thing_by_ref(being_ref)
        inventory = being["inventory"]
        if("Food" not in inventory):
            inventory["Food"] = {}
        return inventory["Food"]

    def add_to_inventory(self, being_ref, food_to_add, quantity):
        food_inventory = self.get_food_inventory_of(being_ref)
        if(food_to_add not in food_inventory):
            food_inventory[food_to_add] = 0
        
        food_inventory[food_to_add] += quantity
    
    def remove_from_inventory(self, being_ref, food_to_add, quantity):
        food_inventory = self.get_food_inventory_of(being_ref)

        if(food_inventory == {}):
            return False
        if(food_to_add not in food_inventory):
            return False

        new_qtd = max(0, food_inventory[food_to_add] - quantity)
        food_inventory[food_to_add] = new_qtd

        return True



