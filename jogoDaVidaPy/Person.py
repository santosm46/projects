# from Entity import Entity
from LivingBeing import LivingBeing

from RandomName import RandomName
# from common import MAX_HP

class Person(LivingBeing):

    def __init__(self):
        super().__init__()
        self.MAX_HP = 10
    
    def new_concrete_thing(self):
        info_gen : RandomName = self.factory.get_instance("RandomName")
        info = info_gen.gen_person_info()

        concrete = super().new_concrete_thing()
        concrete["genre"] = info["genre"]
        concrete["name"] = info["name"]
        concrete["hp"] = self.MAX_HP
        concrete["max_hp"] = self.MAX_HP
        

        return concrete

        

