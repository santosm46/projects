
from utils.beauty_print import print_beauty_json, print_debug
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
        return education


    def update_concrete(self, education: dict):
        super().update_concrete(education)
        self.add_attr_if_not_exists(education, self.attr_price_per_round, 75)

    
    def get_person_highest_diplom(self, person_ref, mock_person=None):
        if mock_person is None:
            
            person = self.get_concrete_thing_by_ref(person_ref)
            # return person_ref
        else:
            person = mock_person
        # acess person inventory to take the highest school diplom
        # person = self.mock_or_not(person_ref, mock_person)
        # person = self.get_concrete_thing_by_ref(person_ref)
        parent_categ = "Education"
        this_categ = self.get_category()
        inventory = "inventory"
        if(inventory not in person):
            person[inventory] = {}
        if(parent_categ not in person[inventory]):
            person[inventory][parent_categ] = {}
        school = person[inventory][parent_categ]
        if(this_categ not in school):
            school[this_categ] = {
                "Diploms": {}
            }
            return None


        
        diploms = school[this_categ]["Diploms"]

        if(len(diploms) == 0): return None

        max_idx = 0
        for diplom in diploms.keys():
            max_idx = max(max_idx, self.diploms.index(diplom))
        hightest = self.diploms[max_idx]
        return hightest
    

    def highest_diplom(self):
        return self.diploms[len(self.diploms)-1]

    def number_to_grade(self, result):
        return self.grades[result % len(self.grades) -1]
    
    def person_has_highest_level(self, person_ref):
        return self.highest_diplom() == self.get_person_highest_diplom(person_ref)

    def mock_or_not(self, person_ref, mock_person):
        if mock_person is None:
            # print_debug(f"person_ref = {person_ref} e...",__name__)
            # print_beauty_json(person_ref)
            return self.get_concrete_thing_by_ref(person_ref)
            # return person_ref
        else:
            return mock_person

    def can_pass_with(self, note: int, level: str):
        return note <= self.passing_grades[level]


    def next_level_of_person(self, person_ref, mock_person=None):
        # try:
        if self.person_has_highest_level(person_ref):
            # print_debug(f"pessoa tem maior diploma",__name__)
            return None
        diplom = self.get_person_highest_diplom(person_ref, mock_person=None)
        if diplom is None:
            # if person doesn'r have diploms, the next is the first
            return self.diploms[0]
        return self.diploms[self.diploms.index(diplom)+1]
        # except:
        #     return None
    
    def next_level_nick_of(self, person_ref):
        level = self.next_level_of_person(person_ref)
        if not level:
            return "Finished Study"
        return self.level_nick[level]

    def give_diplom_to_person(self, person_ref, new_level, education_id, mock_person=None):
        person = self.mock_or_not(person_ref, mock_person)
        self.get_person_highest_diplom(person_ref, mock_person)
        parent_categ = "Education"
        this_categ = self.get_category()
        person["inventory"][parent_categ][this_categ]["Diploms"][new_level] = education_id

