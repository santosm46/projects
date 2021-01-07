from game.Logger import Logger
from game.DataStructure import DataStructure
from entity.object.building.commerce.Bank import Bank
import random
from game.Event import Event
from utils.beauty_print import bcolors, print_warning
from entity.livingbeing.LivingBeing import LivingBeing

class Person(LivingBeing):

    def __init__(self):
        super().__init__()
        self.MAX_HP = 10
        
        self.modes_func[self.mode_on_building] = self.interact_with_building

        self.attr_genre = "genre"
        self.attr_name = "name"
        self.attr_money = "money"

        self.interactions["be_robbed"] = "Roubar"

    def category_nick(self):
        return "Pessoa"
    
    
    def new_concrete_thing(self):
        person = super().new_concrete_thing()
        self.update_concrete(person)
        person[self.attr_hp] = self.MAX_HP
        person[self.attr_max_hp] = self.MAX_HP
        person[self.attr_mode_info] = {self.mode_on_board: None, self.mode_on_building: {"building":None}}
        return person


    def update_concrete(self, person: dict):
        super().update_concrete(person)

        info = self.get("RandomName").gen_person_info()
        
        self.add_attr_if_not_exists(person, self.attr_genre, info["genre"])
        self.add_attr_if_not_exists(person, self.attr_name, info["name"])
        self.add_attr_if_not_exists(person, self.attr_money, random.randrange(30,70)*5)
        self.add_attr_if_not_exists(person, self.attr_hp, self.MAX_HP)
        self.add_attr_if_not_exists(person, self.attr_max_hp, self.MAX_HP)
        self.add_attr_if_not_exists(person, self.attr_mode_info, {self.mode_on_board: None, self.mode_on_building: {"building":None}})


        
    def on_school_move(self, params=None):
        person = self.get_concrete_thing(params["id"])
        # name = person["name"]
        # print_warning(f"Pessoa {name} está na escola")
        event : Event = self.get("Event")
        event.notify("interact_with_building", self.reference(params["id"]))
    
    def interact_with_building(self, reference=None):
        info = self.get_mode_info_of(reference, self.mode_on_building)
        event : Event = self.get("Event")
        event.notify("entity_interacting_with_building", reference, info["building"])

    
    def kill_being(self, being_ref, cause=None):
        self.drop_inventory(being_ref)
        
        # categ = being_ref["category"]
        
        super().kill_being(being_ref, cause)

    def get_weapon_attack(self, being_ref):
        return 8

    def drop_inventory(self, being_ref):
        bank : Bank = self.get("Bank")
        bank.put_all_money_on_board(being_ref)
        # put_all_money_on_board

    def be_robbed(self, robber_ref, me_ref):
        # input(f"oque_isso -> {oque_isso}")
        e : Event = self.get("Event")
        bank : Bank = self.get("Bank")
        log : Logger = self.get("Logger")

        robber = self.get_concrete_thing_by_ref(robber_ref)

        me = self.get_concrete_thing_by_ref(me_ref)
        # e.notify("entity_interacting_with_entity", robber_ref, me_ref)
        rob_name = robber["name"]
        other_name = me["name"]
        money = random.randrange(50, 300, 10)
        if(me[self.attr_money] <= 0):
            return
        
        if(not bank.transfer_money_or_the_rest(me_ref, robber_ref, money)):
            money = me[self.attr_money]
        log.add(f"{rob_name} roubou {money} de {other_name}")
        