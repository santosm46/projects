

import random
from utils.common import line
from utils.beauty_print import debug_error
from game.Category import Category
from entity.livingbeing.person.npc.Npc import Npc


class Criminal(Npc):

    def __init__(self) -> None:
        super().__init__()

        self.prob_to_crime = {
            "PlayerIM": 50,
            "Robber": 10,
            "Killer": 1,
            # "Nobody": 100,
        }
    
    def make_crime_or_not(self, categ):
        if(categ in self.prob_to_crime.keys()):
            if(random.randrange(0,100) < self.prob_to_crime[categ]):
                return True
        return False
    
    def be_attacked(self, attacker_ref, me_ref, add_info='atacou'):
        if not super().be_attacked(attacker_ref, me_ref):
            return False
        if not self.make_crime_or_not(attacker_ref['category']): return False

        attacker_class = self.get(attacker_ref['category'])
        
        attacker_class.be_attacked(me_ref, attacker_ref, add_info='revidou ataque de')
        # return True
    # def update_subscriber(self, reference: dict):
    #     super().update_subscriber(reference)
    #     e = self.get("Event")
    #     e.subscribe("entity_moved_to_coord", reference, "commit_crime_on_person")

    def be_robbed(self, robber_ref, me_ref):
        if self.make_crime_or_not(robber_ref['category']):
            add_indo = 'foi roubado e atacou'
            if not super().be_robbed(robber_ref, me_ref): return False
        else:
            add_indo = 'sofreu tentativa de roubo e atacou'
        robber_class = self.get(robber_ref['category'])
        if self.make_crime_or_not(robber_ref['category']):
            return False
        
        return robber_class.be_attacked(me_ref, robber_ref, add_info=add_indo)
        # robber = self.get_concrete_thing_by_ref(robber_ref)
        # me = self.get_concrete_thing_by_ref(me_ref)
        # rob_name = robber["name"]
        # other_name = me["name"]
        # self.get('Logger').add('foi roubado e atacou')


    def entity_entered_my_spot(self, myself_ref, entity_ref):
        # return super().entity_entered_my_spot(myself_ref, entity_ref)
        categ_mg : Category = self.get("Category")

        if(not categ_mg.inside_of_category(entity_ref["category"], "Person")):
            return
        
        self.commit_crime(myself_ref, entity_ref)


    # to be overwritten
    def commit_crime(self, criminal_ref, person_ref):
        pass

    def move_to_and_interact_with(self, me_ref, other_ref):
        # it just robs people
        board : Board = self.get("Board")
        other = self.get_concrete_thing_by_ref(other_ref)
        board.move_entity_to(reference=self.reference(me_ref["id"]), coord=other["coord"])
        # print_debug(f"me_ref, other_ref = {me_ref}, {other_ref}",__name__,line())

        self.commit_crime(me_ref, other_ref)
    

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

        return super().gui_output(_id, function, question_id, params)
    

