
# from game.Logger import Logger
from os import kill
from entity.object.weapon.Weapon import Weapon
from entity.livingbeing.person.Person import Person
from utils.beauty_print import debug_error, print_beauty_json, print_debug
from game.Board import Board
from game.Logger import Logger
from entity.object.building.commerce.Bank import Bank
import random
from utils.common import line, log_error
from entity.livingbeing.person.npc.criminal.Criminal import Criminal
from game.Category import Category

class Killer(Criminal):

    def __init__(self) -> None:
        super().__init__()
    
    def commit_crime(self, criminal_ref, person_ref):
        if(self.make_crime_or_not(person_ref["category"])):
            self.kill_person(criminal_ref, person_ref)
    
    def category_nick(self):
        return 'Assassino'
    

    def kill_person(self, me_ref, other_ref):

        person_class : Person = self.get(other_ref['category'])

        person_class.be_attacked(me_ref, other_ref)


    def new_concrete_thing(self):
        killer = super().new_concrete_thing()

        # we : Weapon = self.get('Weapon')

        killer['inventory'] = {
            "Weapon": {
                "Pistol": 1
            }
        }

        killer['hp'] = 13

        # print_beauty_json(killer)

        # we.add_to_inventory(self.reference(killer['id']), 'Pistol', 1)

        return killer


    def risk_of_death(self, being_concr=None, being_ref=None) -> int:
        return 0

