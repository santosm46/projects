
# from game.Logger import Logger
from entity.livingbeing.person.Person import Person
from utils.beauty_print import debug_error, print_debug
from game.Board import Board
from game.Logger import Logger
from entity.object.building.commerce.Bank import Bank
import random
from utils.common import line, log_error
from entity.livingbeing.person.npc.criminal.Criminal import Criminal
from game.Category import Category

class Robber(Criminal):

    def __init__(self) -> None:
        super().__init__()
    
    def commit_crime(self, criminal_ref, person_ref):
        if(self.make_crime_or_not(person_ref["category"])):
            self.rob_person(criminal_ref, person_ref)
    
    def category_nick(self):
        return 'Ladrão'
    

    def rob_person(self, me_ref, other_ref):

        person_class : Person = self.get(other_ref['category'])

        person_class.be_robbed(me_ref, other_ref)

