from entity.object.building.commerce.Bank import Bank
from utils.beauty_print import bcolors
from entity.livingbeing.person.Person import Person
from game.Board import Board
from utils.common import MOCK_ID, UBI
from game.DataStructure import DataStructure
from entity.object.building.Building import Building

class Jail(Building):
    
    def new_concrete_thing(self):

        cemetery = super().new_concrete_thing()
        self.update_concrete(cemetery)
        board : Board = self.get("Board")
        cemetery["id"] = MOCK_ID
        cemetery[self.attr_name] = "Cadeia"
        # cemetery[self.attr_money] = 100
        cemetery[self.attr_owner] = 1000000
        cemetery[self.attr_coord] = board.alphanum_to_coord("J11")
        self.update_subscriber(self.reference(cemetery["id"]))

        return cemetery
    
    def put_person_on_building(self, person_ref, building_ref, years_in_prision):
        if not super().put_person_on_building(person_ref, building_ref):
            return
        person_class : Person = self.get(person_ref["category"])
        mode_info = person_class.get_mode_info_of(person_ref, person_class.mode_on_building)
        mode_info['years_in_prision'] = years_in_prision

    

    def on_building_interact(self, building_ref, person_ref, additional=None):
        pclass : Person = self.get(person_ref["category"])
        log = self.get('Logger')

        bank : Bank = self.get('Bank')
        bank.decrease_person_money(person_ref, UBI)

        mode_info = pclass.get_mode_info_of(person_ref, pclass.mode_on_building)


        name = pclass.person_name(person_ref)

        remaing = mode_info['years_in_prision']
        mode_info['years_in_prision'] -= 1
        if remaing == 0:
            log.add(f"{name} Cumpriu a pena na cadeia e será solto", color=bcolors.OKGREEN)
            self.remove_from_building(building_ref, person_ref)
            return
        remain_info = f'faltam {remaing} anos' if remaing>1 else 'falta 1 ano'
        if pclass.get_category() == 'PlayerIM':
            log.add(f"{name} cumpriu 1 ano na cadeia, {remain_info}")




