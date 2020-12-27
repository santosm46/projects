from beauty_print import print_warning
from LivingBeing import LivingBeing
from RandomName import RandomName
# from common import MAX_HP

class Person(LivingBeing):

    def __init__(self):
        super().__init__()
        self.MAX_HP = 10
        self.modes_info["on_board"] = {"func":self.move_on_board}
        self.modes_info["on_school"] = {"func":self.on_school_move, "school":None}
    
    def new_concrete_thing(self):
        info_gen : RandomName = self.factory.get_instance("RandomName")
        info = info_gen.gen_person_info()

        concrete = super().new_concrete_thing()
        concrete["genre"] = info["genre"]
        concrete["name"] = info["name"]
        concrete["money"] = 200
        concrete["hp"] = self.MAX_HP
        concrete["max_hp"] = self.MAX_HP
        

        return concrete

        
    def on_school_move(self, params=None):
        person = self.get_concrete_thing(params["id"])
        name = person["name"]
        print_warning(f"Me chamo {name} e estou na escolaa")
        input("")

    def move_on_board(self, params=None):
        print_warning("Pessoa genéria movendo no tabueiro...")

