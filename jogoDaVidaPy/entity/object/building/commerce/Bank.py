
from utils.common import MOCK_ID, line, log_error
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
        bank["id"] = MOCK_ID
        bank[self.attr_name] = "Banco"
        bank[self.attr_money] = 10000000
        # bank[self.attr_owner] = 10000000
        bank[self.attr_coord] = board.alphanum_to_coord("H7")
        self.update_subscriber(self.reference(bank["id"]))

        return bank

    
    def update_concrete(self, building: dict):
        super().update_concrete(building)

    def not_has_attr_money(self, entity):
        if(self.attr_money not in entity):
            log_error(f"Can't transfer money, entity doesn't have attr_money\n     -> {entity}",__name__,line())
            return False

    def transfer_money_from_to(self, sender_ref, receiver_ref, amount):
        
        sender = self.get_concrete_thing_by_ref(sender_ref)
        receiver = self.get_concrete_thing_by_ref(receiver_ref)

        # sender has to have sufficient money
        # already checks if it has attr money
        if(not self.entity_can_pay(sender, amount)):
            return False

        # receiver needs to have attr money
        if(self.not_has_attr_money(receiver)):
            return False

        sender[self.attr_money] -= amount
        receiver[self.attr_money] += amount

        return True


    def entity_can_pay(self, entity_concr: dict, amount: int):
        if self.not_has_attr_money(entity_concr):
            return False
        
        money = entity_concr[self.attr_money]

        return money >= amount
        

    def transfer_all_money(self, sender_ref, receiver_ref):
        sender = self.get_concrete_thing_by_ref(sender_ref)
        receiver = self.get_concrete_thing_by_ref(receiver_ref)

        if(self.not_has_attr_money(sender)):
            return False
        if(self.not_has_attr_money(receiver)):
            return False
        

        all_money = sender[self.attr_money]
        if(all_money < 0):
            log_error(f"entity {sender_ref} has negative money",__name__, line())
            return False
        
        sender[self.attr_money] = 0

        receiver[self.attr_money] += all_money

        return True

    # tries to transfer money amount, if doesn't have the money required, transfer the rest
    def transfer_money_or_the_rest(self, sender_ref, receiver_ref, amount):
        if(not self.transfer_money_from_to(sender_ref, receiver_ref, amount)):
            if(not self.transfer_all_money(sender_ref, receiver_ref)):
                return False
        return True
        


    # def give_money()
