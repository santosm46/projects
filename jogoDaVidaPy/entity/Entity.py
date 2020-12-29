
from utils.beauty_print import print_beauty_json, print_debug
from Thing import Thing
from utils.common import log_error, line

class Entity(Thing):

    def __init__(self):
        super().__init__()

        self.attr_coord = 'coord'
        self.attr_dice_method = 'dice_method'
        self.attr_mode = "mode"
        self.attr_mode_info = "mode_info"


        self.modes_func = {}
        self.mode_on_board = "on_board"
    
    def set_factory(self, factory):
        super().set_factory(factory)
        self.update_concretes()
        self.update_subscribers()

    def new_concrete_thing(self):
        concrete = super().new_concrete_thing()
        self.update_concrete(concrete)
        return concrete
    
    # called by self.new_concrete_thing() to create it's attributes
    # and also by self.set_factory() -> update_concretes()
    #   just in case the game updated and a new attribute was created
    #   so the players receives the new attributes 
    def update_concrete(self, concrete: dict):
        super().update_concrete(concrete)
        coord = self.get("Board").alphanum_to_coord("A1")

        self.add_attr_if_not_exists(concrete, self.attr_dice_method, "DiceRandom")
        self.add_attr_if_not_exists(concrete, self.attr_coord, coord)
        self.add_attr_if_not_exists(concrete, self.attr_mode, self.mode_on_board)
        self.add_attr_if_not_exists(concrete, self.attr_mode_info, {})

    def roll_dice(self, _id, max_val=6):
        entity = self.get_concrete_thing(_id)
        dice = self.get(entity[self.attr_dice_method])
        return dice.roll_dice(max_val)

        

    def change_mode(self, _id, new_mode, mode_info=None):
        being = self.get_concrete_thing(_id)
        being[self.attr_mode] = new_mode
        if not mode_info:
            being[self.attr_mode_info][new_mode] = mode_info


    def get_mode_info_of(self, reference, mode):
        being = self.get_concrete_thing_by_ref(reference)
        # print_debug(f"being = ...",__name__)
        try:
            return being[self.attr_mode_info][mode]
        except:
            log_error(f"Can't get mode {mode} of {reference}",__name__, line())
            return None




