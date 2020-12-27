from beauty_print import debug_error
from Entity import Entity


class LivingBeing(Entity):

    def __init__(self):
        self.MAX_HP = 5
        self.modes_info = {}
        super().__init__()


    def new_concrete_thing(self):
        concrete = super().new_concrete_thing()

        concrete["hp"] = self.MAX_HP
        concrete["max_hp"] = self.MAX_HP
        concrete["dice_method"] = "DiceRandom"
        concrete["mode"] = "on_board"


        return concrete
    
    def change_mode(self, _id, new_mode, mode_info=None):
        being = self.get_concrete_thing(_id)
        being["mode"] = new_mode


    def get_mode_info_of(self, mode):
        try:
            return self.modes_info[mode]
        except:
            debug_error(f"Can't get mode {mode} of {self.get_category()}",__name__)
            return None



