
# from game.Event import Event
# from game.Logger import Logger
# from game.Board import Board
from utils.beauty_print import print_beauty_json, print_debug
from Thing import Thing
from utils.common import log_error, line
import random

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
        self.interactions = {}

    
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
        # from game.Board import Board
        super().update_concrete(concrete)
        board : Board = self.get("Board")

        while True:
            r = random.randint(0, board.rows()-1)
            c = random.randint(0, board.columns()-1)
            if(not board.is_city_view(r, c)):
                break
        # .alphanum_to_coord("A1")
        coord = board.rc_to_coord(r, c)
        coord = board.closer_free_spot_to(coord)
        coord = board.alphanum_to_coord(coord)

        self.add_attr_if_not_exists(concrete, self.attr_dice_method, "DiceRandom")
        self.add_attr_if_not_exists(concrete, self.attr_coord, coord)
        self.add_attr_if_not_exists(concrete, self.attr_mode, self.mode_on_board)
        self.add_attr_if_not_exists(concrete, self.attr_mode_info, {})

    
    def update_subscriber(self, reference: dict):
        super().update_subscriber(reference)
        event : Event = self.get("Event")
        event.subscribe("entity_choosing_spot", reference, "on_entity_choosing_spot")
        event.subscribe("entity_interacting_with_entity", reference, "on_entity_interacting_with_entity")
        event.subscribe("entity_moved_to_coord", reference, "on_entity_moved_to_coord")

    def delete_myself(self, myself_ref):
        self.unsubscribe_entity(myself_ref)
        data = self.get("DataStructure")
        data.delete_concrete_thing(myself_ref)


    def unsubscribe_entity(self, reference: dict):
        # from game.Event import Event
        super().unsubscribe_entity(reference)
        event : Event = self.get("Event")
        event.unsubscribe("entity_choosing_spot", reference)
        event.unsubscribe("entity_interacting_with_entity", reference)
        event.unsubscribe("entity_moved_to_coord", reference)


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
            # print_debug(f"being-ref = {reference}, mode= {mode}",__name__)
            return being[self.attr_mode_info][mode]
        except:
            log_error(f"Can't get mode {mode} of {reference}",__name__, line())
            return None

    def on_entity_moved_to_coord(self, interested_ref, entity_ref, additional=None):
        me = self.get_concrete_thing_by_ref(interested_ref)
        other = self.get_concrete_thing_by_ref(entity_ref)
        if(interested_ref == entity_ref): return

        if(me["coord"] == other["coord"]):
            self.entity_entered_my_spot(interested_ref, entity_ref)
    
    def entity_entered_my_spot(self, myself_ref, entity_ref):
        # this is to be overwritten
        pass

    def on_entity_choosing_spot(self, interested_ref, person_ref, additional=None):
        # if Person can reach some building, it is gonna put it's reference for the
        # entity to interact with it

        # this is for some entities_to_interact with special restrictions
        # they will overwrite the function custom_requirement_to_interact()
        if(not self.custom_requirement_to_interact(interested_ref, person_ref, additional)):
            return
        entities_to_interact : list = additional["entities_to_interact"]
        range_ : int = additional["range"]

        # print_debug(f"interested_ref = {interested_ref} person_ref = {person_ref}",__name__,line())
        
        entity_conc = self.get_concrete_thing(interested_ref["id"])
        if(not entity_conc):
            log_error(f"entity {interested_ref} isn't in the game, subscribers need to be cleaned",__name__,line())
            return
        
        board = self.get("Board")
        my_valid_spots = board.get_valid_spots_for_range(entity_conc["coord"], range_)
        person = self.get_concrete_thing_by_ref(person_ref)
        person_alphanum_pos = board.coord_to_alphanum(person["coord"])

        # can only suggest entity_conc if entity can reach entity_conc
        if(person_alphanum_pos not in my_valid_spots):
            return

        building_name = entity_conc["name"]

        addi = ''
        if interested_ref['category'] == 'PlayerIM':
            addi = self.first_interaction
        else:
            addi = 'Pessoa'

        entities_to_interact.append({
            "ref": interested_ref,
            "interaction": f"{addi} {building_name}",
            # "interaction": f"{self.first_interaction} {building_name}",
        })

    def on_entity_interacting_with_entity(self, target_ref, causer_ref, additional=None):
        # checks if it's target is this category
        # if(self.get_category() == 'SuperMarket'):
        # print_debug(f"Vamos ver se vai entrar no {self.get_category()}.   ({__name__}:{line()})")

        if(target_ref["category"] != self.get_category()):
            return
        self.entity_interaction(target_ref, causer_ref, additional)


    # this is to be overwritten, 
    def entity_interaction(self, me_ref, other_ref, additional=None):
        pass
        # log : Logger = self.get("Logger")
        # categ = self.get_category()
        # log.add(f"sou do tipo {categ} e estou interagindo com -> {other_ref}")


    # this is for some entities_to_interact with special restrictions
    # they will overwrite this function
    def custom_requirement_to_interact(self, interested_ref, person_ref, additional=None):
        # can't interact with it self
        if(interested_ref == person_ref):
            return False
        # can't interact if has no interactions
        if(len(self.get_interactions_for(person_ref)) == 0):
            return False
        return True

    def get_interactions_for(self, entity_ref):
        return self.interactions
    
    