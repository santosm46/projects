
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

        self.first_interaction = 'Interagir com'

    
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


    def on_entity_choosing_spot(self, interested_ref, person_ref, additional):
        # if Person can reach some building, it is gonna put it's reference for the
        # entity to interact with it

        # this is for some entities_to_interact with special restrictions
        # they will overwrite the function custom_requirement_to_enter()
        if(not self.custom_requirement_to_enter(interested_ref, person_ref, additional)):
            return
        entities_to_interact : list = additional["entities_to_interact"]
        range_ : int = additional["range"]

        entity_conc = self.get_concrete_thing(interested_ref["id"])
        board = self.get("Board")
        my_valid_spots = board.get_valid_spots_for_range(entity_conc["coord"], range_)
        person = self.get_concrete_thing_by_ref(person_ref)
        person_alphanum_pos = board.coord_to_alphanum(person["coord"])

        # can only suggest entity_conc if entity can reach entity_conc
        if(person_alphanum_pos not in my_valid_spots):
            return

        building_name = entity_conc["name"]

        entities_to_interact.append({
            "ref": interested_ref,
            "interaction": f"{self.first_interaction} {building_name}",
        })

    


