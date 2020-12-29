
from entity.Entity import Entity

class Object(Entity):
    

    def __init__(self):
        super().__init__()
        self.attr_owner = 'owner'
        self.attr_price = 'price'
        self.attr_coord = 'coord'

        self.mode_dropped = "dropped"



    def new_concrete_thing(self):
        concrete = super().new_concrete_thing()
        self.update_concrete(concrete)

        return concrete



    def update_concrete(self, concrete: dict):
        self.add_attr_if_not_exists(concrete, self.attr_owner, None)
        self.add_attr_if_not_exists(concrete, self.attr_price, 5000)
        self.add_attr_if_not_exists(concrete, self.attr_coord, {"row":0,"column":0})


