
from entity.object.building.commerce.Bank import Bank
from utils.beauty_print import bcolors
from game.Event import Event
from utils.common import GOVERNMENT, line, log_error, modes, prim_opt
from game.Board import Board
from game.Category import Category
from entity.livingbeing.person.Person import Person

from entity.object.building.education.Education import Education



class School(Education):

    class level:
        ELEMENTARY = "elementary_school"
        MIDDLE = "middle_school"
        HIGH = "high_school"

    def __init__(self) -> None:
        super().__init__()

        self.passing_grades = {
            self.level.ELEMENTARY: 5,
            self.level.MIDDLE: 4,
            self.level.HIGH: 3,
        }

        self.level_nick = {
            self.level.ELEMENTARY: "Ensino Básico",
            self.level.MIDDLE: "Ensino Fundamental",
            self.level.HIGH: "Ensino Médio"
        }

        self.diploms = list(self.passing_grades.keys())


    def new_concrete_thing(self):
        educ_build = super().new_concrete_thing()
        self.update_concrete(educ_build)
        # these two attributes need to be overwritten after the creation of other educ building
        educ_build[self.attr_coord] = self.get("Board").alphanum_to_coord("D3")
        educ_build[self.attr_name] = "Escola"
        return educ_build
    
    def update_concrete(self, school: dict):
        super().update_concrete(school)
        school[self.attr_price_per_round] = 75
        school[self.attr_price] = 800
        
    










    # def has_high_school(person_ref,)

# violence, endy scott

