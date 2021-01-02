from entity.object.building.education.School import School
from utils.common import valid_number
from utils.beauty_print import bcolors, input_question, print_number_list
from entity.livingbeing.person.Person import Person
from entity.object.building.education.Education import Education

class College(Education):

    class level:
        FIRST_YEAR = "first_year"
        SECOND_YEAR = "second_year"
        CBT = "CBT"
    
    class courses:
        MEDICINE = "Medicine"
        PEDAGOY = "Pedagogy"
        LAW_COURSE = "LawCourse"
        ENGINEER = "Engineer"

    def __init__(self) -> None:
        super().__init__()

        self.passing_grades = {
            self.level.FIRST_YEAR: 3,
            self.level.SECOND_YEAR: 3,
            self.level.CBT: 2,
        }

        self.level_nick = {
            self.level.FIRST_YEAR: "Primeiro ano",
            self.level.SECOND_YEAR: "Segundo ano",
            self.level.CBT: "TCC"
        }

        self.course_nicks = {
            self.courses.MEDICINE: "Medicina",
            self.courses.PEDAGOY: "Pedagogia",
            self.courses.LAW_COURSE: "Direito",
            self.courses.ENGINEER: "Engenharia",
        }
        
        self.diploms = list(self.passing_grades.keys())

    def course_nick(self):
        return self.course_nicks[self.get_category()]
    
    def new_concrete_thing(self):
        educ_build = super().new_concrete_thing()
        educ_build[self.attr_price_per_round] = 100
        educ_build[self.attr_name] = f"Faculdade de {self.course_nick()}"
        return educ_build
    
    def custom_requirement_to_enter(self, building_data, person_ref, additional):
        if not super().custom_requirement_to_enter(building_data, person_ref, additional):
            return False
        school : School = self.get("School")
        return school.person_has_highest_level(person_ref)


class Medicine(College):
    def __init__(self) -> None:
        super().__init__()
    def new_concrete_thing(self):
        educ_build = super().new_concrete_thing()
        # these two attributes need to be overwritten after the creation of other educ building
        educ_build[self.attr_coord] = self.get("Board").alphanum_to_coord("C12")
        return educ_build
    
class Pedagogy(College):
    def __init__(self) -> None:
        super().__init__()
    def new_concrete_thing(self):
        educ_build = super().new_concrete_thing()
        # these two attributes need to be overwritten after the creation of other educ building
        educ_build[self.attr_coord] = self.get("Board").alphanum_to_coord("D12")
        return educ_build
    
class LawCourse(College):
    def __init__(self) -> None:
        super().__init__()
    def new_concrete_thing(self):
        educ_build = super().new_concrete_thing()
        # these two attributes need to be overwritten after the creation of other educ building
        educ_build[self.attr_coord] = self.get("Board").alphanum_to_coord("C13")
        return educ_build
    
class Engineer(College):
    def __init__(self) -> None:
        super().__init__()
    def new_concrete_thing(self):
        educ_build = super().new_concrete_thing()
        # these two attributes need to be overwritten after the creation of other educ building
        educ_build[self.attr_coord] = self.get("Board").alphanum_to_coord("D13")
        return educ_build
    



    # def set_course(self, person_ref, college_ref, course):
    #     person = self.get_concrete_thing_by_ref(person_ref)
    #     categ = college_ref["category"]
    #     self.update_inventory(person["inventory"], categ, course)
    #     person["inventory"][categ]["studying"] = course

    # def choose_course(self, person_ref):
    #     person_class : Person = self.get(person_ref["category"])
    #     courses = list(self.course_nick.values())
    #     while True:
    #         person_class.gui_output("\n\tCursos",color=bcolors.HEADER)
    #         print_number_list(courses)
    #         person_class.gui_output(f"Escolha um dos cursos: (ENTER para cancelar) ")
    #         option = input_question("")
    #         if(len(option) == 0):
    #             return None
    #         if(valid_number(option, 1, len(courses))):
    #             break
    #     return list(self.course_nick.keys())[int(option)-1]


    # def update_inventory(self, inventory, category, course):
    #     # creates a place in the inventory to store the information for this education 
    #     #   instituition if it doesn't exist
    #     if(category not in inventory):
    #         inventory[category] = {"Diploms": {}}
    #         return True
    #     if(course not in inventory["Diploms"]):
    #         inventory[category][course] = {}
    #         return True
    #     return False



# talvez sobrescrever
    # def next_level_of_person(self, person_ref):
    #     if self.person_has_highest_level(person_ref):
    #         return None
    #     diplom = self.get_person_highest_diplom(person_ref)
    #     if diplom is None:
    #         # if person doesn't have diploms, the next is the first
    #         return self.diploms[0]
    #     return self.diploms[self.diploms.index(diplom)+1]




