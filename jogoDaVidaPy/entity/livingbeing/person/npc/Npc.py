from game.Event import Event
from entity.livingbeing.person.Person import Person


class Npc(Person):
    def __init__(self):
        super().__init__()
    

    def get_image(self, _id=None):
        return '👤'
    

    def update_subscriber(self, reference: dict):
        super().update_subscriber(reference)
        # e : Event = self.get("Event")
        # e.subscribe("new_round", reference, "reduce_energy")


        
