
from Thing import Thing

from RandomName import RandomName
from common import MAX_HP

class Person(Thing):

    def __init__(self):
        super().__init__()
    
    def new_concrete_thing(self):
        info_gen : RandomName = self.factory.get_instance("RandomName")
        info = info_gen.gen_person_info()

        concrete = super().new_concrete_thing()
        concrete["name"] = info["name"]
        concrete["genre"] = info["genre"]
        concrete["dice_method"] = "DiceRandom"
        concrete["hp"] = MAX_HP
        concrete["max_hp"] = MAX_HP

        return concrete

        

