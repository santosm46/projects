
from entity.object.building.commerce.Bank import Bank
from utils.beauty_print import bcolors
from game.Event import Event
from utils.common import GOVERNMENT, line, log_error, modes, prim_opt
from game.Board import Board
from game.Category import Category
from entity.livingbeing.person.Person import Person

from entity.object.building.education.Education import Education



class School(Education):

    class school_level:
        ELEMENTARY = "elementary_school"
        MIDDLE = "middle_school"
        HIGH = "high_school"

    def __init__(self) -> None:
        super().__init__()

        self.passing_grades = {
            self.school_level.ELEMENTARY: 5,
            self.school_level.MIDDLE: 4,
            self.school_level.HIGH: 3,
        }

        self.level_nick = {
            self.school_level.ELEMENTARY: "Ensino Básico",
            self.school_level.MIDDLE: "Ensino Fundamental",
            self.school_level.HIGH: "Ensino Médio"
        }

        self.diploms = list(self.passing_grades.keys())
    
    def get_image(self, _id=None):
        return '🏫'

    def new_concrete_thing(self):
        school = super().new_concrete_thing()
        self.update_concrete(school)
        school_ref = self.reference(school["id"])
        self.update_subscriber(school_ref)
        
        return school
    
    # 
    def update_concrete(self, school: dict):
        super().update_concrete(school)
        board : Board = self.get("Board")
        school[self.attr_price_per_round] = 75
        school[self.attr_coord] = board.alphanum_to_coord("D3")
        school[self.attr_name] = "Escola"
        school[self.attr_price] = 800
        
    
    def update_subscriber(self, school_ref):
        super().update_subscriber(school_ref)
        event : Event = self.get("Event")
        event.subscribe("entity_moved_to_coord", school_ref, "put_person_on_school")
        event.subscribe("entity_choosing_spot", school_ref, "on_entity_choosing_spot")
        event.subscribe("entity_interacting_with_building", school_ref, "person_school_interaction")

    def is_person(self, person_categ):
        categ_mg : Category = self.get("Category")
        return categ_mg.is_category_or_inside(person_categ, "Person")

    def put_person_on_school(self, school_ref, person_ref, additional=None):
        person_categ = person_ref["category"]
        if(not self.is_person(person_categ)):
            # only people can enter school
            return
        # print_debug("tentando colocar pessoa na escola 2")
        person_class : Person = self.get(person_categ)
        mode_name = person_class.mode_on_building

        school_id = school_ref["id"]
        school = self.get_concrete_thing(school_id)
        person = person_class.get_concrete_thing(person_ref["id"])
        # can only put person if stepping at school
        if(person["coord"] != school["coord"]):
            return
        # print_debug("tentando colocar pessoa na escola 3")
        mode_info = person_class.get_mode_info_of(person_ref,mode_name)
        # print_beauty_json(mode_info)
        mode_info["building"] = self.reference(school_id)

        person_class.change_mode(person["id"], mode_name, self.reference(school_id))

    def take_person_out_of_school(self, school_ref, person_ref):
        try:
            school = self.get_concrete_thing_by_ref(school_ref)
            person_class : Person = self.get(person_ref["category"])
            person_class.change_mode(person_ref["id"], person_class.mode_on_board)
            board : Board = self.get("Board")
            close_free_spot = board.closer_free_spot_to(school[self.attr_coord])
            board.move_entity_to(person_class.reference(person_ref["id"]), alphanum=close_free_spot)
        except:
            log_error(f"Error trying to take person {person_ref} out of school {school_ref}",__name__,line())

    def on_entity_choosing_spot(self, school_data, person_ref, additional):
        # if Person can reach some school, it is gonna put it's coordenate
        # on the spots options for the player to enter it
        person_categ = person_ref["category"]
        if(not self.is_person(person_categ)):
            return
        # person with highest diplom can't enter school
        if(self.person_has_highest_level(person_ref)):
            return
        spots = additional["spots"]
        buildings = additional["buildings"]
        buildings_list : dict = additional["buildings_list"]
        range_ = additional["range"]

        school = self.get_concrete_thing(school_data["id"])
        board : Board = self.get("Board")
        my_valid_spots = board.get_valid_spots_for_range(school["coord"], range_)
        person = self.get_concrete_thing_by_ref(person_ref)
        person_alphanum_pos = board.coord_to_alphanum(person["coord"])

        # can only suggest school if person can reach school
        if(person_alphanum_pos not in my_valid_spots):
            return
        my_alphanum = board.coord_to_alphanum(school["coord"])
        spots.append(my_alphanum)
        school_name = school["name"]
        # for user to see only
        buildings_list[my_alphanum] = school_name
        buildings.append(f"{bcolors.HEADER}{my_alphanum}) {bcolors.WARNING}{school_name}{bcolors.ENDC}")
        

    # event.notify("entity_choosing_spot", 
        #     self.reference(player["id"]), {"spots":valid_spots, "buildings":buildings})

    

        # print_debug

    def person_school_interaction(self, school_data, person_ref, additional=None):
        # building has to be school
        category = additional["category"]
        if(category != self.get_category()):
            return
        if(not self.is_person(person_ref["category"])):
            return
        person_class : Person = self.get(person_ref["category"])
        person_id = person_ref["id"]
        if(self.person_has_highest_level(person_ref)):
            person_class.change_mode(person_id,modes.ON_BOARD)
            return

        school = self.get_concrete_thing_by_ref(additional)
        person = self.get_concrete_thing_by_ref(person_ref)
        name = school["name"]

        bank : Bank = self.get("Bank")
        price_per_round = school[self.attr_price_per_round]
        if(not bank.entity_can_pay(person, price_per_round)):
            person_class.gui_output(f"Você está sem dinheiro para as despesas da {name} (custo: {price_per_round}). Volte aqui mais tarde. [ENTER]",color=bcolors.WARNING,pause=True)
            self.take_person_out_of_school(self.reference(school["id"]), person_ref)
            return

        level = self.next_level_of_person(person_ref)
        passing_note = self.passing_grades[level]
        text = f"Você está na {name} cursando o {self.level_nick[level]}. Precisa de nota >= {self.number_to_grade(passing_note)} ({passing_note}) para passar"
        text += f"\n\t(Digite {prim_opt.LEAVE} para sair da {name}) (Taxa por rodada: {price_per_round})"
        person_class.gui_output(text, bcolors.HEADER)
        
        result = person_class.roll_dice(person_id)

        if(result is None):
            person_class.gui_output("Saindo da escola...")
            self.take_person_out_of_school(self.reference(school["id"]), person_ref)
            return

        grade = self.number_to_grade(result)

        text = f"\nVocê tirou {grade} ({result}) "
        if(self.can_pass_with(result, level)):
            new_level = self.next_level_of_person(person_ref)
            self.give_diplom_to_person(person_ref, new_level, additional["id"])
            next_level_nick = self.next_level_nick_of(person_ref)
            if(self.person_has_highest_level(person_ref)):
                text += f"e se formou na {name}! Parabéns!"
                self.take_person_out_of_school(self.reference(school["id"]), person_ref)
            else:
                text += f"e passou para o {next_level_nick} "
            color = bcolors.OKGREEN
        else:
            text += "e reprovou. Tente na próxima!"
            color = bcolors.FAIL
        
        bank.transfer_money_from_to(person_ref, additional, price_per_round)
        text += f"\nFoi descontado {price_per_round} da sua conta (ENTER para continuar) "
        person_class.gui_output(text, color=color, pause=True)
    

    





    # def has_high_school(person_ref,)

# violence, endy scott

