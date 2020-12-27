
from beauty_print import print_debug, bcolors
from Education import Education
from Event import Event
from common import GOVERNMENT
from Board import Board
from Category import Category
from Person import Person

class School(Education):

    def __init__(self) -> None:
        super().__init__()

    def set_factory(self, factory):
        super().set_factory(factory)
        

    def new_concrete_thing(self):
        event : Event = self.factory.gi("Event")
        school = super().new_concrete_thing()
        board : Board = self.factory.get_instance("Board")

        school["coord"] = board.alphanum_to_coord("D3")
        school["name"] = "Escola"
        school["selling_price"] = 800
        school["price_per_round"] = 75
        school_ref = self.reference(school["id"])
        event.subscribe("entity_moved_to_coord", school_ref, "put_person_on_school")
        event.subscribe("building_board_print", school_ref, "on_building_board_print")
        event.subscribe("entity_choosing_spot", school_ref, "on_entity_choosing_spot")
        
        
        return school
    
    def is_person(self, person_categ):
        categ_mg : Category = self.factory.gi("Category")
        return categ_mg.is_category_or_inside(person_categ, "Person")

    def put_person_on_school(self, school_data, person_ref, additional=None):
        person_categ = person_ref["category"]
        if(not self.is_person(person_categ)):
            # only people can enter school
            return
        mode_name = "on_school"
        person_class : Person = self.factory.gi(person_categ)
        person_id = person_ref["id"]

        school_id = school_data["id"]
        school = self.get_concrete_thing(school_id)
        person_concr = person_class.get_concrete_thing(person_id)
        # can only put person if stepping at school
        if(person_concr["coord"] != school["coord"]):
            return

        mode_info = person_class.get_mode_info_of(mode_name)
        mode_info["school"] = {"id": school_id}

        person_class.change_mode(person_id, mode_name)

    def on_entity_choosing_spot(self, school_data, person_ref, additional):
        # if Person can reach some school, it is gonna put it's coordenate
        # on the spots options for the player
        person_categ = person_ref["category"]
        if(not self.is_person(person_categ)):
            return
        spots = additional["spots"]
        buildings = additional["buildings"]
        range_ = additional["range"]

        school_id = school_data["id"]
        school = self.get_concrete_thing(school_id)
        board : Board = self.factory.gi("Board")
        my_valid_spots = board.get_valid_spots_for_range(school["coord"], range_)
        person_id = person_ref["id"]
        person_class : Person = self.factory.gi(person_categ)
        person_concr = person_class.get_concrete_thing(person_id)
        person_alphanum_pos = board.coord_to_alphanum(person_concr["coord"])
        person_class : Person = self.factory.gi(person_categ)

        # can only suggest school if person can reach school
        if(person_alphanum_pos not in my_valid_spots):
            return
        my_alphanum = board.coord_to_alphanum(school["coord"])
        spots.append(my_alphanum)
        school_name = school["name"]
        # for user to see only
        buildings.append(f"{bcolors.HEADER}{my_alphanum}) {bcolors.WARNING}{school_name}{bcolors.ENDC}")
        

    # event.notify("entity_choosing_spot", 
        #     self.reference(player["id"]), {"spots":valid_spots, "buildings":buildings})

    def on_building_board_print(self, interested=None, event_causer=None, additional=None):
        # pegar lista de id's dos jogadores IM
        escolas : dict = self.get_dict_list()["concrete_things"]

        category = self.get_category()
        if(category not in additional):
            additional[category] = []
        
        # print_debug(f"chegou na escola -> {escolas}",__name__)

        for building_id, building in escolas.items():
            additional[category].append({
                "image": '🏫',
                "coord": building["coord"]
            })

        # print_debug

