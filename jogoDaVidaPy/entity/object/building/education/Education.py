
from game.Event import Event
from entity.object.building.commerce.Bank import Bank
from game.Category import Category
from utils.common import line, log_error, prim_opt
from game.Board import Board
from entity.livingbeing.person.Person import Person
from utils.beauty_print import bcolors, print_beauty_json, print_debug
from entity.object.building.Building import Building

class Education(Building):

    def __init__(self) -> None:
        super().__init__()
        self.attr_price_per_round = 'price_per_round'

        # to be overwitten
        self.grades = ['A','B','C','D','E','F']
        self.diploms = ['basic', 'medium', 'high']
        self.passing_grades = {
            'basic': 5,
            'medium': 4,
            'high': 3,
        }
        self.level_nick = {
            'basic': "Ensino Básico",
            'medium': "Ensino Fundamental",
            'high': "Ensino Médio"
        }


    def new_concrete_thing(self):
        education = super().new_concrete_thing()
        self.update_concrete(education)
        education_ref = self.reference(education["id"])
        self.update_subscriber(education_ref)
        return education


    def update_concrete(self, education: dict):
        super().update_concrete(education)
        self.add_attr_if_not_exists(education, self.attr_price_per_round, 75)

    def update_subscriber(self, educ_build_ref):
        super().update_subscriber(educ_build_ref)
        event : Event = self.get("Event")
        event.subscribe("entity_moved_to_coord", educ_build_ref, "put_person_on_building")
        event.subscribe("entity_choosing_spot", educ_build_ref, "on_entity_choosing_spot")
        event.subscribe("entity_interacting_with_building", educ_build_ref, "educ_building_interact")

    def custom_requirement_to_enter(self, building_data, person_ref, additional):
        return self.is_person(person_ref["category"])


# "inventory": {
#     "School": {
#         "Diploms": {
#             "elementary_school": school_id
#             "middle_school": school_id
#             "high_school": school_id
#         }
#     },

#     "College": {
#         "coursing": None,
#         "Diploms": {
#             "medicine": {
#                 "first_year": college_id,
#                 "second_year": college_id,
#             },
#         }
#     }
# }

    # all
    def highest_diplom(self):
        return self.diploms[len(self.diploms)-1]

    def number_to_grade(self, result):
        return self.grades[result % len(self.grades) -1]
    
    def person_has_highest_level(self, person_ref):
        return self.highest_diplom() == self.get_person_highest_diplom(person_ref)

    # for college class, it will take the diplom for the current course
    def get_person_highest_diplom(self, person_ref):
        diploms = self.get_person_diploms(person_ref)
        if(not diploms):
            return None

        max_idx = 0
        for diplom in diploms.keys():
            max_idx = max(max_idx, self.diploms.index(diplom))
        hightest = self.diploms[max_idx]
        return hightest
    
    # overwrite this to get diplom by course
    def get_person_diploms(self, person_ref):
        person = self.get_concrete_thing_by_ref(person_ref)
        # acess person inventory to take the highest school diplom
        this_categ = self.get_category()
        inventory = person["inventory"]
        
        # creates a place in the inventory to store the information for this education 
        #   instituition if it doesn't exist
        if(this_categ not in inventory):
            inventory[this_categ] = {"Diploms": {}}
            return None
        
        diploms = inventory[this_categ]["Diploms"]

        if(len(diploms) == 0): return None

        return diploms
    

    def can_pass_with(self, note: int, level: str):
        return note <= self.passing_grades[level]


    def next_level_of_person(self, person_ref):
        if self.person_has_highest_level(person_ref):
            return None
        diplom = self.get_person_highest_diplom(person_ref)
        if diplom is None:
            # if person doesn't have diploms, the next is the first
            return self.diploms[0]
        return self.diploms[self.diploms.index(diplom)+1]
    
    def next_level_nick_of(self, person_ref):
        level = self.next_level_of_person(person_ref)
        if not level:
            return "Finished Study"
        return self.level_nick[level]

    def advance_period(self, person_ref, new_level, education_id):
        person = self.get_concrete_thing_by_ref(person_ref)
        self.get_person_highest_diplom(person_ref)
        this_categ = self.get_category()
        person["inventory"][this_categ]["Diploms"][new_level] = education_id

    def is_person(self, person_categ):
        categ_mg : Category = self.get("Category")
        return categ_mg.is_category_or_inside(person_categ, "Person")


    def educ_building_interact(self, school_data, person_ref, additional=None):
        # building has to be school
        category = additional["category"]
        if(category != self.get_category()):
            return
        if(not self.is_person(person_ref["category"])):
            return
        person_class : Person = self.get(person_ref["category"])
        person_id = person_ref["id"]
        school = self.get_concrete_thing_by_ref(additional)
        name = school["name"]
        if(self.person_has_highest_level(person_ref)):
            person_class.change_mode(person_id,person_class.mode_on_board)
            person_class.gui_output(f"Você já tem todos os diplomas. Será removido da {name}",color=bcolors.WARNING,pause=True)
            self.remove_from_building(self.reference(school["id"]), person_ref)
            return

        person = self.get_concrete_thing_by_ref(person_ref)

        bank : Bank = self.get("Bank")
        price_per_round = school[self.attr_price_per_round]
        if(not bank.entity_can_pay(person, price_per_round)):
            person_class.gui_output(f"Você está sem dinheiro para as despesas da {name} (custo: {price_per_round}). Volte aqui mais tarde. [ENTER]",color=bcolors.WARNING,pause=True)
            self.remove_from_building(self.reference(school["id"]), person_ref)
            return

        level = self.next_level_of_person(person_ref)
        passing_note = self.passing_grades[level]
        text = f"Você está na {self.get_image()} {name} fazendo o {self.level_nick[level]}. Precisa de nota >= {self.number_to_grade(passing_note)} ({passing_note}) para passar"
        text += f"\n\t(Digite {prim_opt.LEAVE} para sair da {name}) (Taxa por rodada: {price_per_round})"
        person_class.gui_output(text, bcolors.HEADER)
        
        result = person_class.roll_dice(person_id)

        if(result is None):
            person_class.gui_output(f"Saindo da {name}...")
            self.remove_from_building(self.reference(school["id"]), person_ref)
            return

        grade = self.number_to_grade(result)

        text = f"\nVocê tirou {grade} ({result}) "
        if(self.can_pass_with(result, level)):
            new_level = self.next_level_of_person(person_ref)
            self.advance_period(person_ref, new_level, additional["id"])
            next_level_nick = self.next_level_nick_of(person_ref)
            if(self.person_has_highest_level(person_ref)):
                text += f"e se formou na {name}! Parabéns!"
                self.remove_from_building(self.reference(school["id"]), person_ref)
            else:
                text += f"e passou para o {next_level_nick} "
            color = bcolors.OKGREEN
        else:
            text += "e reprovou. Tente na próxima!"
            color = bcolors.FAIL
        
        bank.transfer_money_from_to(person_ref, additional, price_per_round)
        text += f"\nFoi descontado {price_per_round} da sua conta (ENTER para continuar) "
        person_class.gui_output(text, color=color, pause=True)
    

    


