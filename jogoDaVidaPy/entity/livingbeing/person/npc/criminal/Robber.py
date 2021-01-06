
# from game.Logger import Logger
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
    
    
    def gui_input(self, _id=None, function=None, question_id=None, params=None):
        # super().gui_input()
        categ_mg : Category = self.get("Category")
        # look for person to rob, or a spot to go
        if function == "choose_spot_to_move":
            entities = params["entities_to_interact"]
            for idx in range(len(entities)):
                # print_debug(f"entities= {entities}",__name__,line())
                to_return = str(idx+1)
                categ = entities[idx]["ref"]["category"]

                if(self.make_crime_or_not(categ)):
                    return to_return
                # elif(categ_mg.inside_of_category(categ, "Criminal")):
                #     return to_return
            go_to = random.choice(params["valid_spots"])
            # input(f"{self.get_category()} Achei ninguem para roubar, vou andar para {go_to}")
            return go_to

        log_error(f"There is no action made for {function}",__name__,line())
        return None
    
    def rob_person(self, me_ref, other_ref):
        # input(f"oque_isso -> {oque_isso}")
        e : Event = self.get("Event")
        bank : Bank = self.get("Bank")
        log : Logger = self.get("Logger")

        me = self.get_concrete_thing_by_ref(me_ref)

        other = self.get_concrete_thing_by_ref(other_ref)
        # e.notify("entity_interacting_with_entity", me_ref, other_ref)
        me_name = me["name"]
        other_name = other["name"]
        money = random.randrange(50, 300, 10)
        if(other[self.attr_money] <= 0):
            return
        
        if(not bank.transfer_money_or_the_rest(other_ref, me_ref, money)):
            money = other[self.attr_money]
        log.add(f"{me_name} roubou {money} de {other_name}")
        # else:
        #     log.add(f"{me_name} tentou roubar {money} de {other_name}, não tinha o valor e roubou tudo")
    
    

    def move_to_and_interact_with(self, me_ref, other_ref):
        # it just robs people
        board : Board = self.get("Board")
        other = self.get_concrete_thing_by_ref(other_ref)
        board.move_entity_to(reference=self.reference(me_ref["id"]), coord=other["coord"])
        # print_debug(f"me_ref, other_ref = {me_ref}, {other_ref}",__name__,line())

        self.rob_person(me_ref, other_ref)
        # self.rob_person(self, me_ref)

    # def entity_interaction(self, me_ref, other_ref, additional):

    #     log : Logger
