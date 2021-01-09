from math import trunc
from utils.common import valid_number
from entity.object.Food import Food
from game.Logger import Logger
from game.DataStructure import DataStructure
from entity.object.building.commerce.Bank import Bank
import random
from game.Event import Event
from utils.beauty_print import bcolors, get_number_list, input_question, print_number_list, print_warning
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


        
    # def on_school_move(self, params=None):
    #     person = self.get_concrete_thing(params["id"])
    #     # name = person["name"]
    #     # print_warning(f"Pessoa {name} está na escola")
    #     event : Event = self.get("Event")
    #     event.notify("interact_with_building", self.reference(params["id"]))
    
    def interact_with_building(self, reference=None):
        info = self.get_mode_info_of(reference, self.mode_on_building)
        event : Event = self.get("Event")
        event.notify("entity_interacting_with_building", reference, info["building"])

    
    def kill_being(self, being_ref, cause=None):
        self.drop_inventory(being_ref)
        
        # categ = being_ref["category"]
        
        super().kill_being(being_ref, cause)

    def get_weapon_attack(self, being_ref):
        return 0

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
    
    def eat_food(self, being_id):

        being_ref = self.reference(being_id)
        person_class : Person = self.get(self.get_category())

        food : Food = self.get("Food")

        while True:

            food_inv : dict = food.get_food_inventory_of(being_ref)

            # will not show food with zero values
            food_not_zero = {}
            for k,v in food_inv.items():
                if v > 0:
                    food_not_zero[k]=v
            food_inv = food_not_zero

            options, food_dict, food_names = food.food_categs_to_options(list(food_inv.keys()), False, food_inv)

            if(len(options) == 0): return True

            person_class.gui_output(get_number_list(options, "\nEscolha algo para comer [ENTER para sair]\n"))

            while True:
                person_class.gui_output("Opção: ", color=bcolors.OKBLUE, end='')
                opt = person_class.gui_input(being_id, 'eat_food', 1, options)
                if(len(opt) == 0): return True
                if(valid_number(opt, 1, len(options))):
                    break
            
            opt = int(opt)-1

            chosen_food = food_names[opt]

            while True:
                max_food_qtd = food_inv[chosen_food]
                person_class.gui_output("Quantidade [ENTER para sair]: ", color=bcolors.OKBLUE,end='')
                qtd = person_class.gui_input(being_id, 'eat_food', 2, max_food_qtd)
                if(len(qtd) == 0): return True
                
                # not eat this food, so choose other
                if(qtd == '0'):
                    break

                if(valid_number(qtd, 1, max_food_qtd)):
                    qtd = int(qtd)
                    survived = food.apply_food_properties_to(being_ref, chosen_food, qtd)
                    image = food_dict[opt]['image']
                    if not survived:
                        return False
                    self.get("GameManager").print_game()
                    person_class.gui_output(f"\nVocê comeu {qtd} {image}", color=bcolors.OKGREEN)
                    break
                    


