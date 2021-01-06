

import random
from game.Category import Category
from entity.livingbeing.person.npc.Npc import Npc


class Criminal(Npc):

    def __init__(self) -> None:
        super().__init__()

        self.prob_to_crime = {
            "PlayerIM": 60,
            "Robber": 10,
            # "Nobody": 100,
        }
    
    def make_crime_or_not(self, categ):
        if(categ in self.prob_to_crime.keys()):
            if(random.randrange(0,100) < self.prob_to_crime[categ]):
                return True
        return False
    
    # def update_subscriber(self, reference: dict):
    #     super().update_subscriber(reference)
    #     e = self.get("Event")
    #     e.subscribe("entity_moved_to_coord", reference, "commit_crime_on_person")

    def entity_entered_my_spot(self, myself_ref, entity_ref):
        # return super().entity_entered_my_spot(myself_ref, entity_ref)
        categ_mg : Category = self.get("Category")

        if(not categ_mg.inside_of_category(entity_ref["category"], "Person")):
            return
        
        self.commit_crime(myself_ref, entity_ref)


    # to be overwritten
    def commit_crime(self, criminal_ref, person_ref):
        pass

