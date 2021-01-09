
from entity.Entity import Entity

class Object(Entity):
    

    def __init__(self):
        super().__init__()
        self.attr_owner = 'owner'
        self.attr_price = 'price'
        self.attr_coord = 'coord'

        self.mode_dropped = "dropped"

        self.i_image = "image"
        self.i_price = "price"



    def new_concrete_thing(self):
        concrete = super().new_concrete_thing()
        self.update_concrete(concrete)

        return concrete



    def update_concrete(self, concrete: dict):
        super().update_concrete(concrete)
        self.add_attr_if_not_exists(concrete, self.attr_owner, None)
        self.add_attr_if_not_exists(concrete, self.attr_price, 5000)
        # self.add_attr_if_not_exists(concrete, self.attr_coord, {"row":0,"column":0})


    def get_item_inventory_of(self, being_ref):
        being = self.get_concrete_thing_by_ref(being_ref)
        item_categ = self.get_category()
        inventory = being["inventory"]
        if(item_categ not in inventory):
            inventory[item_categ] = {}
        return inventory[item_categ]

    def add_to_inventory(self, being_ref, food_to_add, quantity):
        food_inventory = self.get_item_inventory_of(being_ref)
        if(food_to_add not in food_inventory):
            food_inventory[food_to_add] = 0
        
        food_inventory[food_to_add] += quantity
    
    def remove_from_inventory(self, being_ref, food_to_add, quantity):
        food_inventory = self.get_item_inventory_of(being_ref)

        if(food_inventory == {}):
            return False
        if(food_to_add not in food_inventory):
            return False

        new_qtd = max(0, food_inventory[food_to_add] - quantity)
        food_inventory[food_to_add] = new_qtd

        return True

    def item_categs_to_options(self, item_categ_list, show_price=True, item_qtd=None):
        options = []
        item_dict = []
        item_names = []

        for name in item_categ_list:
            opt = self.get_gui_item(name, show_price, item_qtd)
            item_names.append(name)
            item_dict.append(self.items_info[name])
            options.append(opt)
        
        return options, item_dict, item_names


