
from game.Board import Board
from game.Event import Event

from entity.object.building.commerce.Commerce import Commerce

class Bank(Commerce):


    def __init__(self) -> None:
        super().__init__()
    

    def get_image(self, _id=None):
        return '🏦'
    
    # def update_subscriber(self, school_ref):
        # event : Event = self.get("Event")
        # event.subscribe("entity_moved_to_coord", school_ref, "put_person_on_school")
        # event.subscribe("building_board_print", school_ref, "on_building_board_print")
        # event.subscribe("entity_choosing_spot", school_ref, "on_entity_choosing_spot")
        # event.subscribe("entity_interacting_with_building", school_ref, "person_school_interaction")



    def new_concrete_thing(self):
        bank = super().new_concrete_thing()
        self.update_concrete(bank)
        board : Board = self.get("Board")
        bank[self.attr_name] = "Banco"
        bank[self.attr_money] = 10000000
        bank[self.attr_coord] = board.alphanum_to_coord("H7")
        self.update_subscriber(self.reference(bank["id"]))

        return bank

    
    def update_concrete(self, building: dict):
        super().update_concrete(building)


