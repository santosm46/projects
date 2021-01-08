
from game.Event import Event
from utils.beauty_print import bcolors, debug_error, print_debug
from entity.object.Object import Object
from utils.common import GOVERNMENT, line, log_error
from game.Board import Board
import random

class Building(Object):

    def __init__(self) -> None:
        super().__init__()
        self.attr_money = 'money'
        self.attr_name = 'name'

        self.first_interaction = 'Entrar no/na'
    
    images = {
        "Medicine": '💉',
        "Pedagogy": '📚',
        # "LawCourse": '⚖ ',
        # "LawCourse": ' 🖋️',
        "LawCourse": '🔏',
        "Engineer": '🔩',
        "School": '🏫',
        "House": ['🏠', '🏡'],
        "Hospital": '🏥',
        "Church": '⛪',
        "Bank": '🏦',
        "TownHall": '🏛️',
        "GasStation": '⛽',
        "Castle": '🏰',
        "SuperMarket": '🛒',
        "Casino": '🎰',
        "Cemetery": 'Ce'
    }

    def update_subscriber(self, reference: dict):
        super().update_subscriber(reference)
        event : Event = self.get("Event")
        # event.subscribe("entity_interacting_with_entity", reference, "put_person_on_building")
        
        event.subscribe("entity_interacting_with_building", reference, "on_building_interact")

    def on_building_interact(self, building_ref, person_ref, additional=None):
        log_error(f"This funcion [on_building_interact] needs to be overwritten",__name__,line())


    def get_image(self, _id=None):
        categ = self.get_category()
        image = self.images[categ]
        if(type(image) == list):
            return random.choice(image)
        return image

    def new_concrete_thing(self):
        building = super().new_concrete_thing()

        self.update_concrete(building)
        building[self.attr_owner] = GOVERNMENT

        return building
    
    
    def update_concrete(self, building: dict):
        super().update_concrete(building)

        board : Board = self.get("Board")
        
        self.add_attr_if_not_exists(building, self.attr_coord, board.alphanum_to_coord("A1"))
        self.add_attr_if_not_exists(building, self.attr_price, 125000000)
        self.add_attr_if_not_exists(building, self.attr_money, 0)
        self.add_attr_if_not_exists(building, self.attr_name  ,"Nome da construção")

    def remove_from_building(self, building_ref, person_ref):
        try:
            building = self.get_concrete_thing_by_ref(building_ref)
            person_class = self.get(person_ref["category"])
            person_class.change_mode(person_ref["id"], person_class.mode_on_board)
            board : Board = self.get("Board")
            close_free_spot = board.closer_free_spot_to(building[self.attr_coord])
            board.move_entity_to(person_class.reference(person_ref["id"]), alphanum=close_free_spot)
        except:
            log_error(f"Error trying to take person {person_ref} out of building {building_ref}",__name__,line())

    def is_person(self, person_categ):
        categ_mg = self.get("Category")
        return categ_mg.is_category_or_inside(person_categ, "Person")


    def entity_interaction(self, me_ref, other_ref, additional):
        self.put_person_on_building(me_ref, other_ref, additional)


    def put_person_on_building(self, building_ref, person_ref, additional=None):
        person_categ = person_ref["category"]
        if(not self.is_person(person_categ)):
            # only people can enter building
            return
        # print_debug("tentando colocar pessoa na escola 2")
        person_class = self.get(person_categ)
        mode_name = person_class.mode_on_building

        building_id = building_ref["id"]
        building = self.get_concrete_thing(building_id)
        person = person_class.get_concrete_thing(person_ref["id"])
        # can only put person if stepping at building
        if(person["coord"] != building["coord"]):
            return
        # print_debug("tentando colocar pessoa na escola 3")
        mode_info = person_class.get_mode_info_of(person_ref,mode_name)
        # print_beauty_json(mode_info)
        mode_info["building"] = self.reference(building_id)

        person_class.change_mode(person["id"], mode_name, self.reference(building_id))



    


    

